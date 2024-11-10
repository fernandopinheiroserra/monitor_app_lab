from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.heartbeat import Heartbeat
from app.database import get_mongo_client
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
from app.initialize_db import initialize_database


app = FastAPI()
templates = Jinja2Templates(directory="templates")

db = initialize_database()

heartbeat_service = Heartbeat(db=db)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ping")
async def receive_ping(
    request: Request,
    empresa: str = Query(..., description="Nome da empresa"),
    sinc: str = Query(..., description="Nome do sincronizador")
):
    try:
        client_host = request.client.host
        print(f"Recebido ping de {client_host} - Empresa: {empresa}, Sinc: {sinc}")

        heartbeat_service.receive_heartbeat(
            source=client_host, 
            empresa=empresa,
            sinc=sinc
        )

        return {
            "message": "Heartbeat received",
            "client": client_host,
            "empresa": empresa,
            "sinc": sinc
        }
    except Exception as e:
        print(f"Erro ao processar ping: {e}")
        return {"error": "Erro interno no servidor"}, 500
    

@app.get("/status")
async def check_status():
    if heartbeat_service.is_heartbeat_missing():
        return {"status": "No heartbeat received in the last minute"}
    return {"status": "Heartbeat active"}

@app.get("/absences")
async def get_absences():
    client = get_mongo_client()
    db = client.get_database("master_alert")
    absences = db.absences.find({})
    return {"absences": list(absences)}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    last_heartbeat = heartbeat_service.last_heartbeat.strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "No heartbeat" if heartbeat_service.is_heartbeat_missing() else "Heartbeat active"
    sources = heartbeat_service.sources
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "last_heartbeat": last_heartbeat,
        "current_time": current_time,
        "status": status,
        "sources": sources
    })


@app.get("/metrics/uptime")
async def get_uptime_metrics():
    client = get_mongo_client()
    db = client.get_database("master_alert")

    period_start = datetime.now() - timedelta(minutes=30)

    pings = db.pings.aggregate([
        {
            "$match": {
                "time": {"$gte": period_start}
            }
        },
        {
            "$group": {
                "_id": {"empresa": "$empresa", "sinc": "$sinc"},
                "last_ping": {"$max": "$time"},
                "total_pings": {"$sum": 1}
            }
        }
    ])

    uptime_metrics = []
    for ping in pings:
        empresa = ping["_id"]["empresa"]
        sinc = ping["_id"]["sinc"]
        last_ping = ping["last_ping"]
        
        is_active = (datetime.now() - last_ping) <= timedelta(minutes=1)
        
        uptime_metrics.append({
            "empresa": empresa,
            "sinc": sinc,
            "last_ping": last_ping,
            "is_active": is_active,
            "total_pings": ping["total_pings"]
        })

    return JSONResponse(content=uptime_metrics)

@app.get("/metrics/uptime_history")
async def get_uptime_history():
    client = get_mongo_client()
    db = client.get_database("master_alert")

    period_start = datetime.now() - timedelta(days=7)

    history_data = db.pings.aggregate([
        {"$match": {"time": {"$gte": period_start}}},
        {"$project": {"day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$time"}}, "app_name": 1}},
        {"$group": {"_id": {"day": "$day", "app_name": "$app_name"}, "pings": {"$sum": 1}}},
        {"$sort": {"_id.day": 1}}
    ])

    uptime_history = {}
    for record in history_data:
        if "app_name" in record["_id"]:
            app_name = record["_id"]["app_name"]
            day = record["_id"]["day"]
            
            if app_name not in uptime_history:
                uptime_history[app_name] = {}
            uptime_history[app_name][day] = record["pings"]

    return JSONResponse(content=uptime_history)

@app.get("/metrics/uptime_percentage")
async def get_uptime_percentage():
    client = get_mongo_client()
    db = client.get_database("master_alert")

    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_minutes = (datetime.now() - month_start).total_seconds() / 60

    uptime_data = db.pings.aggregate([
        {"$match": {"time": {"$gte": month_start}}},
        {"$group": {"_id": "$app_name", "active_minutes": {"$sum": 1}}}
    ])

    uptime_percentage = [
        {
            "app_name": u["_id"],
            "uptime_percent": (u["active_minutes"] / total_minutes) * 100
        } for u in uptime_data
    ]
    return JSONResponse(content=uptime_percentage)