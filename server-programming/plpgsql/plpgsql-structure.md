<a id="PLPGSQL-STRUCTURE"></a>
## 41.2. PL/pgSQL 的結構 [#](#PLPGSQL-STRUCTURE)

以 PL/pgSQL 撰寫的函式，是透過執行 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md) 命令向伺服器定義的。這樣的命令通常看起來像這樣：

```

CREATE FUNCTION somefunc(integer, text) RETURNS integer
AS 'function body text'
LANGUAGE plpgsql;
```

就 `CREATE FUNCTION` 而言，函式主體只是一個字串常值。撰寫函式主體時，通常會使用錢字符引用（dollar quoting，見[4.1.2.4 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)），而非一般的單引號語法，這樣做通常很有幫助。若不使用錢字符引用，函式主體中任何單引號或反斜線都必須以重複兩次的方式加以逸出。本章幾乎所有範例都使用以錢字符括住的字串常值來撰寫函式主體。

PL/pgSQL 是一種以區塊為結構的語言。函式主體的完整文字必須是一個*區塊*。區塊的定義如下：

```

[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
END [ label ];
```

區塊中的每一個宣告與每一個陳述式，都必須以分號結尾。出現在另一個區塊內部的區塊，其 `END`
之後必須有分號，如上所示；但函式主體結尾的最後一個 `END` 則不需要分號。

### 提示

常見的錯誤是在 `BEGIN` 之後立即加上分號。這是不正確的，會導致語法錯誤。

*`label`* 只有在您想要於 `EXIT` 陳述式中識別該區塊，或是想要限定區塊中所宣告變數的名稱時才需要。若在
`END` 之後加上標籤，該標籤必須與區塊開頭的標籤相符。

所有關鍵字皆不區分大小寫。識別字若未加雙引號，會如同一般 SQL 命令中的做法，隱含轉換為小寫。

PL/pgSQL 程式碼中的註解，運作方式與一般 SQL 相同。雙破折號（`--`）會開始一個延伸至該行結尾的註解。`/*`
會開始一個區塊註解，延伸至相符的 `*/`
為止。區塊註解可以巢狀。

區塊中陳述式部分的任何陳述式，都可以是一個*子區塊*。子區塊可用於邏輯分組，或是將變數的作用範圍侷限於一小群陳述式。在子區塊中宣告的變數，會在該子區塊的存續期間，遮蔽外層區塊中任何同名的變數；但若以外層區塊的標籤限定其名稱，您仍然可以存取外層變數。例如：

```

CREATE FUNCTION somefunc() RETURNS integer AS $$
<< outerblock >>
DECLARE
    quantity integer := 30;
BEGIN
    RAISE NOTICE 'Quantity here is %', quantity;  -- Prints 30
    quantity := 50;
    --
    -- Create a subblock
    --
    DECLARE
        quantity integer := 80;
    BEGIN
        RAISE NOTICE 'Quantity here is %', quantity;  -- Prints 80
        RAISE NOTICE 'Outer quantity here is %', outerblock.quantity;  -- Prints 50
    END;

    RAISE NOTICE 'Quantity here is %', quantity;  -- Prints 50

    RETURN quantity;
END;
$$ LANGUAGE plpgsql;
```

### 注意

事實上，每一個 PL/pgSQL 函式主體外面都隱含包著一個「外層區塊」。這個區塊提供了函式參數（若有的話）的宣告，以及一些特殊變數，例如
`FOUND`（見[41.5.5 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)）。這個外層區塊以函式名稱作為標籤，意味著參數與特殊變數都可以用函式名稱來限定。

請務必不要將 PL/pgSQL 中用於陳述式分組的
`BEGIN`／`END`，與名稱相似、用於交易控制的 SQL 命令混淆。PL/pgSQL 的
`BEGIN`／`END`
僅用於分組；它們並不會開始或結束交易。關於在 PL/pgSQL 中管理交易的資訊，請見[41.8 節](plpgsql-transactions.md)。此外，含有
`EXCEPTION` 子句的區塊，實際上會形成一個子交易，可在不影響外層交易的情況下回復（rollback）。詳情請見[41.6.8 節](plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-structure.html)（原文版本：18.6；核對日期：2026-09-15）
