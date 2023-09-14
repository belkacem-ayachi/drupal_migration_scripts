from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

def transfer_files_to_azure_blob_storage(local_folder_path, storage_account_name, container_name):
    try:
        # Replace the following variables with your Azure Blob Storage connection string and the container name
        connection_string = "DefaultEndpointsProtocol=https;AccountName=drupalstoragev1;AccountKey=fWVfket0+ldSDI31pHFICYVPbb7ZUFHAdk226aIPQp42jlzgznVJgQ/mRAx7hUDx3/JT9KhpTfWJ+AStw7dK6w==;EndpointSuffix=core.windows.net"

        # Create a blob service client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create a container client if it doesn't exist
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()

        # Transfer each file to the Azure Blob Storage container
        for root, _, files in os.walk(local_folder_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)

                # Create a blob client for the file (use relative path as blob name to maintain the folder structure)
                blob_name = os.path.relpath(local_file_path, start=local_folder_path).replace(os.sep, '/')
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

                # Upload the file to the blob storage
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)

                print(f"File '{local_file_path}' has been transferred to Azure Blob Storage as '{blob_name}'.")

    except Exception as e:
        print("An error occurred:", e)

def main():
    # Example usage:
    default_local_folder = "files"
    storage_account = "drupalstoragev1"
    container = "escwa-corporate"

    local_folder_path = input(f"Enter the path to the folder to transfer (or press Enter to use '{default_local_folder}'): ")
    if not local_folder_path:
        local_folder_path = default_local_folder

    transfer_files_to_azure_blob_storage(local_folder_path, storage_account, container)

if __name__ == "__main__":
    main()
