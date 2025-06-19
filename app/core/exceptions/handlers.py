from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

from .auth import (
    AuthenticationError, 
    InvalidCredentialsError, 
    TokenGenerationError,
    TokenExpiredError,
    RefreshTokenError
)
from .user import (
    UserNotFoundError, 
    UserAlreadyExistsError, 
    UserValidationError,
    UserPermissionError
)

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    """Registrar todos los manejadores globales de excepciones"""
    
    @app.exception_handler(AuthenticationError)
    @app.exception_handler(InvalidCredentialsError)
    async def authentication_exception_handler(request: Request, exc: AuthenticationError):
        logger.warning(f"Authentication error: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": str(exc),
                "type": "authentication_error"
            }
        )
    
    @app.exception_handler(TokenGenerationError)
    async def token_generation_exception_handler(request: Request, exc: TokenGenerationError):
        logger.error(f"Token generation error: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": str(exc),
                "type": "token_generation_error"
            }
        )
    
    @app.exception_handler(TokenExpiredError)
    @app.exception_handler(RefreshTokenError)
    async def token_exception_handler(request: Request, exc: Exception):
        logger.warning(f"Token error: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": str(exc),
                "type": "token_error"
            }
        )
    
    @app.exception_handler(UserNotFoundError)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
        logger.info(f"User not found: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc),
                "type": "user_not_found_error"
            }
        )
    
    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsError):
        logger.info(f"User already exists: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": str(exc),
                "type": "user_already_exists_error"
            }
        )
    
    @app.exception_handler(UserValidationError)
    async def user_validation_exception_handler(request: Request, exc: UserValidationError):
        logger.warning(f"User validation error: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": str(exc),
                "type": "user_validation_error"
            }
        )
    
    @app.exception_handler(UserPermissionError)
    async def user_permission_exception_handler(request: Request, exc: UserPermissionError):
        logger.warning(f"User permission error: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": str(exc),
                "type": "user_permission_error"
            }
        )
    
    # Handle FastAPI validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Error de validación en los datos enviados",
                "errors": exc.errors(),
                "type": "validation_error"
            }
        )
    
    # Handle general HTTP exceptions
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP error {exc.status_code}: {exc.detail} - Path: {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "type": "http_error"
            }
        )
    
    # Handle unexpected errors
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {str(exc)} - Path: {request.url.path}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Error interno del servidor",
                "type": "internal_server_error"
            }
        )