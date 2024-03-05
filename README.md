# Consulta de CNPJ

Este é um aplicativo simples para consulta de CNPJ. Ele permite que os usuários insiram um CNPJ, médias de faturamento mensal de anos atual e anterior, bem como o score da empresa. Com base nesses dados, o aplicativo consulta uma API para obter informações da empresa e calcula um novo limite liberado para empréstimos a partir do score e médias de faturamento fornecidas.

## Funcionalidades

- Consulta de informações da empresa com base no CNPJ fornecido.
- Cálculo do novo limite liberado para empréstimos com base no score e médias de faturamento.
- Geração de um PDF com os dados da empresa e do novo limite liberado.

## Tecnologias Utilizadas

- Python
- Streamlit: Biblioteca para construção de aplicativos web com Python.
- Pandas: Biblioteca para manipulação e análise de dados.
- Numpy: Biblioteca para computação numérica.
- Requests: Biblioteca para fazer requisições HTTP em Python.
- FPDF: Biblioteca para geração de documentos PDF.

## Como Utilizar

1. Clone este repositório.
2. Instale as dependências listadas no arquivo `requirements.txt`.
3. Execute o arquivo `app.py`.
4. Insira o CNPJ da empresa, médias de faturamento mensal dos anos atual e anterior, e o score da empresa.
5. Clique no botão "Consultar" para obter as informações da empresa e calcular o novo limite liberado para empréstimos.
6. Um PDF será gerado com os dados da empresa e do novo limite liberado. Você pode baixá-lo clicando no botão "Baixe o PDF".

## Autor

[Dheime Mocelin]

## Licença

Este projeto está sob a [Licença MIT](LICENSE).
