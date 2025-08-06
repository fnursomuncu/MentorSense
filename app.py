import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai

# Ortam değişkenlerini yükle (api.env dosyasından)
load_dotenv(dotenv_path='api.env')

# Flask uygulaması
app = Flask(__name__, template_folder='templates', static_folder='static')

# Gemini API yapılandırması
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# genai kütüphanesini kullanarak model adını doğrudan belirleyebiliriz
genai.configure(api_key=GEMINI_API_KEY)


# Ana sayfa (index.html'yi sunar)
@app.route('/')
def index():
    return render_template('index.html')


# Gemini API endpoint'i
@app.route('/generate', methods=['POST'])
def generate_content():
    if not GEMINI_API_KEY:
        return jsonify({'error': 'API anahtarı sunucuda yapılandırılmamış.'}), 500

    client_data = request.get_json()
    prompt = client_data.get('prompt')

    if not prompt:
        return jsonify({'error': 'İstek gövdesi boş veya geçerli bir prompt içermiyor.'}), 400

    try:
        # gemini-2.5-flash modelini kullanma
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        
        response = model.generate_content(prompt)
        
        # Yanıtı JSON formatında döndürme
        return jsonify({'response': response.text})

    except Exception as e:
        print(f"Gemini API çağrısında hata: {e}")
        return jsonify({'error': f'Gemini API çağrısında bir hata oluştu: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)