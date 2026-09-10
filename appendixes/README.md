# 第八部分：附錄

**目錄**

[A. PostgreSQL 錯誤代碼](errcodes-appendix/README.md)

[B. 日期／時間支援](datetime-appendix/README.md)
:   [B.1. 日期／時間輸入解讀](datetime-appendix/datetime-input-rules.md)

    [B.2. 處理無效或模稜兩可的時間戳記](datetime-appendix/datetime-invalid-input.md)

    [B.3. 日期／時間關鍵字](datetime-appendix/datetime-keywords.md)

    [B.4. 日期／時間設定檔](datetime-appendix/datetime-config-files.md)

    [B.5. POSIX 時區規格](datetime-appendix/datetime-posix-timezone-specs.md)

    [B.6. 單位的歷史](datetime-appendix/datetime-units-history.md)

    [B.7. 儒略日](datetime-appendix/datetime-julian-dates.md)

[C. SQL 關鍵字](sql-keywords-appendix/README.md)

[D. SQL 相容性](features/README.md)
:   [D.1. 支援的功能](features/features-sql-standard.md)

    [D.2. 不支援的功能](features/unsupported-features-sql-standard.md)

    [D.3. XML 限制及對 SQL/XML 的相容性](features/xml-limits-conformance.md)

[E. 版本說明](release/README.md)
:   [E.1. 18.6 版本](release/release-18-6.md)

    [E.2. 18.4 版本](release/release-18-4.md)

    [E.3. 18.3 版本](release/release-18-3.md)

    [E.4. 18.2 版本](release/release-18-2.md)

    [E.5. 18.1 版本](release/release-18-1.md)

    [E.6. 18 版本](release/release-18.md)

    [E.7. 先前版本](release/release-prior.md)

[F. 額外提供的模組與擴充功能](contrib/README.md)
:   [F.1. amcheck — 驗證資料表與索引一致性的工具](contrib/amcheck.md)

    [F.2. auth_delay — 驗證失敗時暫停](contrib/auth-delay.md)

    [F.3. auto_explain — 記錄慢速查詢的執行計畫](contrib/auto-explain.md)

    [F.4. basebackup_to_shell — 「shell」pg_basebackup 模組範例](contrib/basebackup-to-shell.md)

    [F.5. basic_archive — WAL 封存模組範例](contrib/basic-archive.md)

    [F.6. bloom — Bloom 篩選器索引存取方法](contrib/bloom.md)

    [F.7. btree_gin — 具有 B-tree 行為的 GIN 運算子類別](contrib/btree-gin.md)

    [F.8. btree_gist — 具有 B-tree 行為的 GiST 運算子類別](contrib/btree-gist.md)

    [F.9. citext — 不區分大小寫的字元字串型別](contrib/citext.md)

    [F.10. cube — 多維立方體資料型別](contrib/cube.md)

    [F.11. dblink — 連線至其他 PostgreSQL 資料庫](contrib/dblink.md)

    [F.12. dict_int — 整數全文檢索字典範例](contrib/dict-int.md)

    [F.13. dict_xsyn — 同義詞全文檢索字典範例](contrib/dict-xsyn.md)

    [F.14. earthdistance — 計算大圓距離](contrib/earthdistance.md)

    [F.15. file_fdw — 存取伺服器檔案系統中的資料檔](contrib/file-fdw.md)

    [F.16. fuzzystrmatch — 判定字串相似度與距離](contrib/fuzzystrmatch.md)

    [F.17. hstore — hstore 索引鍵／值資料型別](contrib/hstore.md)

    [F.18. intagg — 整數彙總器與列舉器](contrib/intagg.md)

    [F.19. intarray — 操作整數陣列](contrib/intarray.md)

    [F.20. isn — 國際標準號碼（ISBN、EAN、UPC 等）的資料型別](contrib/isn.md)

    [F.21. lo — 管理大型物件](contrib/lo.md)

    [F.22. ltree — 階層式樹狀資料型別](contrib/ltree.md)

    [F.23. pageinspect — 資料庫頁面的低階檢查](contrib/pageinspect.md)

    [F.24. passwordcheck — 驗證密碼強度](contrib/passwordcheck.md)

    [F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態](contrib/pgbuffercache.md)

    [F.26. pgcrypto — 加密函式](contrib/pgcrypto.md)

    [F.27. pg_freespacemap — 檢視可用空間對應表](contrib/pgfreespacemap.md)

    [F.28. pg_logicalinspect — 邏輯解碼元件檢查](contrib/pglogicalinspect.md)

    [F.29. pg_overexplain — 允許 EXPLAIN 傾印更多細節](contrib/pgoverexplain.md)

    [F.30. pg_prewarm — 將關聯資料預先載入緩衝區快取](contrib/pgprewarm.md)

    [F.31. pgrowlocks — 顯示資料表的資料列鎖定資訊](contrib/pgrowlocks.md)

    [F.32. pg_stat_statements — 追蹤 SQL 規劃與執行的統計資訊](contrib/pgstatstatements.md)

    [F.33. pgstattuple — 取得 tuple 層級的統計資訊](contrib/pgstattuple.md)

    [F.34. pg_surgery — 對關聯資料執行低階修復](contrib/pgsurgery.md)

    [F.35. pg_trgm — 支援以三元組比對文字相似度](contrib/pgtrgm.md)

    [F.36. pg_visibility — 可見性對應表資訊與工具](contrib/pgvisibility.md)

    [F.37. pg_walinspect — WAL 低階檢查](contrib/pgwalinspect.md)

    [F.38. postgres_fdw — 存取外部 PostgreSQL 伺服器中的資料](contrib/postgres-fdw.md)

    [F.39. seg — 線段或浮點數區間的資料型別](contrib/seg.md)

    [F.40. sepgsql — 以 SELinux 標籤為基礎的強制存取控制（MAC）安全模組](contrib/sepgsql.md)

    [F.41. spi — 伺服器程式設計介面功能與範例](contrib/contrib-spi.md)

    [F.42. sslinfo — 取得用戶端 SSL 資訊](contrib/sslinfo.md)

    [F.43. tablefunc — 傳回資料表的函式（`crosstab` 等）](contrib/tablefunc.md)

    [F.44. tcn — 通知監聽者資料表內容變更的觸發程序函式](contrib/tcn.md)

    [F.45. test_decoding — 以 SQL 為基礎的 WAL 邏輯解碼測試／範例模組](contrib/test-decoding.md)

    [F.46. tsm_system_rows — `TABLESAMPLE` 的 `SYSTEM_ROWS` 取樣方法](contrib/tsm-system-rows.md)

    [F.47. tsm_system_time — `TABLESAMPLE` 的 `SYSTEM_TIME` 取樣方法](contrib/tsm-system-time.md)

    [F.48. unaccent — 移除變音符號的文字檢索字典](contrib/unaccent.md)

    [F.49. uuid-ossp — UUID 產生器](contrib/uuid-ossp.md)

    [F.50. xml2 — XPath 查詢與 XSLT 功能](contrib/xml2.md)

