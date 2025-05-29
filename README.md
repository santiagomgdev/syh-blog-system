# Plantilla FastAPI Python

## Configuracion de la plantilla para usarse en git

### Paso 1: Hacer un fork a este repositorio 

desde tu cuenta de github hacer un fork a este repositorio para que se cree en el proyecto syh-python-template en el dasborad

### Paso 2: Hacer el repositorio una plantilla

En el repositorio local ingresa a settings, activa la casilla Template repository  para hacer ese repositorio una plantilla

## Paso 3: Crear un nuevo repositorio apartir de esta plantilla

Ahora pára crear un repositorio nuevo apartir de esta plantilla, en la pestaña crear repositorio nuevo despliega las opciones de repository template
seleciona el template que se acabo de crear

## Configuracion del Proyecto 

## Paso 1: Configuración Inicial

Abre Git Bash y ejecuta:

```bash
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

## Paso 2: Instalar dependencias

Con el entorno virtual activado:

```bash
# instala dependencias
pip install -r requirements.txt
```

## Paso 7: Ejecutar tu app de FastAPI

En Git Bash, con el entorno virtual activado:

```bash
uvicorn main:app --reload
```

Visita [http://127.0.0.1:8000](http://127.0.0.1:8000) en tu navegador para ver tu API funcionando.

También puedes revisar la documentación interactiva automática en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
