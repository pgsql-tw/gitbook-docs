<a id="ECPG"></a>

## 第 34 章 ECPG — C 語言中的嵌入式 SQL

**目錄**

- [34.1. 概念](ecpg-concept.md)

- [34.2. 管理資料庫連線](ecpg-connect.md)
  - [34.2.1. 連線到資料庫伺服器](ecpg-connect.md#ecpg-connecting)

  - [34.2.2. 選擇連線](ecpg-connect.md#ecpg-set-connection)

  - [34.2.3. 關閉連線](ecpg-connect.md#ecpg-disconnect)

- [34.3. 執行 SQL 命令](ecpg-commands.md)
  - [34.3.1. 執行 SQL 陳述式](ecpg-commands.md#ecpg-executing)

  - [34.3.2. 使用游標](ecpg-commands.md#ecpg-cursors)

  - [34.3.3. 管理交易](ecpg-commands.md#ecpg-transactions)

  - [34.3.4. 預備陳述式](ecpg-commands.md#ecpg-prepared)

- [34.4. 使用主機變數](ecpg-variables.md)
  - [34.4.1. 概觀](ecpg-variables.md#ecpg-variables-overview)

  - [34.4.2. 宣告區段](ecpg-variables.md#ecpg-declare-sections)

  - [34.4.3. 取得查詢結果](ecpg-variables.md#ecpg-retrieving)

  - [34.4.4. 型別對應](ecpg-variables-type-mapping.md#ecpg-variables-type-mapping)
    - [34.4.4.1. 處理字元字串](ecpg-variables-type-mapping.md#ecpg-char)
    - [34.4.4.2. 存取特殊資料型別](ecpg-variables-special-types.md#ecpg-special-types)
      - [34.4.4.2.1. timestamp、date](ecpg-variables-special-types.md#ecpg-special-types-timestamp-date)
      - [34.4.4.2.2. interval](ecpg-variables-special-types.md#ecpg-type-interval)
      - [34.4.4.2.3. numeric、decimal](ecpg-variables-special-types.md#ecpg-type-numeric-decimal)
      - [34.4.4.2.4. bytea](ecpg-variables-special-types.md#ecpg-special-types-bytea)
    - [34.4.4.3. 非基本型別的主機變數](ecpg-variables-nonprimitive-c.md#ecpg-variables-nonprimitive-c)
      - [34.4.4.3.1. 陣列](ecpg-variables-nonprimitive-c.md#ecpg-variables-arrays)
      - [34.4.4.3.2. 結構](ecpg-variables-nonprimitive-c.md#ecpg-variables-struct)
      - [34.4.4.3.3. 型別定義（typedef）](ecpg-variables-nonprimitive-c.md#ecpg-variables-nonprimitive-c-typedefs)
      - [34.4.4.3.4. 指標](ecpg-variables-nonprimitive-c.md#ecpg-variables-nonprimitive-c-pointers)

  - [34.4.5. 處理非基本 SQL 資料型別](ecpg-variables-nonprimitive-sql.md#ecpg-variables-nonprimitive-sql)
    - [34.4.5.1. 陣列](ecpg-variables-nonprimitive-sql.md#ecpg-variables-nonprimitive-sql-arrays)
    - [34.4.5.2. 複合型別](ecpg-variables-nonprimitive-sql.md#ecpg-variables-nonprimitive-sql-composite)
    - [34.4.5.3. 使用者自訂基本型別](ecpg-variables-nonprimitive-sql.md#ecpg-variables-nonprimitive-sql-user-defined-base-types)

  - [34.4.6. 指示變數](ecpg-variables.md#ecpg-indicators)

- [34.5. 動態 SQL](ecpg-dynamic.md)
  - [34.5.1. 執行不傳回結果集的陳述式](ecpg-dynamic.md#ecpg-dynamic-without-result)

  - [34.5.2. 執行帶有輸入參數的陳述式](ecpg-dynamic.md#ecpg-dynamic-input)

  - [34.5.3. 執行傳回結果集的陳述式](ecpg-dynamic.md#ecpg-dynamic-with-result)

- [34.6. pgtypes 函式庫](ecpg-pgtypes.md)
  - [34.6.1. 字串](ecpg-pgtypes.md#ecpg-pgtypes-cstrings)

  - [34.6.2. numeric 型別](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric)
    - [`PGTYPESnumeric_new`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-new)
    - [`PGTYPESnumeric_free`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-free)
    - [`PGTYPESnumeric_from_asc`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-from-asc)
    - [`PGTYPESnumeric_to_asc`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-to-asc)
    - [`PGTYPESnumeric_add`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-add)
    - [`PGTYPESnumeric_sub`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-sub)
    - [`PGTYPESnumeric_mul`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-mul)
    - [`PGTYPESnumeric_div`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-div)
    - [`PGTYPESnumeric_cmp`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-cmp)
    - [`PGTYPESnumeric_from_int`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-from-int)
    - [`PGTYPESnumeric_from_long`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-from-long)
    - [`PGTYPESnumeric_copy`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-copy)
    - [`PGTYPESnumeric_from_double`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-from-double)
    - [`PGTYPESnumeric_to_double`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-to-double)
    - [`PGTYPESnumeric_to_int`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-to-int)
    - [`PGTYPESnumeric_to_long`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-to-long)
    - [`PGTYPESnumeric_to_decimal`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-to-decimal)
    - [`PGTYPESnumeric_from_decimal`](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric-from-decimal)

  - [34.6.3. date 型別](ecpg-pgtypes-date.md#ecpg-pgtypes-date)
    - [`PGTYPESdate_from_timestamp`](ecpg-pgtypes-date.md#pgtypesdatefromtimestamp)
    - [`PGTYPESdate_from_asc`](ecpg-pgtypes-date.md#pgtypesdatefromasc)
    - [`PGTYPESdate_to_asc`](ecpg-pgtypes-date.md#pgtypesdatetoasc)
    - [`PGTYPESdate_julmdy`](ecpg-pgtypes-date.md#pgtypesdatejulmdy)
    - [`PGTYPESdate_mdyjul`](ecpg-pgtypes-date.md#pgtypesdatemdyjul)
    - [`PGTYPESdate_dayofweek`](ecpg-pgtypes-date.md#pgtypesdatedayofweek)
    - [`PGTYPESdate_today`](ecpg-pgtypes-date.md#pgtypesdatetoday)
    - [`PGTYPESdate_fmt_asc`](ecpg-pgtypes-date.md#pgtypesdatefmtasc)
    - [`PGTYPESdate_defmt_asc`](ecpg-pgtypes-date.md#pgtypesdatedefmtasc)

  - [34.6.4. timestamp 型別](ecpg-pgtypes.md#ecpg-pgtypes-timestamp)

  - [34.6.5. interval 型別](ecpg-pgtypes.md#ecpg-pgtypes-interval)

  - [34.6.6. decimal 型別](ecpg-pgtypes.md#ecpg-pgtypes-decimal)

  - [34.6.7. pgtypeslib 的 errno 值](ecpg-pgtypes.md#ecpg-pgtypes-errno)

  - [34.6.8. pgtypeslib 的特殊常數](ecpg-pgtypes.md#ecpg-pgtypes-constants)

- [34.7. 使用描述區](ecpg-descriptors.md)
  - [34.7.1. 具名 SQL 描述區](ecpg-descriptors.md#ecpg-named-descriptors)

  - [34.7.2. SQLDA 描述區](ecpg-sqlda-descriptors.md#ecpg-sqlda-descriptors)
    - [34.7.2.1. SQLDA 資料結構](ecpg-sqlda-data-structures.md)
      - [34.7.2.1.1. sqlda_t 結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-sqlda)
      - [34.7.2.1.2. sqlvar_t 結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-sqlvar)
      - [34.7.2.1.3. struct sqlname 結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-sqlname)
    - [34.7.2.2. 使用 SQLDA 取得結果集](ecpg-sqlda-descriptors.md#ecpg-sqlda-output)
    - [34.7.2.3. 使用 SQLDA 傳遞查詢參數](ecpg-sqlda-descriptors.md#ecpg-sqlda-input)
    - [34.7.2.4. 使用 SQLDA 的範例應用程式](ecpg-sqlda-descriptors.md#ecpg-sqlda-example)

- [34.8. 錯誤處理](ecpg-errors.md)
  - [34.8.1. 設定回呼](ecpg-errors.md#ecpg-whenever)

  - [34.8.2. sqlca](ecpg-errors.md#ecpg-sqlca)

  - [34.8.3. `SQLSTATE` 與 `SQLCODE` 的比較](ecpg-errors.md#ecpg-sqlstate-sqlcode)

- [34.9. 前置處理器指令](ecpg-preproc.md)
  - [34.9.1. 引入檔案](ecpg-preproc.md#ecpg-include)

  - [34.9.2. define 與 undef 指令](ecpg-preproc.md#ecpg-define)

  - [34.9.3. ifdef、ifndef、elif、else 與 endif 指令](ecpg-preproc.md#ecpg-ifdef)

- [34.10. 處理嵌入式 SQL 程式](ecpg-process.md)

- [34.11. 函式庫函式](ecpg-library.md)

- [34.12. 大型物件](ecpg-lo.md)

- [34.13. C++ 應用程式](ecpg-cpp.md)
  - [34.13.1. 主機變數的作用域](ecpg-cpp.md#ecpg-cpp-scope)

  - [34.13.2. 搭配外部 C 模組開發 C++ 應用程式](ecpg-cpp.md#ecpg-cpp-and-c)

- [34.14. 嵌入式 SQL 命令](ecpg-sql-commands.md)
  - [ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md) — 配置 SQL 描述區

  - [CONNECT](ecpg-sql-connect.md) — 建立資料庫連線

  - [DEALLOCATE DESCRIPTOR](ecpg-sql-deallocate-descriptor.md) — 釋放 SQL 描述區

  - [DECLARE](ecpg-sql-declare.md) — 定義游標

  - [DECLARE STATEMENT](ecpg-sql-declare-statement.md) — 宣告 SQL 陳述式識別字

  - [DESCRIBE](ecpg-sql-describe.md) — 取得預備陳述式或結果集的相關資訊

  - [DISCONNECT](ecpg-sql-disconnect.md) — 結束資料庫連線

  - [EXECUTE IMMEDIATE](ecpg-sql-execute-immediate.md) — 動態準備並執行陳述式

  - [GET DESCRIPTOR](ecpg-sql-get-descriptor.md) — 從 SQL 描述區取得資訊

  - [OPEN](ecpg-sql-open.md) — 開啟動態游標

  - [PREPARE](ecpg-sql-prepare.md) — 準備陳述式以供執行

  - [SET AUTOCOMMIT](ecpg-sql-set-autocommit.md) — 設定目前工作階段的自動提交行為

  - [SET CONNECTION](ecpg-sql-set-connection.md) — 選取資料庫連線

  - [SET DESCRIPTOR](ecpg-sql-set-descriptor.md) — 在 SQL 描述區中設定資訊

  - [TYPE](ecpg-sql-type.md) — 定義新的資料型別

  - [VAR](ecpg-sql-var.md) — 定義變數

  - [WHENEVER](ecpg-sql-whenever.md) — 指定 SQL 陳述式引發特定類別條件時要採取的動作

- [34.15. Informix 相容模式](ecpg-informix-compat.md)
  - [34.15.1. 額外的型別](ecpg-informix-compat.md#ecpg-informix-types)

  - [34.15.2. 額外／缺少的嵌入式 SQL 陳述式](ecpg-informix-compat.md#ecpg-informix-statements)

  - [34.15.3. 與 Informix 相容的 SQLDA 描述區](ecpg-informix-compat.md#ecpg-informix-sqlda)

  - [34.15.4. 額外的函式](ecpg-informix-compat.md#ecpg-informix-functions)

  - [34.15.5. 額外的常數](ecpg-informix-compat.md#ecpg-informix-constants)

- [34.16. Oracle 相容模式](ecpg-oracle-compat.md)

- [34.17. 內部運作](ecpg-develop.md)

<a id="id-1.7.5.2"></a><a id="id-1.7.5.3"></a><a id="id-1.7.5.4"></a>

本章說明 PostgreSQL 的嵌入式 SQL 套件。它由 Linus Tolke（`<linus@epact.se>`）與 Michael Meskes（`<meskes@postgresql.org>`）撰寫。它原本是為搭配 C 使用而撰寫的，也可以搭配 C++ 使用，但目前還無法辨識所有的 C++ 語法結構。

這份文件相當不完整。不過，由於此介面已經標準化，你可以在許多關於 SQL 的資源中找到更多資訊。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg.html)（原文版本：18.6；核對日期：2026-10-22）
