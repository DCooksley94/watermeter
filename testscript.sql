use `capstoneHugh`;
-- select sum(volume) from water_meter_raw where id > 9022;
-- select sum(volume) from water_meter_raw where id > 9000;
-- select sum(volume) from water_meter_raw;
-- select sum(volume), Day(recordDate) from water_meter_raw group by Day(recordDate);
select * from water_meter_raw where id = (select max(id) from water_meter_raw);
select sum(volume), recordDate from water_meter_raw where Day(recordDate)=10;
select * from day_Meter_Data;
select sum(volume), recordDate from day_meter_data where Month(recordDate)=7;
select * from month_Meter_Data;
select * from water_meter_raw;
select recordDate, volume from day_Meter_Data where recordDate >= "2022-06-28 00:00:00" AND recordDate < "2022-07-03 00:00:00";
INSERT INTO User values ("username", "password", "Joe", "Schmoe", "email@email.com");
select * from User;
select username from User where username="dcooksley" and password = "notpassword";
select * from Report;
delete from Report where id = 2;
insert into Report(`freq`,`user`,`limit`) values ("limit", "dcooksley", 200)