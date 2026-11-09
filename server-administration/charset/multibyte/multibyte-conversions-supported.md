# 23.3.4. 可用的字元集轉換

<a id="MULTIBYTE-CONVERSIONS-SUPPORTED"></a>

## 23.3.4. 可用的字元集轉換 [#](#multibyte-conversions-supported) <a href="#multibyte-conversions-supported" id="multibyte-conversions-supported"></a>

只要轉換函式列於
[`pg_conversion`](../../../internals/catalogs/catalog-pg-conversion.md)
系統目錄中，PostgreSQL 就允許在任意
兩種字元集之間進行轉換。PostgreSQL
內建了一些預先定義的轉換，摘要列於
[表 23.4](#multibyte-translation-table)，並在
[表 23.5](#builtin-conversions-table) 中有更詳細的說明。你可以使用 SQL 指令
[CREATE CONVERSION](../../../reference/sql-commands/sql-createconversion.md) 建立新的轉換。（若要用於自動的
用戶端／伺服器轉換，該轉換必須被標記
為其字元集配對的「default（預設）」。）

<a id="MULTIBYTE-TRANSLATION-TABLE"></a>

### 表 23.4. 內建的用戶端／伺服器字元集轉換 [#](#multibyte-translation-table) <a href="#multibyte-translation-table" id="multibyte-translation-table"></a>

<table border="1" class="table" summary="內建的用戶端／伺服器字元集轉換"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>伺服器字元集</th><th>可用的用戶端字元集</th></tr></thead><tbody><tr><td><code class="literal">BIG5</code></td><td><span class="emphasis"><em>不支援作為伺服器端編碼</em></span>
</td></tr><tr><td><code class="literal">EUC_CN</code></td><td><span class="emphasis"><em>EUC_CN</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_JP</code></td><td><span class="emphasis"><em>EUC_JP</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">SJIS</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_JIS_2004</code></td><td><span class="emphasis"><em>EUC_JIS_2004</em></span>,
        <code class="literal">SHIFT_JIS_2004</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_KR</code></td><td><span class="emphasis"><em>EUC_KR</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_TW</code></td><td><span class="emphasis"><em>EUC_TW</em></span>,
        <code class="literal">BIG5</code>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">GB18030</code></td><td><span class="emphasis"><em>不支援作為伺服器端編碼</em></span>
</td></tr><tr><td><code class="literal">GBK</code></td><td><span class="emphasis"><em>不支援作為伺服器端編碼</em></span>
</td></tr><tr><td><code class="literal">ISO_8859_5</code></td><td><span class="emphasis"><em>ISO_8859_5</em></span>,
        <code class="literal">KOI8R</code>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>,
        <code class="literal">WIN866</code>,
        <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">ISO_8859_6</code></td><td><span class="emphasis"><em>ISO_8859_6</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">ISO_8859_7</code></td><td><span class="emphasis"><em>ISO_8859_7</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">ISO_8859_8</code></td><td><span class="emphasis"><em>ISO_8859_8</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">JOHAB</code></td><td><span class="emphasis"><em>不支援作為伺服器端編碼</em></span>
</td></tr><tr><td><code class="literal">KOI8R</code></td><td><span class="emphasis"><em>KOI8R</em></span>,
        <code class="literal">ISO_8859_5</code>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>,
        <code class="literal">WIN866</code>,
        <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">KOI8U</code></td><td><span class="emphasis"><em>KOI8U</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN1</code></td><td><span class="emphasis"><em>LATIN1</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN2</code></td><td><span class="emphasis"><em>LATIN2</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>,
        <code class="literal">WIN1250</code>
</td></tr><tr><td><code class="literal">LATIN3</code></td><td><span class="emphasis"><em>LATIN3</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN4</code></td><td><span class="emphasis"><em>LATIN4</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN5</code></td><td><span class="emphasis"><em>LATIN5</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN6</code></td><td><span class="emphasis"><em>LATIN6</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN7</code></td><td><span class="emphasis"><em>LATIN7</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN8</code></td><td><span class="emphasis"><em>LATIN8</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN9</code></td><td><span class="emphasis"><em>LATIN9</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN10</code></td><td><span class="emphasis"><em>LATIN10</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">MULE_INTERNAL</code></td><td><span class="emphasis"><em>MULE_INTERNAL</em></span>,
         <code class="literal">BIG5</code>,
         <code class="literal">EUC_CN</code>,
         <code class="literal">EUC_JP</code>,
         <code class="literal">EUC_KR</code>,
         <code class="literal">EUC_TW</code>,
         <code class="literal">ISO_8859_5</code>,
         <code class="literal">KOI8R</code>,
         <code class="literal">LATIN1</code> 至 <code class="literal">LATIN4</code>,
         <code class="literal">SJIS</code>,
         <code class="literal">WIN866</code>,
         <code class="literal">WIN1250</code>,
         <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">SJIS</code></td><td><span class="emphasis"><em>不支援作為伺服器端編碼</em></span>
</td></tr><tr><td><code class="literal">SHIFT_JIS_2004</code></td><td><span class="emphasis"><em>不支援作為伺服器端編碼</em></span>
</td></tr><tr><td><code class="literal">SQL_ASCII</code></td><td><span class="emphasis"><em>任何編碼（不會進行轉換）</em></span>
</td></tr><tr><td><code class="literal">UHC</code></td><td><span class="emphasis"><em>不支援作為伺服器端編碼</em></span>
</td></tr><tr><td><code class="literal">UTF8</code></td><td><span class="emphasis"><em>所有支援的編碼</em></span>
</td></tr><tr><td><code class="literal">WIN866</code></td><td><span class="emphasis"><em>WIN866</em></span>,
         <code class="literal">ISO_8859_5</code>,
         <code class="literal">KOI8R</code>,
         <code class="literal">MULE_INTERNAL</code>,
         <code class="literal">UTF8</code>,
         <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">WIN874</code></td><td><span class="emphasis"><em>WIN874</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1250</code></td><td><span class="emphasis"><em>WIN1250</em></span>,
         <code class="literal">LATIN2</code>,
         <code class="literal">MULE_INTERNAL</code>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1251</code></td><td><span class="emphasis"><em>WIN1251</em></span>,
         <code class="literal">ISO_8859_5</code>,
         <code class="literal">KOI8R</code>,
         <code class="literal">MULE_INTERNAL</code>,
         <code class="literal">UTF8</code>,
         <code class="literal">WIN866</code>
</td></tr><tr><td><code class="literal">WIN1252</code></td><td><span class="emphasis"><em>WIN1252</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1253</code></td><td><span class="emphasis"><em>WIN1253</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1254</code></td><td><span class="emphasis"><em>WIN1254</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1255</code></td><td><span class="emphasis"><em>WIN1255</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1256</code></td><td><span class="emphasis"><em>WIN1256</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1257</code></td><td><span class="emphasis"><em>WIN1257</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1258</code></td><td><span class="emphasis"><em>WIN1258</em></span>,
        <code class="literal">UTF8</code>
</td></tr></tbody></table>

<br class="table-break" />

<a id="BUILTIN-CONVERSIONS-TABLE"></a>

### 表 23.5. 所有內建的字元集轉換 [#](#builtin-conversions-table) <a href="#builtin-conversions-table" id="builtin-conversions-table"></a>

<table border="1" class="table" summary="所有內建的字元集轉換"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>轉換名稱
         <a class="footnote" href="#ftn.id-1.6.10.5.8.4.2.4.1.1.1"><sup class="footnote" id="id-1.6.10.5.8.4.2.4.1.1.1">[a]</sup></a>
</th><th>來源編碼</th><th>目的編碼</th></tr></thead><tbody><tr><td><code class="literal">big5_to_euc_tw</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">big5_to_mic</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">big5_to_utf8</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_cn_to_mic</code></td><td><code class="literal">EUC_CN</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_cn_to_utf8</code></td><td><code class="literal">EUC_CN</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_jp_to_mic</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_jp_to_sjis</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">euc_jp_to_utf8</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_kr_to_mic</code></td><td><code class="literal">EUC_KR</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_kr_to_utf8</code></td><td><code class="literal">EUC_KR</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_tw_to_big5</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">euc_tw_to_mic</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_tw_to_utf8</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">gb18030_to_utf8</code></td><td><code class="literal">GB18030</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">gbk_to_utf8</code></td><td><code class="literal">GBK</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_10_to_utf8</code></td><td><code class="literal">LATIN6</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_13_to_utf8</code></td><td><code class="literal">LATIN7</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_14_to_utf8</code></td><td><code class="literal">LATIN8</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_15_to_utf8</code></td><td><code class="literal">LATIN9</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_16_to_utf8</code></td><td><code class="literal">LATIN10</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_1_to_mic</code></td><td><code class="literal">LATIN1</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_1_to_utf8</code></td><td><code class="literal">LATIN1</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_2_to_mic</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_2_to_utf8</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_2_to_windows_1250</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">iso_8859_3_to_mic</code></td><td><code class="literal">LATIN3</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_3_to_utf8</code></td><td><code class="literal">LATIN3</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_4_to_mic</code></td><td><code class="literal">LATIN4</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_4_to_utf8</code></td><td><code class="literal">LATIN4</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_5_to_koi8_r</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">iso_8859_5_to_mic</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_5_to_utf8</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_5_to_windows_1251</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">iso_8859_5_to_windows_866</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">iso_8859_6_to_utf8</code></td><td><code class="literal">ISO_8859_6</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_7_to_utf8</code></td><td><code class="literal">ISO_8859_7</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_8_to_utf8</code></td><td><code class="literal">ISO_8859_8</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_9_to_utf8</code></td><td><code class="literal">LATIN5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">johab_to_utf8</code></td><td><code class="literal">JOHAB</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">koi8_r_to_iso_8859_5</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">koi8_r_to_mic</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">koi8_r_to_utf8</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">koi8_r_to_windows_1251</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">koi8_r_to_windows_866</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">koi8_u_to_utf8</code></td><td><code class="literal">KOI8U</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">mic_to_big5</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">mic_to_euc_cn</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_CN</code></td></tr><tr><td><code class="literal">mic_to_euc_jp</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">mic_to_euc_kr</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_KR</code></td></tr><tr><td><code class="literal">mic_to_euc_tw</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_1</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN1</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_2</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_3</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN3</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_4</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN4</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_5</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">mic_to_koi8_r</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">mic_to_sjis</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">mic_to_windows_1250</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">mic_to_windows_1251</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">mic_to_windows_866</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">sjis_to_euc_jp</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">sjis_to_mic</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">sjis_to_utf8</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1258_to_utf8</code></td><td><code class="literal">WIN1258</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">uhc_to_utf8</code></td><td><code class="literal">UHC</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_big5</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">utf8_to_euc_cn</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_CN</code></td></tr><tr><td><code class="literal">utf8_to_euc_jp</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">utf8_to_euc_kr</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_KR</code></td></tr><tr><td><code class="literal">utf8_to_euc_tw</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">utf8_to_gb18030</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">GB18030</code></td></tr><tr><td><code class="literal">utf8_to_gbk</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">GBK</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_1</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN1</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_10</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN6</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_13</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN7</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_14</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN8</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_15</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN9</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_16</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN10</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_2</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_3</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN3</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_4</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN4</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_5</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_6</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_6</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_7</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_7</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_8</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_8</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_9</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN5</code></td></tr><tr><td><code class="literal">utf8_to_johab</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">JOHAB</code></td></tr><tr><td><code class="literal">utf8_to_koi8_r</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">utf8_to_koi8_u</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">KOI8U</code></td></tr><tr><td><code class="literal">utf8_to_sjis</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">utf8_to_windows_1258</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1258</code></td></tr><tr><td><code class="literal">utf8_to_uhc</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">UHC</code></td></tr><tr><td><code class="literal">utf8_to_windows_1250</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">utf8_to_windows_1251</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">utf8_to_windows_1252</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1252</code></td></tr><tr><td><code class="literal">utf8_to_windows_1253</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1253</code></td></tr><tr><td><code class="literal">utf8_to_windows_1254</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1254</code></td></tr><tr><td><code class="literal">utf8_to_windows_1255</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1255</code></td></tr><tr><td><code class="literal">utf8_to_windows_1256</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1256</code></td></tr><tr><td><code class="literal">utf8_to_windows_1257</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1257</code></td></tr><tr><td><code class="literal">utf8_to_windows_866</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">utf8_to_windows_874</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN874</code></td></tr><tr><td><code class="literal">windows_1250_to_iso_8859_2</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">windows_1250_to_mic</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_1250_to_utf8</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1251_to_iso_8859_5</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">windows_1251_to_koi8_r</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">windows_1251_to_mic</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_1251_to_utf8</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1251_to_windows_866</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">windows_1252_to_utf8</code></td><td><code class="literal">WIN1252</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1256_to_utf8</code></td><td><code class="literal">WIN1256</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_866_to_iso_8859_5</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">windows_866_to_koi8_r</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">windows_866_to_mic</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_866_to_utf8</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_866_to_windows_1251</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">WIN</code></td></tr><tr><td><code class="literal">windows_874_to_utf8</code></td><td><code class="literal">WIN874</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_jis_2004_to_utf8</code></td><td><code class="literal">EUC_JIS_2004</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_euc_jis_2004</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_JIS_2004</code></td></tr><tr><td><code class="literal">shift_jis_2004_to_utf8</code></td><td><code class="literal">SHIFT_JIS_2004</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_shift_jis_2004</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">SHIFT_JIS_2004</code></td></tr><tr><td><code class="literal">euc_jis_2004_to_shift_jis_2004</code></td><td><code class="literal">EUC_JIS_2004</code></td><td><code class="literal">SHIFT_JIS_2004</code></td></tr><tr><td><code class="literal">shift_jis_2004_to_euc_jis_2004</code></td><td><code class="literal">SHIFT_JIS_2004</code></td><td><code class="literal">EUC_JIS_2004</code></td></tr></tbody><tbody class="footnotes"><tr><td colspan="3"><div class="footnote" id="ftn.id-1.6.10.5.8.4.2.4.1.1.1"><p><a class="para" href="#id-1.6.10.5.8.4.2.4.1.1.1"><sup class="para">[a] </sup></a>轉換名稱遵循一套標準命名方式：來源編碼的
           正式名稱，將所有非英數字元替換為底線，接著加上
           <code class="literal">_to_</code>，再接上經過相同處理的
           目的編碼名稱。因此，這些名稱有時候會與
           <a class="xref" href="multibyte-charset-supported.md#charset-table">表 23.3</a> 中所顯示的慣用編碼名稱不同。
          </p></div></td></tr></tbody></table>

<br class="table-break" />

譯註：表 23.5 中 windows_866_to_windows_1251 一列的目的編碼，原文誤植為 WIN；正確應為 WIN1251（可由表 23.4 中 WIN866 一列的可轉換編碼佐證）。表格內容依原文保留。

[返回 23.3. 字元集支援](../multibyte.md#multibyte)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/multibyte.html)（原文版本：18.6；核對日期：2026-10-23）
