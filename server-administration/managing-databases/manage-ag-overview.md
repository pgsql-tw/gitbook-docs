<a id="MANAGE-AG-OVERVIEW"></a>

## 22.1. 概觀 [#](#MANAGE-AG-OVERVIEW)

<a id="id-1.6.9.4.2"></a>

少數物件，例如角色、資料庫與資料表空間的名稱，是在叢集層級定義，並儲存在
`pg_global` 資料表空間中。叢集內部有多個資料庫，這些資料庫彼此隔離，但可以存取
叢集層級的物件。每個資料庫內部有多個綱要，綱要中包含資料表與函式等物件。
因此完整的階層是：叢集、資料庫、綱要、資料表（或其他種類的物件，例如函式）。

連線到資料庫伺服器時，用戶端必須在其連線請求中指定資料庫名稱。
每個連線無法存取超過一個資料庫。不過，用戶端可以對同一個資料庫或不同的資料庫
開啟多個連線。
資料庫層級的安全性有兩個組成部分：存取控制
（請參閱[第 20.1 節](../client-authentication/auth-pg-hba-conf.md)），在連線層級管理；
以及授權控制
（請參閱[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)），透過授權（grant）系統管理。
外部資料包裝器（請參閱 [postgres_fdw](../../appendixes/contrib/postgres-fdw.md)）
可讓一個資料庫內的物件充當其他資料庫或叢集中物件的代理。
較舊的 dblink 模組（請參閱 [dblink](../../appendixes/contrib/dblink.md)）提供類似的功能。
預設情況下，所有使用者都可以使用所有連線方式連線到所有資料庫。

如果一個 PostgreSQL 伺服器叢集預計容納彼此無關、且大致上應該互不知悉的
專案或使用者，建議將它們放入不同的資料庫，並相應調整授權與存取控制。
如果這些專案或使用者彼此相關，因此應該能夠使用彼此的資源，則應該將它們放在同一個
資料庫中，但或許放入不同的綱要；這樣可以提供具備命名空間隔離與授權控制
的模組化結構。
關於管理綱要的更多資訊，請參閱[第 5.10 節](../../the-sql-language/ddl/ddl-schemas.md)。

雖然可以在單一叢集內建立多個資料庫，但建議審慎考量其效益是否大於風險與限制，
特別是共用 WAL（請參閱[第 28 章](../wal/README.md)）
對備份與復原選項的影響。雖然從使用者的角度來看，叢集中的各個資料庫是彼此隔離的，
但從資料庫管理者的角度來看，它們是緊密相連的。

資料庫以 `CREATE DATABASE` 命令建立
（請參閱[第 22.2 節](manage-ag-createdb.md)），並以
`DROP DATABASE` 命令銷毀
（請參閱[第 22.5 節](manage-ag-dropdb.md)）。
若要得知現有資料庫的集合，請查看
`pg_database` 系統目錄，例如

```

SELECT datname FROM pg_database;
```

[psql](../../reference/reference-client/app-psql.md) 程式的 `\l` 元命令
與 `-l` 命令列選項也可用來列出
現有的資料庫。

<a id="MANAGE-AG-OVERVIEW-NOTE"></a>

### 注意

SQL 標準將資料庫稱為「catalogs」（目錄），但在實務上
兩者沒有差別。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-overview.html)（原文版本：18.6；核對日期：2026-10-10）
