
# 🏴‍☠️ Rei dos Piratas - Assistente Virtual (Sprint 4 - Integração e IA)

Este repositório contém a versão integrada e de produção do Assistente Virtual Inteligente para a plataforma de e-commerce "Rei dos Piratas". A aplicação utiliza Inteligência Artificial Generativa aliada a um banco de dados relacional em nuvem para automatizar o atendimento ao cliente, responder a dúvidas frequentes (FAQ) e atuar como um curador de mangás com base no estoque real.

## 📌 O Problema
Com o crescimento da base de clientes e do catálogo de produtos, o suporte humano se torna um gargalo operacional e financeiro. Dúvidas repetitivas sobre frete, políticas de devolução e disponibilidade de mangás ocupam tempo útil da equipe.

## 💡 A Solução e Arquitetura
Para resolver este problema, implementamos um assistente baseado em LLM (Large Language Model) utilizando a técnica de **RAG (Retrieval-Augmented Generation) Dinâmico**.

* **Modelo Escolhido:** `llama-3.1-8b-instant` (via Groq Cloud).
* **Integração de Dados:** Oracle Autonomous Database (Cloud).
* **Justificativa:** Optamos pelo LLaMA 3.1 rodando na infraestrutura LPU do Groq devido à latência ultrabaixa (respostas em milissegundos). A API foi construída de forma totalmente *stateless* e assíncrona. Em vez de inventar ou simular dados, o backend conecta-se nativamente ao Oracle DB, consulta a tabela `PRODUTOS` em tempo real e injeta os itens com `ESTOQUE > 0` diretamente no contexto da LLM, blindando a aplicação contra alucinações.

## 🔄 Fluxo de Dados
A aplicação roda isolada em um container Docker, garantindo paridade entre desenvolvimento e produção. O fluxo de funcionamento é o seguinte:

1. **Input (User):** O cliente digita a dúvida na interface web.
2. **Data Fetching (FastAPI + Oracle):** O backend recebe a requisição e faz uma consulta assíncrona (via `oracledb` Thin mode) ao Oracle Cloud para buscar o catálogo atualizado.
3. **Contextualização:** A API monta o `SYSTEM_PROMPT` injetando as regras de negócio da loja e o estado atual do catálogo.
4. **Processamento (Groq):** O payload é enviado para o Groq, que gera a resposta baseada *exclusivamente* no contexto injetado e no histórico enviado pelo client.
5. **Output (Frontend):** A resposta é compilada de Markdown para HTML em tempo real e renderizada na UI com tratamento de concorrência e animações nativas.

## 🛠️ Tecnologias Utilizadas
* **Python 3.11 (Slim):** Linguagem base da aplicação.
* **FastAPI & Uvicorn:** Framework web moderno e assíncrono para a API REST.
* **OracleDB Driver:** Driver nativo para consultas assíncronas ao banco de dados.
* **Groq SDK:** Cliente para comunicação ultrarrápida com a LLM.
* **Docker & Docker Compose:** Containerização e orquestração do ambiente.
* **Vanilla JS + Marked.js:** Interface de usuário fluida, resiliente a spam de requisições e com renderização de Markdown.

## 🚀 Como Executar o Projeto

**Pré-requisitos:**
* Docker e Docker Compose instalados.
* Chave de API válida do Groq (`GROQ_API_KEY`).
* Credenciais de acesso ao banco Oracle Cloud.

**Passo a passo:**
1. Clone este repositório:
   ```bash
   git clone [https://github.com/Dejota-04/IA-RDP.git](https://github.com/Dejota-04/IA-RDP.git)
   cd IA-RDP



2.  Crie um arquivo `.env` na raiz do projeto e insira as credenciais:



    ```
    GROQ_API_KEY=gsk_sua_chave_aqui
    GROQ_MODEL=llama-3.1-8b-instant

    # Credenciais Oracle DB
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_DSN=(description=(retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.sa-saopaulo-1.oraclecloud.com))(connect_data=(service_name=seu_service_name.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))

    ```

3.  Suba o container usando o Docker Compose:

    Bash

    ```
    docker compose up -d --build

    ```

4.  Acesse a interface de chat: 👉 **http://localhost:8000**

5.  _(Opcional)_ Acesse o Swagger da API: 👉 **http://localhost:8000/docs**


## 🎥 Demonstração (Vídeo Pitch - Sprint 4)

Assista à demonstração da arquitetura e da integração real com o Oracle DB funcionando na prática:

🔗 **[INSERIR O NOVO LINK DO YOUTUBE AQUI]**


## Diagrama do projeto

<img width="1124" height="624" alt="image" src="https://github.com/user-attachments/assets/513113ce-1bd9-417b-9e94-326ce8108396" />

## 👥 Equipe (Grupo CATECH)

-   Daniel Santana Corrêa Batista [RM559622]

-   Wendell Nascimento Dourado [RM559336]

-   Jonas de Jesus Campos de Oliveira [RM561144]



