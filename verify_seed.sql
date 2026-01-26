USE cppt_db;
SELECT 'Counting Coins...' as check_name;
SELECT COUNT(*) FROM Coins;
SELECT 'Sample Coins...' as check_name;
SELECT * FROM Coins LIMIT 5;
SELECT 'Counting Prices...' as check_name;
SELECT COUNT(*) FROM Prices;
SELECT 'Sample Prices...' as check_name;
SELECT * FROM Prices LIMIT 5;
