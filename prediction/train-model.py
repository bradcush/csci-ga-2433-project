from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle

# Code for training this model was taken from Logistic Regression Explained
# https://medium.com/@zsalifu22/logistic-regression-explained-a-complete-guide-with-python-examples-e7dd27cb8820
# https://stackoverflow.com/questions/56107259/how-to-save-a-trained-model-by-scikit-learn
data = pd.read_csv("./warranties-random.csv")
data.head()

# Split into input/output
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Use 20% of the data for testing purposes
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
)

# Create and train the logistic regression model
model = LogisticRegression(solver="liblinear", max_iter=1000)
model.fit(X_train, y_train)

# Save the model for use later
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
