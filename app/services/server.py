from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.services.server_service import ServerService

router = APIRouter(prefix="/server", tags=["Server"])


@router.get("/status")
async def status():
    return ServerService.status()


@router.get("/widget", response_class=HTMLResponse)
async def widget():

    server = ServerService.status()

    if not server["online"]:
        return """
<div class="card offline">
<h2>?? Server Offline</h2>
</div>
"""

    return f"""
<div class="card online">

<h2>?? {server["name"]}</h2>

<table>

<tr>
<td><b>PID</b></td>
<td>{server["pid"]}</td>
</tr>

<tr>
<td><b>CPU</b></td>
<td>{server["cpu_percent"]:.1f}%</td>
</tr>

<tr>
<td><b>RAM</b></td>
<td>{server["memory_mb"]} MB</td>
</tr>

<tr>
<td><b>Status</b></td>
<td>{server["status"]}</td>
</tr>

<tr>
<td><b>Uptime</b></td>
<td>{server["uptime"]}</td>
</tr>

</table>

</div>
"""