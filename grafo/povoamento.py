import mysql.connector
from mysql.connector import Error
from faker import Faker
from datetime import datetime, timedelta
import random

# Função para gerar datas aleatórias
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

# Função para conectar ao banco de dados
def connect():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="database_application"
        )
        if conn.is_connected():
            print('Conectado ao MySQL')
            return conn
    except Error as e:
        print(e)

# Função para gerar um usuario_id único
def generate_usuario_id(cursor):
    while True:
        usuario_id = random.randint(1, 3000)
        cursor.execute("SELECT usuario_id FROM Usuario WHERE usuario_id = %s", (usuario_id,))
        result = cursor.fetchone()
        if not result:
            return usuario_id

# Função para inserir dados nas tabelas
def insert_data(conn):
    fake = Faker('pt_BR')
    cursor = conn.cursor()

    # Inserindo dados na tabela Usuario
    for i in range(1, 3001):
        usuario_id = generate_usuario_id(cursor)
        nome = fake.name()
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=90)
        genero = random.choice(['Masculino', 'Feminino'])
        inicio_associacao = fake.date_between(start_date='-2y', end_date='today')
        termino_associacao = fake.date_between(start_date=inicio_associacao, end_date='today')
        plano_assinatura = random.choice(['Plano A', 'Plano B', 'Plano C'])
        info_pagamento = fake.credit_card_full()
        status_renovacao = random.choice(['Ativo', 'Inativo'])

        sql_usuario = "INSERT INTO Usuario (usuario_id, nome, data_nascimento, genero, inicio_associacao, termino_associacao, plano_assinatura, info_pagamento, status_renovacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_usuario, (usuario_id, nome, data_nascimento, genero, inicio_associacao, termino_associacao, plano_assinatura, info_pagamento, status_renovacao))
        conn.commit()

        print("\033[92mUsuario adicionado com sucesso ({}/{})\033[0m".format(i, 3000))

    # Inserindo dados na tabela UsoServico
    for _ in range(3000):
        usuario_id = random.randint(1, 3000)
        frequencia_uso = random.randint(1, 10)
        generos_favoritos = ', '.join(fake.words(nb=3))
        dispositivos_usados = ', '.join(fake.words(nb=3))
        metricas_engajamento = ', '.join(fake.words(nb=3))

        sql_uso_servico = "INSERT INTO UsoServico (usuario_id, frequencia_uso, generos_favoritos, dispositivos_usados, metricas_engajamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_uso_servico, (usuario_id, frequencia_uso, generos_favoritos, dispositivos_usados, metricas_engajamento))
        conn.commit()

        print("\033[92mUsoServico adicionado com sucesso ({}/{})\033[0m".format(_, 3000))

    # Inserindo dados na tabela SuporteCliente
    for _ in range(3000):
        suporte_id = _ + 1
        usuario_id = random.randint(1, 3000)
        interacoes_suporte = fake.text(max_nb_chars=200)

        sql_suporte_cliente = "INSERT INTO SuporteCliente (suporte_id, usuario_id, interacoes_suporte) VALUES (%s, %s, %s)"
        cursor.execute(sql_suporte_cliente, (suporte_id, usuario_id, interacoes_suporte))
        conn.commit()

        print("\033[92mSuporteCliente adicionado com sucesso ({}/{})\033[0m".format(_, 3000))

    cursor.close()

# Função principal
def main():
    conn = connect()
    if conn:
        insert_data(conn)
        conn.close()

if __name__ == '__main__':
    main()
