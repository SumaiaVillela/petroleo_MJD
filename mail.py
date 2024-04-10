import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


#Credencial para uso da API do Brevo
EMAIL_SENHA = os.environ["EMAIL_SENHA"]


def envia_email(input, resultado):
    # Dados para conexão no servidor SMTP:
    smtp_server = "smtp-relay.brevo.com"
    port = 587
    email = "dadosparasumaia@gmail.com"
    password = EMAIL_SENHA

    # Dados para o email que será enviado:
    remetente = "dadosparasumaia@gmail.com"
    destinatarios = ["dadosparasumaia@gmail.com", "alvarojusten@gmail.com"]
    titulo = "Aviso de erro - Gota a Gota"
    texto = f"""
    Olá,

    Foi reportado erro para o seguinte retorno:

    Input: {input}

    Resultado: {resultado}

    """

    html = f"""
    Olá, <br><br>
    Aqui está o resultado da pesquisa:<br>
    Input: {input}<br>
    Resultado: {resultado}<br>
    """

    # Iniciando conexão com o servidor:
    server = smtplib.SMTP(smtp_server, port)  # Inicia a conexão com o servidor
    server.starttls()  # Altera a comunicação para utilizar criptografia
    server.login(email, password)  # Autentica

    # Preparando o objeto da mensagem ("documento" do email):
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = ",".join(destinatarios)
    mensagem["Subject"] = titulo
    conteudo_texto = MIMEText(texto, "plain")  # Adiciona a versão de "texto puro"
    conteudo_html = MIMEText(html, "html")  # Adiciona a versão em HTML
    mensagem.attach(conteudo_texto)
    mensagem.attach(conteudo_html)

    # Enviando o email pela conexão já estabelecida:
    return server.sendmail(remetente, destinatarios, mensagem.as_string())