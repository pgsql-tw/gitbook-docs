<a id="SQL-CREATESCHEMA"></a><a id="id-1.9.3.80.1"></a>

## CREATE SCHEMA

CREATE SCHEMA — 定義新的綱要

<a id="id-1.9.3.80.4"></a>

## 語法

```

CREATE SCHEMA schema_name [ AUTHORIZATION role_specification ] [ schema_element [ ... ] ]
CREATE SCHEMA AUTHORIZATION role_specification [ schema_element [ ... ] ]
CREATE SCHEMA IF NOT EXISTS schema_name [ AUTHORIZATION role_specification ]
CREATE SCHEMA IF NOT EXISTS AUTHORIZATION role_specification

where role_specification can be:

    user_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

<a id="id-1.9.3.80.5"></a>

## 說明

`CREATE SCHEMA` 會在目前資料庫中建立一個新的綱要。綱要名稱必須與目前資料庫中任何現有綱要的名稱都不同。

綱要本質上是一個命名空間：它包含具名物件（資料表、資料型別、函式與運算子），這些物件的名稱可以與其他綱要中既有的其他物件名稱重複。存取具名物件的方式，可以是以綱要名稱作為前綴來「限定」其名稱，也可以是設定包含所需綱要的搜尋路徑。指定未限定物件名稱的 `CREATE` 命令，會在目前綱要（搜尋路徑最前面的那個綱要，可以用函式 `current_schema` 確定）中建立該物件。

`CREATE SCHEMA` 可以選擇性地包含子命令，以在新綱要中建立物件。這些子命令的處理方式基本上與建立綱要之後分別下達的命令相同，不同之處在於：若使用了 `AUTHORIZATION` 子句，所有建立的物件都會由該使用者擁有。

<a id="id-1.9.3.80.6"></a>

## 參數

*`schema_name`*
:   要建立的綱要名稱。若省略此項，則以 *`user_name`* 作為綱要名稱。名稱不能以 `pg_` 開頭，因為這類名稱保留給系統綱要使用。

*`user_name`*
:   將擁有新綱要之使用者的角色名稱。若省略，預設為執行此命令的使用者。若要建立由其他角色擁有的綱要，你必須能夠 `SET ROLE` 為該角色。

*`schema_element`*
:   定義要在綱要中建立之物件的 SQL 陳述式。目前在 `CREATE SCHEMA` 中只接受 `CREATE
    TABLE`、`CREATE VIEW`、`CREATE
    INDEX`、`CREATE SEQUENCE`、`CREATE
    TRIGGER` 與 `GRANT` 作為子句。其他種類的物件可以在綱要建立之後，以個別的命令建立。

`IF NOT EXISTS`
:   若已存在同名的綱要，則不執行任何動作（但會發出 notice）。使用此選項時，不能包含 *`schema_element`* 子命令。

<a id="id-1.9.3.80.7"></a>

## 注意事項

若要建立綱要，呼叫的使用者必須擁有目前資料庫的 `CREATE` 權限。（當然，超級使用者不受此檢查限制。）

<a id="id-1.9.3.80.8"></a>

## 範例

建立綱要：

```

CREATE SCHEMA myschema;
```

為使用者 `joe` 建立綱要；該綱要也會命名為 `joe`：

```

CREATE SCHEMA AUTHORIZATION joe;
```

建立名為 `test`、由使用者 `joe` 擁有的綱要，除非已經存在名為 `test` 的綱要。（`joe` 是否擁有該既有綱要並不重要。）

```

CREATE SCHEMA IF NOT EXISTS test AUTHORIZATION joe;
```

建立綱要，並在其中建立資料表與檢視表：

```

CREATE SCHEMA hollywood
    CREATE TABLE films (title text, release date, awards text[])
    CREATE VIEW winners AS
        SELECT title, release FROM films WHERE awards IS NOT NULL;
```

請注意，個別的子命令不以分號結尾。

以下是達成相同結果的等效方式：

```

CREATE SCHEMA hollywood;
CREATE TABLE hollywood.films (title text, release date, awards text[]);
CREATE VIEW hollywood.winners AS
    SELECT title, release FROM hollywood.films WHERE awards IS NOT NULL;
```

<a id="id-1.9.3.80.9"></a>

## 相容性

SQL 標準允許在 `CREATE SCHEMA` 中使用 `DEFAULT CHARACTER SET` 子句，也允許比 PostgreSQL 目前所接受更多種類的子命令。

SQL 標準規定 `CREATE
SCHEMA` 中的子命令可以依任意順序出現。目前的 PostgreSQL 實作並未處理子命令中所有前向參照的情況；有時可能需要重新排列子命令的順序，以避免前向參照。

依據 SQL 標準，綱要的擁有者一律擁有其中的所有物件。PostgreSQL 允許綱要包含由綱要擁有者以外的使用者所擁有的物件。只有在綱要擁有者將其綱要的 `CREATE` 權限授予他人，或超級使用者選擇在其中建立物件時，才會發生這種情況。

`IF NOT EXISTS` 選項是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.80.10"></a>

## 另請參閱

[ALTER SCHEMA](sql-alterschema.md), [DROP SCHEMA](sql-dropschema.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createschema.html)（原文版本：18.6；核對日期：2026-10-04）
