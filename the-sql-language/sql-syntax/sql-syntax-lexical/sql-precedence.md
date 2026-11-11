# 4.1.6. 運算子優先順序

<a id="SQL-PRECEDENCE"></a>

## 4.1.6. 運算子優先順序 [#](#sql-precedence) <a href="#sql-precedence" id="sql-precedence"></a>

<a id="id-1.5.3.5.13.2"></a>

[表 4.2](#sql-precedence-table) 列出了 PostgreSQL 中運算子的優先順序與結合性。大多數運算子具有相同的優先順序，並且是左結合的。運算子的優先順序與結合性是寫死在剖析器中的。如果你希望包含多個運算子的運算式以不同於優先順序規則所暗示的方式剖析，請加上括號。

<a id="SQL-PRECEDENCE-TABLE"></a>

### 表 4.2. 運算子優先順序（由高至低） [#](#sql-precedence-table) <a href="#sql-precedence-table" id="sql-precedence-table"></a>

<table border="1" class="table" summary="Operator Precedence (highest to lowest)"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>運算子／元素</th><th>結合性</th><th>說明</th></tr></thead><tbody><tr><td><code class="token">.</code></td><td>左</td><td>資料表／欄位名稱分隔符號</td></tr><tr><td><code class="token">::</code></td><td>左</td><td><span class="productname">PostgreSQL</span> 風格的型別轉換</td></tr><tr><td><code class="token">[</code> <code class="token">]</code></td><td>左</td><td>陣列元素選取</td></tr><tr><td><code class="token">+</code> <code class="token">-</code></td><td>右</td><td>一元正號、一元負號</td></tr><tr><td><code class="token">COLLATE</code></td><td>左</td><td>定序選取</td></tr><tr><td><code class="token">AT</code></td><td>左</td><td><code class="literal">AT TIME ZONE</code>、<code class="literal">AT LOCAL</code></td></tr><tr><td><code class="token">^</code></td><td>左</td><td>乘冪</td></tr><tr><td><code class="token">*</code> <code class="token">/</code> <code class="token">%</code></td><td>左</td><td>乘法、除法、取餘數</td></tr><tr><td><code class="token">+</code> <code class="token">-</code></td><td>左</td><td>加法、減法</td></tr><tr><td>（任何其他運算子）</td><td>左</td><td>所有其他原生與使用者自訂的運算子</td></tr><tr><td><code class="token">BETWEEN</code> <code class="token">IN</code> <code class="token">LIKE</code> <code class="token">ILIKE</code> <code class="token">SIMILAR</code></td><td> </td><td>範圍包含、集合成員資格、字串比對</td></tr><tr><td><code class="token">&lt;</code> <code class="token">&gt;</code> <code class="token">=</code> <code class="token">&lt;=</code> <code class="token">&gt;=</code> <code class="token">&lt;&gt;</code>
</td><td> </td><td>比較運算子</td></tr><tr><td><code class="token">IS</code> <code class="token">ISNULL</code> <code class="token">NOTNULL</code></td><td> </td><td><code class="literal">IS TRUE</code>、<code class="literal">IS FALSE</code>、<code class="literal">IS
       NULL</code>、<code class="literal">IS DISTINCT FROM</code> 等等</td></tr><tr><td><code class="token">NOT</code></td><td>右</td><td>邏輯否定</td></tr><tr><td><code class="token">AND</code></td><td>左</td><td>邏輯且</td></tr><tr><td><code class="token">OR</code></td><td>左</td><td>邏輯或</td></tr></tbody></table>

<br>

請注意，運算子優先順序規則也適用於與上述內建運算子同名的使用者自訂運算子。例如，如果你為某個自訂資料型別定義了一個「+」運算子，不論你的運算子做什麼事，它都會與內建的「+」運算子具有相同的優先順序。

在 `OPERATOR` 語法中使用以 schema 限定的運算子名稱時，例如：

```

SELECT 3 OPERATOR(pg_catalog.+) 4;
```

`OPERATOR` 結構會被視為具有[表 4.2](#sql-precedence-table) 中「任何其他運算子」的預設優先順序。無論 `OPERATOR()` 中出現的是哪一個特定運算子，都是如此。

### 注意

9.5 版之前的 PostgreSQL 使用略為不同的運算子優先順序規則。特別是，`<=`、`>=` 與 `<>` 過去被當作一般的運算子處理；`IS` 測試過去具有較高的優先順序；而 `NOT BETWEEN` 及相關結構的行為則不一致，在某些情況下會被當作具有 `NOT` 的優先順序，而不是 `BETWEEN` 的優先順序。這些規則之所以變更，是為了更符合 SQL 標準，並減少對邏輯上等價之結構處理不一致所造成的混淆。在大多數情況下，這些變更不會造成任何行為上的改變，或者可能會造成「no such operator」（找不到這種運算子）的錯誤，而這可以透過加上括號來解決。不過，也有一些特殊情況下，查詢的行為可能會改變，卻不會回報任何剖析錯誤。

[返回 4.1. 詞彙結構](../sql-syntax-lexical.md#sql-syntax-lexical)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-syntax-lexical.html)（原文版本：18.6；核對日期：2026-09-11）
