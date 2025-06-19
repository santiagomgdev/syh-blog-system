from .base import DomainException

class UserNotFoundError(DomainException):
    """Se lanza cuando no se encuentra el usuario"""
    pass

class UserAlreadyExistsError(DomainException):
    """Se lanza al intentar crear un usuario que ya existe"""
    pass

class UserValidationError(DomainException):
    """Se lanza cuando falla la validación de los datos del usuario"""
    pass

class UserPermissionError(DomainException):
    """Se lanza cuando el usuario no tiene los permisos requeridos"""
    pass

