import os
import sys
import platform
import camelot
import pandas as pd
import datetime

if platform.system() == "Windows":

    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))


    gs_bin_path = os.path.join(base_dir, 'ghostscript', 'bin')
    os.environ["PATH"] += os.pathsep + gs_bin_path
    

def pdf_table_to_excel(pdf_path, output_path):
    tables = camelot.read_pdf(pdf_path, pages="all")

    if tables.n == 0:
        print("Tidak ada Tabel")
        return False
    
    all_data = []

    for i in range(tables.n):
        df = tables[i].df
        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    def format_tanggal(tanggal):
        try:
            return datetime.datetime.strptime(tanggal, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            return tanggal
        
    final_df.iloc[:,0] = final_df.iloc[:,0].apply(format_tanggal)

    with pd.ExcelWriter(output_path, engine="openpyxl", datetime_format="YYYY-MM-DD") as writer:
        final_df.to_excel(writer, index=False, header=False)
        print(f"Tabel berhasil disimpan sebagai: {output_path}")
        return True