# 8.14.7. jsonpath 型別

<a id="DATATYPE-JSONPATH"></a>

## 8.14.7. jsonpath 型別 [#](#datatype-jsonpath) <a href="#datatype-jsonpath" id="datatype-jsonpath"></a>

<a id="id-1.5.7.22.21.2"></a>

`jsonpath` 型別在
PostgreSQL 中實作了對 SQL/JSON 路徑語言的支援，以有效率地查詢 JSON 資料。
它提供了已剖析之 SQL/JSON 路徑運算式的二進位表示，
指定路徑引擎要從 JSON 資料中擷取哪些項目，
供後續以 SQL/JSON 查詢函式進行處理。

SQL/JSON 路徑述詞與運算子的語意大致遵循 SQL 的做法。
同時，為了提供處理 JSON 資料的自然方式，
SQL/JSON 路徑語法採用了一些 JavaScript 的慣例：

* 點號（`.`）用於成員存取。
* 方括號（`[]`）用於陣列存取。
* SQL/JSON 陣列是以 0 為起始的，這與從 1 開始的一般 SQL
  陣列不同。

SQL/JSON 路徑運算式中的數值字面量遵循 JavaScript 規則，
這在某些小細節上與 SQL 及 JSON 都不同。舉
例來說，SQL/JSON 路徑允許使用 `.1` 與
`1.`，這在 JSON 中是無效的。系統支援非十進位整數
字面量與底線分隔符，例如
`1_000_000`、`0x1EEE_FFFF`、
`0o273`、`0b100101`。在 SQL/JSON 路徑
中（在 JavaScript 中也一樣，但並非 SQL 本身固有的語法），底線
分隔符不得緊接在基數前置詞之後。

