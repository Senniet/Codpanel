async function updateStatus() {

    const response = await fetch("/api/v1/server/status");

    const data = await response.json();

    document.getElementById("serverName").innerText =
        data.name ?? "COD Server";

    document.getElementById("status").innerText =
        data.online ? "?? Online" : "?? Offline";

    document.getElementById("pid").innerText =
        data.pid ?? "-";

    document.getElementById("cpu").innerText =
        data.cpu_percent + " %";

    document.getElementById("ram").innerText =
        data.memory_mb + " MB";

    document.getElementById("uptime").innerText =
        data.uptime;
}


async function serverStart(){

    await fetch("/api/v1/server/start",{
        method:"POST"
    });

    setTimeout(updateStatus,1000);

}


async function serverStop(){

    await fetch("/api/v1/server/stop",{
        method:"POST"
    });

    setTimeout(updateStatus,1000);

}


async function serverRestart(){

    await fetch("/api/v1/server/restart",{
        method:"POST"
    });

    setTimeout(updateStatus,1500);

}


updateStatus();
const badge = document.getElementById("serverBadge");

if(data.online){

    badge.innerText = "?? Online";
    badge.className = "badge online";

}else{

    badge.innerText = "?? Offline";
    badge.className = "badge offline";

}
setInterval(updateStatus,1000);