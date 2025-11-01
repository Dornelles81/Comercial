-- Schema para Dashboard Comercial
-- PostgreSQL (Neon)

-- Tabela de Sheets (abas da planilha)
CREATE TABLE IF NOT EXISTS sheets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    total_records INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Records (registros individuais de cada sheet)
CREATE TABLE IF NOT EXISTS records (
    id SERIAL PRIMARY KEY,
    sheet_id INTEGER REFERENCES sheets(id) ON DELETE CASCADE,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para busca rápida por sheet
CREATE INDEX IF NOT EXISTS idx_records_sheet_id ON records(sheet_id);

-- Índice para busca em campos JSONB comuns
-- GIN index for JSONB data (full document search)
CREATE INDEX IF NOT EXISTS idx_records_data ON records USING GIN (data);

-- Tabela de Estatísticas (dados agregados por sheet)
CREATE TABLE IF NOT EXISTS statistics (
    id SERIAL PRIMARY KEY,
    sheet_id INTEGER REFERENCES sheets(id) ON DELETE CASCADE,
    stats_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sheet_id)
);

-- Tabela de Column Mapping (mapeamento de colunas detectadas)
CREATE TABLE IF NOT EXISTS column_mappings (
    id SERIAL PRIMARY KEY,
    sheet_id INTEGER REFERENCES sheets(id) ON DELETE CASCADE,
    mapping JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sheet_id)
);

-- View para facilitar queries (join de sheet + statistics)
CREATE OR REPLACE VIEW sheet_summary AS
SELECT
    s.id,
    s.name,
    s.total_records,
    s.last_updated,
    s.source_file,
    st.stats_data,
    cm.mapping as column_mapping
FROM sheets s
LEFT JOIN statistics st ON s.id = st.sheet_id
LEFT JOIN column_mappings cm ON s.id = cm.sheet_id;

-- Comentários para documentação
COMMENT ON TABLE sheets IS 'Armazena informações sobre cada aba da planilha Excel';
COMMENT ON TABLE records IS 'Armazena os registros individuais de cada sheet em formato JSONB';
COMMENT ON TABLE statistics IS 'Armazena estatísticas agregadas por sheet (contatos, contratos, etc)';
COMMENT ON TABLE column_mappings IS 'Armazena o mapeamento de colunas detectadas automaticamente';
