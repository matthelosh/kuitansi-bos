# import os
# import sys
# import platform
import camelot
import pandas as pd
import datetime
from sqlalchemy import create_engine
from utils.ghostscript_setup import setup_ghostscript

setup_ghostscript()
    
def extract_table(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages="all")

    if tables.n == 0:
        print("Tidak ada Tabel")
        return False
    
    all_data = [tables[i].df for i in range(tables.n)]
    final_df = pd.concat(all_data, ignore_index=True)


    def format_tanggal(tanggal):
        try:
            return datetime.datetime.strptime(tanggal, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:

            return tanggal
        
    final_df.iloc[:,0] = final_df.iloc[:,0].apply(format_tanggal)

    header_row = final_df.iloc[[0]]
    data_rows = final_df.iloc[1:]

    data_rows = data_rows[data_rows[1].notna() & (data_rows[1].astype(str).str.len() >= 3)]
    data_rows = data_rows[~data_rows[4].astype(str).str.contains("PPh|PPn", na=False, case=False)]
    data_rows = data_rows[data_rows[5].astype(str).str.strip().isin(["0","0.00","0,00",""])]
    
    data_rows[6] = (data_rows[6].astype(str).str.replace(".","",regex=False))

    # Hapus kolom 5 dan 7
    data_rows = data_rows.drop(columns=[5,7], errors='ignore')
    header_row = header_row.drop(columns=[5,7], errors='ignore')
    header_row = header_row.map(
        lambda x: str(x).strip().lower().replace(" ","_").replace(".","").replace("pengeluaran","nilai").replace("\n","_")
    )

    final_df = pd.concat([header_row, data_rows], ignore_index=True)

    return final_df

def pdf_table_to_excel(pdf_path, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl", datetime_format="YYYY-MM-DD") as writer:
        df = extract_table(pdf_path)
        if df is None:
            return False
        df.to_excel(writer, index=False, header=False)
        # print(f"Tabel berhasil disimpan sebagai: {output_path}")
        return True
    
def save_to_db(pdf_path, db_path="sqlite:///data/data.db", table_name="bku"):
    engine = create_engine(db_path)
    df = extract_table(pdf_path)
    header_row = df.iloc[[0]]
    datas = getattr(df, 'data_rows_only', df.iloc[1:])
    column_names = header_row.iloc[0].tolist()
    datas.columns = column_names

    datas.to_sql(table_name, con=engine, if_exists='append', index=False)
    return True
