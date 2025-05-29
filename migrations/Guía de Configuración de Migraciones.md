## Tabla de Contenido

- [Initial Setup](https://claude.ai/chat/15a43565-f7af-4719-ab0d-3d7a0a839242#initial-setup)
- [Basic Operations](https://claude.ai/chat/15a43565-f7af-4719-ab0d-3d7a0a839242#basic-operations)
- [Working with SQLModel](https://claude.ai/chat/15a43565-f7af-4719-ab0d-3d7a0a839242#working-with-sqlmodel)
- [Common Migration Scenarios](https://claude.ai/chat/15a43565-f7af-4719-ab0d-3d7a0a839242#common-migration-scenarios)
- [Advanced Migration Techniques](https://claude.ai/chat/15a43565-f7af-4719-ab0d-3d7a0a839242#advanced-migration-techniques)
- [Troubleshooting](https://claude.ai/chat/15a43565-f7af-4719-ab0d-3d7a0a839242#troubleshooting)
- [Best Practices](https://claude.ai/chat/15a43565-f7af-4719-ab0d-3d7a0a839242#best-practices)

## Configuración Inicial

### Instalación de Alembic

```bash
pip install alembic
```

### Inicialización de Alembic

```bash
# Navigate to your project root directory
cd your-project-root
alembic init migrations
```

Esto crea un directorio llamado `migrations` with the following structure:

```
migrations/
├── README
├── env.py
├── script.py.mako
└── versions/
```

### Configuración de Alembic con SQLModel

Actualizamos el archivo `migrations/env.py` para integrarlo con los modelos de SQLModel:

```python
# migrations/env.py
import os # -- Añadir dependencia
import sys # -- Añadir dependencia
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlmodel import SQLModel # -- Añadir dependencia

# ------------------ Bloque Añadido ------------------ #
# Add the parent directory to sys.path to allow imports from your project
# Esta linea es necesaria ya que permite a Alembic importar los módulos y modelos del proyecto correctamente; esto se debe a que Alembic ejecuta env.py en su propia ruta migrations/, pero las importaciones de los módulo se encuentran fuera del directorio
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importa todos los modelos para asegurar que están registrados con los metadatos de SQLModel
from database.models.common.pais import Pais
from database.models.common.departamento import Departamento
from database.models.common.municipio import Municipio
# Importa otros modelos existentes...

# ------------------ Fin Bloque ------------------ #

# This is the Alembic Config object
config = context.config

# ------------------ Bloque Añadido ------------------ #
# Establece sqlalchemy.url con la URL de la base de datos desde variables de entorno
from dotenv import load_dotenv
load_dotenv()

config.set_main_option("sqlalchemy.url", os.getenv("SQLITE_DATABASE_URL"))
# ------------------ Fin Bloque ------------------ #

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------ Bloque Modificado ------------------ #
# Establece objeto metadata de Alembic para detectar cambios en los modelos
target_metadata = SQLModel.metadata
# ------------------ Fin Bloque ------------------ #

# El resto del código sigue intacto...
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # ... (existing code)

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # ... (existing code)
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives  # Add this line
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Actualiza script.py.mako para incluir import de SQLModel

Editar el archivo `migrations/script.py.mako`:

```python
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # Añadir linea

${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}
```

## Operaciones Básicas

### Crear la migración inicial

```bash
alembic revision --autogenerate -m "Create initial tables"
```

### Aplicar Migraciones

```bash
# Aplicar las migraciones pendientes
alembic upgrade head
```

### Rollback a Migraciones

```bash
# Se devuelve a una migración anterior
alembic downgrade -1

# Se devuelve a una versión especifica de las migraciones
alembic downgrade <revision_id>

# Se devuelve a la migración inicial
alembic downgrade base
```

### Visualiza Información de Migración

```bash
# Muestra la versión actual de migración
alembic current

# Muestra historial de migraciones
alembic history

# Muestra historial de migraciones con detalles
alembic history -v
```

## Uso con SQLModel

### Ejemplo: Modelo SQLModel Pais

```python
# database/models/common/pais.py
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from database.models.common.departamento import Departamento

class Pais(SQLModel, table=True):
    __tablename__ = "paises"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    codigo: str = Field(max_length=2, unique=True)
    
    departamentos: List["Departamento"] = Relationship(back_populates="pais")
```

### Añade nuevo campo a modelo existente

1. Añade el campo:

```python
descripcion: Optional[str] = Field(default=None, description="Descripción del país")
```

2. Genera y aplica la migración:

```bash
alembic revision --autogenerate -m "Add descripcion field to Pais"
alembic upgrade head
```

### Creando un nuevo modelo

1. Crea el archivo modelo
2. Importa en `env.py`
3. Genera y aplica la migración:

```bash
alembic revision --autogenerate -m "Add new model"
alembic upgrade head
```

### Solución al Error "sqlmodel not defined"

Si encuentras un error que dice "sqlmodel is not defined" en tu migración:

1. Opción 1: Agrega la importación al archivo de migración:

```python
import sqlmodel
```

2. Opción 2: Actualiza tu archivo `env.py` como se mostró en la sección de configuración inicial
3. Opción 3: Usa los tipos de SQLAlchemy en su lugar:

```python
op.add_column('paises', sa.Column('descripcion', sa.String(), nullable=True))
```

## Escenarios Comunes de Migración

### Ejecutar Migraciones con el Servidor Apagado (Recomendado)

Para entornos de producción, es más seguro ejecutar migraciones con el servidor apagado:

1. Detener el servidor

```bash
# Si se ejecuta con uvicorn directamente
Ctrl+C

# O si se ejecuta como un servicio
sudo systemctl stop myapp
```

2. Aplicar migraciones

```bash
alembic upgrade head
```

3. Iniciar el servidor

```bash
# Con uvicorn
uvicorn main:app --reload

# O como un servicio
sudo systemctl start myapp
```

### Integración con FastAPI para Desarrollo

```python
# main.py
from fastapi import FastAPI
import os
import alembic.config

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Para desarrollo, ejecutar migraciones automáticamente
    if os.getenv("ENVIRONMENT", "development") == "development":
        try:
            alembic_args = [
                '--raiseerr',
                'upgrade', 'head',
            ]
            alembic.config.main(argv=alembic_args)
        except Exception as e:
            print(f"Error al ejecutar migraciones: {e}")
```

## Técnicas Avanzadas de Migración

### Cambios de Tipo de Columna

Cuando se cambia el tipo de una columna (por ejemplo, de texto a entero), es posible que necesites:

1. Crear una migración personalizada con conversión explícita de tipo:

```python
def upgrade():
    # Crear columna temporal
    op.add_column('table', sa.Column('new_col', sa.Integer()))
    
    # Copiar datos con conversión
    op.execute("UPDATE table SET new_col = CAST(old_col AS INTEGER)")
    
    # Eliminar columna antigua y renombrar la nueva
    op.drop_column('table', 'old_col')
    op.alter_column('table', 'new_col', new_column_name='old_col')
```

### Migraciones de Datos

Para transformar datos durante una migración:

```python
def upgrade():
    # Agregar la columna
    op.add_column('paises', sa.Column('upper_code', sa.String(2)))
    
    # Obtener conexión a la base de datos
    connection = op.get_bind()
    
    # Actualizar datos
    connection.execute(
        sa.text("UPDATE paises SET upper_code = UPPER(codigo)")
    )
```

### Procesamiento por Lotes para Tablas Grandes

Para tablas con millones de filas, usa procesamiento por lotes:

```python
def upgrade():
    connection = op.get_bind()
    
    # Procesar en lotes de 10,000
    offset = 0
    batch_size = 10000
    
    while True:
        # Obtener lote
        results = connection.execute(
            sa.text(f"SELECT id, value FROM table LIMIT {batch_size} OFFSET {offset}")
        ).fetchall()
        
        if not results:
            break
            
        # Procesar lote
        for row in results:
            # Procesar cada fila
            connection.execute(
                sa.text("UPDATE table SET processed = 1 WHERE id = :id"),
                {"id": row.id}
            )
            
        offset += batch_size
```

## Solución de Problemas

### Problemas Comunes y Soluciones

1. **"sqlmodel is not defined"**: Agrega `import sqlmodel` al archivo de migración o actualiza `env.py` como se mostró anteriormente.
    
2. **Modelos no detectados**: Asegúrate de que los modelos estén importados en `env.py` y tengan `table=True`.
    
3. **Migraciones autogeneradas están vacías**: Verifica que:
    
    - Los modelos estén correctamente importados en `env.py`
    - `target_metadata = SQLModel.metadata` esté configurado
    - Los modelos tengan `table=True`
4. **"La base de datos de destino no está actualizada"**: Usa `alembic stamp head` para marcar el estado actual de la base de datos como actualizado.
    
5. **Errores de importación circular**: Usa `TYPE_CHECKING` para importar modelos relacionados:
    
    ```python
    from typing import TYPE_CHECKING
    
    if TYPE_CHECKING:
        from .other_model import OtherModel
    ```
    

## Mejores Prácticas

1. **Control de Versiones**: Siempre incluye los archivos de migración en el control de versiones
2. **Probar Migraciones**: Prueba todas las migraciones en un entorno de pruebas antes de producción
3. **Respaldar Primero**: Siempre haz una copia de seguridad de la base de datos antes de ejecutar migraciones en producción
4. **Un Cambio Por Migración**: Mantén las migraciones enfocadas en un solo cambio lógico
5. **Nombres Descriptivos**: Usa nombres claros y descriptivos para las migraciones
6. **Documentación**: Documenta migraciones complejas, especialmente aquellas con transformaciones de datos
7. **Nunca Edites Migraciones Aplicadas**: Una vez que una migración se aplica en producción, nunca la edites; crea una nueva migración en su lugar
8. **Revisión Offline**: Para cambios críticos, genera SQL con `alembic upgrade head --sql` para revisión antes de aplicar

## Hoja de Referencia de Flujo de Trabajo de Migración

### Flujo de Trabajo de Desarrollo

1. Realiza cambios en tus modelos
2. Genera migración: `alembic revision --autogenerate -m "Descripción"`
3. Revisa la migración generada
4. Aplica migración: `alembic upgrade head`
5. Prueba los cambios

### Flujo de Trabajo de Producción

1. Prueba migraciones en entorno de staging
2. Respalda la base de datos de producción
3. Programa una ventana de mantenimiento
4. Detén la aplicación
5. Aplica migraciones: `alembic upgrade head`
6. Inicia la aplicación
7. Verifica que la aplicación esté funcionando correctamente
