# Relatório Comitê de Crédito

Este é um aplicativo Streamlit para gerar relatórios do comitê de crédito para empresas e pessoas físicas.

## Funcionalidades

### Para Empresas

- Consulta de dados da empresa com base no CNPJ inserido.
- Exibição dos dados da empresa, incluindo razão social, tipo de empresa, data de abertura, média do faturamento mensal do ano atual e anterior, SCORE e risco.
- Geração de um PDF contendo os dados da empresa.

### Para Pessoa Física

- Entrada do nome, CPF e quantidade de animais de uma pessoa física.
- Cálculo do índice de risco e valor liberado com base na quantidade de animais.
- Geração de um PDF contendo os dados da pessoa física.

## Como usar

1. Clone este repositório.
2. Instale as dependências listadas no arquivo `requirements.txt`.
3. Execute o aplicativo usando o comando `streamlit run app.py`.
4. Insira o CNPJ ou CPF, dependendo do tipo de consulta desejada.
5. Insira os dados solicitados e clique no botão correspondente para consultar e gerar o relatório em PDF.

## Dependências

- `requests`: Para fazer solicitações HTTP à API de consulta de CNPJ.
- `pandas`: Para manipulação de dados.
- `numpy`: Para cálculos matemáticos.
- `streamlit`: Para criar a interface do aplicativo web.
- `datetime`: Para manipulação de datas e horários.
- `json`: Para trabalhar com dados JSON.
- `base64`: Para codificar e decodificar dados em base64.
- `fpdf`: Para gerar documentos PDF.

## Autor

Este aplicativo foi desenvolvido por [Dheime Mocelin].

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).
