# 41.11. 深入了解 PL/pgSQL

本節討論一些實作的細節，這些細節通常對於 PL/pgSQL 使用者來說很重要。

## 42.11.1. 變數代換

PL/pgSQL 函數中的 SQL 語句和表示式可以引用函數的變數和參數。在後端處理時，PL/pgSQL 會將查詢參數代換為資料內容的引用。僅在語法上允許使用參數或欄位引用的位置代換參數。有一個極端的情況，請參考以下不良程式風格的範例：

```text
INSERT INTO foo (foo) VALUES (foo);
```

從語法上講，第一個出現的 foo 必須是一個資料表名稱，因此即使該函數具有一個名為 foo 的變數，也不能將其代換。第二個出現的 foo 必須是資料表的欄位名稱，因此也不會被代換。 只有第三次出現的 foo 才可以引用該函數的變數。

**提醒**  
版本 9.0 之前的 PostgreSQL 會在所有這三種情況下都嘗試代換該變數，從而導致語法錯誤。

由於變數的名稱在語法上與資料表欄位的名稱沒有差別，因此在引用資料表的語句中可能存在歧義：給予的名稱是要引用資料表欄位還是變數？ 我們將前面的範例更改為

```text
INSERT INTO dest (col) SELECT foo + bar FROM src;
```

在這裡，dest 和 src 必須是資料表名稱，col 必須是 dest 的欄位，但是 foo 和 bar 可能合理地是函數的變數或 src 的欄位。

預設情況下，如果 SQL 語句中的名稱可以引用變數或資料表欄位，則 PL/pgSQL 將回報錯誤。您可以透過重新命名變數或欄位，限定引用或告訴 PL/pgSQL 偏好哪種解釋來解決此問題。

最簡單的解決方案是重新命名變數或欄位。常見的命名規則是對 PL/pgSQL 變數使用與對欄位名不同的命名約定。例如，如果您一致地命名函數變數 v_something，而您的欄位名稱都不以 v_ 開頭，就絕對不會發生衝突。

或者，您可以限定模糊的引用以使其變得清楚。在上面的範例中，src.foo 將是對資料表欄位的明確引用。要建立對變數的明確引用，請在帶標籤的區塊中對其進行宣告，並使用該區塊的標籤（請參閱[第 42.2 節](structure-of-pl-pgsql.md)）。例如，

```text
<<block>>
DECLARE
    foo int;
BEGIN
    foo := ...;
    INSERT INTO dest (col) SELECT block.foo + bar FROM src;
```

即使在 src 中有欄位 foo，block.foo 也還是會被認定為變數。函數參數以及諸如 FOUND 之類的特殊變數可以透過函數名稱來限定，因為它們是在標有函數名稱的外部區塊中隱含宣告的。

有時在大量的 PL/pgSQL 程式中修復所有模棱兩可的引用是不切實際的。在這種情況下，您可以指定 PL/pgSQL 應該將歧義引用解析為變數（與 PostgreSQL 9.0 之前的 PL/pgSQL 行為相容）或資料表欄位（與 Oracle 這樣的系統相容）。

要在系統範圍內變更行為，請將組態參數 plpgsql.variable\_conflict 設定為 error、use\_variable 或 use\_column（其中 error 是預設設定）之一。 此參數影響 PL/pgSQL 函數中語句的後續編譯，但不影響目前連線中已編譯的語句。由於變更此設定可能會導致 PL/pgSQL 函數的行為發生意外變更，因此只能由超級使用者變更。

您還可以透過在函數內容的開頭插入以下特殊命令之一來達到逐個函數的設定行為：

```text
#variable_conflict error
#variable_conflict use_variable
#variable_conflict use_column
```

這些命令僅影響它們所在的函數，並覆蓋 plpgsql.variable\_conflict 的設定。範例如下

```text
CREATE FUNCTION stamp_user(id int, comment text) RETURNS void AS $$
    #variable_conflict use_variable
    DECLARE
        curtime timestamp := now();
    BEGIN
        UPDATE users SET last_modified = curtime, comment = comment
          WHERE users.id = id;
    END;
$$ LANGUAGE plpgsql;
```

在 UPDATE 指令中，無論使用者是否具有這些名稱的欄位，curtime、comment 和 id 將引用該函數的變數和參數。注意，我們必須在 WHERE 子句中限定對 users.id 的引用，以使其引用資料表欄位。但是我們不必將引用的註釋限定為 UPDATE 列表中的標的，因為在語法上必須是使用者的欄位。我們可以這樣撰寫相同的函數，而毋需依賴 variable\_conflict 設定：

```text
CREATE FUNCTION stamp_user(id int, comment text) RETURNS void AS $$
    <<fn>>
    DECLARE
        curtime timestamp := now();
    BEGIN
        UPDATE users SET last_modified = fn.curtime, comment = stamp_user.comment
          WHERE users.id = stamp_user.id;
    END;
$$ LANGUAGE plpgsql;
```

