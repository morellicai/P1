import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    database = '',
    user = 'root',
    password = 'manager'
)

if conn.is_connected():
    db_info = conn.get_server_info()
    print("Conectado ao servidor MySQL versão", db_info)

    cursor = conn.cursor()
    cursor.execute("create database CRUD();")
    linha = cursor.fetchone()
    print("Conectado ao banco de dados ", linha)

if conn.is_connected():
    cursor.close()
    conn.close()
    print("Conexão ao MySQL foi encerrada")