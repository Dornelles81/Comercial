"""
API Serverless para buscar dados do dashboard
Vercel Function
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.db import Database

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Retorna todos os dados do dashboard
        Formato compatível com all_sheets_data.json
        """
        try:
            db = Database()
            data = db.get_all_sheets_data()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
