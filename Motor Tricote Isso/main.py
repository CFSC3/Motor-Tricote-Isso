from fastapi import FastAPI
from router import router

app = FastAPI(title="Motor Tricote Isso")
app.include_router(router)