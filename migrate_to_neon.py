"""
Script para migrar dados do JSON local para o banco Neon
"""
import json
import os
from database.db import Database

def migrate_data():
    """Migra dados do all_sheets_data.json para o banco Neon"""

    print("\n" + "="*60)
    print("MIGRAÇÃO DE DADOS PARA NEON")
    print("="*60)

    # Verificar DATABASE_URL
    if not os.getenv('DATABASE_URL'):
        print("\n[ERRO] DATABASE_URL não configurada!")
        print("Configure a variável de ambiente DATABASE_URL com a connection string do Neon")
        print("\nExemplo (Windows):")
        print('set DATABASE_URL=postgresql://user:pass@host.neon.tech/dbname?sslmode=require')
        print("\nExemplo (Linux/Mac):")
        print('export DATABASE_URL=postgresql://user:pass@host.neon.tech/dbname?sslmode=require')
        return False

    # Verificar se arquivo JSON existe
    if not os.path.exists('all_sheets_data.json'):
        print("\n[ERRO] Arquivo 'all_sheets_data.json' não encontrado!")
        print("Execute 'python process_excel_dynamic.py' primeiro")
        return False

    print("\n[OK] DATABASE_URL configurada")
    print("[OK] Arquivo JSON encontrado")

    # Conectar ao banco
    print("\n[1/3] Conectando ao banco Neon...")
    try:
        db = Database()
        print("[OK] Conexão estabelecida!")
    except Exception as e:
        print(f"[ERRO] Falha ao conectar: {e}")
        return False

    # Inicializar schema
    print("\n[2/3] Inicializando schema do banco...")
    try:
        db.init_database()
        print("[OK] Schema criado com sucesso!")
    except Exception as e:
        print(f"[AVISO] Erro ao criar schema (pode já existir): {e}")

    # Carregar dados do JSON
    print("\n[3/3] Migrando dados do JSON...")
    with open('all_sheets_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    sheets = data.get('sheets', [])
    print(f"[OK] {len(sheets)} sheets encontradas no JSON")

    # Migrar cada sheet
    success_count = 0
    for sheet in sheets:
        try:
            print(f"\n  -> Migrando '{sheet['name']}'...")
            print(f"     Total de registros: {sheet['total_records']}")

            sheet_id = db.save_sheet_data(sheet)

            print(f"     [OK] Sheet salva com ID: {sheet_id}")
            success_count += 1
        except Exception as e:
            print(f"     [ERRO] Falha ao migrar: {e}")

    print("\n" + "="*60)
    print(f"MIGRAÇÃO CONCLUÍDA: {success_count}/{len(sheets)} sheets migradas")
    print("="*60)

    # Verificar dados migrados
    print("\n[VERIFICAÇÃO] Buscando dados do banco...")
    try:
        all_data = db.get_all_sheets_data()
        print(f"[OK] {len(all_data['sheets'])} sheets no banco")
        for sheet in all_data['sheets']:
            print(f"  - {sheet['name']}: {sheet['total_records']} registros")
    except Exception as e:
        print(f"[ERRO] Falha ao verificar: {e}")
        return False

    print("\n[OK] Migração concluída com sucesso!")
    return True

if __name__ == "__main__":
    try:
        success = migrate_data()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERRO FATAL] {e}")
        import traceback
        traceback.print_exc()
        exit(1)
