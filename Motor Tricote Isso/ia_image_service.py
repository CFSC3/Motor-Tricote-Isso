import os
import asyncio
import base64
from google import genai
from google.genai import types

class GeradorImagensIA:
    def __init__(self, api_key: str = ""):
        # Aponta para o arquivo JSON de credenciais
        caminho_credenciais = os.path.join(os.path.dirname(__file__), 'tricoteIssoVertex.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_credenciais

        # Inicializa o cliente no modo Enterprise
        self.client_visao = genai.Client(
            enterprise=True,
            project="loveyou-21e3d",
            location="global"
         )
        
        # Cliente para o Gemini Flash Image
        self.client_gerador = genai.Client(
            vertexai=True,
            project="loveyou-21e3d", 
            location="global"   
        )
        
        self.modelo_visao = 'gemini-3.8-flash'
        self.modelo_gerador = 'gemini-2.5-flash-image'

    async def gerar_turnaround_amigurumi(self, image_data: bytes, mime_type: str, categoria: str, tex_recomendado: str, tensao_ponto: str, cores_identificadas: str) -> dict:
        categoria_limpa = categoria.strip()
        escolhas_adversas = categoria_limpa in ["Roupas (Vestuário)", "Bebê e Infantil", "Pets", "Acessórios", "Casa e Decoração"]

        # ==========================================
        # PASSO 1: EXTRAÇÃO (Usa client_visao)
        # ==========================================
        if escolhas_adversas:
            prompt_extracao = """
            Você é um diretor de arte focado em moda artesanal. Analise a imagem enviada.
            Concentre-se APENAS na peça de roupa ou acessório de tricô/crochê presente na imagem. 
            REGRA DE ISOLAMENTO: Ignore completamente fundos, cenários, a pessoa/animal vestindo a peça e quaisquer adereços externos.
            Extraia o design estrutural: tipo de gola, mangas, caimento, texturas e padrões visíveis.
            Retorne APENAS a descrição física crua e detalhada da PEÇA em inglês.
            """
        else:
            prompt_extracao = """
            Você é um diretor de arte. Analise a imagem enviada.
            REGRA DE ISOLAMENTO: Ignore completamente fundos, cenários (como ilhas, árvores), adereços externos e símbolos flutuantes. 
            Extraia a identidade visual primária EXCLUSIVA DO PERSONAGEM PRINCIPAL: formato dos olhos, detalhes marcantes e proporções corporais.
            Retorne APENAS a descrição física crua e detalhada em inglês. Não mencione o estilo original da foto.
            """
        
        tentativas_visao = 3
        descricao_extraida = ""
        
        for tentativa in range(tentativas_visao):
            try:
                response_visao = await self.client_visao.aio.models.generate_content(
                    model=self.modelo_visao,
                    contents=[
                        types.Part.from_bytes(data=image_data, mime_type=mime_type),
                        prompt_extracao,
                    ],
                    config=types.GenerateContentConfig(temperature=0.2)
                )
                descricao_extraida = response_visao.text.strip()
                break
                
            except Exception as e:
                if tentativa == tentativas_visao - 1:
                    return {
                        "sucesso": False,
                        "imagem_multi_angulo_base64": "",
                        "descricao_interpretada": f"Falha na leitura visual após {tentativas_visao} tentativas: {str(e)}"
                    }
                await asyncio.sleep(4 * (tentativa + 1))

        # ==========================================
        # PREPARAÇÃO DA FÍSICA DO MATERIAL
        # ==========================================
        aperto_ponto = "tight, flawless stitches" 
        if "Apertada" in tensao_ponto.lower():
            aperto_ponto = "very tight, dense and stiff stitches, completely closed gaps"
        elif "Frouxa" in tensao_ponto.lower():
            aperto_ponto = "loose and relaxed stitches, soft drape, slightly visible gaps"

        espessura_fio = "fine cotton yarn"
        if "alto" in tex_recomendado.lower() or "grosso" in tex_recomendado.lower() or "pelúcia" in tex_recomendado.lower():
            espessura_fio = "chunky thick chenille yarn, fluffy and expansive texture"

        textura_final = f"""
        Material: {espessura_fio}, crocheted/knitted with {aperto_ponto}.
        Mandatory Colors: Use STRICTLY these yarn colors: {cores_identificadas}.
        STRICT RULE: EVERYTHING in this design MUST be made of physical yarn/crochet. 
        NO real fabric, NO plastic, NO leather, NO smooth textures allowed. The ONLY exception is shiny acrylic safety eyes.
        """

        if escolhas_adversas:
            prompt_imagem = f"""
            A professional clothing design turnaround reference sheet. 
            Layout: 3 views side-by-side (Front view, Side view, Back view) on a clean neutral studio background.
            Subject: A handcrafted garment/accessory piece: {descricao_extraida}.
            IMPORTANT: Display the item on an INVISIBLE GHOST MANNEQUIN. NO humans, NO animals, NO dolls. ONLY the clothing/accessory.
            Material Physics: {textura_final}
            Style: Highly detailed physical product photography, studio lighting, realistic knit/crochet fibers and yarn fuzz.
            """
        else:
            prompt_imagem = f"""
            A professional character design turnaround reference sheet. 
            Layout: 3 views side-by-side (Front view, Side view, Back view) on a clean neutral studio background.
            Subject: A handmade 3D crochet amigurumi doll of this character: {descricao_extraida}.
            Material Physics: {textura_final}
            Style: Cute, highly detailed physical product photography, studio lighting, realistic crochet fibers and yarn fuzz.
            """

        # ==========================================
        # PASSO 2: RENDERIZAÇÃO (Usa client_gerador com novo formato)
        # ==========================================
        tentativas_imagem = 6
        for tentativa in range(tentativas_imagem):
            try:
                # Mudança crucial: generate_content com response_modalities
                resultado_imagem = await self.client_gerador.aio.models.generate_content(
                    model=self.modelo_gerador,
                    contents=prompt_imagem,
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                        candidate_count=1,
                    )
                )

                imagem_bytes = None
                # Varre a resposta buscando o bloco que contém os dados da imagem
                for part in resultado_imagem.candidates[0].content.parts:
                    if part.inline_data:
                        imagem_bytes = part.inline_data.data
                        break

                if not imagem_bytes:
                    raise ValueError("O modelo gerou a resposta, mas não incluiu os dados da imagem.")

                imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')

                return {
                    "sucesso": True,
                    "imagem_multi_angulo_base64": imagem_base64,
                    "descricao_interpretada": descricao_extraida
                }

            except Exception as erro:
                if tentativa == tentativas_imagem - 1:
                    return {
                        "sucesso": False,
                        "imagem_multi_angulo_base64": "",
                        "descricao_interpretada": f"Falha após {tentativas_imagem} tentativas de renderização. Detalhe: {str(erro)}"
                    }
                await asyncio.sleep(4 * (tentativa + 1))