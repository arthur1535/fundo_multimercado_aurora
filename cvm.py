import pandas as pd
import datetime as dt
import requests
from io import BytesIO
from zipfile import ZipFile

def baixar_cotas_cvm(year_month):
    """
    Baixa e retorna DataFrame com dados de cotas da CVM para o mês (ano, mês).
    """
    ano, mes = year_month
    url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes:02d}.zip'
    print(f"Baixando dados de {mes:02d}/{ano}...")
    print(f"URL: {url}")
    
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        print("Download concluído com sucesso!")
        
        zin = ZipFile(BytesIO(resp.content))
        filename = next(f for f in zin.namelist() if f.endswith('.csv'))
        print(f"Arquivo encontrado: {filename}")
        
        df = pd.read_csv(zin.open(filename), sep=';', decimal=',', 
                         parse_dates=['DT_COMPTC'], low_memory=False,
                         dtype={'VL_QUOTA': 'str', 'VL_TOTAL': 'str', 'VL_PATRIM_LIQ': 'str'})
        print(f"DataFrame criado com {len(df)} registros")
        return df
    except Exception as e:
        print(f"Erro ao baixar dados de {mes:02d}/{ano}: {e}")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

# ▶️ 1. Definir período de interesse
data_inicio = dt.date(2025, 3, 1)
data_fim = dt.date(2025, 6, 11)
datas = pd.date_range(data_inicio, data_fim, freq='MS').to_series().dt.date.tolist()

# ▶️ 2. Baixar dados mensais da CVM
print("Iniciando download dos dados da CVM...")
list_df = []
for dt in datas:
    df_temp = baixar_cotas_cvm((dt.year, dt.month))
    if not df_temp.empty:
        list_df.append(df_temp)

if not list_df:
    print("ERRO: Nenhum dado foi baixado!")
    exit()
    
print(f"Total de DataFrames baixados: {len(list_df)}")

# ▶️ 3. Combinar dados
df_all = pd.concat(list_df, ignore_index=True)
df_all['DT_COMPTC'] = pd.to_datetime(df_all['DT_COMPTC'])

# Imprime o nome das colunas
print(df_all.columns)

# Procura o nome correto ignorando maiúsculas/minúsculas e espaços
col_cnpj = [c for c in df_all.columns if 'cnpj' in c.lower()][0]
print(f"Coluna CNPJ identificada: {col_cnpj}")

# ▶️ 4. Filtrar pelo CNPJ alvo
cnpj_original = '29177012000178'
# Formatar CNPJ com pontos e barras para corresponder ao formato da CVM
cnpj_formatado = f"{cnpj_original[:2]}.{cnpj_original[2:5]}.{cnpj_original[5:8]}/{cnpj_original[8:12]}-{cnpj_original[12:]}"
print(f"CNPJ original: {cnpj_original}")
print(f"CNPJ formatado: {cnpj_formatado}")

df_raptor = df_all[df_all[col_cnpj] == cnpj_formatado].copy()
print(f"Registros encontrados para o CNPJ: {len(df_raptor)}")

if df_raptor.empty:
    print("ERRO: Nenhum registro encontrado para o CNPJ especificado!")
    print("Verificando CNPJs únicos no dataset...")
    print(df_all[col_cnpj].unique()[:10])  # Mostra os primeiros 10 CNPJs
    exit()

# ▶️ 5. Filtro de datas exatas
df_raptor = df_raptor[(df_raptor['DT_COMPTC'] >= pd.Timestamp(data_inicio)) &
                      (df_raptor['DT_COMPTC'] <= pd.Timestamp(data_fim))]
df_raptor = df_raptor.sort_values('DT_COMPTC')

# Converter VL_QUOTA para numérico (corrigir problema de tipo)
print("Convertendo VL_QUOTA para numérico...")
df_raptor['VL_QUOTA'] = pd.to_numeric(df_raptor['VL_QUOTA'], errors='coerce')
df_raptor = df_raptor.dropna(subset=['VL_QUOTA'])  # Remove linhas com valores inválidos
print(f"Registros válidos após conversão: {len(df_raptor)}")

