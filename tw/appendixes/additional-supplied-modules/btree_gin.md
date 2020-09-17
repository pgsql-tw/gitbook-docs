# F.6. btree\_gin

`btree_gin` provides sample GIN operator classes that implement B-tree equivalent behavior for the data types `int2`, `int4`, `int8`, `float4`, `float8`, `timestamp with time zone`, `timestamp without time zone`, `time with time zone`, `time without time zone`, `date`, `interval`, `oid`, `money`, `"char"`, `varchar`, `text`, `bytea`, `bit`, `varbit`, `macaddr`, `macaddr8`, `inet`, `cidr`, `uuid`, `name`, `bool`, `bpchar`, and all `enum` types.

通常，這些運算子類不會優於等效的標準 B-tree 索引方法，並且它們缺少標準 B-tree 的一個主要功能：強制執行唯一性。但是，它們對於 GIN 測試很有用，並且可以作為開發其他 GIN 運算子類的基礎。同樣地，對於同時測試可索引 GIN 欄位和 B-tree 可索引列的查詢，建立使用這些運算子之一的多欄位 GIN 索引可能比建立兩個必須獨立的索引更有效，以 bitmap ANDing 的方式。

## F.6.1. 使用範例

```text
CREATE TABLE test (a int4);
-- create index
CREATE INDEX testidx ON test USING GIN (a);
-- query
SELECT * FROM test WHERE a < 10;
```

## F.6.2. 作者們

Teodor Sigaev \(`<`[`teodor@stack.net`](mailto:teodor@stack.net)`>`\) and Oleg Bartunov \(`<`[`oleg@sai.msu.su`](mailto:oleg@sai.msu.su)`>`\). See [http://www.sai.msu.su/~megera/oddmuse/index.cgi/Gin](http://www.sai.msu.su/~megera/oddmuse/index.cgi/Gin) for additional information.

