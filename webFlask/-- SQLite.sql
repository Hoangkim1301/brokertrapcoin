-- SQLite
drop table stocks

CREATE TABLE IF NOT EXISTS stocks (
    user_id INTEGER NOT NULL,
    symbol TEXT,
    shares INTEGER,
    price REAL,
    buy_date DATETIME ,
    name TEXT,
    total_price REAL
);


--insert into stocks (user_id, symbol, shares, price, buy_date, name) values (1, 'AAPL', 10, 100.00, 123456789, 'Apple Inc.');
INSERT INTO stocks (user_id, symbol, shares, price, buy_date, name, total_price) VALUES 
(3, 'AAPL', 100, 100.00, '2020-10-27 22:30:10', 'Apple Inc.', 10000.0),
(3, 'AAPL', 10, 100.00, '2020-10-27 22:30:10', 'Apple Inc.', 1000.0),
(3, 'AAPL', 8, 100.00, '2021-10-27 22:30:10', 'Apple Inc.',80.0),
(3, 'AMZN', 16, 100.00, '2020-10-27 22:30:10', 'Amazon Inc.', 1600.0),
(3, 'AMZN', 1, 100.00, '2021-10-27 22:30:10', 'Amazon Inc.', 100.0),
(3, 'AMZN', 5, 100.00, '2021-10-27 22:30:10', 'Amazon Inc.', 500.0),
(3, 'AAPL', 10, 100.00, '2020-10-27 22:30:10', 'Apple Inc.', 1000.0),
(3, 'AAPL', 2, 100.00, '2020-10-27 22:30:10', 'Apple Inc.', 200.0),
(3, 'AMZN', 6, 100.00, '2021-10-27 22:30:10', 'Apple Inc.',600.0)

INSERT INTO stocks (user_id, symbol, shares, price, buy_date, name, total_price) VALUES 
(2, 'AAPL', 10, 100.00, '2020-10-27 22:30:10', 'Apple Inc.', 1000.0),
(2, 'AAPL', -2, 100.00, '2020-10-27 22:30:10', 'Apple Inc.', -200.0),
(1, 'AMZN', 6, 100.00, '2021-10-27 22:30:10', 'Apple Inc.',60.0)

INSERT INTO stocks (user_id, symbol, shares, price, buy_date, name, total_price) VALUES 
(1, 'AMZN', 16, 100.00, '2020-10-27 22:30:10', 'Amazon Inc.', 1600.0),
(1, 'AMZN', 1, 100.00, '2021-10-27 22:30:10', 'Amazon Inc.', 100.0),
(1, 'AMZN', -5, 100.00, '2021-10-27 22:30:10', 'Amazon Inc.', -500.0)



SELECT DISTINCT symbol FROM stocks WHERE user_id = 1;

DELETE FROM stocks WHERE user_id = 3;

select * from stocks
SELECT * from users
select * from stocks where user_id = 1



SELECT SUM(total_price) FROM stocks WHERE user_id = 1 and symbol = 'AAPL' 