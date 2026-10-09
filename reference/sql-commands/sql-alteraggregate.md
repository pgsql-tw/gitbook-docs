<a id="SQL-ALTERAGGREGATE"></a><a id="id-1.9.3.4.1"></a>

## ALTER AGGREGATE

ALTER AGGREGATE — 變更彙總函式的定義

<a id="id-1.9.3.4.4"></a>

## 語法

```

ALTER AGGREGATE name ( aggregate_signature ) RENAME TO new_name
ALTER AGGREGATE name ( aggregate_signature )
                OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER AGGREGATE name ( aggregate_signature ) SET SCHEMA new_schema

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

<a id="id-1.9.3.4.5"></a>

## 說明

`ALTER AGGREGATE` 會變更彙總函式的定義。

你必須是該彙總函式的擁有者才能使用 `ALTER AGGREGATE`。若要變更彙總函式的綱要，你還必須擁有新綱要的 `CREATE` 權限。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，且該角色必須擁有該彙總函式所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法透過刪除並重新建立該彙總函式來做到的事。不過，超級使用者無論如何都可以變更任何彙總函式的擁有權。）

<a id="id-1.9.3.4.6"></a>

## 參數

*`name`*
:   現有彙總函式的名稱（可選擇以綱要限定）。

*`argmode`*
:   引數的模式：`IN` 或 `VARIADIC`。若省略，預設為 `IN`。

*`argname`*
:   引數的名稱。請注意，`ALTER AGGREGATE` 實際上並不會理會引數名稱，因為只需要引數的資料型別就能決定彙總函式的身分。

*`argtype`*
:   彙總函式所操作的輸入資料型別。若要參照零引數的彙總函式，請以 `*` 取代引數規格清單。若要參照有序集合彙總函式，請在直接引數與彙總引數的規格之間寫上 `ORDER BY`。

*`new_name`*
:   彙總函式的新名稱。

*`new_owner`*
:   彙總函式的新擁有者。

*`new_schema`*
:   彙總函式的新綱要。

<a id="id-1.9.3.4.7"></a>

## 注意事項

參照有序集合彙總函式的建議語法，是在直接引數與彙總引數的規格之間寫上 `ORDER BY`，與 [`CREATE AGGREGATE`](sql-createaggregate.md) 中的寫法相同。不過，省略 `ORDER BY`，直接把直接引數與彙總引數的規格串成單一清單也可行。在這種簡寫形式中，若直接引數清單與彙總引數清單都使用了 `VARIADIC "any"`，則 `VARIADIC "any"` 只要寫一次。

<a id="id-1.9.3.4.8"></a>

## 範例

將型別 `integer` 的彙總函式 `myavg` 重新命名為 `my_average`：

```

ALTER AGGREGATE myavg(integer) RENAME TO my_average;
```

將型別 `integer` 的彙總函式 `myavg` 的擁有者變更為 `joe`：

```

ALTER AGGREGATE myavg(integer) OWNER TO joe;
```

將直接引數型別為 `float8`、彙總引數型別為 `integer` 的有序集合彙總函式 `mypercentile` 移到綱要 `myschema`：

```

ALTER AGGREGATE mypercentile(float8 ORDER BY integer) SET SCHEMA myschema;
```

這樣寫也可以：

```

ALTER AGGREGATE mypercentile(float8, integer) SET SCHEMA myschema;
```

<a id="id-1.9.3.4.9"></a>

## 相容性

SQL 標準中沒有 `ALTER AGGREGATE` 陳述式。

<a id="id-1.9.3.4.10"></a>

## 另請參閱

[CREATE AGGREGATE](sql-createaggregate.md), [DROP AGGREGATE](sql-dropaggregate.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alteraggregate.html)（原文版本：18.6；核對日期：2026-10-05）
