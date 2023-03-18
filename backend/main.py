import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from starlette.middleware.sessions import SessionMiddleware

from api.database import database
from api.database.database import engine
from api.payment_gte import server
from api.routes import company, auth, user, newsletter
from api.scripts.ranking import run_process_scripts

load_dotenv()


database.Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost:3000",
    "https://shopit.aybims.app"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv('SECRET_KEY')
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth.router, prefix='/auth')
app.include_router(user.router, prefix='/user')
app.include_router(company.router)
app.include_router(newsletter.router)
app.include_router(server.router)


async def update_script_task():
    print('Running update script...')
    await run_process_scripts()




@app.get('/')
async def get_root():
    return {
        "message": "ShopIt API v1",
    }




if __name__ == "__main__":
    uvicorn.run("main:app", port=int(os.getenv('BACKEND_PORT')), reload=True)
