
#
# Data Access Object genérico para ler/escrever os dados
# de Armazens de Material Apreendido de/para uma base de
# dados
#

import psycopg2
from psycopg2.extras import RealDictCursor

class Dao:
    """ Generic DAO - Implement the CRUD methods that will fit in most concrete DAO(s) """
    def __init__(self,connection):
        self.connection = connection
        self.pkName = 'id'

    def create(self, object):
        """ Insert a new ROW into the database """
        cur = self.connection.cursor()
        cur.execute(self.buildInsertStr(object))
        newId = cur.fetchone()[0]
        cur.close()
        return newId

    def __add__(self, object):
        """
        Redefine o operador + para permitir inserção na tabela com um operador
        Algo como: id = autoDao + auto (insere um auto na BD usando o AutoDAO )
        """
        return self.create(object)

    def readById(self, id):
        """ Read a database row by id (Primary Key) """
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(self.buildSelectByIdStr(id))
        row = cur.fetchall()
        cur.close()
        return row

    def __lshift__(self, id):
        """
        Redefine o operador << para permitir a leitura de dados sa tabela com um operador
        Algo como: auto = autoDao << id (insere um auto na BD usando o AutoDAO )
        """
        return self.readById(id)

    def readAll(self):
        """ Read all rows (and columns from the database """
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(self.buildSelectAllStr())
        values = cur.fetchall()
        cur.close()
        return values

    def readWhere(self, strWhere):
        """ Read rows from the database accoring to a where clause """
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(self.buildSelectWhereStr(strWhere))
        values = cur.fetchall()
        cur.close()
        return values

    def update(self, object):
        cur = self.connection.cursor()
        cur.execute(self.buildUpdateStr(object))
        cur.close()

    def __iadd__(self, object):
        """
        Redefine o operador += para permitir a alteração de dados na tabela com um operador
        Algo como: autoDao += id (insere um auto na BD usando o AutoDAO )
        """
        self.update(object)
        return self

    def deleteById(self, id):
        """ Delete a ROW from the database """
        cur = self.connection.cursor()
        cur.execute(self.buildDeleteByIdStr(id))
        cur.close()

    def __sub__(self, id):
        """
        Redefine o operador - para permitir remoção da tabela com um operador
        Algo como: id = autoDao - id (insere um auto na BD usando o AutoDAO )
        """
        return self.deleteById(id)

    def buildSelectByIdStr(self, id):
        """
        Build the string that select an element from the database
        """
        sqlStr = 'SELECT * FROM ' + self.table_name + ' WHERE ' + self.pkName + "='" + str(id) + "'"
        return sqlStr

    def buildSelectWhereStr(self, strWhere):
        """
        Build the string that select from the database by were clause
        """
        sqlStr = 'SELECT * FROM ' + self.table_name + ' WHERE ' + strWhere
        return sqlStr

    def buildSelectAllStr(self):
        """
        Build the string that select all elments from the database
        """
        sqlStr = 'SELECT * FROM ' + self.table_name
        return sqlStr

    def buildInsertStr(self, object):
        """
        Build the string that insert in the database
        """
        # TODO : Should raise an exception if no tabnle name set
        sqlStr = 'INSERT INTO ' + self.table_name + ' ( '
        valuesStr = '('
        idx = 0
        for attribute, value in object.__dict__.items():
            if value != None:
                if idx > 0:
                    sqlStr += ','
                    valuesStr += ','
                sqlStr += attribute
                valuesStr += "'" + str(value) + "'"
                idx += 1
        sqlStr += ') VALUES ' + valuesStr + ') RETURNING ' + self.pkName
        return sqlStr

    def buildUpdateStr(self, object):
        """
        Build the SQL string that Update a row in the database
        """
        sqlStr = 'UPDATE ' + self.table_name + ' SET '
        idx = 0
        for attribute, value in object.__dict__.items():
            if idx > 0:
                sqlStr += ','
            if value != None:
                sqlStr += attribute + ' = ' + "'" + str(value) + "'"
            else:
                sqlStr += attribute + '= NULL'
            idx += 1
        sqlStr += ' WHERE ' + self.pkName + "='" + str(getattr(object,self.pkName)) + "'"
        return sqlStr

    def buildDeleteByIdStr(self, id):
        """ Create the SQL string to delete from the database by ID """
        return self.buildDeleteStr(self.pkName + "='" + str(id)) + "'"

    def buildDeleteStr(self, strWhere):
        """ Create the SQL string that delete from the database """
        if strWhere == None:
            return 'DELETE FROM ' + self.table_name

        return 'DELETE FROM ' + self.table_name + ' WHERE ' + strWhere
