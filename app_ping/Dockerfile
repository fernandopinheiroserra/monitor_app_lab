# Usar a imagem oficial do Python
FROM python:3.9

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos da aplicação para o diretório de trabalho
COPY . /app

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o emulador de ping
CMD ["python", "ping.py"]