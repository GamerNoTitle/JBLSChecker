from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
import uuid
import string
import random
import xml.etree.ElementTree as ET

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

ascii_list = list(string.ascii_letters + string.digits)
DESKTOP_NAME = "DESKTOP-" + "".join(random.sample(ascii_list, 7)).upper()
MACHINE_ID = uuid.uuid4()
USERNAME = "".join(random.sample(ascii_list, 7)).upper()
VERSION = 2024100
BUILD_NUMBER = "2024.1.4+Build+CL-241.18034.45"

# Configure static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Parse xml response
def get_xml_data(server: str, ticket_path: str):
    client = httpx.Client(verify=False)
    try:
        response = client.get(server + ticket_path, timeout=3)  # timeout 3 sec
        response.raise_for_status()  # check status
        root = ET.fromstring(response.text)

        return {
            "action": root.find("action").text,
            "confirmation_stamp": root.find("confirmationStamp").text,
            "lease_signature": root.find("leaseSignature").text,
            "response_code": root.find("responseCode").text,
            "salt": root.find("salt").text,
            "server_lease": root.find("serverLease").text,
            "server_uid": root.find("serverUid").text,
            "validation_deadline_period": root.find("validationDeadlinePeriod").text,
            "validation_period": root.find("validationPeriod").text,
            "message": root.find("message").text,
        }
    except httpx.ReadTimeout:
        return {"error": "Timeout: Please try again later."}
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}. It seems that this server is not avaliable or you can try again later."
        }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/fetch", response_class=HTMLResponse)
async def fetch_data(request: Request, server: str = Form(...)):
    RELEASE_TICKET_PATH = f"/rpc/releaseTicket.action?buildNumber={BUILD_NUMBER}&clientVersion=16&hostName={DESKTOP_NAME}&machineId={MACHINE_ID}&productCode=cfc7082d-ae43-4978-a2a2-46feb1679405&productFamilyId=cfc7082d-ae43-4978-a2a2-46feb1679405&salt=1726973268812&secure=false&ticketId=rsoaehfbbg&userName={USERNAME}"
    OBTAIN_TICKET_PATH = f"/rpc/obtainTicket.action?buildDate=20240409&{BUILD_NUMBER}&clientVersion=16&hostName={DESKTOP_NAME}&machineId={MACHINE_ID}&productCode=cfc7082d-ae43-4978-a2a2-46feb1679405&productFamilyId=cfc7082d-ae43-4978-a2a2-46feb1679405&salt=1726973269845&secure=false&userName={USERNAME}&version={VERSION}&versionNumber={VERSION}"

    release_ticket_data = get_xml_data(server, RELEASE_TICKET_PATH)
    obtain_ticket_data = get_xml_data(server, OBTAIN_TICKET_PATH)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "release_data": release_ticket_data,
            "obtain_data": obtain_ticket_data,
            "server": server,
        },
    )


@app.get("/api/fetch")
@app.post("/api/fetch")
async def api_fetch(server: str = Form(...)):
    return await handle_fetch(server)


async def handle_fetch(server: str):
    RELEASE_TICKET_PATH = f"/rpc/releaseTicket.action?buildNumber={BUILD_NUMBER}&clientVersion=16&hostName={DESKTOP_NAME}&machineId={MACHINE_ID}&productCode=cfc7082d-ae43-4978-a2a2-46feb1679405&productFamilyId=cfc7082d-ae43-4978-a2a2-46feb1679405&salt=1726973268812&secure=false&ticketId=rsoaehfbbg&userName={USERNAME}"
    OBTAIN_TICKET_PATH = f"/rpc/obtainTicket.action?buildDate=20240409&{BUILD_NUMBER}&clientVersion=16&hostName={DESKTOP_NAME}&machineId={MACHINE_ID}&productCode=cfc7082d-ae43-4978-a2a2-46feb1679405&productFamilyId=cfc7082d-ae43-4978-a2a2-46feb1679405&salt=1726973269845&secure=false&userName={USERNAME}&version={VERSION}&versionNumber={VERSION}"

    release_ticket_data = get_xml_data(server, RELEASE_TICKET_PATH)
    obtain_ticket_data = get_xml_data(server, OBTAIN_TICKET_PATH)

    available = False
    if obtain_ticket_data.get("response_code") == "OK":
        available = True
    elif obtain_ticket_data.get("response_code") == "Error":
        available = False

    return JSONResponse(
        content={
            "available": available,
            "message": obtain_ticket_data.get("message", ""),
            "data": {
                "release_ticket_data": release_ticket_data,
                "obtain_ticket_data": obtain_ticket_data,
            },
        }
    )
