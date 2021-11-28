from google.oauth2 import service_account
from google.cloud import storage

AUTH_PATH = 'sa.json'
AUTH_SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

credentials = service_account.Credentials.from_service_account_file(
    AUTH_PATH,
    scopes=AUTH_SCOPES,
)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    client = storage.Client(credentials=credentials, project='cnft-loots')
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.metadata = {
        "Cache-Control" : 'no-store'
    }
    blob.patch()

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))