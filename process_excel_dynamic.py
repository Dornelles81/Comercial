"""
Script dinâmico para processar qualquer planilha Excel com múltiplas abas
Detecta automaticamente todas as abas e gera estatísticas
"""

import pandas as pd
import json
from datetime import datetime
import numpy as np
import sys

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

    # Procurar por colunas de nome
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

    # Estatísticas de tipo (público/privado)
    if column_info['tipo']:
        tipo_counts = df[column_info['tipo']].value_counts().to_dict()
        stats['por_tipo'] = tipo_counts

    # Estatísticas de cidade
    if column_info['cidade']:
        cidade_counts = df[column_info['cidade']].value_counts().head(10).to_dict()
        stats['top_cidades'] = cidade_counts

    # Estatísticas de contatos
    if column_info['data_contato']:
        contatos_realizados = df[column_info['data_contato']].notna().sum()
        stats['contatos_realizados'] = int(contatos_realizados)
        stats['contatos_pendentes'] = int(len(df) - contatos_realizados)

    # Estatísticas de contratos
    if column_info['contrato']:
        contratos = df[column_info['contrato']].notna().sum()
        stats['com_contrato'] = int(contratos)
        stats['sem_contrato'] = int(len(df) - contratos)

    # Estatísticas de grupo
    if column_info['grupo']:
        grupo_counts = df[column_info['grupo']].value_counts().head(10).to_dict()
        stats['top_grupos'] = grupo_counts

    # Estatísticas temporais de contatos
    if column_info['data_contato']:
        try:
            # Converter para datetime
            df_temp = df.copy()
            df_temp['data_temp'] = pd.to_datetime(df_temp[column_info['data_contato']], errors='coerce')

            # Filtrar apenas datas válidas
            df_temp = df_temp[df_temp['data_temp'].notna()]

            if len(df_temp) > 0:
                # Contatos por mês
                df_temp['mes_ano'] = df_temp['data_temp'].dt.to_period('M').astype(str)
                contatos_por_mes = df_temp['mes_ano'].value_counts().sort_index().to_dict()
                stats['evolucao_temporal'] = contatos_por_mes

                # Contatos por ano
                df_temp['ano'] = df_temp['data_temp'].dt.year
                contatos_por_ano = df_temp['ano'].value_counts().sort_index().to_dict()
                stats['contatos_por_ano'] = {str(k): int(v) for k, v in contatos_por_ano.items()}

                # Últimos 12 meses
                from datetime import datetime, timedelta
                hoje = datetime.now()
                doze_meses_atras = hoje - timedelta(days=365)
                df_temp_12m = df_temp[df_temp['data_temp'] >= doze_meses_atras]

                if len(df_temp_12m) > 0:
                    contatos_12m = df_temp_12m['mes_ano'].value_counts().sort_index().to_dict()
                    stats['ultimos_12_meses'] = contatos_12m
        except Exception as e:
            print(f"  [AVISO] Erro ao processar dados temporais: {e}")

    # Verificar se há coluna de operação de estacionamento
    for col in df.columns:
        if 'estacionamento' in str(col).lower() and 'oper' in str(col).lower():
            opera_est = df[col].value_counts().to_dict()
            stats['operacao_estacionamento'] = opera_est
            break

    # Verificar se há coluna de cobrança de estacionamento
    for col in df.columns:
        if 'cobra' in str(col).lower():
            cobra = df[col].value_counts().to_dict()
            stats['cobra_estacionamento'] = cobra
            break

    return stats

def process_excel(file_path, output_path='all_sheets_data.json'):
    """
    Processa qualquer arquivo Excel detectando automaticamente as abas e estrutura

    Args:
        file_path: Caminho para o arquivo Excel
        output_path: Caminho para salvar o JSON de saída

    Returns:
        dict: Dados processados
    """
    print(f"\n{'='*60}")
    print(f"PROCESSANDO ARQUIVO: {file_path}")
    print('='*60)

    # Ler o arquivo Excel
    excel_file = pd.ExcelFile(file_path)

    print(f"\n[OK] Abas detectadas: {len(excel_file.sheet_names)}")
    for idx, name in enumerate(excel_file.sheet_names, 1):
        print(f"  {idx}. {name}")

    all_data = {
        'sheets': [],
        'last_updated': datetime.now().isoformat(),
        'source_file': file_path
    }

    # Processar cada aba
    for sheet_name in excel_file.sheet_names:
        print(f"\n{'-'*60}")
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

        # Detectar tipos de colunas
        column_info = detect_column_types(df)

        sheet_data = {
            'name': sheet_name,
            'total_records': len(df),
            'columns': list(df.columns),
            'records': df.to_dict('records'),
            'column_mapping': column_info
        }

        # Calcular estatísticas
        stats = calculate_statistics(df, column_info)
        if stats:
            sheet_data['statistics'] = stats

        all_data['sheets'].append(sheet_data)

        print(f"  [OK] Registros: {len(df)}")
        print(f"  [OK] Colunas: {len(df.columns)}")
        if stats:
            print(f"  [OK] Estatisticas geradas: {len(stats)} metricas")

    # Limpar NaN de todos os dados
    all_data_clean = clean_nan(all_data)

    # Salvar tudo em um JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data_clean, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"[OK] PROCESSAMENTO CONCLUIDO")
    print('='*60)
    print(f"Total de abas processadas: {len(all_data['sheets'])}")
    for sheet in all_data['sheets']:
        print(f"  - {sheet['name']}: {sheet['total_records']} registros")
    print(f"\n[OK] Dados salvos em: {output_path}")
    print('='*60)

    return all_data_clean

if __name__ == "__main__":
    # Verificar se foi passado um arquivo como argumento
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        excel_file = 'Lista Prospecçao.xlsx'

    try:
        process_excel(excel_file)
    except FileNotFoundError:
        print(f"\n[ERRO] Arquivo '{excel_file}' nao encontrado!")
        print("\nUso: python process_excel_dynamic.py [caminho_do_arquivo.xlsx]")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO] Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
