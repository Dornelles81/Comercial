from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configurações
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel_file(filepath):
    """Processa o arquivo Excel e gera dashboard_data.json"""
    try:
        excel_file = pd.ExcelFile(filepath)

        all_data = {
            'estados': {},
            'segmentos': {},
            'oportunidades': [],
            'estatisticas': {}
        }

        estados = ['SP', 'RS', 'SC', 'PR']
        total_contatos = 0
        total_ativos = 0

        # Processar estados
        for estado in estados:
            sheet_name = f'Hospitais {estado}'
            if sheet_name not in excel_file.sheet_names:
                continue

            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            records = df.to_dict('records')

            # Processar datas
            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif isinstance(value, pd.Timestamp):
                        record[key] = value.isoformat()

            all_data['estados'][estado] = {
                'data': records,
                'total': len(records),
                'com_contrato': len([r for r in records if r.get('CONTRATO')]),
                'sem_contrato': len([r for r in records if not r.get('CONTRATO')])
            }

            total_contatos += len(records)
            total_ativos += len([r for r in records if r.get('DATA DO ÚLTIMO CONTATO ')])

        # Processar outros segmentos
        for sheet_name in excel_file.sheet_names:
            if sheet_name.startswith('Hospitais ') or sheet_name == 'Oportunidades':
                continue

            df = pd.read_excel(excel_file, sheet_name)
            records = df.to_dict('records')

            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif isinstance(value, pd.Timestamp):
                        record[key] = value.isoformat()

            segment_key = sheet_name.lower().replace(' ', '_')
            all_data['segmentos'][segment_key] = {
                'nome': sheet_name,
                'data': records,
                'total': len(records),
                'colunas': list(df.columns)
            }

        # Processar Oportunidades
        if 'Oportunidades' in excel_file.sheet_names:
            df_oportunidades = pd.read_excel(excel_file, 'Oportunidades')
            records = df_oportunidades.to_dict('records')

            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif isinstance(value, pd.Timestamp):
                        record[key] = value.isoformat()

            all_data['oportunidades'] = records

        # Calcular estatísticas
        total_segmentos = sum(seg['total'] for seg in all_data['segmentos'].values())

        all_data['estatisticas'] = {
            'total_contatos': total_contatos,
            'total_ativos': total_ativos,
            'taxa_resposta': round((total_ativos / total_contatos * 100) if total_contatos > 0 else 0, 1),
            'total_estados': len([k for k, v in all_data['estados'].items() if v['total'] > 0]),
            'total_segmentos': total_segmentos,
            'total_oportunidades': len(all_data['oportunidades'])
        }

        # Adicionar timestamp da atualização
        all_data['last_updated'] = datetime.now().isoformat()

        # Salvar dados processados
        with open('dashboard_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        return {
            'success': True,
            'message': 'Arquivo processado com sucesso!',
            'stats': all_data['estatisticas']
        }

    except Exception as e:
        return {
            'success': False,
            'message': f'Erro ao processar arquivo: {str(e)}'
        }

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

        # Processar arquivo
        result = process_excel_file(filepath)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no upload: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        with open('dashboard_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify({'success': True, 'stats': data['estatisticas']}), 200
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
