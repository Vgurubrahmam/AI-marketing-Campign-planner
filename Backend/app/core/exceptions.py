from fastapi import HTTPException, status


class AppError(HTTPException):
    """Base application error with structured error response."""

    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(
            status_code=status_code,
            detail={"error": {"code": code, "message": message}},
        )


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Invalid or expired authentication token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenError(AppError):
    def __init__(self, message: str = "You don't have permission to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message,
        )


class NotFoundError(AppError):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=f"{resource} not found",
        )


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            message=message,
        )


class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
        )


class AIGenerationError(AppError):
    def __init__(self, section: str = "unknown", message: str = "AI generation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="AI_GENERATION_ERROR",
            message=f"AI generation failed for section '{section}': {message}",
        )
