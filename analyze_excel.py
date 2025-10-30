import pandas as pd
import json

# Ler o arquivo Excel
df = pd.read_excel('Lista Prospecçao.xlsx')

# Exibir informações básicas
print("=== Informações do DataFrame ===")
print(f"Número de linhas: {len(df)}")
print(f"Número de colunas: {len(df.columns)}")
print(f"\nColunas: {list(df.columns)}")

print("\n=== Primeiras 5 linhas ===")
print(df.head())

print("\n=== Tipos de dados ===")
print(df.dtypes)

print("\n=== Valores únicos em cada coluna ===")
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} valores únicos")
    if unique_count < 20:
        print(f"  Valores: {df[col].unique().tolist()}")

# Salvar dados como JSON para usar no dashboard
df_json = df.to_json(orient='records', force_ascii=False)
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(df_json)

print("\n=== Dados salvos em data.json ===")
