<a id="CATALOG-PG-LANGUAGE"></a>

## 52.29. `pg_language` [#](#CATALOG-PG-LANGUAGE)

<a id="id-1.10.4.31.2"></a>

目錄 `pg_language` 登錄可用來撰寫函式或預存程序的語言。關於語言處理常式的更多資訊，請參閱 [CREATE LANGUAGE](../../reference/sql-commands/sql-createlanguage.md) 與[第 40 章](../../server-programming/xplang/README.md)。

<a id="id-1.10.4.31.4"></a>

**表 52.29. `pg_language` 欄位**

<table border="1" class="table" summary="表 52.29. pg_language 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">lanname</code> <code class="type">name</code>
</p>
<p>
       語言的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lanowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       語言的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lanispl</code> <code class="type">bool</code>
</p>
<p>
       內部語言（例如 <acronym class="acronym">SQL</acronym>）此值為 false，使用者自訂的語言則為 true。目前 <span class="application">pg_dump</span> 仍使用此欄位來判斷哪些語言需要傾印，但未來可能會改由其他機制取代。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lanpltrusted</code> <code class="type">bool</code>
</p>
<p>
       若這是受信任的語言則為 true，這表示一般認為它不會授予對正常 SQL 執行環境以外任何事物的存取權。只有超級使用者可以用不受信任的語言建立函式。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lanplcallfoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對於非內部語言，此欄位參照語言處理常式；語言處理常式是一個特殊函式，負責執行以該特定語言撰寫的所有函式。內部語言此值為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">laninline</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此欄位參照一個函式，負責執行<span class="quote">“<span class="quote">行內</span>”</span>匿名程式碼區塊（<a class="xref" href="../../reference/sql-commands/sql-do.md"><span class="refentrytitle">DO</span></a> 區塊）。若不支援行內區塊則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lanvalidator</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此欄位參照語言驗證函式，負責在新函式建立時檢查其語法與有效性。若未提供驗證函式則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lanacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-language.html)（原文版本：18.6；核對日期：2026-10-17）
