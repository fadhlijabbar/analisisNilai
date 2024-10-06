import uuid
from datetime import datetime
import pandas as pd
import mysql.connector
from analysisresult import analysisProcess

def avgNilaiCounter(file_path):
    data = pd.read_excel(file_path)
    numeric_data = data.select_dtypes(include=['number'])
    all_values = numeric_data.values.flatten()
    all_values = all_values[~pd.isnull(all_values)]
    rata_rata_total = all_values.mean()
    avgNilai = round(rata_rata_total)
    return avgNilai

def analisisNilai(
    nama_siswa: str,
    kelas: str,
    nilai_pkn: int,
    nilai_bin: int,
    nilai_big: int,
    nilai_ipa: int,
    nilai_ips: int,
    nilai_mtk: int,
    nilai_pjo: int,
    id_user: int,
):
    file_path = 'files/data_latih.xlsx'
    avgNilai = avgNilaiCounter(file_path)

    perbandinganNilai = {
        'nama_siswa': nama_siswa,
        'nilai_pkn': nilai_pkn >= avgNilai,
        'nilai_bin': nilai_bin >= avgNilai,
        'nilai_big': nilai_big >= avgNilai,
        'nilai_ipa': nilai_ipa >= avgNilai,
        'nilai_ips': nilai_ips >= avgNilai,
        'nilai_mtk': nilai_mtk >= avgNilai,
        'nilai_pjo': nilai_pjo >= avgNilai,
    }

    new_data_instance = [mata_pelajaran for mata_pelajaran, melebihi in perbandinganNilai.items() if mata_pelajaran != 'nama_siswa' and melebihi]

    # Insert data into riwayat table even if no subjects exceed avgNilai
    id_riwayat = None  # Initialize here

    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="skripsi"
        ) as db:
            with db.cursor() as cursor:
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                insert_query_riwayat = """
                INSERT INTO riwayat (id_user, nama_siswa, kelas, nilai_pkn, nilai_bin, nilai_big, nilai_ipa, nilai_ips, nilai_mtk, nilai_pjo, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(insert_query_riwayat, (
                    id_user,
                    nama_siswa,
                    kelas,
                    nilai_pkn,
                    nilai_bin,
                    nilai_big,
                    nilai_ipa,
                    nilai_ips,
                    nilai_mtk,
                    nilai_pjo,
                    current_date
                ))

                db.commit()

                # Get the last inserted id_riwayat
                cursor.execute("SELECT id_riwayat FROM riwayat ORDER BY id_riwayat DESC LIMIT 1")
                id_riwayat = cursor.fetchone()[0]

                # If no subjects exceed avgNilai, stop here
                if not new_data_instance:
                    return id_riwayat

                nama_map = {
                    'nilai_pkn': 'PKN',
                    'nilai_bin': 'BIN',
                    'nilai_big': 'BIG',
                    'nilai_ipa': 'IPA',
                    'nilai_ips': 'IPS',
                    'nilai_mtk': 'MTK',
                    'nilai_pjo': 'PJO'
                }

                new_data_instance = [nama_map[mata_pelajaran] for mata_pelajaran in new_data_instance]

                hasilAnalisis = analysisProcess(new_data_instance)
                print("Hasil: ", hasilAnalisis)

                if hasilAnalisis:
                    insert_query_analysis = """
                    INSERT INTO analysisresult (id_riwayat, mapel)
                    VALUES (%s, %s)
                    """

                    for mapel in hasilAnalisis:
                        cursor.execute(insert_query_analysis, (
                            id_riwayat,
                            mapel
                        ))

                    db.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
    if id_riwayat is None:
        raise RuntimeError("Failed to create id_riwayat")

    return id_riwayat
