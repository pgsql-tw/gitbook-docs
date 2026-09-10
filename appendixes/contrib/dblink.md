## F.11. dblink — 連線至其他 PostgreSQL 資料庫 [#](#DBLINK)

[dblink_connect](contrib-dblink-connect.md) — 開啟遠端資料庫的持續連線

[dblink_connect_u](contrib-dblink-connect-u.md) — 以不安全的方式開啟遠端資料庫的持續連線

[dblink_disconnect](contrib-dblink-disconnect.md) — 關閉遠端資料庫的持續連線

[dblink](contrib-dblink-function.md) — 在遠端資料庫執行查詢

[dblink_exec](contrib-dblink-exec.md) — 在遠端資料庫執行命令

[dblink_open](contrib-dblink-open.md) — 在遠端資料庫開啟游標

[dblink_fetch](contrib-dblink-fetch.md) — 從遠端資料庫的已開啟游標傳回資料列

[dblink_close](contrib-dblink-close.md) — 關閉遠端資料庫的游標

[dblink_get_connections](contrib-dblink-get-connections.md) — 傳回所有已開啟具名 dblink 連線的名稱

[dblink_error_message](contrib-dblink-error-message.md) — 取得具名連線上的最新錯誤訊息

[dblink_send_query](contrib-dblink-send-query.md) — 將非同步查詢傳送至遠端資料庫

[dblink_is_busy](contrib-dblink-is-busy.md) — 檢查連線是否忙於處理非同步查詢

[dblink_get_notify](contrib-dblink-get-notify.md) — 擷取連線上的非同步通知

[dblink_get_result](contrib-dblink-get-result.md) — 取得非同步查詢結果

[dblink_cancel_query](contrib-dblink-cancel-query.md) — 取消具名連線上的任何作用中查詢

[dblink_get_pkey](contrib-dblink-get-pkey.md) — 傳回關聯主鍵欄位的位置及欄位名稱

[dblink_build_sql_insert](contrib-dblink-build-sql-insert.md) — 使用本端 tuple 建立 INSERT 陳述式，並以提供的替代值取代主鍵欄位值

[dblink_build_sql_delete](contrib-dblink-build-sql-delete.md) — 使用提供的主鍵欄位值建立 DELETE 陳述式

[dblink_build_sql_update](contrib-dblink-build-sql-update.md) — 使用本端 tuple 建立 UPDATE 陳述式，並以提供的替代值取代主鍵欄位值

<a id="id-1.11.7.21.2"></a>

`dblink` 是支援從資料庫 session 內連線至其他 PostgreSQL 資料庫的模組。

`dblink` 可在 `Extension` 等待事件類型下回報下列等待事件。

`DblinkConnect`
:   等待建立至遠端伺服器的連線。

`DblinkGetConnect`
:   在已開啟連線清單中找不到連線時，等待建立至遠端伺服器的連線。

`DblinkGetResult`
:   等待接收遠端伺服器傳回的查詢結果。

另請參閱 [postgres_fdw](postgres-fdw.md)，它以較現代且符合標準的基礎架構提供
大致相同的功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dblink.html)
