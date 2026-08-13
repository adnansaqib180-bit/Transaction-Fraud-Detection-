import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from pydantic import BaseModel , field_validator, computed_field
from datetime import datetime, date
from dict import merchant_rate, category_rate
from SRC.UTILS import haversine_np

class Transaction(BaseModel):
    trans_date_trans_time : datetime 
    merchant : str 
    category : str
    amt : int
    gender : str
    lat : float
    long : float
    city_pop : int
    dob : date
    merch_lat: float
    merch_long : float

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
