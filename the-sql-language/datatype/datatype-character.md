<a id="DATATYPE-CHARACTER"></a>
## 8.3. 字元型別 [#](#DATATYPE-CHARACTER)

<a id="id-1.5.7.11.2"></a><a id="id-1.5.7.11.3"></a><a id="id-1.5.7.11.4"></a><a id="id-1.5.7.11.5"></a><a id="id-1.5.7.11.6"></a><a id="id-1.5.7.11.7"></a><a id="id-1.5.7.11.8"></a><a id="id-1.5.7.11.9"></a><a id="DATATYPE-CHARACTER-TABLE"></a>

**表 8.4. 字元型別**

<table border="1" class="table" summary="Character Types"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">character varying(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">varchar(<em class="replaceable"><code>n</code></em>)</code></td><td>可變長度，有長度限制</td></tr><tr><td><code class="type">character(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">char(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">bpchar(<em class="replaceable"><code>n</code></em>)</code></td><td>固定長度，以空白填補</td></tr><tr><td><code class="type">bpchar</code></td><td>可變長度且無上限，會修剪尾端空白</td></tr><tr><td><code class="type">text</code></td><td>可變長度且無上限</td></tr></tbody></table>

<br>

[表 8.4](datatype-character.md#DATATYPE-CHARACTER-TABLE) 顯示了 PostgreSQL 中可用的通用字元型別。

SQL 定義了兩種主要的字元型別：`character varying(n)` 與 `character(n)`，其中 *`n`* 是一個正整數。這兩種型別都可以儲存長度最多達
*`n`* 個字元（而非位元組）的字串。若試圖將更長的字串儲存到這些型別的欄位中，將會導致錯誤，除非超出長度的部分全部都是空白，此時字串會被截斷至最大長度。（這個有點奇特的例外情況是
SQL 標準所要求的。）
不過，若明確地將某個值轉型為 `character
varying(n)` 或
`character(n)`，超過長度的值會被截斷為 *`n`* 個字元，而不會引發錯誤。（這一點同樣是
SQL 標準所要求的。）
若要儲存的字串比宣告的長度短，`character` 型別的值會以空白填補；`character varying`
型別的值則只會單純儲存較短的字串。

此外，PostgreSQL 提供了
`text` 型別，可儲存任意長度的字串。雖然 `text` 型別並不屬於
SQL 標準，但其他幾種 SQL 資料庫管理系統也同樣提供此型別。
`text` 是 PostgreSQL
原生的字串資料型別，因為大多數處理字串的內建函式，其宣告的接受或傳回型別都是 `text` 而非 `character
varying`。就許多用途而言，`character varying`
的行為就像是建立在 `text` 之上的一個[網域](domains.md)。

型別名稱 `varchar` 是 `character
varying` 的別名；而 `bpchar`（附帶長度指定符時）與
`char` 則是 `character` 的別名。
`varchar` 與 `char` 這兩個別名是
SQL 標準所定義的；`bpchar` 則是
PostgreSQL 的擴充功能。

若有指定，長度 *`n`* 必須大於零，且不得超過
10,485,760。若 `character
varying`（或 `varchar`）在使用時未指定長度，該型別可接受任意長度的字串。若
`bpchar` 未指定長度，它同樣可接受任意長度的字串，但尾端空白在語意上並不重要。若
`character`（或 `char`）未指定長度，
則等同於 `character(1)`。

`character` 型別的值，在實際儲存與顯示時，
會以空白填補至指定的寬度 *`n`*。不過，尾端空白在語意上並不重要，
在比較兩個 `character` 型別的值時會被忽略。在空白具有意義的定序
（collation）中，這種行為可能會產生非預期的結果；
舉例來說 `SELECT 'a '::CHAR(2) collate "C" <
E'a\n'::CHAR(2)` 會傳回 true，即使在 `C`
語系（locale）中，空白會被視為大於換行符。
將 `character` 值轉換為其他字串型別之一時，尾端空白會被移除。請注意，在
`character varying` 與 `text` 值中，尾端空白
*確實*在語意上具有意義，在使用模式比對，也就是 `LIKE` 與
正規表示式時，也是如此。

這些資料型別中可以儲存的字元，是由建立資料庫時所選擇的
資料庫字元集所決定的。無論採用哪一種特定的字元集，
編碼為零的字元（有時稱為 NUL）都無法被儲存。
詳情請參閱[23.3 節](../../server-administration/charset/multibyte.md)。

較短字串（最多 126 位元組）的儲存需求，是 1 位元組再加上實際的字串內容，
在 `character` 的情況下，還包含空白填補的部分。較長的字串則有 4
位元組的額外負擔，而非 1 位元組。系統會自動壓縮較長的字串，因此
磁碟上實際所需的空間可能較少。非常長的值也會另外儲存於背景資料表中，以免
影響對較短欄位值的快速存取。無論如何，可儲存的最長
字元字串大約是 1 GB。（資料型別宣告中允許用於 *`n`*
的最大值比這個數字還要小。變更這個上限並不會帶來實質幫助，因為在
多位元組字元編碼下，字元數與位元組數可能有相當大的差異。若您
想要儲存沒有特定上限的長字串，建議使用不指定長度的
`text` 或 `character varying`，而不要自行
訂出一個任意的長度上限。）

### 提示

這三種型別之間並沒有效能上的差異，除了使用空白填補
型別時會增加儲存空間，以及在儲存到有長度限制的欄位時，需要額外花一些
CPU 週期來檢查長度之外。雖然
`character(n)` 在某些其他資料庫系統中具有效能
優勢，但在 PostgreSQL 中並沒有這樣的優勢；事實上
`character(n)` 通常是這三者中最慢的，因為它有額外的儲存成本。在大多數情況下，應該改用
`text` 或 `character varying`。

關於字串常值語法的相關資訊，請參閱[4.1.2.1 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)；
關於可用運算子與函式的相關資訊，請參閱[第 9 章](../functions/README.md)。

<a id="id-1.5.7.11.21"></a>

**範例 8.1. 使用字元型別**

```

CREATE TABLE test1 (a character(4));
INSERT INTO test1 VALUES ('ok');
SELECT a, char_length(a) FROM test1; -- (1)

  a   | char_length
------+-------------
 ok   |           2


CREATE TABLE test2 (b varchar(5));
INSERT INTO test2 VALUES ('ok');
INSERT INTO test2 VALUES ('good      ');
INSERT INTO test2 VALUES ('too long');
ERROR:  value too long for type character varying(5)
INSERT INTO test2 VALUES ('too long'::varchar(5)); -- explicit truncation
SELECT b, char_length(b) FROM test2;

   b   | char_length
-------+-------------
 ok    |           2
 good  |           5
 too l |           5
```

<a id="co.datatype-char"></a>

<table border="0" summary="Callout list"><tr><td align="left" valign="top" width="5%"><p><a href="#co.datatype-char">(1)</a> </p></td><td align="left" valign="top"><p>
       <code class="function">char_length</code> 函式在
       <a class="xref" href="../functions/functions-string.md">9.4 節</a>中討論。
      </p></td></tr></table>

<br>

PostgreSQL 中還有另外兩種固定長度的字元型別，
如[表 8.5](datatype-character.md#DATATYPE-CHARACTER-SPECIAL-TABLE)所示。
這些型別並非設計供一般用途使用，只用於
內部系統目錄中。
`name` 型別用來儲存識別字。其
長度目前定義為 64 位元組（63 個可用字元加上
結尾符），但在 `C` 原始碼中應以常數
`NAMEDATALEN` 來參照。
此長度是在編譯時期設定的（因此可視特殊用途調整）；
未來版本中預設的最大長度可能會改變。型別
`"char"`（請注意有引號）與 `char(1)` 不同，
它只使用一個位元組的儲存空間，因此只能儲存單一
ASCII 字元。它在系統
目錄中被用作一種簡易的列舉型別。

<a id="DATATYPE-CHARACTER-SPECIAL-TABLE"></a>

**表 8.5. 特殊字元型別**

<table border="1" class="table" summary="Special Character Types"><colgroup><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>儲存大小</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">"char"</code></td><td>1 位元組</td><td>單一位元組的內部型別</td></tr><tr><td><code class="type">name</code></td><td>64 位元組</td><td>用於物件名稱的內部型別</td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-character.html)（原文版本：18.6；核對日期：2026-09-15）
