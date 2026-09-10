## F.7. btree_gin — 具有 B-tree 行為的 GIN 運算子類別 [#](#BTREE-GIN)

[F.7.1. 使用範例](btree-gin.md#BTREE-GIN-EXAMPLE-USAGE)

[F.7.2. 作者](btree-gin.md#BTREE-GIN-AUTHORS)

<a id="id-1.11.7.17.2"></a>

`btree_gin` 提供 GIN 運算子類別，為下列資料型別實作等同於 B-tree 的行為：`int2`、`int4`、`int8`、`float4`、`float8`、`timestamp with time zone`、`timestamp without time zone`、`time with time zone`、`time without time zone`、`date`、`interval`、`oid`、`money`、`"char"`、`varchar`、`text`、`bytea`、`bit`、`varbit`、`macaddr`、`macaddr8`、`inet`、`cidr`、`uuid`、`name`、`bool`、`bpchar` 及所有 `enum` 型別。

一般而言，這些運算子類別不會優於等效的標準 B-tree 索引方法，且缺少標準 B-tree 程式碼的一項主要功能：強制唯一性的能力。不過，它們適用於 GIN 測試，也可作為開發其他 GIN 運算子類別的基礎。此外，對同時測試可建立 GIN 索引欄位與可建立 B-tree 索引欄位的查詢，建立使用其中一個運算子類別的多欄位 GIN 索引，可能比建立兩個必須經由 bitmap AND 合併的獨立索引更有效率。

此模組被視為「受信任」，也就是可由在目前資料庫中具有 `CREATE` 權限的非超級使用者安裝。

<a id="BTREE-GIN-EXAMPLE-USAGE"></a>

### F.7.1. 使用範例 [#](#BTREE-GIN-EXAMPLE-USAGE)

```

CREATE TABLE test (a int4);
-- create index
CREATE INDEX testidx ON test USING GIN (a);
-- query
SELECT * FROM test WHERE a < 10;
```

<a id="BTREE-GIN-AUTHORS"></a>

### F.7.2. 作者 [#](#BTREE-GIN-AUTHORS)

Teodor Sigaev（`<teodor@stack.net>`）及 Oleg Bartunov（`<oleg@sai.msu.su>`）。其他資訊請參閱 <http://www.sai.msu.su/~megera/oddmuse/index.cgi/Gin>。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/btree-gin.html)
