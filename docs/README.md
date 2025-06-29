# Documentação do Projeto Aurora

## 📋 Arquivos de Documentação

### 1. Diver.pdf
- **Descrição**: Apresentação completa do projeto Aurora
- **Conteúdo**: 26 slides explicando toda a metodologia, análises e resultados
- **Localização**: Deve ser colocado nesta pasta

### 2. Metodologia

#### Estratégia de Investimento
- **Composição**: 90% em fundos (18% cada) + 10% CDI
- **Fundos Selecionados**: Vertex, Kinea, Raptor, V8, Verde
- **Período de Análise**: março a junho de 2025

#### Cálculos Realizados
1. **Retornos Diários**: Variação percentual das cotas
2. **Retorno Acumulado**: Produto composto dos retornos diários
3. **Benchmarking**: Comparação com CDI
4. **Métricas de Risco**: VaR, volatilidade, Sharpe ratio

#### Estrutura de Taxas
- **Taxa de Administração**: 2% ao ano sobre o patrimônio
- **Taxa de Performance**: 20% sobre retorno acima do CDI
- **Base de Cálculo**: Proporcional ao período analisado

### 3. Dados Utilizados

#### Fontes
- **Info Fundos**: Cotas diárias dos fundos
- **Banco Central**: Taxa Selic/CDI oficial
- **Período**: 05/03/2025 a 11/06/2025

#### Qualidade dos Dados
- Dados alinhados por datas úteis
- Tratamento de valores ausentes
- Validação de consistência

### 4. Resultados Principais

#### Métricas Calculadas
- Rentabilidade líquida após taxas
- Alfa gerado sobre o CDI
- Value at Risk (VaR) 95%
- Índice de Sharpe anualizado
- Volatilidade mensal

#### Visualizações
- Gráfico de rentabilidade comparativa
- Evolução das cotas
- Comparação com benchmark

## 🎯 Objetivo do Projeto

Demonstrar a aplicação prática de conceitos de:
- Gestão de carteiras
- Análise de risco
- Cálculo de taxas
- Benchmarking
- Visualização de dados financeiros

## 📊 Tecnologias Aplicadas

- **Python**: Linguagem de programação
- **Pandas**: Manipulação de dados
- **NumPy**: Cálculos estatísticos
- **Matplotlib**: Visualizações
- **Excel**: Integração com planilhas

## 🔗 Links Úteis

- [Banco Central do Brasil](https://www.bcb.gov.br/)
- [CVM - Comissão de Valores Mobiliários](https://www.cvm.gov.br/)
- [Info Fundos](https://www.infofundos.com.br/)

---

**Desenvolvido para fins educacionais - Curso de Programação Financeira**
