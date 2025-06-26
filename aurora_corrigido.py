import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. COTAS DOS FUNDOS
file_path_fundos = 'D:/user/cotas1749772276365.xlsx'
df_cotas = pd.read_excel(file_path_fundos, sheet_name='Cotas')
codigos_fundos = [39589, 53278, 19042, 57400, 33728]
nomes = ['Vertex', 'Kinea', 'Raptor', 'V8', 'Verde']
df_fundos = df_cotas[df_cotas['Código'].isin(codigos_fundos)]
df_fundos_pivot = (
    df_fundos
    .pivot(index='Data', columns='Código', values='Cota')
    .rename(columns=dict(zip(codigos_fundos, nomes)))
    .sort_index()
)
df_fundos_pivot = df_fundos_pivot.loc['2025-03-01':'2025-06-11'].dropna()

# 2. CDI REAL
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
df_selic = df_selic[(df_selic['Data'] >= '2025-03-01') & (df_selic['Data'] <= '2025-06-11')]
df_selic = df_selic.set_index('Data').sort_index()

# 3. Alinhar datas entre fundos e CDI
datas_comuns = df_fundos_pivot.index.intersection(df_selic.index)
df_fundos_pivot = df_fundos_pivot.loc[datas_comuns]
df_selic = df_selic.loc[datas_comuns]

# 4. Retornos dos fundos
retornos_fundos = df_fundos_pivot.pct_change().dropna()
retornos_cdi = df_selic['Fator diário'] - 1  # Retorno diário do CDI

# 5. Retorno diário do fundo Aurora: 18% de cada fundo, 10% CDI
pesos_aurora = [0.18, 0.18, 0.18, 0.18, 0.18]  # 5 fundos
peso_cdi = 0.10

# Calcular retornos Aurora com verificação de datas
print(f"Número de observações dos fundos: {len(retornos_fundos)}")
print(f"Número de observações do CDI: {len(retornos_cdi)}")

# Alinhar retornos
retornos_cdi_alinhado = retornos_cdi.loc[retornos_fundos.index]

# Dataframe para cálculo conjunto
retornos_aurora = (
    retornos_fundos.mul(pesos_aurora, axis=1).sum(axis=1)
    + peso_cdi * retornos_cdi_alinhado
)

print(f"Número de observações do Aurora: {len(retornos_aurora)}")
print(f"Valores NaN no Aurora: {retornos_aurora.isna().sum()}")

# 6. Acumulado Aurora e dos fundos
aurora_acumulado = (1 + retornos_aurora).cumprod() - 1
acumulado_fundos = {nome: (1 + retornos_fundos[nome]).cumprod() - 1 for nome in nomes}
cdi_acumulado = df_selic['Fator diário'].cumprod() - 1

# Dados principais
montante_inicial = 10_000_000
retorno_final_aurora = aurora_acumulado.iloc[-1]
valor_bruto_final = montante_inicial * (1 + retorno_final_aurora)
ganho_bruto = valor_bruto_final - montante_inicial

# Taxas
dias_uteis = len(aurora_acumulado)
taxa_administracao_anual = 0.02
taxa_adm_periodo = taxa_administracao_anual * (dias_uteis - 1) / 252  # proporcional ao período
taxa_adm_valor = valor_bruto_final * taxa_adm_periodo

# CDI do período (acumulado)
retorno_acumulado_cdi = cdi_acumulado.iloc[-1]
valor_cdi_final = montante_inicial * (1 + retorno_acumulado_cdi)
lucro_acima_cdi = valor_bruto_final - valor_cdi_final
taxa_performance = 0.20
taxa_perf_valor = max(lucro_acima_cdi * taxa_performance, 0)
total_taxas = taxa_adm_valor + taxa_perf_valor
valor_final_liquido = valor_bruto_final - total_taxas

# Rentabilidades
rentabilidade_liquida = ((valor_final_liquido / montante_inicial) - 1) * 100
benchmark_cdi = retorno_acumulado_cdi * 100
alfa_gerado = rentabilidade_liquida - benchmark_cdi

# Cotas
numero_cotas = 100_000
valor_cota_inicial = montante_inicial / numero_cotas
valor_cota_final = valor_final_liquido / numero_cotas
variacao_cota = (valor_cota_final / valor_cota_inicial - 1) * 100
variacao_anualizada = variacao_cota * 252 / (dias_uteis - 1)
percentual_cdi = (variacao_cota / benchmark_cdi) * 100

