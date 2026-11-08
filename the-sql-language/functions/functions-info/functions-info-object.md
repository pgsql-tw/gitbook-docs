# 9.27.5. 物件資訊與定址函式

<a id="FUNCTIONS-INFO-OBJECT"></a>

## 9.27.5. 物件資訊與定址函式 [#](#functions-info-object) <a href="#functions-info-object" id="functions-info-object"></a>

[表 9.81](#functions-info-object-table) 列出了與資料庫物件識別及定址相關的函式。

<a id="FUNCTIONS-INFO-OBJECT-TABLE"></a>

### 表 9.81. 物件資訊與定址函式 [#](#functions-info-object-table) <a href="#functions-info-object-table" id="functions-info-object-table"></a>

<table border="1" class="table" summary="Object Information and Addressing Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.1.1.1.1"></a>
<code class="function">pg_get_acl</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">aclitem[]</code>
</p>
<p>
        回傳以系統目錄 OID、物件 OID 與子物件 ID 指定之資料庫物件的 <acronym class="acronym">ACL</acronym>。對於未定義的物件，這個函式會回傳 <code class="literal">NULL</code> 值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.2.1.1.1"></a>
<code class="function">pg_describe_object</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳以系統目錄 OID、物件 OID 與子物件 ID（例如資料表中的欄位編號；指的是整個物件時，子物件 ID 為零）所識別之資料庫物件的文字描述。這個描述旨在供人閱讀，並且可能會依伺服器的設定而經過翻譯。這特別有助於確認 <code class="structname">pg_depend</code> 系統目錄中所參照之物件的身分。對於未定義的物件，這個函式會回傳 <code class="literal">NULL</code> 值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.3.1.1.1"></a>
<code class="function">pg_identify_object</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>schema</code></em> <code class="type">text</code>,
        <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>identity</code></em> <code class="type">text</code> )
       </p>
<p>
        回傳一筆資料列，其中包含足以唯一識別以系統目錄 OID、物件 OID 與子物件 ID 所指定之資料庫物件的資訊。這些資訊是供機器讀取的，永遠不會被翻譯。<em class="parameter"><code>type</code></em> 識別資料庫物件的類型；<em class="parameter"><code>schema</code></em> 是該物件所屬的綱要名稱，對於不屬於綱要的物件類型則為 <code class="literal">NULL</code>；<em class="parameter"><code>name</code></em> 是物件的名稱（必要時會加上引號），前提是該名稱（在適用時連同綱要名稱）足以唯一識別該物件，否則為 <code class="literal">NULL</code>；<em class="parameter"><code>identity</code></em> 是完整的物件識別，其精確格式取決於物件類型，且格式中的每個名稱都會視需要加上綱要限定與引號。未定義的物件會以 <code class="literal">NULL</code> 值識別。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.4.1.1.1"></a>
<code class="function">pg_identify_object_as_address</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>object_names</code></em> <code class="type">text[]</code>,
        <em class="parameter"><code>object_args</code></em> <code class="type">text[]</code> )
       </p>
<p>
        回傳一筆資料列，其中包含足以唯一識別以系統目錄 OID、物件 OID 與子物件 ID 所指定之資料庫物件的資訊。所回傳的資訊與目前的伺服器無關，也就是說，它可以用來識別另一台伺服器中同名的物件。<em class="parameter"><code>type</code></em> 識別資料庫物件的類型；<em class="parameter"><code>object_names</code></em> 與 <em class="parameter"><code>object_args</code></em> 是文字陣列，兩者共同構成對該物件的參照。這三個值可以傳給 <code class="function">pg_get_object_address</code>，以取得該物件的內部位址。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.5.1.1.1"></a>
<code class="function">pg_get_object_address</code> ( <em class="parameter"><code>type</code></em> <code class="type">text</code>, <em class="parameter"><code>object_names</code></em> <code class="type">text[]</code>, <em class="parameter"><code>object_args</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>objid</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
       </p>
<p>
        回傳一筆資料列，其中包含足以唯一識別以類型代碼、物件名稱與引數陣列所指定之資料庫物件的資訊。所回傳的值就是像 <code class="structname">pg_depend</code> 這類系統目錄中會使用的值；它們可以傳給其他系統函式，例如 <code class="function">pg_describe_object</code> 或 <code class="function">pg_identify_object</code>。<em class="parameter"><code>classid</code></em> 是包含該物件之系統目錄的 OID；<em class="parameter"><code>objid</code></em> 是物件本身的 OID，而 <em class="parameter"><code>objsubid</code></em> 是子物件 ID，若無則為零。這個函式是 <code class="function">pg_identify_object_as_address</code> 的反函式。未定義的物件會以 <code class="literal">NULL</code> 值識別。
       </p></td></tr></tbody></table>

<br>

`pg_get_acl` 可用於擷取並檢視與資料庫物件相關聯的權限，而不必去查看特定的系統目錄。例如，要擷取目前資料庫中所有物件上已授予的權限：

```

postgres=# SELECT
    (pg_identify_object(s.classid,s.objid,s.objsubid)).*,
    pg_catalog.pg_get_acl(s.classid,s.objid,s.objsubid) AS acl
FROM pg_catalog.pg_shdepend AS s
JOIN pg_catalog.pg_database AS d
    ON d.datname = current_database() AND
       d.oid = s.dbid
JOIN pg_catalog.pg_authid AS a
    ON a.oid = s.refobjid AND
       s.refclassid = 'pg_authid'::regclass
WHERE s.deptype = 'a';
-[ RECORD 1 ]-----------------------------------------
type     | table
schema   | public
name     | testtab
identity | public.testtab
acl      | {postgres=arwdDxtm/postgres,foo=r/postgres}
```

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
