-- use zamato
select count(*) from users;

-- Random Sample function
select * from users u order by rand() limit 5 ;

-- Null 
select * from orders where restaurant_rating  is null ;

-- to replace null value 
-- update orders set restaurant_rating  = 0  where restaurant_rating is null

select  name ,Count(*) from users u  join orders o on u.user_id = o.user_id
group by o.user_id 

select r.r_name  ,count(*) as "Num_of_item" from restaurants r join orders  o on r.r_id  = o.r_id 
group  by r.r_name 
order  by Num_of_item   desc;

select r.r_name ,m.price ,count(*) as "Menu_items" from restaurants r  join menu m  on r.r_id =m.r_id 
group by m.r_id ;


select r.r_name ,count(*) as "Number of vote",Round(avg(o.restaurant_rating),2) as "Avg_restaurant_rating" from  
orders o join  restaurants r on o.r_id = r.r_id 
where o.restaurant_rating  is not null
group by o.r_id;


-- 10
select  r.r_name ,sum(o.amount) as "Reneve"  from orders o  join restaurants r  on o.r_id = r.r_id 
group  by o.r_id 
having  Reneve >1500;


-- 
select m.r_id,r.r_name  ,COUNT(*),Round(sum(m.price)/count(*),2) as avg  from menu m
join restaurants r on r.	r_id = m.r_id 
group by m.r_id 		
order by avg desc limit 1 ;

select dp.partner_id ,dp.partner_name,count(*) as "num_of_delivery",
o.restaurant_rating ,round(avg(o.delivery_rating ),2)as "Avg_delivery",
count(*)* 100 + 1000 * round(avg(o.delivery_rating ),2) as "compensation_salary"
from delivery_partner dp join orders o on 
o.partner_id = dp.partner_id 
group by dp.partner_id 
order by compensation_salary  desc ;


-- 17
select corr(delivery_time ,delivery_rating +restaurant_rating ) from orders ;

select t1.r_id,t3.r_name ,type from menu t1 join food t2 
on t1.f_id  = t2.f_id 
join restaurants t3  
group by t1.r_id 
having type like "veg"

select name,MIN(o.amount),MAX(amount),AVG(amount) from orders o join users u on o.user_id =u.user_id 
group  by u.user_id ; 