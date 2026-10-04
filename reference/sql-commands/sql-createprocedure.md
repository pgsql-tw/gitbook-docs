<a id="SQL-CREATEPROCEDURE"></a><a id="id-1.9.3.76.1"></a>

## CREATE PROCEDURE

CREATE PROCEDURE — 定義新的程序

<a id="id-1.9.3.76.4"></a>

## 語法

```

CREATE [ OR REPLACE ] PROCEDURE
    name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
    | sql_body
  } ...
```

<a id="SQL-CREATEPROCEDURE-DESCRIPTION"></a>

## 說明

`CREATE PROCEDURE` 會定義新的程序。`CREATE OR REPLACE PROCEDURE` 會建立新的程序，或取代現有的定義。若要能夠定義程序，使用者必須擁有該語言的 `USAGE` 權限。

若包含綱要名稱，程序就會建立在指定的綱要中；否則會建立在目前的綱要中。新程序的名稱不得與同一綱要中具有相同輸入引數型別的任何現有程序或函式相同。不過，引數型別不同的程序與函式可以共用同一個名稱（這稱為*多載*）。

若要取代現有程序的目前定義，請使用 `CREATE OR REPLACE PROCEDURE`。無法以這種方式變更程序的名稱或引數型別（若你嘗試這麼做，實際上會建立一個新的、不同的程序）。

使用 `CREATE OR REPLACE PROCEDURE` 取代現有程序時，該程序的擁有權與權限不會改變。所有其他程序屬性都會被指派為命令中指定或隱含的值。你必須擁有該程序才能取代它（這包括身為擁有該程序之角色的成員）。

建立程序的使用者會成為該程序的擁有者。

若要能夠建立程序，你必須擁有引數型別的 `USAGE` 權限。

關於撰寫程序的更多資訊，請參閱[第 36.4 節](../../server-programming/extend/xproc.md)。

<a id="id-1.9.3.76.6"></a>

## 參數

*`name`*
:   要建立的程序名稱（可選擇以綱要限定）。

*`argmode`*
:   引數的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。若省略，預設為 `IN`。

*`argname`*
:   引數的名稱。

*`argtype`*
:   程序引數的資料型別（可選擇以綱要限定），若有引數的話。引數型別可以是基本型別、複合型別或網域型別，也可以參照資料表欄位的型別。

    依實作語言而定，也可能允許指定「虛擬型別」，例如 `cstring`。虛擬型別表示實際的引數型別不是未完整指定，就是位於一般 SQL 資料型別的集合之外。

    欄位的型別是以 `table_name.column_name%TYPE` 的寫法來參照。使用此功能有時有助於讓程序不受資料表定義變更的影響。

*`default_expr`*
:   未指定參數時用作預設值的運算式。該運算式必須能強制轉型為該參數的引數型別。位於具有預設值之參數後面的所有輸入參數，也都必須具有預設值。

*`lang_name`*
:   實作此程序所用語言的名稱。它可以是 `sql`、`c`、`internal`，或使用者定義之程序語言的名稱，例如 `plpgsql`。若指定了 *`sql_body`*，預設為 `sql`。以單引號括住名稱的寫法已不建議使用，且大小寫必須相符。

`TRANSFORM { FOR TYPE type_name } [, ... ] }`
:   列出呼叫此程序時應套用哪些轉換（transform）。轉換會在 SQL 型別與語言特定的資料型別之間進行轉換；請參閱 [CREATE TRANSFORM](sql-createtransform.md)。程序語言的實作通常已將內建型別的相關知識寫死在程式中，因此這些型別不需要列在這裡。若程序語言的實作不知道如何處理某個型別，且未提供轉換，它會改用預設的資料型別轉換行為，但這取決於實作。

`[EXTERNAL] SECURITY INVOKER`<br>`[EXTERNAL] SECURITY DEFINER`
:   `SECURITY INVOKER` 表示程序要以呼叫它之使用者的權限執行。這是預設行為。`SECURITY DEFINER` 指定程序要以擁有它之使用者的權限執行。

    允許使用關鍵字 `EXTERNAL` 是為了符合 SQL，但它是選用的，因為與 SQL 不同，此功能適用於所有程序，而不僅是外部程序。

    `SECURITY DEFINER` 程序不能執行交易控制陳述式（例如 `COMMIT` 與 `ROLLBACK`，視語言而定）。

