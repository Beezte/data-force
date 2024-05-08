from neo4j import GraphDatabase
from colorama import init, Fore, Style
init(autoreset=True)

class Neo4jCRUD:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def update_usuario(self, id, novo_status):
        query = (
            "MATCH (u:Usuario {id: $id}) "
            "SET u.status_renovacao = $status "
            "RETURN u.nome, u.status_renovacao"
        )
        params = {"id": id, "status": novo_status}
        print(Fore.MAGENTA + "\n+=============================+")
        print(Fore.LIGHTYELLOW_EX + "Executando consulta Cypher...")
        print(Fore.CYAN + "Query Cypher:", query)
        print(Fore.CYAN + "Parâmetros:", params)

        with self._driver.session() as session:
            result = session.run(query, **params)
            print(Fore.MAGENTA + "\n+---------------------------------+\n")
            print(Fore.YELLOW + Style.BRIGHT + "Resultado da consulta")
            if result.peek() is None:
                print(Fore.RED + "Nenhum nó encontrado para o ID especificado.")
            else:
                for record in result:
                    print(Fore.BLUE + "Nome do usuário:", record["u.nome"])
                    print(Fore.BLUE + "Novo status de renovação:", record["u.status_renovacao"])
            print(Fore.MAGENTA + "\n+---------------------------------+")


# Exemplo de uso
if __name__ == "__main__":
    uri = "neo4j+s://be4fe8d1.databases.neo4j.io"
    user = "neo4j"
    password = "r8__SdUDojPCd8t3AQlgn9nk7vqWQpy8IIC0FYf9HHA"
    neo4j_crud = Neo4jCRUD(uri, user, password)

    # para atualizar o status de um usuário pelo id
    neo4j_crud.update_usuario(3010, "Inativo")

    neo4j_crud.close()
