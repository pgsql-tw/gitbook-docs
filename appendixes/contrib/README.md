## 附錄 F：額外提供的模組與擴充功能

**目錄**

- [F.1. amcheck — 驗證資料表與索引一致性的工具](amcheck.md)
  - [F.1.1. 函式](amcheck.md#amcheck-functions)

  - [F.1.2. 選用的 *`heapallindexed`* 驗證](amcheck.md#amcheck-optional-heapallindexed-verification)

  - [F.1.3. 有效使用 `amcheck`](amcheck.md#amcheck-using-amcheck-effectively)

  - [F.1.4. 修復毀損](amcheck.md#amcheck-repairing-corruption)

- [F.2. auth_delay — 驗證失敗時暫停](auth-delay.md)
  - [F.2.1. 設定參數](auth-delay.md#auth-delay-configuration-parameters)

  - [F.2.2. 作者](auth-delay.md#auth-delay-author)

- [F.3. auto_explain — 記錄慢速查詢的執行計畫](auto-explain.md)
  - [F.3.1. 設定參數](auto-explain.md#auto-explain-configuration-parameters)

  - [F.3.2. 範例](auto-explain.md#auto-explain-example)

  - [F.3.3. 作者](auto-explain.md#auto-explain-author)

- [F.4. basebackup_to_shell — 「shell」pg_basebackup 模組範例](basebackup-to-shell.md)
  - [F.4.1. 設定參數](basebackup-to-shell.md#basebackup-to-shell-configuration-parameters)

  - [F.4.2. 作者](basebackup-to-shell.md#basebackup-to-shell-author)

- [F.5. basic_archive — WAL 封存模組範例](basic-archive.md)
  - [F.5.1. 設定參數](basic-archive.md#basic-archive-configuration-parameters)

  - [F.5.2. 注意事項](basic-archive.md#basic-archive-notes)

  - [F.5.3. 作者](basic-archive.md#basic-archive-author)

- [F.6. bloom — Bloom 篩選器索引存取方法](bloom.md)
  - [F.6.1. 參數](bloom.md#bloom-parameters)

  - [F.6.2. 範例](bloom.md#bloom-examples)

  - [F.6.3. 運算子類別介面](bloom.md#bloom-operator-class-interface)

  - [F.6.4. 限制](bloom.md#bloom-limitations)

  - [F.6.5. 作者](bloom.md#bloom-authors)

- [F.7. btree_gin — 具有 B-tree 行為的 GIN 運算子類別](btree-gin.md)
  - [F.7.1. 使用範例](btree-gin.md#btree-gin-example-usage)

  - [F.7.2. 作者](btree-gin.md#btree-gin-authors)

- [F.8. btree_gist — 具有 B-tree 行為的 GiST 運算子類別](btree-gist.md)
  - [F.8.1. 使用範例](btree-gist.md#btree-gist-example-usage)

  - [F.8.2. 作者](btree-gist.md#btree-gist-authors)

- [F.9. citext — 不區分大小寫的字元字串型別](citext.md)
  - [F.9.1. 原理](citext.md#citext-rationale)

  - [F.9.2. 使用方式](citext.md#citext-how-to-use-it)

  - [F.9.3. 字串比較行為](citext.md#citext-string-comparison-behavior)

  - [F.9.4. 限制](citext.md#citext-limitations)

  - [F.9.5. 作者](citext.md#citext-author)

- [F.10. cube — 多維立方體資料型別](cube.md)
  - [F.10.1. 語法](cube.md#cube-syntax)

  - [F.10.2. 精確度](cube.md#cube-precision)

  - [F.10.3. 用法](cube.md#cube-usage)

  - [F.10.4. 預設值](cube.md#cube-defaults)

  - [F.10.5. 注意事項](cube.md#cube-notes)

  - [F.10.6. 鳴謝](cube.md#cube-credits)

- [F.11. dblink — 連線至其他 PostgreSQL 資料庫](dblink.md)
  - [dblink_connect](contrib-dblink-connect.md) — 開啟至遠端資料庫的持續連線

  - [dblink_connect_u](contrib-dblink-connect-u.md) — 以不安全的方式開啟至遠端資料庫的持續連線

  - [dblink_disconnect](contrib-dblink-disconnect.md) — 關閉至遠端資料庫的持續連線

  - [dblink](contrib-dblink-function.md) — 在遠端資料庫中執行查詢

  - [dblink_exec](contrib-dblink-exec.md) — 在遠端資料庫中執行指令

  - [dblink_open](contrib-dblink-open.md) — 在遠端資料庫中開啟游標

  - [dblink_fetch](contrib-dblink-fetch.md) — 傳回遠端資料庫中已開啟游標的資料列

  - [dblink_close](contrib-dblink-close.md) — 關閉遠端資料庫中的游標

  - [dblink_get_connections](contrib-dblink-get-connections.md) — 傳回所有已開啟具名 dblink 連線的名稱

  - [dblink_error_message](contrib-dblink-error-message.md) — 取得具名連線上的最新錯誤訊息

  - [dblink_send_query](contrib-dblink-send-query.md) — 將非同步查詢傳送至遠端資料庫

  - [dblink_is_busy](contrib-dblink-is-busy.md) — 檢查連線是否正忙於非同步查詢

  - [dblink_get_notify](contrib-dblink-get-notify.md) — 擷取連線上的非同步通知

  - [dblink_get_result](contrib-dblink-get-result.md) — 取得非同步查詢結果

  - [dblink_cancel_query](contrib-dblink-cancel-query.md) — 取消具名連線上的任何作用中查詢

  - [dblink_get_pkey](contrib-dblink-get-pkey.md) — 傳回關聯主鍵欄位的位置與欄位名稱

  - [dblink_build_sql_insert](contrib-dblink-build-sql-insert.md) — 使用本機 tuple 建立 INSERT 陳述式，並以提供的替代值取代主鍵欄位值

  - [dblink_build_sql_delete](contrib-dblink-build-sql-delete.md) — 使用提供的主鍵欄位值建立 DELETE 陳述式

  - [dblink_build_sql_update](contrib-dblink-build-sql-update.md) — 使用本機 tuple 建立 UPDATE 陳述式，並以提供的替代值取代主鍵欄位值

- [F.12. dict_int — 整數全文檢索字典範例](dict-int.md)
  - [F.12.1. 設定](dict-int.md#dict-int-config)

  - [F.12.2. 用法](dict-int.md#dict-int-usage)

- [F.13. dict_xsyn — 同義詞全文檢索字典範例](dict-xsyn.md)
  - [F.13.1. 設定](dict-xsyn.md#dict-xsyn-config)

  - [F.13.2. 用法](dict-xsyn.md#dict-xsyn-usage)

- [F.14. earthdistance — 計算大圓距離](earthdistance.md)
  - [F.14.1. 以立方體為基礎的地球距離](earthdistance.md#earthdistance-cube-based)

  - [F.14.2. 以點為基礎的地球距離](earthdistance.md#earthdistance-point-based)

- [F.15. file_fdw — 存取伺服器檔案系統中的資料檔](file-fdw.md)

- [F.16. fuzzystrmatch — 判定字串相似度與距離](fuzzystrmatch.md)
  - [F.16.1. Soundex](fuzzystrmatch.md#fuzzystrmatch-soundex)

  - [F.16.2. Daitch-Mokotoff Soundex](fuzzystrmatch.md#fuzzystrmatch-daitch-mokotoff)

  - [F.16.3. Levenshtein](fuzzystrmatch.md#fuzzystrmatch-levenshtein)

  - [F.16.4. Metaphone](fuzzystrmatch.md#fuzzystrmatch-metaphone)

  - [F.16.5. Double Metaphone](fuzzystrmatch.md#fuzzystrmatch-double-metaphone)

- [F.17. hstore — hstore 索引鍵／值資料型別](hstore.md)
  - [F.17.1. `hstore` 外部表示法](hstore.md#hstore-external-rep)

  - [F.17.2. `hstore` 運算子與函式](hstore.md#hstore-ops-funcs)

  - [F.17.3. 索引](hstore.md#hstore-indexes)

  - [F.17.4. 範例](hstore.md#hstore-examples)

  - [F.17.5. 統計資訊](hstore.md#hstore-statistics)

  - [F.17.6. 相容性](hstore.md#hstore-compatibility)

  - [F.17.7. 轉換](hstore.md#hstore-transforms)

  - [F.17.8. 作者](hstore.md#hstore-authors)

- [F.18. intagg — 整數彙總器與列舉器](intagg.md)
  - [F.18.1. 函式](intagg.md#intagg-functions)

  - [F.18.2. 使用範例](intagg.md#intagg-samples)

- [F.19. intarray — 操作整數陣列](intarray.md)
  - [F.19.1. `intarray` 函式與運算子](intarray.md#intarray-funcs-ops)

  - [F.19.2. 索引支援](intarray.md#intarray-index)

  - [F.19.3. 範例](intarray.md#intarray-example)

  - [F.19.4. 效能測試](intarray.md#intarray-benchmark)

  - [F.19.5. 作者](intarray.md#intarray-authors)

- [F.20. isn — 國際標準號碼（ISBN、EAN、UPC 等）的資料型別](isn.md)
  - [F.20.1. 資料型別](isn.md#isn-data-types)

  - [F.20.2. 型別轉換](isn.md#isn-casts)

  - [F.20.3. 函式與運算子](isn.md#isn-funcs-ops)

  - [F.20.4. 設定參數](isn.md#isn-configuration-parameters)

  - [F.20.5. 範例](isn.md#isn-examples)

  - [F.20.6. 參考書目](isn.md#isn-bibliography)

  - [F.20.7. 作者](isn.md#isn-author)

- [F.21. lo — 管理大型物件](lo.md)
  - [F.21.1. 原理](lo.md#lo-rationale)

  - [F.21.2. 使用方式](lo.md#lo-how-to-use)

  - [F.21.3. 限制](lo.md#lo-limitations)

  - [F.21.4. 作者](lo.md#lo-author)

- [F.22. ltree — 階層式樹狀資料型別](ltree.md)
  - [F.22.1. 定義](ltree.md#ltree-definitions)

  - [F.22.2. 運算子與函式](ltree.md#ltree-ops-funcs)

  - [F.22.3. 索引](ltree.md#ltree-indexes)

  - [F.22.4. 範例](ltree.md#ltree-example)

  - [F.22.5. 轉換](ltree.md#ltree-transforms)

  - [F.22.6. 作者](ltree.md#ltree-authors)

- [F.23. pageinspect — 資料庫頁面的低階檢查](pageinspect.md)
  - [F.23.1. 一般函式](pageinspect.md#pageinspect-general-funcs)

  - [F.23.2. 堆積函式](pageinspect.md#pageinspect-heap-funcs)

  - [F.23.3. B-tree 函式](pageinspect.md#pageinspect-b-tree-funcs)

  - [F.23.4. BRIN 函式](pageinspect.md#pageinspect-brin-funcs)

  - [F.23.5. GIN 函式](pageinspect.md#pageinspect-gin-funcs)

  - [F.23.6. GiST 函式](pageinspect.md#pageinspect-gist-funcs)

  - [F.23.7. 雜湊函式](pageinspect.md#pageinspect-hash-funcs)

- [F.24. passwordcheck — 驗證密碼強度](passwordcheck.md)
  - [F.24.1. 設定參數](passwordcheck.md#passwordcheck-configuration-parameters)

- [F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態](pgbuffercache.md)
  - [F.25.1. `pg_buffercache` 檢視表](pgbuffercache.md#pgbuffercache-pg-buffercache)

  - [F.25.2. `pg_buffercache_numa` 檢視表](pgbuffercache.md#pgbuffercache-pg-buffercache-numa)

  - [F.25.3. `pg_buffercache_summary()` 函式](pgbuffercache.md#pgbuffercache-summary)

  - [F.25.4. `pg_buffercache_usage_counts()` 函式](pgbuffercache.md#pgbuffercache-usage-counts)

  - [F.25.5. `pg_buffercache_evict()` 函式](pgbuffercache.md#pgbuffercache-pg-buffercache-evict)

  - [F.25.6. `pg_buffercache_evict_relation()` 函式](pgbuffercache.md#pgbuffercache-pg-buffercache-evict-relation)

  - [F.25.7. `pg_buffercache_evict_all()` 函式](pgbuffercache.md#pgbuffercache-pg-buffercache-evict-all)

  - [F.25.8. 輸出範例](pgbuffercache.md#pgbuffercache-sample-output)

  - [F.25.9. 作者](pgbuffercache.md#pgbuffercache-authors)

- [F.26. pgcrypto — 加密函式](pgcrypto.md)
  - [F.26.1. 一般雜湊函式](pgcrypto.md#pgcrypto-general-hashing-funcs)

  - [F.26.2. 密碼雜湊函式](pgcrypto.md#pgcrypto-password-hashing-funcs)

  - [F.26.3. PGP 加密函式](pgcrypto.md#pgcrypto-pgp-enc-funcs)

  - [F.26.4. 原始加密函式](pgcrypto.md#pgcrypto-raw-enc-funcs)

  - [F.26.5. 隨機資料函式](pgcrypto.md#pgcrypto-random-data-funcs)

  - [F.26.6. OpenSSL 支援函式](pgcrypto.md#pgcrypto-openssl-support-funcs)

  - [F.26.7. 設定參數](pgcrypto.md#pgcrypto-configuration-parameters)

  - [F.26.8. 注意事項](pgcrypto.md#pgcrypto-notes)

  - [F.26.9. 作者](pgcrypto.md#pgcrypto-author)

- [F.27. pg_freespacemap — 檢視可用空間對應表](pgfreespacemap.md)
  - [F.27.1. 函式](pgfreespacemap.md#pgfreespacemap-funcs)

  - [F.27.2. 輸出範例](pgfreespacemap.md#pgfreespacemap-sample-output)

  - [F.27.3. 作者](pgfreespacemap.md#pgfreespacemap-author)

- [F.28. pg_logicalinspect — 邏輯解碼元件檢查](pglogicalinspect.md)
  - [F.28.1. 函式](pglogicalinspect.md#pglogicalinspect-funcs)

  - [F.28.2. 作者](pglogicalinspect.md#pglogicalinspect-author)

- [F.29. pg_overexplain — 允許 EXPLAIN 傾印更多細節](pgoverexplain.md)
  - [F.29.1. EXPLAIN (DEBUG)](pgoverexplain.md#pgoverexplain-debug)

  - [F.29.2. EXPLAIN (RANGE_TABLE)](pgoverexplain.md#pgoverexplain-range-table)

  - [F.29.3. 作者](pgoverexplain.md#pgoverexplain-author)

- [F.30. pg_prewarm — 將關聯資料預先載入緩衝區快取](pgprewarm.md)
  - [F.30.1. 函式](pgprewarm.md#pgprewarm-funcs)

  - [F.30.2. 設定參數](pgprewarm.md#pgprewarm-config-params)

  - [F.30.3. 作者](pgprewarm.md#pgprewarm-author)

- [F.31. pgrowlocks — 顯示資料表的資料列鎖定資訊](pgrowlocks.md)
  - [F.31.1. 概觀](pgrowlocks.md#pgrowlocks-overview)

  - [F.31.2. 輸出範例](pgrowlocks.md#pgrowlocks-sample-output)

  - [F.31.3. 作者](pgrowlocks.md#pgrowlocks-author)

- [F.32. pg_stat_statements — 追蹤 SQL 規劃與執行的統計資訊](pgstatstatements.md)
  - [F.32.1. `pg_stat_statements` 檢視表](pgstatstatements.md#pgstatstatements-pg-stat-statements)

  - [F.32.2. `pg_stat_statements_info` 檢視表](pgstatstatements.md#pgstatstatements-pg-stat-statements-info)

  - [F.32.3. 函式](pgstatstatements.md#pgstatstatements-funcs)

  - [F.32.4. 設定參數](pgstatstatements.md#pgstatstatements-config-params)

  - [F.32.5. 輸出範例](pgstatstatements.md#pgstatstatements-sample-output)

  - [F.32.6. 作者](pgstatstatements.md#pgstatstatements-authors)

- [F.33. pgstattuple — 取得 tuple 層級的統計資訊](pgstattuple.md)
  - [F.33.1. 函式](pgstattuple.md#pgstattuple-funcs)

  - [F.33.2. 作者](pgstattuple.md#pgstattuple-authors)

- [F.34. pg_surgery — 對關聯資料執行低階修復](pgsurgery.md)
  - [F.34.1. 函式](pgsurgery.md#pgsurgery-funcs)

  - [F.34.2. 作者](pgsurgery.md#pgsurgery-authors)

- [F.35. pg_trgm — 支援以三元組比對文字相似度](pgtrgm.md)
  - [F.35.1. 三元組（或三字圖）概念](pgtrgm.md#pgtrgm-concepts)

  - [F.35.2. 函式與運算子](pgtrgm.md#pgtrgm-funcs-ops)

  - [F.35.3. GUC 參數](pgtrgm.md#pgtrgm-guc)

  - [F.35.4. 索引支援](pgtrgm.md#pgtrgm-index)

  - [F.35.5. 文字檢索整合](pgtrgm.md#pgtrgm-text-search)

  - [F.35.6. 參考資料](pgtrgm.md#pgtrgm-references)

  - [F.35.7. 作者](pgtrgm.md#pgtrgm-authors)

- [F.36. pg_visibility — 可見性對應表資訊與工具](pgvisibility.md)
  - [F.36.1. 函式](pgvisibility.md#pgvisibility-funcs)

  - [F.36.2. 作者](pgvisibility.md#pgvisibility-author)

- [F.37. pg_walinspect — WAL 低階檢查](pgwalinspect.md)
  - [F.37.1. 一般函式](pgwalinspect.md#pgwalinspect-funcs)

  - [F.37.2. 作者](pgwalinspect.md#pgwalinspect-author)

- [F.38. postgres_fdw — 存取外部 PostgreSQL 伺服器中的資料](postgres-fdw.md)
  - [F.38.1. postgres_fdw 的 FDW 選項](postgres-fdw.md#postgres-fdw-options)

  - [F.38.2. 函式](postgres-fdw.md#postgres-fdw-functions)

  - [F.38.3. 連線管理](postgres-fdw.md#postgres-fdw-connection-management)

  - [F.38.4. 交易管理](postgres-fdw.md#postgres-fdw-transaction-management)

  - [F.38.5. 遠端查詢最佳化](postgres-fdw.md#postgres-fdw-remote-query-optimization)

  - [F.38.6. 遠端查詢執行環境](postgres-fdw.md#postgres-fdw-remote-query-execution-environment)

  - [F.38.7. 跨版本相容性](postgres-fdw.md#postgres-fdw-cross-version-compatibility)

  - [F.38.8. 等待事件](postgres-fdw.md#postgres-fdw-wait-events)

  - [F.38.9. 設定參數](postgres-fdw.md#postgres-fdw-configuration-parameters)

  - [F.38.10. 範例](postgres-fdw.md#postgres-fdw-examples)

  - [F.38.11. 作者](postgres-fdw.md#postgres-fdw-author)

- [F.39. seg — 線段或浮點數區間的資料型別](seg.md)
  - [F.39.1. 原理](seg.md#seg-rationale)

  - [F.39.2. 語法](seg.md#seg-syntax)

  - [F.39.3. 精確度](seg.md#seg-precision)

  - [F.39.4. 用法](seg.md#seg-usage)

  - [F.39.5. 注意事項](seg.md#seg-notes)

  - [F.39.6. 鳴謝](seg.md#seg-credits)

- [F.40. sepgsql — 以 SELinux 標籤為基礎的強制存取控制（MAC）安全模組](sepgsql.md)
  - [F.40.1. 概觀](sepgsql.md#sepgsql-overview)

  - [F.40.2. 安裝](sepgsql.md#sepgsql-installation)

  - [F.40.3. 迴歸測試](sepgsql.md#sepgsql-regression)

  - [F.40.4. GUC 參數](sepgsql.md#sepgsql-parameters)

  - [F.40.5. 功能](sepgsql.md#sepgsql-features)

  - [F.40.6. Sepgsql 函式](sepgsql.md#sepgsql-functions)

  - [F.40.7. 限制](sepgsql.md#sepgsql-limitations)

  - [F.40.8. 外部資源](sepgsql.md#sepgsql-resources)

  - [F.40.9. 作者](sepgsql.md#sepgsql-author)

- [F.41. spi — 伺服器程式設計介面功能與範例](contrib-spi.md)
  - [F.41.1. refint — 實作參照完整性的函式](contrib-spi.md#contrib-spi-refint)

  - [F.41.2. autoinc — 用於欄位自動遞增的函式](contrib-spi.md#contrib-spi-autoinc)

  - [F.41.3. insert_username — 追蹤資料表變更者的函式](contrib-spi.md#contrib-spi-insert-username)

  - [F.41.4. moddatetime — 追蹤最後修改時間的函式](contrib-spi.md#contrib-spi-moddatetime)

- [F.42. sslinfo — 取得用戶端 SSL 資訊](sslinfo.md)
  - [F.42.1. 提供的函式](sslinfo.md#sslinfo-functions)

  - [F.42.2. 作者](sslinfo.md#sslinfo-author)

- [F.43. tablefunc — 傳回資料表的函式（`crosstab` 等）](tablefunc.md)
  - [F.43.1. 提供的函式](tablefunc.md#tablefunc-functions-sect)

  - [F.43.2. 作者](tablefunc.md#tablefunc-author)

- [F.44. tcn — 通知監聽者資料表內容變更的觸發程序函式](tcn.md)

- [F.45. test_decoding — 以 SQL 為基礎的 WAL 邏輯解碼測試／範例模組](test-decoding.md)

- [F.46. tsm_system_rows — `TABLESAMPLE` 的 `SYSTEM_ROWS` 取樣方法](tsm-system-rows.md)
  - [F.46.1. 範例](tsm-system-rows.md#tsm-system-rows-examples)

- [F.47. tsm_system_time — `TABLESAMPLE` 的 `SYSTEM_TIME` 取樣方法](tsm-system-time.md)
  - [F.47.1. 範例](tsm-system-time.md#tsm-system-time-examples)

- [F.48. unaccent — 移除變音符號的文字檢索字典](unaccent.md)
  - [F.48.1. 設定](unaccent.md#unaccent-configuration)

  - [F.48.2. 用法](unaccent.md#unaccent-usage)

  - [F.48.3. 函式](unaccent.md#unaccent-functions)

- [F.49. uuid-ossp — UUID 產生器](uuid-ossp.md)
  - [F.49.1. `uuid-ossp` 函式](uuid-ossp.md#uuid-ossp-functions-sect)

  - [F.49.2. 建置 `uuid-ossp`](uuid-ossp.md#uuid-ossp-building)

  - [F.49.3. 作者](uuid-ossp.md#uuid-ossp-author)

- [F.50. xml2 — XPath 查詢與 XSLT 功能](xml2.md)
  - [F.50.1. 淘汰通知](xml2.md#xml2-deprecation)

  - [F.50.2. 函式說明](xml2.md#xml2-functions)

  - [F.50.3. `xpath_table`](xml2.md#xml2-xpath-table)

  - [F.50.4. XSLT 函式](xml2.md#xml2-xslt)

  - [F.50.5. 作者](xml2.md#xml2-author)

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
