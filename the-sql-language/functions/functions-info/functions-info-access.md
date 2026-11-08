# 9.27.2. 存取權限查詢函式

<a id="FUNCTIONS-INFO-ACCESS"></a>

## 9.27.2. 存取權限查詢函式 [#](#functions-info-access) <a href="#functions-info-access" id="functions-info-access"></a>

<a id="id-1.5.8.33.4.2"></a>

[表 9.72](#functions-info-access-table) 列出了能以程式方式查詢物件存取權限的函式。（關於權限的更多資訊，請參閱[第 5.8 節](../../ddl/ddl-priv.md)。）在這些函式中，要查詢其權限的使用者可以用名稱或 OID（`pg_authid`.`oid`）指定；如果名稱指定為 `public`，則會檢查 PUBLIC 虛擬角色的權限。此外，*`user`* 引數也可以完全省略，此時會假定為 `current_user`。要查詢的物件同樣可以用名稱或 OID 指定。以名稱指定時，若有需要可以包含綱要名稱。所要查詢的存取權限以文字字串指定，其值必須是該物件型別適用的權限關鍵字之一（例如 `SELECT`）。也可以選擇在權限類型後面加上 `WITH GRANT OPTION`，以測試該權限是否帶有授權選項（grant option）。此外，也可以列出以逗號分隔的多個權限類型，此時只要擁有所列權限中的任何一個，結果就為 true。（權限字串不區分大小寫，並且權限名稱之間可以有多餘的空白，但權限名稱內部不可以。）以下是一些範例：

```

SELECT has_table_privilege('myschema.mytable', 'select');
SELECT has_table_privilege('joe', 'mytable', 'INSERT, SELECT WITH GRANT OPTION');
```

<a id="FUNCTIONS-INFO-ACCESS-TABLE"></a>

### 表 9.72. 存取權限查詢函式 [#](#functions-info-access-table) <a href="#functions-info-access-table" id="functions-info-access-table"></a>

<table border="1" class="table" summary="Access Privilege Inquiry Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.1.1.1.1"></a>
<code class="function">has_any_column_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料表的任一欄位擁有權限？只要對整個資料表擁有該權限，或者至少有一個欄位被授予了該權限的欄位層級授權，就會成立。允許的權限類型為 <code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code> 與 <code class="literal">REFERENCES</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.2.1.1.1"></a> <code class="function">has_column_privilege</code> ( [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> 或 <code class="type">oid</code>, </span>] <em class="parameter"><code>table</code></em> <code class="type">text</code> 或 <code class="type">oid</code>, <em class="parameter"><code>column</code></em> <code class="type">text</code> 或 <code class="type">smallint</code>, <em class="parameter"><code>privilege</code></em> <code class="type">text</code> ) → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對指定的資料表欄位擁有權限？只要對整個資料表擁有該權限，或者該欄位被授予了該權限的欄位層級授權，就會成立。欄位可以用名稱或屬性編號（<code class="structname">pg_attribute</code>.<code class="structfield">attnum</code>）指定。允許的權限類型為 <code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code> 與 <code class="literal">REFERENCES</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.3.1.1.1"></a>
<code class="function">has_database_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>database</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料庫擁有權限？允許的權限類型為 <code class="literal">CREATE</code>、<code class="literal">CONNECT</code>、<code class="literal">TEMPORARY</code> 與 <code class="literal">TEMP</code>（等同於 <code class="literal">TEMPORARY</code>）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.4.1.1.1"></a>
<code class="function">has_foreign_data_wrapper_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>fdw</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對外部資料包裝器（foreign-data wrapper）擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.5.1.1.1"></a>
<code class="function">has_function_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>function</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對函式擁有權限？唯一允許的權限類型為 <code class="literal">EXECUTE</code>。
       </p>
<p>
        以名稱而非 OID 指定函式時，允許的輸入與 <code class="type">regprocedure</code> 資料型別相同（請參閱<a class="xref" href="../../datatype/datatype-oid.md">第 8.19 節</a>）。範例如下：
</p><pre class="programlisting">
SELECT has_function_privilege('joeuser', 'myfunc(int, text)', 'execute');
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.6.1.1.1"></a>
<code class="function">has_language_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>language</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對程序語言擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.7.1.1.1"></a>
<code class="function">has_largeobject_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>largeobject</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對大型物件擁有權限？允許的權限類型為 <code class="literal">SELECT</code> 與 <code class="literal">UPDATE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.8.1.1.1"></a>
<code class="function">has_parameter_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>parameter</code></em> <code class="type">text</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對組態參數擁有權限？參數名稱不區分大小寫。允許的權限類型為 <code class="literal">SET</code> 與 <code class="literal">ALTER SYSTEM</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.9.1.1.1"></a>
<code class="function">has_schema_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>schema</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對綱要擁有權限？允許的權限類型為 <code class="literal">CREATE</code> 與 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.10.1.1.1"></a>
<code class="function">has_sequence_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>sequence</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對序列擁有權限？允許的權限類型為 <code class="literal">USAGE</code>、<code class="literal">SELECT</code> 與 <code class="literal">UPDATE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.11.1.1.1"></a>
<code class="function">has_server_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>server</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對外部伺服器擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.12.1.1.1"></a>
<code class="function">has_table_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料表擁有權限？允許的權限類型為 <code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code>、<code class="literal">DELETE</code>、<code class="literal">TRUNCATE</code>、<code class="literal">REFERENCES</code>、<code class="literal">TRIGGER</code> 與 <code class="literal">MAINTAIN</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.13.1.1.1"></a>
<code class="function">has_tablespace_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>tablespace</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料表空間擁有權限？唯一允許的權限類型為 <code class="literal">CREATE</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.14.1.1.1"></a>
<code class="function">has_type_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>type</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對資料型別擁有權限？唯一允許的權限類型為 <code class="literal">USAGE</code>。以名稱而非 OID 指定型別時，允許的輸入與 <code class="type">regtype</code> 資料型別相同（請參閱<a class="xref" href="../../datatype/datatype-oid.md">第 8.19 節</a>）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.15.1.1.1"></a>
<code class="function">pg_has_role</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>role</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        使用者是否對角色擁有權限？允許的權限類型為 <code class="literal">MEMBER</code>、<code class="literal">USAGE</code> 與 <code class="literal">SET</code>。<code class="literal">MEMBER</code> 表示直接或間接身為該角色的成員，而不考慮可能被賦予了哪些具體權限。<code class="literal">USAGE</code> 表示是否不必執行 <code class="command">SET ROLE</code> 就能立即使用該角色的權限，而 <code class="literal">SET</code> 表示是否可以使用 <code class="literal">SET ROLE</code> 指令切換為該角色。可以在上述任何一種權限類型後面加上 <code class="literal">WITH ADMIN OPTION</code> 或 <code class="literal">WITH GRANT
        OPTION</code>，以測試是否持有 <code class="literal">ADMIN</code> 權限（這六種寫法測試的都是同一件事）。這個函式不允許將 <em class="parameter"><code>user</code></em> 設為 <code class="literal">public</code> 的特殊情況，因為 PUBLIC 虛擬角色永遠不可能是實際角色的成員。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.16.1.1.1"></a>
<code class="function">row_security_active</code> (
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        在目前使用者與目前環境的情境下，指定的資料表是否啟用了資料列層級安全性？
       </p></td></tr></tbody></table>

<br>

[表 9.73](#functions-aclitem-op-table) 列出了 `aclitem` 型別可用的運算子，該型別是存取權限在系統目錄中的表示方式。關於如何解讀存取權限值，請參閱[第 5.8 節](../../ddl/ddl-priv.md)。

<a id="FUNCTIONS-ACLITEM-OP-TABLE"></a>

### 表 9.73. `aclitem` 運算子 [#](#functions-aclitem-op-table) <a href="#functions-aclitem-op-table" id="functions-aclitem-op-table"></a>

<table border="1" class="table" summary="aclitem Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
         運算子
        </p>
<p>
         說明
        </p>
<p>
         範例
        </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.6.2.2.1.1.1.1"></a>
<code class="type">aclitem</code> <code class="literal">=</code> <code class="type">aclitem</code>
         → <code class="returnvalue">boolean</code>
</p>
<p>
         兩個 <code class="type">aclitem</code> 是否相等？（請注意，<code class="type">aclitem</code> 型別沒有一般的一整組比較運算子，只有相等比較。因此，<code class="type">aclitem</code> 陣列也只能比較是否相等。）
        </p>
<p>
<code class="literal">'calvin=r*w/hobbes'::aclitem = 'calvin=r*w*/hobbes'::aclitem</code>
         → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.6.2.2.2.1.1.1"></a>
<code class="type">aclitem[]</code> <code class="literal">@&gt;</code> <code class="type">aclitem</code>
         → <code class="returnvalue">boolean</code>
</p>
<p>
         陣列是否包含指定的權限？（如果陣列中有一個項目，其被授權者與授權者都與該 <code class="type">aclitem</code> 相符，並且至少擁有所指定的權限集合，結果即為 true。）
        </p>
<p>
<code class="literal">'{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] @&gt; 'calvin=r*/hobbes'::aclitem</code>
         → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

[表 9.74](#functions-aclitem-fn-table) 列出了一些用於管理 `aclitem` 型別的其他函式。

<a id="FUNCTIONS-ACLITEM-FN-TABLE"></a>

### 表 9.74. `aclitem` 函式 [#](#functions-aclitem-fn-table) <a href="#functions-aclitem-fn-table" id="functions-aclitem-fn-table"></a>

<table border="1" class="table" summary="aclitem Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.1.1.1.1"></a>
<code class="function">acldefault</code> (
          <em class="parameter"><code>type</code></em> <code class="type">"char"</code>,
          <em class="parameter"><code>ownerId</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">aclitem[]</code>
</p>
<p>
        建構一個 <code class="type">aclitem</code> 陣列，內容為某個型別為 <em class="parameter"><code>type</code></em> 之物件的預設存取權限，該物件屬於 OID 為 <em class="parameter"><code>ownerId</code></em> 的角色。這代表了當物件的 <acronym class="acronym">ACL</acronym> 項目為 NULL 時所假定的存取權限。（預設存取權限說明於<a class="xref" href="../../ddl/ddl-priv.md">第 5.8 節</a>。）<em class="parameter"><code>type</code></em> 參數必須是下列之一：'c' 代表 <code class="literal">COLUMN</code>，'r' 代表 <code class="literal">TABLE</code> 及類似資料表的物件，'s' 代表 <code class="literal">SEQUENCE</code>，'d' 代表 <code class="literal">DATABASE</code>，'f' 代表 <code class="literal">FUNCTION</code> 或 <code class="literal">PROCEDURE</code>，'l' 代表 <code class="literal">LANGUAGE</code>，'L' 代表 <code class="literal">LARGE OBJECT</code>，'n' 代表 <code class="literal">SCHEMA</code>，'p' 代表 <code class="literal">PARAMETER</code>，'t' 代表 <code class="literal">TABLESPACE</code>，'F' 代表 <code class="literal">FOREIGN DATA WRAPPER</code>，'S' 代表 <code class="literal">FOREIGN SERVER</code>，或 'T' 代表 <code class="literal">TYPE</code> 或 <code class="literal">DOMAIN</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.2.1.1.1"></a>
<code class="function">aclexplode</code> ( <code class="type">aclitem[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>grantor</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>grantee</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>privilege_type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>is_grantable</code></em> <code class="type">boolean</code> )
       </p>
<p>
        將 <code class="type">aclitem</code> 陣列以一組資料列的形式回傳。如果被授權者是虛擬角色 PUBLIC，則在 <em class="parameter"><code>grantee</code></em> 欄位中以零表示。每一項授予的權限都以 <code class="literal">SELECT</code>、<code class="literal">INSERT</code> 等表示（完整清單請參閱<a class="xref" href="../../ddl/ddl-priv.md#privilege-abbrevs-table">表 5.1</a>）。請注意，每一項權限都會拆成獨立的一筆資料列，因此 <em class="parameter"><code>privilege_type</code></em> 欄位中只會出現一個關鍵字。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.3.1.1.1"></a>
<code class="function">makeaclitem</code> (
          <em class="parameter"><code>grantee</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>grantor</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>privileges</code></em> <code class="type">text</code>,
          <em class="parameter"><code>is_grantable</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">aclitem</code>
</p>
<p>
        以給定的屬性建構一個 <code class="type">aclitem</code>。<em class="parameter"><code>privileges</code></em> 是以逗號分隔的權限名稱清單，例如 <code class="literal">SELECT</code>、<code class="literal">INSERT</code> 等，這些權限都會設定在結果中。（權限字串不區分大小寫，並且權限名稱之間可以有多餘的空白，但權限名稱內部不可以。）
       </p></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
