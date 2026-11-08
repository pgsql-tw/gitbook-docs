# 9.27.6. 註解資訊函式

<a id="FUNCTIONS-INFO-COMMENT"></a>

## 9.27.6. 註解資訊函式 [#](#functions-info-comment) <a href="#functions-info-comment" id="functions-info-comment"></a>

<a id="id-1.5.8.33.8.2"></a>

[表 9.82](#functions-info-comment-table) 所列的函式會擷取先前以 [COMMENT](../../../reference/sql-commands/sql-comment.md) 指令儲存的註解。如果找不到符合指定參數的註解，則回傳 NULL 值。

<a id="FUNCTIONS-INFO-COMMENT-TABLE"></a>

### 表 9.82. 註解資訊函式 [#](#functions-info-comment-table) <a href="#functions-info-comment-table" id="functions-info-comment-table"></a>

<table border="1" class="table" summary="Comment Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.1.1.1.1"></a>
<code class="function">col_description</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code>, <em class="parameter"><code>column</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳資料表欄位的註解，該欄位以其所屬資料表的 OID 與欄位編號指定。（<code class="function">obj_description</code> 無法用於資料表欄位，因為欄位沒有自己的 OID。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.2.1.1.1"></a>
<code class="function">obj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code>, <em class="parameter"><code>catalog</code></em> <code class="type">name</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳以 OID 與所在系統目錄名稱指定之資料庫物件的註解。例如，<code class="literal">obj_description(123456, 'pg_class')</code> 會擷取 OID 為 123456 之資料表的註解。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">obj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳僅以 OID 指定之資料庫物件的註解。這種用法<span class="emphasis"><em>已棄用</em></span>，因為無法保證 OID 在不同的系統目錄之間是唯一的；因此，可能會回傳錯誤的註解。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.4.1.1.1"></a>
<code class="function">shobj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code>, <em class="parameter"><code>catalog</code></em> <code class="type">name</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳以 OID 與所在系統目錄名稱指定之共享資料庫物件的註解。這與 <code class="function">obj_description</code> 相同，只不過它是用來擷取共享物件（也就是資料庫、角色與資料表空間）的註解。有些系統目錄對每個叢集中的所有資料庫而言是全域的，而其中物件的描述也同樣以全域方式儲存。
       </p></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
