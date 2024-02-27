
# Text User Interface para a segunda entrega
# Nao permite a edição. Apenas a navegação dado
# que a edição é sibretudo trabalhosa


# Menu - Mostrar todos os autos e permite escolher o auto
# Ao escolher o auto mostra a lista de termos de entrega
# Para cada termo de entrega mostra a lista de materiais apreendidos

# Tem uma funcao de inicializacao que gera 50 autos, cada um com 2 termos de entrega,
# cada qual com 50 materiais

from ama_dao import AutoDAO, TermoEntregaDAO
from ama_db import AmaDB


class AmaTUI:
    def __init__(self):
        self.amaConnection = AmaDB()
        self.amaConnection.connect()
        self.connection = self.amaConnection.connection

    def entryPoint(self):
        ans = 'X'
        while 1==1:
            self.showMenuAutos()
            ans = input('Escolha um auto (F para sair): ')
            if ans == 'F':
                break
            while ans != 'F':
                self.showMenuTermoEntrega(ans)
                ans = input('Escolha um termo entrega (F para sair): ')


    def showMenuAutos(self):
        """Menu que mostra todos os autos"""
        print("---- Autos ----")
        autoDAO = AutoDAO(self.amaConnection.connection)
        autos = autoDAO.readAll()
        numAutos = len(autos)
        for i in range(numAutos):
            print('   ' + str(autos[i]['id']) +
            ' - Processo: ' + str(autos[i]['num_processo']) +
            '/' + str(autos[i]['ano_processo']))

    def showMenuTermoEntrega(self, id_auto ):
        """Menu que mostra todos os termos de entrega de um auto"""
        print("---- Termos de Entrega ----")
        termoEntregaDAO = TermoEntregaDAO(self.amaConnection.connection)
        termosEntrega = termoEntregaDAO.readByAuto(id_auto)
        numTermosEntrega = len(termosEntrega)
        for i in range(numTermosEntrega):
            print('   ' + str(termosEntrega[i]['id']) +
            ' - TermoEntrega: ' + str(termosEntrega[i]['num_termo']))

amaTUI = AmaTUI()
amaTUI.entryPoint()