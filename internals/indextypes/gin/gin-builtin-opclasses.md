# 65.4.2. 內建運算子類別

<a id="GIN-BUILTIN-OPCLASSES"></a>

## 65.4.2. 內建運算子類別 [#](#gin-builtin-opclasses) <a href="#gin-builtin-opclasses" id="gin-builtin-opclasses"></a>

PostgreSQL 核心發行版本包含[表 65.3](#gin-builtin-opclasses-table) 所列的 GIN 運算子類別。（[附錄 F](../../../appendixes/contrib/README.md) 中所述的部分選用模組提供了額外的 GIN 運算子類別。）

<a id="GIN-BUILTIN-OPCLASSES-TABLE"></a>

### 表 65.3. 內建 GIN 運算子類別 [#](#gin-builtin-opclasses-table) <a href="#gin-builtin-opclasses-table" id="gin-builtin-opclasses-table"></a>

<table border="1" class="table" summary="內建 GIN 運算子類別"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>可索引運算子</th></tr></thead><tbody><tr><td rowspan="4" valign="middle"><code class="literal">array_ops</code></td><td><code class="literal">&amp;&amp; (anyarray,anyarray)</code></td></tr><tr><td><code class="literal">@&gt; (anyarray,anyarray)</code></td></tr><tr><td><code class="literal">&lt;@ (anyarray,anyarray)</code></td></tr><tr><td><code class="literal">= (anyarray,anyarray)</code></td></tr><tr><td rowspan="6" valign="middle"><code class="literal">jsonb_ops</code></td><td><code class="literal">@&gt; (jsonb,jsonb)</code></td></tr><tr><td><code class="literal">@? (jsonb,jsonpath)</code></td></tr><tr><td><code class="literal">@@ (jsonb,jsonpath)</code></td></tr><tr><td><code class="literal">? (jsonb,text)</code></td></tr><tr><td><code class="literal">?| (jsonb,text[])</code></td></tr><tr><td><code class="literal">?&amp; (jsonb,text[])</code></td></tr><tr><td rowspan="3" valign="middle"><code class="literal">jsonb_path_ops</code></td><td><code class="literal">@&gt; (jsonb,jsonb)</code></td></tr><tr><td><code class="literal">@? (jsonb,jsonpath)</code></td></tr><tr><td><code class="literal">@@ (jsonb,jsonpath)</code></td></tr><tr><td valign="middle"><code class="literal">tsvector_ops</code></td><td><code class="literal">@@ (tsvector,tsquery)</code></td></tr></tbody></table>

<br>

在 `jsonb` 型別的兩個運算子類別中，`jsonb_ops` 是預設的。`jsonb_path_ops` 支援的運算子較少，但對這些運算子提供較佳的效能。詳細資訊請參閱[第 8.14.4 節](../../../the-sql-language/datatype/datatype-json.md#json-indexing)。

[返回 65.4. GIN 索引](../gin.md#gin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/gin.html)（原文版本：18.6；核對日期：2026-10-17）
