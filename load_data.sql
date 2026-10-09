-- Bajaj Auto
LOAD DATA LOCAL INFILE 'C:/stocks/Bajaj Auto.csv'
INTO TABLE bajaj_auto
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET date = STR_TO_DATE(@d, '%d-%M-%Y'),
    open_price = NULLIF(@o,''),
    high_price = NULLIF(@h,''),
    low_price = NULLIF(@l,''),
    close_price = NULLIF(@c,''),
    wap = NULLIF(@w,''),
    no_of_shares = NULLIF(@s,''),
    no_of_trades = NULLIF(@tr,''),
    total_turnover = NULLIF(@to,''),
    deliverable_qty = NULLIF(@dq,''),
    pct_deli_qty = NULLIF(@pd,''),
    spread_high_low = NULLIF(@shl,''),
    spread_close_open = NULLIF(TRIM(@sco),'');

-- Eicher Motors
LOAD DATA LOCAL INFILE 'C:/stocks/Eicher Motors.csv'
INTO TABLE eicher_motors
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET date = STR_TO_DATE(@d, '%d-%M-%Y'),
    open_price = NULLIF(@o,''),
    high_price = NULLIF(@h,''),
    low_price = NULLIF(@l,''),
    close_price = NULLIF(@c,''),
    wap = NULLIF(@w,''),
    no_of_shares = NULLIF(@s,''),
    no_of_trades = NULLIF(@tr,''),
    total_turnover = NULLIF(@to,''),
    deliverable_qty = NULLIF(@dq,''),
    pct_deli_qty = NULLIF(@pd,''),
    spread_high_low = NULLIF(@shl,''),
    spread_close_open = NULLIF(TRIM(@sco),'');

-- Hero Motocorp
LOAD DATA LOCAL INFILE 'C:/stocks/Hero Motocorp.csv'
INTO TABLE hero_motocorp
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET date = STR_TO_DATE(@d, '%d-%M-%Y'),
    open_price = NULLIF(@o,''),
    high_price = NULLIF(@h,''),
    low_price = NULLIF(@l,''),
    close_price = NULLIF(@c,''),
    wap = NULLIF(@w,''),
    no_of_shares = NULLIF(@s,''),
    no_of_trades = NULLIF(@tr,''),
    total_turnover = NULLIF(@to,''),
    deliverable_qty = NULLIF(@dq,''),
    pct_deli_qty = NULLIF(@pd,''),
    spread_high_low = NULLIF(@shl,''),
    spread_close_open = NULLIF(TRIM(@sco),'');

-- Infosys
LOAD DATA LOCAL INFILE 'C:/stocks/Infosys.csv'
INTO TABLE infosys
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET date = STR_TO_DATE(@d, '%d-%M-%Y'),
    open_price = NULLIF(@o,''),
    high_price = NULLIF(@h,''),
    low_price = NULLIF(@l,''),
    close_price = NULLIF(@c,''),
    wap = NULLIF(@w,''),
    no_of_shares = NULLIF(@s,''),
    no_of_trades = NULLIF(@tr,''),
    total_turnover = NULLIF(@to,''),
    deliverable_qty = NULLIF(@dq,''),
    pct_deli_qty = NULLIF(@pd,''),
    spread_high_low = NULLIF(@shl,''),
    spread_close_open = NULLIF(TRIM(@sco),'');

-- TCS
LOAD DATA LOCAL INFILE 'C:/stocks/TCS.csv'
INTO TABLE tcs
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET date = STR_TO_DATE(@d, '%d-%M-%Y'),
    open_price = NULLIF(@o,''),
    high_price = NULLIF(@h,''),
    low_price = NULLIF(@l,''),
    close_price = NULLIF(@c,''),
    wap = NULLIF(@w,''),
    no_of_shares = NULLIF(@s,''),
    no_of_trades = NULLIF(@tr,''),
    total_turnover = NULLIF(@to,''),
    deliverable_qty = NULLIF(@dq,''),
    pct_deli_qty = NULLIF(@pd,''),
    spread_high_low = NULLIF(@shl,''),
    spread_close_open = NULLIF(TRIM(@sco),'');

-- TVS Motors
LOAD DATA LOCAL INFILE 'C:/stocks/TVS Motors.csv'
INTO TABLE tvs_motors
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET date = STR_TO_DATE(@d, '%d-%M-%Y'),
    open_price = NULLIF(@o,''),
    high_price = NULLIF(@h,''),
    low_price = NULLIF(@l,''),
    close_price = NULLIF(@c,''),
    wap = NULLIF(@w,''),
    no_of_shares = NULLIF(@s,''),
    no_of_trades = NULLIF(@tr,''),
    total_turnover = NULLIF(@to,''),
    deliverable_qty = NULLIF(@dq,''),
    pct_deli_qty = NULLIF(@pd,''),
    spread_high_low = NULLIF(@shl,''),
    spread_close_open = NULLIF(TRIM(@sco),'');