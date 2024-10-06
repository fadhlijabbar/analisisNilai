from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skripsi"
    )

def showDataRiwayat(id_riwayat: int) -> List[Dict[str, Any]]:
    result = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM riwayat WHERE id_riwayat = %s LIMIT 1"
        cursor.execute(query, (id_riwayat,))
        rows = cursor.fetchall()
        result = [
            {
                "nama_siswa": row[3],
                "nilai_pkn": row[4],
                "nilai_bin": row[5],
                "nilai_big": row[6],
                "nilai_ipa": row[7],
                "nilai_ips": row[8],
                "nilai_mtk": row[9],
                "nilai_pjo": row[10],
            } for row in rows
        ]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return result

def showDataAnalysis(id_riwayat: int) -> List[Dict[str, Any]]:
    result = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analysisresult WHERE id_riwayat = %s"
        cursor.execute(query, (id_riwayat,))
        rows = cursor.fetchall()
        result = [
            {
                "mapel": row[2],
            } for row in rows
        ]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return result

def selectUser(username: str) -> int:
    result = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT id_user FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result is not None:
            result = result[0]  # Extract the single value from the tuple
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return result

def format_tanggal(tanggal_datetime):
    return tanggal_datetime.strftime("%d %B %Y")

def showDataHistory(id_user: int) -> List[Dict[str, Any]]:
    result = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM riwayat WHERE id_user = %s"
        cursor.execute(query, (id_user,))
        rows = cursor.fetchall()
        result = [
            {
                "id_riwayat": row[0],
                "kelas": row[2],
                "nama_siswa": row[3],
                "date": format_tanggal(row[11]),
            } for row in rows
        ]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return result

def showKelas():
    result = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM kelas"
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch all rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return result

def getOptionKelas(username: str):
    result = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            queryWK = "SELECT nama FROM user WHERE username=%s"
            cursor.execute(queryWK, (username,))
            resultWK = cursor.fetchone()
            if resultWK:
                namaWK = resultWK[0]

                query = "SELECT * FROM kelas WHERE wali_kelas=%s"
                cursor.execute(query, (namaWK,))
                result = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

    return result

def tambahKelas(
    tingkat: str,
    alfabet: str,
    username: str
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        kelas = str(tingkat) + str(alfabet)

        querySelectWK = "SELECT nama FROM user WHERE username=%s"
        cursor.execute(querySelectWK, (username,))
        namaWK = cursor.fetchone()

        if not namaWK:
            return False

        cekKelas = "SELECT kelas FROM kelas WHERE kelas=%s"
        cursor.execute(cekKelas, (kelas,))
        resultKelas = cursor.fetchone()
        if resultKelas:
            return False

        query = "INSERT INTO kelas (kelas, wali_kelas) VALUES (%s, %s)"
        cursor.execute(query, (kelas, namaWK[0]))

        conn.commit()
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

def getDataAll(kelas: str):
    # Dictionary to map abbreviations to full names
    abbreviation_to_fullname = {
        'PKN': 'Pendidikan Kewarganegaraan',
        'BIN': 'Bahasa Indonesia',
        'BIG': 'Bahasa Inggris',
        'IPA': 'Ilmu Pengetahuan Alam',
        'IPS': 'Ilmu Pengetahuan Sosial',
        'MTK': 'Matematika',
        'PJO': 'Pendidikan Jasmani dan Olahraga'
    }

    final_results = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fetch data from riwayat table
        query = "SELECT * FROM riwayat WHERE kelas=%s"
        cursor.execute(query, (kelas,))
        resultRiwayat = cursor.fetchall()

        # Process each entry in resultRiwayat
        for row in resultRiwayat:
            id_riwayat = row[0]  # Assuming ID is the first column
            nama = row[3]       # Assuming nama is the fourth column

            # Fetch analysis results for each id_riwayat
            queryAnalysisResult = "SELECT * FROM analysisresult WHERE id_riwayat=%s"
            cursor.execute(queryAnalysisResult, (id_riwayat,))
            resultAnalysisResult = cursor.fetchall()

            # Extract mapel (subjects) from the analysis results and map to full names
            mapel = [abbreviation_to_fullname.get(r[2], r[2]) for r in resultAnalysisResult]  # Assuming mapel is the third column

            # Format the results and add to final results
            final_results.append({'id_riwayat': id_riwayat, 'nama': nama, 'analysis_result': tuple(mapel)})

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    finally:
        cursor.close()
        conn.close()

    return final_results

def getDataMapel(kelas: str, subject_abbreviation: str):
    abbreviation_to_fullname = {
        'PKN': 'Pendidikan Kewarganegaraan',
        'BIN': 'Bahasa Indonesia',
        'BIG': 'Bahasa Inggris',
        'IPA': 'Ilmu Pengetahuan Alam',
        'IPS': 'Ilmu Pengetahuan Sosial',
        'MTK': 'Matematika',
        'PJO': 'Pendidikan Jasmani dan Olahraga'
    }

    final_results = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch data from riwayat table
        query = "SELECT * FROM riwayat WHERE kelas=%s"
        cursor.execute(query, (kelas,))
        resultRiwayat = cursor.fetchall()

        for row in resultRiwayat:
            id_riwayat = row[0]
            nama = row[3]

            # Fetch analysis results for each id_riwayat
            queryAnalysisResult = "SELECT * FROM analysisresult WHERE id_riwayat=%s"
            cursor.execute(queryAnalysisResult, (id_riwayat,))
            resultAnalysisResult = cursor.fetchall()

            # Extract mapel (subjects) and map to full names
            mapel = [abbreviation_to_fullname.get(r[2], r[2]) for r in resultAnalysisResult]

            # Check if the specific subject is in the results
            if any(subject_abbreviation == r[2] for r in resultAnalysisResult):
                final_results.append({'id_riwayat': id_riwayat, 'nama': nama, 'analysis_result': tuple(mapel)})

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except ValueError as ve:
        print(f"Value error: {ve}")
    finally:
        cursor.close()
        conn.close()

    return final_results