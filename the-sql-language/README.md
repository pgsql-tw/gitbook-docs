# 第二部分：SQL 語言

<a id="id-1.5.2"></a>

本部分說明如何在 PostgreSQL 中使用 SQL 語言。我們先介紹 SQL 的一般語法，接著說明如何建立資料表、如何將資料填入資料庫，以及如何查詢資料庫。中間的章節列出可在 SQL 指令中使用的資料型別與函式。最後，我們會探討幾個對於調校資料庫而言相當重要的面向。

這些資訊的編排方式，讓初學者可以從頭讀到尾，在不需要太常往前查閱的情況下完整理解各個主題。各章也力求自成一體，因此進階使用者可以依自己的需要單獨閱讀某一章。內容以敘述的形式依主題單元呈現。想要查閱某個指令完整說明的讀者，建議參閱[第六部分](../reference/README.md)。

讀者應該知道如何連線到 PostgreSQL 資料庫並發出 SQL 指令。對這些事情還不熟悉的讀者，建議先閱讀[第一部分](../tutorial/README.md)。SQL 指令通常是使用 PostgreSQL 的互動式終端機程式 psql 輸入的，但也可以使用其他具有類似功能的程式。

**目錄**

[4. SQL 語法](sql-syntax/README.md)
:   [4.1. 詞彙結構](sql-syntax/sql-syntax-lexical.md)

    [4.2. 值運算式](sql-syntax/sql-expressions.md)

    [4.3. 呼叫函式](sql-syntax/sql-syntax-calling-funcs.md)

[5. 資料定義](ddl/README.md)
:   [5.1. 資料表基礎](ddl/ddl-basics.md)

    [5.2. 預設值](ddl/ddl-default.md)

    [5.3. 識別欄位](ddl/ddl-identity-columns.md)

    [5.4. 產生欄位](ddl/ddl-generated-columns.md)

    [5.5. 限制條件](ddl/ddl-constraints.md)

    [5.6. 系統欄位](ddl/ddl-system-columns.md)

    [5.7. 修改資料表](ddl/ddl-alter.md)

    [5.8. 權限](ddl/ddl-priv.md)

    [5.9. 資料列安全政策](ddl/ddl-rowsecurity.md)

    [5.10. 綱要](ddl/ddl-schemas.md)

    [5.11. 繼承](ddl/ddl-inherit.md)

    [5.12. 資料表分割](ddl/ddl-partitioning.md)

    [5.13. 外部資料](ddl/ddl-foreign-data.md)

    [5.14. 其他資料庫物件](ddl/ddl-others.md)

    [5.15. 相依性追蹤](ddl/ddl-depend.md)

[6. 資料操作](dml/README.md)
:   [6.1. 插入資料](dml/dml-insert.md)

    [6.2. 更新資料](dml/dml-update.md)

    [6.3. 刪除資料](dml/dml-delete.md)

    [6.4. 從修改的資料列回傳資料](dml/dml-returning.md)

[7. 查詢](queries/README.md)
:   [7.1. 概觀](queries/queries-overview.md)

    [7.2. 資料表運算式](queries/queries-table-expressions.md)

    [7.3. 選取清單](queries/queries-select-lists.md)

    [7.4. 組合查詢（`UNION`、`INTERSECT`、`EXCEPT`）](queries/queries-union.md)

    [7.5. 排序資料列（`ORDER BY`）](queries/queries-order.md)

    [7.6. `LIMIT` 與 `OFFSET`](queries/queries-limit.md)

    [7.7. `VALUES` 清單](queries/queries-values.md)

    [7.8. `WITH` 查詢（通用資料表運算式）](queries/queries-with.md)

[8. 資料型別](datatype/README.md)
:   [8.1. 數值型別](datatype/datatype-numeric.md)

    [8.2. 貨幣型別](datatype/datatype-money.md)

    [8.3. 字元型別](datatype/datatype-character.md)

    [8.4. 二進位資料型別](datatype/datatype-binary.md)

    [8.5. 日期／時間型別](datatype/datatype-datetime.md)

    [8.6. 布林型別](datatype/datatype-boolean.md)

    [8.7. 列舉型別](datatype/datatype-enum.md)

    [8.8. 幾何型別](datatype/datatype-geometric.md)

    [8.9. 網路位址型別](datatype/datatype-net-types.md)

    [8.10. 位元字串型別](datatype/datatype-bit.md)

    [8.11. 全文檢索型別](datatype/datatype-textsearch.md)

    [8.12. UUID 型別](datatype/datatype-uuid.md)

    [8.13. XML 型別](datatype/datatype-xml.md)

    [8.14. JSON 型別](datatype/datatype-json.md)

    [8.15. 陣列](datatype/arrays.md)

    [8.16. 複合型別](datatype/rowtypes.md)

    [8.17. 範圍型別](datatype/rangetypes.md)

    [8.18. 網域型別](datatype/domains.md)

    [8.19. 物件識別碼型別](datatype/datatype-oid.md)

    [8.20. `pg_lsn` 型別](datatype/datatype-pg-lsn.md)

    [8.21. 虛擬型別](datatype/datatype-pseudo.md)

