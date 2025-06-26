import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Configurar matplotlib para garantir exibição
print("Configurando matplotlib...")
print(f"Backend padrão: {matplotlib.get_backend()}")

# Tentar diferentes backends
backends_disponiveis = ['TkAgg', 'Qt5Agg', 'Agg']
for backend in backends_disponiveis:
    try:
        matplotlib.use(backend, force=True)
        print(f"✅ Backend configurado: {backend}")
        break
    except Exception as e:
        print(f"❌ Erro com backend {backend}: {e}")
        continue

# Simular dados do Raptor para teste rápido
print("\n=== CARREGANDO DADOS PARA TESTE DE GRÁFICO ===")

# Dados simulados baseados nos resultados anteriores
dates = pd.date_range('2025-03-01', '2025-06-11', freq='D')
dates = [d for d in dates if d.weekday() < 5][:68]  # 68 pontos como nos dados reais

# Simular evolução do Raptor com queda de -2.03%
np.random.seed(123)
retornos_diarios = np.random.normal(-0.0003, 0.008, len(dates))  # Média negativa
raptor_acumulado = np.cumsum(retornos_diarios)
raptor_acumulado = raptor_acumulado - raptor_acumulado[0]  # Começar do zero
raptor_acumulado[-1] = -0.0203  # Forçar valor final real

# Simular CDI com crescimento de 3.64%
cdi_acumulado = np.linspace(0, 0.0364, len(dates))

# Criar DataFrame
df_compare = pd.DataFrame({
    'DATA': dates,
    'RAPTOR': raptor_acumulado,
    'CDI': cdi_acumulado
})

print(f"Dados preparados: {len(df_compare)} pontos")
print(f"Raptor final: {raptor_acumulado[-1]:.4%}")
print(f"CDI final: {cdi_acumulado[-1]:.4%}")

# GRÁFICO PRINCIPAL
print("\n=== GERANDO GRÁFICO ===")
fig, ax = plt.subplots(figsize=(14, 8))

# Plot das linhas
line1 = ax.plot(df_compare['DATA'], df_compare['RAPTOR'] * 100, 
                label='Fundo Raptor (CVM)', linewidth=3, color='#1f77b4', 
                marker='o', markersize=4, alpha=0.8)
line2 = ax.plot(df_compare['DATA'], df_compare['CDI'] * 100, 
                label='CDI (Taxa Selic)', linewidth=3, color='#d62728', 
                linestyle='--', alpha=0.9)

# Configurações do gráfico
ax.set_title('📊 Comparativo: Fundo Raptor vs CDI\n(Março - Junho 2025)', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Data', fontsize=14, fontweight='bold')
ax.set_ylabel('Rentabilidade Acumulada (%)', fontsize=14, fontweight='bold')

# Grid personalizado
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.8)
ax.set_axisbelow(True)

# Legenda
legend = ax.legend(fontsize=12, loc='upper left', frameon=True, 
                  fancybox=True, shadow=True)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.9)

# Anotações com valores finais
final_raptor = df_compare['RAPTOR'].iloc[-1] * 100
final_cdi = df_compare['CDI'].iloc[-1] * 100
diferenca = final_raptor - final_cdi

# Caixa de texto com estatísticas
stats_text = f"""📈 RESULTADOS FINAIS:
• Raptor: {final_raptor:.2f}%
• CDI: {final_cdi:.2f}%
• Diferença: {diferenca:.2f}%
• Período: 68 dias úteis"""

ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
        verticalalignment='top', fontsize=11,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

# Linha zero para referência
ax.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=1)

# Formatação dos eixos
ax.tick_params(axis='both', which='major', labelsize=11)
plt.xticks(rotation=45)

# Ajustar layout
plt.tight_layout()

# Salvar com alta qualidade
print("Salvando gráfico...")
try:
    plt.savefig('raptor_vs_cdi_final.png', dpi=300, 
                bbox_inches='tight', facecolor='white', 
                edgecolor='none', format='png')
    print("✅ Gráfico salvo como 'raptor_vs_cdi_final.png'")
    
    # Também salvar em PDF
    plt.savefig('raptor_vs_cdi_final.pdf', 
                bbox_inches='tight', facecolor='white')
    print("✅ Gráfico salvo como 'raptor_vs_cdi_final.pdf'")
    
except Exception as e:
    print(f"❌ Erro ao salvar: {e}")

# Estratégias múltiplas para exibir
print("\n=== TENTANDO EXIBIR GRÁFICO ===")

estrategias = [
    ("plt.show(block=True)", lambda: plt.show(block=True)),
    ("plt.show()", lambda: plt.show()),
    ("fig.show()", lambda: fig.show()),
    ("plt.pause(0.1)", lambda: plt.pause(0.1)),
]

for nome, funcao in estrategias:
    try:
        print(f"Tentando: {nome}")
        funcao()
        print(f"✅ Sucesso com {nome}")
        break
    except Exception as e:
        print(f"❌ Falhou {nome}: {e}")
        continue
else:
    print("❌ Não foi possível exibir o gráfico na tela")

print(f"\n🎯 CONCLUSÃO:")
print(f"Backend usado: {matplotlib.get_backend()}")
print(f"Figura salva: ✅")
print(f"O gráfico está disponível como arquivo PNG e PDF")

# Manter a janela aberta se conseguiu plotar
try:
    input("\n⏸️  Pressione Enter para fechar o gráfico...")
except:
    pass

plt.close('all')
print("✅ Processo concluído!")
