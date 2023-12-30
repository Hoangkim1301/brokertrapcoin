-- SQLite
drop table stocks

CREATE TABLE IF NOT EXISTS stocks (
    user_id INTEGER NOT NULL,
    symbol TEXT,
    shares INTEGER,
    price REAL,
    buy_date DATETIME ,
    name TEXT
);


--insert into stocks (user_id, symbol, shares, price, buy_date, name) values (1, 'AAPL', 10, 100.00, 123456789, 'Apple Inc.');
INSERT INTO stocks (user_id, symbol, shares, price, buy_date, name) VALUES 
(2, 'AAPL', 10, 100.00, '2020-10-27 22:30:10', 'Apple Inc.'),
(2, 'AAPL', 10, 100.00, '2021-10-27 22:30:10', 'Apple Inc.'),
(2, 'AAPL', 8, 100.00, '2021-10-27 22:30:10', 'Apple Inc.')

;
INSERT INTO stocks (user_id, symbol, shares, price, buy_date, name) VALUES 
(1, 'AMZN', 16, 100.00, '2020-10-27 22:30:10', 'Amazon Inc.'),
(1, 'AMZN', 1, 100.00, '2021-10-27 22:30:10', 'Amazon Inc.'),
(1, 'AMZN', -5, 100.00, '2021-10-27 22:30:10', 'Amazon Inc.');

SELECT DISTINCT symbol FROM stocks WHERE user_id = 1;


select * from stocks
select * from stocks where user_id = 1


SELECT SUM(shares) FROM stocks WHERE symbol = 'AAPL' AND user_id = 1