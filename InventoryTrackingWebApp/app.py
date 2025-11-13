from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("stok_takip.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return redirect(url_for("urunler"))

@app.route("/urunler")
def urunler():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urunler ORDER BY id DESC")
    urunler = cursor.fetchall()
    conn.close()
    return render_template("base.html", urunler=urunler)

@app.route("/urun_ekle", methods=["GET", "POST"])
def urun_ekle():
    if request.method == "POST":
        urun_adi = request.form["urun_adi"]
        kategori = request.form["kategori"]
        miktar = int(request.form["miktar"])
        fiyat = float(request.form["fiyat"])
        ekleme_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO urunler (urun_adi, kategori, miktar, fiyat, ekleme_tarihi)
            VALUES (?, ?, ?, ?, ?)
        """, (urun_adi, kategori, miktar, fiyat, ekleme_tarihi))
        conn.commit()
        conn.close()

        return redirect(url_for("urunler"))

    return render_template("urun_ekle.html")

@app.route("/urun_duzenle/<int:id>", methods=["GET", "POST"])
def urun_duzenle(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urunler WHERE id = ?", (id,))
    urun = cursor.fetchone()

    if not urun:
        conn.close()
        return "Ürün bulunamadı", 404

    if request.method == "POST":
        urun_adi = request.form["urun_adi"]
        kategori = request.form["kategori"]
        miktar = int(request.form["miktar"])
        fiyat = float(request.form["fiyat"])

        cursor.execute("""
            UPDATE urunler
            SET urun_adi = ?, kategori = ?, miktar = ?, fiyat = ?
            WHERE id = ?
        """, (urun_adi, kategori, miktar, fiyat, id))
        conn.commit()
        conn.close()
        return redirect(url_for("urunler"))

    conn.close()
    return render_template("urun_duzenle.html", urun=urun)

@app.route("/urun_sil/<int:id>")
def urun_sil(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urunler WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("urunler"))

@app.route("/grafik")
def grafik():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kategori, SUM(miktar) AS toplam_miktar FROM urunler GROUP BY kategori")
    veriler = cursor.fetchall()
    conn.close()

    kategoriler = [row["kategori"] for row in veriler]
    miktarlar = [row["toplam_miktar"] for row in veriler]

    return render_template("grafik.html", kategoriler=kategoriler, miktarlar=miktarlar)

if __name__ == "__main__":
    app.run(debug=True)
