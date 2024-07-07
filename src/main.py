from fastapi import FastAPI, File, UploadFile, Form, Request
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ambildata import showDataAnalysis
from ambildata import showDataRules
from ambildata import showDataAnalysisAll
from starlette.responses import Response
from analyze import analisisNilai

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/files", StaticFiles(directory="files"), name="files")
templates = Jinja2Templates(directory="templates")

@app.post("/uploadfile")
async def create_upload_file(
    analysis_name: str = Form(...),
    min_score: float = Form(...),
    min_support: float = Form(...),
    min_confidence: float = Form(...),
    file: UploadFile = File(...)
):
    id_analysis = analisisNilai(analysis_name, min_score, min_support, min_confidence, file)

    redirect_url = f"/riwayat/{id_analysis}"
    
    response = Response(status_code=302)
    response.headers["Location"] = redirect_url
    
    return response

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/daftar")
def home(request: Request):
    return templates.TemplateResponse("daftar.html", {"request": request})

@app.get("/analisis")
def home(request: Request):
    return templates.TemplateResponse("analisis.html", {"request": request})

@app.get("/analisis/{id_analysis}")
def get_show_data(id_analysis: int, request: Request):
    dataAnalysis = showDataAnalysis(id_analysis)
    dataRules = showDataRules(id_analysis)
    return templates.TemplateResponse("analisis.html", {"request": request, "dataRules": dataRules, "dataAnalysis": dataAnalysis})

@app.get("/riwayat")
def home(request: Request):
    dataAnalysisAll = showDataAnalysisAll()
    return templates.TemplateResponse("riwayat.html", {"request": request, "dataAnalysisAll": dataAnalysisAll})

@app.get("/riwayat/{id_analysis}")
def home(id_analysis: int, request: Request):
    dataAnalysisAll = showDataAnalysisAll()
    dataAnalysis = showDataAnalysis(id_analysis)
    dataRules = showDataRules(id_analysis)
    return templates.TemplateResponse("riwayat.html", {"request": request, "dataAnalysisAll": dataAnalysisAll, "dataRules": dataRules, "dataAnalysis": dataAnalysis})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))