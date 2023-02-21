
import pandas as pd
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date

def request_wapi(api_key,query):

    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response,i):

    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return fecha,hora,condicion,tempe,rain,prob_rain

def create_df(data):

    col = ['Fecha','Hora','Condicion','Temperatura','Lluvia','prob_lluvia']
    df = pd.DataFrame(data,columns=col)
    df = df.sort_values(by = 'Hora',ascending = True)

    df_rain = df[(df['Lluvia']==1) & (df['Hora']>6) & (df['Hora']< 22)]
    df_rain = df_rain[['Hora','Condicion']]
    df_rain.set_index('Hora', inplace = True)

    return df_rain

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df,query):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)
    
   """ if(df.empty):
        message = client.messages \
                            .create(
                                body='\nHello! \n\n\n Today '+ input_date +' in ' + query +' no rain is expected',
                                from_=PHONE_NUMBER,
                                to='+447568279452'
                            )
    else:
        message = client.messages \
                            .create(
                                body='\nHello! \n\n\n The weather forecast today '+ input_date +' in ' + query +' is : \n\n\n ' + str(df),
                                from_=PHONE_NUMBER,
                                to='+447568279452'
                            )"""
    if(df_rain. empty):
        message = client.messages \
                    .create(
                         body='\nHello! \n\n\n Today '+ df['Date'][0] +' in ' + query +' no rain is expected.',
                         from_='whatsapp:+14155238886',
                         to='whatsapp:+447568279452'
                    )
    else:
        message = client.messages \
                        .create(
                             body='\nHello! \n\n\n The weather forecast today '+ df['Date'][0] +' in ' + query +' is : \n\n\n ' + str(df_rain),
                             from_='whatsapp:+14155238886',
                             to='whatsapp:+447568279452'
                        )

    return message.sid
