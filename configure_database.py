"""
Script interativo para configurar a DATABASE_URL
"""
import os
import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def main():
    print_header("CONFIGURAÇÃO DA DATABASE_URL")

    print("\n📋 Passos para obter sua DATABASE_URL do Neon:\n")
    print("  1. Acesse: https://console.neon.tech/")
    print("  2. Faça login ou crie uma conta")
    print("  3. Crie um projeto (ou selecione um existente)")
    print("  4. Vá em 'Connection Details'")
    print("  5. Copie a 'Connection String' (PostgreSQL)")
    print("\n  A string deve ter este formato:")
    print("  postgresql://usuario:senha@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require")

    print("\n" + "-"*70)

    database_url = input("\n✏️  Cole aqui sua DATABASE_URL do Neon: ").strip()

    # Validação básica
    if not database_url:
        print("\n❌ Nenhuma URL fornecida. Cancelando...")
        sys.exit(1)

    if not database_url.startswith('postgresql://'):
        print("\n❌ URL inválida. Deve começar com 'postgresql://'")
        sys.exit(1)

    if 'neon.tech' not in database_url and 'neon' not in database_url:
        print("\n⚠️  Aviso: Esta não parece ser uma URL do Neon")
        confirm = input("   Deseja continuar mesmo assim? (s/n): ")
        if confirm.lower() != 's':
            print("\nCancelando...")
            sys.exit(1)

    # Criar arquivo .env
    print("\n📝 Criando arquivo .env...")
    with open('.env', 'w', encoding='utf-8') as f:
        f.write("# Configuração do Banco de Dados Neon PostgreSQL\n")
        f.write(f"DATABASE_URL={database_url}\n")

    print("✅ Arquivo .env criado com sucesso!")

    # Testar conexão
    print("\n🔌 Testando conexão com o banco...")
    try:
        os.environ['DATABASE_URL'] = database_url
        from database.db import Database
        db = Database()
        db.init_database()
        print("✅ Conexão estabelecida com sucesso!")
        print("✅ Schema do banco inicializado!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print("\n⚠️  O arquivo .env foi criado, mas há um problema com a conexão.")
        print("   Verifique se a DATABASE_URL está correta.")
        sys.exit(1)

    # Verificar se há dados para migrar
    if os.path.exists('all_sheets_data.json'):
        print("\n📊 Dados locais encontrados!")
        migrate = input("   Deseja migrar os dados agora? (s/n): ")
        if migrate.lower() == 's':
            print("\n🚀 Iniciando migração...")
            import subprocess
            result = subprocess.run(['python', 'migrate_to_neon.py'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Migração concluída!")
            else:
                print(f"❌ Erro na migração:\n{result.stderr}")
        else:
            print("\n   Você pode migrar depois executando: python migrate_to_neon.py")
    else:
        print("\n⚠️  Arquivo all_sheets_data.json não encontrado")
        print("   Você precisará fazer upload de planilhas após o deploy")

    # Instruções para Vercel
    print("\n" + "="*70)
    print("  PRÓXIMO PASSO: CONFIGURAR NO VERCEL")
    print("="*70)
    print("\n📤 Para fazer o deploy funcionar, você precisa:")
    print("\n  OPÇÃO 1 - Pelo terminal:")
    print("    vercel env add DATABASE_URL")
    print("    (Cole a mesma DATABASE_URL quando solicitado)")
    print("\n  OPÇÃO 2 - Pela web:")
    print("    1. Acesse: https://vercel.com/dashboard")
    print("    2. Selecione seu projeto 'dashboard-comercial'")
    print("    3. Vá em Settings > Environment Variables")
    print("    4. Adicione DATABASE_URL com o mesmo valor")
    print("\n  Depois execute:")
    print("    vercel --prod")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Configuração cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
