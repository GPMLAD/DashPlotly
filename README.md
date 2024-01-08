# Dashboard - Plotly + Dash

## Dashboard de Cotações e Notícias

Este é um projeto de construção de um dashboard interativo para exibir cotações de ações e notícias relacionadas a empresas específicas. O dashboard possui duas seções principais: cotações e notícias.

### Configuração do Ambiente

Antes de executar o projeto, é necessário configurar o ambiente Python e instalar as dependências. Utilize o seguinte comando para instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### Executando o Dashboard

Para iniciar o dashboard, execute o seguinte comando na raíz do projeto:

```bash
python main.py
```

O dashboard estará acessível em http://localhost:8050/ em seu navegador.

### Dados Históricos

Os dados históricos utilizados para gerar os arquivos CSV foram extraídos do site oficial da [B3](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/).

Os arquivos **PETR4.csv**, **WEGE3.csv** e **CEAB3.csv** contêm séries históricas de 2023 e 2024.

O arquivo **merged_data.csv** é utilizado para alimentar a aplicação e é atualizado a cada 15 segundos pelos outros 3 arquivos.

### Notícias e dados

As notícias são coletadas do [Brazil Journal](https://braziljournal.com/) utilizando web scraping.
As cotações são coletadas de [InfoMoney](https://www.infomoney.com.br) utilizando web scraping.

Vale lembrar que a InfoMoney disponibiliza publicamente os dados das cotação com um atraso de 15 minutos.

### Observações

Caso os arquivos .csv sejam deletados, para gerá-los novamente, basta executar a função **writeFiles** uma vez. Porém ela necessita da série histórica de ambos os anos, o que não ocorre no repositório pois o arquivo tem tamanho considerável.

Para finalizar a aplicação, é necessário usar o comando **Ctrl+C** duas vezes, pois uma encerra o dash e a outra o restante da aplicação.
