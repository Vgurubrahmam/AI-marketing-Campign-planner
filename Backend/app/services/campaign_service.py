"""
Campaign service: orchestrates the AI generation pipeline.
Runs as a background task (FastAPI BackgroundTasks) and updates
the DB after each section completes so the frontend can poll progress.
"""
import asyncio
import logging

from app.core.config import settings
from app.db.session import async_session
from app.repositories.campaign_repo import CampaignRepository

logger = logging.getLogger(__name__)

# Platform list for ad copy generation
PLATFORMS = ["google", "meta", "linkedin", "instagram"]


async def run_generation_pipeline(campaign_id: str) -> None:
    """
    Run the full AI generation pipeline for a campaign.
    Each section is generated sequentially, and the DB is updated
    after each section completes so the frontend renders section by section.
    """
    async with async_session() as db:
        try:
            repo = CampaignRepository(db)

            # Load campaign data
            campaign = await repo.get_by_id(campaign_id)
            if not campaign:
                logger.error(f"Campaign {campaign_id} not found")
                return

            product = campaign.product_description
            goal = campaign.marketing_goal
            industry = campaign.industry
            budget_amount = float(campaign.budget_amount)

            # ---- Step 1: Generate Personas ----
            try:
                personas_data = await _generate_personas(product, industry, goal)
            except Exception as e:
                logger.warning(f"⚠️ [FALLBACK WARNING] Personas step failed: {e}, falling back to mock generator")
                from app.ai.mock_client import generate_mock_personas
                personas_data = await generate_mock_personas(product, industry, goal)

            await repo.add_personas(campaign_id, personas_data)
            await repo.update_section_status(campaign_id, "persona", "done")
            await db.commit()
            logger.info(f"Campaign {campaign_id}: personas done")

            personas_summary = ", ".join(
                p.get("persona_name", "Target User") for p in personas_data
            )

            # ---- Step 2: Generate Ad Copy ----
            primary_persona = personas_data[0] if personas_data else {}
            try:
                ad_copies = await _generate_ad_copies(product, primary_persona)
            except Exception as e:
                logger.warning(f"⚠️ [FALLBACK WARNING] Ad copy step failed: {e}, falling back to mock generator")
                from app.ai.mock_client import generate_mock_ad_copy
                ad_copies = [
                    {**(await generate_mock_ad_copy(product, primary_persona, p)), "platform": p}
                    for p in PLATFORMS
                ]

            await repo.add_ad_copies(campaign_id, ad_copies)
            await repo.update_section_status(campaign_id, "ad_copy", "done")
            await db.commit()
            logger.info(f"Campaign {campaign_id}: ad_copy done")

            ad_copy_context = " ".join(
                f"{c.get('headline', '')} {c.get('body', '')}" for c in ad_copies
            )

            # ---- Step 3: Generate Keywords ----
            try:
                keywords_data = await _generate_keywords(product, industry, ad_copy_context)
            except Exception as e:
                logger.warning(f"⚠️ [FALLBACK WARNING] Keywords step failed: {e}, falling back to mock generator")
                from app.ai.mock_client import generate_mock_keywords
                keywords_data = await generate_mock_keywords(product, industry)

            await repo.add_keywords(campaign_id, keywords_data)
            await repo.update_section_status(campaign_id, "keywords", "done")
            await db.commit()
            logger.info(f"Campaign {campaign_id}: keywords done")

            # ---- Step 4: Generate Budget ----
            try:
                budget_data = await _generate_budget(goal, industry, budget_amount, personas_summary)
            except Exception as e:
                logger.warning(f"⚠️ [FALLBACK WARNING] Budget step failed: {e}, falling back to mock generator")
                from app.ai.mock_client import generate_mock_budget
                budget_data = await generate_mock_budget(goal, industry, budget_amount)

            await repo.add_budgets(campaign_id, budget_data)
            await repo.update_section_status(campaign_id, "budget", "done")
            await db.commit()
            logger.info(f"Campaign {campaign_id}: budget done")

            # ---- Step 5: Generate Schedule ----
            platforms_used = list(set(c.get("platform", "") for c in ad_copies))
            try:
                schedule_data = await _generate_schedule(product, platforms_used or PLATFORMS, goal, personas_summary)
            except Exception as e:
                logger.warning(f"⚠️ [FALLBACK WARNING] Schedule step failed: {e}, falling back to mock generator")
                from app.ai.mock_client import generate_mock_schedule
                schedule_data = await generate_mock_schedule([], 4)

            await repo.add_publishing_plans(campaign_id, schedule_data)
            await repo.update_section_status(campaign_id, "schedule", "done")
            await db.commit()
            logger.info(f"Campaign {campaign_id}: schedule done")

            # ---- Step 6: Generate Summary ----
            try:
                summary_text = await _generate_summary({
                    "product_description": product,
                    "marketing_goal": goal,
                    "industry": industry,
                    "budget_amount": budget_amount,
                    "personas": personas_data,
                    "ad_copies": ad_copies,
                    "keywords": keywords_data,
                    "budget_allocation": budget_data,
                    "schedule": schedule_data,
                })
            except Exception as e:
                logger.warning(f"⚠️ [FALLBACK WARNING] Summary step failed: {e}, falling back to mock generator")
                from app.ai.mock_client import generate_mock_summary
                summary_text = await generate_mock_summary({"product_description": product, "industry": industry, "marketing_goal": goal, "budget_amount": budget_amount})

            await repo.update_summary(campaign_id, summary_text)
            await repo.update_section_status(campaign_id, "summary", "done")
            await db.commit()
            logger.info(f"Campaign {campaign_id}: summary done")

            # ---- Mark campaign complete ----
            await repo.update_campaign_status(campaign_id, "complete")
            await db.commit()
            logger.info(f"Campaign {campaign_id}: COMPLETE")

        except Exception as e:
            logger.error(f"Campaign {campaign_id} generation pipeline encountered unhandled exception: {e}")
            try:
                # Ensure all section statuses are marked so frontend never hangs indefinitely
                for sec in ["persona", "ad_copy", "keywords", "budget", "schedule", "summary"]:
                    await repo.update_section_status(campaign_id, sec, "done")
                await repo.update_campaign_status(campaign_id, "complete")
                await db.commit()
            except Exception:
                pass


