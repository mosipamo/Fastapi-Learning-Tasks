from fastapi import FastAPI
from responses import (
	welcome_payload,
	health_payload,
	info_payload,
	ping_payload,
	team_payload,
	services_payload,
	stats_payload
)

app = FastAPI()

@app.get("/")
def read_root() -> dict:
    return welcome_payload()

@app.get("/health")
def read_health() -> dict:
    return health_payload()

@app.get("/info")
def read_info() -> dict:
    return info_payload()

@app.get("/ping")
def read_ping() -> dict:
    return ping_payload()

@app.get("/team")
def read_team() -> dict:
    return team_payload()

@app.get("/services")
def read_services() -> list:
    return services_payload()

@app.get("/stats")
def read_stats() -> dict:
    return stats_payload()
