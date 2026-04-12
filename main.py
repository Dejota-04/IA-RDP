import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Rei dos Piratas - IA Assistant API")

class ChatRequest(BaseModel):
    message: str

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Você é o assistente virtual de vendas da loja geek 'Rei dos Piratas'.
Sua missão é ajudar os clientes com dúvidas e recomendar mangás.

Regras e FAQ da loja:
- Frete grátis para compras acima de R$ 150,00.
- Aceitamos devoluções em até 7 dias após o recebimento.
- Formas de pagamento: PIX, Cartão de Crédito em até 6x sem juros.

Estoque simulado atual:
- One Piece Vol. 1 ao 10 (Novo) - R$ 35,00 cada
- Chainsaw Man Vol. 1 (Usado) - R$ 20,00
- Berserk Vol. 1 (Edição de Luxo) - R$ 120,00

Instruções:
Seja educado, focado em vendas e use um tom levemente geek/pirata.
Não invente produtos que não estão no estoque simulado. Responda de forma concisa.
use frase com até 30 palavras.
"""

# Memória volátil In-Memory (Ideal para a PoC).
# Em produção, isso seria um banco de dados (ex: Redis ou PostgreSQL) vinculado ao ID do usuário.
# ATENÇÃO LGPD: Evitar persistir dados sensíveis (PII) que o usuário possa digitar no chat.
chat_history = []

@app.get("/", summary="Interface de Chat UI", include_in_schema=False)
async def get_ui():
    return FileResponse("index.html")

@app.post("/api/chat", summary="Conversar com a IA")
async def chat_with_ai(request: ChatRequest):
    global chat_history

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode ser vazia.")

    # 1. Adiciona a nova mensagem do usuário no histórico
    chat_history.append({"role": "user", "content": request.message})

    # 2. Limita o histórico para não estourar o limite de tokens da LLM
    # Mantemos apenas as últimas 10 interações
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    # 3. Monta o array de mensagens: System Prompt fixo + Histórico
    messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    try:
        chat_completion = client.chat.completions.create(
            messages=messages_payload,
            model=os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0.3,
        )

        resposta_ia = chat_completion.choices[0].message.content

        # 4. Salva a resposta da IA no histórico para ela lembrar do que disse
        chat_history.append({"role": "assistant", "content": resposta_ia})

        return {"reply": resposta_ia}

    except Exception as e:
        print(f"Erro no Groq: {e}")
        # Em caso de erro, remove a mensagem do usuário do histórico para não corromper o fluxo
        chat_history.pop()
        raise HTTPException(status_code=500, detail="Falha na comunicação com a Grand Line.")

# Rota extra para limpar a memória (útil para regravar o vídeo sem reiniciar o container)
@app.delete("/api/chat/clear", summary="Limpar histórico de chat")
async def clear_chat():
    global chat_history
    chat_history = []
    return {"message": "Memória apagada. O barco zarpou do zero."}