*`configuration_parameter`*<br>*`value`*
:   `SET` 子句會使指定的組態參數在進入程序時被設為指定的值，並在程序結束時還原為先前的值。`SET FROM CURRENT` 會將執行 `CREATE PROCEDURE` 當下該參數的目前值，儲存為進入程序時要套用的值。

    若程序附加了 `SET` 子句，則在程序內針對同一變數執行的 `SET LOCAL` 命令，其效果僅限於該程序：組態參數先前的值仍會在程序結束時還原。不過，一般的 `SET` 命令（不含 `LOCAL`）會覆寫 `SET` 子句，就如同它會覆寫先前的 `SET
    LOCAL` 命令一樣：除非目前交易被回復，否則此類命令的效果在程序結束後仍會持續。

    若程序附加了 `SET` 子句，則該程序不能執行交易控制陳述式（例如 `COMMIT` 與 `ROLLBACK`，視語言而定）。

    關於允許的參數名稱與值的更多資訊，請參閱 [SET](sql-set.md) 與[第 19 章](../../server-administration/runtime-config/README.md)。

*`definition`*
:   定義程序的字串常數；其意義取決於語言。它可以是內部程序名稱、目的檔的路徑、SQL 命令，或以程序語言撰寫的文字。

    使用錢號引用（請參閱[第 4.1.2.4 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)）而不是一般的單引號語法來撰寫程序定義字串，通常會很有幫助。若不使用錢號引用，程序定義中的任何單引號或反斜線都必須以重複兩次的方式跳脫。

`obj_file, link_symbol`
:   當 C 語言原始碼中的程序名稱與 SQL 程序的名稱不同時，動態載入的 C 語言程序會使用這種形式的 `AS` 子句。字串 *`obj_file`* 是包含已編譯 C 程序之共用程式庫檔案的名稱，其解讀方式與 [`LOAD`](sql-load.md) 命令相同。字串 *`link_symbol`* 是程序的連結符號，也就是 C 語言原始碼中該程序的名稱。若省略連結符號，則假定它與所定義之 SQL 程序的名稱相同。

    當多次 `CREATE PROCEDURE` 呼叫參照同一個目的檔時，該檔案在每個工作階段中只會載入一次。若要卸載並重新載入該檔案（或許是在開發期間），請開始一個新的工作階段。

*`sql_body`*
:   `LANGUAGE SQL` 程序的主體。這應該是一個區塊

    ```

    BEGIN ATOMIC
      statement;
      statement;
      ...
      statement;
    END
    ```

    這類似於將程序主體的文字寫成字串常數（請參閱上方的 *`definition`*），但有一些差異：此形式只適用於 `LANGUAGE
    SQL`，字串常數形式則適用於所有語言。此形式在定義程序時進行剖析，字串常數形式則在執行時進行剖析；因此，此形式無法支援多型引數型別，以及其他在定義程序時無法解析的結構。此形式會追蹤程序與程序主體中所用物件之間的相依關係，因此 `DROP
    ... CASCADE` 能正確運作，而使用字串常值的形式則可能留下懸置的程序。最後，此形式與 SQL 標準及其他 SQL 實作更為相容。

<a id="SQL-CREATEPROCEDURE-NOTES"></a>

## 注意事項

關於同樣適用於程序之函式建立的更多細節，請參閱 [CREATE FUNCTION](sql-createfunction.md)。

請使用 [CALL](sql-call.md) 執行程序。

<a id="SQL-CREATEPROCEDURE-EXAMPLES"></a>

## 範例

```

CREATE PROCEDURE insert_data(a integer, b integer)
LANGUAGE SQL
AS $$
INSERT INTO tbl VALUES (a);
INSERT INTO tbl VALUES (b);
$$;
```

或

```

CREATE PROCEDURE insert_data(a integer, b integer)
LANGUAGE SQL
BEGIN ATOMIC
  INSERT INTO tbl VALUES (a);
  INSERT INTO tbl VALUES (b);
END;
```

並以如下方式呼叫：

```

CALL insert_data(1, 2);
```

<a id="SQL-CREATEPROCEDURE-COMPAT"></a>

## 相容性

`CREATE PROCEDURE` 命令定義於 SQL 標準中。PostgreSQL 的實作可以用相容的方式使用，但有許多擴充。詳細資訊另請參閱 [CREATE FUNCTION](sql-createfunction.md)。

<a id="id-1.9.3.76.10"></a>

## 另請參閱

[ALTER PROCEDURE](sql-alterprocedure.md), [DROP PROCEDURE](sql-dropprocedure.md), [CALL](sql-call.md), [CREATE FUNCTION](sql-createfunction.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createprocedure.html)（原文版本：18.6；核對日期：2026-10-04）
