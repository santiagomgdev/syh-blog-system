## Paso 1: Instalar Python

1. Ve al sitio web oficial de Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Haz clic en el botón "Download Python" (se recomienda la versión estable más reciente).
3. Ejecuta el instalador una vez descargado.
4. **Importante**: Marca la casilla que dice "Add Python to PATH" durante la instalación.
5. Completa la instalación.

## Paso 2: Instalar Visual Studio Code

1. Descarga VS Code desde: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Ejecuta el instalador y sigue las instrucciones.
3. Completa la instalación.

## Paso 3: Instalar la extensión de Python para VS Code

1. Abre VS Code.
2. Ve a la sección de Extensiones (ícono en la barra lateral izquierda o presiona Ctrl+Shift+X).
3. Busca "Python".
4. Instala la extensión oficial de Python desarrollada por Microsoft.

## Paso 4: Crear un proyecto y entorno virtual

Abre Git Bash y ejecuta:

```bash
# Crea el directorio para el proyecto
mkdir fastapi-project
cd fastapi-project

# Crea un entorno virual
python -m venv venv

# Activa el entorno virtual en Git bash
# Deberías ver `(venv)` al comienzo de tu línea de comandos, lo que indica que el entorno virtual está activo.
source venv/Scripts/activate

# Activa el entorno virtual en Git bash (Alternativa)
. venv/Scripts/activate
```

Para Windows Powershell:

```shell
# Crea el directorio para el proyecto
mkdir fastapi-project
cd fastapi-project

# Crea un entorno virual
python -m venv venv

# Activa el entorno virtual en Windows Powershell
# Deberías ver `(venv)` al comienzo de tu línea de comandos, lo que indica que el entorno virtual está activo.
.\venv\Scripts\activate

# Activa el entorno virtual en Simbolo del sistema (CMD)
venv\Scripts\activate
```

## Paso 5: Instalar FastAPI y dependencias

Con el entorno virtual activado, instala FastAPI:

```bash
# Instala FastAPI y Uvicorn (servidor ASGI)
pip install fastapi uvicorn

# Opcional: Instala todas las dependencias comunes de FastAPI
pip install "fastapi[all]"
```

## Paso 6: Crear una app de prueba con FastAPI

En VSCode, crea un nuevo archivo llamado `main.py` y agrega el siguiente código:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

## Paso 7: Ejecutar tu app de FastAPI

En Git Bash, con el entorno virtual activado:

```bash
uvicorn main:app --reload
```

Visita [http://127.0.0.1:8000](http://127.0.0.1:8000) en tu navegador para ver tu API funcionando.

También puedes revisar la documentación interactiva automática en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
## Notas Adicionales

### Explicación del Entorno Virtual

`python -m venv venv` crea un entorno virtual:

- Es una instalación aislada de Python específica para tu proyecto.
- Ayuda a manejar dependencias sin afectar tu instalación global de Python.
- El primer `venv` es el nombre del módulo, el segundo `venv` es el nombre de la carpeta del entorno.

### Activar/Desactivar el Entorno Virtual

- Para activar en Git Bash: `source venv/Scripts/activate`
- Para desactivar: simplemente escribe `deactivate`

### Guardar Dependencias

Después de instalar paquetes, es buena práctica guardar tus dependencias:

```bash
pip freeze > requirements.txt
```

Esto crea un archivo que puede usarse luego para recrear el entorno:

```bash
pip install -r requirements.txt
```