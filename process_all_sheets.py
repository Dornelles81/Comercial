import pandas as pd
import json
from datetime import datetime
import numpy as np

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

# Ler o arquivo Excel
excel_file = pd.ExcelFile('Lista Prospecçao.xlsx')

all_data = {
    'sheets': [],
    'last_updated': datetime.now().isoformat()
}

# Processar cada aba
for sheet_name in excel_file.sheet_names:
    print(f"Processando: {sheet_name}")

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Limpar nomes de colunas
    df.columns = df.columns.str.strip()

    # Converter datas para string
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str).replace('NaT', None)

    # Converter NaN para None
    df = df.where(pd.notna(df), None)

    sheet_data = {
        'name': sheet_name,
        'total_records': len(df),
        'columns': list(df.columns),
        'records': df.to_dict('records')
    }

    # Calcular estatísticas específicas para cada tipo de aba
    if sheet_name != 'Oportunidades':
        # Para abas de hospitais e parques
        stats = {}

        # Tipo Público/Privado
        if 'PÚBLICO / PRIVADO' in df.columns:
            tipo_counts = df['PÚBLICO / PRIVADO'].value_counts().to_dict()
            stats['por_tipo'] = tipo_counts

        # Por cidade
        if 'CIDADE' in df.columns:
            cidade_counts = df['CIDADE'].value_counts().head(10).to_dict()
            stats['top_cidades'] = cidade_counts

        # Contatos realizados
        if 'DATA DO ÚLTIMO CONTATO' in df.columns:
            contatos_realizados = df['DATA DO ÚLTIMO CONTATO'].notna().sum()
            stats['contatos_realizados'] = int(contatos_realizados)
            stats['contatos_pendentes'] = int(len(df) - contatos_realizados)

        # Contratos
        if 'CONTRATO' in df.columns:
            contratos = df['CONTRATO'].notna().sum()
            stats['com_contrato'] = int(contratos)
            stats['sem_contrato'] = int(len(df) - contratos)

        # Opera estacionamento
        if 'OPER. ESTACIONAMENTO' in df.columns:
            opera_est = df['OPER. ESTACIONAMENTO'].value_counts().to_dict()
            stats['operacao_estacionamento'] = opera_est

        # Cobra estacionamento
        if 'COBRA' in df.columns:
            cobra = df['COBRA'].value_counts().to_dict()
            stats['cobra_estacionamento'] = cobra

        sheet_data['statistics'] = stats

    all_data['sheets'].append(sheet_data)

# Limpar NaN de todos os dados
all_data_clean = clean_nan(all_data)

# Salvar tudo em um JSON
with open('all_sheets_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data_clean, f, ensure_ascii=False, indent=2)

print("\n=== Processamento concluído ===")
print(f"Total de abas processadas: {len(all_data['sheets'])}")
for sheet in all_data['sheets']:
    print(f"  - {sheet['name']}: {sheet['total_records']} registros")
print("\nDados salvos em: all_sheets_data.json")
