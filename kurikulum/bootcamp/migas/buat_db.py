import sqlite3, pandas as pd, os
D="data"; con=sqlite3.connect("migas.db")
for f in os.listdir(D):
    if f.endswith(".csv"):
        t=f[:-4]; df=pd.read_csv(f"{D}/{f}")
        df.to_sql(t, con, if_exists="replace", index=False)
        print(f"{t:20s} {df.shape}")
con.commit()
print("\n--- uji cepat ---")
for q,label in [
 ("SELECT COUNT(*) FROM produksi_harian","baris produksi"),
 ("SELECT ROUND(SUM(oil_bopd),0) FROM produksi_harian","total oil bbl"),
 ("SELECT COUNT(DISTINCT sumur_id) FROM produksi_harian","sumur produser"),
]:
    print(f"{label:20s}", con.execute(q).fetchone()[0])
con.close()
