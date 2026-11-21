from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os

# Inisiasi jembatan (Flask) biar web dan Python bisa ngobrol
app = Flask(__name__)
CORS(app)

# MASUKIN API KEY LO DI SINI
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Atur AI-nya pakai model Gemini yang paling stabil
model = genai.GenerativeModel('gemini-3-flash-preview')
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')
# Ini rute (jalur) yang bakal dipanggil sama tombol di web lo
@app.route('/analisis', methods=['POST'])
def analisis_pesan():
    data = request.json
    pesan_user = data.get('pesan', '')

    # INI SOP / INSTRUKSI KERJA BUAT AI-NYA
    prompt = f"""
    Bertindaklah sebagai sahabat yang juga seorang pakar keuangan dan perlindungan konsumen di Indonesia. 
    Tugasmu adalah menganalisis pesan tawaran investasi atau keuangan berikut:
    "{pesan_user}"
    
    Gunakan gaya bahasa yang ramah, membumi, berempati, dan mudah dipahami awam. 

    Berikan respons singkat dalam format persis seperti di bawah ini, WAJIB tanpa menggunakan markdown tebal/bintang (*):
    STATUS: [Pilih salah satu kata ini saja: AMAN, WASPADA, atau BAHAYA]
    KESIMPULAN: [Berikan 2-3 kalimat penjelasan santai namun logis mengapa pesan tersebut masuk ke dalam status di atas.]
    """

    try:
        # Suruh AI mikir berdasarkan prompt di atas
        response = model.generate_content(prompt)
        jawaban_ai = response.text
        
        return jsonify({"status": "sukses", "hasil": jawaban_ai})
    
    except Exception as e:
        return jsonify({"status": "error", "pesan": str(e)})

if __name__ == '__main__':
    # Nyalain server Python-nya
    app.run(debug=True, port=5000)
# ==============================================================================
# CATATAN UNTUK PENGUJIAN FITUR AI
# ==============================================================================
# 
# Biar fitur "Mulai Analisis AI" di website-nya bisa dicoba,
# mohon bantuannya untuk me-run server Python ini dulu ka, karena
# logika AI-nya butuh nyambung ke backend lokal.
#
# Langkah buat ngetesnya:
# 1. Buka Terminal, pastikan udah di dalam folder tugas ini.
# 2. Run perintah: python app.py dan klik Enter
# 3. Kalau di terminal udah muncul "Running on http://127.0.0.1:5000", 
#    berarti server udah aman.
# 4. Setelah itu, Kakak bisa langsung buka index.html pakai Live Server
#    dan semua fiturnya udah siap dicoba.
#
# Terima kasih banyak atas feedbacknya ka
# ==============================================================================