# Risco e Sharpe - CORREÇÃO DO VaR
print(f"\nAnalisando retornos Aurora para VaR:")
print(f"Tamanho original: {len(retornos_aurora)}")
print(f"Valores finitos: {np.isfinite(retornos_aurora).sum()}")
print(f"Valores NaN: {retornos_aurora.isna().sum()}")
print(f"Valores infinitos: {np.isinf(retornos_aurora).sum()}")

# Remover valores ausentes e infinitos antes de calcular VaR
retornos_aurora_limpo = retornos_aurora.dropna()
retornos_aurora_limpo = retornos_aurora_limpo[np.isfinite(retornos_aurora_limpo)]

print(f"Valores após limpeza: {len(retornos_aurora_limpo)}")

if len(retornos_aurora_limpo) > 0:
    VaR_95 = np.percentile(retornos_aurora_limpo, 5)
    print(f"VaR calculado: {VaR_95}")
else:
    VaR_95 = np.nan
    print("Não foi possível calcular VaR - não há dados válidos")

volatilidade_diaria = retornos_aurora.std()
volatilidade_mensal = volatilidade_diaria * np.sqrt(21)
retorno_medio_diario = retornos_aurora.mean()
cdi_diario_medio = (df_selic['Fator diário'] - 1).mean()
sharpe_diario = (retorno_medio_diario - cdi_diario_medio) / volatilidade_diaria
sharpe_mensal = sharpe_diario * np.sqrt(21)
sharpe_anualizado = sharpe_diario * np.sqrt(252)

# Receita total, margem e estimativa anualizada para a gestora
margem_sobre_pl = (total_taxas / montante_inicial) * 100
estimativa_anualizada = taxa_adm_valor * 252 / (dias_uteis - 1)

# Print amigável dos resultados
print(f"""
🧑‍💼 RESULTADOS PARA O INVESTIDOR:
* Capital Inicial: R${montante_inicial:,.2f}
* Valor Bruto (antes das taxas): R${valor_bruto_final:,.2f}
* Ganho Bruto: R${ganho_bruto:,.2f}
* Total de Taxas Pagas: R${total_taxas:,.2f}
* Valor Final Líquido: R${valor_final_liquido:,.2f}
* Rentabilidade Líquida: {rentabilidade_liquida:.2f}%
* Benchmark (CDI): {benchmark_cdi:.2f}%
* Alfa Gerado: {alfa_gerado:.2f}%

💼 RESULTADOS PARA A GESTORA (RECEITAS):
* Taxa de Administração: R${taxa_adm_valor:,.2f} (2.00% a.a. proporcional)
* Taxa de Performance: R${taxa_perf_valor:,.2f} (20% sobre excedente ao CDI)
* Receita Total: R${total_taxas:,.2f}
* Margem sobre PL: {margem_sobre_pl:.4f}%
* Estimativa Anualizada: R${estimativa_anualizada:,.2f}

💰 VALOR DA COTA:
* Valor da Cota Inicial: R${valor_cota_inicial:.6f}
* Valor da Cota Final: R${valor_cota_final:.6f}
* Variação no Período: {variacao_cota:.4f}%
* Variação Anualizada: {variacao_anualizada:.2f}%
* Benchmark (CDI): {benchmark_cdi:.2f}%
* % do CDI: {percentual_cdi:.2f}%

📊 MÉTRICAS DE RISCO:
* VaR Diário (95%): {VaR_95:.4%}
* Volatilidade (Mensal): {volatilidade_mensal:.4%}
* Índice de Sharpe (mensal): {sharpe_mensal:.4f}
* Índice de Sharpe (anualizado): {sharpe_anualizado:.4f}
""")

# 7. Plot comparativo fundos, Aurora e CDI
plt.figure(figsize=(12,6))
for nome in nomes:
    plt.plot(acumulado_fundos[nome].index, acumulado_fundos[nome].values, label=nome)
plt.plot(aurora_acumulado.index, aurora_acumulado.values, label='Aurora (18% cada fundo + 10% CDI)', color='black', linewidth=2.5)
plt.plot(cdi_acumulado.index, cdi_acumulado.values, '--', color='gray', label='CDI Acumulado')
plt.title('Rentabilidade Acumulada (mar-jun/2025)')
plt.xlabel('Data')
plt.ylabel('Rentabilidade Acumulada')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
