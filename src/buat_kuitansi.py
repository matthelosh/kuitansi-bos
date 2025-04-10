from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate
from reportlab.lib import colors
import sqlite3

F4_SIZE = (595.275590551, 935.433070866)
width, height = F4_SIZE

def ambil_data_db(db_path="data.db", table="bku"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return columns, rows


def buat(c, data, idx, fieldnames):
    #Kop
    file_identitas = open("identitas.txt")
    lines = file_identitas.readlines()
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 2 * cm, lines[0].strip()) # Kabupaten
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, height - 2.5 * cm, lines[1].strip()) # Dinas
    c.drawCentredString(width / 2, height - 3.0 * cm, lines[2].strip()) # Korwil
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width / 2, height - 3.5 * cm, lines[3].strip()) # Lembaga
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 4.0 * cm, lines[4].strip()) # Alamat
    c.drawCentredString(width / 2, height - 4.5 * cm, lines[5].strip()) # Email
    
    file_identitas.close()


    #judul Kuitansi
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 6.2 * cm, "KUITANSI")
    
    #Informasi Utama
    c.setFont("Helvetica", 10)
    c.drawString(2.5*cm, height - 6.5*cm, f"Sudah diterima dari: Bendahara BOS Reguler")
    c.drawString(2.5*cm, height - 7.2*cm, f"Uang sebesar: {data[fieldnames.index('nilai')]}")
    c.drawString(2.5*cm, height - 7.9*cm, f"Untuk keperluan: {data[fieldnames.index('uraian')]}")
    
def simpan():
    fieldnames, rows = ambil_data_db()
    c = canvas.Canvas("Kuitansi.pdf", pagesize=F4_SIZE)

    for idx, row in enumerate(rows):
        buat(c, row, idx, fieldnames)
        c.showPage()

    c.save()
    print("Kuitansi disimpan")

if __name__ == "__main__":
    simpan()
