<a id="LO-FUNCS"></a>

## 33.4. 伺服器端函式 [#](#LO-FUNCS)

專為從 SQL 操作大型物件而設計的伺服器端函式，
列於[表 33.1](lo-funcs.md#LO-FUNCS-TABLE)。

<a id="LO-FUNCS-TABLE"></a>

**表 33.1. 以 SQL 操作的大型物件函式**

<table border="1" class="table" summary="SQL-Oriented Large Object Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.7.4.9.3.2.2.1.1.1.1"></a>
<code class="function">lo_from_bytea</code> ( <em class="parameter"><code>loid</code></em> <code class="type">oid</code>, <em class="parameter"><code>data</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        建立一個大型物件，並將 <em class="parameter"><code>data</code></em> 存入其中。
        若 <em class="parameter"><code>loid</code></em> 為零，系統會選擇一個
        未使用的 OID，否則就使用該 OID（若已有某個大型物件
        使用該 OID，則會發生錯誤）。成功時會傳回該大型物件的
        OID。
       </p>
<p>
<code class="literal">lo_from_bytea(0, '\xffffff00')</code>
        → <code class="returnvalue">24528</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.7.4.9.3.2.2.2.1.1.1"></a>
<code class="function">lo_put</code> ( <em class="parameter"><code>loid</code></em> <code class="type">oid</code>, <em class="parameter"><code>offset</code></em> <code class="type">bigint</code>, <em class="parameter"><code>data</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        從大型物件內給定的位移開始寫入 <em class="parameter"><code>data</code></em>；
        必要時會擴大該大型物件。
       </p>
<p>
<code class="literal">lo_put(24528, 1, '\xaa')</code>
        → <code class="returnvalue"></code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.7.4.9.3.2.2.3.1.1.1"></a>
<code class="function">lo_get</code> ( <em class="parameter"><code>loid</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>offset</code></em> <code class="type">bigint</code>, <em class="parameter"><code>length</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        擷取大型物件的內容，或其中的一段子字串。
       </p>
<p>
<code class="literal">lo_get(24528, 0, 3)</code>
        → <code class="returnvalue">\xffaaff</code>
</p></td></tr></tbody></table>

<br>

另外還有一些伺服器端函式，分別對應於先前說明的每個
用戶端函式；事實上，用戶端函式大多只是對應伺服器端函式的
介面。其中同樣適合透過 SQL 命令呼叫的有
`lo_creat`<a id="id-1.7.4.9.4.2"></a>、
`lo_create`、
`lo_unlink`<a id="id-1.7.4.9.4.5"></a>、
`lo_import`<a id="id-1.7.4.9.4.7"></a> 與
`lo_export`<a id="id-1.7.4.9.4.9"></a>。
以下是它們的使用範例：

```

CREATE TABLE image (
    name            text,
    raster          oid
);

SELECT lo_creat(-1);       -- returns OID of new, empty large object

SELECT lo_create(43213);   -- attempts to create large object with OID 43213

SELECT lo_unlink(173454);  -- deletes large object with OID 173454

INSERT INTO image (name, raster)
    VALUES ('beautiful image', lo_import('/etc/motd'));

INSERT INTO image (name, raster)  -- same as above, but specify OID to use
    VALUES ('beautiful image', lo_import('/etc/motd', 68583));

SELECT lo_export(image.raster, '/tmp/motd') FROM image
    WHERE name = 'beautiful image';
```

伺服器端的 `lo_import` 與
`lo_export` 函式，其行為與對應的用戶端函式
有相當大的差異。這兩個函式會以擁有該資料庫之使用者的權限，
讀寫伺服器檔案系統中的檔案。
因此，預設只有超級使用者可以使用它們。
相較之下，用戶端的匯入與匯出函式會以用戶端程式的權限，
讀寫用戶端檔案系統中的檔案。用戶端函式不需要任何資料庫
權限，只需要讀取或寫入相關大型物件的權限。

### 小心

可以將伺服器端 `lo_import`
與 `lo_export` 函式的使用權限 [GRANT](../../reference/sql-commands/sql-grant.md) 給
非超級使用者，但必須審慎考量其安全性影響。
擁有這類權限的惡意使用者，可以輕易地利用它們成為
超級使用者（例如藉由改寫伺服器設定檔），或者可以
攻擊伺服器檔案系統的其他部分，而根本不必取得
資料庫超級使用者權限。*因此，對於擁有
這類權限之角色的存取，必須與對超級使用者角色的存取同樣謹慎地加以防護。*
儘管如此，若某些例行工作需要使用
伺服器端的 `lo_import`
或 `lo_export`，使用擁有這類權限的角色，
會比使用擁有完整超級使用者權限的角色更安全，因為這有助於降低
意外錯誤所造成損害的風險。

`lo_read` 與
`lo_write` 的功能也可以透過伺服器端呼叫取得，
但伺服器端函式的名稱與用戶端介面不同，
其中不含底線。你必須以
`loread` 與 `lowrite` 呼叫這些函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/lo-funcs.html)（原文版本：18.6；核對日期：2026-10-18）
