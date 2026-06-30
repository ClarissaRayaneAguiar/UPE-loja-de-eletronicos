import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_REMETENTE = "llekkxysmicrowear@gmail.com"
SENHA_APP = "oelmehgqaagqjzul"

def enviar_email_boas_vindas(destinatario: str, nome: str):
    assunto = "Bem-vindo a UPE Loja de Eletronicos!"
    corpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
            <div style="background-color: #003399; color: white; padding: 20px; text-align: center;">
                <h1 style="margin: 0;">UPE LOJA DE ELETRÔNICOS</h1>
            </div>
            <div style="padding: 30px;">
                <h2 style="color: #003399;">Ola, {nome}!</h2>
                <p>Seu cadastro foi realizado com sucesso no sistema <strong>UPE Loja de Eletronicos</strong>.</p>
                <p>Agora voce pode acessar o sistema com seu email e senha.</p>
                <p style="margin-top: 30px;">Atenciosamente,<br><strong>Equipe UPE Loja de Eletronicos</strong></p>
            </div>
            <div style="background-color: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #666;">
                <p>Este email foi enviado automaticamente. Por favor, nao responda.</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "html"))

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_APP)
        servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        servidor.quit()
        print(f"Email enviado para {destinatario}")
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False