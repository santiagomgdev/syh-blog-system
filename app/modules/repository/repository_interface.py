from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Type

# Crea un tipo genérico T para las entidades del repositorio
T = TypeVar('T')

class RepositoryInterface(Generic[T], ABC):
    """
    Interface para las implementaciones de repositorio.
    Define las operaciones estandar que se deben realizar sobre un modelo.
    """
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene todos los registros con paginación"""
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> T:
        """Obtiene un registro por ID"""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Crea un nuevo registro"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Actualiza un registro existente"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Elimina un registro por ID"""
        pass