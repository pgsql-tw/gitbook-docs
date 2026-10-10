<a id="SQL-ALTERDOMAIN"></a><a id="id-1.9.3.9.1"></a>

## ALTER DOMAIN

ALTER DOMAIN — 變更網域的定義

<a id="id-1.9.3.9.4"></a>

## 語法

```

ALTER DOMAIN name
    { SET DEFAULT expression | DROP DEFAULT }
ALTER DOMAIN name
    { SET | DROP } NOT NULL
ALTER DOMAIN name
    ADD domain_constraint [ NOT VALID ]
ALTER DOMAIN name
    DROP CONSTRAINT [ IF EXISTS ] constraint_name [ RESTRICT | CASCADE ]
ALTER DOMAIN name
     RENAME CONSTRAINT constraint_name TO new_constraint_name
ALTER DOMAIN name
    VALIDATE CONSTRAINT constraint_name
ALTER DOMAIN name
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER DOMAIN name
    RENAME TO new_name
ALTER DOMAIN name
    SET SCHEMA new_schema

where domain_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL | CHECK (expression) }
```

<a id="id-1.9.3.9.5"></a>

## 說明

`ALTER DOMAIN` 會變更現有網域的定義。它有以下幾種子形式：

`SET`/`DROP DEFAULT`
:   這些形式會設定或移除網域的預設值。請注意，預設值只會套用到之後的 `INSERT` 命令；它們不會影響使用該網域之資料表中已存在的資料列。

`SET`/`DROP NOT NULL`
:   這些形式會變更網域被標記為允許 NULL 值還是拒絕 NULL 值。只有在使用該網域的欄位不含任何 NULL 值時，你才能 `SET NOT NULL`。

`ADD domain_constraint [ NOT VALID ]`
:   此形式會為網域新增限制條件。當網域新增限制條件時，所有使用該網域的欄位都會依新加入的限制條件進行檢查。若使用 `NOT VALID` 選項新增限制條件，就可以略過這些檢查；之後可以使用 `ALTER DOMAIN ... VALIDATE CONSTRAINT` 完成該限制條件的驗證（確認既有資料都符合該限制條件）。新插入或更新的資料列一律會依所有限制條件進行檢查，包括標記為 `NOT VALID` 的限制條件。`NOT VALID` 只接受用於 `CHECK` 限制條件。

`DROP CONSTRAINT [ IF EXISTS ]`
:   此形式會移除網域上的限制條件。若指定了 `IF EXISTS` 而該限制條件不存在，則不擲出錯誤；此情況會改為發出 notice。

`RENAME CONSTRAINT`
:   此形式會變更網域上某個限制條件的名稱。

`VALIDATE CONSTRAINT`
:   此形式會驗證先前以 `NOT VALID` 加入的限制條件，也就是確認該網域型別之資料表欄位中的所有值都滿足指定的限制條件。

`OWNER`
:   此形式會將網域的擁有者變更為指定的使用者。

`RENAME`
:   此形式會變更網域的名稱。

`SET SCHEMA`
:   此形式會變更網域的綱要。與該網域相關聯的所有限制條件也會一併移到新的綱要中。

你必須是網域的擁有者，才能使用 `ALTER DOMAIN`。若要變更網域的綱要，你還必須在新的綱要上具有 `CREATE` 權限。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，而且該角色必須在網域所屬的綱要上具有 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法透過移除並重新建立網域而做到的事。不過，超級使用者無論如何都可以變更任何網域的擁有權。）

<a id="id-1.9.3.9.6"></a>

## 參數

*`name`*
:   要變更之現有網域的名稱（可能以綱要限定）。

*`domain_constraint`*
:   網域的新限制條件。

*`constraint_name`*
:   要移除或重新命名之現有限制條件的名稱。

`NOT VALID`
:   不驗證現有已儲存資料是否符合限制條件。

`CASCADE`
:   自動移除相依於該限制條件的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該限制條件，則拒絕移除。這是預設行為。

*`new_name`*
:   網域的新名稱。

*`new_constraint_name`*
:   限制條件的新名稱。

*`new_owner`*
:   網域新擁有者的使用者名稱。

*`new_schema`*
:   網域的新綱要。

<a id="id-1.9.3.9.7"></a>

## 注意事項

雖然 `ALTER DOMAIN ADD CONSTRAINT` 會嘗試驗證現有已儲存的資料是否滿足新的限制條件，但這項檢查並非萬無一失，因為此命令無法「看見」新插入或更新但尚未提交的資料表資料列。若有並行操作可能插入不良資料的風險，做法是使用 `NOT VALID` 選項新增限制條件、提交該命令、等待所有在該次提交之前開始的交易結束，然後再執行 `ALTER DOMAIN VALIDATE
CONSTRAINT` 搜尋違反限制條件的資料。這個方法是可靠的，因為一旦限制條件已提交，所有新的交易都保證會對該網域型別的新值強制執行它。

目前，若指定的網域或任何衍生網域被用在資料庫中任何資料表的容器型別欄位（複合、陣列或範圍欄位）內，`ALTER DOMAIN ADD CONSTRAINT`、`ALTER
DOMAIN VALIDATE CONSTRAINT` 與 `ALTER DOMAIN SET NOT
NULL` 將會失敗。這些命令最終應該要改進為能夠對這類巢狀值驗證新的限制條件。

<a id="id-1.9.3.9.8"></a>

## 範例

為網域加上 `NOT NULL` 限制條件：

```

ALTER DOMAIN zipcode SET NOT NULL;
```

從網域移除 `NOT NULL` 限制條件：

```

ALTER DOMAIN zipcode DROP NOT NULL;
```

為網域加上檢查限制條件：

```

ALTER DOMAIN zipcode ADD CONSTRAINT zipchk CHECK (char_length(VALUE) = 5);
```

從網域移除檢查限制條件：

```

ALTER DOMAIN zipcode DROP CONSTRAINT zipchk;
```

重新命名網域上的檢查限制條件：

```

ALTER DOMAIN zipcode RENAME CONSTRAINT zipchk TO zip_check;
```

將網域移到另一個綱要：

```

ALTER DOMAIN zipcode SET SCHEMA customers;
```

<a id="SQL-ALTERDOMAIN-COMPATIBILITY"></a>

## 相容性

`ALTER DOMAIN` 符合 SQL 標準，但 `OWNER`、`RENAME`、`SET SCHEMA` 與 `VALIDATE CONSTRAINT` 這幾種變體除外，它們是 PostgreSQL 的擴充語法。`ADD CONSTRAINT` 變體的 `NOT VALID` 子句也是 PostgreSQL 的擴充語法。

<a id="SQL-ALTERDOMAIN-SEE-ALSO"></a>

## 另請參閱

[CREATE DOMAIN](sql-createdomain.md), [DROP DOMAIN](sql-dropdomain.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterdomain.html)（原文版本：18.6；核對日期：2026-10-10）
