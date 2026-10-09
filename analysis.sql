-- ============================================================
-- Stock Market Analysis Project
-- Database: stocks.db (SQLite)
-- Author: [Your Name]
-- Date: 2026-10-08
-- ============================================================

-- ============================================================
-- TASK 1: How much history do we have?
-- ============================================================
SELECT COUNT(*) AS trading_days,
       MIN(date) AS first_day,
       MAX(date) AS last_day
FROM bajaj_auto;

889	2015-01-01	2018-07-31


-- ============================================================
-- TASK 2: Eicher's five best closes
-- ============================================================
SELECT date, close_price
FROM eicher_motors
ORDER BY close_price DESC
LIMIT 5;

2017-09-07	32786.4
2017-09-18	32763.85
2017-09-08	32628.7
2017-09-12	32582.3
2017-09-11	32466.75

-- ============================================================
-- TASK 3: TCS year-by-year average
-- ============================================================
SELECT strftime('%Y', date) AS year,
       ROUND(AVG(close_price), 2) AS avg_close
FROM tcs
GROUP BY strftime('%Y', date)
ORDER BY year;

2015	2537.39
2016	2419.0
2017	2475.36
2018	2729.12


-- ============================================================
-- TASK 4: Find the holes (NULL deliverable_qty)
-- ============================================================
SELECT 'bajaj_auto' AS stock, date FROM bajaj_auto WHERE deliverable_qty IS NULL
UNION ALL SELECT 'eicher_motors', date FROM eicher_motors WHERE deliverable_qty IS NULL
UNION ALL SELECT 'hero_motocorp', date FROM hero_motocorp WHERE deliverable_qty IS NULL
UNION ALL SELECT 'infosys',       date FROM infosys       WHERE deliverable_qty IS NULL
UNION ALL SELECT 'tcs',           date FROM tcs           WHERE deliverable_qty IS NULL
UNION ALL SELECT 'tvs_motors',    date FROM tvs_motors    WHERE deliverable_qty IS NULL;

bajaj_auto	2017-08-31
eicher_motors	2015-12-09
hero_motocorp	2015-12-09
infosys	2017-08-31
tcs	2015-12-09
tvs_motors	2015-12-09

-- ============================================================
-- TASK 5: Moving averages for Bajaj Auto
-- ============================================================
DROP TABLE IF EXISTS bajaj1;
CREATE TABLE bajaj1 AS
SELECT date, close_price,
       CASE WHEN ROW_NUMBER() OVER (ORDER BY date) >= 20
            THEN ROUND(AVG(close_price) OVER (
                 ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW), 2)
       END AS ma20,
       CASE WHEN ROW_NUMBER() OVER (ORDER BY date) >= 50
            THEN ROUND(AVG(close_price) OVER (
                 ORDER BY date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW), 2)
       END AS ma50
FROM bajaj_auto;
-- Checkpoints: first ma20 = 2015-01-29 (2415.53)
--              first ma50 = 2015-03-13 (2283.80)
--              last ma20 = 2018-07-31 (2918.51)

2015-01-01	2454.1	1	2454.1
2015-01-02	2453.5	2	2453.8
2015-01-05	2460.15	3	2455.92
2015-01-06	2440.35	4	2452.03
2015-01-07	2447.2	5	2451.06
2015-01-08	2450.05	6	2450.89
2015-01-09	2381.5	7	2440.98
2015-01-12	2333.25	8	2427.51
2015-01-13	2326.25	9	2416.26
2015-01-14	2363.65	10	2411.0
2015-01-15	2417.95	11	2411.63
2015-01-16	2420.05	12	2412.33
2015-01-19	2411.3	13	2412.25
2015-01-20	2411.05	14	2412.17
2015-01-21	2442.0	15	2414.16
2015-01-22	2438.9	16	2415.7
2015-01-23	2442.2	17	2417.26
2015-01-27	2417.55	18	2417.28
2015-01-28	2396.9	19	2416.21
2015-01-29	2402.7	20	2415.53
2015-01-30	2389.35	21	2412.29
2015-02-02	2347.8	22	2407.01
2015-02-03	2260.1	23	2397.01
2015-02-04	2247.55	24	2387.37
2015-02-05	2243.05	25	2377.16


-- ============================================================
-- TASK 6: Master table (all 6 stocks joined on date)
-- ============================================================
DROP TABLE IF EXISTS master_table;
CREATE TABLE master_table AS
SELECT b.date,
       b.close_price AS bajaj,
       t.close_price AS tcs,
       v.close_price AS tvs,
       i.close_price AS infosys,
       e.close_price AS eicher,
       h.close_price AS hero
FROM bajaj_auto    b
JOIN tcs           t ON t.date = b.date
JOIN tvs_motors    v ON v.date = b.date
JOIN infosys       i ON i.date = b.date
JOIN eicher_motors e ON e.date = b.date
JOIN hero_motocorp h ON h.date = b.date;
-- Checkpoint: 889 rows, no NULLs, 2018-07-31 row matches

