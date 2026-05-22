import os
import json
import oracledb
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Rei dos Piratas - IA Assistant API")

# Conecta ao Redis de forma assíncrona.
# O fallback "redis://redis:6379/0" garante que vai funcionar no Docker Compose.
redis_client = redis.from_url(os.environ.get("REDIS_URL", "redis://redis:6379/0"), decode_responses=True)

class ChatRequest(BaseModel):
    message: str
    session_id: str  # <- Identificador único exigido pelo back-end agora

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def get_dynamic_context() -> str:
    """
    Conecta ao Oracle DB de forma assíncrona, busca o estoque atualizado
    e injeta as informações no System Prompt.
    """
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_dsn = os.environ.get("DB_DSN")

    estoque_linhas = []

    try:
        async with oracledb.connect_async(user=db_user, password=db_password, dsn=db_dsn) as connection:
            async with connection.cursor() as cursor:
                sql = """
                    SELECT NOME, PRECO
                    FROM PRODUTOS
                    WHERE ESTOQUE > 0
                """
                await cursor.execute(sql)
                rows = await cursor.fetchall()

                for row in rows:
                    nome = row[0]
                    preco = row[1]
                    estoque_linhas.append(f"- {nome} - R$ {preco:.2f}")

    except Exception as e:
        print(f"Erro ao conectar/consultar o Oracle DB: {e}")
        estoque_linhas.append("Aviso: Não foi possível carregar o estoque em tempo real.")

    estoque_formatado = "\n".join(estoque_linhas) if estoque_linhas else "Nenhum mangá disponível no estoque no momento."

    return f"""
    Você é Takamura, assistente de vendas da loja de mangás "Rei dos Piratas".

    [ESTOQUE DISPONÍVEL]
    Informe SOMENTE produtos desta lista. Nunca invente itens ou altere preços:
    {estoque_formatado}

    [ESCOPO — LEIA COM ATENÇÃO]
    DENTRO do escopo (sempre responda normalmente):
    - Qualquer mangá ou anime, mesmo que não esteja no estoque
    - Dúvidas sobre frete, pagamento e devoluções

    FORA do escopo (use a resposta padrão abaixo):
    - Assuntos completamente não relacionados: matemática, programação, culinária, política, etc.
    Resposta padrão para fora do escopo: "Opa! Só entendo de mangás e dúvidas da loja. Quer ver nosso estoque?"

    [REGRAS DE NEGÓCIO]
    - Mangá no estoque: informe o preço e disponibilidade.
    - Mangá FORA do estoque: diga que está esgotado/indisponível e sugira similares do catálogo.
    - Frete grátis apenas em compras acima de R$ 150,00. Abaixo disso, o frete é calculado no checkout. Nunca calcule o valor do frete.
    - Pagamento: PIX ou Cartão de Crédito em até 6x sem juros.
    - Devoluções aceitas em até 7 dias após o recebimento.

    [COMPORTAMENTO]
    Tom: amigável, direto, levemente descontraído.
    Limite: máximo 40 palavras por resposta.
    """

@app.get("/", summary="Interface de Chat UI", include_in_schema=False)
async def get_ui():
    return FileResponse("index.html")

@app.post("/api/chat", summary="Conversar com a IA")
async def chat_with_ai(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode ser vazia.")

    # Cria a chave única para esse usuário no Redis
    session_key = f"chat:{request.session_id}"

    # 1. Recupera o histórico existente no Redis
    history_str = await redis_client.get(session_key)
    chat_history = json.loads(history_str) if history_str else []

    # 2. Adiciona a nova mensagem
    chat_history.append({"role": "user", "content": request.message})

    # 3. Limita o histórico para não estourar tokens
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    # 4. Aguarda a construção assíncrona do contexto via Oracle DB
    system_prompt = await get_dynamic_context()
    messages_payload = [{"role": "system", "content": system_prompt}] + chat_history

    try:
        # Chamada para o Groq
        chat_completion = client.chat.completions.create(
            messages=messages_payload,
            model=os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0.3,
        )

        resposta_ia = chat_completion.choices[0].message.content

        # 5. Salva a resposta da IA no histórico
        chat_history.append({"role": "assistant", "content": resposta_ia})

        # 6. Salva tudo de volta no Redis (Expira em 3600 segundos / 1 Hora)
        await redis_client.set(session_key, json.dumps(chat_history), ex=3600)

        return {"reply": resposta_ia}

    except Exception as e:
        print(f"Erro no Groq: {e}")
        raise HTTPException(status_code=500, detail="Falha na comunicação com a Grand Line.")

@app.delete("/api/chat/clear", summary="Limpar histórico de chat")
async def clear_chat(session_id: str):
    # Rota ajustada para limpar apenas a memória do usuário que pediu
    await redis_client.delete(f"chat:{session_id}")
    return {"message": "Memória apagada. O barco zarpou do zero."}