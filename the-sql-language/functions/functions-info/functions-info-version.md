# 9.27.11. 版本資訊函式

<a id="FUNCTIONS-INFO-VERSION"></a>

## 9.27.11. 版本資訊函式 [#](#functions-info-version) <a href="#functions-info-version" id="functions-info-version"></a>

[表 9.93](#functions-version) 所列的函式會輸出版本資訊。

<a id="FUNCTIONS-VERSION"></a>

### 表 9.93. 版本資訊函式 [#](#functions-version) <a href="#functions-version" id="functions-version"></a>

<table border="1" class="table" summary="Version Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.1.1.1.1"></a>
<code class="function">version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳描述 <span class="productname">PostgreSQL</span> 伺服器版本的字串。你也可以從 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-preset.md#GUC-SERVER-VERSION">server_version</a> 取得這項資訊；若需要機器可讀的版本，則可以使用 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-preset.md#GUC-SERVER-VERSION-NUM">server_version_num</a>。軟體開發人員應該使用 <code class="varname">server_version_num</code>（自 8.2 版起提供）或 <a class="xref" href="../../../client-interfaces/libpq/libpq-status.md#libpq-pqserverversion"><code class="function">PQserverVersion</code></a>，而不是剖析文字形式的版本。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.2.1.1.1"></a>
<code class="function">unicode_version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳代表 <span class="productname">PostgreSQL</span> 所使用之 Unicode 版本的字串。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.3.1.1.1"></a>
<code class="function">icu_unicode_version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        如果伺服器建置時加入了 ICU 支援，則回傳代表 ICU 所使用之 Unicode 版本的字串；否則回傳 <code class="literal">NULL</code> </p></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
