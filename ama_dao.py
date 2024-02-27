#!/usr/bin/python
# -*- coding: latin-1 -*-

import psycopg2
from ama_model import Auto, TipoMaterial, TermoEntrega, Material, Fabricante, Armazem
from dao import Dao

#
# Armazem de Material Apreendido
# Implementação dos Data Access Objects para a persistência de cada
# objecto em base de dados
#
# Nota: no momento da implementação, é possível que a maioria da implementação
# da leitura da BD, de cada tipo de dados possa ser genérica e implementada
# na super class DAO
#

class AutoDAO(Dao,Auto):
    """
      Classe para efectuar a interacao com a base de dados especifica para
      um Auto relativo a máquinas de jogo ilegal
    """
    def __init__(self, connection):
      super().__init__(connection)
      self.table_name = "auto"

class TermoEntregaDAO(Dao,TermoEntrega):
    """
      Classe para efectuar a interacao com a base de dados especifica para
      um Termo de entrega relativo a máquinas de jogo ilegal
    """
    def __init__(self, connection):
      super().__init__(connection)
      self.table_name = "termo_entrega"

    def readByAuto(self, id_auto):
      cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      rows = self.readWhere(' id_auto = ' + str(id_auto))
      return rows

class MaterialDAO(Dao,Material):
    """
      Classe para efectuar a interacao com a base de dados especifica para
      um Material relativo a máquinas de jogo ilegal

      TODO : A funcionalidade concreta será implementada na fase seguinte
    """
    def __init__(self, connection):
      super().__init__(connection)
      self.table_name = "material"

class TipoMaterialDAO(Dao, TipoMaterial):
    """
      Classe para efectuar a interacao com a base de dados especifica para
      um Material relativo a máquinas de jogo ilegal
    """
    def __init__(self, connection):
      super().__init__(connection)
      self.table_name = "tipo_material"
      self.pkName = 'codigo'
class FabricanteDAO(Dao, Fabricante):
    """
      Classe para efectuar a interacao com a base de dados especifica para
      um Material relativo a máquinas de jogo ilegal
    """
    def __init__(self, connection):
      super().__init__(connection)
      self.table_name = "fabricante"
      self.pkName = 'codigo'

class ArmazemDAO(Dao, Armazem):
    """
      Classe para efectuar a interacao com a base de dados especifica para
      um Material relativo a máquinas de jogo ilegal
    """
    def __init__(self, connection):
      super().__init__(connection)
      self.table_name = "armazem"
      self.pkName = 'codigo'

class Autos:
    """
    Todos os autos existentes em base de dados
    """
    def __init__():
        this.autos = this.readAutos()

    def readAutos():
        """
        Lê todos os autos existentes na BD
        """
        this.autosDAO = AutoDAO()
        autos = autosDAO.list()
        #
        # Iterar nos autos
        # Para cada auto
        #   readTermoEntrega
        # Fim
        #
        return autos

    def readTermoEntrega(auto):
      """
      Lê os termos de entrega de um auto
      """
      # Inicializa DAO
      # list(auto)
      # return termosEntrega

    def readMateriais(auto,termoEntrega):
      """
      Lê os materiais entregues no ambito de um termo de entrega
      e auto
      """
      # Inicializa DAO
      # list(auto,termoEntrega)
      # return materiais

    def saveAutos(autos):
      """
      Salva na base de dados, toda a informação existente
      em this.autos
      """
      # Inicializa DAO
      # Para cada auto
      #   insere auto
      #   insere termos de entrega

    def saveTermosEntrega(auto, termosEntrega):
      """
      Salva os termos de entrega de um auto
      """

    def saveMateriais(termoEntrega, materiais):
      """
      Grava na base de dados os materiais de um termo de entrega
      """