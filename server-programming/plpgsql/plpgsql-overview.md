<a id="PLPGSQL-OVERVIEW"></a>

## 41.1. 概觀 [#](#PLPGSQL-OVERVIEW)

[41.1.1. 使用 PL/pgSQL 的優點](plpgsql-overview.md#PLPGSQL-ADVANTAGES)

[41.1.2. 支援的引數與結果資料型別](plpgsql-overview.md#PLPGSQL-ARGS-RESULTS)

PL/pgSQL 是 PostgreSQL 資料庫系統可載入的程序語言。PL/pgSQL 的設計目標是要打造一個可載入的程序語言，它能夠：

* 用來建立函式、程序與觸發程序，
* 為 SQL 語言加上控制結構，
* 進行複雜的運算，
* 繼承所有使用者定義的型別、函式、程序與運算子，
* 可以被定義為受伺服器信任，
* 容易使用。

以 PL/pgSQL 建立的函式，可以用在任何能使用內建函式的地方。舉例來說，你可以建立複雜的條件式運算函式，之後再用它們來定義運算子，或是用在索引運算式中。

在 PostgreSQL 9.0 以後的版本中，PL/pgSQL 預設就會安裝。不過它仍然是一個可載入的模組，因此特別注重安全性的管理者可以選擇把它移除。

<a id="PLPGSQL-ADVANTAGES"></a>

### 41.1.1. 使用 PL/pgSQL 的優點 [#](#PLPGSQL-ADVANTAGES)

SQL 是 PostgreSQL 以及大多數其他關聯式資料庫所使用的查詢語言。它具可攜性，也容易學習。但是每一個 SQL 陳述式都必須由資料庫伺服器個別執行。

這表示你的用戶端應用程式必須把每一個查詢送到資料庫伺服器，等待它處理，接收並處理結果，做一些運算，然後再送出後續的查詢給伺服器。這一切都會產生程序間通訊的成本；如果你的用戶端與資料庫伺服器不在同一台機器上，還會額外產生網路負擔。

有了 PL/pgSQL，你可以把一段運算與一系列查詢集中在資料庫伺服器*內部*，因此既能擁有程序語言的威力與 SQL 的易用性，又能大幅節省用戶端／伺服器之間的通訊負擔。

* 省去用戶端與伺服器之間額外的來回往返
* 用戶端不需要的中間結果，不必在伺服器與用戶端之間封送或傳輸
* 可以避免多輪的查詢剖析

比起不使用預存函式的應用程式，這可以帶來相當可觀的效能提升。

此外，有了 PL/pgSQL，你可以使用 SQL 的所有資料型別、運算子與函式。

<a id="PLPGSQL-ARGS-RESULTS"></a>

### 41.1.2. 支援的引數與結果資料型別 [#](#PLPGSQL-ARGS-RESULTS)

以 PL/pgSQL 撰寫的函式可以接受伺服器所支援的任何純量或陣列資料型別作為引數，也可以回傳這些型別中任一種的結果。它們也可以接受或回傳任何以名稱指定的複合型別（資料列型別）。你也可以把 PL/pgSQL 函式宣告成接受 `record`，意思是任何複合型別都可以作為輸入；或是宣告成回傳 `record`，意思是其結果為一個資料列型別，而其欄位由呼叫端查詢中的指定內容決定，詳見[第 7.2.1.4 節](../../the-sql-language/queries/queries-table-expressions.md#QUERIES-TABLEFUNCTIONS)。

PL/pgSQL 函式可以使用 `VARIADIC` 標記宣告成接受可變數量的引數。其運作方式與 SQL 函式完全相同，詳見[第 36.5.6 節](../extend/xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)。

PL/pgSQL 函式也可以宣告成接受並回傳[第 36.2.5 節](../extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)所描述的多型型別，如此一來，函式實際處理的資料型別就可以隨每次呼叫而不同。範例請見[第 41.3.1 節](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS)。

PL/pgSQL 函式還可以宣告成回傳任何能以單一實例回傳之資料型別的「集合」（或資料表）。這樣的函式會針對結果集合中每個想要的元素執行 `RETURN NEXT`，或是使用 `RETURN QUERY` 輸出計算某個查詢所得的結果，藉此產生輸出。

最後，如果 PL/pgSQL 函式沒有有用的回傳值，可以宣告成回傳 `void`。（或者，這種情況下也可以把它寫成一個程序。）

PL/pgSQL 函式也可以用輸出參數來取代明確指定回傳型別。這並不會為這個語言增加任何根本性的能力，但通常很方便，尤其是在要回傳多個值的時候。`RETURNS TABLE` 標記法也可以用來取代 `RETURNS SETOF`。

具體的範例請見[第 41.3.1 節](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS)與[第 41.6.1 節](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-overview.html)（原文版本：18.6；核對日期：2026-09-13）