[9. 函式與運算子](functions/README.md)
:   [9.1. 邏輯運算子](functions/functions-logical.md)

    [9.2. 比較函式與運算子](functions/functions-comparison.md)

    [9.3. 數學函式與運算子](functions/functions-math.md)

    [9.4. 字串函式與運算子](functions/functions-string.md)

    [9.5. 二進位字串函式與運算子](functions/functions-binarystring.md)

    [9.6. 位元字串函式與運算子](functions/functions-bitstring.md)

    [9.7. 模式比對](functions/functions-matching.md)

    [9.8. 資料型別格式化函式](functions/functions-formatting.md)

    [9.9. 日期／時間函式與運算子](functions/functions-datetime.md)

    [9.10. 列舉支援函式](functions/functions-enum.md)

    [9.11. 幾何函式與運算子](functions/functions-geometry.md)

    [9.12. 網路位址函式與運算子](functions/functions-net.md)

    [9.13. 文字搜尋函式與運算子](functions/functions-textsearch.md)

    [9.14. UUID 函式](functions/functions-uuid.md)

    [9.15. XML 函式](functions/functions-xml.md)

    [9.16. JSON 函式與運算子](functions/functions-json.md)

    [9.17. 序列操作函式](functions/functions-sequence.md)

    [9.18. 條件運算式](functions/functions-conditional.md)

    [9.19. 陣列函式與運算子](functions/functions-array.md)

    [9.20. 範圍／多重範圍函式與運算子](functions/functions-range.md)

    [9.21. 彙總函式](functions/functions-aggregate.md)

    [9.22. Window 函式](functions/functions-window.md)

    [9.23. 合併支援函式](functions/functions-merge-support.md)

    [9.24. 子查詢運算式](functions/functions-subquery.md)

    [9.25. 資料列與陣列比較](functions/functions-comparisons.md)

    [9.26. 集合回傳函式](functions/functions-srf.md)

    [9.27. 系統資訊函式與運算子](functions/functions-info.md)

    [9.28. 系統管理函式](functions/functions-admin.md)

    [9.29. 觸發程序函式](functions/functions-trigger.md)

    [9.30. 事件觸發程序函式](functions/functions-event-triggers.md)

    [9.31. 統計資訊函式](functions/functions-statistics.md)

[10. 型別轉換](typeconv/README.md)
:   [10.1. 概觀](typeconv/typeconv-overview.md)

    [10.2. 運算子](typeconv/typeconv-oper.md)

    [10.3. 函式](typeconv/typeconv-func.md)

    [10.4. 值的儲存](typeconv/typeconv-query.md)

    [10.5. `UNION`、`CASE` 與相關結構](typeconv/typeconv-union-case.md)

    [10.6. `SELECT` 輸出欄位](typeconv/typeconv-select.md)

[11. 索引](indexes/README.md)
:   [11.1. 簡介](indexes/indexes-intro.md)

    [11.2. 索引類型](indexes/indexes-types.md)

    [11.3. 多欄位索引](indexes/indexes-multicolumn.md)

    [11.4. 索引與 `ORDER BY`](indexes/indexes-ordering.md)

    [11.5. 組合多個索引](indexes/indexes-bitmap-scans.md)

    [11.6. 唯一值索引](indexes/indexes-unique.md)

    [11.7. 運算式索引](indexes/indexes-expressional.md)

    [11.8. 部分索引](indexes/indexes-partial.md)

    [11.9. 僅索引掃描與涵蓋索引](indexes/indexes-index-only-scans.md)

    [11.10. 運算子類別與運算子族系](indexes/indexes-opclass.md)

    [11.11. 索引與定序](indexes/indexes-collations.md)

    [11.12. 檢查索引的使用情形](indexes/indexes-examine.md)

[12. 全文檢索](textsearch/README.md)
:   [12.1. 簡介](textsearch/textsearch-intro.md)

    [12.2. 資料表與索引](textsearch/textsearch-tables.md)

    [12.3. 控制文字搜尋](textsearch/textsearch-controls.md)

    [12.4. 其他功能](textsearch/textsearch-features.md)

    [12.5. 剖析器](textsearch/textsearch-parsers.md)

    [12.6. 字典](textsearch/textsearch-dictionaries.md)

    [12.7. 設定範例](textsearch/textsearch-configuration.md)

    [12.8. 測試與除錯文字搜尋](textsearch/textsearch-debugging.md)

    [12.9. 文字搜尋的建議索引型別](textsearch/textsearch-indexes.md)

    [12.10. psql 支援](textsearch/textsearch-psql.md)

    [12.11. 限制](textsearch/textsearch-limitations.md)

[13. 並行控制](mvcc/README.md)
:   [13.1. 簡介](mvcc/mvcc-intro.md)

    [13.2. 交易隔離](mvcc/transaction-iso.md)

    [13.3. 明確鎖定](mvcc/explicit-locking.md)

    [13.4. 應用程式層級的資料一致性檢查](mvcc/applevel-consistency.md)

    [13.5. 序列化失敗的處理](mvcc/mvcc-serialization-failure-handling.md)

    [13.6. 注意事項](mvcc/mvcc-caveats.md)

    [13.7. 鎖定與索引](mvcc/locking-indexes.md)

[14. 效能提示](performance-tips/README.md)
:   [14.1. 使用 `EXPLAIN`](performance-tips/using-explain.md)

    [14.2. 規劃器使用的統計資訊](performance-tips/planner-stats.md)

    [14.3. 以明確的 `JOIN` 子句控制規劃器](performance-tips/explicit-joins.md)

    [14.4. 填入資料庫](performance-tips/populate.md)

    [14.5. 非持久性設定](performance-tips/non-durability.md)

[15. 平行查詢](parallel-query/README.md)
:   [15.1. 平行查詢的運作方式](parallel-query/how-parallel-query-works.md)

    [15.2. 何時可以使用平行查詢？](parallel-query/when-can-parallel-query-be-used.md)

    [15.3. 平行計畫](parallel-query/parallel-plans.md)

    [15.4. 平行安全性](parallel-query/parallel-safety.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql.html)（原文版本：18.6；核對日期：2026-09-13）
