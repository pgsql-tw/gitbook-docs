<a id="SQL-CREATEFOREIGNDATAWRAPPER"></a><a id="id-1.9.3.65.1"></a>

## CREATE FOREIGN DATA WRAPPER

CREATE FOREIGN DATA WRAPPER — 定義新的外部資料包裝器

<a id="id-1.9.3.65.4"></a>

## 語法

```

CREATE FOREIGN DATA WRAPPER name
    [ HANDLER handler_function | NO HANDLER ]
    [ VALIDATOR validator_function | NO VALIDATOR ]
    [ OPTIONS ( option 'value' [, ... ] ) ]
```

<a id="id-1.9.3.65.5"></a>

## 說明

`CREATE FOREIGN DATA WRAPPER` 會建立一個新的外部資料包裝器。定義外部資料包裝器的使用者會成為其擁有者。

外部資料包裝器的名稱在資料庫內必須是唯一的。

只有超級使用者可以建立外部資料包裝器。

<a id="id-1.9.3.65.6"></a>

## 參數

*`name`*
:   要建立的外部資料包裝器名稱。

`HANDLER handler_function`
:   *`handler_function`* 是先前已註冊之函式的名稱，系統會呼叫它來取得外部資料表的執行函式。處理函式不得接受任何引數，且其回傳型別必須是 `fdw_handler`。

    可以建立沒有處理函式的外部資料包裝器，但使用這種包裝器的外部資料表只能被宣告，無法被存取。

`VALIDATOR validator_function`
:   *`validator_function`* 是先前已註冊之函式的名稱，系統會呼叫它來檢查提供給外部資料包裝器的通用選項，以及使用該外部資料包裝器之外部伺服器、使用者對應與外部資料表的選項。若未指定驗證函式，或指定了 `NO
    VALIDATOR`，則建立時不會檢查選項。（外部資料包裝器可能會在執行時忽略或拒絕無效的選項設定，視實作而定。）驗證函式必須接受兩個引數：一個是 `text[]` 型別，內容為儲存在系統目錄中的選項陣列；另一個是 `oid` 型別，為包含這些選項之系統目錄的 OID。回傳型別會被忽略；該函式應該使用 `ereport(ERROR)` 函式回報無效的選項。

`OPTIONS ( option 'value' [, ... ] )`
:   此子句指定新外部資料包裝器的選項。允許的選項名稱與值由各個外部資料包裝器各自規定，並由該外部資料包裝器的驗證函式進行驗證。選項名稱必須是唯一的。

<a id="id-1.9.3.65.7"></a>

## 注意事項

PostgreSQL 的外部資料功能仍在積極開發中。查詢最佳化仍相當初步（而且大多也交由包裝器處理）。因此，未來在效能上還有相當大的改進空間。

<a id="id-1.9.3.65.8"></a>

## 範例

建立一個無用的外部資料包裝器 `dummy`：

```

CREATE FOREIGN DATA WRAPPER dummy;
```

建立一個具有處理函式 `file_fdw_handler` 的外部資料包裝器 `file`：

```

CREATE FOREIGN DATA WRAPPER file HANDLER file_fdw_handler;
```

建立一個具有一些選項的外部資料包裝器 `mywrapper`：

```

CREATE FOREIGN DATA WRAPPER mywrapper
    OPTIONS (debug 'true');
```

<a id="id-1.9.3.65.9"></a>

## 相容性

`CREATE FOREIGN DATA WRAPPER` 符合 ISO/IEC 9075-9（SQL/MED），例外的是 `HANDLER` 與 `VALIDATOR` 子句是擴充語法，而標準的 `LIBRARY` 與 `LANGUAGE` 子句在 PostgreSQL 中並未實作。

不過請注意，SQL/MED 功能整體而言尚未符合標準。

<a id="id-1.9.3.65.10"></a>

## 另請參閱

[ALTER FOREIGN DATA WRAPPER](sql-alterforeigndatawrapper.md), [DROP FOREIGN DATA WRAPPER](sql-dropforeigndatawrapper.md), [CREATE SERVER](sql-createserver.md), [CREATE USER MAPPING](sql-createusermapping.md), [CREATE FOREIGN TABLE](sql-createforeigntable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createforeigndatawrapper.html)（原文版本：18.6；核對日期：2026-10-04）
