<a id="SQL-ALTERSERVER"></a><a id="id-1.9.3.31.1"></a>

## ALTER SERVER

ALTER SERVER — 變更外部伺服器的定義

<a id="id-1.9.3.31.4"></a>

## 語法

```

ALTER SERVER name [ VERSION 'new_version' ]
    [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] ) ]
ALTER SERVER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SERVER name RENAME TO new_name
```

<a id="id-1.9.3.31.5"></a>

## 說明

`ALTER SERVER` 會變更外部伺服器的定義。第一種形式會變更伺服器版本字串或伺服器的通用選項（至少需要一個子句）。第二種形式會變更伺服器的擁有者。

若要變更伺服器，你必須是該伺服器的擁有者。此外，若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，並且必須擁有該伺服器之外部資料包裝器的 `USAGE` 權限。（請注意，超級使用者會自動滿足所有這些條件。）

<a id="id-1.9.3.31.6"></a>

## 參數

*`name`*
:   現有伺服器的名稱。

*`new_version`*
:   新的伺服器版本。

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`
:   變更伺服器的選項。`ADD`、`SET` 與 `DROP` 指定要執行的動作。若未明確指定操作，則假定為 `ADD`。選項名稱必須唯一；名稱與值也會使用伺服器的外部資料包裝器函式庫進行驗證。

*`new_owner`*
:   外部伺服器新擁有者的使用者名稱。

*`new_name`*
:   外部伺服器的新名稱。

<a id="id-1.9.3.31.7"></a>

## 範例

變更伺服器 `foo`，加入連線選項：

```

ALTER SERVER foo OPTIONS (host 'foo', dbname 'foodb');
```

變更伺服器 `foo`，變更版本，並變更 `host` 選項：

```

ALTER SERVER foo VERSION '8.4' OPTIONS (SET host 'baz');
```

<a id="id-1.9.3.31.8"></a>

## 相容性

`ALTER SERVER` 符合 ISO/IEC 9075-9（SQL/MED）。`OWNER TO` 與 `RENAME` 形式是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.31.9"></a>

## 另請參閱

[CREATE SERVER](sql-createserver.md), [DROP SERVER](sql-dropserver.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterserver.html)（原文版本：18.6；核對日期：2026-10-05）
