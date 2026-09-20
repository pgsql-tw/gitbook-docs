<a id="EXTEND-TYPE-SYSTEM"></a>
## 36.2. PostgreSQL 型別系統 [#](#EXTEND-TYPE-SYSTEM)

[36.2.1. 基礎型別](extend-type-system.md#EXTEND-TYPE-SYSTEM-BASE)

[36.2.2. 容器型別](extend-type-system.md#EXTEND-TYPE-SYSTEM-CONTAINER)

[36.2.3. 網域](extend-type-system.md#EXTEND-TYPE-SYSTEM-DOMAINS)

[36.2.4. 虛擬型別](extend-type-system.md#EXTEND-TYPE-SYSTEM-PSEUDO)

[36.2.5. 多型型別](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)

<a id="id-1.8.3.5.2"></a><a id="id-1.8.3.5.3"></a><a id="id-1.8.3.5.4"></a><a id="id-1.8.3.5.5"></a><a id="id-1.8.3.5.6"></a><a id="id-1.8.3.5.7"></a>

PostgreSQL 的資料型別可以分為基礎
型別、容器型別、網域與虛擬型別。

<a id="EXTEND-TYPE-SYSTEM-BASE"></a>

### 36.2.1. 基礎型別 [#](#EXTEND-TYPE-SYSTEM-BASE)

基礎型別是指像 `integer` 這樣，在
SQL 語言層級之下實作的型別
（通常以 C 之類的低階語言撰寫）。它們大致對應於一般所稱的抽象資料型別。
PostgreSQL 只能透過使用者所提供的函式來操作這類
型別，並且僅在使用者已對其行為做出描述的範圍內，才能理解這類型別的行為。
內建的基礎型別說明於[第 8 章](../../the-sql-language/datatype/README.md)。

列舉（enum）型別可視為基礎型別的一個子類別。主要
差異在於，它們可以只用 SQL 命令建立，而不需要任何低階程式設計。
詳情請參閱[8.7 節](../../the-sql-language/datatype/datatype-enum.md)。

<a id="EXTEND-TYPE-SYSTEM-CONTAINER"></a>

### 36.2.2. 容器型別 [#](#EXTEND-TYPE-SYSTEM-CONTAINER)

PostgreSQL 有三種「容器」
型別，也就是包含其他型別多個值的型別。這三種分別是陣列、複合型別與範圍型別。

陣列可以保存多個值，這些值都屬於同一種型別。系統會為每一種基礎型別、複合
型別、範圍型別與網域型別自動建立對應的陣列型別。但並不存在陣列的陣列。就
型別系統而言，多維陣列與一維陣列並無不同。詳情請參閱[8.15 節](../../the-sql-language/datatype/arrays.md)。

複合型別（或稱資料列型別），會在使用者
建立資料表時一併建立。也可以使用 [CREATE TYPE](../../reference/sql-commands/sql-createtype.md)
來定義一個沒有關聯資料表的「獨立」複合型別。複合型別
就是一份帶有相應欄位名稱的型別清單。複合型別的值，即為一組欄位值所組成的資料列或
紀錄。詳情請參閱[8.16 節](../../the-sql-language/datatype/rowtypes.md)。

範圍型別可以保存兩個相同型別的值，分別是該範圍的下界
與上界。範圍型別是由使用者建立的，不過也存在少數幾種內建的範圍型別。詳情請參閱[8.17 節](../../the-sql-language/datatype/rangetypes.md)。

<a id="EXTEND-TYPE-SYSTEM-DOMAINS"></a>

### 36.2.3. 網域 [#](#EXTEND-TYPE-SYSTEM-DOMAINS)

網域是以某個特定的底層型別為基礎，並且在許多用途上，都可以與其底層型別
互換使用。不過，網域可以帶有限制條件，將其有效值限縮為底層
型別所允許範圍的一個子集。網域是使用
SQL 命令 [CREATE DOMAIN](../../reference/sql-commands/sql-createdomain.md) 建立的。
詳情請參閱[8.18 節](../../the-sql-language/datatype/domains.md)。

<a id="EXTEND-TYPE-SYSTEM-PSEUDO"></a>

### 36.2.4. 虛擬型別 [#](#EXTEND-TYPE-SYSTEM-PSEUDO)

有少數幾種特殊用途的「虛擬型別」。
虛擬型別不能作為資料表的欄位，或容器型別的組成部分，但可以用來宣告函式的
引數與結果型別。這在型別系統中提供了一種機制，用以識別特殊
類別的函式。[表 8.27](../../the-sql-language/datatype/datatype-pseudo.md#DATATYPE-PSEUDOTYPES-TABLE) 列出了現有的
虛擬型別。

<a id="EXTEND-TYPES-POLYMORPHIC"></a>

### 36.2.5. 多型型別 [#](#EXTEND-TYPES-POLYMORPHIC)

<a id="id-1.8.3.5.13.2"></a><a id="id-1.8.3.5.13.3"></a><a id="id-1.8.3.5.13.4"></a><a id="id-1.8.3.5.13.5"></a>

有一些特別值得關注的虛擬型別，稱為*多型
型別*，用來宣告*多型
函式*。這項強大的功能，讓單一函式
定義即可對許多不同的資料型別進行操作，實際的資料型別會由特定呼叫中
實際傳入的資料型別所決定。多型型別列於
[表 36.1](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC-TABLE) 中。其用法範例
出現在[36.5.11 節](xfunc-sql.md#XFUNC-SQL-POLYMORPHIC-FUNCTIONS)中。

<a id="EXTEND-TYPES-POLYMORPHIC-TABLE"></a>

**表 36.1. 多型型別**

<table border="1" class="table" summary="Polymorphic Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>系列</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">anyelement</code></td><td>簡單</td><td>表示某函式可接受任何資料型別</td></tr><tr><td><code class="type">anyarray</code></td><td>簡單</td><td>表示某函式可接受任何陣列資料型別</td></tr><tr><td><code class="type">anynonarray</code></td><td>簡單</td><td>表示某函式可接受任何非陣列資料型別</td></tr><tr><td><code class="type">anyenum</code></td><td>簡單</td><td>表示某函式可接受任何列舉資料型別
        （見 <a class="xref" href="../../the-sql-language/datatype/datatype-enum.md">8.7 節</a>）
        </td></tr><tr><td><code class="type">anyrange</code></td><td>簡單</td><td>表示某函式可接受任何範圍資料型別
        （見 <a class="xref" href="../../the-sql-language/datatype/rangetypes.md">8.17 節</a>）
        </td></tr><tr><td><code class="type">anymultirange</code></td><td>簡單</td><td>表示某函式可接受任何多重範圍資料型別
        （見 <a class="xref" href="../../the-sql-language/datatype/rangetypes.md">8.17 節</a>）
        </td></tr><tr><td><code class="type">anycompatible</code></td><td>共通</td><td>表示某函式可接受任何資料型別，
        並自動將多個引數提升為單一共通資料型別
        </td></tr><tr><td><code class="type">anycompatiblearray</code></td><td>共通</td><td>表示某函式可接受任何陣列資料型別，
        並自動將多個引數提升為單一共通資料型別
        </td></tr><tr><td><code class="type">anycompatiblenonarray</code></td><td>共通</td><td>表示某函式可接受任何非陣列資料型別，
        並自動將多個引數提升為單一共通資料型別
        </td></tr><tr><td><code class="type">anycompatiblerange</code></td><td>共通</td><td>表示某函式可接受任何範圍資料型別，
        並自動將多個引數提升為單一共通資料型別
        </td></tr><tr><td><code class="type">anycompatiblemultirange</code></td><td>共通</td><td>表示某函式可接受任何多重範圍資料型別，
        並自動將多個引數提升為單一共通資料型別
        </td></tr></tbody></table>

<br>

多型引數與結果彼此相互連結，並會在剖析呼叫某個多型函式的查詢時，
被解析為特定的資料型別。當有一個以上的多型引數時，輸入值
實際的資料型別必須依下述方式相符。若
該函式的結果型別為多型，或其輸出參數為多型型別，這些結果的
型別將依下述方式，由多型輸入的實際型別推導而得。

對於「簡單」系列的多型型別，其
比對與推導規則運作方式如下：

每個宣告為 `anyelement` 的位置（無論是引數或傳回值），都允許
使用任何特定的實際資料型別，但在任一次呼叫中，它們
全部都必須是*相同*的實際型別。每個
宣告為 `anyarray` 的位置，可以是任何陣列資料型別，
但同樣地，它們全部都必須是相同的型別。同樣地，
宣告為 `anyrange` 的位置也全部必須是相同的範圍
型別。`anymultirange` 亦是如此。

此外，若同時存在
宣告為 `anyarray` 與宣告為
`anyelement` 的位置，`anyarray`
位置上實際的陣列型別，其元素必須與
`anyelement` 位置上所出現的型別相同。
`anynonarray` 的處理方式與 `anyelement` 完全相同，
但額外加上了實際型別不得為陣列型別的限制。
`anyenum` 的處理方式與 `anyelement` 完全相同，
但額外加上了實際型別必須為列舉型別的限制。

同樣地，若同時存在宣告為 `anyrange`
以及宣告為 `anyelement` 或 `anyarray` 的位置，
`anyrange` 位置上實際的範圍型別，其子型別必須與
`anyelement` 位置上所出現的型別相同，
也必須與 `anyarray` 位置的元素型別相同。
若存在宣告為 `anymultirange` 的位置，
其實際的多重範圍型別，必須包含與宣告為 `anyrange`
的參數相符的範圍，以及與宣告為
`anyelement` 及 `anyarray` 的參數相符的基礎元素。

因此，當有一個以上的引數位置宣告為多型
型別時，其淨效果就是只允許特定組合的實際引數
型別。舉例來說，宣告為
`equal(anyelement, anyelement)` 的函式，會接受任何兩個輸入值，
只要它們屬於相同的資料型別即可。

當某函式的傳回值宣告為多型型別時，
至少必須有一個引數位置同樣是多型，而
提供給這些多型引數的實際資料型別，即決定了
該次呼叫的實際結果型別。舉例來說，若原本並不存在
陣列下標機制，我們或許可以定義一個函式，以
`subscript(anyarray, integer)
returns anyelement` 的形式實作下標存取。此宣告限制了實際的第一個
引數必須是陣列型別，並讓剖析器能從實際第一個引數的型別，推導出正確的
結果型別。另一個例子是，宣告為 `f(anyarray) returns anyenum`
的函式，將只會接受列舉型別的陣列。

在大多數情況下，剖析器可以從同一系列中屬於不同
多型型別的引數，推導出多型結果型別的實際資料型別；舉例來說，
`anyarray` 可以從 `anyelement` 推導而得，反之亦然。
但有一項例外：`anyrange` 型別的多型
結果，需要有一個 `anyrange` 型別的引數；它無法
從 `anyarray` 或 `anyelement` 引數推導而得。這是
因為可能存在多個子型別相同的範圍型別。

請注意，`anynonarray` 與 `anyenum` 並不代表
獨立的型別變數；它們與
`anyelement` 是相同的型別，只是額外附加了限制條件。舉例來說，
將函式宣告為 `f(anyelement, anyenum)`
等同於將其宣告為 `f(anyenum, anyenum)`：
兩個實際引數都必須是相同的列舉型別。

對於「共通」系列的多型型別，其
比對與推導規則的運作方式，大致與「簡單」系列
相同，但有一項主要差異：引數的實際
型別不需要完全相同，只要它們可以隱含轉型為單一共通型別即可。共通型別的
選擇方式，與 `UNION`
及相關結構所採用的規則相同（見[10.5 節](../../the-sql-language/typeconv/typeconv-union-case.md)）。
選擇共通型別時，會考量 `anycompatible` 與
`anycompatiblenonarray` 輸入的實際型別、
`anycompatiblearray` 輸入的陣列元素型別、
`anycompatiblerange` 輸入的範圍子型別，
以及 `anycompatiblemultirange` 輸入的多重範圍
子型別。若存在 `anycompatiblenonarray`，則
共通型別必須為非陣列型別。一旦確定共通型別後，
位於 `anycompatible` 與
`anycompatiblenonarray` 位置的引數，會自動
轉型為該型別，而位於 `anycompatiblearray`
位置的引數，則會自動轉型為該型別的陣列型別。

由於無法僅根據子型別來選出範圍型別，因此
使用 `anycompatiblerange` 及／或
`anycompatiblemultirange` 時，要求所有宣告為該型別的引數，都必須具有相同的實際範圍及／或多重範圍型別，且
該型別的子型別必須與所選出的共通型別一致，如此才不需要對
範圍值進行轉型。與 `anyrange` 及
`anymultirange` 相同，若將 `anycompatiblerange` 及
`anymultirange` 用作函式的結果型別，則要求必須存在一個
`anycompatiblerange` 或 `anycompatiblemultirange`
引數。

請注意，並不存在 `anycompatibleenum` 型別。這樣的
型別不會太有用，因為通常不存在任何轉型至列舉型別的
隱含轉型，這意味著將無法為相異的列舉輸入解析出共通型別。

「簡單」與「共通」這兩個多型
系列，代表兩組彼此獨立的型別變數。舉例來說，考慮以下範例

```

CREATE FUNCTION myfunc(a anyelement, b anyelement,
                       c anycompatible, d anycompatible)
RETURNS anycompatible AS ...
```

在此函式的實際呼叫中，前兩個輸入值必須具有
完全相同的型別。後兩個輸入值必須可提升為單一
共通型別，但此型別不需要與前兩個輸入值的
型別有任何關聯。結果將採用後兩個輸入值的共通型別。

可變引數函式（接受可變數量引數的函式，如
[36.5.6 節](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)所述）也可以是
多型函式：做法是將其最後一個參數宣告為
`VARIADIC` `anyarray` 或
`VARIADIC` `anycompatiblearray`。
就引數比對與判斷實際結果型別而言，這樣的函式表現得
就如同您撰寫了適當數量的
`anynonarray` 或 `anycompatiblenonarray`
參數一樣。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/extend-type-system.html)（原文版本：18.6；核對日期：2026-09-16）
