## F.8. btree_gist — 具有 B-tree 行為的 GiST 運算子類別 [#](#BTREE-GIST)

[F.8.1. 使用範例](btree-gist.md#BTREE-GIST-EXAMPLE-USAGE)

[F.8.2. 作者](btree-gist.md#BTREE-GIST-AUTHORS)

<a id="id-1.11.7.18.2"></a>

`btree_gist` 提供 GiST 索引運算子類別，為下列資料型別實作等同於 B-tree 的行為：`int2`、`int4`、`int8`、`float4`、`float8`、`numeric`、`timestamp with time zone`、`timestamp without time zone`、`time with time zone`、`time without time zone`、`date`、`interval`、`oid`、`money`、`char`、`varchar`、`text`、`bytea`、`bit`、`varbit`、`macaddr`、`macaddr8`、`inet`、`cidr`、`uuid`、`bool` 及所有 `enum` 型別。

一般而言，這些運算子類別不會優於等效的標準 B-tree 索引方法，且缺少標準 B-tree 程式碼的一項主要功能：強制唯一性的能力。不過，如下所述，它們提供一些 B-tree 索引沒有的其他功能。此外，當需要多欄位 GiST 索引，而其中部分欄位的資料型別只能使用 GiST 建立索引，其他欄位則只是簡單資料型別時，這些運算子類別很有用。最後，它們也適用於 GiST 測試，以及作為開發其他 GiST 運算子類別的基礎。

除了典型 B-tree 搜尋運算子外，`btree_gist` 也為 `<>`（「不等於」）提供索引支援。如後文所述，這可能適合與[排除限制條件](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-EXCLUDE)搭配使用。

此外，對於具有自然距離度量的資料型別，`btree_gist` 定義距離運算子 `<->`，並為使用此運算子的最近鄰搜尋提供 GiST 索引支援。`int2`、`int4`、`int8`、`float4`、`float8`、`timestamp with time zone`、`timestamp without time zone`、`time without time zone`、`date`、`interval`、`oid` 與 `money` 都提供距離運算子。

預設情況下，`btree_gist` 會以*已排序*模式使用 `sortsupport` 建置 GiST 索引，通常可大幅加快索引建置速度。建立索引時仍可使用 `buffering` 參數，改回緩衝式建置策略。

此模組被視為「受信任」，也就是可由在目前資料庫中具有 `CREATE` 權限的非超級使用者安裝。

<a id="BTREE-GIST-EXAMPLE-USAGE"></a>

### F.8.1. 使用範例 [#](#BTREE-GIST-EXAMPLE-USAGE)

使用 `btree_gist` 取代 `btree` 的簡單範例：

```

CREATE TABLE test (a int4);
-- create index
CREATE INDEX testidx ON test USING GIST (a);
-- query
SELECT * FROM test WHERE a < 10;
-- nearest-neighbor search: find the ten entries closest to "42"
SELECT *, a <-> 42 AS dist FROM test ORDER BY a <-> 42 LIMIT 10;
```

使用[排除限制條件](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-EXCLUDE)，強制動物園中的一個籠子只能容納一種動物：

```

=> CREATE TABLE zoo (
  cage   INTEGER,
  animal TEXT,
  EXCLUDE USING GIST (cage WITH =, animal WITH <>)
);

=> INSERT INTO zoo VALUES(123, 'zebra');
INSERT 0 1
=> INSERT INTO zoo VALUES(123, 'zebra');
INSERT 0 1
=> INSERT INTO zoo VALUES(123, 'lion');
ERROR:  conflicting key value violates exclusion constraint "zoo_cage_animal_excl"
DETAIL:  Key (cage, animal)=(123, lion) conflicts with existing key (cage, animal)=(123, zebra).
=> INSERT INTO zoo VALUES(124, 'lion');
INSERT 0 1
```

<a id="BTREE-GIST-AUTHORS"></a>

### F.8.2. 作者 [#](#BTREE-GIST-AUTHORS)

Teodor Sigaev (`<teodor@stack.net>`),
Oleg Bartunov (`<oleg@sai.msu.su>`),
Janko Richter (`<jankorichter@yahoo.de>`), and
Paul Jungwirth（`<pj@illuminatedcomputing.com>`）。其他資訊請參閱 <http://www.sai.msu.su/~megera/postgres/gist/>。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/btree-gist.html)
