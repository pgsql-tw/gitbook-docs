<a id="SQL-ALTERUSERMAPPING"></a><a id="id-1.9.3.44.1"></a>

## ALTER USER MAPPING

ALTER USER MAPPING — 變更使用者對應的定義

<a id="id-1.9.3.44.4"></a>

## 語法

```

ALTER USER MAPPING FOR { user_name | USER | CURRENT_ROLE | CURRENT_USER | SESSION_USER | PUBLIC }
    SERVER server_name
    OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )
```

<a id="id-1.9.3.44.5"></a>

## 說明

`ALTER USER MAPPING` 會變更使用者對應的定義。

外部伺服器的擁有者可以為任何使用者變更該伺服器的使用者對應。此外，若使用者已被授予該伺服器的 `USAGE` 權限，該使用者也可以為自己的使用者名稱變更使用者對應。

<a id="id-1.9.3.44.6"></a>

## 參數

*`user_name`*
:   該對應的使用者名稱。`CURRENT_ROLE`、`CURRENT_USER` 與 `USER` 均符合目前使用者的名稱。`PUBLIC` 用來符合系統中所有現有及未來的使用者名稱。

*`server_name`*
:   該使用者對應的伺服器名稱。

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`
:   變更該使用者對應的選項。新的選項會覆寫任何先前指定的選項。`ADD`、`SET` 與 `DROP` 指定要執行的動作。若未明確指定操作，則假定為 `ADD`。選項名稱必須是唯一的；選項也會由該伺服器的外部資料包裝器進行驗證。

<a id="id-1.9.3.44.7"></a>

## 範例

變更使用者對應 `bob`、伺服器 `foo` 的密碼：

```

ALTER USER MAPPING FOR bob SERVER foo OPTIONS (SET password 'public');
```

<a id="id-1.9.3.44.8"></a>

## 相容性

`ALTER USER MAPPING` 符合 ISO/IEC 9075-9（SQL/MED）。這裡有一個細微的語法問題：標準省略了 `FOR` 關鍵字。由於 `CREATE
USER MAPPING` 與 `DROP USER MAPPING` 都在類似的位置使用 `FOR`，而且 IBM DB2（另一個主要的 SQL/MED 實作）的 `ALTER USER MAPPING` 也要求使用它，因此 PostgreSQL 在此偏離標準，以求一致性與互通性。

<a id="id-1.9.3.44.9"></a>

## 另請參閱

[CREATE USER MAPPING](sql-createusermapping.md), [DROP USER MAPPING](sql-dropusermapping.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterusermapping.html)（原文版本：18.6；核對日期：2026-10-04）
