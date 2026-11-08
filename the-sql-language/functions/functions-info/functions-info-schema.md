# 9.27.3. 綱要可見性查詢函式

<a id="FUNCTIONS-INFO-SCHEMA"></a>

## 9.27.3. 綱要可見性查詢函式 [#](#functions-info-schema) <a href="#functions-info-schema" id="functions-info-schema"></a>

[表 9.75](#functions-info-schema-table) 列出了用來判斷某個物件在目前的綱要搜尋路徑中是否*可見*的函式。舉例來說，如果一個資料表所屬的綱要位於搜尋路徑中，並且搜尋路徑中較前面的位置沒有同名的資料表，就稱該資料表是可見的。這等同於說，該資料表可以只用名稱來引用，而不需明確的綱要限定。因此，要列出所有可見資料表的名稱：

```

SELECT relname FROM pg_class WHERE pg_table_is_visible(oid);
```

對於函式與運算子而言，如果搜尋路徑中較前面的位置沒有名稱*與引數資料型別*都相同的物件，就稱搜尋路徑中的該物件是可見的。對於運算子類別與運算子家族，則會同時考慮名稱與相關聯的索引存取方法。

<a id="id-1.5.8.33.5.3"></a><a id="FUNCTIONS-INFO-SCHEMA-TABLE"></a>

### 表 9.75. 綱要可見性查詢函式 [#](#functions-info-schema-table) <a href="#functions-info-schema-table" id="functions-info-schema-table"></a>

<table border="1" class="table" summary="Schema Visibility Inquiry Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.1.1.1.1"></a>
<code class="function">pg_collation_is_visible</code> ( <em class="parameter"><code>collation</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        定序在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.2.1.1.1"></a>
<code class="function">pg_conversion_is_visible</code> ( <em class="parameter"><code>conversion</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        編碼轉換（conversion）在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.3.1.1.1"></a>
<code class="function">pg_function_is_visible</code> ( <em class="parameter"><code>function</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        函式在搜尋路徑中是否可見？（這也適用於程序與彙總函式。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.4.1.1.1"></a>
<code class="function">pg_opclass_is_visible</code> ( <em class="parameter"><code>opclass</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        運算子類別在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.5.1.1.1"></a>
<code class="function">pg_operator_is_visible</code> ( <em class="parameter"><code>operator</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        運算子在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.6.1.1.1"></a>
<code class="function">pg_opfamily_is_visible</code> ( <em class="parameter"><code>opclass</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        運算子家族在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.7.1.1.1"></a>
<code class="function">pg_statistics_obj_is_visible</code> ( <em class="parameter"><code>stat</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        統計資訊物件在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.8.1.1.1"></a>
<code class="function">pg_table_is_visible</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        資料表在搜尋路徑中是否可見？（這適用於所有種類的關聯，包括檢視表、具體化檢視表、索引、序列與外部資料表。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.9.1.1.1"></a>
<code class="function">pg_ts_config_is_visible</code> ( <em class="parameter"><code>config</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索設定在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.10.1.1.1"></a>
<code class="function">pg_ts_dict_is_visible</code> ( <em class="parameter"><code>dict</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索字典在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.11.1.1.1"></a>
<code class="function">pg_ts_parser_is_visible</code> ( <em class="parameter"><code>parser</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索剖析器在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.12.1.1.1"></a>
<code class="function">pg_ts_template_is_visible</code> ( <em class="parameter"><code>template</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        全文檢索範本在搜尋路徑中是否可見？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.13.1.1.1"></a>
<code class="function">pg_type_is_visible</code> ( <em class="parameter"><code>type</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        型別（或值域）在搜尋路徑中是否可見？
       </p></td></tr></tbody></table>

<br>

這些函式全都需要以物件 OID 來識別要檢查的物件。如果你想以名稱來測試物件，使用 OID 別名型別（`regclass`、`regtype`、`regprocedure`、`regoperator`、`regconfig` 或 `regdictionary`）會很方便，例如：

```

SELECT pg_type_is_visible('myschema.widget'::regtype);
```

請注意，以這種方式測試未經綱要限定的型別名稱並沒有太大意義——如果這個名稱能夠被辨識，它就必定是可見的。

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