async def regenerate_section(campaign_id: str, section: str) -> None:
    """Regenerate a single section of a campaign."""
    async with async_session() as db:
        try:
            repo = CampaignRepository(db)
            campaign = await repo.get_by_id(campaign_id)
            if not campaign:
                return

            product = campaign.product_description
            goal = campaign.marketing_goal
            industry = campaign.industry
            budget_amount = float(campaign.budget_amount)

            # Clear existing section data
            await repo.clear_section(campaign_id, section)
            await repo.update_section_status(campaign_id, section, "generating")
            await repo.update_campaign_status(campaign_id, "generating")
            await db.commit()

            # Regenerate based on section type
            if section == "persona":
                data = await _generate_personas(product, industry, goal)
                await repo.add_personas(campaign_id, data)
            elif section == "ad_copy":
                persona = (
                    {
                        "persona_name": campaign.personas[0].persona_name,
                        "demographics": campaign.personas[0].demographics,
                        "pain_points": campaign.personas[0].pain_points,
                    }
                    if campaign.personas
                    else {}
                )
                data = await _generate_ad_copies(product, persona)
                await repo.add_ad_copies(campaign_id, data)
            elif section == "keywords":
                data = await _generate_keywords(product, industry)
                await repo.add_keywords(campaign_id, data)
            elif section == "budget":
                personas_summary = ", ".join(
                    p.persona_name for p in campaign.personas
                )
                data = await _generate_budget(goal, industry, budget_amount, personas_summary)
                await repo.add_budgets(campaign_id, data)
            elif section == "schedule":
                platforms = list(set(c.platform for c in campaign.ad_copies))
                data = await _generate_schedule(product, platforms or PLATFORMS, goal)
                await repo.add_publishing_plans(campaign_id, data)
            elif section == "summary":
                summary_text = await _generate_summary({
                    "product_description": product,
                    "marketing_goal": goal,
                    "industry": industry,
                    "budget_amount": budget_amount,
                    "personas": [{"persona_name": p.persona_name} for p in campaign.personas],
                    "ad_copies": [{"headline": c.headline, "platform": c.platform} for c in campaign.ad_copies],
                    "keywords": [{"keyword": k.keyword} for k in campaign.keywords],
                    "budget_allocation": [{"channel": b.channel, "amount": b.amount} for b in campaign.budgets],
                    "schedule": [{"day_offset": s.day_offset, "channel": s.channel} for s in campaign.publishing_plans],
                })
                await repo.update_summary(campaign_id, summary_text)

            await repo.update_section_status(campaign_id, section, "done")
            await repo.update_campaign_status(campaign_id, "complete")
            await db.commit()

        except Exception as e:
            logger.error(f"Section regeneration failed ({section}): {e}")
            try:
                await repo.update_section_status(campaign_id, section, "done")
                await repo.update_campaign_status(campaign_id, "complete")
                await db.commit()
            except Exception:
                pass


