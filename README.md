# TioCPS

## Quickstart

To quickly install all the needed dependencies run:
```
pip install -r reqs.txt
```

To start the application run [`main.py`](/api/main.py)


### Notas Rafael

- criar novo mecanismo para ler configurações (em vez de ler todas as vezes, ler apenas no inicio)


QUAIS É QUE ESTÃO FEITAS?
Tarefas

- ligação entre  python e a API do edificio para obter dados de dispositivos
- estudo e teste de execução de threads
- criar um modelo de um dispositivo para se monitorizar usando a API do edificio  (eg. Criar um dispositivo de consumo ou produção)
- efetuar uma rotina de monitorização parameterizada de dados (eg. 5 em 5 segundos)
- fazer gravação dos dados em mongo
- atribuir permissões e tokens aos dados em tempo real e aos dados armazenados
- criar uma API base para consulta de dados dos dispositivos monitorizados para pedir dados usando os tokens de permissões. Dependendo das permissões dos tokens, os resultados mostrados devem ser diferentes
- criar uma rota na API em python para a criação de tokens, identificando o tipo de permissão pretendida







- Fazer um request para pedir à API os dados, através da libraria requests fazer um pedido get para aceder aos dados do gecad para aceder aos dispositivos IOT.

criar um modelo de um dispositivo iot
- ir buscar os dados em json à api, passa-los para um objeto de uma classe, para conseguir manipular os dados. 
Criar uma thread para monitorizar um dispositivo
Testar com 50 ar condicionados para testar as threads, criar na classe main os acs e ligar atraves de uma thread uma classe à outra. Instanciar 50 objetos do tipo air conditioner para cada um correr numa thread diferente e para se ligar à classe thread air conditioner.
Rotina de monitorização fazer um loop com intervalos de 5 em 5 segundos para monitorizar o dispositivo iot de 5 em 5 segundos
Fazer a gravação em compass com o mongo.
