from fastapi import FastAPI

from routes.artists import router as artists_router

from routes.genres import router as genres_router

app = FastAPI(title="Vinyl API")
app.include_router(artists_router)

app.include_router(genres_router)