"""
Script automatizado para configurar e fazer deploy do dashboard
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(step, text):
    print(f"\n[{step}] {text}")

def run_command(cmd, description):
    """Executa um comando e retorna o resultado"""
    print(f"  Executando: {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ Sucesso!")
            return True, result.stdout
        else:
            print(f"  ✗ Erro: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"  ✗ Exceção: {e}")
        return False, str(e)

def check_env_file():
    """Verifica se o arquivo .env existe"""
    if os.path.exists('.env'):
        print("  ✓ Arquivo .env encontrado")
        return True
    else:
        print("  ✗ Arquivo .env não encontrado")
        return False

def check_database_url():
    """Verifica se DATABASE_URL está configurada"""
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgresql://'):
        print("  ✓ DATABASE_URL configurada")
        print(f"  Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'N/A'}")
        return True
    else:
        print("  ✗ DATABASE_URL não configurada ou inválida")
        return False

def setup():
    """Executa o setup completo"""
    print_header("SETUP E DEPLOY DO DASHBOARD COMERCIAL")

    # 1. Verificar .env
    print_step("1/6", "Verificando arquivo .env")
    if not check_env_file():
        print("\n  AÇÃO NECESSÁRIA:")
        print("  1. Crie uma conta no Neon: https://console.neon.tech/signup")
        print("  2. Copie a Connection String do seu projeto")
        print("  3. Execute: copy .env.example .env")
        print("  4. Cole a DATABASE_URL no arquivo .env")
        print("\n  Depois execute este script novamente.")
        return False

    # 2. Verificar DATABASE_URL
    print_step("2/6", "Verificando DATABASE_URL")

    # Carregar .env
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

    if not check_database_url():
        print("\n  AÇÃO NECESSÁRIA:")
        print("  1. Abra o arquivo .env")
        print("  2. Cole sua DATABASE_URL do Neon")
        print("  3. Salve o arquivo")
        print("\n  Depois execute este script novamente.")
        return False

    # 3. Testar conexão com banco
    print_step("3/6", "Testando conexão com o banco")
    try:
        from database.db import Database
        db = Database()
        print("  ✓ Conexão com o banco estabelecida!")
    except Exception as e:
        print(f"  ✗ Erro ao conectar: {e}")
        print("\n  Verifique se a DATABASE_URL está correta")
        return False

    # 4. Migrar dados
    print_step("4/6", "Migrando dados locais para o Neon")
    if os.path.exists('all_sheets_data.json'):
        success, output = run_command('python migrate_to_neon.py', 'Executando migração')
        if not success:
            print("  ⚠ Erro na migração, mas continuando...")
    else:
        print("  ⚠ Arquivo all_sheets_data.json não encontrado")
        print("  Você precisará fazer upload de uma planilha após o deploy")

    # 5. Configurar DATABASE_URL no Vercel
    print_step("5/6", "Configurando DATABASE_URL no Vercel")
    print("\n  VOCÊ PRECISA FAZER MANUALMENTE:")
    print("  Execute: vercel env add DATABASE_URL")
    print("  Ou configure em: https://vercel.com/dashboard > Settings > Environment Variables")
    input("\n  Pressione ENTER após configurar no Vercel...")

    # 6. Deploy no Vercel
    print_step("6/6", "Fazendo deploy no Vercel")
    success, output = run_command('vercel --prod', 'Deploy em produção')
    if success:
        print("\n  ✓ Deploy concluído com sucesso!")
        print("\n  URL do deploy:")
        # Extrair URL do output
        for line in output.split('\n'):
            if 'https://' in line:
                print(f"    {line.strip()}")
    else:
        print("  ✗ Erro no deploy")
        return False

    print_header("SETUP CONCLUÍDO!")
    print("\n  Próximos passos:")
    print("  1. Acesse a URL do deploy")
    print("  2. Verifique se os dados estão carregando")
    print("  3. Teste o upload de uma planilha")
    print("\n")

    return True

if __name__ == "__main__":
    try:
        success = setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n  Setup cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n  ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
