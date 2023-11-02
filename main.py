# main.py
import uvicorn
from contact import router
from customer import customer_router
from interactions.interactions import interact_router
from deals.deal import deal_router
from fastapi import FastAPI, Depends, Request,HTTPException, WebSocket
from app.database import engine
from app import models
#from fastapi_jwt_auth import AuthJWT
from app.schema import Settings
from fastapi.middleware.cors import CORSMiddleware
from localization.localization import get_gettext
from prometheus_fastapi_instrumentator import Instrumentator, metrics
# from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter, WebSocketRateLimiter
import redis.asyncio as redis
from walrus import Database, RateLimitException
from fastapi.responses import JSONResponse
app = FastAPI()

# @AuthJWT.load_config
# def get_config():
#     return Settings 


# Define CORS settings
origins = ["http://localhost", "http://localhost:8080", "http://localhost:8000"]
# Replace the above origins with the actual domains you want to allow.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = Database()
rate = db.rate_limit('xxx', limit=5, per=60)  # in 60s just can only click 5 times
@app.exception_handler(RateLimitException)
def parse_rate_litmit_exception(request: Request, exc: RateLimitException):
    msg = {'success': False, 'msg': f'please have a tea for sleep, your ip is: {request.client.host}.'}
    return JSONResponse(status_code=429, content=msg)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def index():
    return {'success': True}
@app.get('/crm_api')
@rate.rate_limited(lambda request: request.client.host)
def query_important_data(request: Request):
    data = 'important data'
    return {'success': True, 'data': data}


#     return {"message": "Welcome to your CRM API"}
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     ratelimit = WebSocketRateLimiter(times=1, seconds=5)
#     while True:
#         try:
#             data = await websocket.receive_text()
#             await ratelimit(websocket, context_key=data)  # NB: context_key is optional
#             await websocket.send_text("Hello, welcome to your CRM API")
#         except HTTPException:
#             await websocket.send_text("Hello again")

def get_user_language(request: Request):
    # Determine the user's language based on their profile settings or request headers.
    user_language = "en_US"  
    return user_language

@app.middleware("http")
async def set_user_language(request: Request, call_next):
    user_language = get_user_language(request)
    gettext = get_gettext("customer", "path_to_locales", user_language)
    request.state.locale = gettext
    response = await call_next(request)
    return response

# Instrument  FastAPI application
Instrumentator().instrument(app)

app.include_router(router,)
app.include_router(customer_router,)
app.include_router(interact_router,)
app.include_router(deal_router,)


if __name__ == "__main__":
    
    uvicorn.run("main:app", port=9000, reload=True)