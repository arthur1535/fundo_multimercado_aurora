import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuração do matplotlib
plt.ion()  # Modo interativo
print("Configurando matplotlib em modo interativo...")

# Dados dos resultados reais
dados_reais = {
    'data': pd.date_range('2025-03-01', periods=68, freq='D'),
    'raptor': np.linspace(0, -2.0330, 68),  # -2.03% final
    'cdi': np.linspace(0, 3.6408, 68)       # 3.64% final
}

# Criar gráfico
plt.figure(figsize=(12, 8))

# Plotar dados
plt.plot(dados_reais['data'], dados_reais['raptor'], 
         'b-', linewidth=3, label='Fundo Raptor', marker='o', markersize=3)
plt.plot(dados_reais['data'], dados_reais['cdi'], 
         'r--', linewidth=3, label='CDI')

# Formatação
plt.title('Fundo Raptor vs CDI (Março-Junho 2025)', fontsize=16, fontweight='bold')
plt.xlabel('Data', fontsize=12)
plt.ylabel('Rentabilidade Acumulada (%)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Adicionar estatísticas
plt.text(0.02, 0.98, 
         f'Raptor: {dados_reais["raptor"][-1]:.2f}%\nCDI: {dados_reais["cdi"][-1]:.2f}%\nDiferença: {dados_reais["raptor"][-1] - dados_reais["cdi"][-1]:.2f}%', 
         transform=plt.gca().transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.tight_layout()

# Salvar
plt.savefig('grafico_raptor_cdi.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo como 'grafico_raptor_cdi.png'")

# Exibir
plt.show()
print("✅ Comando plt.show() executado")

# Aguardar
input("🔍 Pressione Enter para continuar...")
plt.close()

print("🎯 Gráfico processado!")
print("📁 Verifique o arquivo 'grafico_raptor_cdi.png' na pasta atual")
