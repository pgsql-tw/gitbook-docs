# 5.9. 繼承[^1]

PostgreSQL 實作了資料表的繼承方式，對於資料庫設計人員來說，將會是很好用的功能。（SQL:1999 之後定義了型別繼承的功能，但和這裡所介紹的方向有許多不同。）

我們直接以一個例子作為開始：假設我們嘗試建立「城市（city）」的資料模型。每一個州（state）都會有許多城市（city），但只會有一個首都（capital）。我們想要很快地可以找到某個州的首都。這件事我們需要建立兩個資料表，一個存放首都，而另一個記載非首都的城市。只是，當我們想要取得的是所有城市，不論是否為首都，似乎會有些麻煩？這時候繼承功能就可以幫助我們解決這個問題。我們可以定義一個資料表 capitals，它是由資料表 cities 繼承而來：

```
CREATE TABLE cities (
    name            text,
    population      float,
    altitude        int     -- in feet
);

CREATE TABLE capitals (
    state           char(2)
) INHERITS (cities);
```

在這個例子中，資料表 capitals 會繼承父資料表 cities 的所有欄位。只是 capitals 會多一個欄位 state，表示它是哪個州的首都。

在 PostgreSQL 裡，一個資料表可以繼承多個資料表，而一個查詢可以引用該資料表裡的所有資料列或在其所屬的資料表的資料列，後者的行為是預設的。舉個例子，下面的查詢可以列出所有海沷在 500 英呎以上的城市名稱，州的首都也包含在內：

```
SELECT name, altitude
    FROM cities
    WHERE altitude > 500;
```

使用 [2.1 節](/the-sql-language/21-introduction.md)中的範例資料，將會回傳：

```
   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
 Madison   |      845
```

換句話說，下面的查詢就會查出非首都且海沷超過 500 英呎以上的城市：

```
SELECT name, altitude
    FROM ONLY cities
    WHERE altitude > 500;

   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
```

這裡「ONLY」關鍵字指的是查詢只需要包含資料表 cities 就好，而不是任何繼承 cities 的資料表都包含在內。我們先前介紹過的指令：SELECT、UPDATE、和 DELETE，都可以使用 ONLY 關鍵字。

你也可以在資料表名稱後面加上「\*」，明確指出繼承的資料表都需要包含在內：

```
SELECT name, altitude
    FROM cities*
    WHERE altitude > 500;
```

注意這個「\*」並不是必要的，因為這個行為本來就是預設的。這個語法用於相容舊的版本，有些版本的預設行為可能不太一樣。

在某些例子裡，也許你會希望知道哪些資料列來自於哪個資料表。有一個系統欄位稱作 tableoid，每一個資料表都會有，而它可告訴你資料列的來源：

```
SELECT c.tableoid, c.name, c.altitude
FROM cities c
WHERE c.altitude > 500;
```

這將會回傳：

```
 tableoid |   name    | altitude
----------+-----------+----------
   139793 | Las Vegas |     2174
   139793 | Mariposa  |     1953
   139798 | Madison   |      845
```

（如果你嘗試重覆執行這個例子，你可能會得到不同的 OID 值。）藉由和資料表 pg\_class 交叉查詢，你可以看到實際的資料表名稱：

```
SELECT p.relname, c.name, c.altitude
FROM cities c, pg_class p
WHERE c.altitude > 500 AND c.tableoid = p.oid;
```

將會回傳：

```
 relname  |   name    | altitude
----------+-----------+----------
 cities   | Las Vegas |     2174
 cities   | Mariposa  |     1953
 capitals | Madison   |      845
```

另一個可以得到相同結果的方式是，使用 regclass 別名型別，這個型別會將 OID 轉換成名稱輸出：

```
SELECT c.tableoid::regclass, c.name, c.altitude
FROM cities c
WHERE c.altitude > 500;
```

在使用 INSERT 或 COPY 指令時，繼承並不會自動轉存資料。在我們的例子中，下面的 INSERT 指令將會失敗：

```
INSERT INTO cities (name, population, altitude, state)
VALUES ('Albany', NULL, NULL, 'NY');
```

我們可能會希望資料以某種方式轉送到資料表 capitals 中，但這不會發生：INSERT 指令永遠只會將資料插入到指定的資料表中。在某些情況下，如果設定了存取規則（[第 40 章](/v-server-programming/the-rule-system.md)）的話，那有可能做到類似的效果。然而，在這個例子下是沒有辦法執行的，因為資料表 cities 中並沒有一個欄位稱作 state，所以這個指令將會被拒絕執行，如果沒有其他規則被設定的話。

所有限制條件的檢查，還有非空值的限制，都會自動從父資料表繼承下來，除非特別使用 NO INHERIT 子句來設定拋棄繼承。而其他型態的限制條件（唯一性、主鍵、外部鍵）都不會自動繼承。

