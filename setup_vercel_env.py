"""
Script para configurar DATABASE_URL no Vercel via CLI
"""
import subprocess
import sys

def setup_vercel_env():
    """Configura DATABASE_URL no Vercel"""

    database_url = "postgresql://neondb_owner:npg_v0rVhpLa5BHD@ep-patient-frost-acio5b40-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

    print("Configurando DATABASE_URL no Vercel...")
    print(f"Valor: {database_url[:50]}...")

    try:
        # Executar comando vercel env add
        process = subprocess.Popen(
            ['vercel', 'env', 'add', 'DATABASE_URL', 'production'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Enviar a DATABASE_URL via stdin
        stdout, stderr = process.communicate(input=f"{database_url}\n")

        if process.returncode == 0:
            print("✓ DATABASE_URL configurada para Production!")
        else:
            print(f"Erro: {stderr}")
            return False

        # Preview
        process = subprocess.Popen(
            ['vercel', 'env', 'add', 'DATABASE_URL', 'preview'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=f"{database_url}\n")

        if process.returncode == 0:
            print("✓ DATABASE_URL configurada para Preview!")

        # Development
        process = subprocess.Popen(
            ['vercel', 'env', 'add', 'DATABASE_URL', 'development'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=f"{database_url}\n")

        if process.returncode == 0:
            print("✓ DATABASE_URL configurada para Development!")

        print("\n✅ DATABASE_URL configurada em todos os ambientes!")
        return True

    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    success = setup_vercel_env()
    sys.exit(0 if success else 1)
