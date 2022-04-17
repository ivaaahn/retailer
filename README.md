#Coursework
## Retailer

### *Подключение к базе данных:*
1. Создать роль
   + `create user user_name with encrypted password 'userpassword';`
2. Создать БД
   + `CREATE DATABASE dbname;`
3. Определить права
   + `grant all privileges on database sample_db to user_name;`
4. Загрузить все изменения из ветки *dev*
5. Создать переменную окружения, находясь в корне проекта
   + `export PYTHONPATH=$PYTHONPATH:${PWD}/retailer`
6. Накатить миграции
   + `alembic upgrade head`
