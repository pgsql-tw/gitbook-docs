<a id="XML-LIMITS-CONFORMANCE"></a>

## D.3. XML 限制與 SQL/XML 符合性 [#](#XML-LIMITS-CONFORMANCE)

[D.3.1. 查詢僅限於 XPath 1.0](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-XPATH1)

[D.3.2. 實作上的附帶限制](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL)

<a id="id-1.11.5.13.2"></a>

ISO/IEC 9075-14（SQL/XML）中 XML 相關規範的重大修訂是在 SQL:2006 引入的。
PostgreSQL 對 XML 資料型別及相關函式的實作大致遵循較早的 2003 年版，並從較新的版本借用了部分內容。具體而言：

* 現行標準提供一系列 XML 資料型別，用來存放無型別或依 XML Schema 定型之變體的「document」或「content」，並提供型別
  `XML(SEQUENCE)` 來存放任意的 XML 內容片段；而
  PostgreSQL 只提供單一的
  `xml` 型別，可存放「document」或
  「content」。標準中的「sequence」型別沒有對應的型別。
* PostgreSQL 提供了兩個在 SQL:2006 引入的函式，但其變體使用的是 XPath 1.0
  語言，而非標準中為它們指定的 XML Query。
* PostgreSQL 不支援
  `RETURNING CONTENT` 或 `RETURNING SEQUENCE`
  子句；規範中定義為具有這些子句的函式，一律隱含地回傳內容（content）。

本節說明你可能會遇到的部分差異。

<a id="FUNCTIONS-XML-LIMITS-XPATH1"></a>

### D.3.1. 查詢僅限於 XPath 1.0 [#](#FUNCTIONS-XML-LIMITS-XPATH1)

PostgreSQL 特有的函式
`xpath()` 與 `xpath_exists()`
使用 XPath 語言查詢 XML 文件。
PostgreSQL 也為標準函式 `XMLEXISTS` 與
`XMLTABLE` 提供僅支援 XPath 的變體，而這兩個標準函式正式上使用的是
XQuery 語言。對於上述所有函式，
PostgreSQL 都仰賴
libxml2 函式庫，而該函式庫只提供 XPath 1.0。

XQuery 語言與 XPath 2.0 及之後的版本之間有很強的關聯：任何在兩者中語法皆有效且能成功執行的運算式，都會產生相同的結果（只有一個小例外：含有數值字元參照或預先定義實體參照的運算式，XQuery 會將其替換為對應的字元，而 XPath 則保持原樣）。但這些語言與 XPath 1.0 之間並沒有這樣的關聯；XPath 1.0 是較早的語言，在許多方面都有所不同。

需要留意的限制有兩類：一是 SQL 標準所規定的函式從 XQuery 限縮為 XPath，二是標準函式與
PostgreSQL 特有函式都將 XPath 限縮為 1.0 版。

<a id="FUNCTIONS-XML-LIMITS-XPATH1-XQUERY-RESTRICTION"></a>

#### D.3.1.1. 從 XQuery 限縮為 XPath [#](#FUNCTIONS-XML-LIMITS-XPATH1-XQUERY-RESTRICTION)

XQuery 超出 XPath 的特性包括：

* 除了所有可能的 XPath 值之外，XQuery 運算式還可以建構並回傳新的 XML 節點。XPath 可以建立並回傳原子型別（數字、字串等）的值，但只能回傳原本就存在於作為運算式輸入之文件中的 XML 節點。
* XQuery 具有用於迭代、排序與分組的控制結構。
* XQuery 允許宣告並使用區域函式。

較新的 XPath 版本開始提供與上述功能重疊的能力（例如函數式風格的 `for-each` 與
`sort`、匿名函式，以及用來從字串建立節點的
`parse-xml`），但這些特性在 XPath 3.0 之前都無法使用。

<a id="XML-XPATH-1-SPECIFICS"></a>

#### D.3.1.2. 將 XPath 限縮為 1.0 [#](#XML-XPATH-1-SPECIFICS)

對熟悉 XQuery 與 XPath 2.0 或之後版本的開發者而言，XPath 1.0
有許多需要應付的差異：

* XQuery/XPath 運算式的基本型別
  `sequence` 可以包含 XML 節點、原子值，或兩者兼有，但它在 XPath 1.0 中並不存在。1.0 的運算式只能產生節點集合（包含零個或多個 XML 節點），或單一原子值。
* XQuery/XPath 的序列（sequence）可以依任何所需順序包含任何所需項目；與此不同，XPath 1.0 的節點集合沒有保證的順序，而且如同任何集合，不允許同一個項目出現超過一次。

  ### 注意

  libxml2 函式庫似乎總是將節點集合傳回給 PostgreSQL，
  且其成員維持在輸入文件中的相對順序。但其文件並未承諾此行為，而 XPath 1.0 運算式也無法控制它。
* XQuery/XPath 提供 XML Schema 中定義的所有型別，以及作用於這些型別的許多運算子與函式；而 XPath 1.0 只有節點集合與三種原子型別 `boolean`、
  `double` 與 `string`。
* XPath 1.0 沒有條件運算子。像
  `if ( hat ) then hat/@size else "no hat"`
  這樣的 XQuery/XPath 運算式，在 XPath 1.0 中沒有對應的寫法。
* XPath 1.0 沒有字串的大小比較運算子。
  `"cat" < "dog"` 與
  `"cat" > "dog"` 皆為 false，因為兩者都是兩個 `NaN` 的數值比較。相對地，
  `=` 與 `!=` 則確實是以字串的方式比較字串。
