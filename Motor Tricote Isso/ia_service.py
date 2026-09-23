import os
import json
import asyncio
from google import genai
from google.genai import types
from schemas import FichaTecnica

class AnalisadorTextilIA:
    def __init__(self, api_key: str = ""):
        # Aponta para o arquivo JSON de credenciais
        caminho_credenciais = os.path.join(os.path.dirname(__file__), 'tricoteIssoVertex.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_credenciais

        # Inicializa o cliente na plataforma de agente atualizada
        self.client = genai.Client(
            enterprise=True,
            project="loveyou-21e3d",
            location="global"
        )
        
        # Identificador completo compatível com o Vertex AI na SDK nova
        self.modelo_visao = 'gemini-3.8-flash'

    async def analisar_imagem(self, image_data: bytes, mime_type: str, categoria: str, tamanho_alvo: str, mao_dominante: str, tensao_ponto: str) -> dict:

        categoria_limpa = categoria.strip()
        if categoria_limpa == "Roupas (Vestuário)":
            prompt = self._montar_prompt_roupa(categoria_limpa, tamanho_alvo, mao_dominante, tensao_ponto)
        elif categoria_limpa == "Bebê e Infantil":
            prompt = self._montar_prompt_bebe(categoria_limpa, tamanho_alvo, mao_dominante, tensao_ponto)
        elif categoria_limpa == "Pets":
            prompt = self._montar_prompt_pet(categoria_limpa, tamanho_alvo, mao_dominante, tensao_ponto)
        else:
            prompt = self._montar_prompt(categoria_limpa, tamanho_alvo, mao_dominante, tensao_ponto)
            
        tentativas_maximas = 3
        
        for tentativa in range(tentativas_maximas):
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.modelo_visao,
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
                
    def _montar_prompt(self, categoria: str, tamanho_alvo: str, mao_dominante: str, tensao: str) -> str:
        aviso = "ALERTA: A usuária é CANHOTA. Adicione na 'diretriz_inicial' cuidados para a linha não desenrolar ou dar nó durante a torção." if mao_dominante.lower() == "canhota" else ""
        return f"""
        Você é uma engenheira têxtil estritamente matemática.
        - Categoria: {categoria}
        - Tamanho final: {tamanho_alvo} cm
        - Tensão do Ponto: {tensao}
        
        REGRAS:
        1. Identifique as cores e NOMEIE CADA UMA COM UMA ÚNICA PALAVRA OU TOM DEFINITIVO. Proibido usar barras (/) ou dar múltiplas opções (Ex: use "Caramelo" ao invés de "Caramelo / Castanho"). Não inclua a função da cor no nome (Ex: use "Preto" ao invés de "Preto (Cascos)").
        2. Distribua a metragem linear. Ajuste o cálculo de consumo baseado na tensão '{tensao}' (pontos frouxos gastam mais).
        3. Adicione 15% de margem de segurança. Assuma novelos de 150 metros.
        4. Determine a espessura do fio (Tex). Lembre-se: Tex alto = pesado/grosseiro, Tex baixo = maleável/rendado. Gere o valor ideal para 'tex_recomendado'.
        5. Identifique a agulha ideal para o Tex e SEMPRE crave o tamanho MÉDIO (ex: entre 2.5 e 4.5, retorne 3.5mm).
        6. {aviso}
        """

    def _montar_prompt_roupa(self, categoria: str, tamanho_alvo: str, mao_dominante: str, tensao: str) -> str:
        aviso = "ALERTA: A usuária é CANHOTA. Adicione na 'diretriz_inicial' cuidados para a linha não desenrolar ou dar nó durante a torção." if mao_dominante.lower() == "canhota" else ""
        return f"""
        Você é uma engenheira têxtil estritamente matemática, especializada em vestuário.
        - Categoria: {categoria}
        - Tamanho de Confecção: {tamanho_alvo}
        - Tensão do Ponto: {tensao}
        
        REGRAS:
        1. Estime altura/largura e calcule a metragem. Ajuste o consumo considerando a tensão '{tensao}'.
        2. Identifique as cores de forma DEFINITIVA E ÚNICA. Proibido usar barras (/) ou dar opções (Ex: use "Azul" e nunca "Azul / Marinho"). Não descreva partes da peça no nome da cor.
        3. Adicione 15% de margem de segurança. Assuma novelos de 150 metros.
        4. Determine o Tex ideal para caimento de roupas e informe no 'tex_recomendado' (geralmente Tex mais baixo para maleabilidade).
        5. Identifique a variação de agulha e SEMPRE crave o tamanho MÉDIO exato.
        6. {aviso}
        """

    def _montar_prompt_bebe(self, categoria: str, tamanho_alvo: str, mao_dominante: str, tensao: str) -> str:
        aviso = "ALERTA: A usuária é CANHOTA. Adicione na 'diretriz_inicial' cuidados para a linha não desenrolar ou dar nó." if mao_dominante.lower() == "canhota" else ""
        return f"""
        Você é uma engenheira têxtil matemática para bebês.
        - Categoria: {categoria}
        - Fase: {tamanho_alvo}
        - Tensão do Ponto: {tensao}
        
        REGRAS:
        1. Identifique as cores com um ÚNICO NOME EXATO. Sem barras (/), sem sinônimos e sem descrever a parte da peça (Ex: use "Branco" ao invés de "Branco Natural / Cru").
        2. Calcule a metragem e ajuste o consumo pela tensão '{tensao}'. Adicione 15% de margem (novelo de 150m).
        3. Determine o Tex ideal para bebês (fios leves e delicados) em 'tex_recomendado'.
        4. Identifique a variação de agulha e SEMPRE crave o tamanho MÉDIO exato.
        5. {aviso}
        """

    def _montar_prompt_pet(self, categoria: str, tamanho_alvo: str, mao_dominante: str, tensao: str) -> str:
        aviso = "ALERTA: A usuária é CANHOTA. Adicione na 'diretriz_inicial' cuidados para a linha não desenrolar ou dar nó." if mao_dominante.lower() == "canhota" else ""
        return f"""
        Você é uma engenheira têxtil matemática para animais.
        - Categoria: {categoria}
        - Porte: {tamanho_alvo}
        - Tensão do Ponto: {tensao}
        
        REGRAS:
        1. Identifique as cores cravando um ÚNICO TOM para cada fio. É terminantemente proibido usar barras (/) ou dar duas opções de nome. Não adicione a parte do corpo no nome da cor.
        2. Calcule a metragem e ajuste o consumo pela tensão '{tensao}'. Adicione 15% de margem (novelo de 150m).
        3. Determine o Tex ideal para pets e informe em 'tex_recomendado'.
        4. Identifique a variação de agulha e SEMPRE crave o tamanho MÉDIO exato.
        5. {aviso}
        """
    
    def _gerar_resposta_erro(self, detalhe: str) -> dict:
        return {
            "fios_necessarios": [],
            "total_novelos_peca": 0,
            "tamanho_agulha_recomendado": "Erro",
            "tex_recomendado": "Erro",
            "diretriz_inicial": f"Falha na comunicação. Detalhe: {detalhe}"
        }