SQL/JSON 路徑運算式通常會以 SQL 字元字串字面量的形式
寫在 SQL 查詢中，因此必須以單引號括住，
其中若需要單引號，則必須以雙倍表示
（請參閱[4.1.2.1 節](../../sql-syntax/sql-syntax-lexical/sql-syntax-constants.md#sql-syntax-strings)）。
某些形式的路徑運算式在其中需要字串字面量。
這些內嵌的字串字面量遵循 JavaScript／ECMAScript 慣例：
必須以雙引號括住，並可以在其中使用反斜線逸出序列
來表示原本難以輸入的字元。
特別是，若要在內嵌字串字面量中寫入雙引號，方式為
`\"`；若要寫入反斜線本身，
則必須寫成 `\\`。其他特殊的反斜線序列
還包括 JavaScript 字串中所辨識的：
`\b`、
`\f`、
`\n`、
`\r`、
`\t`、
`\v`，
用於表示各種 ASCII 控制字元，
`\xNN` 用於表示以兩位十六進位數字
書寫的字元碼，
`\uNNNN` 用於表示由 4 位十六進位碼位
所識別的 Unicode 字元，而
`\u{N...}` 則用於表示以 1 到 6 位
十六進位數字書寫的 Unicode 字元碼位。

路徑運算式由一連串路徑元素組成，
可以是下列任何一種：

* JSON 基本型別的路徑字面量：
  Unicode 文字、數字、true、false 或 null。
* [表 8.24](#type-jsonpath-variables)中所列的路徑變數。
* [表 8.25](#type-jsonpath-accessors)中所列的存取器運算子。
* [9.16.2.3 節](../../functions/functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS)中所列的
  `jsonpath` 運算子與方法。
* 括號，可用於提供篩選運算式
  或定義路徑求值的順序。

關於在 SQL/JSON 查詢函式中使用 `jsonpath` 運算式的
詳情，請參閱[9.16.2 節](../../functions/functions-json.md#functions-sqljson-path)。

<a id="TYPE-JSONPATH-VARIABLES"></a>

### 表 8.24. `jsonpath` 變數 [#](#type-jsonpath-variables) <a href="#type-jsonpath-variables" id="type-jsonpath-variables"></a>

<table border="1" class="table" summary="jsonpath 變數"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>變數</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">$</code></td><td>代表被查詢之 JSON 值的變數
      （即<em class="firstterm">上下文項目</em>）。
      </td></tr><tr><td><code class="literal">$varname</code></td><td>
        具名變數。其值可透過多個 JSON 處理函式的
        <em class="parameter"><code>vars</code></em> 參數設定；
        詳情請參閱<a class="xref" href="../../functions/functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE">表 9.51</a>。
      </td></tr><tr><td><code class="literal">@</code></td><td>代表篩選運算式中路徑求值結果的
      變數。
      </td></tr></tbody></table>

<br><a id="TYPE-JSONPATH-ACCESSORS"></a>

### 表 8.25. `jsonpath` 存取器 [#](#type-jsonpath-accessors) <a href="#type-jsonpath-accessors" id="type-jsonpath-accessors"></a>

<table border="1" class="table" summary="jsonpath 存取器"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>存取器運算子</th><th>說明</th></tr></thead><tbody><tr><td>
<p>
<code class="literal">.<em class="replaceable"><code>key</code></em></code>
</p>
<p>
<code class="literal">."$<em class="replaceable"><code>varname</code></em>"</code>
</p>
</td><td>
<p>
        成員存取器，傳回具有指定鍵的物件成員。若鍵名
        與某個以 <code class="literal">$</code> 開頭的具名變數相符，
        或不符合識別字的
        JavaScript 規則，則必須以雙引號括住，使其成為字串字面量。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">.*</code>
</p>
</td><td>
<p>
        萬用字元成員存取器，傳回位於目前物件頂層的所有
        成員之值。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">.**</code>
</p>
</td><td>
<p>
        遞迴萬用字元成員存取器，會處理目前物件之 JSON 階層的所有
        層級，並傳回所有的
        成員值，無論其巢狀層級為何。這是
        <span class="productname">PostgreSQL</span> 對
        SQL/JSON 標準的擴充。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">.**{<em class="replaceable"><code>level</code></em>}</code>
</p>
<p>
<code class="literal">.**{<em class="replaceable"><code>start_level</code></em> to
        <em class="replaceable"><code>end_level</code></em>}</code>
</p>
</td><td>
<p>
        與 <code class="literal">.**</code> 類似，但只選取指定的
        JSON 階層層級。巢狀層級以整數指定。
        第零層對應目前的物件。若要存取最低的
        巢狀層級，可以使用 <code class="literal">last</code> 關鍵字。
        這是 <span class="productname">PostgreSQL</span> 對
        SQL/JSON 標準的擴充。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">[<em class="replaceable"><code>subscript</code></em>, ...]</code>
</p>
</td><td>
<p>
        陣列元素存取器。
        <code class="literal"><em class="replaceable"><code>subscript</code></em></code> 可以
        以兩種形式給定：<code class="literal"><em class="replaceable"><code>index</code></em></code>
        或 <code class="literal"><em class="replaceable"><code>start_index</code></em> to <em class="replaceable"><code>end_index</code></em></code>。
        第一種形式依索引傳回單一陣列元素。第二種
        形式則依索引範圍傳回一段陣列切片，包含對應於所提供的
        <em class="replaceable"><code>start_index</code></em> 與 <em class="replaceable"><code>end_index</code></em> 的
        元素。
       </p>
<p>
        指定的 <em class="replaceable"><code>index</code></em> 可以是整數，
        也可以是傳回單一數值的運算式，該數值會自動
        轉型為整數。索引零對應陣列的第一個
        元素。您也可以使用 <code class="literal">last</code> 關鍵字
        來表示陣列的最後一個元素，這對於處理長度未知的
        陣列相當有用。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">[*]</code>
</p>
</td><td>
<p>
        萬用字元陣列元素存取器，傳回所有陣列元素。
       </p>
</td></tr></tbody></table>

<br>

<br>

[返回 8.14. JSON 型別](../datatype-json.md#datatype-json)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-json.html)（原文版本：18.6；核對日期：2026-09-25）
