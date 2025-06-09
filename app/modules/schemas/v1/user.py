from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre_usuario: str
    correo: str

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(BaseModel):
    id: int

    class Config:
        from_attributes = True
        # Enable ORM mode to allow Pydantic to work with ORM models
        # orm_mode = True
        # allow_population_by_field_name = True
        # use_enum_values = True
        # arbitrary_types_allowed = True
        # json_encoders = {
        #     # Add custom encoders if needed
        # }