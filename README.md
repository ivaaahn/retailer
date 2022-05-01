# Coursework
## Retailer

### *Подключение к базе данных:*
1. Создать роль
   + `create user user_name with encrypted password 'userpassword';`
2. Создать БД
   + `CREATE DATABASE dbname;`
3. Определить права
   + `grant all privileges on database sample_db to user_name;`
4. Накатить миграции
   + `alembic upgrade head`
