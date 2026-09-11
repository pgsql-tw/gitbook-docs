<a id="TYPECONV-FUNC"></a>

## 10.3. 函式 [#](#TYPECONV-FUNC)

<a id="id-1.5.9.8.2"></a>

函式呼叫所參照的特定函式，是依下列程序決定的。

<a id="id-1.5.9.8.4"></a>

**函式型別解析**

1. 從 `pg_proc` 系統目錄中選出要考慮的函式。如果使用的是未以 schema 限定的函式名稱，要考慮的函式是那些名稱與參數數量相符、且在目前搜尋路徑中可見的函式（請參閱[第 5.10.3 節](../ddl/ddl-schemas.md#DDL-SCHEMAS-PATH)）。如果給定的是限定名稱的函式，則只考慮指定 schema 中的函式。

   1. 如果搜尋路徑中找到多個參數型別完全相同的函式，只會考慮在路徑中最先出現的那一個。參數型別不同的函式，則不論在搜尋路徑中的位置為何，都會一視同仁地納入考慮。
   2. 如果函式宣告了 `VARIADIC` 陣列參數，而呼叫時沒有使用 `VARIADIC` 關鍵字，則會將該函式視為其陣列參數被替換成一個或多個其元素型別的參數，數量依呼叫所需而定。經過這樣的展開之後，該函式的有效參數型別可能與某個非 variadic 函式完全相同。在這種情況下，會使用在搜尋路徑中較早出現的函式；如果兩個函式位於同一個 schema，則優先使用非 variadic 的那一個。

      在透過限定名稱
      [<a id="FUNC-QUALIFIED-SECURITY"></a>[10]](#ftn.FUNC-QUALIFIED-SECURITY)
      呼叫位於允許不受信任使用者建立物件之 schema 中的 variadic 函式時，這會產生安全風險。惡意使用者可以取得控制權，並以彷彿是你所執行的身分執行任意 SQL 函式。請改用帶有 `VARIADIC` 關鍵字的呼叫，即可避開這項風險。填入 `VARIADIC "any"` 參數的呼叫，通常沒有包含 `VARIADIC` 關鍵字的等價寫法。要安全地發出這類呼叫，該函式所在的 schema 必須只允許受信任的使用者建立物件。
   3. 參數具有預設值的函式，會被視為與省略了零個或多個可使用預設值參數位置的任何呼叫相符。如果有多個這樣的函式與呼叫相符，會使用在搜尋路徑中最先出現的那一個。如果同一個 schema 中有兩個或更多這樣的函式，且它們在非預設值位置上的參數型別完全相同（當它們可使用預設值的參數組合不同時，就有可能發生），系統將無法決定要優先使用哪一個，因此若找不到與呼叫更相符的函式，就會產生「ambiguous function call」（函式呼叫有歧義）錯誤。

      在透過限定名稱[[10]](typeconv-func.md#ftn.FUNC-QUALIFIED-SECURITY)呼叫位於允許不受信任使用者建立物件之 schema 中的任何函式時，這會產生可用性風險。惡意使用者可以建立一個與既有函式同名的函式，複製該函式的參數，並附加具有預設值的新參數。這會讓新的呼叫無法再使用原本的函式。要預防這項風險，請將函式放在只允許受信任使用者建立物件的 schema 中。
2. 檢查是否有函式完全接受這些輸入參數型別。如果存在（在所考慮的函式集合中，完全相符的只可能有一個），就使用它。在透過限定名稱[[10]](typeconv-func.md#ftn.FUNC-QUALIFIED-SECURITY)呼叫位於允許不受信任使用者建立物件之 schema 中的函式時，如果沒有完全相符的函式，就會產生安全風險。在這種情況下，請轉換參數型別以強制完全相符。（涉及 `unknown` 的情況在這個步驟中永遠找不到相符的函式。）
3. 如果找不到完全相符的函式，就檢查這個函式呼叫是否看起來像是特殊的型別轉換請求。當函式呼叫只有一個參數，且函式名稱與某個資料型別的（內部）名稱相同時，就會發生這種情況。此外，函式的參數必須是型別未知的字面值、可以二進位相容地轉換為所指名資料型別的型別，或是可以透過套用該型別的 I/O 函式轉換為所指名資料型別的型別（也就是說，轉換的來源或目標是標準字串型別之一）。符合這些條件時，該函式呼叫會被視為一種 `CAST` 規格。
   [<a id="id-1.5.9.8.4.4.1.2"></a>[11]](#ftn.id-1.5.9.8.4.4.1.2)
4. 尋找最佳相符項目。

   1. 捨棄輸入型別不相符、且無法（使用隱含轉換）轉換成相符的候選函式。為此目的，會假設 `unknown` 字面值可以轉換為任何型別。如果只剩下一個候選，就使用它；否則繼續下一步。
   2. 如果任何輸入參數是網域型別，在後續所有步驟中都將它視為該網域的基礎型別。這可確保在解析有歧義的函式時，網域的行為與其基礎型別相同。
   3. 逐一檢查所有候選，保留在輸入型別上完全相符數量最多的那些。如果沒有任何候選完全相符，就保留全部候選。如果只剩下一個候選，就使用它；否則繼續下一步。
   4. 逐一檢查所有候選，保留在需要型別轉換的位置上，接受（輸入資料型別所屬型別類別中的）優先型別數量最多的那些。如果沒有任何候選接受優先型別，就保留全部候選。如果只剩下一個候選，就使用它；否則繼續下一步。
   5. 如果有任何輸入參數是 `unknown`，檢查其餘候選在這些參數位置上接受的型別類別。在每個位置上，只要有任何候選接受 `string` 類別，就選擇該類別。（之所以偏向字串是合理的，是因為型別未知的字面值看起來就像字串。）否則，如果其餘所有候選都接受相同的型別類別，就選擇該類別；否則就失敗，因為沒有更多線索就無法推斷出正確的選擇。接著捨棄不接受所選型別類別的候選。此外，如果有任何候選在該類別中接受優先型別，就捨棄在該參數上接受非優先型別的候選。如果沒有任何候選通過這些檢驗，就保留全部候選。如果只剩下一個候選，就使用它；否則繼續下一步。
   6. 如果同時存在 `unknown` 與已知型別的參數，而且所有已知型別的參數都是相同型別，就假設 `unknown` 參數也是該型別，並檢查哪些候選能在 `unknown` 參數的位置上接受該型別。如果恰好只有一個候選通過這項檢驗，就使用它。否則就失敗。

請注意，運算子與函式型別解析的「最佳相符」規則是相同的。以下是一些範例。

<a id="id-1.5.9.8.6"></a>

**範例 10.6. 四捨五入函式的參數型別解析**

只有一個接受兩個參數的 `round` 函式；它的第一個參數型別是 `numeric`，第二個參數型別是 `integer`。因此，下列查詢會自動將 `integer` 型別的第一個參數轉換為 `numeric`：

```

SELECT round(4, 4);

 round
--------
 4.0000
(1 row)
```

這個查詢實際上會被剖析器轉換為：

```

SELECT round(CAST (4 AS numeric), 4);
```

由於帶有小數點的數值常數一開始就會被指派 `numeric` 型別，下列查詢不需要任何型別轉換，因此可能會稍微有效率一些：

```

SELECT round(4.0, 4);
```

<br><a id="id-1.5.9.8.7"></a>

**範例 10.7. Variadic 函式的解析**

```

CREATE FUNCTION public.variadic_example(VARIADIC numeric[]) RETURNS int
  LANGUAGE sql AS 'SELECT 1';
CREATE FUNCTION
```

這個函式接受 VARIADIC 關鍵字，但並不要求使用。它可以同時接受整數與數值參數：

```

SELECT public.variadic_example(0),
       public.variadic_example(0.0),
       public.variadic_example(VARIADIC array[0.0]);
 variadic_example | variadic_example | variadic_example
------------------+------------------+------------------
                1 |                1 |                1
(1 row)
```

不過，如果有更具體的函式可用，第一個與第二個呼叫會優先使用它們：

```

CREATE FUNCTION public.variadic_example(numeric) RETURNS int
  LANGUAGE sql AS 'SELECT 2';
CREATE FUNCTION

CREATE FUNCTION public.variadic_example(int) RETURNS int
  LANGUAGE sql AS 'SELECT 3';
CREATE FUNCTION

SELECT public.variadic_example(0),
       public.variadic_example(0.0),
       public.variadic_example(VARIADIC array[0.0]);
 variadic_example | variadic_example | variadic_example
------------------+------------------+------------------
                3 |                2 |                1
(1 row)
```

在預設設定下，且只有第一個函式存在時，第一個與第二個呼叫是不安全的。任何使用者都可以藉由建立第二個或第三個函式來攔截這些呼叫。第三個呼叫由於完全符合參數型別並使用了 `VARIADIC` 關鍵字，因此是安全的。

<br><a id="id-1.5.9.8.8"></a>

**範例 10.8. 子字串函式的型別解析**

有好幾個 `substr` 函式，其中一個接受 `text` 與 `integer` 型別。如果以未指定型別的字串常數呼叫，系統會選擇接受優先類別 `string` 參數（也就是 `text` 型別）的候選函式。

```

SELECT substr('1234', 3);

 substr
--------
     34
(1 row)
```

如果字串被宣告為 `varchar` 型別（例如它來自資料表時可能就是如此），剖析器會嘗試將它轉換為 `text`：

```

SELECT substr(varchar '1234', 3);

 substr
--------
     34
(1 row)
```

這會被剖析器轉換為實際上等同於：

```

SELECT substr(CAST (varchar '1234' AS text), 3);
```

### 注意

剖析器從 `pg_cast` 系統目錄得知 `text` 與 `varchar` 是二進位相容的，也就是說，其中一種型別可以直接傳給接受另一種型別的函式，而不需要進行任何實體轉換。因此，在這種情況下並不會真的插入任何型別轉換呼叫。

而如果以 `integer` 型別的參數呼叫該函式，剖析器會嘗試將它轉換為 `text`：

```

SELECT substr(1234, 3);
ERROR:  function substr(integer, integer) does not exist
HINT:  No function matches the given name and argument types. You might need
to add explicit type casts.
```

這樣行不通，因為 `integer` 沒有隱含轉換為 `text` 的型別轉換。不過，明確的型別轉換是可行的：

```

SELECT substr(CAST (1234 AS text), 3);

 substr
--------
     34
(1 row)
```

<br>

<br>

---

<a id="ftn.FUNC-QUALIFIED-SECURITY"></a>

[[10]](#FUNC-QUALIFIED-SECURITY) 
使用未以 schema 限定的名稱時不會產生這種風險，因為包含允許不受信任使用者建立物件之 schema 的搜尋路徑，並不是[安全的 schema 使用模式](../ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS)。

<a id="ftn.id-1.5.9.8.4.4.1.2"></a>

[[11]](#id-1.5.9.8.4.4.1.2) 
這個步驟的目的，是在沒有實際型別轉換函式的情況下，支援函式形式的型別轉換規格。如果有型別轉換函式，依慣例會以其輸出型別命名，因此不需要特殊處理。更多說明請參閱 [CREATE CAST](../../reference/sql-commands/sql-createcast.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/typeconv-func.html)（原文版本：18.6；核對日期：2026-09-11）
