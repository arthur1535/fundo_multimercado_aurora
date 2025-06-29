# 🚀 Análise do Fundo Aurora - Projeto de Gestão de Investimentos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-orange.svg)](https://matplotlib.org)

## 📊 Sobre o Projeto

Este projeto implementa uma análise completa de um fundo de investimentos fictício chamado **Aurora**, que segue uma estratégia de alocação diversificada com:

- **90% em Fundos**: 18% em cada um dos 5 fundos selecionados (Vertex, Kinea, Raptor, V8, Verde)
- **10% em CDI**: Para liquidez e redução de risco

### 🎯 Objetivos

1. **Análise de Performance**: Comparar o desempenho do fundo Aurora vs. benchmark (CDI)
2. **Gestão de Risco**: Calcular métricas como VaR, volatilidade e Índice de Sharpe
3. **Estrutura de Taxas**: Simular taxas de administração (2% a.a.) e performance (20% sobre excesso do CDI)
4. **Visualização**: Gerar gráficos comparativos de rentabilidade

## 📁 Estrutura do Projeto

```
aurora-fund-analysis/
├── 📄 aurora_corrigido.py          # Script principal de análise
├── 📁 data/                        # Arquivos de dados
│   ├── taxa_selic_apurada.csv     # Dados do CDI (Banco Central)
│   ├── cotas1749772276365.xlsx    # Dados das cotas (Info Fundos)
│   └── README_DADOS.md            # Instruções sobre os dados
├── 📁 docs/                        # Documentação adicional
│   └── Diver.pdf                  # Apresentação do projeto
├── 📊 requirements.txt             # Dependências Python
├── 🖼️ raptor_vs_cdi_*.png/pdf    # Gráficos gerados
└── 📖 README.md                   # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Cálculos numéricos e estatísticos
- **Matplotlib**: Visualização de dados
- **openpyxl**: Leitura de arquivos Excel

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/aurora-fund-analysis.git
cd aurora-fund-analysis
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Obtenha os dados necessários
- **CDI**: O arquivo `taxa_selic_apurada.csv` já está incluído (fonte: Banco Central)
- **Cotas**: Baixe `cotas1749772276365.xlsx` do Info Fundos (veja `data/README_DADOS.md`)

### 4. Execute a análise
```bash
python aurora_corrigido.py
```

## 📈 Resultados Principais

### Para o Investidor:
- **Capital Inicial**: R$ 10,000,000.00
- **Rentabilidade Líquida**: Calculada após taxas
- **Alfa Gerado**: Retorno adicional sobre o CDI
- **Métricas de Risco**: VaR, Volatilidade, Sharpe Ratio

### Para a Gestora:
- **Taxa de Administração**: 2% a.a. sobre o patrimônio
- **Taxa de Performance**: 20% sobre excesso do CDI
- **Receita Total**: Soma das taxas cobradas
- **Margem sobre PL**: Percentual de receita sobre patrimônio

## 📊 Métricas Calculadas

| Métrica | Descrição |
|---------|-----------|
| **VaR 95%** | Value at Risk - perda máxima esperada em 95% dos casos |
| **Volatilidade** | Medida de risco (desvio padrão dos retornos) |
| **Sharpe Ratio** | Retorno ajustado ao risco vs. taxa livre de risco |
| **Alfa** | Retorno adicional sobre o benchmark (CDI) |
| **Beta** | Sensibilidade aos movimentos do mercado |

## 🎨 Visualizações

O script gera automaticamente:
- Gráfico de rentabilidade acumulada comparativa
- Comparação Aurora vs. Fundos individuais vs. CDI
- Período de análise: março a junho de 2025

## 📋 Dados Utilizados

### Fundos Analisados:
| Código | Nome | Peso na Carteira |
|--------|------|------------------|
| 39589 | Vertex | 18% |
| 53278 | Kinea | 18% |
| 19042 | Raptor | 18% |
| 57400 | V8 | 18% |
| 33728 | Verde | 18% |
| - | CDI | 10% |

### Fontes de Dados:
- **Info Fundos**: Cotas diárias dos fundos
- **Banco Central**: Taxa Selic/CDI oficial
- **Período**: 05/03/2025 a 11/06/2025

## 🔧 Configurações

### Parâmetros do Fundo:
```python
# Pesos na carteira
pesos_aurora = [0.18, 0.18, 0.18, 0.18, 0.18]  # 5 fundos
peso_cdi = 0.10

# Taxas
taxa_administracao_anual = 0.02  # 2% a.a.
taxa_performance = 0.20  # 20% sobre excesso do CDI

# Capital inicial
montante_inicial = 10_000_000  # R$ 10 milhões
```

## 📚 Documentação Adicional

- `docs/Diver.pdf`: Apresentação completa do projeto
- `data/README_DADOS.md`: Instruções detalhadas sobre dados
- Código comentado para facilitar compreensão

## 🤝 Contribuições

Este é um projeto acadêmico desenvolvido para fins educacionais. Sugestões e melhorias são bem-vindas!

## 📞 Contato

Desenvolvido como parte do curso de programação financeira.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**⚠️ Aviso Legal**: Este projeto é apenas para fins educacionais e de demonstração. Não constitui recomendação de investimento. Sempre consulte um profissional qualificado antes de tomar decisões de investimento.
