import boto3, os, time, json, sentry_sdk


log_group_name = '/aws/lambda/teste_goncalves'
log_stream_name = 'teste_chat_gpt'
region_name = 'us-east-1'

sentry_sdk.init(
    dsn=os.environ['DSN_SENTRY'],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    environment='CloudWatch',
    traces_sample_rate=1.0
)
# def put_log_event(log_group_name, log_stream_name, log_message):
def put_log_event(data, acao):
    # Cria uma instância do cliente do CloudWatch Logs
    client = boto3.client('logs', region_name=region_name)  # Substitua 'us-east-1' pela região desejada

    data = {
        'acao': acao,
        'pk': data.pk,
        'modelo': data.modelo,
        'marca': data.marca,
        'ano': data.ano,
    }
    log_data = json.dumps(data)

    # Cria um evento de log
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': log_data
            }
        ]
    )

    # Verifica se o registro foi bem-sucedido
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Log registrado com sucesso!")
    else:
        sentry_sdk.consts(response['ResponseMetadata'])
        print("Erro ao registrar o log.")
