from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware configuration. Allow us to be able to get pass CORS errors
# when we try to access the API from the frontend. THIS MAY COME FROM OUR NEXTJS APP
# Note: The frontend is running on localhost3000
# Note: The backend is running on localhost8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return "Health Check Complete"