# ---- Private helpers that switch between mock and real AI ----


async def _generate_personas(product: str, industry: str, goal: str) -> list[dict]:
    if settings.use_mock_ai:
        from app.ai.mock_client import generate_mock_personas
        return await generate_mock_personas(product, industry, goal)
    else:
        from app.ai.prompts.persona import generate_personas
        return await generate_personas(product, industry, goal)


async def _generate_ad_copies(product: str, persona: dict) -> list[dict]:
    if settings.use_mock_ai:
        from app.ai.mock_client import generate_mock_ad_copy

        results = await asyncio.gather(
            *[generate_mock_ad_copy(product, persona, p) for p in PLATFORMS]
        )
        return [
            {**copy, "platform": platform}
            for copy, platform in zip(results, PLATFORMS)
        ]
    else:
        from app.ai.prompts.adcopy import generate_all_ad_copies
        from app.ai.mock_client import generate_mock_ad_copy

        try:
            copies = await generate_all_ad_copies(product, persona)
            if copies and len(copies) > 0:
                return copies
        except Exception as e:
            logger.warning(f"Batch ad copy generation failed: {e}, using dynamic fallback")

        out_copies = []
        for platform in PLATFORMS:
            fallback = await generate_mock_ad_copy(product, persona, platform)
            out_copies.append({**fallback, "platform": platform})
        return out_copies


async def _generate_keywords(product: str, industry: str, ad_copy_context: str = "") -> list[dict]:
    if settings.use_mock_ai:
        from app.ai.mock_client import generate_mock_keywords
        return await generate_mock_keywords(product)
    else:
        from app.ai.prompts.keywords import generate_keywords
        return await generate_keywords(product, industry, ad_copy_context)


async def _generate_budget(
    goal: str, industry: str, budget_amount: float, personas_summary: str = ""
) -> list[dict]:
    from app.services.budget_rules import compute_budget_allocation

    # Step 1: Deterministic allocation from rules engine
    allocations = compute_budget_allocation(goal, industry, budget_amount)

    if settings.use_mock_ai:
        from app.ai.mock_client import generate_mock_budget
        mock_data = await generate_mock_budget(goal, industry, budget_amount)
        for alloc in allocations:
            alloc["reasoning"] = _get_reasoning_for_channel(alloc["channel"], mock_data)
        return allocations
    else:
        try:
            from app.ai.prompts.budget import generate_budget_reasoning

            reasoning_data = await generate_budget_reasoning(
                goal, industry, budget_amount, allocations, personas_summary
            )
            reasoning_items = reasoning_data if isinstance(reasoning_data, list) else []
            for alloc in allocations:
                alloc["reasoning"] = _get_reasoning_for_channel(alloc["channel"], reasoning_items)
            return allocations
        except Exception as e:
            logger.warning(f"⚠️ [FALLBACK WARNING] Budget reasoning LLM call failed: {e}, using dynamic fallback")
            from app.ai.mock_client import generate_mock_budget
            mock_data = await generate_mock_budget(goal, industry, budget_amount)
            for alloc in allocations:
                alloc["reasoning"] = _get_reasoning_for_channel(alloc["channel"], mock_data)
            return allocations


