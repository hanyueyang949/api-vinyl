from fastapi import FastAPI


from routes.vinyls import router as vinyls_router

app = FastAPI(title="Vinyl API")


app.include_router(vinyls_router)
