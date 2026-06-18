from fastapi import APIRouter
import psutil
import datetime

router = APIRouter(
    prefix="/system",
    tags=["System Monitoring"]
)
@router.get("/stats")
def get_system_stats():

    #CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(logical=True)

    #RAM
    ram = psutil.virtual_memory()

    #Umrechnung in GB
    total_gb = ram.total / (1024 ** 3)
    used_gb = ram.used / (1024 ** 3)
    available_gb = ram.available / (1024 ** 3)

    #Uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time

    return {
        "status": "online",
        "uptime": str(uptime).split(".")[0], #schneidet Millisekunden ab
        "cpu": {
            "usage_percent": cpu_usage,
            "cores": cpu_cores
        },
        "ram": {
            "total_gb": round(total_gb, 2),
            "used_gb": round(used_gb, 2),
            "available_gb": round(available_gb, 2),
            "usage_percent": ram.percent
        }
    }