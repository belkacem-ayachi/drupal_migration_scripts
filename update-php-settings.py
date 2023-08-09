

def read_file_by_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []


def save_file_with_lines( new_file_path, lines):
    try:
        with open(new_file_path, 'w') as new_file:
            new_file.writelines(lines)
        print(f"File has been saved to: {new_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")



if __name__ == "__main__":
    file_path = "model_settings.php"  # Replace this with the path of the file you want to read
    lines = read_file_by_lines(file_path)

    azure_host = "drupal-d-mariadb-001.mariadb.database.azure.com"
    azure_user = "drupaladmin@drupal-d-mariadb-001.mariadb.database.azure.com"
    azure_password = "UNescwa2020@@"
    azure_database = "escwabeta"
    application_DNS = "beta-dev.unescwa"

    updated_config = f"$databases['default']['default'] = array (\
    'database' => '{azure_database}',\
    'username' => '{azure_user}',\
    'password' => '{azure_password}',\
    'prefix' => '',\
    'host' => '{azure_host}',\
    'port' => '3306',\
    'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',\
    'driver' => 'mysql',\
    'options' => array( PDO::MYSQL_ATTR_SSL_CA => './DigiCertGlobalRootG2.crt.pem')\
    );\
    $settings['trusted_host_patterns'] = array(\
        '^{application_DNS}\.org$',\
        '^.+\{application_DNS}\.org$',\
        );\
    "

    lines[800] = updated_config
    del lines[801:815]
    save_file_with_lines( new_file_path='./settings_updates.php', lines= lines)


