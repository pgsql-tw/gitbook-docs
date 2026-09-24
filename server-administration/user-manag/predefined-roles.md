<a id="PREDEFINED-ROLES"></a>

## 21.5. 預先定義的角色 [#](#PREDEFINED-ROLES)

<a id="id-1.6.8.9.2"></a>

PostgreSQL 提供一組預先定義的角色，
可用來存取某些常見所需的特殊權限功能與資訊。管理者
（包括具有 `CREATEROLE` 權限的角色），
可以將這些角色 `GRANT` 給其環境中的使用者
及／或其他角色，讓這些使用者能夠存取指定的功能與資訊。
舉例來說：

```

GRANT pg_signal_backend TO admin_user;
```

### 警告

在授予這些角色時，應格外謹慎，確保它們只在真正需要的地方
使用，並且要了解這些角色會授予對特權資訊的存取權。

以下說明這些預先定義的角色。請注意，隨著日後
新增更多功能，各角色的具體權限，未來可能會有所變更。
管理者應密切留意版本說明中的相關變更。

<a id="PREDEFINED-ROLE-PG-CHECKPOINT"></a>

`pg_checkpoint` [#](#PREDEFINED-ROLE-PG-CHECKPOINT)
:   `pg_checkpoint` 允許執行
    [`CHECKPOINT`](../../reference/sql-commands/sql-checkpoint.md) 指令。
<a id="PREDEFINED-ROLE-PG-CREATE-SUBSCRIPTION"></a>

`pg_create_subscription` [#](#PREDEFINED-ROLE-PG-CREATE-SUBSCRIPTION)
:   `pg_create_subscription` 允許在資料庫上
    具有 `CREATE` 權限的使用者，發出
    [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md) 指令。
<a id="PREDEFINED-ROLE-PG-DATABASE-OWNER"></a>

`pg_database_owner` [#](#PREDEFINED-ROLE-PG-DATABASE-OWNER)
:   `pg_database_owner` 一律恰好具有一個隱含成員：
    目前的資料庫擁有者。無法將此角色的成員資格授予任何其他角色，
    也不能將任何角色的成員資格，授予
    `pg_database_owner`。不過，就像任何其他角色一樣，
    它可以擁有物件，也可以被授予存取權限。因此，
    一旦 `pg_database_owner` 在某個範本資料庫中
    具有某些權限，則由該範本實體化建立的每一個資料庫，
    其擁有者都會具有這些權限。此角色最初擁有
    `public` schema，因此每個資料庫擁有者，
    都能掌控該 schema 的本機使用方式。
<a id="PREDEFINED-ROLE-PG-MAINTAIN"></a>

`pg_maintain` [#](#PREDEFINED-ROLE-PG-MAINTAIN)
:   `pg_maintain` 允許對所有關聯執行
    [`VACUUM`](../../reference/sql-commands/sql-vacuum.md)、
    [`ANALYZE`](../../reference/sql-commands/sql-analyze.md)、
    [`CLUSTER`](../../reference/sql-commands/sql-cluster.md)、
    [`REFRESH MATERIALIZED VIEW`](../../reference/sql-commands/sql-refreshmaterializedview.md)、
    [`REINDEX`](../../reference/sql-commands/sql-reindex.md)
    以及 [`LOCK TABLE`](../../reference/sql-commands/sql-lock.md)，
    如同對這些物件具有 `MAINTAIN` 權限一般。
<a id="PREDEFINED-ROLE-PG-MONITOR"></a>

`pg_monitor`<br>`pg_read_all_settings`<br>`pg_read_all_stats`<br>`pg_stat_scan_tables` [#](#PREDEFINED-ROLE-PG-MONITOR)
:   這些角色的目的，是讓管理者能夠輕鬆地設定一個角色，
    用於監控資料庫伺服器。它們會授予一組常見的權限，
    讓該角色能夠讀取各種實用的組態設定、統計資訊，
    以及通常僅限超級使用者存取的其他系統資訊。

    `pg_monitor` 允許讀取／執行各種
    監控用的檢視表與函式。此角色是
    `pg_read_all_settings`、
    `pg_read_all_stats` 與
    `pg_stat_scan_tables` 的成員。

    `pg_read_all_settings` 允許讀取所有組態變數，
    即使是通常僅超級使用者可見的變數也不例外。

    `pg_read_all_stats` 允許讀取所有 pg_stat_\* 檢視表，
    並使用各種與統計資訊相關的擴充功能，
    即使是通常僅超級使用者可見的項目也不例外。

    `pg_stat_scan_tables` 允許執行可能會對資料表
    取得 `ACCESS SHARE` 鎖定的監控函式，
    這類鎖定有時可能會持續相當長的時間
    （例如 [pgrowlocks](../../appendixes/contrib/pgrowlocks.md)
    擴充功能中的 `pgrowlocks(text)`）。
<a id="PREDEFINED-ROLE-PG-READ-ALL-DATA"></a>

`pg_read_all_data`<br>`pg_write_all_data` [#](#PREDEFINED-ROLE-PG-READ-ALL-DATA)
:   `pg_read_all_data` 允許讀取所有資料
    （資料表、檢視表、序列），如同對這些物件具有
    `SELECT` 權限、並對所有 schema 具有
    `USAGE` 權限一般。此角色不會略過
    資料列層級安全性（RLS）政策。若有使用 RLS，
    管理者或許會想針對被授予此角色的角色，
    另外設定 `BYPASSRLS`。

    `pg_write_all_data` 允許寫入所有資料
    （資料表、檢視表、序列），如同對這些物件具有
    `INSERT`、`UPDATE` 與
    `DELETE` 權限、並對所有 schema 具有
    `USAGE` 權限一般。此角色不會略過
    資料列層級安全性（RLS）政策。若有使用 RLS，
    管理者或許會想針對被授予此角色的角色，
    另外設定 `BYPASSRLS`。
<a id="PREDEFINED-ROLE-PG-READ-SERVER-FILES"></a>

`pg_read_server_files`<br>`pg_write_server_files`<br>`pg_execute_server_program` [#](#PREDEFINED-ROLE-PG-READ-SERVER-FILES)
:   這些角色的目的，是讓管理者能夠擁有受信任、但非超級使用者的
    角色，讓其能以資料庫執行時所使用的使用者身分，
    存取伺服器上的檔案並執行程式。這些角色在直接存取檔案時，
    會略過所有資料庫層級的權限檢查，因此可能被用來取得
    等同超級使用者層級的存取權。因此，在將這些角色授予
    使用者時，應格外謹慎。

    `pg_read_server_files` 允許使用
    `COPY` 及其他檔案存取函式，讀取資料庫
    在伺服器上能夠存取之任何位置的檔案。

    `pg_write_server_files` 允許使用
    `COPY` 及其他檔案存取函式，寫入至資料庫
    在伺服器上能夠存取之任何位置的檔案。

    `pg_execute_server_program` 允許使用
    `COPY` 及其他能夠執行伺服端程式的函式，
    以資料庫執行時所使用的使用者身分，
    在資料庫伺服器上執行程式。
<a id="PREDEFINED-ROLE-PG-SIGNAL-AUTOVACUUM-WORKER"></a>

`pg_signal_autovacuum_worker` [#](#PREDEFINED-ROLE-PG-SIGNAL-AUTOVACUUM-WORKER)
:   `pg_signal_autovacuum_worker` 允許發送信號給
    autovacuum 工作程序，以取消目前資料表的 vacuum 操作，
    或終止其工作階段。請參閱
    [9.28.2 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)。
<a id="PREDEFINED-ROLE-PG-SIGNAL-BACKEND"></a>

`pg_signal_backend` [#](#PREDEFINED-ROLE-PG-SIGNAL-BACKEND)
:   `pg_signal_backend` 允許發送信號給另一個後端程序，
    以取消查詢或終止其工作階段。請注意，此角色不允許
    對超級使用者所擁有的後端程序發送信號。請參閱
    [9.28.2 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)。
<a id="PREDEFINED-ROLE-PG-USE-RESERVED-CONNECTIONS"></a>

`pg_use_reserved_connections` [#](#PREDEFINED-ROLE-PG-USE-RESERVED-CONNECTIONS)
:   `pg_use_reserved_connections` 允許使用透過
    [reserved_connections](../runtime-config/runtime-config-connection.md#GUC-RESERVED-CONNECTIONS)
    保留的連線插槽。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/predefined-roles.html)（原文版本：18.6；核對日期：2026-09-24）
