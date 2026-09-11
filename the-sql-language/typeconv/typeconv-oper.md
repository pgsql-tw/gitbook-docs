<a id="TYPECONV-OPER"></a>

## 10.2. 運算子 [#](#TYPECONV-OPER)

<a id="id-1.5.9.7.2"></a>

運算子運算式所參照的特定運算子，是依下列程序決定的。請注意，這個程序會間接受到所涉及運算子優先順序的影響，因為優先順序決定了哪些子運算式會被視為哪些運算子的輸入。詳細資訊請參閱[第 4.1.6 節](../sql-syntax/sql-syntax-lexical.md#SQL-PRECEDENCE)。

<a id="id-1.5.9.7.4"></a>

**運算子型別解析**

<a id="OP-RESOL-SELECT"></a>1. 從 `pg_operator` 系統目錄中選出要考慮的運算子。如果使用的是未以 schema 限定的運算子名稱（一般情況），要考慮的運算子是那些名稱與參數數量相符、且在目前搜尋路徑中可見的運算子（請參閱[第 5.10.3 節](../ddl/ddl-schemas.md#DDL-SCHEMAS-PATH)）。如果給定的是限定名稱的運算子，則只考慮指定 schema 中的運算子。

   1. 如果搜尋路徑中找到多個參數型別完全相同的運算子，只會考慮在路徑中最先出現的那一個。參數型別不同的運算子，則不論在搜尋路徑中的位置為何，都會一視同仁地納入考慮。
<a id="OP-RESOL-EXACT-MATCH"></a>2. 檢查是否有運算子完全接受這些輸入參數型別。如果存在（在所考慮的運算子集合中，完全相符的只可能有一個），就使用它。在透過限定名稱呼叫
   [<a id="OP-QUALIFIED-SECURITY"></a>[9]](#ftn.OP-QUALIFIED-SECURITY)
   （並不常見）某個位於允許不受信任使用者建立物件之 schema 中的運算子時，如果沒有完全相符的運算子，就會產生安全風險。在這種情況下，請轉換參數型別以強制完全相符。

   <a id="OP-RESOL-EXACT-UNKNOWN"></a>1. 如果二元運算子呼叫的其中一個參數是 `unknown` 型別，在這項檢查中就假設它與另一個參數的型別相同。涉及兩個 `unknown` 輸入的呼叫，或是具有 `unknown` 輸入的前置運算子，在這個步驟中永遠找不到相符的運算子。
   <a id="OP-RESOL-EXACT-DOMAIN"></a>2. 如果二元運算子呼叫的其中一個參數是 `unknown` 型別，而另一個是網域型別，接著檢查是否有運算子在兩側都完全接受該網域的基礎型別；如果有，就使用它。
<a id="OP-RESOL-BEST-MATCH"></a>3. 尋找最佳相符項目。

   1. 捨棄輸入型別不相符、且無法（使用隱含轉換）轉換成相符的候選運算子。為此目的，會假設 `unknown` 字面值可以轉換為任何型別。如果只剩下一個候選，就使用它；否則繼續下一步。
   2. 如果任何輸入參數是網域型別，在後續所有步驟中都將它視為該網域的基礎型別。這可確保在解析有歧義的運算子時，網域的行為與其基礎型別相同。
   3. 逐一檢查所有候選，保留在輸入型別上完全相符數量最多的那些。如果沒有任何候選完全相符，就保留全部候選。如果只剩下一個候選，就使用它；否則繼續下一步。
   4. 逐一檢查所有候選，保留在需要型別轉換的位置上，接受（輸入資料型別所屬型別類別中的）優先型別數量最多的那些。如果沒有任何候選接受優先型別，就保留全部候選。如果只剩下一個候選，就使用它；否則繼續下一步。
   5. 如果有任何輸入參數是 `unknown`，檢查其餘候選在這些參數位置上接受的型別類別。在每個位置上，只要有任何候選接受 `string` 類別，就選擇該類別。（之所以偏向字串是合理的，是因為型別未知的字面值看起來就像字串。）否則，如果其餘所有候選都接受相同的型別類別，就選擇該類別；否則就失敗，因為沒有更多線索就無法推斷出正確的選擇。接著捨棄不接受所選型別類別的候選。此外，如果有任何候選在該類別中接受優先型別，就捨棄在該參數上接受非優先型別的候選。如果沒有任何候選通過這些檢驗，就保留全部候選。如果只剩下一個候選，就使用它；否則繼續下一步。
   <a id="OP-RESOL-LAST-UNKNOWN"></a>6. 如果同時存在 `unknown` 與已知型別的參數，而且所有已知型別的參數都是相同型別，就假設 `unknown` 參數也是該型別，並檢查哪些候選能在 `unknown` 參數的位置上接受該型別。如果恰好只有一個候選通過這項檢驗，就使用它。否則就失敗。

以下是一些範例。

<a id="id-1.5.9.7.6"></a>

**範例 10.1. 平方根運算子的型別解析**

標準系統目錄中只定義了一個平方根運算子（前置 `|/`），它接受 `double precision` 型別的參數。在這個查詢運算式中，掃描器會先為參數指派 `integer` 型別：

```

SELECT |/ 40 AS "square root of 40";
 square root of 40
-------------------
 6.324555320336759
(1 row)
```

因此剖析器會對運算元進行型別轉換，這個查詢等同於：

```

SELECT |/ CAST(40 AS double precision) AS "square root of 40";
```

<br><a id="id-1.5.9.7.7"></a>

**範例 10.2. 字串串接運算子的型別解析**

類似字串的語法會用來處理字串型別，也會用來處理複雜的擴充型別。未指定型別的字串會與可能的候選運算子進行比對。

有一個未指定型別參數的範例：

```

SELECT text 'abc' || 'def' AS "text and unknown";

 text and unknown
------------------
 abcdef
(1 row)
```

在這個例子中，剖析器會檢查是否有兩個參數都接受 `text` 的運算子。由於確實存在，它就假設第二個參數應該解讀為 `text` 型別。

以下是兩個未指定型別的值的串接：

```

SELECT 'abc' || 'def' AS "unspecified";

 unspecified
-------------
 abcdef
(1 row)
```

在這個例子中，由於查詢中沒有指定任何型別，一開始並沒有應該使用哪種型別的提示。因此，剖析器會找出所有候選運算子，並發現有接受字串類別輸入的候選，也有接受位元字串類別輸入的候選。由於在可用時會優先選擇字串類別，因此會選擇該類別，然後使用字串的優先型別 `text` 作為解析這些型別未知字面值的具體型別。

<br><a id="id-1.5.9.7.8"></a>

**範例 10.3. 絕對值與取負運算子的型別解析**

PostgreSQL 的運算子系統目錄中有好幾個前置運算子 `@` 的項目，它們都為各種數值資料型別實作絕對值運算。其中一個項目是 `float8` 型別的，該型別是數值類別的優先型別。因此，PostgreSQL 在遇到 `unknown` 輸入時會使用該項目：

```

SELECT @ '-4.5' AS "abs";
 abs
-----
 4.5
(1 row)
```

這裡系統在套用所選的運算子之前，已經隱含地將型別未知的字面值解析為 `float8` 型別。我們可以驗證所使用的確實是 `float8`，而不是其他型別：

```

SELECT @ '-4.5e500' AS "abs";

ERROR:  "-4.5e500" is out of range for type double precision
```

另一方面，前置運算子 `~`（位元反相）只為整數資料型別定義，並沒有為 `float8` 定義。因此，如果我們用 `~` 嘗試類似的情況，會得到：

```

SELECT ~ '20' AS "negation";

ERROR:  operator is not unique: ~ "unknown"
HINT:  Could not choose a best candidate operator. You might need to add
explicit type casts.
```

會發生這種情況，是因為系統無法決定應該優先使用幾個可能的 `~` 運算子中的哪一個。我們可以用明確的型別轉換來協助它：

```

SELECT ~ CAST('20' AS int8) AS "negation";

 negation
----------
      -21
(1 row)
```

<br><a id="id-1.5.9.7.9"></a>

**範例 10.4. 陣列包含運算子的型別解析**

以下是另一個解析具有一個已知輸入與一個未知輸入之運算子的範例：

```

SELECT array[1,2] <@ '{1,2,3}' as "is subset";

 is subset
-----------
 t
(1 row)
```

PostgreSQL 的運算子系統目錄中有好幾個中置運算子 `<@` 的項目，但其中可能在左側接受整數陣列的只有兩個：陣列包含（`anyarray` `<@` `anyarray`）與範圍包含（`anyelement` `<@` `anyrange`）。由於這些多型虛擬型別（請參閱[第 8.21 節](../datatype/datatype-pseudo.md)）都不被視為優先型別，剖析器無法依此解決歧義。不過，[步驟 3.f](typeconv-oper.md#OP-RESOL-LAST-UNKNOWN) 告訴它要假設型別未知的字面值與另一個輸入的型別相同，也就是整數陣列。這時兩個運算子中只有一個能相符，因此會選擇陣列包含。（如果選到的是範圍包含，我們就會得到錯誤，因為該字串的格式不是正確的範圍字面值。）

<br><a id="id-1.5.9.7.10"></a>

**範例 10.5. 網域型別上的自訂運算子**

使用者有時會嘗試宣告只適用於某個網域型別的運算子。這是可行的，但遠不如看起來那麼有用，因為運算子解析規則的設計是選擇適用於網域基礎型別的運算子。例如，考慮

```

CREATE DOMAIN mytext AS text CHECK(...);
CREATE FUNCTION mytext_eq_text (mytext, text) RETURNS boolean AS ...;
CREATE OPERATOR = (procedure=mytext_eq_text, leftarg=mytext, rightarg=text);
CREATE TABLE mytable (val mytext);

SELECT * FROM mytable WHERE val = 'foo';
```

這個查詢不會使用自訂運算子。剖析器會先檢查是否有 `mytext` `=` `mytext` 運算子（[步驟 2.a](typeconv-oper.md#OP-RESOL-EXACT-UNKNOWN)），但並沒有；接著它會考慮網域的基礎型別 `text`，並檢查是否有 `text` `=` `text` 運算子（[步驟 2.b](typeconv-oper.md#OP-RESOL-EXACT-DOMAIN)），而這個運算子確實存在；因此它會將 `unknown` 型別的字面值解析為 `text`，並使用 `text` `=` `text` 運算子。要讓自訂運算子被使用，唯一的方法是明確轉換字面值的型別：

```

SELECT * FROM mytable WHERE val = text 'foo';
```

這樣就能依完全相符規則立即找到 `mytext` `=` `text` 運算子。如果進入了最佳相符規則，這些規則會刻意排除網域型別上的運算子。如果不這麼做，這樣的運算子會造成太多有歧義的運算子錯誤，因為型別轉換規則總是將網域視為可以與其基礎型別互相轉換，因此在所有能使用基礎型別上同名運算子的情況下，網域運算子也都會被視為可用。

<br>

<br>

---

<a id="ftn.OP-QUALIFIED-SECURITY"></a>

[[9]](#OP-QUALIFIED-SECURITY) 
使用未以 schema 限定的名稱時不會產生這種風險，因為包含允許不受信任使用者建立物件之 schema 的搜尋路徑，並不是[安全的 schema 使用模式](../ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/typeconv-oper.html)（原文版本：18.6；核對日期：2026-09-11）
