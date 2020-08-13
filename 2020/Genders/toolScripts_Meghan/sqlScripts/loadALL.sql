create gender;

insert into NODE (cluster,node_num,node_name)
values("test",1,"test1");
insert into NODE (cluster,node_num,node_name)
values("test",2,"test2");
insert into NODE (cluster,node_num,node_name)
values("test",3,"test3");
insert into NODE (cluster,node_num,node_name)
values("experiment",1,"experiment1");
insert into NODE (cluster,node_num,node_name)
values("experiment",2,"experiment2");

insert into GENDER(gender_name,descrip)
values("archive_zone","Facility");
insert into GENDER(gender_name,descrip)
values("center","Facility");
insert into GENDER(gender_name,descrip)
values("arena","Facility");

insert into GENDER(gender_name,descrip)
values("rdma","Hardware");
insert into GENDER(gender_name,descrip)
values("model","Hardware");

insert into GENDER(gender_name,descrip)
values("mgmt", "mgmt");
insert into GENDER(gender_name,descrip)
values("crond","Login");

insert into CONFIGURATION(config_id,val,node_name,gender_name)
values("test1_archive_zone","green","test1","archive_zone");
insert into CONFIGURATION(config_id,val,node_name,gender_name)
values("test2_archive_zone","green","test2","archive_zone");
insert into CONFIGURATION(config_id,val,node_name,gender_name)
values("test1_arena","attb","test1","arena");
insert into CONFIGURATION(config_id,node_name,gender_name)
values("test3_rdma","test3","rdma");


