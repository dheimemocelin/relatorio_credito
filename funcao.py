import requests
import pandas as pd
import numpy as np




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
            print(f"Erro na solicitação. Código de status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

# Função para solicitar CNPJ ao usuário e obter dados da empresa
def main():
    cnpj = input("Por favor, insira o CNPJ da empresa (apenas números): ")
    company_data = get_company_data(cnpj)
    
    if company_data:
        print("Dados da empresa:")
        print(company_data)
    else:
        print("Não foi possível obter os dados da empresa.")

if __name__ == "__main__":
    main()
