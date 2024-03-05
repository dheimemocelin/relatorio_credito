import requests
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import json
import base64
from fpdf import FPDF


def calcular_score_e_risco(valor):
    if valor >= 1000:
        return "Baixíssimo", 200000.00
    elif valor >=501:
        return "Baixíssimo", 120000.00
    elif valor >= 301:
        return "Baixo", 50000.00
    elif valor >= 200:
        return "Baixo", 30000.00
    elif valor >= 101:
        return "Médio", 20000.00
    elif valor >= 50:
        return "Médio", 10000.00
    elif valor >= 30:
        return "Alto",7000.00
    elif valor >= 10:
        return "Alto", 5000.00
    else:
        return "Muito Alto", 0.00
    

def application():
    # Título do formulário
    st.title("Pessoa Física")
    
    # Hora atual
    data_hora_atual = datetime.now()
    
    # Convertendo para uma string formatada
    data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y")

    # Campo de entrada para o CNPJ
    nome = st.text_input('Nome:')
    cnpj = st.text_input("Por favor, insira o N° do CPF (apenas números):")
    qtd_animais = st.text_input('Quantidade Animais')
    
