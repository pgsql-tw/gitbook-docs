<a id="PGPREWARM"></a>

## F.30. pg_prewarm — 將關聯資料預先載入緩衝區快取 [#](#PGPREWARM)

[F.30.1. 函式](pgprewarm.md#PGPREWARM-FUNCS)

[F.30.2. 設定參數](pgprewarm.md#PGPREWARM-CONFIG-PARAMS)

[F.30.3. 作者](pgprewarm.md#PGPREWARM-AUTHOR)

<a id="id-1.11.7.40.2"></a>

`pg_prewarm` 模組提供一種便利的方式，將關聯資料載入作業系統緩衝區快取或 PostgreSQL 緩衝區快取。預熱可以使用 `pg_prewarm` 函式手動執行，也可以將 `pg_prewarm` 加入
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 來自動執行。在後者的情況下，系統會執行一個背景工作程序，定期將共享緩衝區的內容記錄到名為 `autoprewarm.blocks` 的檔案中，並在重新啟動後使用 2 個背景工作程序重新載入這些相同的區塊。

<a id="PGPREWARM-FUNCS"></a>

### F.30.1. 函式 [#](#PGPREWARM-FUNCS)

```

pg_prewarm(regclass, mode text default 'buffer', fork text default 'main',
           first_block int8 default null,
           last_block int8 default null) RETURNS int8
```

第一個引數是要預熱的關聯。第二個引數是要使用的預熱方法，下文會進一步說明；第三個引數是要預熱的關聯 fork，通常是 `main`。
第四個引數是要預熱的第一個區塊編號（`NULL` 視同零）。第五個引數是要預熱的最後一個區塊編號（`NULL`
表示一路預熱到關聯的最後一個區塊）。傳回值是已預熱的區塊數。

有三種可用的預熱方法。`prefetch`
會向作業系統發出非同步的預先擷取（prefetch）請求；若不支援，則擲出錯誤。`read` 會讀取所要求範圍的區塊；與 `prefetch` 不同，它是同步的，且在所有平台與建置上都受支援，但可能較慢。
`buffer` 會將所要求範圍的區塊讀入資料庫緩衝區快取。

請注意，不論使用哪一種方法，若嘗試預熱的區塊數超過可快取的量（使用 `prefetch` 或
`read` 時由作業系統快取，使用 `buffer` 時由 PostgreSQL 快取），隨著編號較高的區塊被讀入，編號較低的區塊很可能會被逐出。預熱的資料也不會受到任何特別保護而免於被逐出快取，因此其他系統活動可能在新預熱的區塊讀入後不久就將它們逐出；反過來說，預熱也可能將其他資料逐出快取。基於這些原因，預熱通常在啟動時最有用，因為此時快取大多是空的。

```

autoprewarm_start_worker() RETURNS void
```

啟動主要的 autoprewarm 工作程序。這通常會自動發生，但若伺服器啟動時並未設定自動預熱，而你希望稍後再啟動該工作程序，此函式就很有用。

```

autoprewarm_dump_now() RETURNS int8
```

立即更新 `autoprewarm.blocks`。若 autoprewarm 工作程序並未執行，但你預期在下次重新啟動後執行它，此函式可能很有用。傳回值是寫入
`autoprewarm.blocks` 的紀錄數。

<a id="PGPREWARM-CONFIG-PARAMS"></a>

### F.30.2. 設定參數 [#](#PGPREWARM-CONFIG-PARAMS)

`pg_prewarm.autoprewarm` (`boolean`) <a id="id-1.11.7.40.5.2.1.1.3"></a>
:   控制伺服器是否應該執行 autoprewarm 工作程序。預設為開啟。此參數只能在伺服器啟動時設定。

`pg_prewarm.autoprewarm_interval` (`integer`) <a id="id-1.11.7.40.5.3.1.1.3"></a>
:   這是兩次更新 `autoprewarm.blocks` 之間的間隔。
    預設為 300 秒。若設為 0，該檔案不會定期傾印，只會在伺服器關閉時傾印。

這些參數必須在 `postgresql.conf` 中設定。
典型的用法可能如下：

```

# postgresql.conf
shared_preload_libraries = 'pg_prewarm'

pg_prewarm.autoprewarm = true
pg_prewarm.autoprewarm_interval = 300s
```

<a id="PGPREWARM-AUTHOR"></a>

### F.30.3. 作者 [#](#PGPREWARM-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgprewarm.html)（原文版本：18.6；核對日期：2026-10-23）
