# HSA13_hw9_Database_Replication

docker-compose up -d

## MASTER SETUP

```
docker exec -it mysql-m mysql -uroot -prootpass
```


```
CREATE USER 'repl'@'%' IDENTIFIED WITH 'sha256_password' BY 'replpass';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
ALTER USER 'repl'@'%' REQUIRE NONE;
FLUSH PRIVILEGES;
```

```
mysql> SELECT user, host, plugin, ssl_type FROM mysql.user WHERE user = 'repl';
```



| user | host | plugin          | ssl_type |
|------|------|-----------------|----------|
| repl | %    | sha256_password |          |



1 row in set (0.00 sec)


mysql> SHOW VARIABLES LIKE 'require_secure_transport';
|--------------------------|-------|
| Variable_name            | Value |
|--------------------------|-------|
| require_secure_transport | OFF   |
|--------------------------|-------|
1 row in set (0.00 sec)


SHOW BINARY LOG STATUS;
mysql> SHOW BINARY LOG STATUS;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000003 |     3095 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+


mysql> SHOW BINARY LOGS;
+------------------+-----------+-----------+
| Log_name         | File_size | Encrypted |
+------------------+-----------+-----------+
| mysql-bin.000001 |       181 | No        |
| mysql-bin.000002 |   2976178 | No        |
| mysql-bin.000003 |      3095 | No        |
+------------------+-----------+-----------+
3 rows in set (0.00 sec)


mysql> SHOW BINLOG EVENTS;
+------------------+-----+----------------+-----------+-------------+----------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                             |
+------------------+-----+----------------+-----------+-------------+----------------------------------+
| mysql-bin.000001 |   4 | Format_desc    |         1 |         127 | Server ver: 9.2.0, Binlog ver: 4 |
| mysql-bin.000001 | 127 | Previous_gtids |         1 |         158 |                                  |
| mysql-bin.000001 | 158 | Stop           |         1 |         181 |                                  |
+------------------+-----+----------------+-----------+-------------+----------------------------------+
3 rows in set (0.00 sec)



mysql> SELECT user, host, plugin FROM mysql.user WHERE user = 'root';
+------+-----------+-----------------------+
| user | host      | plugin                |
+------+-----------+-----------------------+
| root | %         | caching_sha2_password |
| root | localhost | caching_sha2_password |
+------+-----------+-----------------------+
2 rows in set (0.01 sec)

mysql> SELECT user, host, plugin FROM mysql.user WHERE user = 'repl';
+------+------+-----------------+
| user | host | plugin          |
+------+------+-----------------+
| repl | %    | sha256_password |
+------+------+-----------------+
1 row in set (0.00 sec)


exit
.\.venv\Scripts\Activate.ps1

# mysql-s1:
docker exec -it mysql-s1 mysql -uroot -prootpass

mysql> STOP REPLICA;


CHANGE REPLICATION SOURCE TO
         SOURCE_HOST='mysql-m',
         SOURCE_USER='repl',
         SOURCE_PASSWORD='replpass',
         SOURCE_LOG_FILE='mysql-bin.000003',
         SOURCE_LOG_POS=3095;
mysql> CHANGE REPLICATION SOURCE TO
    ->     SOURCE_HOST='mysql-m',
    ->     SOURCE_USER='repl',
    ->     SOURCE_PASSWORD='replpass',
    ->     SOURCE_LOG_FILE='mysql-bin.000003',
    ->     SOURCE_LOG_POS=2283;
Query OK, 0 rows affected, 2 warnings (0.03 sec)


mysql> START REPLICA;
Query OK, 0 rows affected (0.02 sec)

mysql> SHOW REPLICA STATUS\G
*************************** 1. row ***************************
             Replica_IO_State: Waiting for source to send event
                  Source_Host: mysql-m
                  Source_User: repl
                  Source_Port: 3306
                Connect_Retry: 60
              Source_Log_File: mysql-bin.000003
          Read_Source_Log_Pos: 3095
               Relay_Log_File: relay-bin.000002
                Relay_Log_Pos: 328
        Relay_Source_Log_File: mysql-bin.000003
           Replica_IO_Running: Yes
          Replica_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Source_Log_Pos: 3095
              Relay_Log_Space: 533
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Source_SSL_Allowed: No
           Source_SSL_CA_File:
           Source_SSL_CA_Path:
              Source_SSL_Cert:
            Source_SSL_Cipher:
               Source_SSL_Key:
        Seconds_Behind_Source: 0
Source_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Source_Server_Id: 1
                  Source_UUID: 0611a0f7-fd0c-11ef-8473-0242ac120002
             Source_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
    Replica_SQL_Running_State: Replica has read all relay log; waiting for more updates
           Source_Retry_Count: 10
                  Source_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Source_SSL_Crl:
           Source_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Source_TLS_Version:
       Source_public_key_path:
        Get_Source_public_key: 0
            Network_Namespace:
1 row in set (0.00 sec)



# mysql-s2:
docker exec -it mysql-s2 mysql -uroot -prootpass


mysql> STOP REPLICA;
Query OK, 0 rows affected (0.02 sec)

