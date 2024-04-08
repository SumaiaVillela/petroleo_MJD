import base64
import os
import requests
import gspread
import unicodedata
from oauth2client.service_account import ServiceAccountCredentials


#Credencial para uso da API do Google Sheets
arquivo_credenciais = "petroleo-em-tudo-9f1b09147a04.json"
conteudo_credenciais = os.environ["GSPREAD_CREDENTIALS"]
with open(arquivo_credenciais, mode="w") as arquivo:
    arquivo.write(conteudo_credenciais)
conta = ServiceAccountCredentials.from_json_keyfile_name(arquivo_credenciais)


# Autenticação para acessar o Google Sheets

def autentica_sheets(key):
    arquivo_credenciais = "petroleo-em-tudo-9f1b09147a04.json"
    conteudo_credenciais = os.environ["GSPREAD_CREDENTIALS"]
    with open(arquivo_credenciais, mode="w") as arquivo:
        arquivo.write(conteudo_credenciais)
    conta = ServiceAccountCredentials.from_json_keyfile_name(arquivo_credenciais)
    api = gspread.authorize(conta)
    planilha = api.open_by_key(key)
    sheet = planilha.worksheet("Sheet1")

    return sheet


# Função para buscar termos da planilha e comparar com o texto extraído

def compara_lista(input):
    sheet = autentica_sheets("1JP0cZ_TVzicML0hQA6mXJA6w8ecqlgZv96RCxpPTucs")

    termos_coluna1 = sheet.col_values(1)
    termos_coluna2 = sheet.col_values(2)
    termos_coluna3 = sheet.col_values(3)
    termos_coluna4 = sheet.col_values(4)

    # Remove a acentuação do texto extraído
    texto_sem_acentos = unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore').decode('utf-8')

    # Verifica se algum termo das colunas está presente no texto extraído
    termos_presentes = []
    
    # Verifica se algum termo da primeira coluna está presente no texto extraído
    for i, termo in enumerate(termos_coluna1):
        termo_sem_acentos = unicodedata.normalize('NFKD', termo).encode('ASCII', 'ignore').decode('utf-8')
        if termo_sem_acentos.lower() in texto_sem_acentos.lower():
            termo_encontrado = termo
            tem_derivado = termos_coluna3[i]
            explicacao = termos_coluna4[i]
            if termo_encontrado:
                termos_presentes.append({
                    'termo_encontrado': termo_encontrado,
                    'tem_derivado': tem_derivado,
                    'explicacao': explicacao
                })

    # Verifica se algum termo da segunda coluna está presente no texto extraído
    if not termos_presentes:  # Se nenhum termo da coluna 1 foi encontrado, verifique a coluna 2
        for i, termo in enumerate(termos_coluna2):
            termo_sem_acentos = unicodedata.normalize('NFKD', termo).encode('ASCII', 'ignore').decode('utf-8')
            if termo_sem_acentos.lower() in texto_sem_acentos.lower():
                termo_encontrado = termo
                tem_derivado = termos_coluna3[i]
                explicacao = termos_coluna4[i]
                if termo_encontrado:
                    termos_presentes.append({
                        'termo_encontrado': termo_encontrado,
                        'tem_derivado': tem_derivado,
                        'explicacao': explicacao
                    })

    return termos_presentes