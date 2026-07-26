# 🚀 AI Marketing Campaign Planner

> **An automated, data-grounded AI campaign planner that transforms product descriptions, goals, and budget constraints into full-funnel marketing strategies in seconds.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://ai-marketing-campign-planner.vercel.app)
[![Backend API](https://img.shields.io/badge/Backend%20API-Render-00B5AD?style=for-the-badge&logo=render)](https://campaign-ai-backend-2i65.onrender.com)
[![API Docs](https://img.shields.io/badge/Swagger%20Docs-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://campaign-ai-backend-2i65.onrender.com/docs)
[![Database](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com)

---

## 🌟 Overview

The **AI Marketing Campaign Planner** is an enterprise-grade web application built to eliminate hours of manual marketing strategy work. By combining **FastAPI**, **Groq Llama 3.1 LLM**, **Deterministic Rules Engines**, and a **Modern React Dashboard**, it generates hyper-personalized, domain-accurate marketing strategies tailored to any industry or product type.

---

## 🧠 Key Features & Architectural Innovations

### 1. 👥 Audience Personas
- Generates **3 distinct, well-grounded buyer personas** complete with demographic profiles, pain points, preferred channels, and positioning angles.
- Enforces strict currency consistency (`₹` INR) for income levels across all regions and industries.

### 2. 🎯 Platform-Specific Ad Copy
- Produces high-converting ad copy for **Google Search, Meta Ads (Facebook/Instagram), LinkedIn, and Instagram**.
- Respects strict platform character limits and incorporates direct product value propositions.

### 3. 🔍 Domain-Grounded Keywords
- Uses domain-noun extraction to generate SEO & PPC keyword lists with intent metrics (`transactional`, `informational`, `navigational`) and relevance scores.
- Prohibits generic SaaS/software fallback noise for physical, B2C, or e-commerce products.

### 4. 📊 Deterministic Budget Allocation Engine
- **Zero-Hallucination Financial Math**: Computes exact percentage allocations and rupee amounts using a rule-based mathematical matrix (`compute_budget_allocation`) based on campaign goal and industry.
- Pairs allocations with LLM-generated strategic reasoning via semantic channel matching (`_get_reasoning_for_channel`), preventing channel swaps.

### 5. 📅 28-Day Publishing Schedule
- Delivers a structured, 3-phase execution roadmap (**Launch → Optimize → Scale**).
- Contextually targets the current campaign's actual product description and buyer personas with zero cross-contamination.

### 6. 📝 Dynamic Executive Campaign Summary
- Synthesizes a bespoke 3-paragraph executive narrative drawing directly from the generated personas, top budget channels, keyword targets, and 28-day roadmap.
- Employs dynamic phrasing variation so no two campaign summaries feature identical connective structures.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 + Vite + TypeScript
- **Styling**: Modern CSS variables (Glassmorphism, dark/light theme tokens, responsive grid)
- **Charts & Visualization**: Recharts (Pie charts & interactive budget breakdowns)
- **Icons**: Lucide React
- **Notifications**: Sonner

### Backend
- **Framework**: FastAPI (Async Python 3.11+)
- **LLM Engine**: Groq API (`llama-3.1-8b-instant`) with batched prompt optimization
- **Database ORM**: SQLAlchemy 2.0 (Async Engine) + AsyncPG
- **Database**: Supabase PostgreSQL (Port 6543 PgBouncer transaction pooler)
- **Security**: JWT Authentication + Password Hashing (bcrypt)

---

## 📁 Repository Structure

```text
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── prompts/          # Optimized LLM prompt templates (personas, adcopy, keywords, budget, schedule, summary)
│   │   │   ├── llm_client.py     # Groq API client with batched execution
│   │   │   └── mock_client.py    # Dynamic fallback mock generator
│   │   ├── core/                 # App configuration & JWT security
│   │   ├── db/                   # Supabase database session & engine setup
│   │   ├── models/               # SQLAlchemy models (User, Campaign, Personas, Budgets, etc.)
│   │   ├── schemas/              # Pydantic data validation schemas
│   │   ├── services/
│   │   │   ├── budget_rules.py   # Deterministic budget allocation rules engine
│   │   │   └── campaign_service.py # Core generation pipeline & isolation orchestrator
│   │   └── main.py               # FastAPI application entry point
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── components/           # Reusable UI components
    │   ├── pages/                # Dashboard, Campaign Create, Campaign Detail
    │   ├── services/             # Axios API client
    │   └── hooks/                # React Query data fetching hooks
    ├── package.json
    └── vite.config.ts
```

---

## ⚡ Quick Start & Local Setup

### Prerequisites
- **Python**: 3.11 or higher
- **Node.js**: v18 or higher
- **Groq API Key**: (Optional for live LLM mode)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat <<EOT > .env
DATABASE_URL=sqlite+aiosqlite:///./campaign_planner.db
JWT_SECRET=hackathon-secret-key-2025
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
USE_MOCK_AI=false
CORS_ORIGINS=http://localhost:5173
EOT

# Start backend server
uvicorn app.main:app --reload --port 8000
```

The backend server will run at `http://localhost:8000`. Swagger API documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend application will be live at `http://localhost:5173`.

---

## 🔗 Main API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new user account |
| `POST` | `/api/auth/login` | Authenticate user & return JWT token |
| `POST` | `/api/campaigns/generate` | Trigger async multi-section campaign generation pipeline |
| `GET` | `/api/campaigns/{id}` | Retrieve complete campaign details & section outputs |
| `GET` | `/api/campaigns/{id}/status` | Polling endpoint for real-time section generation progress |
| `POST` | `/api/campaigns/{id}/regenerate/{section}` | Regenerate a specific section (e.g. `persona`, `ad_copy`) |

---

## 🌐 Live Deployments

- **Frontend Application**: [https://ai-marketing-campign-planner.vercel.app](https://ai-marketing-campign-planner.vercel.app)
- **Backend API Service**: [https://campaign-ai-backend-2i65.onrender.com](https://campaign-ai-backend-2i65.onrender.com)
- **Interactive Swagger Docs**: [https://campaign-ai-backend-2i65.onrender.com/docs](https://campaign-ai-backend-2i65.onrender.com/docs)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
