import mysql.connector
import pymysql
import os
import subprocess
import time
import sys
def export_remote_mysql_database(remote_host, remote_user, remote_password, remote_database, output_dir):
    """
    Exports a full MySQL database from a remote server using mysqldump.

    Args:
        remote_host (str): Remote MySQL host.
        remote_user (str): Remote MySQL user.
        remote_password (str): Remote MySQL password for the given user.
        remote_database (str): Name of the remote database to be exported.
        output_dir (str): Directory where the export file will be saved.

    Returns:
        str: The filename of the exported backup file.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the export filename based on the current timestamp
    export_filename = f"{remote_database}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    export_path = os.path.join(output_dir, export_filename)

    print(f"Starting database export to: {export_path}")

    # Construct the mysqldump command for remote export
    command = f"mysqldump --host={remote_host} --user={remote_user} --password={remote_password} --default-character-set=utf8mb4 -N --routines --skip-triggers  {remote_database} > {export_path}"

    try:
        # Execute the mysqldump command for remote export
        subprocess.run(command, shell=True, check=True)
        print(f"Database '{remote_database}' exported successfully. Export file: {export_path}")
        return export_path
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while exporting the remote database: {e}")
        return None

def import_to_azure_mariadb(azure_host, azure_user, azure_password, azure_database, import_file, connection):
    """
    Imports a MySQL database backup file to Azure MariaDB.

    Args:
        azure_host (str): Azure MariaDB host.
        azure_user (str): Azure MariaDB user.
        azure_password (str): Azure MariaDB password for the given user.
        azure_database (str): Name of the database to import the backup into.
        import_file (str): Path to the MySQL database backup file.

    Returns:
        bool: True if the import was successful, False otherwise.
    """
    # Construct the mysql command for importing the backup into Azure MariaDB
    command = f"mysql --host={azure_host} --user={azure_user} --password={azure_password} --ssl-mode=VERIFY_CA --ssl-ca=.\DigiCertGlobalRootG2.crt.pem {azure_database} < {import_file}"
    # command = f"'mysql --host={azure_host} --user={azure_user} --password={azure_password} --default-character-set=utf8mb4 -N --routines --skip-triggers {azure_database}  < {import_file}"
    try:
        # Check if the database exists on the cloud DB
        db_exists = mysql_database_exists(connection = connection,database_name = azure_database)
        if db_exists:
            # Execute the mysql command to import the backup into Azure MariaDB
            subprocess.run(command, shell=True, check=True)
            print(f"Backup successfully imported into '{azure_database}' in Azure MariaDB.")
            return True
        else:
            create_mysql_database(connection = connection,database_name = azure_database)
            subprocess.run(command, shell=True, check=True)
            print(f"Backup successfully imported into '{azure_database}' in Azure MariaDB.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while importing the backup: {e}")
        return False

# Function to check if a database exists in MySQL
def mysql_database_exists(connection, database_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = [row[0] for row in cursor]
            return database_name in databases
    except mysql.connector.Error as err:
        print(f"Error checking if database exists: {err}")
        return False

# Function to create a database in MySQL
def create_mysql_database(connection, database_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' created successfully!")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# Function to connect to the source MySQL database
def connect_to_mysql(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            # database=database
        )
        print("Connected to MySQL successfully!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Function to connect to the destination MariaDB database on Azure
def connect_to_mariadb_azure(host, user, password, database):
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            # database=database
        )
        print("Connected to MariaDB on Azure successfully!")
        return conn
    except pymysql.Error as err:
        print(f"Error connecting to MariaDB on Azure: {err}")
        return None


# Example usage
if __name__ == "__main__":
    # Replace these with your remote MySQL credentials
    project_name = sys.argv[1] 
    project_name = project_name if project_name else ''

    remote_mysql_database = input("Please enter the name of the remote MySQL database: ")

    remote_mysql_host = "10.30.42.24"
    remote_mysql_user = "root"
    remote_mysql_password = ""
    remote_mysql_database = remote_mysql_database if remote_mysql_database!="" or remote_mysql_database!= None else 'files'

    export_directory = f".{project_name}/db_exports/"

    # Replace these with your Azure MariaDB credentials
    azure_host = "drupal-d-mariadb-001.mariadb.database.azure.com"
    azure_user = "drupaladmin@drupal-d-mariadb-001.mariadb.database.azure.com"
    azure_password = "UNescwa2020@@"
    azure_database = remote_mysql_database

    # Initializing the connections 
    remote_db = connect_to_mysql(host = remote_mysql_host, user = remote_mysql_user, password = remote_mysql_password, database = remote_mysql_database )
    cloud_db = connect_to_mariadb_azure(host = azure_host, user = azure_user, password = azure_password, database = azure_database)

    # Exporting the on prem's DB
    db_path = export_remote_mysql_database(remote_mysql_host, remote_mysql_user, remote_mysql_password, remote_mysql_database, export_directory)

    # Importing the database into mariaDb
    import_to_azure_mariadb(azure_host = azure_host, azure_user = azure_user, azure_password = azure_password, azure_database = azure_database,connection = cloud_db, import_file = db_path)


    # Close connections
    remote_db.close()
    cloud_db.close()
