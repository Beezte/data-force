from neo4j import GraphDatabase
from colorama import init, Fore, Style
init(autoreset=True)

class Neo4jCRUD:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_max_user_id(self):
        with self._driver.session() as session:
            result = session.run("MATCH (u:Usuario) RETURN max(u.id) AS max_id")
            record = result.single()
            return record["max_id"] if record["max_id"] is not None else 0

    def create_usuario(self, nome, plano):
        max_id = self.get_max_user_id()
        novo_id = max_id + 1
        with self._driver.session() as session:
            session.run("CREATE (u:Usuario {id: $id, nome: $nome, status_renovacao: $plano})",
                        id=novo_id, nome=nome, plano=plano)
            print(Fore.MAGENTA + "\n+---------------------------------+")
            print(Fore.GREEN + Style.BRIGHT + f"✅ | Êxito")
            print(Fore.BLUE + Style.BRIGHT + "Usuário criado com as seguintes credenciais")
            print(Fore.BLUE + f"Nome: {nome}")
            print(Fore.BLUE + f"ID único: {novo_id}")
            print(Fore.BLUE + f"Com o plano: {plano}")
            print(Fore.MAGENTA + "+---------------------------------+\n")


if __name__ == "__main__":
    uri = "neo4j+s://be4fe8d1.databases.neo4j.io"
    user = "neo4j"
    password = "r8__SdUDojPCd8t3AQlgn9nk7vqWQpy8IIC0FYf9HHA"
    neo4j_crud = Neo4jCRUD(uri, user, password)

    # Criar um novo usuário
    neo4j_crud.create_usuario("Testeteste 4", "Inativo")

    neo4j_crud.close()