def _get_reasoning_for_channel(channel: str, reasoning_items: list[dict]) -> str:
    """Find channel reasoning by fuzzy keyword matching instead of positional zip."""
    ch_lower = channel.lower()

    # Exact or substring channel match check
    for item in reasoning_items:
        if isinstance(item, dict):
            item_ch = str(item.get("channel", "")).lower()
            if item_ch == ch_lower or item_ch in ch_lower or ch_lower in item_ch:
                res = item.get("reasoning", "").strip()
                if res:
                    return res

    # Semantic channel keyword match check
    for item in reasoning_items:
        if isinstance(item, dict):
            item_ch = str(item.get("channel", "")).lower()
            if ("email" in ch_lower and "email" in item_ch) or \
               (("content" in ch_lower or "seo" in ch_lower) and ("content" in item_ch or "seo" in item_ch)) or \
               (("google" in ch_lower or "search" in ch_lower) and ("google" in item_ch or "search" in item_ch)) or \
               (("meta" in ch_lower or "facebook" in ch_lower or "instagram" in ch_lower) and ("meta" in item_ch or "social" in item_ch or "facebook" in item_ch)) or \
               ("linkedin" in ch_lower and "linkedin" in item_ch) or \
               (("influencer" in ch_lower or "partner" in ch_lower) and ("influencer" in item_ch or "partner" in item_ch)):
                res = item.get("reasoning", "").strip()
                if res:
                    return res

    # Fallback per channel category
    if "email" in ch_lower:
        return "Automated email welcome series, lead nurturing, and repeat customer incentives to maximize customer LTV."
    elif "content" in ch_lower or "seo" in ch_lower:
        return "Long-term organic search authority and educational content driving sustainable organic traffic."
    elif "google" in ch_lower:
        return "High-intent search ads capturing prospects actively seeking solutions with clear purchase intent."
    elif "meta" in ch_lower or "facebook" in ch_lower or "instagram" in ch_lower:
        return "Visual product creative and targeted social campaigns to build brand awareness and retargeting engagement."
    elif "linkedin" in ch_lower:
        return "Targeting career-minded professionals and affluent consumers with high engagement potential."
    elif "influencer" in ch_lower or "partner" in ch_lower:
        return "Targeted influencer sampling and partner endorsements to build authentic social proof."

    return "Strategic budget allocation focused on high-converting audience reach and ROI."


async def _generate_schedule(
    product: str, platforms: list[str], goal: str, personas_summary: str = ""
) -> list[dict]:
    if settings.use_mock_ai:
        from app.ai.mock_client import generate_mock_schedule
        return await generate_mock_schedule(product, personas_summary, goal)
    else:
        try:
            from app.ai.prompts.schedule import generate_schedule
            data = await generate_schedule(product, platforms, goal, personas_summary)
            if data and isinstance(data, list) and len(data) > 0:
                return data
        except Exception as e:
            logger.warning(f"⚠️ [FALLBACK WARNING] Schedule LLM call failed: {e}, using dynamic fallback")

        from app.ai.mock_client import generate_mock_schedule
        return await generate_mock_schedule(product, personas_summary, goal)


async def _generate_summary(campaign_data: dict) -> str:
    if settings.use_mock_ai:
        from app.ai.mock_client import generate_mock_summary
        return await generate_mock_summary(campaign_data)
    else:
        try:
            from app.ai.prompts.summary import generate_summary
            text = await generate_summary(campaign_data)
            if text and isinstance(text, str) and len(text.strip()) > 0:
                return text
        except Exception as e:
            logger.warning(f"Summary LLM call failed: {e}, using dynamic fallback")

        from app.ai.mock_client import generate_mock_summary
        return await generate_mock_summary(campaign_data)
