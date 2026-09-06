# 31.11. 快速設定

首先在 postgresql.conf 中進行組態設定：

```
wal_level = logical
```

其他所需的設定的預設值已經足夠。

需要調整 pg\_hba.conf 以允許複寫（這裡的內容取決於您想要用於連線的實際網路配置和使用者）：

```
host     all     repuser     0.0.0.0/0     md5
```

然後在發佈者的資料庫上：

```
CREATE PUBLICATION mypub FOR TABLE users, departments;
```

在訂閱者的資料庫上：

```
CREATE SUBSCRIPTION mysub CONNECTION 'dbname=foo host=bar user=repuser' PUBLICATION mypub;
```

以上將啟動複寫程序，此程序同步資料表 users 和 departments 的初始資料表內容，然後開始以增量變更複寫到這些資料表。
