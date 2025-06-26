import pandas as pd
import datetime as dt
import requests
from io import BytesIO
from zipfile import ZipFile
import matplotlib.pyplot as plt

def baixar_cotas_cvm_teste(year_month):
    """Versão de teste para baixar dados da CVM"""
    ano, mes = year_month
    url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes:02d}.zip'
    print(f"Tentando baixar: {url}")
    
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        print("✅ Download OK")
        
        zin = ZipFile(BytesIO(resp.content))
        filename = next(f for f in zin.namelist() if f.endswith('.csv'))
        print(f"✅ Arquivo: {filename}")
        
        # Ler apenas as primeiras 1000 linhas para teste
        df = pd.read_csv(zin.open(filename), sep=';', decimal=',', nrows=1000)
        print(f"✅ DataFrame: {len(df)} registros")
        return df
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

# Teste simples
print("=== TESTE DE DOWNLOAD DA CVM ===")
df_teste = baixar_cotas_cvm_teste((2025, 3))

if df_teste is not None:
    print("\n=== COLUNAS DISPONÍVEIS ===")
    print(df_teste.columns.tolist())
    
    print("\n=== PRIMEIROS REGISTROS ===")
    print(df_teste.head())
    
    # Teste simples de gráfico
    print("\n=== TESTE DE GRÁFICO ===")
    plt.figure(figsize=(8, 4))
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3], 'o-', label='Teste')
    plt.title('Gráfico de Teste')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    
    # Tentar mostrar
    try:
        plt.show(block=False)
        print("✅ Gráfico plotado!")
    except:
        try:
            plt.savefig('teste_grafico.png')
            print("✅ Gráfico salvo como teste_grafico.png")
        except Exception as e:
            print(f"❌ Erro no gráfico: {e}")
    
else:
    print("❌ Falha no download")
