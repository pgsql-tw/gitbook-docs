<a id="SQL-ALTERPROCEDURE"></a><a id="id-1.9.3.24.1"></a>

## ALTER PROCEDURE

ALTER PROCEDURE — 變更程序的定義

<a id="id-1.9.3.24.4"></a>

## 語法

```

ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

<a id="id-1.9.3.24.5"></a>

## 說明

`ALTER PROCEDURE` 會變更程序的定義。

你必須擁有該程序，才能使用 `ALTER PROCEDURE`。若要變更程序的綱要，你還必須擁有新綱要的 `CREATE` 權限。若要變更擁有者，你必須能對新的擁有者角色執行 `SET ROLE`，且該角色必須擁有該程序所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立程序而做到的事。不過，超級使用者無論如何都可以變更任何程序的擁有權。）

<a id="id-1.9.3.24.6"></a>

## 參數

*`name`*
:   現有程序的名稱（可選擇以綱要限定）。若未指定引數列表，該名稱在其綱要中必須是唯一的。

*`argmode`*
:   引數的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。若省略，預設為 `IN`。

*`argname`*
:   引數的名稱。請注意，`ALTER PROCEDURE` 實際上並不會理會引數名稱，因為只有引數的資料型別會用來判定程序的身分。

*`argtype`*
:   程序引數（若有的話）的資料型別（可選擇以綱要限定）。關於如何使用引數資料型別查找程序的細節，請參閱 [DROP PROCEDURE](sql-dropprocedure.md)。

*`new_name`*
:   程序的新名稱。

*`new_owner`*
:   程序的新擁有者。請注意，若程序被標記為 `SECURITY DEFINER`，之後它將以新擁有者的身分執行。

*`new_schema`*
:   程序的新綱要。

*`extension_name`*
:   此形式會將程序標記為相依於該擴充功能；若指定 `NO`，則標記為不再相依於該擴充功能。被標記為相依於擴充功能的程序，會在該擴充功能被移除時一併被移除，即使未指定 CASCADE 也是如此。一個程序可以相依於多個擴充功能，並會在其中任何一個擴充功能被移除時被移除。

`[ EXTERNAL ] SECURITY INVOKER`<br>`[ EXTERNAL ] SECURITY DEFINER`
:   變更程序是否為 SECURITY DEFINER 程序。為了符合 SQL，關鍵字 `EXTERNAL` 會被忽略。關於此功能的更多資訊，請參閱 [CREATE PROCEDURE](sql-createprocedure.md)。

*`configuration_parameter`*<br>*`value`*
:   新增或變更呼叫程序時要對組態參數進行的設定。若 *`value`* 為 `DEFAULT`，或等效地使用 `RESET`，則會移除程序本身的區域設定，使程序以其環境中現有的值執行。使用 `RESET
    ALL` 可清除所有程序本身的區域設定。`SET FROM CURRENT` 會將執行 `ALTER PROCEDURE` 時該參數的目前值，儲存為進入程序時要套用的值。

    關於允許的參數名稱與值的更多資訊，請參閱 [SET](sql-set.md) 與[第 19 章](../../server-administration/runtime-config/README.md)。

`RESTRICT`
:   為符合 SQL 標準而接受，但會被忽略。

<a id="id-1.9.3.24.7"></a>

## 範例

將具有兩個 `integer` 型別引數的程序 `insert_data` 重新命名為 `insert_record`：

```

ALTER PROCEDURE insert_data(integer, integer) RENAME TO insert_record;
```

將具有兩個 `integer` 型別引數的程序 `insert_data` 的擁有者變更為 `joe`：

```

ALTER PROCEDURE insert_data(integer, integer) OWNER TO joe;
```

將具有兩個 `integer` 型別引數的程序 `insert_data` 的綱要變更為 `accounting`：

```

ALTER PROCEDURE insert_data(integer, integer) SET SCHEMA accounting;
```

將程序 `insert_data(integer, integer)` 標記為相依於擴充功能 `myext`：

```

ALTER PROCEDURE insert_data(integer, integer) DEPENDS ON EXTENSION myext;
```

調整程序自動設定的搜尋路徑：

```

ALTER PROCEDURE check_password(text) SET search_path = admin, pg_temp;
```

停用程序自動設定 `search_path`：

```

ALTER PROCEDURE check_password(text) RESET search_path;
```

現在，程序會以其呼叫者所使用的搜尋路徑執行。

<a id="id-1.9.3.24.8"></a>

## 相容性

此陳述式與 SQL 標準中的 `ALTER
PROCEDURE` 陳述式部分相容。標準允許修改程序的更多屬性，但不提供重新命名程序、將程序設為 SECURITY DEFINER、為程序附加組態參數值，或變更程序的擁有者、綱要或揮發性等功能。標準也要求使用 `RESTRICT` 關鍵字，而這在 PostgreSQL 中是選擇性的。

<a id="id-1.9.3.24.9"></a>

## 另請參閱

[CREATE PROCEDURE](sql-createprocedure.md), [DROP PROCEDURE](sql-dropprocedure.md), [ALTER FUNCTION](sql-alterfunction.md), [ALTER ROUTINE](sql-alterroutine.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterprocedure.html)（原文版本：18.6；核對日期：2026-10-05）
