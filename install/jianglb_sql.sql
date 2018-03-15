

1、安装sqlite3，创建token_db_new数据库
sudo apt-get install sqlite3
sqlite3 -version

cd /root/
mkdir
sqlite3 token.db

2、 创建 token_db_new 数据表
create table token_db_new(
username char(20) not null,
workid  char(50) not null,
token char(50) not null
)
