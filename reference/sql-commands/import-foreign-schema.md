# IMPORT FOREIGN SCHEMA

IMPORT FOREIGN SCHEMA — 從外部伺服器匯入資料表定義

### 語法

```
IMPORT FOREIGN SCHEMA remote_schema
    [ { LIMIT TO | EXCEPT } ( table_name [, ...] ) ]
    FROM SERVER server_name
    INTO local_schema
    [ OPTIONS ( option 'value' [, ... ] ) ]
```

### 說明

IMPORT FOREIGN SCHEMA 會建立外部資料表，這些外部資料表是外部伺服器上現有的資料表。新的外部資料表將由發出命令的使用者所有，並使用正確的欄位定義和選項來建立，以搭配遠端的資料表。

預設情況下，將導入外部伺服器上特定 schema 中存在的所有資料表和檢視表。可以選擇將資料表限制為指定的名單，也可以排除特定的資料表。所有新的外部資料表都會在目標 schema 中建立，該 schema 必須已經存在。

要使用 IMPORT FOREIGN SCHEMA，使用者必須在外部伺服器上具有 USAGE 權限，並在目標 schema 上具有 CREATE 權限。

### Parameters

_`remote_schema`_

The remote schema to import from. The specific meaning of a remote schema depends on the foreign data wrapper in use.

`LIMIT TO (`` `_`table_name`_ \[, ...] )

Import only foreign tables matching one of the given table names. Other tables existing in the foreign schema will be ignored.

`EXCEPT (`` `_`table_name`_ \[, ...] )

Exclude specified foreign tables from the import. All tables existing in the foreign schema will be imported except the ones listed here.

_`server_name`_

The foreign server to import from.

_`local_schema`_

The schema in which the imported foreign tables will be created.

`OPTIONS (`` `_`option`_ '_`value`_' \[, ...] )

Options to be used during the import. The allowed option names and values are specific to each foreign data wrapper.

### 範例

從伺服器 film\_server 上的遠端 schema foreign\_films 匯入資料表定義，然後在本機 schema films 中建立外部資料表：

```
IMPORT FOREIGN SCHEMA foreign_films
    FROM SERVER film_server INTO films;
```

如上所述，但僅導入兩個資料表 actors 和 directors（如果它們存在的話）：

```
IMPORT FOREIGN SCHEMA foreign_films LIMIT TO (actors, directors)
    FROM SERVER film_server INTO films;
```

### 相容性

IMPORT FOREIGN SCHEMA 指令符合 SQL 標準，但 OPTIONS 子句是 PostgreSQL 的延伸功能。

### _`參閱`_

[CREATE FOREIGN TABLE](create-foreign-table.md), [CREATE SERVER](create-server.md)
