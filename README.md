# python_chat

## Серверная часть

Сервер работает 2 режимах параллельно: публичный (порт 9090) и приватный (порт 9091). Доступ в приватный чат осуществляется по ID. ID клиентов хранятся в файле cliemts.txt. В файл можно добавлять и удалять клиентов при работающей программе.

`Start server`: python server.py [file with ID clients]


## Клиентская часть

`Start client`: python client.py [file with ID clients]




