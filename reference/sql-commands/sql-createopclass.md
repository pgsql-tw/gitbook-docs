<a id="id-1.9.3.73.1"></a>

## CREATE OPERATOR CLASS

CREATE OPERATOR CLASS — 定義新的運算子類別

## 語法

```

CREATE OPERATOR CLASS name [ DEFAULT ] FOR TYPE data_type
  USING index_method [ FAMILY family_name ] AS
  {  OPERATOR strategy_number operator_name [ ( op_type, op_type ) ] [ FOR SEARCH | FOR ORDER BY sort_family_name ]
   | FUNCTION support_number [ ( op_type [ , op_type ] ) ] function_name ( argument_type [, ...] )
   | STORAGE storage_type
  } [, ... ]
```

<a id="id-1.9.3.73.5"></a>

## 說明

`CREATE OPERATOR CLASS` 會建立新的運算子類別。運算子類別定義特定資料型別如何搭配索引使用。它指定某些運算子在該資料型別與索引方法中應扮演的角色或「策略」，也指定當索引欄位選用該運算子類別時，索引方法要使用的支援函式。建立運算子類別前，必須先定義它使用的所有運算子與函式。

若給定 schema 名稱，運算子類別會建立在指定的 schema；否則會建立在目前 schema。相同 schema 中的兩個運算子類別，只有在它們對應不同索引方法時才能同名。

定義運算子類別的使用者會成為其擁有者。目前建立者必須是超級使用者。（此限制是因為錯誤的運算子類別定義可能使伺服器混亂甚至當機。）

`CREATE OPERATOR CLASS` 目前不檢查運算子類別定義是否包含索引方法所需的所有運算子與函式，也不檢查運算子與函式是否構成自洽的集合。定義有效的運算子類別是使用者的責任。

相關的運算子類別可歸入*運算子家族*。若要將新的運算子類別加入既有家族，請在 `CREATE OPERATOR CLASS` 中指定 `FAMILY` 選項。未指定時，新類別會放入與新類別同名的家族（若不存在則建立）。

更多資訊請參閱[第 36.16 節](../../server-programming/extend/xindex.md)。

<a id="id-1.9.3.73.6"></a>

## 參數

*`name`*
:   要建立之運算子類別的名稱，可使用 schema 限定。

`DEFAULT`
:   若指定，該運算子類別會成為其資料型別的預設運算子類別。特定資料型別與索引方法最多只能有一個預設運算子類別。

*`data_type`*
:   此運算子類別所對應的欄位資料型別。

*`index_method`*
:   此運算子類別所對應的索引方法名稱。

*`family_name`*
:   要將此運算子類別加入的既有運算子家族名稱。未指定時，使用與運算子類別同名的家族（若不存在則建立）。

*`strategy_number`*
:   索引方法中與運算子類別相關運算子的策略編號。

*`operator_name`*
:   與運算子類別相關之運算子的名稱（可使用 schema 限定）。

*`op_type`*
:   在 `OPERATOR` 子句中，運算子的運算元資料型別；`NONE` 表示前綴運算子。一般情況下，運算元資料型別與運算子類別資料型別相同，可省略。在 `FUNCTION` 子句中，若函式要支援的運算元資料型別不同於函式的輸入資料型別（B-tree 比較函式與雜湊函式），或不同於類別的資料型別（B-tree 排序支援函式、B-tree equal image 函式及 GiST、SP-GiST、GIN、BRIN 運算子類別的所有函式），則指定它。這些預設值正確，因此 `FUNCTION` 子句通常不需指定 *`op_type`*；例外是要支援跨資料型別比較的 B-tree 排序支援函式。

*`sort_family_name`*
:   描述排序運算子相關排序順序之既有 `btree` 運算子家族名稱（可使用 schema 限定）。若 `FOR SEARCH` 與 `FOR ORDER BY` 均未指定，預設為 `FOR SEARCH`。

*`support_number`*
:   索引方法中與運算子類別相關函式的支援函式編號。

*`function_name`*
:   作為此運算子類別索引方法支援函式的函式名稱（可使用 schema 限定）。

*`argument_type`*
:   函式的參數資料型別。

*`storage_type`*
:   實際儲存在索引中的資料型別。通常與欄位資料型別相同，但某些索引方法（目前為 GiST、GIN、SP-GiST 和 BRIN）允許不同。除非索引方法允許不同型別，否則必須省略 `STORAGE` 子句。若欄位 *`data_type`* 指定為 `anyarray`，可將 *`storage_type`* 宣告為 `anyelement`，表示索引項目是各個特定索引所建立之實際陣列型別的元素型別成員。

`OPERATOR`、`FUNCTION` 與 `STORAGE` 子句可按任何順序出現。

<a id="id-1.9.3.73.7"></a>

## 注意事項

由於索引機制在使用函式前不檢查其存取權限，將函式或運算子納入運算子類別，等同於授予所有人執行它的權限。對運算子類別有用的函式通常不會有此問題。

不應以 SQL 函式定義運算子。SQL 函式很可能被內嵌至呼叫查詢，導致最佳化器無法辨識查詢符合索引。

<a id="id-1.9.3.73.8"></a>

## 範例

下列範例命令為資料型別 `_int4`（`int4` 的陣列）定義 GiST 索引運算子類別。完整範例請參閱 [intarray](../../appendixes/contrib/intarray.md) 模組。

```

CREATE OPERATOR CLASS gist__int_ops
    DEFAULT FOR TYPE _int4 USING gist AS
        OPERATOR        3       &&,
        OPERATOR        6       = (anyarray, anyarray),
        OPERATOR        7       @>,
        OPERATOR        8       <@,
        OPERATOR        20      @@ (_int4, query_int),
        FUNCTION        1       g_int_consistent (internal, _int4, smallint, oid, internal),
        FUNCTION        2       g_int_union (internal, internal),
        FUNCTION        3       g_int_compress (internal),
        FUNCTION        4       g_int_decompress (internal),
        FUNCTION        5       g_int_penalty (internal, internal, internal),
        FUNCTION        6       g_int_picksplit (internal, internal),
        FUNCTION        7       g_int_same (_int4, _int4, internal);
```

<a id="id-1.9.3.73.9"></a>

## 相容性

`CREATE OPERATOR CLASS` 是 PostgreSQL 擴充功能。SQL 標準沒有 `CREATE OPERATOR CLASS` 陳述式。

<a id="id-1.9.3.73.10"></a>

## 參閱

[ALTER OPERATOR CLASS](sql-alteropclass.md), [DROP OPERATOR CLASS](sql-dropopclass.md), [CREATE OPERATOR FAMILY](sql-createopfamily.md), [ALTER OPERATOR FAMILY](sql-alteropfamily.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createopclass.html)（原文版本：18.6；核對日期：2026-09-06）
