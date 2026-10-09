<a id="SQL-ALTERFOREIGNDATAWRAPPER"></a><a id="id-1.9.3.12.1"></a>

## ALTER FOREIGN DATA WRAPPER

ALTER FOREIGN DATA WRAPPER — 變更外部資料包裝器的定義

<a id="id-1.9.3.12.4"></a>

## 語法

```

ALTER FOREIGN DATA WRAPPER name
    [ HANDLER handler_function | NO HANDLER ]
    [ VALIDATOR validator_function | NO VALIDATOR ]
    [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ]) ]
ALTER FOREIGN DATA WRAPPER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER FOREIGN DATA WRAPPER name RENAME TO new_name
```

<a id="id-1.9.3.12.5"></a>

## 說明

`ALTER FOREIGN DATA WRAPPER` 會變更外部資料包裝器的定義。此命令的第一種形式會變更外部資料包裝器的支援函式或通用選項（至少需要一個子句）。第二種形式會變更外部資料包裝器的擁有者。

只有超級使用者可以變更外部資料包裝器。此外，也只有超級使用者可以擁有外部資料包裝器。

<a id="id-1.9.3.12.6"></a>

## 參數

*`name`*
:   現有外部資料包裝器的名稱。

`HANDLER handler_function`
:   為外部資料包裝器指定新的處理函式。

`NO HANDLER`
:   用來指定外部資料包裝器不應再有處理函式。

    請注意，使用沒有處理函式之外部資料包裝器的外部資料表無法被存取。

`VALIDATOR validator_function`
:   為外部資料包裝器指定新的驗證函式。

    請注意，外部資料包裝器或相依的外部伺服器、使用者對應或外部資料表既有的選項，依新的驗證函式判斷可能是無效的。PostgreSQL 不會檢查這一點。使用者必須自行確認這些選項正確，再使用修改後的外部資料包裝器。不過，在這個 `ALTER FOREIGN DATA
    WRAPPER` 命令中指定的任何選項，都會使用新的驗證函式檢查。

`NO VALIDATOR`
:   用來指定外部資料包裝器不應再有驗證函式。

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`
:   變更外部資料包裝器的選項。`ADD`、`SET` 與 `DROP` 指定要執行的動作。若未明確指定操作，則假定為 `ADD`。選項名稱必須唯一；若外部資料包裝器有驗證函式，名稱與值也會經由該驗證函式檢查。

*`new_owner`*
:   外部資料包裝器新擁有者的使用者名稱。

*`new_name`*
:   外部資料包裝器的新名稱。

<a id="id-1.9.3.12.7"></a>

## 範例

變更外部資料包裝器 `dbi`，新增選項 `foo`，並移除 `bar`：

```

ALTER FOREIGN DATA WRAPPER dbi OPTIONS (ADD foo '1', DROP bar);
```

將外部資料包裝器 `dbi` 的驗證函式變更為 `bob.myvalidator`：

```

ALTER FOREIGN DATA WRAPPER dbi VALIDATOR bob.myvalidator;
```

<a id="id-1.9.3.12.8"></a>

## 相容性

`ALTER FOREIGN DATA WRAPPER` 符合 ISO/IEC 9075-9（SQL/MED），但 `HANDLER`、`VALIDATOR`、`OWNER TO` 與 `RENAME` 子句是擴充語法。

<a id="id-1.9.3.12.9"></a>

## 另請參閱

[CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md), [DROP FOREIGN DATA WRAPPER](sql-dropforeigndatawrapper.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterforeigndatawrapper.html)（原文版本：18.6；核對日期：2026-10-05）
