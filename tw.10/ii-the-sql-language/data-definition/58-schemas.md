# 5.8. Schemas[^1]

> Schema 在台灣並沒有習慣的中文說法，所以仍使用原文，而不翻譯。

PostgreSQL 資料庫叢集（cluster）可以包含一個或多個資料庫。使用者和群組則是共用於叢集的層次，但沒有任何資料面是在資料庫之間能共用的。任何用戶端連到資料庫服務，都只能存取單一資料庫，你必須在連線時指定一個資料庫。

### 注意

在叢集內的使用者並不需要對每個資料庫都有使用權。使用者共用指的是它們不能有同名的情況，例如在同一個叢集內，不能有兩個使用者名稱都叫 joe。但系統可以只允許 joe 使用某些叢集內的資料庫。

一個資料庫可以包含一個或多個 schema，它會包含一些資料表。Schema 也可以包含一些資料庫物件，像是資料型別、函數、和運算子。同樣的物件名稱在不同的 schema 中是不會衝突的。舉例來說，schema1 和 myschema 都可以擁有一個叫作 mytable 的資料表。和資料庫不同， schema 並不是完全隔離的：使用者可以直接取用他們連接的資料庫中的任何 schema，只要他們擁有足夠的權限。

使用 schema 有幾個好處：

* 允許多個使用者存取相同資料庫，而不會互相干擾。
* 將資料庫物件建立邏輯上的管理層，它們會更有彈性。
* 第三方的應用結構可以放在不同的 schema 中，避免有撞名的情況產生。

Schema 和作業系統裡的資料夾是類似的，只是它不能使用巢狀結構。

### 5.8.1. 建立 Schema

要建立 schema，請使用 [CREATE SCHEMA](/vi-reference/i-sql-commands/create-schema.md) 指令。給予一個自訂的名稱。例如：

```
CREATE SCHEMA myschema;
```

要在 schema 中建立或存取某個物件，請使用句點（.）將兩者名稱串連起來：

```
schema.table
```

這個形式在任何可以使用資料表的地方都是可以的，包含資料表結構更新指令，以及在接下來章節會討論到的資料處理指令。（我們只提到資料表的部份，但相同的概念用於其他資料庫物件都是一樣的，像是資料型別和函數。）

實際上，更一般化的語法是：

```
database.schema.table
```

也可以這樣使用，但目前這只是為了符合 SQL 標準而已。如果你填上了資料庫的名稱，也必須填上你所連線的資料庫而已。

所以，要在新的 schema 中建立一個資料表，請使用：

```
CREATE TABLE myschema.mytable (
 ...
);
```

要移除一個 schema，它必須要是空的，也就是所有所屬物件都已經被移除了，請使用：

```
DROP SCHEMA myschema;
```

但你也可以同步移除 schema 及其所屬物件，請使用：

```
DROP SCHEMA myschema CASCADE;
```

這個部份的機制請參閱 [5.13 節](/ii-the-sql-language/data-definition/513-dependency-tracking.md)，會深入介紹移除時的問題。

通常你會想要建立一個 schema 給某個使用者使用（這是一種藉由命名空間規畫來限制使用者權限的方法）。可以使用下列語法：

```
CREATE SCHEMA schema_name AUTHORIZATION user_name;
```

你甚至可以省略 schema 名稱，省略的話，schema 名稱會與使用者名稱相同。請參閱後續的 5.8.6 節來瞭解如何使用。

Schema 名稱以「pg\_」開頭的，是系統的保留名稱，使用者不能使用這樣的名稱建立 schema。

### 5.8.2. 公開的 Schema

在前面我們所建立的資料表都沒有指定 schema 名稱。預設使用的 schema 是「public」，每一個資料庫都會有這個 schema。所以，下面兩種寫法是一樣的：

```
CREATE TABLE products ( ... );
```

以及：

```
CREATE TABLE public.products ( ... );
```

### 5.8.3. Schema 搜尋路徑

完整的名稱寫法是冗長而不容易使用的，通常最好不要把一些特別的 schema 名稱寫到應用程式裡。而資料表時常是以簡要的寫法引用，也就是只寫資料表本身的名稱。資料庫系統依據搜尋路徑的規則找到該資料表。在搜尋路徑上所遇到的第一個資料表就會被使用。如果整個搜尋路徑走完都沒有符合的資料表，那麼才會回報錯誤，即使該資料表名稱有出現在資料庫裡的其他 schema 中。

第一個會被搜尋的 schema，就是目前的 schema。除此之外也用於新的資料表建立，當 CREATE TABLE 未指定 schema 名稱的話，也會依搜尋路徑的 schema 建立。

要顯示目前的搜尋路徑，請使用下面的指令：

```
SHOW search_path;
```

預設的情況是：

```
 search_path
--------------
 "$user", public
```

