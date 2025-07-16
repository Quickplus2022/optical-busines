from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BizPlanner SaaS API", version="0.1.0")

# CORS configuration — libere origens conforme necessário
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def health_check():
    """Endpoint de verificação de vida da API."""
    return {"status": "ok"}