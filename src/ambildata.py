from fastapi import FastAPI, Request
import mysql.connector
from pydantic import BaseModel

app = FastAPI()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="skripsi"
)

def showDataAnalysis(id_analysis: int):
    mydb.connect()
    cursor = mydb.cursor()
    
    query = "SELECT * FROM analysis WHERE id_analysis = %s LIMIT 1"
    
    try:
        cursor.execute(query, (id_analysis,))
        result = cursor.fetchall()
        return [
            {
                "date": row[1],
                "analysis_name": row[2],
                "data_file": row[3],
                "filename": row[4],
                "min_score": int(row[5]),
                "min_support": int(row[6]),
                "min_confidence": int(row[7]),
            } for row in result
        ]
    
    except Exception as e:
        mydb.close()
        response = {
            'status': 'error',
            'message': 'Terjadi kesalahan saat mengambil data',
            'error': str(e)
        }
        return [response]
    

def showDataRules(id_analysis: int):
    mydb.connect()
    cursor = mydb.cursor()
    
    query = "SELECT * FROM rules WHERE id_analysis = %s"
    
    try:
        cursor.execute(query, (id_analysis,))
        result = cursor.fetchall()
        return [
            {
                "antecedents": row[2],
                "consequents": row[3],
                "support": int(row[4]*100),
                "confidence": int(row[5]*100),
                "lift": row[6],
                "leverage": row[7],
                "conviction": row[8],
                "z_metric": row[9],
            } for row in result
        ]
    
    except Exception as e:
        mydb.close()
        response = {
            'status': 'error',
            'message': 'Terjadi kesalahan saat mengambil data',
            'error': str(e)
        }
        return [response]
    
def showDataAnalysisAll():
    mydb.connect()
    cursor = mydb.cursor()
    
    queryAnalysis = "SELECT * FROM analysis ORDER BY date DESC"
    
    try:
        cursor.execute(queryAnalysis)
        result = cursor.fetchall()

        data = []
        for row in result:
            queryRules = "SELECT count(*) as numberRules FROM rules WHERE id_analysis = %s"
            cursor.execute(queryRules, (row[0],))
            rules_count = cursor.fetchone()[0] 

            analysis_data = {
                "id_analysis": row[0],
                "date": row[1].strftime('%d %B %Y'),
                "analysis_name": row[2],
                "numberRules": rules_count,
            }
            data.append(analysis_data)
        
        return data
    
    except Exception as e:
        mydb.close()
        response = {
            'status': 'error',
            'message': 'Terjadi kesalahan saat mengambil data',
            'error': str(e)
        }
        return [response]