[G. 額外提供的程式](contrib-prog/README.md)
:   [G.1. 用戶端應用程式](contrib-prog/contrib-prog-client.md)

    [G.2. 伺服器應用程式](contrib-prog/contrib-prog-server.md)

[H. 外部專案](external-projects/README.md)
:   [H.1. 用戶端介面](external-projects/external-interfaces.md)

    [H.2. 管理工具](external-projects/external-admin-tools.md)

    [H.3. 程序語言](external-projects/external-pl.md)

    [H.4. 擴充功能](external-projects/external-extensions.md)

[I. 原始碼儲存庫](sourcerepo/README.md)
:   [I.1. 透過 Git 取得原始碼](sourcerepo/git.md)

[J. 文件](docguide/README.md)
:   [J.1. DocBook](docguide/docguide-docbook.md)

    [J.2. 工具集](docguide/docguide-toolsets.md)

    [J.3. 使用 Make 建置文件](docguide/docguide-build.md)

    [J.4. 使用 Meson 建置文件](docguide/docguide-build-meson.md)

    [J.5. 文件撰寫](docguide/docguide-authoring.md)

    [J.6. 樣式指南](docguide/docguide-style.md)

[K. PostgreSQL 限制](limits/README.md)

[L. 縮寫](acronyms/README.md)

[M. 詞彙表](glossary/README.md)

[N. 色彩支援](color/README.md)
:   [N.1. 使用色彩的時機](color/color-when.md)

    [N.2. 設定色彩](color/color-which.md)

[O. 已淘汰或改名的功能](appendix-obsolete/README.md)
:   [O.1. `recovery.conf` 檔案已併入 `postgresql.conf`](appendix-obsolete/recovery-config.md)

    [O.2. 預設角色已改名為預先定義角色](appendix-obsolete/default-roles.md)

    [O.3. `pg_xlogdump` 已改名為 `pg_waldump`](appendix-obsolete/pgxlogdump.md)

    [O.4. `pg_resetxlog` 已改名為 `pg_resetwal`](appendix-obsolete/app-pgresetxlog.md)

    [O.5. `pg_receivexlog` 已改名為 `pg_receivewal`](appendix-obsolete/app-pgreceivexlog.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/appendixes.html)
