from fastapi import FastAPI
from core.startup import setup_app

app = FastAPI()

setup_app(app)