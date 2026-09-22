# **Motor Tricote Isso**

O **Motor Tricote Isso** é a inteligência artificial de backend desenvolvida especificamente para dar suporte ao aplicativo mobile **Tricote Isso**, voltado para artesãos de crochê e tricô. O motor processa fotografias de peças artesanais para fornecer estimativas precisas de consumo de fios, recomendações de agulhas, diretrizes técnicas personalizadas e a renderização gráfica de *turnarounds* em múltiplos ângulos (amigurumis e vestuário).

O sistema é construído sobre o framework FastAPI e opera em ambiente de produção corporativa na nuvem, utilizando a infraestrutura avançada do Google Cloud (Vertex AI).

---

## **Estrutura do Projeto**

A arquitetura do sistema está organizada para garantir alta performance, segurança de credenciais e separação clara de responsabilidades:

| **Arquivo** | **Descrição** |
| :--- | :--- |
| `main.py` | Ponto de entrada que inicializa a aplicação FastAPI e configura as rotas básicas. |
| `router.py` | Gerencia os endpoints de processamento, recebendo uploads de imagens e dados de formulário (categoria, tamanho, mão dominante e tensão do ponto). |
| `ia_service.py` | Implementa a classe `AnalisadorTextilIA`. Utiliza o modelo `gemini-1.5-flash-002` via Vertex AI para análise visual e estruturação da ficha técnica têxtil. |
| `ia_image_service.py` | Implementa a classe `GeradorImagensIA`. Utiliza o modelo de ponta `imagen-3.0-generate-002` para renderizar folhas de referência em múltiplos ângulos (3 views). |
| `schemas.py` | Define a estrutura de dados via Pydantic, garantindo validação rigorosa de esquemas JSON. |

---

## **Tecnologias Utilizadas**

- **FastAPI**: Framework moderno de alta performance para a construção de APIs em Python.
- **Google Cloud Vertex AI & Google GenAI SDK**: Plataforma corporativa de IA para processamento multimodal e geração gráfica.
  - `gemini-1.5-flash-002`: Análise visual rápida e extração de dados têxteis.
  - `imagen-3.0-generate-002`: Geração de imagens fotorrealistas de alta fidelidade para amigurumis e peças de vestuário.
- **Render (Cloud Hosting)**: Hospedagem web com suporte a injeção segura de arquivos de configuração via *Secret Files*.
- **Pydantic**: Biblioteca para validação e tipagem de dados.

---

## **Funcionalidades**

- **Análise Têxtil Inteligente**: Identificação automática de padrões, cores e complexidade de pontos a partir de fotos.
- **Cálculo Preciso de Metragem**: Estimativa de novelos necessários considerando margem de segurança e ajustes por tensão de ponto.
- **Diretrizes Personalizadas**: Recomendações adaptadas ao perfil do artesão (como orientações específicas para usuários canhotos).
- **Geração Gráfica de Turnaround**: Criação automática de vistas ortográficas (frente, perfil e costas) de bonecos e peças de vestuário em manequim invisível.

---

## **Configuração e Execução**

### **1. Requisitos de Ambiente**
- Python 3.9+
- Conta no Google Cloud configurada com o Vertex AI ativado no projeto do Firebase (`loveyou-21e3d`).

### **2. Autenticação e Segurança (Produção / Render)**
Em vez de expor chaves de API em texto plano, o motor utiliza o arquivo de credenciais da Conta de Serviço (`tricoteIssoVertex.json`).
- No ambiente de produção (Render), o arquivo é injetado diretamente na raiz do servidor através da ferramenta de **Secret Files**.
- A variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` aponta automaticamente para o caminho do arquivo seguro.

### **3. Instalação Local e Execução**
Para rodar o ambiente de desenvolvimento localmente:

     # Instale as dependências
     pip install -r requirements.txt
    
    # Inicie o servidor local via Uvicorn
    uvicorn main:app --reload

O servidor estará disponível em `http://localhost:8000`. Você pode acessar a documentação interativa da API em `/docs`.

---

**Responsável pelo Projeto:** Carlos Felipe 

**Data da última atualização:** 22/09/2026
