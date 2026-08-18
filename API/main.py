import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from SRC.UTILS import load_model
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from scemas import Transaction
from contextlib import asynccontextmanager
import psycopg2


MODEL_VERSION = '1.0.0'
model_info ={}

DB_SETTINGS = {
    'host' : 'ep-round-dawn-ayns25o6-pooler.c-5.us-east-2.aws.neon.tech',
    'database' : 'neondb',
    'user' : 'neondb_owner',
    'password' : 'npg_IVf95SoGQepE',
    'port' : 5432,
    'sslmode' : 'require'
}


@asynccontextmanager 
async def lifespan(app: FastAPI):
    model_info['model'] = load_model()
    yield
    model_info.clear()

app =  FastAPI(lifespan=lifespan)

@app.post('/predict')
def predict_fraud(data : Transaction):
    model = model_info.get('model')
    if not model :
        raise HTTPException(status_code=500,detail='model not loaded successfully ')

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

    input_df['gender'] = input_df['gender'].map({'M': 1, 'F': 0})
    prediction = model.predict_proba(input_df)[0][1]

    Prediction = model.predict_proba(input_df)[0][0]

    propability = round(prediction*100, 2)

    if prediction > 0.2 :
        prediction = 'fraud_transaction. '

    else :
        prediction = 'normal_transaction. '
    try:
        connection = psycopg2.connect(**DB_SETTINGS)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO predictions (amt, gender, city_pop, unix_time, hour, merchant_rate, age, distance_km, category_rate, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (data.amt, data.gender, data.city_pop, data.unix_time, data.hour, data.merchant_rate, data.age, data.distance_km, data.category_rate, prediction ))
        connection.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        
    return JSONResponse(status_code=200,content={'prediction is ': prediction, 'probability': propability})

@app.get('/health')
def health_check():
    return {
        'status' : 'ok',
        'model_version' : MODEL_VERSION
    }
