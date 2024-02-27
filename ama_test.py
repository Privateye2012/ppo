

import unittest

from ama_dao import ArmazemDAO, AutoDAO, FabricanteDAO, MaterialDAO, TermoEntregaDAO, TipoMaterialDAO
from ama_db import AmaDB
from ama_model import Armazem, Auto, Fabricante, Material, TermoEntrega, TipoMaterial
from datetime import datetime

class TestAmaCRUD(unittest.TestCase):
    """ Unit tests to check if all the concrete DAOs do work """

    def __init__(self, methodName):
        super().__init__(methodName)
        self.amaConnection = AmaDB()
        self.amaConnection.connect()
        self.connection = self.amaConnection.connection

    def setUp(self):
        """ Situação inicial para todos os testes """
        self.clearDatabase()

    def tearDown(self):
        """ Deixa a base de dados devidamente limpa """

    def testAutoCRUD(self):
        """ Test the creation of an auto in the database """

        autoDAO = AutoDAO(self.amaConnection.connection)
        # Afirma que nada existe na tabela de Autos
        self.assertEqual(len(autoDAO.readAll()),0)

        # Insere um novo auto
        auto = Auto()
        auto.num_processo = 1
        auto.num_auto = 2
        newId = autoDAO + auto
        auto.id = newId

        # Le da BD por ID
        readAuto = autoDAO << newId
        self.assertEqual(readAuto[0]['id'], newId)
        self.assertEqual(readAuto[0]['num_processo'], auto.num_processo)
        self.assertEqual(readAuto[0]['num_auto'], auto.num_auto)
        self.assertEqual(readAuto[0]['ano_processo'],datetime.now().year)

        # Lê todos os autos existentes (só deve ser 1)
        numAutos = len(autoDAO.readAll())
        self.assertEqual(numAutos,1)

        # Altera um auto
        auto.num_processo = 3
        autoDAO += auto
        updatedAuto = autoDAO << auto.id
        self.assertEqual(updatedAuto[0]['num_processo'], 3)


        # Remove um auto
        autoDAO - newId
        numAutos = len(autoDAO.readAll())
        self.assertEqual(numAutos,0)

    def testTermoEntregaCRUD(self):
        """ Testa as operações CRUD sobre um termo de entrega """

        autoDAO = AutoDAO(self.amaConnection.connection)
        # Insere um novo auto (não podem existir termos de entrega sem auto)
        auto = Auto()
        auto.num_processo = 1
        auto.num_auto = 2
        newId = autoDAO + auto
        auto.id = newId

        # Insere um novo termo de entrega
        termoEntregaDAO = TermoEntregaDAO(self.amaConnection.connection)
        termoEntrega = TermoEntrega(auto.id)
        termoEntrega.id_auto = auto.id
        termoEntrega.num_termo = 5
        newId = termoEntregaDAO + termoEntrega
        termoEntrega.id = newId

        # Le da BD, um termo de entrega por ID
        readTermoEntrega = termoEntregaDAO << newId
        self.assertEqual(readTermoEntrega[0]['id'], newId)
        self.assertEqual(readTermoEntrega[0]['id_auto'], auto.id)
        self.assertEqual(readTermoEntrega[0]['num_termo'], termoEntrega.num_termo)

        # Lê todos os termos de entregas existentes (só deve ser 1)
        numTermosEntrega = len(termoEntregaDAO.readAll())
        self.assertEqual(numTermosEntrega,1)

        # Altera um termo de entrega
        termoEntrega.num_termo = 6
        termoEntregaDAO += termoEntrega
        updatedTermoEntrega = termoEntregaDAO << termoEntrega.id
        self.assertEqual(updatedTermoEntrega[0]['num_termo'], 6)

        # Remove um termo de entrega
        termoEntregaDAO - newId
        numTermosEntrega = len(termoEntregaDAO.readAll())
        self.assertEqual(numTermosEntrega,0)

        # Remove o auto inserido
        autoDAO - auto.id

    def testMaterialCRUD(self):
        """ Testa as operações CRUD sobre um material """

        # Insere um novo auto (não podem existir termos de entrega sem auto)
        autoDAO = AutoDAO(self.amaConnection.connection)
        auto = Auto()
        auto.num_processo = 1
        auto.num_auto = 2
        auto.id = autoDAO + auto

        # Insere um novo termo de entrega (para efeitos de teste)
        termoEntregaDAO = TermoEntregaDAO(self.amaConnection.connection)
        termoEntrega = TermoEntrega(auto.id)
        termoEntrega.id_auto = auto.id
        termoEntrega.num_termo = 5
        termoEntrega.id = termoEntregaDAO + termoEntrega

        # Criar um tipo de material
        tipoMaterialDAO = TipoMaterialDAO(self.amaConnection.connection)
        tipoMaterial = TipoMaterial()
        tipoMaterial.codigo = 'ROL'
        tipoMaterial.descricao = 'ROLETA'
        tipoMaterialDAO + tipoMaterial;

        # Insere um novo material
        materialDAO =  MaterialDAO(self.amaConnection.connection)
        material = Material(termoEntrega.id, auto.id)
        material.id_auto = auto.id
        material.id_termo_entrada = termoEntrega.id
        material.id_tipo_material = tipoMaterial.codigo
        material.descricao = 'Um material'
        newId = materialDAO + material
        material.id = newId

        # Le da BD, um termo de entrega por ID
        readMaterial = materialDAO << newId
        self.assertEqual(readMaterial[0]['id'], newId)
        self.assertEqual(readMaterial[0]['id_auto'], auto.id)
        self.assertEqual(readMaterial[0]['id_termo_entrada'], termoEntrega.id)
        # Termo de saida
        self.assertEqual(readMaterial[0]['id_tipo_material'], material.id_tipo_material)
        self.assertEqual(readMaterial[0]['descricao'], material.descricao)

        # Lê todos os termos de entregas existentes (só deve ser 1)
        numMateriais = len(materialDAO.readAll())
        self.assertEqual(numMateriais,1)

        # Altera um termo de entrega
        material.descricao = 'Outra descricao'
        materialDAO += material
        updatedMaterial = materialDAO << material.id
        self.assertEqual(updatedMaterial[0]['descricao'], 'Outra descricao')

        # Remove um termo de entrega
        materialDAO - newId
        numMateriais = len(materialDAO.readAll())
        self.assertEqual(numMateriais,0)

        # Remove o auto e termo de entrega inseridos como auxiliar
        termoEntregaDAO - termoEntrega.id
        autoDAO - auto.id
        tipoMaterialDAO - tipoMaterial.codigo

    def testTipoMaterialCRUD(self):
        """ Testa as operações CRUD sobre a tabela auxiliar de tipos de material """

        tipoMaterialDAO = TipoMaterialDAO(self.amaConnection.connection)
        self.assertEqual(len(tipoMaterialDAO.readAll()),0)

        # Insere um novo tipo de material
        tipoMaterial = TipoMaterial()
        tipoMaterial.codigo = 'CONS'
        tipoMaterial.descricao = 'CONSOLA'
        tipoMaterialDAO + tipoMaterial

        # Le da BD, o tipo de material, por ID
        readTipoMaterial = tipoMaterialDAO << tipoMaterial.codigo
        self.assertEqual(readTipoMaterial[0]['codigo'], tipoMaterial.codigo)
        self.assertEqual(readTipoMaterial[0]['descricao'], tipoMaterial.descricao)

        # Lê todos os tipos de material existentes (só deve ser 1)
        numTiposMaterial = len(tipoMaterialDAO.readAll())
        self.assertEqual(numTiposMaterial,1)

        # Altera um tipo de material
        tipoMaterial.descricao = 'Nintendo'
        tipoMaterialDAO += tipoMaterial
        updatedTipoMaterial = tipoMaterialDAO << tipoMaterial.codigo
        self.assertEqual(updatedTipoMaterial[0]['descricao'], 'Nintendo')

        # Remove um tipo de matial
        tipoMaterialDAO - tipoMaterial.codigo
        numTiposMaterial = len(tipoMaterialDAO.readAll())
        self.assertEqual(numTiposMaterial,0)

    def testFabricanteCRUD(self):
        """ Testa as operações CRUD sobre a tabela auxiliar de fabricantes """

        fabricanteDAO = FabricanteDAO(self.amaConnection.connection)
        self.assertEqual(len(fabricanteDAO.readAll()),0)

        # Insere um novo fabricante
        fabricante = Fabricante()
        fabricante.codigo = 'SONY'
        fabricante.descricao = 'Sony Inc'
        fabricanteDAO + fabricante

        # Le da BD, o fabricante, por ID
        readFabricante = fabricanteDAO << fabricante.codigo
        self.assertEqual(readFabricante[0]['codigo'], fabricante.codigo)
        self.assertEqual(readFabricante[0]['descricao'], fabricante.descricao)

        # Lê todos os fabricantes existentes (só deve ser 1)
        numTiposMaterial = len(fabricanteDAO.readAll())
        self.assertEqual(numTiposMaterial,1)

        # Altera um fabricante
        fabricante.descricao = 'Microsoft'
        fabricanteDAO += fabricante
        updatedFabricante = fabricanteDAO << fabricante.codigo
        self.assertEqual(updatedFabricante[0]['descricao'], 'Microsoft')

        # Remove um fabricante
        fabricanteDAO - fabricante.codigo
        numTiposMaterial = len(fabricanteDAO.readAll())
        self.assertEqual(numTiposMaterial,0)

    def testArmazemCRUD(self):
        """ Testa as operações CRUD sobre a tabela auxiliar de armazens """

        armazemDAO = ArmazemDAO(self.amaConnection.connection)
        self.assertEqual(len(armazemDAO.readAll()),0)

        # Insere um novo armazem
        armazem = Armazem()
        armazem.codigo = 'PSI'
        armazem.descricao = 'Povoa'
        armazemDAO + armazem

        # Le da BD, o armazem, por ID
        readArmazem = armazemDAO << armazem.codigo
        self.assertEqual(readArmazem[0]['codigo'], armazem.codigo)
        self.assertEqual(readArmazem[0]['descricao'], armazem.descricao)

        # Lê todos os armazens existentes (só deve ser 1)
        numTiposMaterial = len(armazemDAO.readAll())
        self.assertEqual(numTiposMaterial,1)

        # Altera um armazem
        armazem.descricao = 'Lisboa'
        armazemDAO += armazem
        updatedArmazem = armazemDAO << armazem.codigo
        self.assertEqual(updatedArmazem[0]['descricao'], 'Lisboa')

        # Remove um armazem
        armazemDAO - armazem.codigo
        numTiposMaterial = len(armazemDAO.readAll())
        self.assertEqual(numTiposMaterial,0)

    def clearDatabase(self):
        cur = self.connection.cursor()
        strSql = """
            DELETE FROM material;
            DELETE FROM termo_entrega;
            DELETE FROM auto;
            DELETE FROM tipo_material;
            DELETE FROM fabricante;
            DELETE FROM armazem;
        """
        cur.execute(strSql)
        cur.close()


if __name__ == '__main__':
    unittest.main()