第一個項目指的就是和目前使用者同名的 schema 會被使用，而如果沒有同名的，它就會被忽略。第二個項目則是先前介紹過的公開 schema。第一個被找到的 schema，就會是新建物件時預設的位置，這就是為什麼預設都會被建立在公開的 schema。當某個物件在使用（資料表結構調整、資料更新、或查詢指令）時沒有註明 schema 的話，那也會使用搜尋路徑來找到符合的物件。不過，預設上只會搜尋公開的 schema。

要設定新的搜尋路徑，請使用：

```
SET search_path TO myschema,public;
```

（我們在這邊暫時忽略掉 $user，因為還沒有立即性的需要。）然後我們就可以試著存取資料表而不用加上 schema：

```
DROP TABLE mytable;
```

因為 myschema 在搜尋路徑裡是第一個項目，所以新的物件就會被建立在該處。

我們也可以這樣寫：

```
SET search_path TO myschema;
```

這樣的話，不指定的話就不再能夠再使用公開的 schema 了。

Then we no longer have access to the public schema without explicit qualification. There is nothing special about the public schema except that it exists by default. It can be dropped, too.

See also[Section 9.25](https://www.postgresql.org/docs/10/static/functions-info.html)for other ways to manipulate the schema search path.

The search path works in the same way for data type names, function names, and operator names as it does for table names. Data type and function names can be qualified in exactly the same way as table names. If you need to write a qualified operator name in an expression, there is a special provision: you must write

```
OPERATOR(schema.operator)
```

This is needed to avoid syntactic ambiguity. An example is:

```
SELECT 3 OPERATOR(pg_catalog.+) 4;
```

In practice one usually relies on the search path for operators, so as not to have to write anything so ugly as that.

### 5.8.4. Schemas and Privileges

By default, users cannot access any objects in schemas they do not own. To allow that, the owner of the schema must grant the`USAGE`privilege on the schema. To allow users to make use of the objects in the schema, additional privileges might need to be granted, as appropriate for the object.

A user can also be allowed to create objects in someone else's schema. To allow that, the`CREATE`privilege on the schema needs to be granted. Note that by default, everyone has`CREATE`and`USAGE`privileges on the schema`public`. This allows all users that are able to connect to a given database to create objects in its`public`schema. If you do not want to allow that, you can revoke that privilege:

```
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
```

\(The first“public”is the schema, the second“public”means“every user”. In the first sense it is an identifier, in the second sense it is a key word, hence the different capitalization; recall the guidelines from[Section 4.1.1](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-syntax-identifiers).\)

### 5.8.5. The System Catalog Schema

In addition to`public`and user-created schemas, each database contains a`pg_catalog`schema, which contains the system tables and all the built-in data types, functions, and operators.`pg_catalog`is always effectively part of the search path. If it is not named explicitly in the path then it is implicitly searched\_before\_searching the path's schemas. This ensures that built-in names will always be findable. However, you can explicitly place`pg_catalog`at the end of your search path if you prefer to have user-defined names override built-in names.

Since system table names begin with`pg_`, it is best to avoid such names to ensure that you won't suffer a conflict if some future version defines a system table named the same as your table. \(With the default search path, an unqualified reference to your table name would then be resolved as the system table instead.\) System tables will continue to follow the convention of having names beginning with`pg_`, so that they will not conflict with unqualified user-table names so long as users avoid the`pg_`prefix.

### 5.8.6. Usage Patterns

Schemas can be used to organize your data in many ways. There are a few usage patterns that are recommended and are easily supported by the default configuration:

* If you do not create any schemas then all users access the public schema implicitly. This simulates the situation where schemas are not available at all. This setup is mainly recommended when there is only a single user or a few cooperating users in a database. This setup also allows smooth transition from the non-schema-aware world.

* You can create a schema for each user with the same name as that user. Recall that the default search path starts with`$user`, which resolves to the user name. Therefore, if each user has a separate schema, they access their own schemas by default.

  If you use this setup then you might also want to revoke access to the public schema \(or drop it altogether\), so users are truly constrained to their own schemas.

* To install shared applications \(tables to be used by everyone, additional functions provided by third parties, etc.\), put them into separate schemas. Remember to grant appropriate privileges to allow the other users to access them. Users can then refer to these additional objects by qualifying the names with a schema name, or they can put the additional schemas into their search path, as they choose.

### 5.8.7. Portability

In the SQL standard, the notion of objects in the same schema being owned by different users does not exist. Moreover, some implementations do not allow you to create schemas that have a different name than their owner. In fact, the concepts of schema and user are nearly equivalent in a database system that implements only the basic schema support specified in the standard. Therefore, many users consider qualified names to really consist of`user_name`.`table_name`. This is howPostgreSQLwill effectively behave if you create a per-user schema for every user.

Also, there is no concept of a`public`schema in the SQL standard. For maximum conformance to the standard, you should not use \(perhaps even remove\) the`public`schema.

Of course, some SQL database systems might not implement schemas at all, or provide namespace support by allowing \(possibly limited\) cross-database access. If you need to work with those systems, then maximum portability would be achieved by not using schemas at all.

---

[^1]: [PostgreSQL: Documentation: 10: 5.8. Schemas](https://www.postgresql.org/docs/10/static/ddl-schemas.html)

