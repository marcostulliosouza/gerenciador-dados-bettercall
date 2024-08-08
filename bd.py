import pymysql.cursors
from pymysql import MySQLError
class GerenciadorBancoDados:
    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8',
        }
        self.pagina_atual = 0
        self.resultados_por_pagina = 15

    def conectar(self):
        try:
            self.conexao = pymysql.connect(**self.config)
            self.cursor = self.conexao.cursor()
        except MySQLError as e:
            raise Exception(f'Erro ao conectar ao banco de dados: {e}')

    def desconectar(self):
        if hasattr(self, 'conexao') and self.conexao.open:
            self.conexao.close()

    def listar_tabelas(self):
        try:
            query = "SHOW TABLES"
            self.cursor.execute(query)
            tabelas = [row[0] for row in self.cursor.fetchall()]
            return tabelas
        except MySQLError as e:
            raise Exception(f'Erro ao listar as tabelas: {e}')

    def listar_colunas(self, tabela):
        try:
            query = f"SHOW COLUMNS FROM {tabela}"
            self.cursor.execute(query)
            colunas = [row[0] for row in self.cursor.fetchall()]
            return colunas
        except MySQLError as e:
            raise Exception(f'Erro ao listar colunas da tabela {tabela}: {e}')

    def listar_elementos(self, tabela, pagina, coluna_id, termo_pesquisa=None):
        offset = pagina * self.resultados_por_pagina
        try:
            if termo_pesquisa:
                query = f"SELECT * FROM {tabela} WHERE {coluna_id} LIKE %s ORDER BY {coluna_id} DESC LIMIT {self.resultados_por_pagina} OFFSET {offset}"
                self.cursor.execute(query, ('%' + termo_pesquisa + '%',))
            else:
                query = f"SELECT * FROM {tabela} ORDER BY {coluna_id} DESC LIMIT {self.resultados_por_pagina} OFFSET {offset}"
                self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            return resultados
        except MySQLError as e:
            raise Exception(f'Erro ao listar elementos da tabela {tabela}: {e}')

    def total_elementos(self, tabela):
        try:
            query = f"SELECT COUNT(*) FROM {tabela}"
            self.cursor.execute(query)
            total = self.cursor.fetchone()[0]
            return total
        except MySQLError as e:
            raise Exception(f'Erro ao contar elementos da tabela {tabela}: {e}')

    def adicionar_elemento(self, tabela, valores):
        try:
            colunas = self.listar_colunas(tabela)
            placeholders = ', '.join(['%s'] * len(colunas))
            query = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"
            self.cursor.execute(query, valores)
            self.conexao.commit()
        except MySQLError as e:
            self.conexao.rollback()
            raise Exception(f'Erro ao adicionar elemento na tabela {tabela}: {e}')

    def atualizar_elemento(self, tabela, id_coluna, id_valor, valores):
        try:
            colunas = self.listar_colunas(tabela)
            sets = ', '.join([f"{coluna}=%s" for coluna in colunas])
            query = f"UPDATE {tabela} SET {sets} WHERE {id_coluna}=%s"
            self.cursor.execute(query, valores + [id_valor])
            self.conexao.commit()
        except MySQLError as e:
            self.conexao.rollback()
            raise Exception(f'Erro ao atualizar elemento na tabea {tabela}: {e}')

    def apagar_elemento(self, tabela, id_coluna, id_valor):
        try:
            query = f"DELETE FROM {tabela} WHERE {id_coluna}=%s"
            self.cursor.execute(query, (id_valor,))
            self.conexao.commit()
        except MySQLError as e:
            raise Exception(f'Erro ao apagar elemento na tabela {tabela}: {e}')