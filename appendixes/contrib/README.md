## 附錄 F：額外提供的模組與擴充功能

**目錄**

[F.1. amcheck — 驗證資料表與索引一致性的工具](amcheck.md)
:   [F.1.1. 函式](amcheck.md#AMCHECK-FUNCTIONS)

    [F.1.2. 選用的 *`heapallindexed`* 驗證](amcheck.md#AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION)

    [F.1.3. 有效使用 `amcheck`](amcheck.md#AMCHECK-USING-AMCHECK-EFFECTIVELY)

    [F.1.4. 修復毀損](amcheck.md#AMCHECK-REPAIRING-CORRUPTION)

[F.2. auth_delay — 驗證失敗時暫停](auth-delay.md)
:   [F.2.1. 設定參數](auth-delay.md#AUTH-DELAY-CONFIGURATION-PARAMETERS)

    [F.2.2. 作者](auth-delay.md#AUTH-DELAY-AUTHOR)

[F.3. auto_explain — 記錄慢速查詢的執行計畫](auto-explain.md)
:   [F.3.1. 設定參數](auto-explain.md#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS)

    [F.3.2. 範例](auto-explain.md#AUTO-EXPLAIN-EXAMPLE)

    [F.3.3. 作者](auto-explain.md#AUTO-EXPLAIN-AUTHOR)

[F.4. basebackup_to_shell — 「shell」pg_basebackup 模組範例](basebackup-to-shell.md)
:   [F.4.1. 設定參數](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS)

    [F.4.2. 作者](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-AUTHOR)

[F.5. basic_archive — WAL 封存模組範例](basic-archive.md)
:   [F.5.1. 設定參數](basic-archive.md#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)

    [F.5.2. 注意事項](basic-archive.md#BASIC-ARCHIVE-NOTES)

    [F.5.3. 作者](basic-archive.md#BASIC-ARCHIVE-AUTHOR)

[F.6. bloom — Bloom 篩選器索引存取方法](bloom.md)
:   [F.6.1. 參數](bloom.md#BLOOM-PARAMETERS)

    [F.6.2. 範例](bloom.md#BLOOM-EXAMPLES)

    [F.6.3. 運算子類別介面](bloom.md#BLOOM-OPERATOR-CLASS-INTERFACE)

    [F.6.4. 限制](bloom.md#BLOOM-LIMITATIONS)

    [F.6.5. 作者](bloom.md#BLOOM-AUTHORS)

[F.7. btree_gin — 具有 B-tree 行為的 GIN 運算子類別](btree-gin.md)
:   [F.7.1. 使用範例](btree-gin.md#BTREE-GIN-EXAMPLE-USAGE)

    [F.7.2. 作者](btree-gin.md#BTREE-GIN-AUTHORS)

[F.8. btree_gist — 具有 B-tree 行為的 GiST 運算子類別](btree-gist.md)
:   [F.8.1. 使用範例](btree-gist.md#BTREE-GIST-EXAMPLE-USAGE)

    [F.8.2. 作者](btree-gist.md#BTREE-GIST-AUTHORS)

[F.9. citext — 不區分大小寫的字元字串型別](citext.md)
:   [F.9.1. 原理](citext.md#CITEXT-RATIONALE)

    [F.9.2. 使用方式](citext.md#CITEXT-HOW-TO-USE-IT)

    [F.9.3. 字串比較行為](citext.md#CITEXT-STRING-COMPARISON-BEHAVIOR)

    [F.9.4. 限制](citext.md#CITEXT-LIMITATIONS)

    [F.9.5. 作者](citext.md#CITEXT-AUTHOR)

[F.10. cube — 多維立方體資料型別](cube.md)
:   [F.10.1. 語法](cube.md#CUBE-SYNTAX)

    [F.10.2. 精確度](cube.md#CUBE-PRECISION)

    [F.10.3. 用法](cube.md#CUBE-USAGE)

    [F.10.4. 預設值](cube.md#CUBE-DEFAULTS)

    [F.10.5. 注意事項](cube.md#CUBE-NOTES)

    [F.10.6. 鳴謝](cube.md#CUBE-CREDITS)

[F.11. dblink — 連線至其他 PostgreSQL 資料庫](dblink.md)
:   [dblink_connect](contrib-dblink-connect.md) — 開啟至遠端資料庫的持續連線

    [dblink_connect_u](contrib-dblink-connect-u.md) — 以不安全的方式開啟至遠端資料庫的持續連線

    [dblink_disconnect](contrib-dblink-disconnect.md) — 關閉至遠端資料庫的持續連線

    [dblink](contrib-dblink-function.md) — 在遠端資料庫中執行查詢

    [dblink_exec](contrib-dblink-exec.md) — 在遠端資料庫中執行指令

    [dblink_open](contrib-dblink-open.md) — 在遠端資料庫中開啟游標

    [dblink_fetch](contrib-dblink-fetch.md) — 傳回遠端資料庫中已開啟游標的資料列

    [dblink_close](contrib-dblink-close.md) — 關閉遠端資料庫中的游標

    [dblink_get_connections](contrib-dblink-get-connections.md) — 傳回所有已開啟具名 dblink 連線的名稱

    [dblink_error_message](contrib-dblink-error-message.md) — 取得具名連線上的最新錯誤訊息

    [dblink_send_query](contrib-dblink-send-query.md) — 將非同步查詢傳送至遠端資料庫

    [dblink_is_busy](contrib-dblink-is-busy.md) — 檢查連線是否正忙於非同步查詢

    [dblink_get_notify](contrib-dblink-get-notify.md) — 擷取連線上的非同步通知

    [dblink_get_result](contrib-dblink-get-result.md) — 取得非同步查詢結果

    [dblink_cancel_query](contrib-dblink-cancel-query.md) — 取消具名連線上的任何作用中查詢

    [dblink_get_pkey](contrib-dblink-get-pkey.md) — 傳回關聯主鍵欄位的位置與欄位名稱

    [dblink_build_sql_insert](contrib-dblink-build-sql-insert.md) — 使用本機 tuple 建立 INSERT 陳述式，並以提供的替代值取代主鍵欄位值

    [dblink_build_sql_delete](contrib-dblink-build-sql-delete.md) — 使用提供的主鍵欄位值建立 DELETE 陳述式

    [dblink_build_sql_update](contrib-dblink-build-sql-update.md) — 使用本機 tuple 建立 UPDATE 陳述式，並以提供的替代值取代主鍵欄位值

[F.12. dict_int — 整數全文檢索字典範例](dict-int.md)
:   [F.12.1. 設定](dict-int.md#DICT-INT-CONFIG)

    [F.12.2. 用法](dict-int.md#DICT-INT-USAGE)

[F.13. dict_xsyn — 同義詞全文檢索字典範例](dict-xsyn.md)
:   [F.13.1. 設定](dict-xsyn.md#DICT-XSYN-CONFIG)

    [F.13.2. 用法](dict-xsyn.md#DICT-XSYN-USAGE)

[F.14. earthdistance — 計算大圓距離](earthdistance.md)
:   [F.14.1. 以立方體為基礎的地球距離](earthdistance.md#EARTHDISTANCE-CUBE-BASED)

    [F.14.2. 以點為基礎的地球距離](earthdistance.md#EARTHDISTANCE-POINT-BASED)

[F.15. file_fdw — 存取伺服器檔案系統中的資料檔](file-fdw.md)

[F.16. fuzzystrmatch — 判定字串相似度與距離](fuzzystrmatch.md)
:   [F.16.1. Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-SOUNDEX)

    [F.16.2. Daitch-Mokotoff Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-DAITCH-MOKOTOFF)

    [F.16.3. Levenshtein](fuzzystrmatch.md#FUZZYSTRMATCH-LEVENSHTEIN)

    [F.16.4. Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-METAPHONE)

    [F.16.5. Double Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-DOUBLE-METAPHONE)

[F.17. hstore — hstore 索引鍵／值資料型別](hstore.md)
:   [F.17.1. `hstore` 外部表示法](hstore.md#HSTORE-EXTERNAL-REP)

    [F.17.2. `hstore` 運算子與函式](hstore.md#HSTORE-OPS-FUNCS)

    [F.17.3. 索引](hstore.md#HSTORE-INDEXES)

    [F.17.4. 範例](hstore.md#HSTORE-EXAMPLES)

    [F.17.5. 統計資訊](hstore.md#HSTORE-STATISTICS)

    [F.17.6. 相容性](hstore.md#HSTORE-COMPATIBILITY)

    [F.17.7. 轉換](hstore.md#HSTORE-TRANSFORMS)

    [F.17.8. 作者](hstore.md#HSTORE-AUTHORS)

[F.18. intagg — 整數彙總器與列舉器](intagg.md)
:   [F.18.1. 函式](intagg.md#INTAGG-FUNCTIONS)

    [F.18.2. 使用範例](intagg.md#INTAGG-SAMPLES)

[F.19. intarray — 操作整數陣列](intarray.md)
:   [F.19.1. `intarray` 函式與運算子](intarray.md#INTARRAY-FUNCS-OPS)

    [F.19.2. 索引支援](intarray.md#INTARRAY-INDEX)

    [F.19.3. 範例](intarray.md#INTARRAY-EXAMPLE)

    [F.19.4. 效能測試](intarray.md#INTARRAY-BENCHMARK)

    [F.19.5. 作者](intarray.md#INTARRAY-AUTHORS)

[F.20. isn — 國際標準號碼（ISBN、EAN、UPC 等）的資料型別](isn.md)
:   [F.20.1. 資料型別](isn.md#ISN-DATA-TYPES)

    [F.20.2. 型別轉換](isn.md#ISN-CASTS)

    [F.20.3. 函式與運算子](isn.md#ISN-FUNCS-OPS)

    [F.20.4. 設定參數](isn.md#ISN-CONFIGURATION-PARAMETERS)

    [F.20.5. 範例](isn.md#ISN-EXAMPLES)

    [F.20.6. 參考書目](isn.md#ISN-BIBLIOGRAPHY)

    [F.20.7. 作者](isn.md#ISN-AUTHOR)

[F.21. lo — 管理大型物件](lo.md)
:   [F.21.1. 原理](lo.md#LO-RATIONALE)

    [F.21.2. 使用方式](lo.md#LO-HOW-TO-USE)

    [F.21.3. 限制](lo.md#LO-LIMITATIONS)

    [F.21.4. 作者](lo.md#LO-AUTHOR)

[F.22. ltree — 階層式樹狀資料型別](ltree.md)
:   [F.22.1. 定義](ltree.md#LTREE-DEFINITIONS)

    [F.22.2. 運算子與函式](ltree.md#LTREE-OPS-FUNCS)

    [F.22.3. 索引](ltree.md#LTREE-INDEXES)

    [F.22.4. 範例](ltree.md#LTREE-EXAMPLE)

    [F.22.5. 轉換](ltree.md#LTREE-TRANSFORMS)

    [F.22.6. 作者](ltree.md#LTREE-AUTHORS)

[F.23. pageinspect — 資料庫頁面的低階檢查](pageinspect.md)
:   [F.23.1. 一般函式](pageinspect.md#PAGEINSPECT-GENERAL-FUNCS)

    [F.23.2. 堆積函式](pageinspect.md#PAGEINSPECT-HEAP-FUNCS)

    [F.23.3. B-tree 函式](pageinspect.md#PAGEINSPECT-B-TREE-FUNCS)

    [F.23.4. BRIN 函式](pageinspect.md#PAGEINSPECT-BRIN-FUNCS)

    [F.23.5. GIN 函式](pageinspect.md#PAGEINSPECT-GIN-FUNCS)

    [F.23.6. GiST 函式](pageinspect.md#PAGEINSPECT-GIST-FUNCS)

    [F.23.7. 雜湊函式](pageinspect.md#PAGEINSPECT-HASH-FUNCS)

[F.24. passwordcheck — 驗證密碼強度](passwordcheck.md)
:   [F.24.1. 設定參數](passwordcheck.md#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

[F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態](pgbuffercache.md)
:   [F.25.1. `pg_buffercache` 檢視表](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE)

    [F.25.2. `pg_buffercache_numa` 檢視表](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)

    [F.25.3. `pg_buffercache_summary()` 函式](pgbuffercache.md#PGBUFFERCACHE-SUMMARY)

    [F.25.4. `pg_buffercache_usage_counts()` 函式](pgbuffercache.md#PGBUFFERCACHE-USAGE-COUNTS)

    [F.25.5. `pg_buffercache_evict()` 函式](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)

    [F.25.6. `pg_buffercache_evict_relation()` 函式](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)

    [F.25.7. `pg_buffercache_evict_all()` 函式](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)

    [F.25.8. 輸出範例](pgbuffercache.md#PGBUFFERCACHE-SAMPLE-OUTPUT)

    [F.25.9. 作者](pgbuffercache.md#PGBUFFERCACHE-AUTHORS)

[F.26. pgcrypto — 加密函式](pgcrypto.md)
:   [F.26.1. 一般雜湊函式](pgcrypto.md#PGCRYPTO-GENERAL-HASHING-FUNCS)

    [F.26.2. 密碼雜湊函式](pgcrypto.md#PGCRYPTO-PASSWORD-HASHING-FUNCS)

    [F.26.3. PGP 加密函式](pgcrypto.md#PGCRYPTO-PGP-ENC-FUNCS)

    [F.26.4. 原始加密函式](pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS)

    [F.26.5. 隨機資料函式](pgcrypto.md#PGCRYPTO-RANDOM-DATA-FUNCS)

    [F.26.6. OpenSSL 支援函式](pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)

    [F.26.7. 設定參數](pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS)

    [F.26.8. 注意事項](pgcrypto.md#PGCRYPTO-NOTES)

    [F.26.9. 作者](pgcrypto.md#PGCRYPTO-AUTHOR)

[F.27. pg_freespacemap — 檢視可用空間對應表](pgfreespacemap.md)
:   [F.27.1. 函式](pgfreespacemap.md#PGFREESPACEMAP-FUNCS)

    [F.27.2. 輸出範例](pgfreespacemap.md#PGFREESPACEMAP-SAMPLE-OUTPUT)

    [F.27.3. 作者](pgfreespacemap.md#PGFREESPACEMAP-AUTHOR)

[F.28. pg_logicalinspect — 邏輯解碼元件檢查](pglogicalinspect.md)
:   [F.28.1. 函式](pglogicalinspect.md#PGLOGICALINSPECT-FUNCS)

    [F.28.2. 作者](pglogicalinspect.md#PGLOGICALINSPECT-AUTHOR)

[F.29. pg_overexplain — 允許 EXPLAIN 傾印更多細節](pgoverexplain.md)
:   [F.29.1. EXPLAIN (DEBUG)](pgoverexplain.md#PGOVEREXPLAIN-DEBUG)

    [F.29.2. EXPLAIN (RANGE_TABLE)](pgoverexplain.md#PGOVEREXPLAIN-RANGE-TABLE)

    [F.29.3. 作者](pgoverexplain.md#PGOVEREXPLAIN-AUTHOR)

[F.30. pg_prewarm — 將關聯資料預先載入緩衝區快取](pgprewarm.md)
:   [F.30.1. 函式](pgprewarm.md#PGPREWARM-FUNCS)

    [F.30.2. 設定參數](pgprewarm.md#PGPREWARM-CONFIG-PARAMS)

    [F.30.3. 作者](pgprewarm.md#PGPREWARM-AUTHOR)

[F.31. pgrowlocks — 顯示資料表的資料列鎖定資訊](pgrowlocks.md)
:   [F.31.1. 概觀](pgrowlocks.md#PGROWLOCKS-OVERVIEW)

    [F.31.2. 輸出範例](pgrowlocks.md#PGROWLOCKS-SAMPLE-OUTPUT)

    [F.31.3. 作者](pgrowlocks.md#PGROWLOCKS-AUTHOR)

[F.32. pg_stat_statements — 追蹤 SQL 規劃與執行的統計資訊](pgstatstatements.md)
:   [F.32.1. `pg_stat_statements` 檢視表](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)

    [F.32.2. `pg_stat_statements_info` 檢視表](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)

    [F.32.3. 函式](pgstatstatements.md#PGSTATSTATEMENTS-FUNCS)

    [F.32.4. 設定參數](pgstatstatements.md#PGSTATSTATEMENTS-CONFIG-PARAMS)

    [F.32.5. 輸出範例](pgstatstatements.md#PGSTATSTATEMENTS-SAMPLE-OUTPUT)

    [F.32.6. 作者](pgstatstatements.md#PGSTATSTATEMENTS-AUTHORS)

[F.33. pgstattuple — 取得 tuple 層級的統計資訊](pgstattuple.md)
:   [F.33.1. 函式](pgstattuple.md#PGSTATTUPLE-FUNCS)

    [F.33.2. 作者](pgstattuple.md#PGSTATTUPLE-AUTHORS)

[F.34. pg_surgery — 對關聯資料執行低階修復](pgsurgery.md)
:   [F.34.1. 函式](pgsurgery.md#PGSURGERY-FUNCS)

    [F.34.2. 作者](pgsurgery.md#PGSURGERY-AUTHORS)

[F.35. pg_trgm — 支援以三元組比對文字相似度](pgtrgm.md)
:   [F.35.1. 三元組（或三字圖）概念](pgtrgm.md#PGTRGM-CONCEPTS)

    [F.35.2. 函式與運算子](pgtrgm.md#PGTRGM-FUNCS-OPS)

    [F.35.3. GUC 參數](pgtrgm.md#PGTRGM-GUC)

    [F.35.4. 索引支援](pgtrgm.md#PGTRGM-INDEX)

    [F.35.5. 文字檢索整合](pgtrgm.md#PGTRGM-TEXT-SEARCH)

    [F.35.6. 參考資料](pgtrgm.md#PGTRGM-REFERENCES)

    [F.35.7. 作者](pgtrgm.md#PGTRGM-AUTHORS)

[F.36. pg_visibility — 可見性對應表資訊與工具](pgvisibility.md)
:   [F.36.1. 函式](pgvisibility.md#PGVISIBILITY-FUNCS)

    [F.36.2. 作者](pgvisibility.md#PGVISIBILITY-AUTHOR)

[F.37. pg_walinspect — WAL 低階檢查](pgwalinspect.md)
:   [F.37.1. 一般函式](pgwalinspect.md#PGWALINSPECT-FUNCS)

    [F.37.2. 作者](pgwalinspect.md#PGWALINSPECT-AUTHOR)

[F.38. postgres_fdw — 存取外部 PostgreSQL 伺服器中的資料](postgres-fdw.md)
:   [F.38.1. postgres_fdw 的 FDW 選項](postgres-fdw.md#POSTGRES-FDW-OPTIONS)

    [F.38.2. 函式](postgres-fdw.md#POSTGRES-FDW-FUNCTIONS)

    [F.38.3. 連線管理](postgres-fdw.md#POSTGRES-FDW-CONNECTION-MANAGEMENT)

    [F.38.4. 交易管理](postgres-fdw.md#POSTGRES-FDW-TRANSACTION-MANAGEMENT)

    [F.38.5. 遠端查詢最佳化](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION)

    [F.38.6. 遠端查詢執行環境](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT)

    [F.38.7. 跨版本相容性](postgres-fdw.md#POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY)

    [F.38.8. 等待事件](postgres-fdw.md#POSTGRES-FDW-WAIT-EVENTS)

    [F.38.9. 設定參數](postgres-fdw.md#POSTGRES-FDW-CONFIGURATION-PARAMETERS)

    [F.38.10. 範例](postgres-fdw.md#POSTGRES-FDW-EXAMPLES)

    [F.38.11. 作者](postgres-fdw.md#POSTGRES-FDW-AUTHOR)

[F.39. seg — 線段或浮點數區間的資料型別](seg.md)
:   [F.39.1. 原理](seg.md#SEG-RATIONALE)

    [F.39.2. 語法](seg.md#SEG-SYNTAX)

    [F.39.3. 精確度](seg.md#SEG-PRECISION)

    [F.39.4. 用法](seg.md#SEG-USAGE)

    [F.39.5. 注意事項](seg.md#SEG-NOTES)

    [F.39.6. 鳴謝](seg.md#SEG-CREDITS)

[F.40. sepgsql — 以 SELinux 標籤為基礎的強制存取控制（MAC）安全模組](sepgsql.md)
:   [F.40.1. 概觀](sepgsql.md#SEPGSQL-OVERVIEW)

    [F.40.2. 安裝](sepgsql.md#SEPGSQL-INSTALLATION)

    [F.40.3. 迴歸測試](sepgsql.md#SEPGSQL-REGRESSION)

    [F.40.4. GUC 參數](sepgsql.md#SEPGSQL-PARAMETERS)

    [F.40.5. 功能](sepgsql.md#SEPGSQL-FEATURES)

    [F.40.6. Sepgsql 函式](sepgsql.md#SEPGSQL-FUNCTIONS)

    [F.40.7. 限制](sepgsql.md#SEPGSQL-LIMITATIONS)

    [F.40.8. 外部資源](sepgsql.md#SEPGSQL-RESOURCES)

    [F.40.9. 作者](sepgsql.md#SEPGSQL-AUTHOR)

[F.41. spi — 伺服器程式設計介面功能與範例](contrib-spi.md)
:   [F.41.1. refint — 實作參照完整性的函式](contrib-spi.md#CONTRIB-SPI-REFINT)

    [F.41.2. autoinc — 用於欄位自動遞增的函式](contrib-spi.md#CONTRIB-SPI-AUTOINC)

    [F.41.3. insert_username — 追蹤資料表變更者的函式](contrib-spi.md#CONTRIB-SPI-INSERT-USERNAME)

    [F.41.4. moddatetime — 追蹤最後修改時間的函式](contrib-spi.md#CONTRIB-SPI-MODDATETIME)

[F.42. sslinfo — 取得用戶端 SSL 資訊](sslinfo.md)
:   [F.42.1. 提供的函式](sslinfo.md#SSLINFO-FUNCTIONS)

    [F.42.2. 作者](sslinfo.md#SSLINFO-AUTHOR)

[F.43. tablefunc — 傳回資料表的函式（`crosstab` 等）](tablefunc.md)
:   [F.43.1. 提供的函式](tablefunc.md#TABLEFUNC-FUNCTIONS-SECT)

    [F.43.2. 作者](tablefunc.md#TABLEFUNC-AUTHOR)

[F.44. tcn — 通知監聽者資料表內容變更的觸發程序函式](tcn.md)

[F.45. test_decoding — 以 SQL 為基礎的 WAL 邏輯解碼測試／範例模組](test-decoding.md)

[F.46. tsm_system_rows — `TABLESAMPLE` 的 `SYSTEM_ROWS` 取樣方法](tsm-system-rows.md)
:   [F.46.1. 範例](tsm-system-rows.md#TSM-SYSTEM-ROWS-EXAMPLES)

[F.47. tsm_system_time — `TABLESAMPLE` 的 `SYSTEM_TIME` 取樣方法](tsm-system-time.md)
:   [F.47.1. 範例](tsm-system-time.md#TSM-SYSTEM-TIME-EXAMPLES)

[F.48. unaccent — 移除變音符號的文字檢索字典](unaccent.md)
:   [F.48.1. 設定](unaccent.md#UNACCENT-CONFIGURATION)

    [F.48.2. 用法](unaccent.md#UNACCENT-USAGE)

    [F.48.3. 函式](unaccent.md#UNACCENT-FUNCTIONS)

[F.49. uuid-ossp — UUID 產生器](uuid-ossp.md)
:   [F.49.1. `uuid-ossp` 函式](uuid-ossp.md#UUID-OSSP-FUNCTIONS-SECT)

    [F.49.2. 建置 `uuid-ossp`](uuid-ossp.md#UUID-OSSP-BUILDING)

    [F.49.3. 作者](uuid-ossp.md#UUID-OSSP-AUTHOR)

[F.50. xml2 — XPath 查詢與 XSLT 功能](xml2.md)
:   [F.50.1. 淘汰通知](xml2.md#XML2-DEPRECATION)

    [F.50.2. 函式說明](xml2.md#XML2-FUNCTIONS)

    [F.50.3. `xpath_table`](xml2.md#XML2-XPATH-TABLE)

    [F.50.4. XSLT 函式](xml2.md#XML2-XSLT)

    [F.50.5. 作者](xml2.md#XML2-AUTHOR)

本附錄及下一個附錄包含 PostgreSQL 發行版 `contrib` 目錄中選用元件的資訊。這些元件包括移植工具、分析公用程式及非核心 PostgreSQL 系統一部分的外掛功能。它們獨立提供，主要是因為其適用對象有限，或實驗性太高而不宜納入主要原始碼樹；這不表示它們沒有用處。

本附錄涵蓋 `contrib` 中的擴充功能及其他伺服器外掛模組程式庫。[附錄 G](../contrib-prog/README.md) 則涵蓋工具程式。

從原始碼發行版建置時，除非建置「world」目標（請參閱[步驟 2](../../server-administration/installation/install-make.md#BUILD)），否則不會自動建置這些選用元件。你可以執行下列命令以建置及安裝所有元件：

```

make
make install
```

請在已設定原始碼樹的 `contrib` 目錄中執行；或者只要建置及安裝某一個選定模組，請在該模組的子目錄中執行相同命令。許多模組提供迴歸測試，可在安裝前執行：

```

make check
```

或在安裝完成、且 PostgreSQL 伺服器已執行後，執行：

```

make installcheck
```


如果使用預先封裝的 PostgreSQL 版本，這些元件通常會以獨立子套件提供，例如 `postgresql-contrib`。

許多元件會提供新的使用者定義函式、運算子或型別，並封裝為*擴充功能*。若要使用其中一個擴充功能，安裝程式碼後，必須在資料庫系統中登錄新的 SQL 物件。請執行 [CREATE EXTENSION](../../reference/sql-commands/sql-createextension.md) 指令。在新建立的資料庫中，只要執行：

```

CREATE EXTENSION extension_name;
```

此指令只會在目前資料庫中登錄新的 SQL 物件，因此必須在每個需要使用擴充功能的資料庫中執行。或者，可在資料庫 `template1` 中執行，讓擴充功能預設複製到之後建立的資料庫中。

除非擴充功能被視為「受信任」，否則所有擴充功能的 `CREATE EXTENSION` 指令都必須由資料庫超級使用者執行。受信任擴充功能可由在目前資料庫中具有 `CREATE` 權限的任何使用者執行。下列章節會標示哪些擴充功能受信任。一般而言，受信任擴充功能是不會提供資料庫外部功能存取權的擴充功能。

<a id="CONTRIB-TRUSTED-EXTENSIONS"></a>

在預設安裝中，下列擴充功能受信任：

<table border="0" class="simplelist" summary="Simple list"><tr><td><a class="xref" href="btree-gin.md">btree_gin</a></td><td><a class="xref" href="fuzzystrmatch.md">fuzzystrmatch</a></td><td><a class="xref" href="ltree.md">ltree</a></td><td><a class="xref" href="tcn.md">tcn</a></td></tr><tr><td><a class="xref" href="btree-gist.md">btree_gist</a></td><td><a class="xref" href="hstore.md">hstore</a></td><td><a class="xref" href="pgcrypto.md">pgcrypto</a></td><td><a class="xref" href="tsm-system-rows.md">tsm_system_rows</a></td></tr><tr><td><a class="xref" href="citext.md">citext</a></td><td><a class="xref" href="intarray.md">intarray</a></td><td><a class="xref" href="pgtrgm.md">pg_trgm</a></td><td><a class="xref" href="tsm-system-time.md">tsm_system_time</a></td></tr><tr><td><a class="xref" href="cube.md">cube</a></td><td><a class="xref" href="isn.md">isn</a></td><td><a class="xref" href="seg.md">seg</a></td><td><a class="xref" href="unaccent.md">unaccent</a></td></tr><tr><td><a class="xref" href="dict-int.md">dict_int</a></td><td><a class="xref" href="lo.md">lo</a></td><td><a class="xref" href="tablefunc.md">tablefunc</a></td><td><a class="xref" href="uuid-ossp.md">uuid-ossp</a></td></tr></table>

許多擴充功能允許你將其物件安裝在自行選擇的 schema 中。若要這麼做，請在 `CREATE EXTENSION` 指令中加入 `SCHEMA schema_name`。預設會將物件置於目前的建立目標 schema，而該 schema 預設為 `public`。

但請注意，其中某些元件並非此處所稱的「擴充功能」，而是透過其他方式載入伺服器，例如透過 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)。詳情請參閱各元件的文件。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib.html)
