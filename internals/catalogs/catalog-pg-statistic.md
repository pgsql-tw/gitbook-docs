<a id="CATALOG-PG-STATISTIC"></a>

## 52.51. `pg_statistic` [#](#catalog-pg-statistic) <a href="#catalog-pg-statistic" id="catalog-pg-statistic"></a>

<a id="id-1.10.4.53.2"></a>

目錄 `pg_statistic` 儲存關於資料庫內容的統計資料。項目由 [`ANALYZE`](../../reference/sql-commands/sql-analyze.md) 建立，之後供查詢規劃器使用。請注意，即使假設統計資料是最新的，所有統計資料本質上都只是近似值。

通常，每個已分析過的資料表欄位都有一個 `stainherit` = `false` 的項目。若該資料表有繼承子資料表或分割區，還會另外建立第二個 `stainherit` = `true` 的項目。這個資料列代表該欄位在整個繼承樹上的統計資訊，也就是你用 `SELECT column FROM table*` 所看到之資料的統計資訊；而 `stainherit` = `false` 的資料列代表的則是 `SELECT column FROM ONLY table` 的結果。

`pg_statistic` 也儲存關於索引運算式之值的統計資料。這些資料的描述方式就如同它們是實際的資料欄位一樣；特別是，`starelid` 參照的是該索引。不過，一般的非運算式索引欄位不會建立項目，因為它會與底層資料表欄位的項目重複。目前，索引運算式的項目一律是 `stainherit` = `false`。

由於不同種類的資料可能適合不同種類的統計資訊，`pg_statistic` 在設計上不對它所儲存的統計資訊種類做太多假設。只有極為通用的統計資訊（例如是否為 null 的情形）才在 `pg_statistic` 中擁有專屬欄位。其他所有內容都儲存在「槽」（slot）中；槽是一組相關聯的欄位，其內容由該槽某一個欄位中的代碼編號來識別。詳細資訊請參閱 `src/include/catalog/pg_statistic.h`。

`pg_statistic` 不應讓所有人（public）都能讀取，因為即使只是資料表內容的統計資訊，也可能被視為敏感資訊。（例如：薪資欄位的最小值與最大值可能相當引人關注。）[`pg_stats`](../views/view-pg-stats.md) 是建立在 `pg_statistic` 之上、可公開讀取的檢視表，它只公開目前使用者可讀取之資料表的相關資訊。

<a id="id-1.10.4.53.8"></a>

**表 52.51. `pg_statistic` 欄位**

<table border="1" class="table" summary="表 52.51. pg_statistic 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">starelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       所描述欄位所屬的資料表或索引
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">staattnum</code> <code class="type">int2</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       所描述欄位的編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stainherit</code> <code class="type">bool</code>
</p>
<p>
       若為真，統計資訊包含子資料表中的值，而不只是指定關聯中的值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stanullfrac</code> <code class="type">float4</code>
</p>
<p>
       欄位項目中為 null 的比例
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stawidth</code> <code class="type">int4</code>
</p>
<p>
       非 null 項目的平均儲存寬度，以位元組為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stadistinct</code> <code class="type">float4</code>
</p>
<p>
       欄位中相異非 null 資料值的數目。
       大於零的值就是相異值的實際數目。
       小於零的值則是資料表資料列數之乘數的負值；例如，若某欄位約 80% 的值為非 null，
       且每個非 null 值平均約出現兩次，就可以表示為 <code class="structfield">stadistinct</code> = -0.4。
       值為零表示相異值的數目未知。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stakind<em class="replaceable"><code>N</code></em></code> <code class="type">int2</code>
</p>
<p>
       代碼編號，指出儲存在第 <em class="replaceable"><code>N</code></em> 個<span class="quote">“<span class="quote">槽</span>”</span>中的統計資訊種類
       （該槽位於 <code class="structname">pg_statistic</code> 資料列中）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">staop<em class="replaceable"><code>N</code></em></code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       用來推導儲存在第 <em class="replaceable"><code>N</code></em> 個<span class="quote">“<span class="quote">槽</span>”</span>中之統計資訊的運算子。例如，
       直方圖槽會顯示定義資料排序順序的 <code class="literal">&lt;</code> 運算子。
       若該統計資訊種類不需要運算子，則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stacoll<em class="replaceable"><code>N</code></em></code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       用來推導儲存在第 <em class="replaceable"><code>N</code></em> 個<span class="quote">“<span class="quote">槽</span>”</span>中之統計資訊的定序。例如，
       可定序欄位的直方圖槽會顯示定義資料排序順序的定序。不可定序的資料則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stanumbers<em class="replaceable"><code>N</code></em></code> <code class="type">float4[]</code>
</p>
<p>
       適合第 <em class="replaceable"><code>N</code></em> 個<span class="quote">“<span class="quote">槽</span>”</span>之種類的數值統計資訊；
       若該槽的種類不涉及數值，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stavalues<em class="replaceable"><code>N</code></em></code> <code class="type">anyarray</code>
</p>
<p>
       適合第 <em class="replaceable"><code>N</code></em> 個<span class="quote">“<span class="quote">槽</span>”</span>之種類的欄位資料值；
       若該槽的種類不儲存任何資料值，則為 null。每個陣列的元素值實際上
       屬於該特定欄位的資料型別，或相關的型別（例如陣列的元素型別），因此無法
       比 <code class="type">anyarray</code> 更具體地定義這些欄位的型別。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-statistic.html)（原文版本：18.6；核對日期：2026-10-17）
