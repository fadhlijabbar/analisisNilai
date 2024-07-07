from fastapi import FastAPI, File, UploadFile, Form, Request
import pandas as pd
import mysql.connector
from mlxtend.frequent_patterns import fpgrowth, association_rules
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ambildata import showDataAnalysis
from ambildata import showDataRules
from ambildata import showDataAnalysisAll
from starlette.responses import Response
import uuid
from datetime import datetime

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/files", StaticFiles(directory="files"), name="files")
templates = Jinja2Templates(directory="templates")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skripsi"
)
cursor = db.cursor()

@app.post("/uploadfile")
async def create_upload_file(
    analysis_name: str = Form(...),
    min_score: float = Form(...),
    min_support: float = Form(...),
    min_confidence: float = Form(...),
    file: UploadFile = File(...)
):
    filenamebaru = f"{uuid.uuid4()}_{file.filename}"
    file_location = f"files/{filenamebaru}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    df = pd.read_excel(file_location)

    frequent_items = fpgrowth(df, min_support=min_support/100, use_colnames=True)
    rules = association_rules(frequent_items, metric="confidence", min_threshold=min_confidence/100)
    print(rules)

    rules = rules.drop(columns=['antecedent support', 'consequent support'])

    db.connect()

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    insert_query = """
    INSERT INTO analysis (date, analysis_name, data_file, filename, min_score, min_support, min_confidence)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (
        current_date,
        analysis_name,
        filenamebaru,
        file.filename,
        min_score,
        min_support,
        min_confidence,
    ))
    
    db.commit()

    select_last_analysis = "SELECT id_analysis FROM analysis ORDER BY id_analysis DESC LIMIT 1"
    cursor.execute(select_last_analysis)
    id_analysis = cursor.fetchone()[0]

    insert_query = """
    INSERT INTO rules (id_analysis, antecedents, consequents, support, confidence, lift, leverage, conviction, z_metric)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for index, row in rules.iterrows():
        cursor.execute(insert_query, (
            id_analysis,
            ', '.join(list(row['antecedents'])),
            ', '.join(list(row['consequents'])),
            row['support'],
            row['confidence'],
            row['lift'],
            row['leverage'],
            row['conviction'],
            row['zhangs_metric']
        ))
        
    db.commit()
    db.close()

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