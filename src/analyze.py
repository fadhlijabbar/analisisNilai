import uuid
from datetime import datetime
import pandas as pd
import mysql.connector
from fastapi import FastAPI, File, UploadFile, Form, Request
from mlxtend.frequent_patterns import fpgrowth, association_rules


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skripsi"
)
cursor = db.cursor()

def analisisNilai(
    analysis_name: str,
    min_score: float,
    min_support: float,
    min_confidence: float,
    file: UploadFile
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

    insert_query_analysis = """
    INSERT INTO analysis (date, analysis_name, data_file, filename, min_score, min_support, min_confidence)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query_analysis, (
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

    insert_query_rules = """
    INSERT INTO rules (id_analysis, antecedents, consequents, support, confidence, lift, leverage, conviction, z_metric)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for index, row in rules.iterrows():
        cursor.execute(insert_query_rules, (
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

    return id_analysis
