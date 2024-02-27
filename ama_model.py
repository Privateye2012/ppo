#!/usr/bin/python
# -*- coding: latin-1 -*-

from strenum import StrEnum
from datetime import datetime

#
# Sistema para gestão dos autos relativos a máquinas de jogo ilegal
#
# Modelo de classes que vão suportar os objectos com a informação que
# existe na base de dados.
#
# Nesta fase do projecto apenas estão definidas as classes, com as respectivas
# propriedades e as funções contêm comentários que vão depois permitir
# a sua implementação concreta
#

class TipoAuto(StrEnum):
    AUTO_NOTICIA_CRIME           = 'Auto-noticia crime'
    AUTO_APREENSAO               = 'Auto-apreensão'
    AUTO_NOTICIA_CO              = 'Auto-notícia C O'

class Auto(object):
    """
      Um auto é levantado quando é detectado
    """
    def __init__(self):
        self.id = None
        self.ano_processo = datetime.now().year
        self.num_processo = None
        self.nuipc = None
        self.contra_ordenacao = None
        self.num_auto = None
        self.tipo = TipoAuto.AUTO_NOTICIA_CRIME
        self.data = None
        self.data_recepcao_igc = None
        self.data_recepcao_armazem = None
        self.data_registo = None
    def teste():
        print("Teste Auto");

class TipoTermoEntrega(StrEnum):
    ENTRADA          = 'Entrada'
    ENTREGA_ARGUIDO  = 'Entrega Arguido'
    ENTREGA_ENTIDADE = 'Entrega Entidade'
    DESTRUICAO       = 'Destruição'

class TermoEntrega(object):
    """
    Termo de entrega de um material na instituição
    """
    def __init__(self, id_auto):
        self.id_auto = id_auto
        self.num_termo = None
        self.data_registo = None
        self.data_termo = None
        self.tipo_termo_entrega = TipoTermoEntrega.ENTRADA
        self.cod_entidade = None
        self.cod_meio_humano = None

class EstadoMaterial(StrEnum):
    DESTRUIDO         = 'Destruido'
    ENTREGUE_ARGUIDO  = 'Entregue Arguido'
    REVERTE_ENTIDADES = 'Reverte Entidades'
    ARMAZEM           = 'Armazem'

class ExameMaterial(StrEnum):
    EXAME_EFECTUADO = 'Exame Efectuado'
    EFECTUAR_EXAME  = 'Efectuar Exame'
    NAO_NECESSARIO  = 'Não é necessário'
    NAO_PREENCHIDO  = 'Não preenchido'

class TipoMaterial(object):
    """
    Tipologia de materiais para a sua caracterização
    concreta. Não é um enum pois pode ter algum dinamismo
    de informação, não se pretendendo assim ter de mudar
    o programa quando for necessário inserir algo
    """
    def __init__(self):
        self.codigo = None
        self.descricao = None

class Fabricante(object):
    """
    Fabricantes do material apreendido
    Dado o seu dinamismo (necessitar de se inserir novos)
    é implementado sob a forma de classe
    """
    def __init__(self):
        self.codigo = None
        self.descricao = None

class Armazem(object):
    """
    Armazem onde os materiais apreendido podem ser armazenados
    Como podem ser criados novos, foi implementado sob a forma de
    classe
    """
    def __init__(self):
        self.codigo = None
        self.descricao = None

class Material(object):
    """
    Materiais concretos apreendidos no ambito de um auto
    e descritos por um termo de entrega
    """
    def __init__(self, id_termo_entrada, id_auto):
        self.id_termo_entrada = id_termo_entrada
        self.id_termo_saida = None
        self.id_auto = id_auto
        self.estadoMaterial = EstadoMaterial.DESTRUIDO
        self.exameMaterial = ExameMaterial.EFECTUAR_EXAME
        self.id_tipo_material = None
        self.descricao = None
        self.quantidade = None
        self.fila = None
        self.lugar = None
        self.prateleira = None
        self.cor = None
        self.id_fabricante = None
        self.id_armazem = None

