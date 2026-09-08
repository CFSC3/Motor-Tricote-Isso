import os
from fastapi import APIRouter, UploadFile, Form, File
from ia_service import AnalisadorTextilIA

router = APIRouter()

# O sistema agora busca a chave de forma oculta nas variáveis do Render
CHAVE_API = os.getenv("GEMINI_API_KEY")
servico_ia = AnalisadorTextilIA(api_key=CHAVE_API)

@router.post("/analisar_peca")
async def processar_peca(
    categoria: str = Form(...),
    tamanho_alvo: str = Form(...),
    imagem: UploadFile = File(...)
):
    image_data = await imagem.read()
    resultado = await servico_ia.analisar_imagem(
        image_data=image_data,
        mime_type=imagem.content_type,
        categoria=categoria,
        tamanho_alvo=tamanho_alvo
    )
    return resultado
