
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv, find_dotenv

def entry_data():
    """
    This function is used to upload the entry data in the Azure Blob storage container.
    The azure function does not change, it just uploads these two files for the recommendation.
    """
    # Connection
    load_dotenv(find_dotenv())
    azure_connect = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(azure_connect)
    
    # blob_client & upload - click_user_article_cat.csv
    blob_client_click = blob_service_client.get_blob_client(container="data", blob="click_user_article_cat.csv")
    with open("click_user_article_cat.csv", "rb") as f:
        blob_client_click.upload_blob(f, overwrite=True)
    
    # blob_client & upload - articles_embeddings.picke
    blob_client_art_emb = blob_service_client.get_blob_client(container="data", blob="articles_embeddings.pickle")
    with open("articles_embeddings.pickle", "rb") as f:
        blob_client_art_emb.upload_blob(f, overwrite=True)    
        
entry_data()