給予 EXECUTE 或其等效的指令字串中不會發生變數代換。如果您需要在這樣的命令中插入變化的值，則應在建構字串的過程中進行，或使用 USING，如[第 42.5.4 節](42.5.-basic-statements.md#42-5-4-executing-dynamic-commands)中所示。

目前，變數代換僅在 SELECT、INSERT、UPDATE 和 DELETE 指令中有作用，因為主要的 SQL 引擎僅在這些指令中允許查詢參數。要在其他語句類型（通常稱為工具程序語句 utility statements）中使用非常數的名稱或值，必須將工具程序語句建構為字串再使用 EXECUTE。

## 42.11.2. 查詢計劃快取

The PL/pgSQL interpreter parses the function's source text and produces an internal binary instruction tree the first time the function is called \(within each session\). The instruction tree fully translates the PL/pgSQL statement structure, but individual SQL expressions and SQL commands used in the function are not translated immediately.

As each expression and SQL command is first executed in the function, the PL/pgSQL interpreter parses and analyzes the command to create a prepared statement, using the SPI manager's `SPI_prepare` function. Subsequent visits to that expression or command reuse the prepared statement. Thus, a function with conditional code paths that are seldom visited will never incur the overhead of analyzing those commands that are never executed within the current session. A disadvantage is that errors in a specific expression or command cannot be detected until that part of the function is reached in execution. \(Trivial syntax errors will be detected during the initial parsing pass, but anything deeper will not be detected until execution.\)

PL/pgSQL \(or more precisely, the SPI manager\) can furthermore attempt to cache the execution plan associated with any particular prepared statement. If a cached plan is not used, then a fresh execution plan is generated on each visit to the statement, and the current parameter values \(that is, PL/pgSQL variable values\) can be used to optimize the selected plan. If the statement has no parameters, or is executed many times, the SPI manager will consider creating a _generic_ plan that is not dependent on specific parameter values, and caching that for re-use. Typically this will happen only if the execution plan is not very sensitive to the values of the PL/pgSQL variables referenced in it. If it is, generating a plan each time is a net win. See [PREPARE](https://www.postgresql.org/docs/12/sql-prepare.html) for more information about the behavior of prepared statements.

Because PL/pgSQL saves prepared statements and sometimes execution plans in this way, SQL commands that appear directly in a PL/pgSQL function must refer to the same tables and columns on every execution; that is, you cannot use a parameter as the name of a table or column in an SQL command. To get around this restriction, you can construct dynamic commands using the PL/pgSQL `EXECUTE` statement — at the price of performing new parse analysis and constructing a new execution plan on every execution.

The mutable nature of record variables presents another problem in this connection. When fields of a record variable are used in expressions or statements, the data types of the fields must not change from one call of the function to the next, since each expression will be analyzed using the data type that is present when the expression is first reached. `EXECUTE` can be used to get around this problem when necessary.

If the same function is used as a trigger for more than one table, PL/pgSQL prepares and caches statements independently for each such table — that is, there is a cache for each trigger function and table combination, not just for each function. This alleviates some of the problems with varying data types; for instance, a trigger function will be able to work successfully with a column named `key` even if it happens to have different types in different tables.

Likewise, functions having polymorphic argument types have a separate statement cache for each combination of actual argument types they have been invoked for, so that data type differences do not cause unexpected failures.

Statement caching can sometimes have surprising effects on the interpretation of time-sensitive values. For example there is a difference between what these two functions do:

```text
CREATE FUNCTION logfunc1(logtxt text) RETURNS void AS $$
    BEGIN
        INSERT INTO logtable VALUES (logtxt, 'now');
    END;
$$ LANGUAGE plpgsql;
```

and:

```text
CREATE FUNCTION logfunc2(logtxt text) RETURNS void AS $$
    DECLARE
        curtime timestamp;
    BEGIN
        curtime := 'now';
        INSERT INTO logtable VALUES (logtxt, curtime);
    END;
$$ LANGUAGE plpgsql;
```

In the case of `logfunc1`, the PostgreSQL main parser knows when analyzing the `INSERT` that the string `'now'` should be interpreted as `timestamp`, because the target column of `logtable` is of that type. Thus, `'now'` will be converted to a `timestamp` constant when the `INSERT` is analyzed, and then used in all invocations of `logfunc1` during the lifetime of the session. Needless to say, this isn't what the programmer wanted. A better idea is to use the `now()` or `current_timestamp` function.

In the case of `logfunc2`, the PostgreSQL main parser does not know what type `'now'` should become and therefore it returns a data value of type `text` containing the string `now`. During the ensuing assignment to the local variable `curtime`, the PL/pgSQL interpreter casts this string to the `timestamp` type by calling the `text_out` and `timestamp_in` functions for the conversion. So, the computed time stamp is updated on each execution as the programmer expects. Even though this happens to work as expected, it's not terribly efficient, so use of the `now()` function would still be a better idea.

