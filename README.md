# csci-ga-2433-project

Database Systems

## Setup

``` sh
# Create environment if needed
cd ~/venvs # Store in venvs
python -m venv csci-ga-2433-project
source ~/venvs/csci-ga-2433-project/bin/activate
deactivate # Deactivate from within environment
```

## Heroku

Running the application locally

``` sh
heroku local --port 5001
```

## PosgreSQL

Open a psql shell to the database

``` sh
heroku pg:psql
```

## Schemas

- `schema/circuit-blocks.png`
- `schema/circuit-blocks.sql`

## Insights

A model has been trained for predicting whether someone purchasing a warranty
for their product purchase will carry addition risk. We use this data to assess
new warranty sign-ups, charging $5 for those that carry no additional risk, and
charging $10 for those that are deemed risky.

### Training

The file used for training is `prediction/warranties-actual.csv` which is
programmatically generated data representative of the real world.

``` sh
cd prediction
python train-model.py
```

### Predicting

Prediction can be run on either `prediction/warranties-actual.csv` or
`prediction/warranties-random.csv`. Note that random data is included only for
a sanity check where prediction should be around 50% accurate. We've hardcoded
the training data as `warranties-actual.csv` for now which is predicted with
around 90% accuracy.

``` sh
cd prediction
python predict-risk.py
```
