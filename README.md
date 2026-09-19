# **Motor Tricote Isso**

O **Motor Tricote Isso** é uma ferramenta inteligente desenvolvida especificamente para artesãos de crochê e tricô. O núcleo deste projeto é um motor de Inteligência Artificial capaz de analisar fotografias de peças artesanais para fornecer estimativas precisas de consumo de fios, recomendações de agulhas e diretrizes técnicas personalizadas, visando a redução do desperdício de materiais no processo criativo.

O backend é construído sobre o framework FastAPI para processamento eficiente de imagens. O roadmap futuro do projeto inclui funcionalidades de precificação automática e visualização de peças em 3D.

## **Estrutura do Projeto**

A arquitetura do sistema está organizada para garantir escalabilidade e clareza na separação de responsabilidades. Abaixo estão descritos os principais arquivos:

| **Arquivo** | **Descrição** |
| :--- | :--- |
| `main.py` | Ponto de entrada que inicializa a aplicação FastAPI e configura as rotas básicas. |
| `router.py` | Gerencia o endpoint `/analisar_peca`, processando uploads de imagens e dados de formulário (categoria, tamanho, mão dominante e tensão do ponto). |
| `ia_service.py` | Implementa a classe `AnalisadorTextilIA`. Utiliza a Gemini API (`gemini-3.6-flash`) para análise visual e geração da `FichaTecnica`. Contém prompts otimizados para categorias como Roupas, Bebê, Pets e Geral. |
| `schemas.py` | Define a estrutura de dados via Pydantic, incluindo os modelos `FioCor` e `FichaTecnica` para garantir saídas JSON validadas. |

## **Tecnologias Utilizadas**

Para garantir a robustez e a modernidade da solução, foram utilizadas as seguintes tecnologias:

- **FastAPI**: Framework moderno de alta performance para a construção de APIs em Python.
- **Google GenAI SDK (Gemini API)**: Motor de inteligência artificial multimodal para análise de imagens e raciocínio técnico têxtil.
- **Pydantic**: Biblioteca para validação de dados e gerenciamento de configurações por meio de modelos de dados Python.

## **Funcionalidades**

O sistema oferece um conjunto de recursos focados na otimização do trabalho artesanal:

- **Análise de Imagem por IA**: Identificação automática de padrões de pontos e complexidade da peça através de fotos.
- **Cálculo de Metragem e Novelos**: Estimativa detalhada da quantidade de fio necessária, incluindo uma margem de segurança de 15% para evitar faltas durante a produção.
- **Sugestão Técnica**: Recomendação de valores de Tex (densidade do fio) e numeração ideal de agulhas com base na peça analisada.
- **Orientações Personalizadas**: Geração de diretrizes específicas que consideram o perfil do artesão, como adaptações para usuários canhotos e ajustes baseados na tensão do ponto.

## **Configuração e Execução**

Para configurar o ambiente de desenvolvimento e executar o servidor localmente, siga os passos abaixo:

### **1. Requisitos de Ambiente**
Certifique-se de ter o Python 3.9+ instalado. É recomendável o uso de um ambiente virtual (`venv`).

### **2. Variáveis de Ambiente**
Configure a sua chave de API para o serviço Gemini:
```bash
export GEMINI_API_KEY="SUA_CHAVE_AQUI"
