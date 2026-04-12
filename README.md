
# 🏴‍☠️ Rei dos Piratas - Assistente Virtual (Sprint 3 - IA)

Este repositório contém a Prova de Conceito (PoC) do Assistente Virtual Inteligente para a plataforma de e-commerce "Rei dos Piratas". A aplicação utiliza Inteligência Artificial Generativa para automatizar o atendimento ao cliente, responder a dúvidas frequentes (FAQ) e atuar como um curador de mangás.

## 📌 O Problema
Com o crescimento da base de clientes e do catálogo de produtos, o suporte humano se torna um gargalo operacional e financeiro. Dúvidas repetitivas sobre frete, políticas de devolução e disponibilidade de mangás ocupam tempo útil da equipe.

## 💡 A Solução e Justificativa do Modelo
Para resolver este problema, implementamos um assistente baseado em LLM (Large Language Model) utilizando a técnica de **RAG (Retrieval-Augmented Generation)** simulado.

* **Modelo Escolhido:** `llama-3.1-8b-instant` (via Groq Cloud).
*  **Justificativa:** Optamos pelo LLaMA 3.1 rodando na infraestrutura LPU do Groq devido à **latência ultrabaixa** (respostas em milissegundos) e **custo zero** para desenvolvimento[cite: 200]. Modelos locais (como Ollama) exigiriam hardware dedicado pesado, enquanto o Groq nos permite escalar a aplicação com baixo custo e alta performance, essencial para uma experiência mobile fluida. A versão 3.1 de 8 bilhões de parâmetros é mais do que suficiente para tarefas de NLP como recomendação de produtos e FAQ.

## 🔄 Arquitetura e Fluxo de Dados
A aplicação foi isolada em um container Docker, garantindo paridade entre desenvolvimento e produção.  O fluxo de funcionamento da IA é o seguinte[cite: 202, 203]:

1. **Input (User):** O cliente digita a dúvida na interface web.
2. **Backend (FastAPI):** A API recebe a requisição e injeta o `SYSTEM_PROMPT` contendo o contexto dinâmico do negócio.
3.  **Dados Utilizados:** O contexto contém as regras de negócio da loja (FAQ, frete, pagamentos) e o estado atual do catálogo de mangás em estoque[cite: 201].
4. **Processamento (Groq):** O payload é enviado via API REST para o Groq, que gera a resposta baseada *exclusivamente* no contexto injetado (mitigando alucinações).
5. **Output:** A resposta é renderizada na UI do usuário instantaneamente.

## 🛠️ Tecnologias Utilizadas
* **Python 3.11:** Linguagem base da aplicação.
* **FastAPI:** Framework web moderno e assíncrono para a criação da API REST e geração do Swagger.
* **Groq SDK:** Cliente para comunicação com a LLM.
* **Docker & Docker Compose:** Containerização e orquestração do ambiente.
* **HTML/CSS/JS (Vanilla):** Interface de usuário leve para demonstração.

## 🚀 Como Executar o Projeto

**Pré-requisitos:**
* Docker e Docker Compose instalados.
* Uma chave de API válida do Groq (`GROQ_API_KEY`).

**Passo a passo:**
1. Clone este repositório:
   ```bash
   git clone https://github.com/Dejota-04/IA-RDP.git
   cd IA-RDP



2.  Crie um arquivo `.env` na raiz do projeto e insira sua chave e o modelo:

    Snippet de código

    ```
    GROQ_API_KEY=gsk_sua_chave_aqui
    GROQ_MODEL=llama-3.1-8b-instant

    ```

3.  Suba o container usando o Docker Compose:

    Bash

    ```
    docker compose up -d --build

    ```

4.  Acesse a interface de chat: 👉 **http://localhost:8000**

5.  (Opcional) Acesse a documentação Swagger da API: 👉 **http://localhost:8000/docs**


## 🎥 Demonstração (Vídeo Pitch)

Assista à demonstração do funcionamento da arquitetura e da integração da IA clicando no link abaixo:

🔗 **https://youtu.be/_c_M5mhEKJ0**


## Diagrama do projeto

<img width="1124" height="624" alt="image" src="https://github.com/user-attachments/assets/513113ce-1bd9-417b-9e94-326ce8108396" />


## 👥 Equipe (Grupo CATECH)

-   Daniel Santana Corrêa Batista [RM559622]

-   Wendell Nascimento Dourado [RM559336]

-   Jonas de Jesus Campos de Oliveira [RM561144]
