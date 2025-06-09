from fastapi import FastAPI, Form, Request, HTTPException, UploadFile, File
import tempfile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.installexe import download_and_install_software
from utils.pdf import extract_text_from_pdf
from utils.software_details import get_hardware_details, scan_apps_and_storage
from utils.model import model

import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/scan-apps")
async def scan_apps():
    try:
        system, downloaded, system_total, downloaded_total = scan_apps_and_storage()
        return {
            "system_apps": system,
            "downloaded_apps": downloaded,
            "system_total_size_gb": system_total / 1e9,
            "downloaded_total_size_gb": downloaded_total / 1e9,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hardware-info")
async def hardware_info():
    try:
        return get_hardware_details()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/install-software", response_class=HTMLResponse)
async def install_software(request: Request, software_key: str = Form(...)):
    try:
        download_and_install_software(software_key)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"✅ Installation started for: {software_key}"
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"❌ Installation failed: {str(e)}"
        })


@app.post("/upload-pdf", response_class=HTMLResponse)
async def upload_pdf(request: Request, pdf_file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await pdf_file.read())
            tmp_path = tmp.name

        extracted_text = extract_text_from_pdf(tmp_path)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "pdf_text_preview": extracted_text[:1000],  # limit to 1000 chars
            "message": f"✅ PDF '{pdf_file.filename}' processed successfully"
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"❌ Error processing PDF: {str(e)}"
        })


@app.post("/chat", response_class=HTMLResponse)
async def chat_with_ai(request: Request, prompt: str = Form(...), pdf_context: str = Form("")):
    try:
        context = f"{pdf_context}\n\nUser Question: {prompt}" if pdf_context else prompt
        response = model.start_chat(history=[]).send_message(context)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "response": response.text,
            "prompt": prompt
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "response": f"❌ Error: {str(e)}",
            "prompt": prompt
        })


if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
