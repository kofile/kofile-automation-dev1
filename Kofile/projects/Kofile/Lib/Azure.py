from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO

from projects.Kofile.Lib.test_parent import LibParent


class AzureBlobStorage(LibParent):

    def __init__(self, data):
        super(AzureBlobStorage, self).__init__()
        self.data = data
        self.azure_connect = self._access_to_azure_blob()

    def _access_to_azure_blob(self):
        """Connect to Azure Blob"""
        azure = self.data["env"].get("azure")
        if azure:
            blob_service = BlobServiceClient(f"https://{azure['account_name']}.blob.core.windows.net", azure["account_key"])
            return blob_service

    def get_blobs_in_container(self, container):
        return self.azure_connect.get_container_client(container)

    def get_blobs_list_in_container(self, container, name_starts_with):
        """Get list of files in specified container by file name prefix"""
        return self.get_blobs_in_container(container).list_blobs(name_starts_with)

    def check_blob_existence_in_container(self, file_name, container="wfcontent-69999-printfolder"):
        """Check existence of file in container"""
        file = self.azure_connect.get_blob_client(container, file_name)
        assert file.exists(), f"File '{file_name}' not found in Azure Blob container '{container}'"
        return file

    def get_all_files_in_folder(self, container, folder="/"):
        container = self.azure_connect.get_container_client(container)
        return container.walk_blobs(folder)

    def download_file(self, file_name, container="wfcontent-69999-printfolder"):
        file = self.azure_connect.get_blob_client(container, file_name)
        self._actions.step(f"FILENAME: {file.blob_name}")
        return BytesIO(file.download_blob().readall())

    def get_text_from_file(self, file_name, container="wfcontent-69999-printfolder", encoding="unicode_escape"):
        file = self.azure_connect.get_blob_client(container, file_name)
        self._actions.step(f"FILENAME: {file.blob_name}")
        return file.download_blob(encoding=encoding).readall()

    @staticmethod
    def save_blob(download_file_path, file_content):
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        with open(download_file_path, "wb") as file:
            file.write(file_content)

    def download_all_blobs_in_container(self, container, file_name, download_folder):
        my_blobs = self.get_blobs_list_in_container(container, file_name)
        for blob in my_blobs:
            rows = self.get_blobs_in_container(container).get_blob_client(blob).download_blob().readall()
            download_file_path = os.path.join(download_folder, blob.name)
            self.save_blob(download_file_path, rows)
