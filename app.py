import os
import requests
import json
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, render_template
from sheets import autentica_sheets, compara_lista
from gpt import analisa_imagem, analisa_texto
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#Credencial para uso da API do ChatGPT
ROBO_GPT_TOKEN = os.environ["ROBO_GPT_TOKEN"]

#Credencial para uso da API do Google Sheets
arquivo_credenciais = "petroleo-em-tudo-9f1b09147a04.json"
conteudo_credenciais = os.environ["GSPREAD_CREDENTIALS"]
with open(arquivo_credenciais, mode="w") as arquivo:
    arquivo.write(conteudo_credenciais)
conta = ServiceAccountCredentials.from_json_keyfile_name(arquivo_credenciais)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Pasta onde as imagens serão armazenadas localmente

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # Captura os termos da primeira coluna da planilha
        all_terms = []
        folha = autentica_sheets("1JP0cZ_TVzicML0hQA6mXJA6w8ecqlgZv96RCxpPTucs")
        all_terms.extend(folha.col_values(1)[1:])

        return render_template('index.html', termos=all_terms)
    
    if request.method == 'POST':
        if 'image' in request.files:
            # Processar imagem
            image = request.files['image']
            image_path = "temp_image.jpg"
            image.save(image_path)

            resultado,input = analisa_imagem(image_path)

            if isinstance(resultado, list):
                 return render_template('resultado_lista.html', resultado = resultado, input=input)
            elif isinstance(resultado, str):
                return render_template('resultado.html', resultado = resultado)
            
        elif 'texto' in request.form:
            # Processar texto
            input = request.form['texto']

            resultado = analisa_texto(input)

            if isinstance(resultado, list):
                 return render_template('resultado_lista.html', resultado = resultado, input=input)
            elif isinstance(resultado, str):
                return render_template('resultado.html', resultado = resultado, input=input)
        
        elif 'substance' in request.form:
            # Se o formulário submetido for o dropdown
            input = request.form['substance']

            resultado = compara_lista(input)

            return render_template('resultado_lista.html', input=input, resultado=resultado)

    return render_template('index.html')


@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')

if __name__ == '__main__':
    app.run(debug=True)