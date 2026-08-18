import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from SRC.UTILS import load_model
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from scemas import Transaction
MODEL_VERSION = '1.0.0'
app =  FastAPI()

@app.post('/predict')
def predict_fraud(data : Transaction):
    model = load_model()

    input_df = pd.DataFrame({
        'amt' : data.amt,
        'gender' : data.gender,
        'city_pop' : data.city_pop,
        'unix_time' : data.unix_time,
        'hour' : data.hour,
        'merchant_rate': data.merchant_rate,
        'age' : data.age ,
        'distance_km' : data.distance_km,
        'category_rate' : data.category_rate
    }, index=[0])
    input_df['gender'] = input_df['gender'].map({'M': 1, 'F': 0})
    prediction = model.predict_proba(input_df)[0][1]
    Prediction = model.predict_proba(input_df)[0][0]
    propability = round(prediction*100, 2)
    if prediction > 0.2 :
        prediction = 'fraud_transaction. '
    else :
        prediction = 'normal_transaction. '
    return JSONResponse(status_code=200,content={'prediction is ': prediction, 'probability': propability})
@app.get('/health')
def health_check():
    return {
        'status' : 'ok',
        'model_version' : MODEL_VERSION
    }
