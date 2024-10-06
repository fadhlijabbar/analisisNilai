from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from getdata import showDataRiwayat
from getdata import showDataAnalysis
from getdata import selectUser
from getdata import showDataHistory
from getdata import showKelas
from getdata import tambahKelas
from getdata import getOptionKelas
from getdata import getDataAll
from getdata import getDataMapel
from mapelcounter import countMapel
from starlette.responses import Response, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from daftar import daftarAkun
from login import loginAkun
from analyze import analisisNilai
from fastapi.responses import JSONResponse

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/files", StaticFiles(directory="files"), name="files")
templates = Jinja2Templates(directory="templates")

# Configure session middleware
config = Config(".env")
SECRET_KEY = config("SECRET_KEY", default="your_secret_key")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Proses Login
@app.post("/proseslogin")
async def proseslogin(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if loginAkun(username, password):
        request.session["username"] = username
        return RedirectResponse(url="/analisis", status_code=302)
    else:
        return RedirectResponse(url="/?error_message=1", status_code=302)
    
# Proses Analisis
@app.post("/prosesanalisis")
async def prosesanalisis(
    request: Request,
    nama_siswa: str = Form(...),
    kelas: str = Form(...),
    nilai_pkn: int = Form(...),
    nilai_bin: int = Form(...),
    nilai_big: int = Form(...),
    nilai_ipa: int = Form(...),
    nilai_ips: int = Form(...),
    nilai_mtk: int = Form(...),
    nilai_pjo: int = Form(...)
):
    username = request.session["username"]
    id_user = selectUser(username)
    id_riwayat = analisisNilai(nama_siswa, kelas, nilai_pkn, nilai_bin, nilai_big, nilai_ipa, nilai_ips, nilai_mtk, nilai_pjo, id_user)
    return RedirectResponse(url=f"/riwayat/{id_riwayat}", status_code=302)

# Proses Daftar
@app.post("/prosesdaftar")
async def prosesdaftar(
    nama: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
): 
    
    result = daftarAkun(nama, username, password)

    if result == "Username sudah terdaftar":
        redirect_url = "/daftar?error_message=1"
        response = Response(status_code=302)
        response.headers["Location"] = redirect_url
        return response

    redirect_url = "/"
    
    response = Response(status_code=302)
    response.headers["Location"] = redirect_url

    return response


# Proses Tambah Kelas
@app.post("/prosestambahkelas")
def home(
    tingkat: str = Form(...),
    alfabet: str = Form(...),
    username: str = Form(...),
):
    prosesTambahKelas = tambahKelas(tingkat, alfabet, username)

    if prosesTambahKelas:
        return RedirectResponse(url="/kelas", status_code=302)
    else:
        return RedirectResponse(url="/kelas/tambah?error_message=1", status_code=302)

# Cek Koneksi
@app.get("/cek")
def home():
    return "Koneksi Aman"


# Logout
@app.get("/logout")
def home(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

# Home (Login Page)
@app.get("/")
def home(request: Request):
    if "username" in request.session:
        return RedirectResponse(url="/analisis")
    error_message = request.query_params.get("error_message")
    return templates.TemplateResponse("login.html", {"request": request, "error_message": error_message})

# Daftar
@app.get("/daftar")
def home(request: Request):
    if "username" in request.session:
        return RedirectResponse(url="/analisis")
    error_message = request.query_params.get("error_message")
    return templates.TemplateResponse("daftar.html", {"request": request, "error_message": error_message})

# Analisis
@app.get("/analisis")
def home(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    username = request.session["username"]
    hasilCountMapel = countMapel(["PKN","BIN","BIG","IPA","IPS","MTK","PJO"])
    optionKelas = getOptionKelas(username)
    return templates.TemplateResponse("analisis.html", {
        "request": request,
        "username": username,
        "countMapel": hasilCountMapel,
        "optionKelas": optionKelas
    })

# Riwayat
@app.get("/riwayat")
def home(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    username = request.session["username"]
    id_user = selectUser(username)
    dataRiwayat = showDataHistory(id_user)
    hasilCountMapel = countMapel(["PKN", "BIN", "BIG", "IPA", "IPS", "MTK", "PJO"])
    return templates.TemplateResponse("riwayat.html", {
        "request": request,
        "dataRiwayat": dataRiwayat,
        "username": username,
        "countMapel": hasilCountMapel,
    })

# Hasil Riwayat
@app.get("/riwayat/{id_riwayat}")
def home(id_riwayat: int, request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    dataRiwayat = showDataRiwayat(id_riwayat)
    dataAnalysis = showDataAnalysis(id_riwayat)
    username = request.session["username"]
    hasilCountMapel = countMapel(["PKN", "BIN", "BIG", "IPA", "IPS", "MTK", "PJO"])
    return templates.TemplateResponse("hasil.html", {
        "request": request,
        "dataRiwayat": dataRiwayat,
        "dataAnalysis": dataAnalysis,
        "username": username,
        "countMapel": hasilCountMapel,
    })

# Mapel
@app.get("/mapel/{mapel}")
def home(mapel: str, request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    username = request.session["username"]
    hasilCountMapel = countMapel(["PKN", "BIN", "BIG", "IPA", "IPS", "MTK", "PJO"])
    
    return templates.TemplateResponse("mapel.html", {
        "request": request,
        "username": username,
        "countMapel": hasilCountMapel,
        "current_mapel": mapel
    })

# Kelas
@app.get("/kelas")
def home(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    username = request.session["username"]
    dataKelas = showKelas()
    hasilCountMapel = countMapel(["PKN", "BIN", "BIG", "IPA", "IPS", "MTK", "PJO"])
    
    return templates.TemplateResponse("kelas.html", {
        "request": request,
        "username": username,
        "countMapel": hasilCountMapel,
        "dataKelas": dataKelas
    })

# Tambah Kelas
@app.get("/kelas/tambah")
def home(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    username = request.session["username"]
    error_message = request.query_params.get("error_message")
    hasilCountMapel = countMapel(["PKN", "BIN", "BIG", "IPA", "IPS", "MTK", "PJO"])
    
    return templates.TemplateResponse("tambahkelas.html", {
        "request": request,
        "username": username,
        "countMapel": hasilCountMapel,
        "error_message": error_message
    })

# Detail Kelas
@app.get("/kelas/{kelas}")
def home(kelas: str, request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    username = request.session["username"]
    thisKelas = kelas
    resultByAll = getDataAll(kelas)
    resultByPKN = getDataMapel(kelas, "PKN")
    resultByBIN = getDataMapel(kelas, "BIN")
    resultByBIG = getDataMapel(kelas, "BIG")
    resultByIPA = getDataMapel(kelas, "IPA")
    resultByIPS = getDataMapel(kelas, "IPS")
    resultByMTK = getDataMapel(kelas, "MTK")
    resultByPJO = getDataMapel(kelas, "PJO")
    hasilCountMapel = countMapel(["PKN", "BIN", "BIG", "IPA", "IPS", "MTK", "PJO"])

    return templates.TemplateResponse("detailkelas.html", {
        "request": request,
        "username": username,
        "countMapel": hasilCountMapel,
        "kelas": thisKelas,
        "resultByAll": resultByAll,
        "resultByPKN": resultByPKN,
        "resultByBIN": resultByBIN,
        "resultByBIG": resultByBIG,
        "resultByIPA": resultByIPA,
        "resultByIPS": resultByIPS,
        "resultByMTK": resultByMTK,
        "resultByPJO": resultByPJO
    })

# Hasil Kelas
@app.get("/kelas/{kelas}/{id_riwayat}")
def home(kelas: str, id_riwayat: int, request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/")
    dataRiwayat = showDataRiwayat(id_riwayat)
    dataAnalysis = showDataAnalysis(id_riwayat)
    username = request.session["username"]
    thisKelas = kelas
    hasilCountMapel = countMapel(["PKN", "BIN", "BIG", "IPA", "IPS", "MTK", "PJO"])
    return templates.TemplateResponse("detailsiswa.html", {
        "request": request,
        "dataRiwayat": dataRiwayat,
        "dataAnalysis": dataAnalysis,
        "username": username,
        "countMapel": hasilCountMapel,
        "kelas": thisKelas
    })

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))