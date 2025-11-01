"""
API Serverless para upload e processamento de Excel
Vercel Function
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.db import Database
from werkzeug.utils import secure_filename
import tempfile
import pandas as pd
from datetime import datetime
import numpy as np

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_nan(obj):
    """Recursivamente converte NaN, inf, e -inf para None"""
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(item) for item in obj]
    elif isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    else:
        return obj

def detect_column_types(df):
    """Detecta automaticamente os tipos de colunas importantes"""
    column_info = {
        'nome': None,
        'tipo': None,
        'cidade': None,
        'contato': None,
        'data_contato': None,
        'contrato': None,
        'grupo': None
    }

    for col in df.columns:
        col_lower = str(col).lower().strip()
        if 'nome' in col_lower and not column_info['nome']:
            column_info['nome'] = col
        elif 'tipo' in col_lower or 'público' in col_lower or 'privado' in col_lower:
            column_info['tipo'] = col
        elif 'cidade' in col_lower:
            column_info['cidade'] = col
        elif 'data' in col_lower and 'contato' in col_lower:
            column_info['data_contato'] = col
        elif 'contrato' in col_lower:
            column_info['contrato'] = col
        elif 'grupo' in col_lower:
            column_info['grupo'] = col

    return column_info

def calculate_statistics(df, column_info):
    """Calcula estatísticas baseadas nas colunas detectadas"""
    stats = {}

    if column_info['tipo']:
        tipo_counts = df[column_info['tipo']].value_counts().to_dict()
        stats['por_tipo'] = tipo_counts

    if column_info['cidade']:
        cidade_counts = df[column_info['cidade']].value_counts().head(10).to_dict()
        stats['top_cidades'] = cidade_counts

    if column_info['data_contato']:
        contatos_realizados = df[column_info['data_contato']].notna().sum()
        stats['contatos_realizados'] = int(contatos_realizados)
        stats['contatos_pendentes'] = int(len(df) - contatos_realizados)

    if column_info['contrato']:
        contratos = df[column_info['contrato']].notna().sum()
        stats['com_contrato'] = int(contratos)
        stats['sem_contrato'] = int(len(df) - contratos)

    if column_info['grupo']:
        grupo_counts = df[column_info['grupo']].value_counts().head(10).to_dict()
        stats['top_grupos'] = grupo_counts

    # Estatísticas temporais
    if column_info['data_contato']:
        try:
            df_temp = df.copy()
            df_temp['data_temp'] = pd.to_datetime(df_temp[column_info['data_contato']], errors='coerce')
            df_temp = df_temp[df_temp['data_temp'].notna()]

            if len(df_temp) > 0:
                df_temp['mes_ano'] = df_temp['data_temp'].dt.to_period('M').astype(str)
                contatos_por_mes = df_temp['mes_ano'].value_counts().sort_index().to_dict()
                stats['evolucao_temporal'] = contatos_por_mes

                df_temp['ano'] = df_temp['data_temp'].dt.year
                contatos_por_ano = df_temp['ano'].value_counts().sort_index().to_dict()
                stats['contatos_por_ano'] = {str(k): int(v) for k, v in contatos_por_ano.items()}

                from datetime import timedelta
                hoje = datetime.now()
                doze_meses_atras = hoje - timedelta(days=365)
                df_temp_12m = df_temp[df_temp['data_temp'] >= doze_meses_atras]

                if len(df_temp_12m) > 0:
                    contatos_12m = df_temp_12m['mes_ano'].value_counts().sort_index().to_dict()
                    stats['ultimos_12_meses'] = contatos_12m
        except Exception as e:
            print(f"[AVISO] Erro ao processar dados temporais: {e}")

    # Opera estacionamento
    for col in df.columns:
        if 'estacionamento' in str(col).lower() and 'oper' in str(col).lower():
            opera_est = df[col].value_counts().to_dict()
            stats['operacao_estacionamento'] = opera_est
            break

    return stats

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Endpoint para upload de arquivo Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido'}), 400

        # Salvar temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        # Processar Excel
        excel_file = pd.ExcelFile(tmp_path)
        db = Database()

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            df.columns = df.columns.str.strip()

            # Converter datas para string
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].astype(str).replace('NaT', None)

            df = df.where(pd.notna(df), None)

            column_info = detect_column_types(df)
            stats = calculate_statistics(df, column_info)

            sheet_data = {
                'name': sheet_name,
                'total_records': len(df),
                'records': df.to_dict('records'),
                'statistics': stats,
                'column_mapping': column_info,
                'source_file': secure_filename(file.filename)
            }

            sheet_data_clean = clean_nan(sheet_data)
            db.save_sheet_data(sheet_data_clean)

        # Remover arquivo temporário
        os.unlink(tmp_path)

        return jsonify({
            'success': True,
            'message': 'Arquivo processado com sucesso',
            'sheets_count': len(excel_file.sheet_names)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Vercel handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
