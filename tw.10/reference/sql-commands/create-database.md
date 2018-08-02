---
description: 版本：10
---

# CREATE DATABASE

CREATE DATABASE — 建立一個新的資料庫

### 語法

```text
CREATE DATABASE name
    [ [ WITH ] [ OWNER [=] user_name ]
           [ TEMPLATE [=] template ]
           [ ENCODING [=] encoding ]
           [ LC_COLLATE [=] lc_collate ]
           [ LC_CTYPE [=] lc_ctype ]
           [ TABLESPACE [=] tablespace_name ]
           [ ALLOW_CONNECTIONS [=] allowconn ]
           [ CONNECTION LIMIT [=] connlimit ]
           [ IS_TEMPLATE [=] istemplate ] ]
```

### 說明

CREATE DATABASE 建立一個新的 PostgreSQL 資料庫。

要建立資料庫，您必須是超級使用者或具有特殊的 CREATEDB 權限。請參閱 [CREATE USER](create-user.md)。

預設情況下，將透過複製標準系統資料庫 template1 來建立新的資料庫。可以透過修改 TEMPLATE 名稱來指定不同的樣板。特別是，通過修改 TEMPLATE template0，您可以建立一個僅包含您的 PostgreSQL 版本預定義的標準物件的原始資料庫。如果您希望避免複製可能已添加到 template1 的任何本地物件，這將非常有用。

### Parameters

_`name`_

The name of a database to create.

_`user_name`_

The role name of the user who will own the new database, or `DEFAULT` to use the default \(namely, the user executing the command\). To create a database owned by another role, you must be a direct or indirect member of that role, or be a superuser.

_`template`_

The name of the template from which to create the new database, or `DEFAULT` to use the default template \(`template1`\).

_`encoding`_

Character set encoding to use in the new database. Specify a string constant \(e.g., `'SQL_ASCII'`\), or an integer encoding number, or `DEFAULT` to use the default encoding \(namely, the encoding of the template database\). The character sets supported by the PostgreSQL server are described in [Section 23.3.1](https://www.postgresql.org/docs/10/static/multibyte.html#MULTIBYTE-CHARSET-SUPPORTED). See below for additional restrictions.

_`lc_collate`_

Collation order \(`LC_COLLATE`\) to use in the new database. This affects the sort order applied to strings, e.g. in queries with ORDER BY, as well as the order used in indexes on text columns. The default is to use the collation order of the template database. See below for additional restrictions.

_`lc_ctype`_

Character classification \(`LC_CTYPE`\) to use in the new database. This affects the categorization of characters, e.g. lower, upper and digit. The default is to use the character classification of the template database. See below for additional restrictions.

_`tablespace_name`_

The name of the tablespace that will be associated with the new database, or `DEFAULT` to use the template database's tablespace. This tablespace will be the default tablespace used for objects created in this database. See [CREATE TABLESPACE](https://www.postgresql.org/docs/10/static/sql-createtablespace.html) for more information.

_`allowconn`_

If false then no one can connect to this database. The default is true, allowing connections \(except as restricted by other mechanisms, such as `GRANT`/`REVOKE CONNECT`\).

_`connlimit`_

How many concurrent connections can be made to this database. -1 \(the default\) means no limit.

_`istemplate`_

If true, then this database can be cloned by any user with `CREATEDB` privileges; if false \(the default\), then only superusers or the owner of the database can clone it.

Optional parameters can be written in any order, not only the order illustrated above.

### 注意

不能在交易事務區塊內執行 CREATE DATABASE。

「無法初始化資料庫目錄」的錯誤很可能與資料目錄，磁碟空間滿載或其他檔案系統的權限不足問題有關。

使用 [DROP DATABASE](drop-database.md) 移除資料庫。

工具 [createdb](../client-applications/createdb.md) 是一個封裝此指令的程式，為方便起見而提供。

不會從樣板資料庫中複製資料庫級的組態參數（透過 ALTER DATABASE 設定）。

雖然可以透過將其名稱指定為模板來複製除 template1 之外的資料庫，但這並不是（通常）用作通用的「COPY DATABASE」工具。主要限制是在複製樣板資料庫時不能有其他連線到樣板資料庫。如果啟動時存在任何其他連線，則 CREATE DATABASE 將失敗；否則，在 CREATE DATABASE 完成之前，將鎖定與樣版資料庫新的連線。有關更多訊息，請參閱[第 22.3 節](../../server-administration/22.-managing-databases/22.3.-template-databases.md)。

為新資料庫指定的字元集編碼必須與所選的區域設定（LC\_COLLATE 和 LC\_CTYPE）相容。如果語言環境是 C（或等效 POSIX），則允許所有編碼，但對於其他語言環境設定，只有一種編碼可以正常工作。（不過，在Windows上，UTF-8 編碼可以與任何語言環境一起使用。）CREATE DATABASE 將允許超級使用者指定 SQL\_ASCII 編碼而不管語言環境設定如何，但是這種方式已被棄用。如果資料可能導致字串函數的不當行為，則與語言環境不相容的編碼就會儲存在資料庫中。

編碼和語言環境設定必須與樣板資料庫的設定相符合，除非將 template0 用作樣板。這是因為其他資料庫可能包含與指定編碼不相符合的資料，或者可能包含其排序順序受 LC\_COLLATE 和 LC\_CTYPE 影響的索引。複製此類資料將導致資料庫根據新設定而損壞。總之，template0 不包含任何會受影響的資料或索引。

CONNECTION LIMIT 選項僅近乎強制執行：如果兩個新連線幾乎同時開始，當資料庫只剩下一個連線「插槽」時，則兩者都可能會失敗。此外，不會對超級使用者或後台工作程序強制執行此限制。

### 範例

要建立新資料庫：

```text
CREATE DATABASE lusiadas;
```

使用 salesspace 預設資料表空間並建立由使用者 salesapp 所擁有的資料庫 sales：

```text
CREATE DATABASE sales OWNER salesapp TABLESPACE salesspace;
```

要使用不同的區域設定來建立資料庫 music：

```text
CREATE DATABASE music
    LC_COLLATE 'sv_SE.utf8' LC_CTYPE 'sv_SE.utf8'
    TEMPLATE template0;
```

在此範例中，如果指定的語言環境與 template1 中的語言環境不同，則需要 TEMPLATE template0 子句。（如果不是，則明確指定語言環境是多餘的。）

要建立具有不同區域設定和不同字元集編碼的資料庫 music2：

```text
CREATE DATABASE music2
    LC_COLLATE 'sv_SE.iso885915' LC_CTYPE 'sv_SE.iso885915'
    ENCODING LATIN9
    TEMPLATE template0;
```

指定的區域設定和編碼設定必須相符合，否則將回報錯誤。

請注意，區域設定名稱專屬於作業系統，因此上述指令可能無法在其他地方以相同的方式工作。

### 相容性

SQL 標準中沒有 CREATE DATABASE 語句。資料庫等同於目錄，其建立是實作上定義的。

### 參閱

[ALTER DATABASE](alter-database.md), [DROP DATABASE](drop-database.md)

