<a id="FUNCTIONS-LOGICAL"></a>

## 9.1. 邏輯運算子 [#](#FUNCTIONS-LOGICAL)

<a id="id-1.5.8.7.2"></a><a id="id-1.5.8.7.3"></a>

可用的是一般的邏輯運算子：
<a id="id-1.5.8.7.4.1"></a>
<a id="id-1.5.8.7.4.2"></a>
<a id="id-1.5.8.7.4.3"></a>
<a id="id-1.5.8.7.4.4"></a>
<a id="id-1.5.8.7.4.5"></a>
<a id="id-1.5.8.7.4.6"></a>

```

boolean AND boolean → boolean
boolean OR boolean → boolean
NOT boolean → boolean
```

SQL 使用三值邏輯系統，包含 true、false 以及代表「未知」的 `null`。請看下列真值表：

<table border="1" class="informaltable"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th><em class="replaceable"><code>a</code></em></th><th><em class="replaceable"><code>b</code></em></th><th><em class="replaceable"><code>a</code></em> AND <em class="replaceable"><code>b</code></em></th><th><em class="replaceable"><code>a</code></em> OR <em class="replaceable"><code>b</code></em></th></tr></thead><tbody><tr><td>TRUE</td><td>TRUE</td><td>TRUE</td><td>TRUE</td></tr><tr><td>TRUE</td><td>FALSE</td><td>FALSE</td><td>TRUE</td></tr><tr><td>TRUE</td><td>NULL</td><td>NULL</td><td>TRUE</td></tr><tr><td>FALSE</td><td>FALSE</td><td>FALSE</td><td>FALSE</td></tr><tr><td>FALSE</td><td>NULL</td><td>FALSE</td><td>NULL</td></tr><tr><td>NULL</td><td>NULL</td><td>NULL</td><td>NULL</td></tr></tbody></table>

<table border="1" class="informaltable"><colgroup><col/><col/></colgroup><thead><tr><th><em class="replaceable"><code>a</code></em></th><th>NOT <em class="replaceable"><code>a</code></em></th></tr></thead><tbody><tr><td>TRUE</td><td>FALSE</td></tr><tr><td>FALSE</td><td>TRUE</td></tr><tr><td>NULL</td><td>NULL</td></tr></tbody></table>

運算子 `AND` 與 `OR` 具有交換律，也就是說，你可以對調左右運算元而不影響結果。（不過，並不保證左運算元會在右運算元之前被評估。關於子運算式評估順序的更多資訊，請參閱[第 4.2.14 節](../sql-syntax/sql-expressions.md#SYNTAX-EXPRESS-EVAL)。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-logical.html)（原文版本：18.6；核對日期：2026-09-11）
