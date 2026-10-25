<a id="CATALOG-PG-AMOP"></a>

## 52.4. `pg_amop` [#](#catalog-pg-amop) <a href="#catalog-pg-amop" id="catalog-pg-amop"></a>

<a id="id-1.10.4.6.2"></a>

系統目錄 `pg_amop` 存放與存取方法運算子家族相關聯之運算子的資訊。
每個身為運算子家族成員的運算子各有一筆資料列。家族成員可以是*搜尋*運算子，
也可以是*排序*運算子。一個運算子
可以出現在超過一個家族中，但在同一個家族內，既不能出現在超過一個搜尋位置，
也不能出現在超過一個排序位置。
（允許一個運算子同時用於搜尋與排序兩種用途，雖然這種情況不太可能出現。）

<a id="id-1.10.4.6.4"></a>

**表 52.4. `pg_amop` 欄位**

<table border="1" class="table" summary="表 52.4. pg_amop 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amopfamily</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此項目所屬的運算子家族
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amoplefttype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       運算子的左側輸入資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amoprighttype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       運算子的右側輸入資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amopstrategy</code> <code class="type">int2</code>
</p>
<p>
       運算子策略編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amoppurpose</code> <code class="type">char</code>
</p>
<p>
       運算子用途，<code class="literal">s</code> 表示搜尋，
       <code class="literal">o</code> 表示排序
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amopopr</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       運算子的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amopmethod</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子家族所屬的索引存取方法
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amopsortfamily</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若為排序運算子，則為此項目排序所依據的 B-tree 運算子家族；
       若為搜尋運算子則為零
      </p></td></tr></tbody></table>

<br>

「搜尋」運算子項目表示，可以搜尋此運算子家族的索引，以找出所有滿足
`WHERE`
*`indexed_column`*
*`operator`*
*`constant`*
的資料列。
顯然，這樣的運算子必須傳回 `boolean`，且其左側輸入
型別必須與索引欄位的資料型別相符。

「排序」運算子項目表示，可以掃描此運算子家族的索引，以依照
`ORDER BY`
*`indexed_column`*
*`operator`*
*`constant`*
所表示的順序傳回資料列。
這樣的運算子可以傳回任何可排序的資料型別，不過同樣地，
其左側輸入型別必須與索引欄位的資料型別相符。
`ORDER BY` 的確切語意由
`amopsortfamily` 欄位指定，該欄位必須參照
適用於該運算子結果型別的 B-tree 運算子家族。

### 注意

目前假設排序運算子的排序順序就是所參照運算子家族的預設順序，也就是 `ASC NULLS
LAST`。日後可能會藉由新增額外欄位來明確指定排序選項，以放寬此限制。

項目的 `amopmethod` 必須與其所屬運算子家族的
`opfmethod` 相符（在此包含 `amopmethod`，是基於效能考量而刻意對
系統目錄結構所做的反正規化）。此外，
`amoplefttype` 與 `amoprighttype` 必須與
所參照之 [`pg_operator`](catalog-pg-operator.md) 項目的
`oprleft` 與 `oprright` 欄位相符。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-amop.html)（原文版本：18.6；核對日期：2026-10-17）
