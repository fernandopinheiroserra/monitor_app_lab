# Master Alert

Master Alert é um serviço desenvolvido em Python com FastAPI para monitorar a presença de sistemas enviando "heartbeats" a cada 30 segundos. Se o sistema monitorado falhar em enviar um ping dentro de 1 minuto, o Master Alert registra a ausência no banco de dados MongoDB na nuvem. O projeto inclui endpoints para monitoramento e dashboard para acompanhamento de consultas ao banco de dados.

## Tecnologias Utilizadas

Python 3.10+
FastAPI - para criação da API REST.
MongoDB - banco de dados na nuvem para registrar a ausência de heartbeats.
Uvicorn - servidor ASGI para executar a aplicação FastAPI.

## Funcionalidades

Heartbeat Endpoint: Recebe um ping a cada 30 segundos do sistema monitorado.
Registro de Ausência: Se não receber um heartbeat dentro de 1 minuto, registra a ausência no MongoDB.
Dashboard: Visualização do status das ausências com base nas consultas ao banco de dados.

## Requisitos

Python 3.10 ou superior
MongoDB Atlas (ou outro MongoDB na nuvem)
Dependências descritas no arquivo requirements.txt

## Estrutura

master-alert/
│
├── app/
│   ├── main.py
│   ├── heartbeat.py
│   ├── database.py
│   └── models.py
├── .env
├── requirements.txt
└── README.md
