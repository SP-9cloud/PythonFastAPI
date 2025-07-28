from fastapi import FastAPI, BackgroundTasks
from app.server.routes.student import router as StudentRouter
from app.server.routes.user import router as UserRouter
from app.server.middleware.logger import log_requests
from app.server.background_tasks.tasks import log_request_time




app = FastAPI()
app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# IMPLEMENT MIDDLEWARE
app.middleware("http")(log_requests)

# IMPLEMENT BACKGROUND LOGGING
@app.get("/add-request-log")
def log_request_task(background_tasks: BackgroundTasks = None):
    background_tasks.add_task(log_request_time)
    return {"message": f"Request logged" }

#if __name__ == "__main__": #this is for DB
#    import uvicorn
#    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)