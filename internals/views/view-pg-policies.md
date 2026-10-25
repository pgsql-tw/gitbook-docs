<a id="VIEW-PG-POLICIES"></a>

## 53.15. `pg_policies` [#](#view-pg-policies) <a href="#view-pg-policies" id="view-pg-policies"></a>

<a id="id-1.10.5.19.2"></a>

檢視表 `pg_policies` 可用來存取資料庫中每個資料列層級安全性政策的實用資訊。

<a id="id-1.10.5.19.4"></a>

**表 53.15. `pg_policies` 欄位**

<table border="1" class="table" summary="表 53.15. pg_policies 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       此政策所套用之資料表所在的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       此政策所套用之資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">policyname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-policy.md"><code class="structname">pg_policy</code></a>.<code class="structfield">polname</code>）
      </p>
<p>
       政策名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">permissive</code> <code class="type">text</code>
</p>
<p>
       此政策是寬鬆型（permissive）還是限制型（restrictive）？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">roles</code> <code class="type">name[]</code>
</p>
<p>
       此政策所適用的角色
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cmd</code> <code class="type">text</code>
</p>
<p>
       此政策所套用的命令類型
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">qual</code> <code class="type">text</code>
</p>
<p>
       加入到此政策所適用查詢之安全屏障條件中的運算式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">with_check</code> <code class="type">text</code>
</p>
<p>
       加入到嘗試將資料列新增至此資料表之查詢的 WITH CHECK 條件中的運算式
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-policies.html)（原文版本：18.6；核對日期：2026-10-10）
