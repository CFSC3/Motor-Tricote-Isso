from pydantic import BaseModel
from typing import List

class FioCor(BaseModel):
    nome_da_cor: str
    metragem_metros: int
    quantidade_novelos: int

class FichaTecnica(BaseModel):
    fios_necessarios: List[FioCor]
    total_novelos_peca: int
    tamanho_agulha_recomendado: str
    tex_recomendado: str  
    diretriz_inicial: str