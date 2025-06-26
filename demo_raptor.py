import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Criar dados simulados do Raptor para demonstração
print("=== CRIANDO DEMONSTRAÇÃO COM DADOS SIMULADOS ===")

# Simular dados do Raptor (baseado em padrões típicos de fundos)
dates = pd.date_range('2025-03-01', '2025-06-11', freq='D')
dates = [d for d in dates if d.weekday() < 5]  # Apenas dias úteis

# Simular retornos do Raptor com alguma volatilidade
np.random.seed(42)
retornos_raptor = np.random.normal(0.0008, 0.012, len(dates))  # Retorno médio 0.08% com volatilidade
raptor_acumulado = (1 + pd.Series(retornos_raptor)).cumprod() - 1

# Carregar dados reais da Selic
print("Carregando dados reais da Selic...")
try:
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
    # Garantir que 'Fator diário' seja numérico
    df_selic['Fator diário'] = pd.to_numeric(df_selic['Fator diário'], errors='coerce')
    df_selic = df_selic.dropna()  # Remove linhas com valores não numéricos
    df_selic = df_selic.set_index('Data').sort_index()
    
    # Filtrar para o período
    df_selic_periodo = df_selic.loc['2025-03-01':'2025-06-11']
    cdi_acumulado = df_selic_periodo['Fator diário'].cumprod() - 1
    
    # Alinhar datas
    dates_common = pd.to_datetime(dates)
    cdi_aligned = cdi_acumulado.reindex(dates_common).ffill()
    
    print("✅ Dados da Selic carregados com sucesso!")
    
except Exception as e:
    print(f"❌ Erro ao carregar Selic: {e}")
    # Simular CDI se não conseguir carregar
    retornos_cdi = np.full(len(dates), 0.000453)  # ~11.5% ao ano
    cdi_aligned = pd.Series((1 + retornos_cdi).cumprod() - 1, index=pd.to_datetime(dates))

# Criar DataFrame para comparação
df_compare = pd.DataFrame({
    'DATA': dates_common,
    'RAPTOR_SIMULADO': raptor_acumulado.values,
    'CDI': cdi_aligned.values
})

# Plotar gráfico
print("Gerando gráfico de demonstração...")
plt.figure(figsize=(12, 7))
plt.plot(df_compare['DATA'], df_compare['RAPTOR_SIMULADO'] * 100, 
         label='Raptor (Dados Simulados)', linewidth=2.5, color='blue')
plt.plot(df_compare['DATA'], df_compare['CDI'] * 100, 
         '--', label='CDI (Dados Reais)', linewidth=2, color='red')

plt.title('Demonstração: Raptor vs CDI (mar-jun/2025)', fontsize=14, fontweight='bold')
plt.xlabel('Data', fontsize=12)
plt.ylabel('Rentabilidade Acumulada (%)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(alpha=0.4)
plt.xticks(rotation=45)
plt.tight_layout()

# Tentar exibir o gráfico
try:
    plt.show(block=False)
    print("✅ Gráfico de demonstração plotado com sucesso!")
except:
    try:
        plt.savefig('raptor_vs_cdi_demo.png', dpi=300, bbox_inches='tight')
        print("✅ Gráfico salvo como 'raptor_vs_cdi_demo.png'")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

# Estatísticas finais
rentabilidade_raptor = df_compare['RAPTOR_SIMULADO'].iloc[-1] * 100
rentabilidade_cdi = df_compare['CDI'].iloc[-1] * 100
diferenca = rentabilidade_raptor - rentabilidade_cdi

print(f"""
📊 RESULTADOS DA DEMONSTRAÇÃO:
• Rentabilidade Raptor (simulada): {rentabilidade_raptor:.2f}%
• Rentabilidade CDI (real): {rentabilidade_cdi:.2f}%
• Diferença (Raptor - CDI): {diferenca:.2f}%
• Período: {dates[0].strftime('%d/%m/%Y')} a {dates[-1].strftime('%d/%m/%Y')}

💡 NOTA: Os dados do Raptor são simulados para demonstração.
   Para dados reais, aguarde o download da CVM ser concluído.
""")

print("\n🔄 O download dos dados reais da CVM pode levar alguns minutos...")
print("   Quando concluído, execute novamente cvm.py para ver os dados reais.")
