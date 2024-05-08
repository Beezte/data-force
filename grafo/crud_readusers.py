from neo4j import GraphDatabase
from colorama import init, Fore, Style
init(autoreset=True)

class Neo4jCRUD:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()


    def read_usuarios(self):
        with self._driver.session() as session:
            result = session.run("MATCH (u:Usuario) RETURN u")
            return [record["u"] for record in result]


if __name__ == "__main__":
    uri = "neo4j+s://be4fe8d1.databases.neo4j.io"
    user = "neo4j"
    password = "r8__SdUDojPCd8t3AQlgn9nk7vqWQpy8IIC0FYf9HHA"
    neo4j_crud = Neo4jCRUD(uri, user, password)

    print(Fore.RED + "\n╔════════════════════════════════════════════════╗")
    print(Fore.RED + "║ " + Style.BRIGHT + Fore.MAGENTA + "                   Usuários                    " + Fore.RED + "║")
    print(Fore.RED + "╠════════════════════════════════════════════════╣")
    usuarios = neo4j_crud.read_usuarios()
    for usuario in usuarios:
        nome = usuario['nome']
        plano = usuario['status_renovacao']
        idusuario = usuario['id']
        total_length = 50
        espacos_em_branco = total_length - len(f"ID {idusuario}") - len(nome) - len(f" (Plano {plano}) ")
        print(f"{Fore.RESET}║ {Fore.CYAN}[ID {idusuario}] {nome} (plano {plano}){' ' * espacos_em_branco}{Fore.RESET}║")
    print(Fore.RED + "╚═════════════════════════════════════════════════════╝")

    neo4j_crud.close()