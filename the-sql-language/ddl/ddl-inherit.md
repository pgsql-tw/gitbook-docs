<a id="DDL-INHERIT"></a>

## 5.11. 繼承 [#](#DDL-INHERIT)

[5.11.1. 注意事項](ddl-inherit.md#DDL-INHERIT-CAVEATS)

<a id="id-1.5.4.13.2"></a><a id="id-1.5.4.13.3"></a>

PostgreSQL 實作了資料表繼承，這對資料庫設計人員來說可能是很有用的工具。（SQL:1999 及之後的標準定義了一種型別繼承功能，它在許多方面都與這裡所描述的功能不同。）

讓我們從一個範例開始：假設我們要為城市建立資料模型。每個州有許多城市，但只有一個首府。我們希望能夠快速取得任一特定州的首府。這可以藉由建立兩個資料表來做到，一個用於州首府，另一個用於非首府的城市。不過，當我們想查詢某個城市的資料，而不管它是否為首府時，會發生什麼事呢？繼承功能可以幫助解決這個問題。我們將 `capitals` 資料表定義為繼承自 `cities`：

```

CREATE TABLE cities (
    name            text,
    population      float,
    elevation       int     -- in feet
);

CREATE TABLE capitals (
    state           char(2)
) INHERITS (cities);
```

在這個例子中，`capitals` 資料表*繼承*了其父資料表 `cities` 的所有欄位。州首府還多了一個額外的欄位 `state`，用來顯示它們所屬的州。

在 PostgreSQL 中，一個資料表可以繼承零個或多個其他資料表，而查詢可以參照資料表的所有資料列，或是資料表的所有資料列再加上其所有後代資料表的資料列。後者是預設的行為。例如，下面的查詢會找出所有位於海拔 500 英尺以上之城市的名稱，包括州首府在內：

```

SELECT name, elevation
    FROM cities
    WHERE elevation > 500;
```

以 PostgreSQL 教學中的範例資料（請參閱[第 2.1 節](../../tutorial/tutorial-sql/tutorial-sql-intro.md)）而言，這會回傳：

```

   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
 Madison   |       845
```

另一方面，下面的查詢會找出所有不是州首府、且位於海拔 500 英尺以上的城市：

```

SELECT name, elevation
    FROM ONLY cities
    WHERE elevation > 500;

   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
```

在這裡，`ONLY` 關鍵字表示查詢應該只套用到 `cities`，而不套用到繼承階層中位於 `cities` 之下的任何資料表。我們已經討論過的許多命令——`SELECT`、`UPDATE` 與 `DELETE`——都支援 `ONLY` 關鍵字。

你也可以在資料表名稱後面加上 `*`，明確指定要包含後代資料表：

```

SELECT name, elevation
    FROM cities*
    WHERE elevation > 500;
```

寫出 `*` 並不是必要的，因為這一向是預設的行為。不過，為了與可以更改預設值的舊版本相容，這個語法仍然受到支援。

在某些情況下，你可能想知道某筆資料列來自哪一個資料表。每個資料表中都有一個名為 `tableoid` 的系統欄位，可以告訴你資料列的來源資料表：

```

SELECT c.tableoid, c.name, c.elevation
FROM cities c
WHERE c.elevation > 500;
```

這會回傳：

```

 tableoid |   name    | elevation
----------+-----------+-----------
   139793 | Las Vegas |      2174
   139793 | Mariposa  |      1953
   139798 | Madison   |       845
```

（如果你試著重現這個範例，得到的 OID 數值很可能會不同。）藉由與 `pg_class` 進行聯結，你就可以看到實際的資料表名稱：

```

SELECT p.relname, c.name, c.elevation
FROM cities c, pg_class p
WHERE c.elevation > 500 AND c.tableoid = p.oid;
```

這會回傳：

```

 relname  |   name    | elevation
----------+-----------+-----------
 cities   | Las Vegas |      2174
 cities   | Mariposa  |      1953
 capitals | Madison   |       845
```

另一種達到相同效果的方法是使用 `regclass` 別名型別，它會以符號形式印出資料表的 OID：

```

SELECT c.tableoid::regclass, c.name, c.elevation
FROM cities c
WHERE c.elevation > 500;
```

繼承並不會自動將 `INSERT` 或 `COPY` 命令的資料傳播到繼承階層中的其他資料表。在我們的範例中，下面的 `INSERT` 陳述式會失敗：

```

INSERT INTO cities (name, population, elevation, state)
VALUES ('Albany', NULL, NULL, 'NY');
```

我們也許會希望資料能以某種方式被導向到 `capitals` 資料表，但這並不會發生：`INSERT` 一定只會插入到所指定的那個資料表。在某些情況下，可以使用規則（請參閱[第 39 章](../../server-programming/rules/README.md)）來重新導向插入操作。不過，這對上面的情況沒有幫助，因為 `cities` 資料表不包含 `state` 欄位，所以該命令在規則能夠套用之前就會被拒絕。

父資料表上的所有檢查限制條件與非 null 限制條件，都會自動被其子資料表繼承，除非以 `NO INHERIT` 子句明確另行指定。其他類型的限制條件（唯一、主鍵與外鍵限制條件）則不會被繼承。

一個資料表可以繼承多個父資料表，在這種情況下，它擁有由各父資料表所定義之欄位的聯集。子資料表定義中所宣告的任何欄位都會加入其中。如果相同的欄位名稱出現在多個父資料表中，或同時出現在父資料表與子資料表的定義中，這些欄位就會被「合併」，使子資料表中只有一個這樣的欄位。要能合併，欄位必須具有相同的資料型別，否則會引發錯誤。可繼承的檢查限制條件與非 null 限制條件也會以類似的方式合併。因此，例如只要合併來源中任何一個欄位定義被標記為非 null，合併後的欄位就會被標記為非 null。檢查限制條件如果名稱相同就會被合併，而如果它們的條件不同，合併就會失敗。

資料表繼承通常是在建立子資料表時，使用 [`CREATE TABLE`](../../reference/sql-commands/sql-createtable.md) 陳述式的 `INHERITS` 子句來建立的。另外，對於一個已經以相容方式定義好的資料表，也可以使用 [`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) 的 `INHERIT` 變化形式，為它加入新的父資料表關係。要這麼做，新的子資料表必須已經包含與父資料表欄位同名、同型別的欄位。它也必須包含與父資料表同名且檢查運算式相同的檢查限制條件。同樣地，可以使用 `ALTER TABLE` 的 `NO INHERIT` 變化形式，從子資料表移除繼承連結。當繼承關係被用於資料表分割（請參閱[第 5.12 節](ddl-partitioning.md)）時，像這樣動態地加入與移除繼承連結可能會很有用。

要建立一個之後會成為新子資料表的相容資料表，一種方便的方式是在 `CREATE TABLE` 中使用 `LIKE` 子句。這會建立一個與來源資料表具有相同欄位的新資料表。如果來源資料表上定義了任何 `CHECK` 限制條件，就應該為 `LIKE` 指定 `INCLUDING CONSTRAINTS` 選項，因為新的子資料表必須具有與父資料表相符的限制條件，才會被視為相容。

只要還有任何子資料表存在，父資料表就不能被刪除。子資料表的欄位或檢查限制條件，如果是從任何父資料表繼承而來的，也不能被刪除或修改。如果你想移除一個資料表及其所有後代，一種簡單的方式是以 `CASCADE` 選項刪除父資料表（請參閱[第 5.15 節](ddl-depend.md)）。

`ALTER TABLE` 會將欄位資料定義與檢查限制條件的任何變更，沿著繼承階層向下傳播。同樣地，只有在使用 `CASCADE` 選項時，才能刪除被其他資料表依賴的欄位。`ALTER TABLE` 在合併與拒絕重複欄位時，遵循與 `CREATE TABLE` 相同的規則。

繼承查詢只會對父資料表進行存取權限檢查。因此，例如授予 `cities` 資料表的 `UPDATE` 權限，也就意味著在透過 `cities` 存取時，有權限更新 `capitals` 資料表中的資料列。這維持了資料（也）位於父資料表中的表象。但若沒有額外的授權，就無法直接更新 `capitals` 資料表。類似地，在繼承查詢期間，父資料表的資料列安全政策（請參閱[第 5.9 節](ddl-rowsecurity.md)）會套用到來自子資料表的資料列上。子資料表自己的政策（如果有的話）只有在它是查詢中明確指名的資料表時才會套用；而在這種情況下，附加在其父資料表上的任何政策都會被忽略。

外部資料表（請參閱[第 5.13 節](ddl-foreign-data.md)）也可以像一般資料表一樣，作為父資料表或子資料表成為繼承階層的一部分。如果外部資料表是繼承階層的一部分，那麼該外部資料表不支援的任何操作，在整個階層上也都不受支援。

<a id="DDL-INHERIT-CAVEATS"></a>

### 5.11.1. 注意事項 [#](#DDL-INHERIT-CAVEATS)

請注意，並非所有 SQL 命令都能作用在繼承階層上。用於資料查詢、資料修改或綱要修改的命令（例如 `SELECT`、`UPDATE`、`DELETE`、`ALTER TABLE` 的大多數變化形式，但不包括 `INSERT` 或 `ALTER TABLE ... RENAME`），通常預設會包含子資料表，並支援以 `ONLY` 表示法將它們排除。大多數進行資料庫維護與調校的命令（例如 `REINDEX`）只作用在個別的實體資料表上，不支援在繼承階層上遞迴。不過，`VACUUM` 與 `ANALYZE` 命令預設都會包含子資料表，並支援以 `ONLY` 表示法將它們排除。每個命令各自的行為，都記載在其參考頁面中（[SQL 命令](../../reference/sql-commands/README.md)）。

繼承功能的一項嚴重限制是，索引（包括唯一限制條件）與外鍵限制條件只適用於單一資料表，而不適用於其繼承子資料表。在外鍵限制條件的參照端與被參照端都是如此。因此，以上面的範例來說：

* 如果我們將 `cities`.`name` 宣告為 `UNIQUE` 或 `PRIMARY KEY`，這並不會阻止 `capitals` 資料表中出現與 `cities` 中資料列名稱重複的資料列。而且這些重複的資料列預設會出現在對 `cities` 的查詢中。事實上，`capitals` 預設完全沒有唯一限制條件，因此可能包含多筆同名的資料列。你可以為 `capitals` 加上唯一限制條件，但這並不能防止它與 `cities` 之間的重複。
* 同樣地，如果我們指定 `cities`.`name` `REFERENCES` 某個其他資料表，這個限制條件並不會自動傳播到 `capitals`。在這種情況下，你可以手動為 `capitals` 加上相同的 `REFERENCES` 限制條件來因應。
* 指定另一個資料表的欄位 `REFERENCES cities(name)`，會讓該資料表可以包含城市名稱，但不能包含首府名稱。這種情況沒有好的因應辦法。

有些沒有為繼承階層實作的功能，已經為宣告式分割實作了。在決定以舊有的繼承方式進行分割對你的應用程式是否有用時，需要相當謹慎。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-inherit.html)（原文版本：18.6；核對日期：2026-09-11）
