from minio import Minio
from app import app
import os


@app.route("/stackhero")
def stackhero():
    """
    Temporary S3 storage integration to make
    sure things are hooked up properly
    """
    endpoint = os.environ.get("STACKHERO_MINIO_HOST")
    if endpoint is None:
        return "Missing endpoint"
    endpoint = endpoint + ":443"
    client = Minio(
        endpoint=endpoint,
        secure=True,
        access_key=os.environ.get("STACKHERO_MINIO_ACCESS_KEY"),
        secret_key=os.environ.get("STACKHERO_MINIO_SECRET_KEY"),
        region="us-east-1",
    )
    found = client.bucket_exists("test")
    if not found:
        client.make_bucket("test")
    else:
        return "Bucket already exists"
    # Upload 'README.md' as object name
    # 'README.md' to bucket 'test'
    client.fput_object(
        "test",
        "README.md",
        "/home/bradcush/Documents/repos/csci-ga-2433-project/README.md",
    )
    return "Successful test"
