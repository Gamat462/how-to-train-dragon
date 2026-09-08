"""Menjalankan isi query.sql pada wawancara.duckdb dan mencetak hasilnya.

Cara pakai:
    python jalankan.py              # menjalankan query.sql
    python jalankan.py soal1.sql    # menjalankan berkas lain

Dipakai di Minggu 14 Hari 97-98. Tulis SQL-mu di query.sql, simpan, jalankan ini.
"""
import pathlib
import sys
import duckdb

berkas = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "query.sql")
if not berkas.exists():
    print(f"berkas {berkas} tidak ada. Buat dulu, isi dengan SQL-mu.")
    raise SystemExit(2)

sql = berkas.read_text(encoding="utf-8").strip().rstrip(";")
if not sql:
    print(f"{berkas} masih kosong.")
    raise SystemExit(2)

con = duckdb.connect("wawancara.duckdb", read_only=True)
print(con.sql(sql))
con.close()
