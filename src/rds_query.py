import json
import pymysql

endpoint = 'endpoint_da_instancia_rds'
username = 'seu_user'
password = 'sua_senha_forte'
database_name = 'nome_do_db'

connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)

def lambda_handler(event, context):
    page = int(event.get('page', 1))  # Obter o número da página dos parâmetros do evento
    page_size = 10  # Definir o tamanho da página

    start_index = (page - 1) * page_size  # Calcular o índice inicial para a página atual
    end_index = start_index + page_size  # Calcular o índice final para a página atual

    cursor = connection.cursor()
    cursor.execute('SELECT user.id, user.email, user.username, role.id AS role_id, role.name AS role_name FROM user JOIN user_roles on (user.id=user_roles.user_id) JOIN role on (role.id=user_roles.role_id) LIMIT %s, %s', (start_index, page_size))

    # Converter os resultados em uma lista de dicionários
    rows = [{'id': row[0], 'email': row[1], 'username': row[2], 'role_id': row[3], 'role_name': row[4]} for row in cursor.fetchall()]

    return {
        'statusCode': 200,
        'body': json.dumps(rows)
    }
