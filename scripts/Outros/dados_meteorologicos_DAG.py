from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
from airflow.macros import ds_add

import os
from os.path import join

import pandas as pd


with DAG(
    "Dados_Meteorologicos",
    start_date=pendulum.datetime(2022, 12, 26, tz='UTC'),
    schedule_interval='0 0 * * 1',
    default_args={
            "retries": 0,
            "owner": "alura"
        },
        tags=["Estudo", "Alura"]
) as dag:
    
    file_path = '/home/eduardo/vscode/airflow/work/temp/alura_pipeline/semana_{{ data_interval_end.strftime("%Y-%m-%d") }}'
    def pasta():
        os.makedirs(file_path, exist_ok=True)
    
    t1 = PythonOperator(task_id = 'Criar_Pasta',
                        python_callable=pasta
                        )
    
    
    def coleta_dados(data_interval_end):
        key = 'BP9DCQQ9RUD6WK798W797XGBV'
        city = 'RioDeJaneiro'

        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
                    f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?key={key}&unitGroup=metric&include=days&contentType=csv')
        dados = pd.read_csv(URL)
        
        dados.to_csv(file_path + 'dados_brutos.csv')
        dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'dados_temperaturas.csv')
        dados[['datetime', 'description', 'icon']].to_csv(file_path + 'dados_condicionais.csv')
    
    t2 = PythonOperator(task_id='Captura_dos_Dados',
                        python_callable=coleta_dados,
                        op_kwargs={'data_interval_end': 'data_interval_end.strftime("%Y-%m-%d")'}
                        )


    t1 >> t2