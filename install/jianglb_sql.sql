




1、增加redis缓存机制，对于asset或者host等常用信息，放置在redis下，
   两种情况更新redis:

    (1) redis已经没有数据，第一次先去mysql查询，同时同步到redis,然后后面的查询都去到redis;

    (2) asset数据库的更新，会马上同步到mysql,然后马上同步到redis (大概两分钟)，如果查询到redis 没有更新后的数据，马上去mysql里面查询