* XPath 1.0 模糊了 XQuery/XPath 所定義之
  *value comparisons*（值比較）與
  *general comparisons*（一般比較）之間的區別。`sale/@hatsize = 7` 與
  `sale/@customer = "alice"` 都是存在量化的比較：只要有任何
  `sale` 的該屬性具有指定的值，結果即為 true；但 `sale/@taxable = false()` 則是與整個節點集合之
  *effective boolean value*（有效布林值）進行的值比較。
  只有在沒有任何 `sale` 具有
  `taxable` 屬性時，它才為 true。
* 在 XQuery/XPath 資料模型中，*document
  node*（文件節點）可以是文件（document）形式（亦即恰好一個最上層元素，元素之外只有註解與處理指令），也可以是內容（content）形式（放寬上述限制）。它在 XPath 1.0 中的對應物
  *root node*（根節點）只能是文件形式。
  這也是為什麼作為上下文項目傳給任何 PostgreSQL
  以 XPath 為基礎之函式的 `xml` 值必須是文件形式的原因之一。

此處列出的差異並不完整。在 XQuery 以及 XPath 2.0 與之後的版本中，有一個 XPath 1.0 相容模式，而 W3C 列出的該模式下所套用的
[函式庫變更](https://www.w3.org/TR/2010/REC-xpath-functions-20101214/#xpath1-compatibility)
與
[語言變更](https://www.w3.org/TR/xpath20/#id-backwards-compatibility)
清單，對這些差異提供了更完整（但仍非詳盡無遺）的說明。相容模式無法讓較新的語言與 XPath 1.0 完全等價。

<a id="FUNCTIONS-XML-LIMITS-CASTS"></a>

#### D.3.1.3. SQL 與 XML 資料型別及值之間的對應 [#](#FUNCTIONS-XML-LIMITS-CASTS)

在 SQL:2006 及之後的版本中，標準 SQL 資料型別與 XML Schema 型別之間雙向的轉換都有精確的規定。然而，這些規則是以 XQuery/XPath 的型別與語意表達的，無法直接套用於 XPath 1.0 不同的資料模型。

當 PostgreSQL 將 SQL 資料值對應到 XML（如在 `xmlelement` 中），或將 XML 對應到 SQL（如在 `xmltable` 的輸出欄位中）時，除了少數特別處理的情況之外，PostgreSQL 只是假設
XML 資料型別的 XPath 1.0 字串形式會是 SQL 資料型別的有效文字輸入形式，反之亦然。這項規則的優點是簡單，同時對許多資料型別而言，產生的結果也與標準中規定的對應相近。

若需考量與其他系統的互通性，對某些資料型別而言，可能需要明確使用資料型別格式化函式（例如[第 9.8 節](../../the-sql-language/functions/functions-formatting.md)中的函式）來產生標準的對應。

<a id="FUNCTIONS-XML-LIMITS-POSTGRESQL"></a>

### D.3.2. 實作上的附帶限制 [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL)

本節說明的限制並非 libxml2 函式庫本身所固有，而是適用於 PostgreSQL 目前的實作。

<a id="FUNCTIONS-XML-LIMITS-POSTGRESQL-BY-VALUE-ONLY"></a>

#### D.3.2.1. 只支援 `BY VALUE` 傳遞機制 [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL-BY-VALUE-ONLY)

SQL 標準定義了兩種 *passing mechanisms*（傳遞機制），
適用於將 XML 引數從 SQL 傳給 XML 函式或接收結果時：`BY REF`，此時特定的 XML
值會保留其節點識別；以及 `BY VALUE`，此時會傳遞 XML 的內容，但不保留節點識別。傳遞機制可以指定在參數清單之前，作為所有參數的預設機制；也可以指定在任何參數之後，以覆寫預設機制。

為了說明其中的差異，若
*`x`* 是一個 XML 值，則下列兩個查詢在
SQL:2006 環境中會分別產生 true 與 false：

```

SELECT XMLQUERY('$a is $b' PASSING BY REF x AS a, x AS b NULL ON EMPTY);
SELECT XMLQUERY('$a is $b' PASSING BY VALUE x AS a, x AS b NULL ON EMPTY);
```

PostgreSQL 在
`XMLEXISTS` 或 `XMLTABLE`
建構中會接受 `BY VALUE` 或 `BY REF`，但會忽略它們。`xml` 資料型別存放的是序列化的字元字串表示，因此沒有節點識別需要保留，而傳遞實際上一律是 `BY
VALUE`。

<a id="FUNCTIONS-XML-LIMITS-POSTGRESQL-NAMED-PARAMETERS"></a>

#### D.3.2.2. 無法將具名參數傳給查詢 [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL-NAMED-PARAMETERS)

以 XPath 為基礎的函式支援傳遞一個參數作為 XPath 運算式的上下文項目，但不支援傳遞其他值作為具名參數供運算式使用。

<a id="FUNCTIONS-XML-LIMITS-POSTGRESQL-NO-XML-SEQUENCE"></a>

#### D.3.2.3. 沒有 `XML(SEQUENCE)` 型別 [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL-NO-XML-SEQUENCE)

PostgreSQL 的 `xml` 資料型別只能存放 `DOCUMENT`
或 `CONTENT` 形式的值。XQuery/XPath 運算式的上下文項目必須是單一 XML 節點或原子值，但 XPath 1.0
進一步限制它只能是 XML 節點，而且沒有允許 `CONTENT` 的節點型別。結果是，格式正確（well-formed）的 `DOCUMENT` 是
PostgreSQL 唯一能作為 XPath 上下文項目提供的 XML 值形式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xml-limits-conformance.html)（原文版本：18.6；核對日期：2026-10-22）
