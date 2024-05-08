from neo4j import GraphDatabase
from colorama import init, Fore, Style
init(autoreset=True)

class Neo4jCRUD:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def delete_usuario(self, usuario_id):
        confirmacao = input(Fore.RED + Style.BRIGHT + "\n\nTem certeza que deseja excluir o usuário? (s/n): ")
        if confirmacao.lower() == "s":
            with self._driver.session() as session:
                session.run("MATCH (u:Usuario {id: $usuario_id}) DELETE u", usuario_id=usuario_id)
            print(Fore.GREEN + Style.BRIGHT + "\nUsuário excluído com sucesso!\n")
        else:
            print(Fore.GREEN + Style.BRIGHT + "Exclusão cancelada.")

# Exemplo de uso
if __name__ == "__main__":
    uri = "neo4j+s://be4fe8d1.databases.neo4j.io"
    user = "neo4j"
    password = "r8__SdUDojPCd8t3AQlgn9nk7vqWQpy8IIC0FYf9HHA"
    neo4j_crud = Neo4jCRUD(uri, user, password)


    neo4j_crud.delete_usuario(3011)

    neo4j_crud.close()
