-- alter table table1 add transactor varchar(10) not Null;

-- alter table  core_sqlorder add  approve_time  varchar(100)   after assigned;
-- alter table  core_sqlorder add  approve_status   int(11)  default 0   after approve_time;

-- alter table  core_sqlorder  DROP COLUMN approve_time;
-- alter table  core_sqlorder  DROP COLUMN approve_status;





alter TABLE   core_sqlorder add  backup_sql text after approve_time;

--  备份SQL主表
create table core_sqlorder_bak(
  id
  work_id
  order_id
  sql_content
);
