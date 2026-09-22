import os
from fastapi import APIRouter, UploadFile, Form, File
from ia_service import AnalisadorTextilIA
from ia_image_service import GeradorImagensIA

router = APIRouter()

# Instanciando os serviços limpos (eles já leem o arquivo JSON por conta própria)
servico_ia = AnalisadorTextilIA()
servico_imagem_ia = GeradorImagensIA()

@router.post("/analisar_peca")
async def processar_peca(
    categoria: str = Form(...),
    tamanho_alvo: str = Form(...),
    mao_dominante: str = Form(...),  
    tensao_ponto: str = Form(...),   
    imagem: UploadFile = File(...)
):
    image_data = await imagem.read()
    resultado = await servico_ia.analisar_imagem(
        image_data=image_data,
        mime_type=imagem.content_type,
        categoria=categoria,
        tamanho_alvo=tamanho_alvo,
        mao_dominante=mao_dominante, 
        tensao_ponto=tensao_ponto    
    )
    return resultado

# ROTA DA VERSÃO 2 
@router.post("/gerar_projeto_visual")
async def criar_imagens_referencia(
    categoria: str = Form(...),       
    tex_recomendado: str = Form(...),
    tensao_ponto: str = Form(...), 
    cores_identificadas: str = Form(...), 
    imagem: UploadFile = File(...)
):
    image_data = await imagem.read()
    
    resultado = await servico_imagem_ia.gerar_turnaround_amigurumi(
        image_data=image_data,
        mime_type=imagem.content_type,
        categoria=categoria,         
        tex_recomendado=tex_recomendado,
        tensao_ponto=tensao_ponto,
        cores_identificadas=cores_identificadas 
    )
    
    return resultado