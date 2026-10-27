<a id="FUNCTIONS"></a>

## 第 9 章 函式與運算子

**目錄**

- [9.1. 邏輯運算子](functions-logical.md)

- [9.2. 比較函式與運算子](functions-comparison.md)

- [9.3. 數學函式與運算子](functions-math.md)

- [9.4. 字串函式與運算子](functions-string.md)
  - [9.4.1. `format`](functions-string.md#functions-string-format)

- [9.5. 二進位字串函式與運算子](functions-binarystring.md)

- [9.6. 位元字串函式與運算子](functions-bitstring.md)

- [9.7. 模式比對](functions-matching.md)
  - [9.7.1. `LIKE`](functions-matching.md#functions-like)

  - [9.7.2. `SIMILAR TO` 正規表示式](functions-matching.md#functions-similarto-regexp)

  - [9.7.3. POSIX 正規表示式](functions-matching.md#functions-posix-regexp)

- [9.8. 資料型別格式化函式](functions-formatting.md)

- [9.9. 日期／時間函式與運算子](functions-datetime.md)
  - [9.9.1. `EXTRACT`、`date_part`](functions-datetime.md#functions-datetime-extract)

  - [9.9.2. `date_trunc`](functions-datetime.md#functions-datetime-trunc)

  - [9.9.3. `date_bin`](functions-datetime.md#functions-datetime-bin)

  - [9.9.4. `AT TIME ZONE` 與 `AT LOCAL`](functions-datetime.md#functions-datetime-zoneconvert)

  - [9.9.5. 目前日期／時間](functions-datetime.md#functions-datetime-current)

  - [9.9.6. 延遲執行](functions-datetime.md#functions-datetime-delay)

- [9.10. 列舉支援函式](functions-enum.md)

- [9.11. 幾何函式與運算子](functions-geometry.md)

- [9.12. 網路位址函式與運算子](functions-net.md)

- [9.13. 文字搜尋函式與運算子](functions-textsearch.md)

- [9.14. UUID 函式](functions-uuid.md)

- [9.15. XML 函式](functions-xml.md)
  - [9.15.1. 產生 XML 內容](functions-xml.md#functions-producing-xml)

  - [9.15.2. XML 述詞](functions-xml.md#functions-xml-predicates)

  - [9.15.3. 處理 XML](functions-xml.md#functions-xml-processing)

  - [9.15.4. 將資料表對應到 XML](functions-xml.md#functions-xml-mapping)

- [9.16. JSON 函式與運算子](functions-json.md)
  - [9.16.1. 處理與建立 JSON 資料](functions-json.md#functions-json-processing)

  - [9.16.2. SQL/JSON 路徑語言](functions-json.md#functions-sqljson-path)

  - [9.16.3. SQL/JSON 查詢函式](functions-json.md#sqljson-query-functions)

  - [9.16.4. JSON_TABLE](functions-json.md#functions-sqljson-table)

- [9.17. 序列操作函式](functions-sequence.md)

- [9.18. 條件運算式](functions-conditional.md)
  - [9.18.1. `CASE`](functions-conditional.md#functions-case)

  - [9.18.2. `COALESCE`](functions-conditional.md#functions-coalesce-nvl-ifnull)

  - [9.18.3. `NULLIF`](functions-conditional.md#functions-nullif)

  - [9.18.4. `GREATEST` 與 `LEAST`](functions-conditional.md#functions-greatest-least)

- [9.19. 陣列函式與運算子](functions-array.md)

- [9.20. 範圍／多重範圍函式與運算子](functions-range.md)

- [9.21. 彙總函式](functions-aggregate.md)

- [9.22. Window 函式](functions-window.md)

- [9.23. 合併支援函式](functions-merge-support.md)

- [9.24. 子查詢運算式](functions-subquery.md)
  - [9.24.1. `EXISTS`](functions-subquery.md#functions-subquery-exists)

  - [9.24.2. `IN`](functions-subquery.md#functions-subquery-in)

  - [9.24.3. `NOT IN`](functions-subquery.md#functions-subquery-notin)

  - [9.24.4. `ANY`/`SOME`](functions-subquery.md#functions-subquery-any-some)

  - [9.24.5. `ALL`](functions-subquery.md#functions-subquery-all)

  - [9.24.6. 單列比較](functions-subquery.md#functions-subquery-single-row-comp)

- [9.25. 資料列與陣列比較](functions-comparisons.md)
  - [9.25.1. `IN`](functions-comparisons.md#functions-comparisons-in-scalar)

  - [9.25.2. `NOT IN`](functions-comparisons.md#functions-comparisons-not-in)

  - [9.25.3. `ANY`/`SOME`（陣列）](functions-comparisons.md#functions-comparisons-any-some)

  - [9.25.4. `ALL`（陣列）](functions-comparisons.md#functions-comparisons-all)

  - [9.25.5. 資料列建構子比較](functions-comparisons.md#row-wise-comparison)

  - [9.25.6. 複合型別比較](functions-comparisons.md#composite-type-comparison)

- [9.26. 集合回傳函式](functions-srf.md)

- [9.27. 系統資訊函式與運算子](functions-info.md)
  - [9.27.1. 工作階段資訊函式](functions-info.md#functions-info-session)

  - [9.27.2. 存取權限查詢函式](functions-info.md#functions-info-access)

  - [9.27.3. 綱要可見性查詢函式](functions-info.md#functions-info-schema)

  - [9.27.4. 系統目錄資訊函式](functions-info.md#functions-info-catalog)

  - [9.27.5. 物件資訊與定址函式](functions-info.md#functions-info-object)

  - [9.27.6. 註解資訊函式](functions-info.md#functions-info-comment)

  - [9.27.7. 資料有效性檢查函式](functions-info.md#functions-info-validity)

  - [9.27.8. 交易 ID 與快照資訊函式](functions-info.md#functions-info-snapshot)

  - [9.27.9. 已提交交易資訊函式](functions-info.md#functions-info-commit-timestamp)

  - [9.27.10. 控制資料函式](functions-info.md#functions-info-controldata)

  - [9.27.11. 版本資訊函式](functions-info.md#functions-info-version)

  - [9.27.12. WAL 摘要資訊函式](functions-info.md#functions-info-wal-summary)

- [9.28. 系統管理函式](functions-admin.md)
  - [9.28.1. 組態設定函式](functions-admin.md#functions-admin-set)

  - [9.28.2. 伺服器訊號函式](functions-admin.md#functions-admin-signal)

  - [9.28.3. 備份控制函式](functions-admin.md#functions-admin-backup)

  - [9.28.4. 復原控制函式](functions-admin.md#functions-recovery-control)

  - [9.28.5. 快照同步函式](functions-admin.md#functions-snapshot-synchronization)

  - [9.28.6. 複寫管理函式](functions-admin.md#functions-replication)

  - [9.28.7. 資料庫物件管理函式](functions-admin.md#functions-admin-dbobject)

  - [9.28.8. 索引維護函式](functions-admin.md#functions-admin-index)

  - [9.28.9. 通用檔案存取函式](functions-admin.md#functions-admin-genfile)

  - [9.28.10. 諮詢鎖定函式](functions-admin.md#functions-advisory-locks)

- [9.29. 觸發程序函式](functions-trigger.md)

- [9.30. 事件觸發程序函式](functions-event-triggers.md)
  - [9.30.1. 在命令結束時擷取變更](functions-event-triggers.md#pg-event-trigger-ddl-command-end-functions)

  - [9.30.2. 處理被 DDL 命令刪除的物件](functions-event-triggers.md#pg-event-trigger-sql-drop-functions)

  - [9.30.3. 處理資料表改寫事件](functions-event-triggers.md#pg-event-trigger-table-rewrite-functions)

- [9.31. 統計資訊函式](functions-statistics.md)
  - [9.31.1. 檢視 MCV 清單](functions-statistics.md#functions-statistics-mcv)

<a id="id-1.5.8.2"></a><a id="id-1.5.8.3"></a>

PostgreSQL 為內建資料型別提供了大量的函式與運算子。本章說明其中大部分，不過另外還有一些特殊用途的函式，會出現在手冊的相關章節中。使用者也可以定義自己的函式與運算子，如[第五部](../../server-programming/README.md)所述。psql 命令 `\df` 與 `\do` 可以分別用來列出所有可用的函式與運算子。

本章用來描述函式或運算子之引數與結果資料型別的表示法如下：

```

repeat ( text, integer ) → text
```

這表示函式 `repeat` 接受一個 text 引數與一個 integer 引數，並回傳 text 型別的結果。右箭頭也用來表示範例的結果，例如：

```

repeat('Pg', 4) → PgPgPgPg
```

如果你在意可攜性，請注意，本章所說明的大部分函式與運算子，除了最基本的算術與比較運算子以及一些有明確標示的函式之外，都不是 SQL 標準所規定的。這些擴充功能中有些也存在於其他 SQL 資料庫管理系統中，而且在許多情況下，這些功能在各種實作之間是相容且一致的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions.html)（原文版本：18.6；核對日期：2026-09-11）
