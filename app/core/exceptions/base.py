class DomainException(Exception):
    """Excepción base para todos los errores relacionados con el dominio"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)