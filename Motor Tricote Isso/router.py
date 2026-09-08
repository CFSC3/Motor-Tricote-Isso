from fastapi import APIRouter, UploadFile, Form, File
from ia_service import AnalisadorTextilIA

router = APIRouter()

# Injeção da chave diretamente no construtor do serviço
CHAVE_API = "AQ.Ab8RN6Ih9iFVlJEpLyQDOpjHujaJV0TbTVT2EIaS6s5uKUq6Yw"
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