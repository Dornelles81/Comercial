"""
Módulo de interação com banco de dados Neon PostgreSQL
"""
import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from datetime import datetime

class Database:
    def __init__(self, connection_string=None):
        """
        Inicializa conexão com o banco
        connection_string: URL de conexão do Neon (env var DATABASE_URL)
        """
        self.connection_string = connection_string or os.getenv('DATABASE_URL')
        if not self.connection_string:
            raise ValueError("DATABASE_URL não configurada")

    def get_connection(self):
        """Retorna uma conexão com o banco"""
        return psycopg2.connect(self.connection_string)

    def execute_query(self, query, params=None, fetch=False):
        """Executa uma query SQL"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params or ())
                if fetch:
                    return cur.fetchall()
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()

    def save_sheet_data(self, sheet_data):
        """
        Salva dados de uma sheet completa no banco

        Args:
            sheet_data: dict com keys: name, total_records, records, statistics, column_mapping

        Returns:
            sheet_id: ID da sheet salva
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # 1. Inserir ou atualizar sheet
                cur.execute("""
                    INSERT INTO sheets (name, total_records, source_file)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (name) DO UPDATE
                    SET total_records = EXCLUDED.total_records,
                        last_updated = CURRENT_TIMESTAMP
                    RETURNING id
                """, (
                    sheet_data['name'],
                    sheet_data['total_records'],
                    sheet_data.get('source_file', '')
                ))
                sheet_id = cur.fetchone()[0]

                # 2. Deletar records antigos
                cur.execute("DELETE FROM records WHERE sheet_id = %s", (sheet_id,))

                # 3. Inserir novos records
                for record in sheet_data.get('records', []):
                    cur.execute("""
                        INSERT INTO records (sheet_id, data)
                        VALUES (%s, %s)
                    """, (sheet_id, Json(record)))

                # 4. Salvar/atualizar statistics
                if sheet_data.get('statistics'):
                    cur.execute("""
                        INSERT INTO statistics (sheet_id, stats_data)
                        VALUES (%s, %s)
                        ON CONFLICT (sheet_id) DO UPDATE
                        SET stats_data = EXCLUDED.stats_data,
                            created_at = CURRENT_TIMESTAMP
                    """, (sheet_id, Json(sheet_data['statistics'])))

                # 5. Salvar/atualizar column_mapping
                if sheet_data.get('column_mapping'):
                    cur.execute("""
                        INSERT INTO column_mappings (sheet_id, mapping)
                        VALUES (%s, %s)
                        ON CONFLICT (sheet_id) DO UPDATE
                        SET mapping = EXCLUDED.mapping,
                            created_at = CURRENT_TIMESTAMP
                    """, (sheet_id, Json(sheet_data['column_mapping'])))

                conn.commit()
                return sheet_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_all_sheets_data(self):
        """
        Retorna todos os dados em formato compatível com o dashboard
        (mesmo formato do all_sheets_data.json)
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Buscar todas as sheets com suas estatísticas
                cur.execute("""
                    SELECT
                        s.id,
                        s.name,
                        s.total_records,
                        s.last_updated,
                        s.source_file,
                        st.stats_data as statistics,
                        cm.mapping as column_mapping
                    FROM sheets s
                    LEFT JOIN statistics st ON s.id = st.sheet_id
                    LEFT JOIN column_mappings cm ON s.id = cm.sheet_id
                    ORDER BY s.name
                """)
                sheets = cur.fetchall()

                # Para cada sheet, buscar seus records
                result = {
                    'sheets': [],
                    'last_updated': datetime.now().isoformat()
                }

                for sheet in sheets:
                    cur.execute("""
                        SELECT data FROM records
                        WHERE sheet_id = %s
                        ORDER BY id
                    """, (sheet['id'],))
                    records = [r['data'] for r in cur.fetchall()]

                    # Buscar colunas únicas dos records
                    columns = []
                    if records:
                        columns = list(records[0].keys())

                    result['sheets'].append({
                        'name': sheet['name'],
                        'total_records': sheet['total_records'],
                        'columns': columns,
                        'records': records,
                        'statistics': sheet['statistics'] or {},
                        'column_mapping': sheet['column_mapping'] or {}
                    })

                return result
        finally:
            conn.close()

    def delete_all_data(self):
        """Limpa todos os dados (útil para testes)"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE sheets CASCADE")
                conn.commit()
        finally:
            conn.close()

    def init_database(self, schema_file='database/schema.sql'):
        """Inicializa o banco com o schema"""
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = f.read()

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(schema)
                conn.commit()
                print("[OK] Database inicializado com sucesso!")
        finally:
            conn.close()
