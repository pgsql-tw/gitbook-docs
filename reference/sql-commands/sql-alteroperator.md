<a id="SQL-ALTEROPERATOR"></a><a id="id-1.9.3.20.1"></a>

## ALTER OPERATOR

ALTER OPERATOR — 變更運算子的定義

<a id="id-1.9.3.20.4"></a>

## 語法

```

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    SET SCHEMA new_schema

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    SET ( {  RESTRICT = { res_proc | NONE }
           | JOIN = { join_proc | NONE }
           | COMMUTATOR = com_op
           | NEGATOR = neg_op
           | HASHES
           | MERGES
          } [, ... ] )
```

<a id="id-1.9.3.20.5"></a>

## 說明

`ALTER OPERATOR` 會變更運算子的定義。

你必須擁有該運算子，才能使用 `ALTER OPERATOR`。若要變更擁有者，你必須能對新的擁有者角色執行 `SET ROLE`，且該角色必須擁有該運算子所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立運算子而做到的事。不過，超級使用者無論如何都可以變更任何運算子的擁有權。）

<a id="id-1.9.3.20.6"></a>

## 參數

*`name`*
:   現有運算子的名稱（可選擇以綱要限定）。

*`left_type`*
:   運算子左運算元的資料型別；若運算子沒有左運算元，請寫 `NONE`。

*`right_type`*
:   運算子右運算元的資料型別。

*`new_owner`*
:   運算子的新擁有者。

*`new_schema`*
:   運算子的新綱要。

*`res_proc`*
:   此運算子的限制選擇率估算函式；寫 NONE 可移除既有的選擇率估算函式。

*`join_proc`*
:   此運算子的連接選擇率估算函式；寫 NONE 可移除既有的選擇率估算函式。

*`com_op`*
:   此運算子的交換子。只有在運算子尚未有交換子時才能變更。

*`neg_op`*
:   此運算子的否定子。只有在運算子尚未有否定子時才能變更。

`HASHES`
:   表示此運算子可以支援雜湊連接。只能啟用，不能停用。

`MERGES`
:   表示此運算子可以支援合併連接。只能啟用，不能停用。

<a id="id-1.9.3.20.7"></a>

## 注意事項

更多資訊請參閱[第 36.14 節](../../server-programming/extend/xoper.md)與[第 36.15 節](../../server-programming/extend/xoper-optimization.md)。

由於交換子是成對出現、互為彼此的交換子，`ALTER OPERATOR SET COMMUTATOR` 也會將 *`com_op`* 的交換子設為目標運算子。同樣地，`ALTER OPERATOR SET
NEGATOR` 也會將 *`neg_op`* 的否定子設為目標運算子。因此，除了目標運算子之外，你也必須擁有該交換子或否定子運算子。

<a id="id-1.9.3.20.8"></a>

## 範例

變更型別 `text` 的自訂運算子 `a @@ b` 的擁有者：

```

ALTER OPERATOR @@ (text, text) OWNER TO joe;
```

變更型別 `int[]` 的自訂運算子 `a && b` 的限制與連接選擇率估算函式：

```

ALTER OPERATOR && (int[], int[]) SET (RESTRICT = _int_contsel, JOIN = _int_contjoinsel);
```

將 `&&` 運算子標記為它自己的交換子：

```

ALTER OPERATOR && (int[], int[]) SET (COMMUTATOR = &&);
```

<a id="id-1.9.3.20.9"></a>

## 相容性

SQL 標準中沒有 `ALTER OPERATOR` 陳述式。

<a id="id-1.9.3.20.10"></a>

## 另請參閱

[CREATE OPERATOR](sql-createoperator.md), [DROP OPERATOR](sql-dropoperator.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alteroperator.html)（原文版本：18.6；核對日期：2026-10-05）
