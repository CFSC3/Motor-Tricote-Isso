import asyncio
import json
from google import genai
from google.genai import types
from schemas import FichaTecnica

class AnalisadorTextilIA:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.modelo = 'gemini-3.6-flash'

    async def analisar_imagem(self, image_data: bytes, mime_type: str, categoria: str, tamanho_alvo: str) -> dict:

        categoria_limpa = categoria.strip()
        # Roteamento inteligente de prompts baseado na categoria
        if categoria_limpa == "Roupas (Vestuário)":
            prompt = self._montar_prompt_roupa(categoria_limpa, tamanho_alvo)
        elif categoria_limpa == "Bebê e Infantil":
            prompt = self._montar_prompt_bebe(categoria_limpa, tamanho_alvo)
        elif categoria_limpa == "Pets":
            prompt = self._montar_prompt_pet(categoria_limpa, tamanho_alvo)
        else:
            prompt = self._montar_prompt(categoria_limpa, tamanho_alvo)
            
        tentativas_maximas = 3
        
        for tentativa in range(tentativas_maximas):
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.modelo,
                    contents=[
                        types.Part.from_bytes(data=image_data, mime_type=mime_type),
                        prompt,
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=FichaTecnica,
                        temperature=0.0,
                    ),
                )
                return json.loads(response.text)
                
            except Exception as erro:
                if tentativa == tentativas_maximas - 1:
                    return self._gerar_resposta_erro(str(erro))
                await asyncio.sleep(2 * (tentativa + 1))
                
    def _montar_prompt(self, categoria: str, tamanho_alvo: str) -> str:
        return f"""
        Você é uma engenheira têxtil estritamente matemática.
        - Categoria: {categoria}
        - Tamanho final: {tamanho_alvo} cm
        
        REGRAS OBRIGATÓRIAS:
        1. Identifique todas as cores visíveis na peça.
        2. Calcule o volume total e distribua a metragem linear proporcionalmente entre as cores encontradas.
        3. Adicione 15% de margem de segurança sobre o valor de CADA cor. Assuma um novelo padrão de 150 metros.
        4. Crave um único tamanho de agulha (ex: 4.0mm). NUNCA forneça intervalos.
        """

    # NOVO PROMPT EXCLUSIVO PARA ROUPAS (Com altura e largura inferidas)
    def _montar_prompt_roupa(self, categoria: str, tamanho_alvo: str) -> str:
        return f"""
        Você é uma engenheira têxtil estritamente matemática, especializada na confecção de vestuário.
        - Categoria: {categoria}
        - Tamanho de Confecção: {tamanho_alvo} (Padrões de manequim PP, P, M, G, GG)
        
        REGRAS OBRIGATÓRIAS:
        1. Identifique todas as cores visíveis na peça de roupa.
        2. Estime as proporções de altura e largura necessárias para confeccionar a peça no tamanho {tamanho_alvo} para um ser humano adulto.
        3. Calcule a metragem linear de fios necessária para cobrir a área do corpo (frente, costas e mangas, se aplicável) e distribua o valor proporcionalmente entre as cores encontradas.
        4. Adicione 15% de margem de segurança sobre o valor de CADA cor. Assuma um novelo padrão de 150 metros.
        5. Crave um único tamanho de agulha (ex: 4.0mm ou 5.0mm). NUNCA forneça intervalos.
        """

    def _montar_prompt_bebe(self, categoria: str, tamanho_alvo: str) -> str:
        return f"""
        Você é uma engenheira têxtil estritamente matemática, especializada em confecção infantil e para bebês.
        - Categoria: {categoria}
        - Tamanho/Fase: {tamanho_alvo} 
        
        REGRAS OBRIGATÓRIAS:
        1. Identifique todas as cores visíveis na peça.
        2. Estime as proporções (altura, largura, cavas) compatíveis com a idade/fase "{tamanho_alvo}".
        3. Calcule a metragem linear de fios e distribua proporcionalmente entre as cores encontradas.
        4. Adicione 15% de margem de segurança. Assuma um novelo padrão de 150 metros.
        5. Crave um único tamanho de agulha (ex: 3.0mm ou 4.0mm). NUNCA forneça intervalos.
        """

    def _montar_prompt_pet(self, categoria: str, tamanho_alvo: str) -> str:
        return f"""
        Você é uma engenheira têxtil estritamente matemática, especializada em acessórios e roupas para animais.
        - Categoria: {categoria}
        - Porte do Animal: {tamanho_alvo} 
        
        REGRAS OBRIGATÓRIAS:
        1. Identifique todas as cores visíveis na peça.
        2. Estime as proporções anatômicas (circunferência de pescoço, tórax e comprimento) correspondentes ao porte "{tamanho_alvo}".
        3. Calcule a metragem linear de fios necessária para cobrir o dorso/tubo e distribua entre as cores.
        4. Adicione 15% de margem de segurança. Assuma um novelo padrão de 150 metros.
        5. Crave um único tamanho de agulha. NUNCA forneça intervalos.
        """
    
    def _gerar_resposta_erro(self, detalhe: str) -> dict:
        return {
            "fios_necessarios": [],
            "total_novelos_peca": 0,
            "tamanho_agulha_recomendado": "Erro",
            "diretriz_inicial": f"Falha na comunicação com a IA. Detalhe: {detalhe}"
        }