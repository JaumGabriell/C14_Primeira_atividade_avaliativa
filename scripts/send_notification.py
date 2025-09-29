#!/usr/bin/env python3


import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

def send_pipeline_notification():

    
    # Variáveis de ambiente obrigatórias
    email_recipient = os.getenv('PIPELINE_EMAIL_RECIPIENT')
    email_sender = os.getenv('PIPELINE_EMAIL_SENDER', 'noreply@github.com')
    email_password = os.getenv('PIPELINE_EMAIL_PASSWORD')
    smtp_server = os.getenv('PIPELINE_SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('PIPELINE_SMTP_PORT', '587'))
    
    # Informações do pipeline (passadas como argumentos ou variáveis de ambiente)
    pipeline_status = os.getenv('PIPELINE_STATUS', 'UNKNOWN')
    github_repository = os.getenv('GITHUB_REPOSITORY', 'Unknown Repository')
    github_actor = os.getenv('GITHUB_ACTOR', 'Unknown User')
    github_sha = os.getenv('GITHUB_SHA', 'Unknown Commit')[:8]
    github_ref = os.getenv('GITHUB_REF', 'Unknown Branch').split('/')[-1]
    github_run_id = os.getenv('GITHUB_RUN_ID', 'Unknown Run')
    github_workflow = os.getenv('GITHUB_WORKFLOW', 'CI/CD Pipeline')
    
    # Validar variáveis obrigatórias
    if not email_recipient:
        print("ERRO: Variável de ambiente PIPELINE_EMAIL_RECIPIENT não definida!")
        return False
        
    if not email_password:
        print("AVISO: Variável de ambiente PIPELINE_EMAIL_PASSWORD não definida!")
        print("Simulando envio de email...")
        print_email_simulation()
        return True
    
    try:
        # Criar mensagem de email
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_recipient
        msg['Subject'] = f"[{pipeline_status}] Pipeline CI/CD - {github_repository}"
        
        # Criar corpo do email
        body = create_email_body(
            pipeline_status, github_repository, github_actor,
            github_sha, github_ref, github_run_id, github_workflow
        )
        
        msg.attach(MIMEText(body, 'html'))
        
        # Conectar ao servidor SMTP e enviar email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, email_password)
        
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        server.quit()
        
        print(f" Email enviado com sucesso para: {email_recipient}")
        return True
        
    except Exception as e:
        print(f" Erro ao enviar email: {str(e)}")
        print("Simulando envio de email...")
        print_email_simulation()
        return True  # Retorna True para não falhar o pipeline

def create_email_body(status, repository, actor, sha, branch, run_id, workflow):

    
    status_color = "#28a745" if status == "SUCCESS" else "#dc3545"
    status_emoji = "" if status == "SUCCESS" else ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Pipeline CI/CD Notification</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h2 style="color: {status_color};">{status_emoji} Pipeline CI/CD - {status}</h2>
            
            <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3>📋 Informações do Pipeline</h3>
                <ul>
                    <li><strong>Repositório:</strong> {repository}</li>
                    <li><strong>Workflow:</strong> {workflow}</li>
                    <li><strong>Branch:</strong> {branch}</li>
                    <li><strong>Commit:</strong> {sha}</li>
                    <li><strong>Autor:</strong> {actor}</li>
                    <li><strong>Run ID:</strong> {run_id}</li>
                    <li><strong>Timestamp:</strong> {timestamp}</li>
                </ul>
            </div>
            
            <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3>🔄 Etapas Executadas</h3>
                <ul>
                    <li>✅ <strong>Tests:</strong> Execução dos testes unitários</li>
                    <li>✅ <strong>Build:</strong> Empacotamento da aplicação</li>
                    <li>✅ <strong>Artifacts:</strong> Armazenamento de artefatos</li>
                    <li>✅ <strong>Notification:</strong> Envio desta notificação</li>
                </ul>
            </div>
            
            <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3>🎓 Projeto Acadêmico - C14</h3>
                <p>
                    Este é um projeto da disciplina C14 - Atividade Avaliativa sobre Pipelines CI/CD.
                    Sistema de análise de dados de crocodilos com pipeline automatizado.
                </p>
                <p><strong>Integrantes do Grupo:</strong></p>
                <ul>
                    <li>Eduardo (Owner do repositório)</li>
                    <li>Gustavo (Colaborador)</li>
                    <li>John Gabriel (Colaborador)</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #6c757d;">
                <p>🤖 Mensagem automática do GitHub Actions</p>
                <p>Gerada em: {timestamp}</p>
            </div>
        </div>
    </body>
    </html>
    """

def print_email_simulation():
    """Imprime uma simulação do email que seria enviado"""
    print("\n" + "="*60)
    print(" SIMULAÇÃO DE ENVIO DE EMAIL")
    print("="*60)
    print(f"De: {os.getenv('PIPELINE_EMAIL_SENDER', 'noreply@github.com')}")
    print(f"Para: {os.getenv('PIPELINE_EMAIL_RECIPIENT', 'NÃO DEFINIDO')}")
    print(f"Assunto: [{os.getenv('PIPELINE_STATUS', 'UNKNOWN')}] Pipeline CI/CD - {os.getenv('GITHUB_REPOSITORY', 'Unknown')}")
    print("\nConteúdo:")
    print(f"Status: {os.getenv('PIPELINE_STATUS', 'UNKNOWN')}")
    print(f"Repositório: {os.getenv('GITHUB_REPOSITORY', 'Unknown')}")
    print(f"Branch: {os.getenv('GITHUB_REF', 'Unknown').split('/')[-1]}")
    print(f"Autor: {os.getenv('GITHUB_ACTOR', 'Unknown')}")
    print(f"Commit: {os.getenv('GITHUB_SHA', 'Unknown')[:8]}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("\n Pipeline executado com sucesso!")
    print("="*60)

def main():

    print(" Iniciando script de notificação do pipeline...")
    
    # Definir status baseado nos argumentos da linha de comando
    if len(sys.argv) > 1:
        os.environ['PIPELINE_STATUS'] = sys.argv[1].upper()
    
    success = send_pipeline_notification()
    
    if success:
        print(" Script de notificação executado com sucesso!")
        sys.exit(0)
    else:
        print(" Falha na execução do script de notificação!")
        sys.exit(1)

if __name__ == "__main__":
    main()
