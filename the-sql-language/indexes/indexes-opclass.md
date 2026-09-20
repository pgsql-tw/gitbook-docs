<a id="INDEXES-OPCLASS"></a>

## 11.10. 運算子類別與運算子族系 [#](#INDEXES-OPCLASS)

<a id="id-1.5.10.13.2"></a><a id="id-1.5.10.13.3"></a>

索引定義可以為索引的每個欄位指定一個*運算子類別*（operator class）。

```

CREATE INDEX name ON table (column opclass [ ( opclass_options ) ] [sort options] [, ...]);
```

運算子類別指定了索引在該欄位上所要使用的運算子。例如，建立在 `int4` 型別上的 B-tree 索引會使用 `int4_ops` 類別；這個運算子類別包含了用於 `int4` 型別值的比較函式。在實務上，欄位資料型別的預設運算子類別通常就已足夠。之所以要有運算子類別，主要是因為對某些資料型別而言，可能有不只一種有意義的索引行為。例如，我們可能想依絕對值或依實部來排序複數資料型別。我們可以為該資料型別定義兩個運算子類別，然後在建立索引時選擇適當的類別來做到這一點。運算子類別決定了基本的排序順序（之後可以藉由加上排序選項 `COLLATE`、`ASC`／`DESC` 和／或 `NULLS FIRST`／`NULLS LAST` 來修改）。

除了預設的運算子類別之外，還有一些內建的運算子類別：

* 運算子類別 `text_pattern_ops`、`varchar_pattern_ops` 與 `bpchar_pattern_ops` 分別支援 `text`、`varchar` 與 `char` 型別上的 B-tree 索引。它們與預設運算子類別的差別在於，值是嚴格地逐字元比較，而不是依照語系特定的定序規則比較。這使得當資料庫不使用標準的「C」語系時，這些運算子類別適合用於涉及模式比對運算式（`LIKE` 或 POSIX 正規表示式）的查詢。例如，你可以像這樣為 `varchar` 欄位建立索引：

  ```

  CREATE INDEX test_index ON test_table (col varchar_pattern_ops);
  ```

  請注意，如果你希望涉及一般 `<`、`<=`、`>` 或 `>=` 比較的查詢能使用索引，也應該以預設的運算子類別建立一個索引。這類查詢無法使用 `xxx_pattern_ops` 運算子類別。（不過，一般的相等比較可以使用這些運算子類別。）可以在同一個欄位上以不同的運算子類別建立多個索引。如果你確實使用 C 語系，就不需要 `xxx_pattern_ops` 運算子類別，因為在 C 語系中，使用預設運算子類別的索引就可用於模式比對查詢。

下列查詢會顯示所有已定義的運算子類別：

```

SELECT am.amname AS index_method,
       opc.opcname AS opclass_name,
       opc.opcintype::regtype AS indexed_type,
       opc.opcdefault AS is_default
    FROM pg_am am, pg_opclass opc
    WHERE opc.opcmethod = am.oid
    ORDER BY index_method, opclass_name;
```

運算子類別其實只是一個稱為*運算子族系*（operator family）之較大結構的子集。當好幾種資料型別具有相似的行為時，定義跨資料型別的運算子並讓它們能搭配索引使用，往往很有用。要做到這一點，各個型別的運算子類別必須歸入同一個運算子族系。跨型別的運算子是該族系的成員，但不與族系中任何單一類別相關聯。

先前查詢的這個擴充版本，會顯示每個運算子類別所屬的運算子族系：

```

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

這個查詢會顯示所有已定義的運算子族系，以及每個族系中包含的所有運算子：

```

SELECT am.amname AS index_method,
       opf.opfname AS opfamily_name,
       amop.amopopr::regoperator AS opfamily_operator
    FROM pg_am am, pg_opfamily opf, pg_amop amop
    WHERE opf.opfmethod = am.oid AND
          amop.amopfamily = opf.oid
    ORDER BY index_method, opfamily_name, opfamily_operator;
```

### 提示

[psql](../../reference/reference-client/app-psql.md) 有 `\dAc`、`\dAf` 與 `\dAo` 命令，它們提供了這些查詢稍微更進階的版本。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-opclass.html)（原文版本：18.6；核對日期：2026-09-15）
