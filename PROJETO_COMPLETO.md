# 📊 Projeto Aurora - Análise Completa de Fundos de Investimento

## 🎯 Visão Geral do Trabalho

Este projeto representa uma **análise completa de gestão de investimentos**, desenvolvida como parte do curso de programação financeira. O trabalho simula a criação e análise de um fundo de investimentos chamado **Aurora**, aplicando conceitos avançados de finanças quantitativas.

## 🏗️ Arquitetura do Projeto

### 1. **Coleta de Dados**
- **Fonte CDI**: Banco Central do Brasil (taxa_selic_apurada.csv)
- **Fonte Fundos**: Info Fundos (cotas1749772276365.xlsx)
- **Período**: março a junho de 2025 (dados reais)

### 2. **Estratégia de Investimento Aurora**
```
Composição da Carteira:
├── 90% Fundos de Investimento
│   ├── 18% Vertex Capital (Código: 39589)
│   ├── 18% Kinea (Código: 53278)
│   ├── 18% Raptor (Código: 19042)
│   ├── 18% V8 Capital (Código: 57400)
│   └── 18% Verde Asset (Código: 33728)
└── 10% CDI (Liquidez e Redução de Risco)
```

### 3. **Metodologia de Análise**

#### 📈 Cálculos de Performance
1. **Retornos Diários**: `R_t = (P_t / P_{t-1}) - 1`
2. **Retorno Acumulado**: `R_{acum} = ∏(1 + R_t) - 1`
3. **Retorno Aurora**: `R_{Aurora} = Σ(w_i × R_i) + w_{CDI} × R_{CDI}`

#### 🎯 Métricas de Risco
1. **VaR 95%**: `P_5(R_t)` - Percentil 5% dos retornos
2. **Volatilidade**: `σ = √(Var(R_t))`
3. **Sharpe Ratio**: `SR = (R_{Aurora} - R_{CDI}) / σ_{Aurora}`

#### 💰 Estrutura de Taxas
1. **Taxa de Administração**: 2% a.a. sobre patrimônio
2. **Taxa de Performance**: 20% sobre excesso do CDI
3. **Cálculo Proporcional**: Ajustado para período de análise

## 📊 Resultados e Insights

### Performance Financeira
- **Capital Inicial**: R$ 10.000.000,00
- **Rentabilidade**: Calculada após dedução de todas as taxas
- **Alfa**: Retorno adicional sobre o benchmark (CDI)
- **Tracking Error**: Medida de aderência ao benchmark

### Análise de Risco
- **VaR Diário**: Perda máxima esperada em 95% dos casos
- **Volatilidade Mensal**: Medida de oscilação dos retornos
- **Correlação**: Análise entre fundos e CDI

### Simulação para Gestora
- **Receita de Taxa de Administração**: Baseada no patrimônio médio
- **Receita de Performance**: Apenas sobre excesso do CDI
- **Margem sobre PL**: Percentual de receita sobre patrimônio
- **Projeção Anualizada**: Estimativa de receitas anuais

## 🛠️ Tecnologias e Ferramentas

### Python Stack
```python
import pandas as pd          # Manipulação de dados
import numpy as np           # Cálculos matemáticos
import matplotlib.pyplot as plt  # Visualizações
```

### Funcionalidades Implementadas
1. **Data Alignment**: Sincronização de datas entre diferentes fontes
2. **Missing Data Handling**: Tratamento de dados ausentes
3. **Performance Attribution**: Decomposição de retornos por ativo
4. **Risk Analytics**: Cálculo de métricas de risco avançadas
5. **Visualization**: Gráficos comparativos profissionais

## 📋 Estrutura de Arquivos

```
testecdi/
├── 📄 aurora_corrigido.py       # Script principal
├── 📁 data/                     # Dados de entrada
│   ├── taxa_selic_apurada.csv  # CDI (Banco Central)
│   ├── cotas1749772276365.xlsx # Cotas (Info Fundos)
│   └── README_DADOS.md         # Documentação dos dados
├── 📁 docs/                     # Documentação
│   ├── Diver.pdf              # Apresentação (26 slides)
│   └── README.md              # Metodologia detalhada
├── 📊 requirements.txt          # Dependências
├── 🖼️ *.png, *.pdf            # Gráficos gerados
└── 📖 README.md               # Documentação principal
```

## 🎓 Conceitos Aplicados

### Finanças Quantitativas
- **Modern Portfolio Theory**: Diversificação e otimização
- **Risk Management**: VaR, volatilidade, correlações
- **Performance Measurement**: Sharpe ratio, alfa, beta
- **Fee Structure**: Modeling de taxas de gestão

### Programação Financeira
- **Data Wrangling**: Limpeza e preparação de dados
- **Time Series Analysis**: Análise de séries temporais
- **Statistical Computing**: Cálculos estatísticos avançados
- **Financial Modeling**: Modelagem de produtos financeiros

### Visualização de Dados
- **Comparative Charts**: Gráficos comparativos
- **Performance Plots**: Visualização de rentabilidade
- **Risk Metrics**: Representação visual de risco

## 🔍 Pontos de Destaque

### 1. **Realismo dos Dados**
- Dados reais do Banco Central (CDI)
- Cotas reais de fundos brasileiros
- Período atual (2025)

### 2. **Complexidade Técnica**
- Alinhamento de diferentes fontes de dados
- Tratamento de feriados e fins de semana
- Cálculos proporcionais de taxas

### 3. **Aplicação Prática**
- Simulação realista de um fundo de investimentos
- Estrutura de taxas do mercado brasileiro
- Métricas utilizadas por gestores profissionais

### 4. **Qualidade do Código**
- Código bem documentado
- Tratamento de erros
- Validações de consistência

## 📈 Como Executar o Projeto

### Pré-requisitos
```bash
pip install pandas numpy matplotlib openpyxl
```

### Execução
```bash
# 1. Clone o repositório
git clone [seu-repositorio]

# 2. Navegue para o diretório
cd testecdi

# 3. Execute a análise
python aurora_corrigido.py
```

### Saída Esperada
- Métricas de performance no console
- Gráfico comparativo de rentabilidade
- Análise detalhada de risco e retorno

## 🎯 Valor Educacional

Este projeto demonstra:
1. **Integração de Dados**: Como combinar diferentes fontes de dados financeiros
2. **Modelagem Financeira**: Implementação de modelos de gestão de ativos
3. **Análise de Risco**: Cálculo de métricas de risco modernas
4. **Visualização**: Apresentação profissional de resultados
5. **Programação Aplicada**: Uso de Python para finanças

## 🚀 Próximos Passos

Possíveis melhorias futuras:
- [ ] Backtesting com períodos mais longos
- [ ] Otimização de carteira (Markowitz)
- [ ] Análise de drawdown
- [ ] Stress testing
- [ ] Dashboard interativo
- [ ] API para dados em tempo real

---

**Desenvolvido como projeto final do curso de Programação Financeira**
*Demonstra aplicação prática de conceitos avançados de finanças quantitativas*
