#!/usr/bin/python
# -*- coding: latin-1 -*-

#
# Implementação de métodos de query, de acordo com as
# necessidades de pesquisa concretas, definidas pelos
# utilizadores.
#
# As query(s) concretas sobre a BD, em vez de apostar
# na conjunção de dados dos objectos (que pode ser
# feita sem problema), tornam o sistema mais versátil.
#

import psycopg2
from psycopg2.extras import RealDictCursor
import csv
import sys
import xlsxwriter

from ama_db import AmaDB

class Query:
    """ Query genérico/abstracto
        A ser usado por herditariedade por querys concretos
    """
    def __init__(self,connection):
        self.connection = connection
        self.result = None
        self.reportName = 'Report AMA'

    def executeQuery(self):
        """ Executa a query e deixa o resultdo numa lista """
        cur = self.connection.cursor()
        cur.execute(self.queryText)
        self.result = cur.fetchall()
        cur.close()

    def exportToCSV(self, fileName):
        """ Exporta os dados para um ficheiro CSV"""
        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file)
            for line in self.result:
                row = list(line)
                writer.writerow(row)

    def exportToXls(self, fileName):
        """ Exporta o resultado da query para Excel """
        workbook = xlsxwriter.Workbook(fileName)
        worksheet = workbook.add_worksheet(self.reportName)

        row = 0
        col = 0

        for line in self.result:
            rowAsList = list(line)
            for column in rowAsList:
                cell = str(column)
                if column == None:
                    cell = ''
                worksheet.write(row, col, cell)
                col += 1
                worksheet.write(row, col + 1, cell)
            col = 0
            row += 1
        workbook.close()

class QueryMaterial(Query):
    """
    Efectua uma pesquisa de materiais por nuipc e(ou)
    por numero de contra ordenacao
    """
    def __init__(self, connection):
        super().__init__(connection)
        self.reportName = 'Materiais'

    def queryByNumero(self, identificador):
        """ Efectua a pesquisa por identificador """
        self.queryText = "SELECT material.* " + \
            "FROM auto INNER JOIN material " + \
            " ON auto.id = material.id_auto " + \
            " WHERE nuipc LIKE '%" + identificador + "%' OR" + \
            " contra_ordenacao LIKE '%" + identificador +"%'"
        self.executeQuery()


amaConnection = AmaDB()
amaConnection.connect()
queryMaterial = QueryMaterial(amaConnection.connection)
queryMaterial.queryByNumero(sys.argv[1])
queryMaterial.exportToXls(sys.argv[2])



