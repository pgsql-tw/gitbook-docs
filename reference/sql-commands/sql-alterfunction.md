<a id="SQL-ALTERFUNCTION"></a><a id="id-1.9.3.14.1"></a>

## ALTER FUNCTION

ALTER FUNCTION — 變更函式的定義

<a id="id-1.9.3.14.4"></a>

## 語法

```

ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT
    IMMUTABLE | STABLE | VOLATILE
    [ NOT ] LEAKPROOF
    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    COST execution_cost
    ROWS result_rows
    SUPPORT support_function
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

<a id="id-1.9.3.14.5"></a>

## 說明

`ALTER FUNCTION` 會變更函式的定義。

你必須擁有該函式，才能使用 `ALTER FUNCTION`。若要變更函式的綱要，你還必須擁有新綱要的 `CREATE` 權限。若要變更擁有者，你必須能對新的擁有者角色執行 `SET ROLE`，且該角色必須擁有該函式所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立函式而做到的事。不過，超級使用者無論如何都可以變更任何函式的擁有權。）

<a id="id-1.9.3.14.6"></a>

## 參數

*`name`*
:   現有函式的名稱（可選擇以綱要限定）。若未指定引數列表，該名稱在其綱要中必須是唯一的。

*`argmode`*
:   引數的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。若省略，預設為 `IN`。請注意，`ALTER FUNCTION` 實際上並不會理會 `OUT` 引數，因為只需要輸入引數就能判定函式的身分。因此，列出 `IN`、`INOUT` 與 `VARIADIC` 引數就足夠了。

*`argname`*
:   引數的名稱。請注意，`ALTER FUNCTION` 實際上並不會理會引數名稱，因為只需要引數的資料型別就能判定函式的身分。

*`argtype`*
:   函式引數（若有的話）的資料型別（可選擇以綱要限定）。

*`new_name`*
:   函式的新名稱。

*`new_owner`*
:   函式的新擁有者。請注意，若函式被標記為 `SECURITY DEFINER`，之後它將以新擁有者的身分執行。

*`new_schema`*
:   函式的新綱要。

`DEPENDS ON EXTENSION extension_name`<br>`NO DEPENDS ON EXTENSION extension_name`
:   此形式會將函式標記為相依於該擴充功能；若指定 `NO`，則標記為不再相依於該擴充功能。被標記為相依於擴充功能的函式，會在該擴充功能被移除時一併被移除，即使未指定 `CASCADE` 也是如此。一個函式可以相依於多個擴充功能，並會在其中任何一個擴充功能被移除時被移除。

`CALLED ON NULL INPUT`<br>`RETURNS NULL ON NULL INPUT`<br>`STRICT`
:   `CALLED ON NULL INPUT` 會變更函式，使其在部分或全部引數為 null 時仍會被呼叫。`RETURNS NULL ON NULL INPUT` 或 `STRICT` 會變更函式，使其在任何引數為 null 時不被呼叫，而是自動假定結果為 null。更多資訊請參閱 [CREATE FUNCTION](sql-createfunction.md)。

`IMMUTABLE`<br>`STABLE`<br>`VOLATILE`
:   將函式的揮發性變更為指定的設定。細節請參閱 [CREATE FUNCTION](sql-createfunction.md)。

`[ EXTERNAL ] SECURITY INVOKER`<br>`[ EXTERNAL ] SECURITY DEFINER`
:   變更函式是否為 SECURITY DEFINER 函式。為了符合 SQL，關鍵字 `EXTERNAL` 會被忽略。關於此功能的更多資訊，請參閱 [CREATE FUNCTION](sql-createfunction.md)。

`PARALLEL`
:   變更函式是否被視為可安全地平行執行。細節請參閱 [CREATE FUNCTION](sql-createfunction.md)。

`LEAKPROOF`
:   變更函式是否被視為 leakproof（不洩漏資訊）。關於此功能的更多資訊，請參閱 [CREATE FUNCTION](sql-createfunction.md)。

`COST` *`execution_cost`*
:   變更函式的估計執行成本。更多資訊請參閱 [CREATE FUNCTION](sql-createfunction.md)。

`ROWS` *`result_rows`*
:   變更傳回集合之函式的估計傳回資料列數。更多資訊請參閱 [CREATE FUNCTION](sql-createfunction.md)。

`SUPPORT` *`support_function`*

設定或變更此函式要使用的規劃器支援函式。細節請參閱[第 36.11 節](../../server-programming/extend/xfunc-optimization.md)。你必須是超級使用者才能使用此選項。

此選項無法用來完全移除支援函式，因為它必須指名一個新的支援函式。若需要移除，請使用 `CREATE OR
REPLACE FUNCTION`。

*`configuration_parameter`*<br>*`value`*

新增或變更呼叫函式時要對組態參數進行的設定。若 *`value`* 為 `DEFAULT`，或等效地使用 `RESET`，則會移除函式本身的區域設定，使函式以其環境中現有的值執行。使用 `RESET
ALL` 可清除所有函式本身的區域設定。`SET FROM CURRENT` 會將執行 `ALTER FUNCTION` 時該參數的目前值，儲存為進入函式時要套用的值。

關於允許的參數名稱與值的更多資訊，請參閱 [SET](sql-set.md) 與[第 19 章](../../server-administration/runtime-config/README.md)。

`RESTRICT`
:   為符合 SQL 標準而接受，但會被忽略。

<a id="id-1.9.3.14.7"></a>

## 範例

將型別 `integer` 的函式 `sqrt` 重新命名為 `square_root`：

```

ALTER FUNCTION sqrt(integer) RENAME TO square_root;
```

將型別 `integer` 的函式 `sqrt` 的擁有者變更為 `joe`：

```

ALTER FUNCTION sqrt(integer) OWNER TO joe;
```

將型別 `integer` 的函式 `sqrt` 的綱要變更為 `maths`：

```

ALTER FUNCTION sqrt(integer) SET SCHEMA maths;
```

將型別 `integer` 的函式 `sqrt` 標記為相依於擴充功能 `mathlib`：

```

ALTER FUNCTION sqrt(integer) DEPENDS ON EXTENSION mathlib;
```

調整函式自動設定的搜尋路徑：

```

ALTER FUNCTION check_password(text) SET search_path = admin, pg_temp;
```

停用函式自動設定 `search_path`：

```

ALTER FUNCTION check_password(text) RESET search_path;
```

現在，函式會以其呼叫者所使用的搜尋路徑執行。

<a id="id-1.9.3.14.8"></a>

## 相容性

此陳述式與 SQL 標準中的 `ALTER
FUNCTION` 陳述式部分相容。標準允許修改函式的更多屬性，但不提供重新命名函式、將函式設為 SECURITY DEFINER、為函式附加組態參數值，或變更函式的擁有者、綱要或揮發性等功能。標準也要求使用 `RESTRICT` 關鍵字，而這在 PostgreSQL 中是選擇性的。

<a id="id-1.9.3.14.9"></a>

## 另請參閱

[CREATE FUNCTION](sql-createfunction.md), [DROP FUNCTION](sql-dropfunction.md), [ALTER PROCEDURE](sql-alterprocedure.md), [ALTER ROUTINE](sql-alterroutine.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterfunction.html)（原文版本：18.6；核對日期：2026-10-05）
