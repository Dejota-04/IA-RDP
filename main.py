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
"""

# --- ROTA NOVA PARA O FRONT-END ---
@app.get("/", summary="Interface de Chat UI", include_in_schema=False)
async def get_ui():
    return FileResponse("index.html")
# ----------------------------------

@app.post("/api/chat", summary="Conversar com a IA")
async def chat_with_ai(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode ser vazia.")

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            model=os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0.3,
        )

        return {"reply": chat_completion.choices[0].message.content}

    except Exception as e:
        print(f"Erro no Groq: {e}")
        raise HTTPException(status_code=500, detail="Falha na comunicação com a Grand Line.")