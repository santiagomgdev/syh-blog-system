from .base import DomainException

class AuthenticationError(DomainException):
    """Se lanza cuando falla la autenticación"""
    pass

class InvalidCredentialsError(AuthenticationError):
    """Se lanza cuando las credenciales son inválidas"""
    pass

class TokenGenerationError(DomainException):
    """Se lanza cuando falla la generación del token"""
    pass

class TokenExpiredError(DomainException):
    """Se lanza cuando el token ha expirado"""
    pass

class RefreshTokenError(DomainException):
    """Se lanza cuando fallan las operaciones del refresh token"""
    pass