import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from pydantic import BaseModel , field_validator, computed_field, Field
from typing import Annotated
from datetime import datetime, date
from dict import merchant_rate, category_rate
from SRC.UTILS import haversine_np

class Transaction(BaseModel):
    trans_date_trans_time :  Annotated[datetime, "Transaction date and time"] = Field(example="2021-01-01 12:00:00")
    merchant : Annotated[str, "Merchant name"] = Field(example="fraud_Abbott-Rogahn")
    category : Annotated[str, "Transaction category"] = Field(example="health_fitness")
    amt : Annotated[int, "Transaction amount"] = Field(example=765,gt=0)
    gender : Annotated[str, "Customer gender only M and F "] = Field(example="M",min_length=1,max_length=1)
    lat : Annotated[float, "Customer latitude"] = Field(example=40.7128,ge=-90,le=90)
    long : Annotated[float, "Customer longitude"] = Field(example=-74.0060,ge=-180,le=180)
    city_pop : Annotated[int, "City population"] = Field(example=8000000,ge=1)
    dob : Annotated[date, "Customer date of birth"] = Field(example="1990-01-01")
    merch_lat: Annotated[float, "Merchant latitude"] = Field(example=40.7128,ge=-90,le=90)
    merch_long : Annotated[float, "Merchant longitude"] = Field(example=-74.0060,ge=-90,le=90)


    @field_validator('gender')
    @classmethod
    def gender_validator(cls,value : str ):
        if value not in ['m','f','M','F']:
            raise ValueError('invalid gender ')
        return value.upper()
    @computed_field
    @property
    def unix_time(self) -> int:
        unix = self.trans_date_trans_time.timestamp()
        return int(unix)
    
    @computed_field
    @property
    def hour (self) -> int:
        hr = self.trans_date_trans_time.hour
        return int(hr)

    @field_validator('merchant',mode='before')
    @classmethod
    def merchant_validator(cls,value):
       valid_merchants = list(merchant_rate.keys())
       if value not in valid_merchants:
           raise ValueError('invalid merchant')
       return value
    @field_validator('category',mode='before')
    @classmethod
    def category_validator(cls,value):
        valid_categ = list(category_rate.keys())
        if value not in valid_categ:
            raise ValueError('invalid category')
        return value
    @computed_field
    @property
    def age(self) -> int:
       aage = (datetime.today() - self.dob).days // 365
       if aage > 120:
           raise ValueError('invalid age ')
       elif aage < 1:
           raise ValueError('inavlid age')
       return int(aage)

    @computed_field
    @property
    def distance_km(self) -> int:
        d = haversine_np(self.long,self.lat,self.merch_long,self.merch_lat)
        return int(d)

    @computed_field
    @property
    def category_rate(self) -> int:
        if self.category not in category_rate:
            raise ValueError('invalid category')
        return category_rate[self.category]
    @computed_field
    @property
    def merchant_rate(self) -> int:
        if self.category not in merchant_rate:
            raise ValueError('invalid merchant')
        return merchant_rate[self.merchant]

        

    
    #    Index(['amt', 'gender', 'city_pop', 'unix_time', 'is_fraud', 'hour',
    #    'merchant_rate', 'age', 'distance_km', 'category_rate'],
    #   dtype='str')
