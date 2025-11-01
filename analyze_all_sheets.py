import pandas as pd
import json

# Ler o arquivo Excel
excel_file = pd.ExcelFile('Lista Prospecçao.xlsx')

print("=== Abas disponíveis na planilha ===")
print(excel_file.sheet_names)
print(f"\nTotal de abas: {len(excel_file.sheet_names)}")

# Analisar cada aba
for sheet_name in excel_file.sheet_names:
    print(f"\n{'='*60}")
    print(f"ABA: {sheet_name}")
    print('='*60)

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    print(f"Linhas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    print(f"\nPrimeiras linhas:")
    print(df.head(3))
