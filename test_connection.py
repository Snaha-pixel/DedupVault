import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="backup_optimizer"
    )

    if connection.is_connected():
        print("Connected to MySQL successfully!")
        print("DedupVault database is ready.")

    connection.close()

except mysql.connector.Error as error:
    print("Database connection failed:", error)