A table can inherit from more than one parent table, in which case it has the union of the columns defined by the parent tables. Any columns declared in the child table's definition are added to these. If the same column name appears in multiple parent tables, or in both a parent table and the child's definition, then these columns are“merged”so that there is only one such column in the child table. To be merged, columns must have the same data types, else an error is raised. Inheritable check constraints and not-null constraints are merged in a similar fashion. Thus, for example, a merged column will be marked not-null if any one of the column definitions it came from is marked not-null. Check constraints are merged if they have the same name, and the merge will fail if their conditions are different.

Table inheritance is typically established when the child table is created, using the`INHERITS`clause of the[CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html)statement. Alternatively, a table which is already defined in a compatible way can have a new parent relationship added, using the`INHERIT`variant of[ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html). To do this the new child table must already include columns with the same names and types as the columns of the parent. It must also include check constraints with the same names and check expressions as those of the parent. Similarly an inheritance link can be removed from a child using the`NO INHERIT`variant of`ALTER TABLE`. Dynamically adding and removing inheritance links like this can be useful when the inheritance relationship is being used for table partitioning \(see[Section 5.10](https://www.postgresql.org/docs/10/static/ddl-partitioning.html)\).

One convenient way to create a compatible table that will later be made a new child is to use the`LIKE`clause in`CREATE TABLE`. This creates a new table with the same columns as the source table. If there are any`CHECK`constraints defined on the source table, the`INCLUDING CONSTRAINTS`option to`LIKE`should be specified, as the new child must have constraints matching the parent to be considered compatible.

A parent table cannot be dropped while any of its children remain. Neither can columns or check constraints of child tables be dropped or altered if they are inherited from any parent tables. If you wish to remove a table and all of its descendants, one easy way is to drop the parent table with the`CASCADE`option \(see[Section 5.13](https://www.postgresql.org/docs/10/static/ddl-depend.html)\).

[ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html)will propagate any changes in column data definitions and check constraints down the inheritance hierarchy. Again, dropping columns that are depended on by other tables is only possible when using the`CASCADE`option.`ALTER TABLE`follows the same rules for duplicate column merging and rejection that apply during`CREATE TABLE`.

Inherited queries perform access permission checks on the parent table only. Thus, for example, granting`UPDATE`permission on the`cities`table implies permission to update rows in the`capitals`table as well, when they are accessed through`cities`. This preserves the appearance that the data is \(also\) in the parent table. But the`capitals`table could not be updated directly without an additional grant. In a similar way, the parent table's row security policies \(see[Section 5.7](https://www.postgresql.org/docs/10/static/ddl-rowsecurity.html)\) are applied to rows coming from child tables during an inherited query. A child table's policies, if any, are applied only when it is the table explicitly named in the query; and in that case, any policies attached to its parent\(s\) are ignored.

Foreign tables \(see[Section 5.11](https://www.postgresql.org/docs/10/static/ddl-foreign-data.html)\) can also be part of inheritance hierarchies, either as parent or child tables, just as regular tables can be. If a foreign table is part of an inheritance hierarchy then any operations not supported by the foreign table are not supported on the whole hierarchy either.

### 5.9.1. Caveats

Note that not all SQL commands are able to work on inheritance hierarchies. Commands that are used for data querying, data modification, or schema modification \(e.g.,`SELECT`,`UPDATE`,`DELETE`, most variants of`ALTER TABLE`, but not`INSERT`or`ALTER TABLE ... RENAME`\) typically default to including child tables and support the`ONLY`notation to exclude them. Commands that do database maintenance and tuning \(e.g.,`REINDEX`,`VACUUM`\) typically only work on individual, physical tables and do not support recursing over inheritance hierarchies. The respective behavior of each individual command is documented in its reference page \([SQL Commands](https://www.postgresql.org/docs/10/static/sql-commands.html)\).

A serious limitation of the inheritance feature is that indexes \(including unique constraints\) and foreign key constraints only apply to single tables, not to their inheritance children. This is true on both the referencing and referenced sides of a foreign key constraint. Thus, in the terms of the above example:

* If we declared`cities`.`name`to be`UNIQUE`or a`PRIMARY KEY`, this would not stop the`capitals`table from having rows with names duplicating rows in`cities`. And those duplicate rows would by default show up in queries from`cities`. In fact, by default`capitals`would have no unique constraint at all, and so could contain multiple rows with the same name. You could add a unique constraint to`capitals`, but this would not prevent duplication compared to`cities`.

* Similarly, if we were to specify that`cities`.`nameREFERENCES`some other table, this constraint would not automatically propagate to`capitals`. In this case you could work around it by manually adding the same`REFERENCES`constraint to`capitals`.

* Specifying that another table's column`REFERENCES cities(name)`would allow the other table to contain city names, but not capital names. There is no good workaround for this case.

These deficiencies will probably be fixed in some future release, but in the meantime considerable care is needed in deciding whether inheritance is useful for your application.

---

[^1]: [PostgreSQL: Documentation: 10: 5.9. Inheritance](https://www.postgresql.org/docs/10/static/ddl-inherit.html)

