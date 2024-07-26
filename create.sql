-- SQL script to bootstrap the DB:
--
-- Пользователи бота
CREATE TABLE IF NOT EXISTS users
                (
                tg_id INTEGER,
                name TEXT,
                age INTEGER
                );

