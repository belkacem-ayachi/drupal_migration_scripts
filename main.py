import subprocess , os

def run_python_script_interactively(script_path, project_name):
    try:
        
        # Run the specified script interactively
        subprocess.run(['python', script_path, project_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
    except FileNotFoundError:
        print(f"Script not found: {script_path}")

def create_docker_file(project_name,file_path='./Dockerfile'):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Check if the file has at least 5 lines
        if len(lines) < 5:
            print("File does not have 5 lines to replace.")
            return
        
        
       
        lines[0] = "FROM php:8.1-apache-bullseye \n"
        lines[1] = f"COPY ./ /var/www/html/{project_name}/  \n"
        lines[2] = f"COPY ./apache-config/ /etc/apache2/sites-available/  \n"
        lines[3] = f"RUN ln -s /etc/apache2/sites-available/{project_name}.conf /etc/apache2/sites-enabled/  \n"

        # Open the file in write mode and write the modified content
        with open(f"./{project_name}/Dockerfile", 'w') as file:
            file.writelines(lines)

        print("Replacement successful!")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    # getting the project name
    PROJECT_NAME = input("Enter the name of the project you want to migrate (as name in folder /var/www/html/X)")
    os.makedirs(f'./{PROJECT_NAME}', exist_ok=True)
    # Create the dockerfile
    create_docker_file(project_name= PROJECT_NAME)
    
    #Create the settings.php
    create_settings_php = "./update-php-settings.py"
    run_python_script_interactively(create_settings_php, project_name= PROJECT_NAME)
    
    

    # migrate database
    migrate_db = "./db-migrate.py"
    run_python_script_interactively(migrate_db, project_name= PROJECT_NAME)