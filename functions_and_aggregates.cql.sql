CREATE FUNCTION count_if_true(input boolean)
RETURNS NULL ON NULL INPUT
RETURNS int
LANGUAGE java AS 'if (input) return 1; else return 0;';

SELECT room_number, count_if_true(is_available)
FROM available_rooms_by_hotel_date
WHERE hotel_id='AZ123' and date='2016-01-05';

CREATE FUNCTION state_count_if_true(total int, input boolean)
RETURNS NULL ON NULL INPUT
RETURNS int
LANGUAGE java AS 'if (input) return total+1; else return total;';

CREATE AGGREGATE total_available (boolean)
SFUNC state_count_if_true
STYPE int
INITCOND 0;

SELECT total_available(is_available)
FROM available_rooms_by_hotel_date
WHERE hotel_id='AZ123' and date='2016-01-05';