CHANGE REPLICATION SOURCE TO
         SOURCE_HOST='mysql-m',
         SOURCE_USER='repl',
         SOURCE_PASSWORD='replpass',
         SOURCE_LOG_FILE='mysql-bin.000003',
         SOURCE_LOG_POS=3095;
mysql> CHANGE REPLICATION SOURCE TO
    ->     SOURCE_HOST='mysql-m',
    ->     SOURCE_USER='repl',
    ->     SOURCE_PASSWORD='replpass',
    ->     SOURCE_LOG_FILE='mysql-bin.000003',
    ->     SOURCE_LOG_POS=3095;
Query OK, 0 rows affected, 2 warnings (0.03 sec)


mysql> START REPLICA;
Query OK, 0 rows affected (0.02 sec)

mysql> SHOW REPLICA STATUS\G
*************************** 1. row ***************************
             Replica_IO_State: Waiting for source to send event
                  Source_Host: mysql-m
                  Source_User: repl
                  Source_Port: 3306
                Connect_Retry: 60
              Source_Log_File: mysql-bin.000003
          Read_Source_Log_Pos: 3095
               Relay_Log_File: relay-bin.000002
                Relay_Log_Pos: 328
        Relay_Source_Log_File: mysql-bin.000003
           Replica_IO_Running: Yes
          Replica_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Source_Log_Pos: 3095
              Relay_Log_Space: 533
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Source_SSL_Allowed: No
           Source_SSL_CA_File:
           Source_SSL_CA_Path:
              Source_SSL_Cert:
            Source_SSL_Cipher:
               Source_SSL_Key:
        Seconds_Behind_Source: 0
Source_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Source_Server_Id: 1
                  Source_UUID: 0611a0f7-fd0c-11ef-8473-0242ac120002
             Source_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
    Replica_SQL_Running_State: Replica has read all relay log; waiting for more updates
           Source_Retry_Count: 10
                  Source_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Source_SSL_Crl:
           Source_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Source_TLS_Version:
       Source_public_key_path:
        Get_Source_public_key: 0
            Network_Namespace:
1 row in set (0.00 sec)



# MASTER
mysql> USE test_db;
Database changed
mysql> CREATE TABLE test_table (   id INT AUTO_INCREMENT PRIMARY KEY,   name VARCHAR(50),   timestamp DATETIME );
Query OK, 0 rows affected (0.07 sec)

mysql> INSERT INTO test_table VALUES (2, 'Test2','2025-03-09');
Query OK, 1 row affected (0.02 sec)

mysql> select * from test_table;
+----+-------+---------------------+
| id | name  | timestamp           |
+----+-------+---------------------+
|  2 | Test2 | 2025-03-09 00:00:00 |
+----+-------+---------------------+
1 row in set (0.00 sec)

mysql> INSERT INTO test_table VALUES (3, 'Test3','2025-03-09');
Query OK, 1 row affected (0.00 sec)
mysql> INSERT INTO test_table VALUES (4, 'Test4','2025-03-09');
Query OK, 1 row affected (0.00 sec)

# mysql-s1:
mysql> select * from test_table;
+----+-------+---------------------+
| id | name  | timestamp           |
+----+-------+---------------------+
|  2 | Test2 | 2025-03-09 00:00:00 |
|  3 | Test3 | 2025-03-09 00:00:00 |
|  4 | Test4 | 2025-03-09 00:00:00 |
+----+-------+---------------------+
3 rows in set (0.00 sec)

# mysql-s2:
mysql> select * from test_table;
+----+-------+---------------------+
| id | name  | timestamp           |
+----+-------+---------------------+
|  2 | Test2 | 2025-03-09 00:00:00 |
|  3 | Test3 | 2025-03-09 00:00:00 |
|  4 | Test4 | 2025-03-09 00:00:00 |
+----+-------+---------------------+
3 rows in set (0.00 sec)


pip install -r requirements.txt
.\.venv\Scripts\python.exe .\app\app.py

# mysql-s1:
# mysql-s2:
mysql> SELECT * FROM test_table;
+-----+-------------+---------------------+
| id  | name        | timestamp           |
+-----+-------------+---------------------+
|   2 | Test2       | 2025-03-09 00:00:00 |
|   3 | Test3       | 2025-03-09 00:00:00 |
|   4 | Test4       | 2025-03-09 00:00:00 |
|   5 | test_name_0 | 2025-03-09 21:16:48 |
|   6 | test_name_1 | 2025-03-09 21:16:48 |
|   7 | test_name_2 | 2025-03-09 21:16:48 |
|   8 | test_name_3 | 2025-03-09 21:16:48 |
|   9 | test_name_4 | 2025-03-09 21:16:48 |
|  10 | test_name_5 | 2025-03-09 21:16:48 |
|  11 | test_name_6 | 2025-03-09 21:16:48 |
|  12 | test_name_7 | 2025-03-09 21:16:48 |
|  13 | test_name_8 | 2025-03-09 21:16:48 |
|  14 | test_name_9 | 2025-03-09 21:16:48 |
