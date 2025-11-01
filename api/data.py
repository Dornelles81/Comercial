"""
API Serverless para buscar dados do dashboard
Vercel Function
"""
from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.db import Database

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    """
    Retorna todos os dados do dashboard
    Formato compatível com all_sheets_data.json
    """
    try:
        db = Database()
        data = db.get_all_sheets_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
