import requests
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import json
import base64
from fpdf import FPDF

# Função para obter dados da empresa com base no CNPJ
def get_company_data(cnpj):
    # URL da API para consultar dados do CNPJ
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    
    try:
        # Fazendo a solicitação GET à API
        response = requests.get(url)
        
        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Retorna os dados da empresa (presumindo que a API retorna dados JSON)
            return response.json()
        else:
            st.error(f"Erro na solicitação. Código de status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None


def generate_pdf(data_hora_formatada, razao_social, cnpj, tipo_empresa, abertura, faturamento_mensal_ano_atual, faturamento_mensal_ano_anterior, media_emprestimo, score, score_indice):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Dados da empresa ao PDF
    pdf.cell(200, 10, txt="Data do Pedido: " + data_hora_formatada, ln=True)
    pdf.cell(200, 10, txt="Razão Social: " + razao_social, ln=True)
    pdf.cell(200, 10, txt="CNPJ: " + cnpj, ln=True)
    pdf.cell(200, 10, txt="Tipo de Empresa: " + tipo_empresa, ln=True)
    pdf.cell(200, 10, txt="Data da Abertura: " + abertura, ln=True)
    pdf.cell(200, 10, txt="Média do Faturamento mensal do ano atual: " + str(faturamento_mensal_ano_atual), ln=True)
    pdf.cell(200, 10, txt="Média do Faturamento mensal do ano anterior: " + str(faturamento_mensal_ano_anterior), ln=True)
    pdf.cell(200, 10, txt="SCORE: " + str(score), ln=True)
    pdf.cell(200, 10, txt="Risco: " + score_indice, ln=True)
    pdf.cell(200, 10, txt="NOVO Limite Liberado PJ: " + str(media_emprestimo), ln=True)
    
    # Salva o PDF
    pdf_file_path = "dados_da_empresa.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path


# Definição da função
def calcular_classificacao_e_valor(score):
    if score >= 800:
        return "Baixíssimo", 0.5
    elif score >= 700:
        return "Baixo", 0.4
    elif score >= 500:
        return "Médio", 0.3
    else:
        return "Muito Alto", 0


def main():
    # Título do formulário
    st.title("Consulta de CNPJ")
    
    # Hora atual
    data_hora_atual = datetime.now()
    # Convertendo para uma string formatada
    data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y")

    # Campo de entrada para o CNPJ
    cnpj = st.text_input("Por favor, insira o CNPJ da empresa (apenas números):")
    faturamento_mensal_ano_atual = st.number_input("Qual a média do Faturamento mensal do ano atual?")
    faturamento_mensal_ano_anterior = st.number_input("Qual a média do Faturamento mensal do ano anterior?")

    total_media = (faturamento_mensal_ano_atual + faturamento_mensal_ano_anterior) / 2
    
    # Campo de entrada para o SCORE
    score = st.text_input("Qual o SCORE?")   
    if score:
        score = int(score)
        # Chamada da função e atribuição somente do segundo elemento retornado
        score_indice, valor = calcular_classificacao_e_valor(score)
        
        # Calcular a media_emprestimo
        media_emprestimo = total_media * valor
        
        # Botão para enviar o formulário
        if st.button("Consultar"):
            # Verifica se o CNPJ foi inserido
            if cnpj:
                # Chamada à função para obter dados da empresa
                company_data = get_company_data(cnpj)
                
                # Verifica se os dados da empresa foram obtidos com sucesso
                if company_data:
                    razao_social = company_data['nome']
                    tipo_empresa = company_data['tipo']
                    abertura = company_data['abertura']
                    
                    
                    # Exibe os dados da empresa
                    st.write("Data do Pedido:", data_hora_formatada)
                    st.write("Razão Social:", razao_social)
                    st.write('CNPJ: ', cnpj)
                    st.write("Tipo de Empresa:", tipo_empresa)
                    st.write('Data da Abertura:', abertura)
                    st.write('Média do Faturamento mensal do ano atual:', faturamento_mensal_ano_atual)
                    st.write('Média do Faturamento mensal do ano anterior:', faturamento_mensal_ano_anterior)
                    st.write('Média do Faturamento mensal:', total_media)
                    st.write('SCORE: ', score)
                    st.write('Risco: ', score_indice)
                    st.write('NOVO Limite Liberado PJ: ',media_emprestimo)
                    
                    
                    # Gera o PDF
                    pdf_file_path = generate_pdf(data_hora_formatada, razao_social, cnpj, tipo_empresa, abertura, faturamento_mensal_ano_atual, faturamento_mensal_ano_anterior, media_emprestimo, score, score_indice)
                    
                    # Cria o botão de download para o PDF
                    with open(pdf_file_path, "rb") as f:
                        st.download_button(
                            label="Baixe o PDF",
                            data=f,
                            file_name="dados_da_empresa.pdf",
                            mime="application/pdf"
                        )
                    
                else:
                    st.error("Não foi possível obter os dados da empresa.")
            else:
                st.warning("Por favor, insira um CNPJ válido.")

if __name__ == "__main__":
    main()
