
import time
import uuid
from statistics import mean

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-73vu33.example.com"
EMAIL = "23f2001158@ds.study.iitm.ac.in"

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# Add required headers to every response
@app.middleware("http")
async def add_custom_headers(request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{max(0.0, elapsed):.6f}"

    return response


# Calculate descriptive statistics
@app.get("/stats")
def get_stats(values: str = Query(...)):
    try:
        numbers = [int(x.strip()) for x in values.split(",")]

        if not numbers:
            return JSONResponse(
                status_code=400,
                content={"error": "values must not be empty"},
            )

        return {
            "email": EMAIL,
            "count": len(numbers),
            "sum": sum(numbers),
            "min": min(numbers),
            "max": max(numbers),
            "mean": mean(numbers),
        }

    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "error": "values must contain comma-separated integers"
            },
        )
