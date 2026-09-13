<a id="PLPGSQL-EXPRESSIONS"></a>

## 41.4. 運算式 [#](#PLPGSQL-EXPRESSIONS)

PL/pgSQL 陳述式中所使用的所有運算式，都是以伺服器主要的 SQL 執行器來處理。舉例來說，當你寫出像這樣的 PL/pgSQL 陳述式

```

IF expression THEN ...
```

PL/pgSQL 會把類似下面這樣的查詢

```

SELECT expression
```

送進主要的 SQL 引擎，藉此求出該運算式的值。在組成這個 `SELECT` 指令時，其中出現的 PL/pgSQL 變數名稱都會被替換成查詢參數，詳見 [第 41.11.1 節](plpgsql-implementation.md#PLPGSQL-VAR-SUBST)。這麼做可以讓該 `SELECT` 的查詢計畫只準備一次，之後便能在變數帶有不同值時重複使用。因此，一個運算式第一次被使用時，實際上發生的事情等同於一個 `PREPARE` 指令。例如，如果我們宣告了兩個整數變數 `x` 與 `y`，而我們寫下

```

IF x < y THEN ...
```

那麼幕後所發生的事情就等同於

```

PREPARE statement_name(integer, integer) AS SELECT $1 < $2;
```

接著每次執行這個 `IF` 陳述式時，就會以 PL/pgSQL 變數當下的值作為參數值，去 `EXECUTE` 這個預備陳述式。通常 PL/pgSQL 使用者不需要在意這些細節，但是在試著診斷問題時，知道這些會很有幫助。更多資訊請見 [第 41.11.2 節](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)。

由於 *`expression`* 會被轉換成一個 `SELECT` 指令，因此它可以包含一般 `SELECT` 所能包含的相同子句，只是它不能包含頂層的 `UNION`、`INTERSECT` 或 `EXCEPT` 子句。所以，舉例來說，你可以用下列方式測試某個資料表是否非空：

```

IF count(*) > 0 FROM my_table THEN ...
```

因為介於 `IF` 與 `THEN` 之間的 *`expression`* 在剖析時，會被視為 `SELECT count(*) > 0 FROM my_table`。這個 `SELECT` 必須產生單一欄位，而且不能超過一筆資料列。（如果它沒有產生任何資料列，其結果會被視為 NULL。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-expressions.html)（原文版本：18.6；核對日期：2026-09-13）
