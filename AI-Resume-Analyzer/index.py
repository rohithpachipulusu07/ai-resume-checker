from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="My FastAPI App",
    description="A modern FastAPI application deployed on Vercel",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI on Vercel!",
        "endpoints": {
            "health": "/health",
            "hello": "/hello?name=World"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/hello")
async def hello(name: str = "World"):
    """Simple hello endpoint with a name parameter"""
    return {"message": f"Hello, {name}!"}

@app.post("/items")
async def create_item(item: dict):
    """Create a new item"""
    return {"item": item, "status": "created"}
