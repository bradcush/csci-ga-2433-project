from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import numpy as np
import pickle

# Load the exsting model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

data = pd.read_csv("./warranties-actual.csv")
data.head()

# Split into input/output
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Use 20% of the data for testing purposes
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Get predicticed outcomes ag:inst actual
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)
pred = pd.DataFrame(np.vstack((y_pred, y_test)), index=["Predicted", "Actual"])
pred.iloc[:, :20]

# Evaluate the model performance
accuracy = metrics.accuracy_score(y_test, y_pred)
precision = metrics.precision_score(y_test, y_pred)
recall = metrics.recall_score(y_test, y_pred)
f1 = metrics.f1_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")
