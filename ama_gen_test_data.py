
#
# Gera dados de teste para permitir ver que o TUI está a
# funcionar correctamente
#

from ama_db import AmaDB
from ama_dao import AutoDAO, MaterialDAO, TermoEntregaDAO, TipoMaterialDAO
from ama_model import Auto, Material, TermoEntrega, TipoMaterial


class GenTestData:
    def __init__(self):
        self.amaConnection = AmaDB()
        self.amaConnection.connect()
        self.connection = self.amaConnection.connection

    def clean(self):
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

    def generate(self):
        tipoMaterialDAO = TipoMaterialDAO(self.amaConnection.connection)
        tipoMaterial = TipoMaterial()
        tipoMaterial.codigo = 'ROL'
        tipoMaterial.descricao = 'ROLETA'
        tipoMaterialDAO.create(tipoMaterial)

        for i in range (10):
            autoDAO = AutoDAO(self.amaConnection.connection)
            auto = Auto()
            auto.num_processo = i
            auto.num_auto = i + 5
            if i == 1 or i == 3:
                auto.nuipc = 'XPTO'
            if i == 2 or i == 4:
                auto.contra_ordenacao = 'HELLO'
            auto.id = autoDAO.create(auto)

            for j in range (10):
                termoEntregaDAO = TermoEntregaDAO(self.amaConnection.connection)
                termoEntrega = TermoEntrega(auto.id)
                termoEntrega.id_auto = auto.id
                termoEntrega.num_termo = i + j
                termoEntrega.id = termoEntregaDAO.create(termoEntrega)

                for k in range (50):
                    materialDAO =  MaterialDAO(self.amaConnection.connection)
                    material = Material(termoEntrega.id, auto.id)
                    material.id_auto = auto.id
                    material.id_termo_entrada = termoEntrega.id
                    material.id_tipo_material = tipoMaterial.codigo
                    material.descricao = 'Um material'
                    materialDAO.create(material)

genTestData = GenTestData()
genTestData.clean()
genTestData.generate()