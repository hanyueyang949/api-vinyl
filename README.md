# api-vinyl

## Arranque local

Entorno comprobado con Python 3.15.2 en macOS. Desde la carpeta del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --only-binary=watchfiles -r requirements.txt
python -m uvicorn main:app --reload
```

Con el servidor en marcha, abre [Swagger](http://127.0.0.1:8000/docs).
Para detener el servidor, pulsa `Ctrl+C` en la terminal.