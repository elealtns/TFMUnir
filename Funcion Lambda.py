import boto3
import json
import csv
from datetime import date
from datetime import datetime

#Variables de ambiente
ENDPOINT_NAME = 'DEMO-linear-endpoint-202305251028'
#os.environt['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    try:
        print("Parámetros Recibidos Evento: " + json.dumps(event, indent=2))
        payload = format(event['queryStringParameters']['data'])
        print("Payload: " + payload)
        ENDPOINT_NAME = format(event['queryStringParameters']['endpoint'])
    
        print("End-Point: " + ENDPOINT_NAME)
        
        response = runtime.invoke_endpoint(EndpointName= ENDPOINT_NAME, ContentType='text/csv',Body=payload)
        print("Response: ")
        print(response)
        
        result = json.loads(response['Body'].read().decode())
        print("Result: ")
        print(result)
        
        pred = (result['predictions'][0]['score'])
        predicted_label = 'Good' if pred >= 0.85 else 'Bad'
        
        fecha = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
    
        # Crear un objeto JSON de respuesta
        respuesta = {
            'prediccion': predicted_label,
            'fecha': fecha
        }
        
        print(predicted_label)
        return {
                'statusCode': 200,
                'body': json.dumps(respuesta),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # Esto es para CORS, si es necesario
                }
        }
    
    except Exception as e:
        # Captura y maneja cualquier excepción que ocurra
        error_message = str(e)
        print("Error: " + error_message)

        # Devuelve una respuesta de error
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Esto es para CORS, si es necesario
            }
        }