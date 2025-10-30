import pandas as pd
import json
from datetime import datetime

# Ler todas as abas do Excel
excel_file = pd.ExcelFile('Lista Prospecçao.xlsx')

# Dicionário para armazenar todos os dados
all_data = {
    'estados': {},
    'segmentos': {},  # Novo: segmentos dinâmicos
    'oportunidades': [],
    'estatisticas': {}
}

# Processar abas de hospitais por estado
estados = ['SP', 'RS', 'SC', 'PR']
total_contatos = 0
total_ativos = 0

print("\n" + "="*50)
print("PROCESSANDO ESTADOS")
print("="*50)

for estado in estados:
    sheet_name = f'Hospitais {estado}'
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Converter para JSON
        records = df.to_dict('records')

        # Processar datas para formato ISO
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
        # Considerar ativos os que têm data de último contato
        total_ativos += len([r for r in records if r.get('DATA DO ÚLTIMO CONTATO ')])

        print(f"[OK] Processado {sheet_name}: {len(records)} registros")
    except Exception as e:
        print(f"[ERRO] Erro ao processar {sheet_name}: {e}")

# Processar outros segmentos (abas que não sejam estados ou oportunidades)
print("\n" + "="*50)
print("PROCESSANDO SEGMENTOS")
print("="*50)

for sheet_name in excel_file.sheet_names:
    # Pular abas de estados e oportunidades
    if sheet_name.startswith('Hospitais ') or sheet_name == 'Oportunidades':
        continue

    try:
        df = pd.read_excel(excel_file, sheet_name)
        records = df.to_dict('records')

        # Processar datas para formato ISO
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, pd.Timestamp):
                    record[key] = value.isoformat()

        # Criar segmento dinamicamente
        segment_key = sheet_name.lower().replace(' ', '_')
        all_data['segmentos'][segment_key] = {
            'nome': sheet_name,
            'data': records,
            'total': len(records),
            'colunas': list(df.columns)
        }

        print(f"[OK] Processado segmento '{sheet_name}': {len(records)} registros")
    except Exception as e:
        print(f"[ERRO] Erro ao processar segmento '{sheet_name}': {e}")

# Processar Oportunidades
print("\n" + "="*50)
print("PROCESSANDO OPORTUNIDADES")
print("="*50)

try:
    df_oportunidades = pd.read_excel(excel_file, 'Oportunidades')
    records = df_oportunidades.to_dict('records')

    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif isinstance(value, pd.Timestamp):
                record[key] = value.isoformat()

    all_data['oportunidades'] = records
    print(f"[OK] Processado Oportunidades: {len(records)} registros")
except Exception as e:
    print(f"[ERRO] Erro ao processar Oportunidades: {e}")

# Calcular estatísticas gerais
total_segmentos = sum(seg['total'] for seg in all_data['segmentos'].values())

all_data['estatisticas'] = {
    'total_contatos': total_contatos,
    'total_ativos': total_ativos,
    'taxa_resposta': round((total_ativos / total_contatos * 100) if total_contatos > 0 else 0, 1),
    'total_estados': len([k for k, v in all_data['estados'].items() if v['total'] > 0]),
    'total_segmentos': total_segmentos,
    'total_oportunidades': len(all_data['oportunidades'])
}

# Salvar dados processados
with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("\n" + "="*50)
print("RESUMO GERAL")
print("="*50)
print(f"Total de Contatos: {all_data['estatisticas']['total_contatos']}")
print(f"Contatos Ativos: {all_data['estatisticas']['total_ativos']}")
print(f"Taxa de Resposta: {all_data['estatisticas']['taxa_resposta']}%")
print(f"Estados Cobertos: {all_data['estatisticas']['total_estados']}")
print(f"\nSegmentos Processados:")
for key, seg in all_data['segmentos'].items():
    print(f"  - {seg['nome']}: {seg['total']} registros")
print(f"\nTotal de Oportunidades: {all_data['estatisticas']['total_oportunidades']}")
print("="*50)
print("\n[OK] Dados salvos em dashboard_data.json")
