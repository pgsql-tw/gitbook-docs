## 29.14. 快速設定 [#](#LOGICAL-REPLICATION-QUICK-SETUP)

首先，在 `postgresql.conf` 中設定下列選項：

```

wal_level = logical
```

其他必要設定的預設值已足以滿足基本設定需求。

需要調整 `pg_hba.conf` 以允許複寫（此處的值取決於實際網路設定及要用來連線的使用者）：

```

host     all     repuser     0.0.0.0/0     scram-sha-256
```

接著，在發佈者資料庫中執行：

```

CREATE PUBLICATION mypub FOR TABLE users, departments;
```

並在訂閱者資料庫中執行：

```

CREATE SUBSCRIPTION mysub CONNECTION 'dbname=foo host=bar user=repuser' PUBLICATION mypub;
```

以上操作會啟動複寫程序，先同步 `users` 與 `departments` 資料表的初始內容，再開始複寫這些資料表的增量變更。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-quick-setup.html)（原文版本：18.6；核對日期：2026-09-07）