# ▶️ 6. Calcular retorno acumulado
df_raptor['RET_DIARIO'] = df_raptor['VL_QUOTA'].pct_change()
df_raptor['ACUMULADO'] = (1 + df_raptor['RET_DIARIO']).cumprod() - 1

# ▶️ 7. Carregar dados da Selic para comparação
file_path_selic = 'D:/user/taxa_selic_apurada.csv'
df_selic = pd.read_csv(
    file_path_selic,
    sep=';',
    encoding='utf-8',
    skiprows=1,
    parse_dates=['Data'],
    dayfirst=True,
    decimal=','
)
df_selic = df_selic[['Data', 'Fator diário']]
# Converter 'Fator diário' para numérico
df_selic['Fator diário'] = pd.to_numeric(df_selic['Fator diário'], errors='coerce')
df_selic = df_selic.dropna(subset=['Fator diário'])
df_selic = df_selic.set_index('Data').sort_index()

# ▶️ 8. Comparar com CDI
cdi_acum = (df_selic.reindex(df_raptor['DT_COMPTC']).ffill()['Fator diário']
            .sub(1).add(1).cumprod().sub(1))
df_compare = pd.DataFrame({
    'DATA': df_raptor['DT_COMPTC'],
    'RAPTOR': df_raptor['ACUMULADO'].values,
    'CDI': cdi_acum.values
})

# ▶️ 9. Plot
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Definir backend para exibição

print("Gerando gráfico...")
print(f"Dados para plotar - Raptor: {len(df_compare)} pontos")

plt.figure(figsize=(12, 8))
plt.plot(df_compare['DATA'], df_compare['RAPTOR'] * 100, 
         label='Raptor (CVM)', linewidth=2.5, color='blue', marker='o', markersize=3)
plt.plot(df_compare['DATA'], df_compare['CDI'] * 100, 
         '--', label='CDI (Dados Reais)', linewidth=2.5, color='red')

plt.title('Fundo Raptor vs CDI (01/03 a 11/06/2025)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Rentabilidade Acumulada (%)', fontsize=12)
plt.legend(fontsize=11, loc='upper left')
plt.grid(alpha=0.3, linestyle='-', linewidth=0.5)
plt.xticks(rotation=45)

# Adicionar anotações com valores finais
final_raptor = df_compare['RAPTOR'].iloc[-1] * 100
final_cdi = df_compare['CDI'].iloc[-1] * 100
plt.text(0.02, 0.98, f'Raptor: {final_raptor:.2f}%\nCDI: {final_cdi:.2f}%', 
         transform=plt.gca().transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()

# Salvar o gráfico primeiro
try:
    plt.savefig('raptor_vs_cdi_real.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("✅ Gráfico salvo como 'raptor_vs_cdi_real.png'")
except Exception as e:
    print(f"❌ Erro ao salvar gráfico: {e}")

# Tentar diferentes métodos para exibir o gráfico
print("Tentando exibir o gráfico...")
try:
    plt.show(block=True)  # Bloquear até fechar a janela
    print("✅ Gráfico exibido com sucesso!")
except Exception as e:
    print(f"❌ Erro ao exibir gráfico: {e}")
    print("🔍 Verificando backends disponíveis...")
    print(f"Backend atual: {matplotlib.get_backend()}")
    print("Tentando outros backends...")
    
    backends = ['Qt5Agg', 'TkAgg', 'Agg']
    for backend in backends:
        try:
            matplotlib.use(backend)
            plt.show(block=False)
            print(f"✅ Gráfico exibido usando backend {backend}")
            break
        except:
            continue
    else:
        print("❌ Não foi possível exibir o gráfico em nenhum backend")
        print("📁 O gráfico foi salvo como arquivo PNG")

# Mostrar estatísticas finais
print(f"\n📊 RESUMO DOS RESULTADOS:")
print(f"Rentabilidade Raptor no período: {df_raptor['ACUMULADO'].iloc[-1]:.4%}")
print(f"Rentabilidade CDI no período: {cdi_acum.iloc[-1]:.4%}")
print(f"Diferença (Raptor - CDI): {(df_raptor['ACUMULADO'].iloc[-1] - cdi_acum.iloc[-1]):.4%}")
