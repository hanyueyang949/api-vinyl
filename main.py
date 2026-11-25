from fastapi import FastAPI

from routes.artists import router as artists_router
from routes.genres import router as genres_router
from routes.vinyls import router as vinyls_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Vinyl API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)
app.include_router(artists_router)
app.include_router(genres_router)
app.include_router(vinyls_router)
