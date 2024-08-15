-- Начало транзакции
BEGIN;

-- Создание вспомогательной таблицы с базовыми именами и статусами из plans_shortname
CREATE TABLE IF NOT EXISTS shortname_base1 AS
SELECT name AS base_name, 
       status
FROM plans_shortname;

-- Создание индекса на вспомогательной таблице для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_base_name ON shortname_base1 (base_name);

-- Обновление статусов в plans_fullname на основе данных из shortname_base1
UPDATE plans_fullname fn
SET status = sb.status
FROM shortname_base1 sb
WHERE LEFT(fn.full_name, LENGTH(fn.full_name) - POSITION('.' IN REVERSE(fn.full_name))) = sb.base_name
  AND fn.status IS NULL;

-- Завершение транзакции
COMMIT;