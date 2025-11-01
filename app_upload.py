"""
Servidor Flask para upload e processamento de arquivos Excel
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from process_excel_dynamic import process_excel
import traceback

app = Flask(__name__)
CORS(app)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Criar pasta de uploads se não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página inicial"""
    return send_from_directory('.', 'upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint para upload de arquivo Excel
    """
    try:
        # Verificar se o arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo enviado'
            }), 400

        file = request.files['file']

        # Verificar se um arquivo foi selecionado
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo selecionado'
            }), 400

        # Verificar extensão
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Tipo de arquivo não permitido. Use .xlsx ou .xls'
            }), 400

        # Salvar arquivo
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_with_timestamp = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_timestamp)

        file.save(filepath)

        # Processar arquivo
        print(f"\n[OK] Arquivo salvo: {filepath}")
        print(f"[OK] Iniciando processamento...")

        result = process_excel(filepath)

        return jsonify({
            'success': True,
            'message': 'Arquivo processado com sucesso!',
            'data': {
                'filename': filename,
                'sheets_count': len(result['sheets']),
                'sheets': [
                    {
                        'name': sheet['name'],
                        'records': sheet['total_records']
                    }
                    for sheet in result['sheets']
                ],
                'last_updated': result['last_updated']
            }
        })

    except Exception as e:
        error_msg = str(e)
        print(f"\n[ERRO] Erro ao processar arquivo: {error_msg}")
        traceback.print_exc()

        return jsonify({
            'success': False,
            'error': f'Erro ao processar arquivo: {error_msg}'
        }), 500

@app.route('/current-data', methods=['GET'])
def get_current_data():
    """
    Retorna informações sobre os dados atualmente carregados
    """
    try:
        if os.path.exists('all_sheets_data.json'):
            import json
            with open('all_sheets_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            return jsonify({
                'success': True,
                'data': {
                    'last_updated': data.get('last_updated'),
                    'sheets_count': len(data.get('sheets', [])),
                    'sheets': [
                        {
                            'name': sheet['name'],
                            'records': sheet['total_records']
                        }
                        for sheet in data.get('sheets', [])
                    ]
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado carregado ainda'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    from datetime import datetime
    print("\n" + "="*60)
    print("SERVIDOR DE UPLOAD INICIADO")
    print("="*60)
    print("\nDashboard de Upload disponivel em:")
    print("   http://localhost:5000")
    print("\nDashboard Principal:")
    print("   http://localhost:8000/dashboard_completo.html")
    print("\n" + "="*60)

    app.run(host='0.0.0.0', port=5000, debug=True)
