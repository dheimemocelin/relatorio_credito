import requests
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import json
import base64
from fpdf import FPDF


def get_company_data(cnpj):
    # URL da API
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'

    # Cabeçalho do agente do usuário
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # Fazendo a solicitação GET à API com o cabeçalho do agente do usuário
        response = requests.get(url, headers=headers)
        
        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Retorna os dados da empresa (presumindo que a API retorna dados JSON)
            data = response.json()
            return data
        else:
            return f"Erro na solicitação. Código de status: {response.status_code}"
    except Exception as e:
        return f"Ocorreu um erro: {e}"

    
def generate_pdf(data_hora_formatada, titulo, dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título do PDF
    pdf.cell(200, 10, txt=titulo, ln=True)

    # Dados do PDF
    for chave, valor in dados.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)
    
    # Salva o PDF
    pdf_file_path = f"{titulo.replace(' ', '_').lower()}.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path

def calcular_classificacao_e_valor(score):
    if score >= 800:
        return "Baixíssimo", 0.5
    elif score >= 700:
        return "Baixo", 0.4
    elif score >= 500:
        return "Médio", 0.3
    else:
        return "Muito Alto", 0

def calcular_score_e_risco(qtd_animais):
    valor_base = int(qtd_animais) * 500

    if valor_base >= 200000:
        return "Baixíssimo", valor_base
    elif valor_base >= 120000:
        return "Baixíssimo", valor_base
    elif valor_base >= 50000:
        return "Baixo", valor_base
    elif valor_base >= 30000:
        return "Baixo", valor_base
    elif valor_base >= 20000:
        return "Médio", valor_base
    elif valor_base >= 10000:
        return "Médio", valor_base
    elif valor_base >= 7000:
        return "Alto", valor_base
    elif valor_base >= 5000:
        return "Alto", valor_base
    else:
        return "Muito Alto", valor_base

def application():
    # Título do formulário
    st.title("Relatório Comitê de Crédito")
    
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
        score_indice, valor = calcular_classificacao_e_valor(score)
        media_emprestimo = total_media * valor
        
        if st.button("Consultar"):
            if cnpj:
                company_data = get_company_data(cnpj)
                
                if company_data:
                    razao_social = company_data['nome']
                    tipo_empresa = company_data['tipo']
                    abertura = company_data['abertura']
                    
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
                    st.write('NOVO Limite Liberado PJ: ', media_emprestimo)
                    
                    pdf_data = {
                        "Data do Pedido": data_hora_formatada,
                        "Razão Social": razao_social,
                        'CNPJ': cnpj,
                        "Tipo de Empresa": tipo_empresa,
                        'Data da Abertura': abertura,
                        'Média do Faturamento mensal do ano atual': faturamento_mensal_ano_atual,
                        'Média do Faturamento mensal do ano anterior': faturamento_mensal_ano_anterior,
                        'Média do Faturamento mensal': total_media,
                        'SCORE': score,
                        'Risco': score_indice,
                        'NOVO Limite Liberado PJ': media_emprestimo
                    }
                    pdf_file_path = generate_pdf(data_hora_formatada, razao_social, pdf_data)
                    
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

    # Para Pessoa Física
    st.title("Pessoa Física")
    # Campo de entrada para o CPF
    cpf = st.text_input("Por favor, insira o CPF (apenas números):")
    qtd_animais = st.text_input('Quantidade de Animais')

    if qtd_animais:
        score_indice, valor_liberado = calcular_score_e_risco(qtd_animais)
        
        st.write(f"Índice de risco: {score_indice}")
        st.write(f"Valor liberado: R${valor_liberado}")

        if st.button("Gerar PDF - Pessoa Física"):
            if cpf:
                pdf_data = {
                    "Data do Pedido": data_hora_formatada,
                    "CPF": cpf,
                    "Quantidade de Animais": qtd_animais,
                    "Risco": score_indice,
                    "Valor liberado": valor_liberado
                }
                pdf_file_path = generate_pdf(data_hora_formatada, "Dados da Pessoa Física", pdf_data)
                    
                with open(pdf_file_path, "rb") as f:
                    st.download_button(
                        label="Baixe o PDF",
                        data=f,
                        file_name="dados_da_pessoa_fisica.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("Por favor, insira um CPF válido.")

application()


        