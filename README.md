# Glossary API

## Функциональность

- Получение списка терминов
- Добавление нового термина
- Обновление существующего термина
- Удаление термина

### Локальный запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/MypyMypy/itmo_grpc_edu.git
   cd ./itmo_grpc_edu

   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Сгенерируйте Protobuf файлы:
   `python -m grpc_tools.protoc -I./app --python_out=./app --grpc_python_out=./app ./app/glossary.proto`

4. Запустите сервер - входная точка: `/app/main.py`

## Запуск в Docker

1. `docker compose up --build`

## Тестирование

1. Сервер будет доступен по адресу localhost:50051.

2. Для тестирования gRPC сервиса используйте grpcurl (рабочий способ установки на Linux можно найти в конце данного файла)

3. Примеры команд для тестирования:

- Получить список терминов: `grpcurl -plaintext localhost:50051 glossary.GlossaryService.GetTerms`
- Добавить новый термин: `grpcurl -plaintext -d '{"name": "Example", "description": "This is an example term."}' localhost:50051 glossary.GlossaryService.AddTerm`
- Обновить термин: `grpcurl -plaintext -d '{"current_name": "Example", "updated_term": {"name": "Updated Example", "description": "Updated description"}}' localhost:50051 glossary.GlossaryService.UpdateTerm`
- Удалить термин: `grpcurl -plaintext -d '{"name": "Updated Example"}' localhost:50051 glossary.GlossaryService.DeleteTerm`

**DEMO**
![DEMO](https://github.com/MypyMypy/itmo_grpc_edu/blob/main/demo.png)

### Установка grpcurl на Linux

1. `wget https://github.com/fullstorydev/grpcurl/releases/download/v1.8.0/grpcurl_1.8.0_linux_x86_64.tar.gz`
2. `tar -xzvf grpcurl_1.8.0_linux_x86_64.tar.gz`
3. `sudo mv grpcurl /usr/local/bin/`
