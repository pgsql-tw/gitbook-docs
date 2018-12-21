# 11.9. 運算子物件及家族

索引定義可以為索引的每個欄位指定運算子類。

```text
CREATE INDEX name ON table (column opclass [sort options] [, ...]);
```

運算子類標示該欄位的索引所要使用的運算子。例如，int4 型別的 B-tree 索引將使用 int4\_ops 類；此運算子類包含 int4 型別的比較函數。實際上，欄位的資料型別的預設運算子類通常就足夠了。指定運算子類的主要原因是對於某些資料型別，可能存在多個有意義的索引行為。例如，我們可能希望按絕對值或複數的實部資料型別進行排序。我們可以透過為資料型別定義兩個運算子類，然後在建立索引時選擇適當的子類來實現。運算子類決定基本排序順序（然後可以通過增加排序選項 COLLATE，ASC / DESC 和 NULLS FIRST / NULLS LAST 來變更）。

除了預設的子類之外，還有一些內建的運算子類：

* 運算子類 text\_pattern\_ops，varchar\_pattern\_ops 和 bpchar\_pattern\_ops 分別支援型別 text，varchar 和 char 上的 B-tree 索引。與預設運算子類的不同之處在於，這些值嚴格按字元進行比較，而不是根據特定於語言環境的排序規則進行比較。這使得當資料庫不使用標準“C”語言環境時，這些運算子類適合於涉及樣式匹配表示式（LIKE 或 POSIX 正規表示式）的查詢。 例如，您可以像這樣索引 varchar 欄位：

  ```text
  CREATE INDEX test_index ON test_table (col varchar_pattern_ops);
  ```

  請注意，如果希望涉及普通 &lt;，&lt;=，&gt; 或 &gt;= 比較的查詢使用索引，還應使用預設運算子類建立索引。此類查詢不能使用 xxx\_pattern\_ops 運算子類。（但是，普通的相等比較可以使用這些運算子類。）可以使用不同的運算子類在同一欄位上建立多個索引。如果確實使用了「C語言」（C locale）環境，則不需要 xxx\_pattern\_ops 運算子類，因為具有預設運算子類的索引可用於「C」語言環境中的樣式匹配查詢。

以下查詢顯示所有已定義的運算子類：

```text
SELECT am.amname AS index_method,
       opc.opcname AS opclass_name,
       opc.opcintype::regtype AS indexed_type,
       opc.opcdefault AS is_default
    FROM pg_am am, pg_opclass opc
    WHERE opc.opcmethod = am.oid
    ORDER BY index_method, opclass_name;
```

運算子類實際上只是一個稱為運算子族的較大結構的子集。 在多個資料型別具有相似行為的情況下，定義跨資料型別運算子並允許它們使用索引通常很有用。為此，必須將每種型別的運算子類分組到同一運算子族中。跨型別運算子是該族的成員，但不與該族中的任何單個子類相關聯。

上一個查詢的延伸版本顯示了每個運算子類所屬的運算子族：

```text
SELECT am.amname AS index_method,
       opc.opcname AS opclass_name,
       opf.opfname AS opfamily_name,
       opc.opcintype::regtype AS indexed_type,
       opc.opcdefault AS is_default
    FROM pg_am am, pg_opclass opc, pg_opfamily opf
    WHERE opc.opcmethod = am.oid AND
          opc.opcfamily = opf.oid
    ORDER BY index_method, opclass_name;
```

此查詢顯示所有已定義的運算子系列以及每個系列中包含的所有運算子：

```text
SELECT am.amname AS index_method,
       opf.opfname AS opfamily_name,
       amop.amopopr::regoperator AS opfamily_operator
    FROM pg_am am, pg_opfamily opf, pg_amop amop
    WHERE opf.opfmethod = am.oid AND
          amop.amopfamily = opf.oid
    ORDER BY index_method, opfamily_name, opfamily_operator;
```

