# api-vinyl

## Arranque local

Entorno comprobado con Python 3.15.2 en macOS. Ejecuta los comandos desde la carpeta `api-vinyl`.

### 1. Instalar las dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --only-binary=watchfiles -r requirements.txt
```

### 2. Configurar SQLite

Crea un archivo `.env` junto a `main.py` y añade esta línea. Si ya tienes ese archivo, comprueba el valor de `DATABASE_URL` antes de continuar.

```dotenv
DATABASE_URL=sqlite:///./vinyl.db
```

Con esa ruta, SQLite guarda la base de datos en `vinyl.db` dentro de `api-vinyl`. Git ignora tanto `.env` como `vinyl.db`.

### 3. Crear las tablas

```bash
python -c "from database.database import Base, engine; from models import artist, genre, vinyl; Base.metadata.create_all(engine)"
```

El comando crea las tablas `artists`, `genres` y `vinyls` si faltan y conserva los registros existentes.

### 4. Arrancar y comprobar la API

```bash
python -m uvicorn main:app --reload
```

Abre [Swagger](http://127.0.0.1:8000/docs). Para comprobar que la API puede leer la base de datos, abre el [listado de vinilos](http://127.0.0.1:8000/vinyls). Con una base recién creada, el listado responde `200` con `[]`.

Para detener el servidor, pulsa `Ctrl+C` en la terminal.
