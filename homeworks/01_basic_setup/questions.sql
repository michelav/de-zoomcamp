-- Q3. How many taxi trips were there on January 15?
select 'Many trips on Jan, 15' as Q3,  count(*) from yellow_taxi_data where tpep_pickup_datetime::date = '2021-01-15';

-- Q4. Find the largest tip for each day. On which day it was the largest tip in January?
select 'Which day has the largest tip' as Q4,  DATE_TRUNC('day', tpep_pickup_datetime) as dt, max(tip_amount) as max_tip from yellow_taxi_data 
group by dt order by max_tip desc limit 1;

-- Q5. What was the most popular destination for passengers picked up in central park on January 14?
select 'Most popular destination' as Q5, up."Zone" as pickup, down."Zone" as dest, count(up."Zone") as counting from yellow_taxi_data td 
    inner join taxi_zone up on (td."PULocationID" = up."LocationID") left join taxi_zone down on 
    (td."DOLocationID" = down."LocationID") where up."Zone" = 'Central Park' AND 
    td.tpep_pickup_datetime::date = '2021-01-14' group by down."Zone", up."Zone" order by counting desc limit 1;

-- Q6. What's the pickup-dropoff pair with the largest average price for a ride (calculated based on total_amount)?
select 'Largest avg price pickup-dropoff' as Q6, CONCAT(coalesce(up."Zone", 'Unknown') , ' / ', coalesce(down."Zone", 'Unknown')) as pair, 
    avg(td.total_amount) as max_fare from yellow_taxi_data td left join taxi_zone up 
    on (td."PULocationID" = up."LocationID") left join taxi_zone down on (td."DOLocationID" = down."LocationID") 
    group by 2 order by max_fare desc limit 1;
