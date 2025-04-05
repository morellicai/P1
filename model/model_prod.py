import mysql.connector
from database.database import connectar

def criar_database():
    conn = connectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE DATABASE cadastro_prod;
        """)
        conn.commit()
        print("Tabela Criada com Sucesso")
    except mysql.connector.Error as e:
        if hasattr(e, 'errno') and e.errno == 1007:
            print("database ja existente...")
        else:
            print(f"Error MySQL: {e}")
    finally:
        cursor.close()
        conn.close()