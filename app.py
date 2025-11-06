from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from process_excel_dynamic import process_excel

app = Flask(__name__)
CORS(app)

# Configurações
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'Nenhum arquivo selecionado'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Tipo de arquivo não permitido. Use .xlsx ou .xls'}), 400

    try:
        # Salvar arquivo com nome fixo
        filename = 'Lista Prospecçao.xlsx'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Processar arquivo usando process_excel_dynamic
        data = process_excel(filepath, 'all_sheets_data.json')

        # Retornar sucesso com informações do processamento
        return jsonify({
            'success': True,
            'message': 'Arquivo processado com sucesso!',
            'data': {
                'sheets_count': len(data.get('sheets', [])),
                'last_updated': data.get('last_updated'),
                'total_records': sum(s.get('total_records', 0) for s in data.get('sheets', []))
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro no upload: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        with open('all_sheets_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Calcular estatísticas gerais
            total_records = sum(s.get('total_records', 0) for s in data.get('sheets', []))
            return jsonify({
                'success': True,
                'stats': {
                    'total_records': total_records,
                    'sheets_count': len(data.get('sheets', [])),
                    'last_updated': data.get('last_updated')
                }
            }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("SERVIDOR DASHBOARD DE PROSPECÇÃO")
    print("="*60)
    print("\nAcesse: http://localhost:5000")
    print("\nFuncionalidades:")
    print("  - Dashboard interativo")
    print("  - Upload de arquivo Excel")
    print("  - Processamento automático")
    print("  - Atualização em tempo real")
    print("\n" + "="*60)
    app.run(debug=True, port=5000, host='0.0.0.0')
