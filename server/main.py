from fastapi import FastAPI
import uvicorn
from db.base import database
from endpoints.users import router
from endpoints.matches import router as match_router



app = FastAPI(title='Scopegg')
app.include_router(router, tags=["User"], prefix="/user")
app.include_router(match_router, tags=['Match'], prefix='/match')


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)