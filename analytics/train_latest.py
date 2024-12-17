from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from minio.commonconfig import CopySource
from helpers import hash_time
from minio import Minio
import pandas as pd
import pickle
import os


REPOS_DIRECTORY = "/home/bradcush/Documents/repos"
ANALYTICS_DIRECTORY = f"{REPOS_DIRECTORY}/csci-ga-2433-project/analytics"
TEMP_CSV_FILEPATH = f"{ANALYTICS_DIRECTORY}/current.csv"
TEMP_PKL_FILEPATH = f"{ANALYTICS_DIRECTORY}/current.pkl"


# Download the latest external data
def download_external(client):
    client.fget_object(
        "analytics",
        # Current folder should always be the latest. For now it's considered
        # that we rename the file to current locally before uploading.
        "external/risk/current.csv",
        TEMP_CSV_FILEPATH,
    )


# Train a model from some data
def train_model(data):
    data.head()
    X_train, _, y_train, _ = train_test_split(
        data.iloc[:, :-1],
        data.iloc[:, -1],
        test_size=0.2,
    )
    model = LogisticRegression(solver="liblinear", max_iter=1000)
    model.fit(X_train, y_train)
    return model


# Archive the current file by moving it to archive and
# changing the filename to a hash of the current time
def archive_remote(client, filename):
    # Archive the file currently in current
    client.copy_object(
        "analytics",
        f"models/risk/archive/{filename}.pkl",
        CopySource("analytics", "models/risk/current.pkl"),
    )


# Persist the model locally and remotely
def upload_remote(client, model):
    # Save the model locally for now
    with open(TEMP_PKL_FILEPATH, "wb") as f:
        pickle.dump(model, f)
    # Upload the new file to current
    client.fput_object(
        "analytics",
        # Current folder should always be the latest. For now it's considered
        # that we rename the file to current locally before uploading.
        "models/risk/current.pkl",
        TEMP_PKL_FILEPATH,
    )


# Removes all temp files
def remove_tempfile():
    os.remove(TEMP_PKL_FILEPATH)
    os.remove(TEMP_CSV_FILEPATH)


# Download the most current external data from S3 and train the
# model. Then upload the trained model back for inference.
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
    download_external(client)
    data = pd.read_csv(TEMP_CSV_FILEPATH)
    model = train_model(data)
    filename = hash_time()
    archive_remote(client, filename)
    upload_remote(client, model)
    remove_tempfile()
    print("Finished")


run()
