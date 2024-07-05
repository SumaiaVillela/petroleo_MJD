import base64
import requests
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from sheets import autentica_sheets, compara_lista


#Credencial para uso da API do ChatGPT
ROBO_GPT_TOKEN = os.environ["ROBO_GPT_TOKEN"]


#Analisando textos

def analisa_texto(input):
  
  termos_presentes = compara_lista(input)

  if termos_presentes:
    resposta = termos_presentes

  elif not termos_presentes:
    prompt = "Analise se o termo ou a lista de termos enviada tem derivados de petróleo. Caso exista alguma substância geralmente derivada de petróleo, indique, de forma objetiva, qual é ou quais são e em que produtos normalmente é usada ou são usadas. Caso não tenha, informe que não foi possível encontrar dentro do limite dos seus conhecimentos (e não acrescente nada mais sobre que produtos ou substâncias podem ser derivadas do petróleo). Se o input for uma mensagem dizendo que não foi possível extrair texto da imagem ou que não há substâncias na imagem, diga literalmente que não foi possível fazer a análise com base no que foi extraído da imagem. O retorno deste prompt precisa ter no máximo 300 tokens."
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ROBO_GPT_TOKEN}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },

                    {
                        "type": "text",
                        "text": input
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    resposta = response.json()['choices'][0]['message']['content']

    prova = autentica_sheets("1qqHt7RTxKevh3ZmLRovW_NzWSVNaK3GituqFPVvsCnQ")
    prova.append_row([input, prompt, resposta], value_input_option='RAW')

  return resposta



#Extraindo o texto das imagens e analisando

def analisa_imagem(image_path):
  # Transformando uma imagem em um arquivo legível para o OpenAI
  with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
  prompt = "Existe uma lista de ingredientes nesta imagem. O trecho normalmente começa com 'composição', 'ingredientes', 'ingredients', 'ingr' ou uma palavra sinônima. Extraia essa lista de ingredientes."
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ROBO_GPT_TOKEN}"
  }

  payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  texto_extraido = response.json()['choices'][0]['message']['content']

  resposta = analisa_texto(texto_extraido)

  resultado = {"texto_extraido": texto_extraido, "resposta": resposta}

  return resultado