2018-07-31	2918.51


-- ============================================================
-- TASK 7: Golden cross signals for Bajaj Auto
-- ============================================================
DROP TABLE IF EXISTS bajaj2;
CREATE TABLE bajaj2 AS
WITH t AS (
  SELECT date, close_price, ma20, ma50,
         LAG(ma20) OVER (ORDER BY date) AS prev_ma20,
         LAG(ma50) OVER (ORDER BY date) AS prev_ma50
  FROM bajaj1
)
SELECT date, close_price,
  CASE
    WHEN ma20 IS NULL OR ma50 IS NULL
      OR prev_ma20 IS NULL OR prev_ma50 IS NULL THEN 'Hold'
    WHEN prev_ma20 <= prev_ma50 AND ma20 > ma50 THEN 'Buy'
    WHEN prev_ma20 >= prev_ma50 AND ma20 < ma50 THEN 'Sell'
    ELSE 'Hold'
  END AS signal
FROM t;

2018-07-31	2700.7	1941.25	517.45	1365.0	27820.95	3293.8


-- ============================================================
-- TASK 8: Signal counts
-- ============================================================
SELECT signal, COUNT(*) AS days FROM bajaj2 GROUP BY signal ORDER BY signal;

Buy	12
Hold	866
Sell	11

-- ============================================================
-- TASK 9: Spot-check specific dates
-- ============================================================
SELECT signal FROM bajaj2 WHERE date = '2015-05-18';  -- Buy
SELECT signal FROM bajaj2 WHERE date = '2016-01-04';  -- Hold
SELECT signal FROM bajaj2 WHERE date = '2018-06-21';  -- final check for the function

Buy
Hold

-- ============================================================
-- TASK 10: All 6 stocks in one query with PARTITION BY
-- ============================================================
WITH prices AS (
  SELECT 'Bajaj Auto'    AS stock, date, close_price FROM bajaj_auto
  UNION ALL SELECT 'Eicher Motors', date, close_price FROM eicher_motors
  UNION ALL SELECT 'Hero Motocorp', date, close_price FROM hero_motocorp
  UNION ALL SELECT 'Infosys',       date, close_price FROM infosys
  UNION ALL SELECT 'TCS',           date, close_price FROM tcs
  UNION ALL SELECT 'TVS Motors',    date, close_price FROM tvs_motors
),
ma AS (
  SELECT stock, date, close_price,
         CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY date) >= 20
              THEN AVG(close_price) OVER (PARTITION BY stock ORDER BY date
                     ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)
         END AS ma20,
         CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY date) >= 50
              THEN AVG(close_price) OVER (PARTITION BY stock ORDER BY date
                     ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)
         END AS ma50
  FROM prices
),
lagged AS (
  SELECT stock, date, close_price, ma20, ma50,
         LAG(ma20) OVER (PARTITION BY stock ORDER BY date) AS prev_ma20,
         LAG(ma50) OVER (PARTITION BY stock ORDER BY date) AS prev_ma50
  FROM ma
),
sig AS (
  SELECT stock, date, close_price,
    CASE
      WHEN ma20 IS NULL OR ma50 IS NULL
        OR prev_ma20 IS NULL OR prev_ma50 IS NULL THEN 'Hold'
      WHEN prev_ma20 <= prev_ma50 AND ma20 > ma50 THEN 'Buy'
      WHEN prev_ma20 >= prev_ma50 AND ma20 < ma50 THEN 'Sell'
      ELSE 'Hold'
    END AS signal
  FROM lagged
),
latest AS (
  SELECT stock, date AS last_signal_date, signal AS last_signal,
         ROW_NUMBER() OVER (PARTITION BY stock ORDER BY date DESC) AS rn
  FROM sig
  WHERE signal <> 'Hold'
)
SELECT
  s.stock,
  SUM(CASE WHEN s.signal = 'Buy'  THEN 1 ELSE 0 END) AS buys,
  SUM(CASE WHEN s.signal = 'Sell' THEN 1 ELSE 0 END) AS sells,
  l.last_signal_date,
  l.last_signal
FROM sig s
JOIN latest l ON l.stock = s.stock AND l.rn = 1
GROUP BY s.stock, l.last_signal_date, l.last_signal
ORDER BY s.stock;
-- Checkpoints: 6 rows; sum of buys = 56, sum of sells = 57

Bajaj Auto	12	11	2018-06-21	Buy
Eicher Motors	6	7	2018-06-06	Sell
Hero Motocorp	9	9	2018-05-22	Sell
Infosys	9	9	2018-05-07	Buy
TCS	12	13	2018-06-05	Sell
TVS Motors	8	8	2018-05-17	Sell

