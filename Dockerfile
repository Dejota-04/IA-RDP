# Usamos a versão 'slim' do Python.
# Imagens menores significam deploys mais rápidos, menos custos de rede e menor superfície de ataque (segurança).
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia os requirements primeiro (isso otimiza o cache do Docker)
COPY requirements.txt .

# Instala as dependências sem guardar cache inútil
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da sua API
COPY main.py index.html ./

# Expõe a porta que o FastAPI vai rodar
EXPOSE 8000

# O comando para rodar o servidor.
# O host 0.0.0.0 é obrigatório no Docker para que a porta seja acessível do lado de fora do container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]