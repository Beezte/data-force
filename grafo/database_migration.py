import mysql.connector
from py2neo import Graph, Node, Relationship

mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="database_application"
)

graph = Graph("neo4j+s://be4fe8d1.databases.neo4j.io", auth=("neo4j", "r8__SdUDojPCd8t3AQlgn9nk7vqWQpy8IIC0FYf9HHA"))

cursor = mysql_conn.cursor()
cursor.execute("SELECT * FROM Usuario")

for (usuario_id, nome, data_nascimento, genero, inicio_associacao, termino_associacao, plano_assinatura, info_pagamento, status_renovacao) in cursor:

    user_node = Node("Usuario", id=usuario_id, nome=nome, data_nascimento=str(data_nascimento), genero=genero,
                     inicio_associacao=str(inicio_associacao), termino_associacao=str(termino_associacao),
                     plano_assinatura=plano_assinatura, info_pagamento=info_pagamento,
                     status_renovacao=status_renovacao)
    graph.create(user_node)

cursor.execute("SELECT * FROM UsoServico")

for (usuario_id, frequencia_uso, generos_favoritos, dispositivos_usados, metricas_engajamento) in cursor:
    service_usage_node = Node("UsoServico", frequencia_uso=frequencia_uso, generos_favoritos=generos_favoritos,
                              dispositivos_usados=dispositivos_usados, metricas_engajamento=metricas_engajamento)
    user_node = graph.nodes.match("Usuario", id=usuario_id).first()
    if user_node:
        rel = Relationship(user_node, "USA", service_usage_node)
        graph.create(rel)

cursor.execute("SELECT * FROM SuporteCliente")

for (suporte_id, usuario_id, interacoes_suporte) in cursor:
    support_node = Node("SuporteCliente", id=suporte_id, interacoes_suporte=interacoes_suporte)
    user_node = graph.nodes.match("Usuario", id=usuario_id).first()
    if user_node:
        rel = Relationship(user_node, "RECEBE_SUPROE", support_node)
        graph.create(rel)

cursor.close()
mysql_conn.close()