-- ------------------------------------------------------------
-- TASK 11: Who went up? (first vs last close, unadjusted)
-- ------------------------------------------------------------
-- Checkpoint: 6 rows; TVS at top with +86.9%
WITH prices AS (
  SELECT 'Bajaj Auto'    AS stock, date, close_price FROM bajaj_auto
  UNION ALL SELECT 'Eicher Motors', date, close_price FROM eicher_motors
  UNION ALL SELECT 'Hero Motocorp', date, close_price FROM hero_motocorp
  UNION ALL SELECT 'Infosys',       date, close_price FROM infosys
  UNION ALL SELECT 'TCS',           date, close_price FROM tcs
  UNION ALL SELECT 'TVS Motors',    date, close_price FROM tvs_motors
),
ends AS (
  SELECT stock, MIN(date) AS first_date, MAX(date) AS last_date
  FROM prices GROUP BY stock
)
SELECT p1.stock,
       p1.close_price AS first_close,
       p2.close_price AS last_close,
       ROUND(100.0 * (p2.close_price - p1.close_price) / p1.close_price, 1) AS pct_change
FROM ends e
JOIN prices p1 ON p1.stock = e.stock AND p1.date = e.first_date
JOIN prices p2 ON p2.stock = e.stock AND p2.date = e.last_date
ORDER BY pct_change DESC;
-- Result (unadjusted — later shown to be WRONG for TCS/Infosys):
--   TVS Motors      276.85   517.45    86.9
--   Eicher Motors 15239.15 27820.95    82.6
--   Bajaj Auto     2454.10  2700.70    10.0
--   Hero Motocorp  3107.30  3293.80     6.0
--   TCS            2548.20  1941.25   -23.8   ← fake loss
--   Infosys        1975.80  1365.00   -30.9   ← fake loss


-- ------------------------------------------------------------
-- TASK 12: Worst day per stock — the data trap
-- ------------------------------------------------------------
-- Checkpoints: 6 rows; two are far worse than the rest
WITH prices AS (
  SELECT 'Bajaj Auto'    AS stock, date, close_price FROM bajaj_auto
  UNION ALL SELECT 'Eicher Motors', date, close_price FROM eicher_motors
  UNION ALL SELECT 'Hero Motocorp', date, close_price FROM hero_motocorp
  UNION ALL SELECT 'Infosys',       date, close_price FROM infosys
  UNION ALL SELECT 'TCS',           date, close_price FROM tcs
  UNION ALL SELECT 'TVS Motors',    date, close_price FROM tvs_motors
),
moves AS (
  SELECT stock, date, close_price,
         ROUND(100.0 * (close_price /
              LAG(close_price) OVER (PARTITION BY stock ORDER BY date) - 1), 1) AS pct_move
  FROM prices
),
ranked AS (
  SELECT stock, date, close_price, pct_move,
         ROW_NUMBER() OVER (PARTITION BY stock ORDER BY pct_move) AS rn
  FROM moves
  WHERE pct_move IS NOT NULL
)
SELECT stock, date, close_price, pct_move
FROM ranked
WHERE rn = 1
ORDER BY pct_move;
-- Result:
--   TCS            2018-05-31  ~1744   ≈ -50%   ← 1:1 BONUS ISSUE
--   Infosys        2015-06-15   ~991   ≈ -50%   ← 1:1 BONUS ISSUE
--   (other 4 stocks: worst day between -6% and -10%)
-- Root cause confirmed via:
--   SELECT date, close_price FROM tcs      WHERE date BETWEEN '2018-05-28' AND '2018-06-01';
--   SELECT date, close_price FROM infosys  WHERE date BETWEEN '2015-06-10' AND '2015-06-15';
-- The price literally halves overnight — a 1:1 bonus, not a real loss.


-- ------------------------------------------------------------
-- TASK 13: Adjust TCS and Infosys for bonus issues
-- ------------------------------------------------------------
-- Event dates (first trading day at the new post-bonus level):
--   TCS     : 2018-05-31
--   Infosys : 2015-06-15
-- For a 1:1 bonus, divide all prices BEFORE the event date by 2.
WITH adjusted AS (
  SELECT 'TCS' AS stock, date,
         CASE WHEN date < '2018-05-31' THEN close_price / 2.0
              ELSE close_price END AS adj_close
  FROM tcs
  UNION ALL
  SELECT 'Infosys', date,
         CASE WHEN date < '2015-06-15' THEN close_price / 2.0
              ELSE close_price END
  FROM infosys
),
ends AS (
  SELECT stock, MIN(date) AS first_date, MAX(date) AS last_date
  FROM adjusted GROUP BY stock
)
SELECT a1.stock,
       a1.adj_close AS first_adjusted,
       a2.adj_close AS last_adjusted,
       ROUND(100.0 * (a2.adj_close - a1.adj_close) / a1.adj_close, 1) AS adjusted_pct_change
FROM ends e
JOIN adjusted a1 ON a1.stock = e.stock AND a1.date = e.first_date
JOIN adjusted a2 ON a2.stock = e.stock AND a2.date = e.last_date
ORDER BY a1.stock;
-- Result:
--   Infosys   987.90   1365.00   38.2
--   TCS      1274.10   1941.25   52.4
-- TCS and Infosys flip from "losers" to "winners" once adjusted.


-- ============================================================
-- END OF ANALYSIS
-- ============================================================