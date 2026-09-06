## 9.1. Logical Operators [#](#FUNCTIONS-LOGICAL)

<a id="id-1.5.8.7.2"></a><a id="id-1.5.8.7.3"></a>

The usual logical operators are available:
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

SQL uses a three-valued logic system with true,
false, and `null`, which represents “unknown”.
Observe the following truth tables:

<table border="1" class="informaltable"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th><em class="replaceable"><code>a</code></em></th><th><em class="replaceable"><code>b</code></em></th><th><em class="replaceable"><code>a</code></em> AND <em class="replaceable"><code>b</code></em></th><th><em class="replaceable"><code>a</code></em> OR <em class="replaceable"><code>b</code></em></th></tr></thead><tbody><tr><td>TRUE</td><td>TRUE</td><td>TRUE</td><td>TRUE</td></tr><tr><td>TRUE</td><td>FALSE</td><td>FALSE</td><td>TRUE</td></tr><tr><td>TRUE</td><td>NULL</td><td>NULL</td><td>TRUE</td></tr><tr><td>FALSE</td><td>FALSE</td><td>FALSE</td><td>FALSE</td></tr><tr><td>FALSE</td><td>NULL</td><td>FALSE</td><td>NULL</td></tr><tr><td>NULL</td><td>NULL</td><td>NULL</td><td>NULL</td></tr></tbody></table>

<table border="1" class="informaltable"><colgroup><col/><col/></colgroup><thead><tr><th><em class="replaceable"><code>a</code></em></th><th>NOT <em class="replaceable"><code>a</code></em></th></tr></thead><tbody><tr><td>TRUE</td><td>FALSE</td></tr><tr><td>FALSE</td><td>TRUE</td></tr><tr><td>NULL</td><td>NULL</td></tr></tbody></table>

The operators `AND` and `OR` are
commutative, that is, you can switch the left and right operands
without affecting the result. (However, it is not guaranteed that
the left operand is evaluated before the right operand. See [Section 4.2.14](../sql-syntax/sql-expressions.md#SYNTAX-EXPRESS-EVAL) for more information about the
order of evaluation of subexpressions.)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-logical.html)（英文原文，待翻譯）
