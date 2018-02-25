-- alter table table1 add transactor varchar(10) not Null;

-- alter table  core_sqlorder add  approve_time  varchar(100)   after assigned;
-- alter table  core_sqlorder add  approve_status   int(11)  default 0   after approve_time;

-- alter table  core_sqlorder  DROP COLUMN approve_time;
-- alter table  core_sqlorder  DROP COLUMN approve_status;



-- 资源表，这里主要是menu表
create table t_resource(
  id int primary key ,
  name char(30) not null,
  type char(15) not null,
  status char(40) not null,
  order_num int ,
  is_parent  int default 0 not null
)

