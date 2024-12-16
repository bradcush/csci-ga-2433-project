from minio import Minio
from minio.commonconfig import CopySource
import hashlib
import time
import shutil
import os

REPOS_DIRECTORY = "/home/bradcush/Documents/repos"
ANALYTICS_DIRECTORY = f"{REPOS_DIRECTORY}/csci-ga-2433-project/analytics"


# Create time-based hash for now but
# better could be to hash the contents
def hash_time():
    now = str(time.time()).encode()
    m = hashlib.sha1()
    m.update(now)
    return m.hexdigest()


# Archive the current file by moving it to archive and
# changing the filename to a hash of the current time
def archive_remote(client, filename):
    # Archive the file currently in current
    client.copy_object(
        "analytics",
        f"external/risk/archive/{filename}.csv",
        CopySource("analytics", "external/risk/current.csv"),
    )


# Overwrite the new current file on remote
def upload_remote(client):
    # Upload the new file to current
    client.fput_object(
        "analytics",
        # Current folder should always be the latest. For now it's considered
        # that we rename the file to current locally before uploading.
        "external/risk/current.csv",
        f"{ANALYTICS_DIRECTORY}/current.csv",
    )


# Archives then removes the original file
def archive_local(filename):
    current_filepath = f"{ANALYTICS_DIRECTORY}/current.csv"
    archive_filepath = f"{ANALYTICS_DIRECTORY}/archive/{filename}.csv"
    shutil.copyfile(current_filepath, archive_filepath)
    os.remove(current_filepath)


# Upload externally fetched risk data from to bucket
# in S3 and archive any file that's already there
def run():
    # Make sure to set API keys for environment
    # if you want to run this script locally
    endpoint = os.environ.get("STACKHERO_MINIO_HOST")
    if endpoint is None:
        print("Missing endpoint")
        return
    endpoint = endpoint + ":443"
    client = Minio(
        endpoint=endpoint,
        secure=True,
        access_key=os.environ.get("STACKHERO_MINIO_ACCESS_KEY"),
        secret_key=os.environ.get("STACKHERO_MINIO_SECRET_KEY"),
    )
    found = client.bucket_exists("analytics")
    if not found:
        client.make_bucket("analytics")
    filename = hash_time()
    archive_remote(client, filename)
    upload_remote(client)
    archive_local(filename)
    print("Finished")


run()
