<a id="MULTIBYTE"></a>

## 23.3. 字元集支援 [#](#multibyte) <a href="#multibyte" id="multibyte"></a>

[23.3.1. 支援的字元集](multibyte.md#multibyte-charset-supported)

[23.3.2. 設定字元集](multibyte.md#multibyte-setting)

[23.3.3. 伺服器與用戶端間的自動字元集轉換](multibyte.md#multibyte-automatic-conversion)

[23.3.4. 可用的字元集轉換](multibyte.md#multibyte-conversions-supported)

[23.3.5. 延伸閱讀](multibyte.md#multibyte-further-reading)

<a id="id-1.6.10.5.2"></a>

PostgreSQL 的字元集支援
讓你可以用多種字元集（也稱為
編碼）來儲存文字，包括
單位元組字元集（例如 ISO 8859 系列）以及
多位元組字元集（例如 EUC（Extended Unix
Code）、UTF-8 及 Mule 內部編碼）。所有支援的字元集
都可以被用戶端透明地使用，但其中少數幾種不支援
在伺服器內部使用（也就是不能作為伺服器端編碼）。
預設字元集會在使用 `initdb` 初始化
PostgreSQL 資料庫
叢集時選定。建立資料庫時可以覆寫此設定，因此你可以讓多個
資料庫各自使用不同的字元集。

不過，這裡有一項重要的限制：每個資料庫的字元集
必須與該資料庫的 `LC_CTYPE`（字元
分類）以及 `LC_COLLATE`（字串排序順序）區域設定
相容。對於 `C` 或
`POSIX` 區域設定，可以使用任何字元集，但對於其他
由 libc 提供的區域設定，只有一種字元集能正確
運作。
（不過在 Windows 上，UTF-8 編碼可以搭配任何區域設定使用。）
若你已設定了 ICU 支援，ICU 所提供的區域設定可以搭配大部分（但非全部）伺服器端編碼使用。

<a id="MULTIBYTE-CHARSET-SUPPORTED"></a>

### 23.3.1. 支援的字元集 [#](#multibyte-charset-supported) <a href="#multibyte-charset-supported" id="multibyte-charset-supported"></a>

[表 23.3](multibyte.md#CHARSET-TABLE) 顯示了
PostgreSQL 中可用的字元集。

<a id="CHARSET-TABLE"></a>

**表 23.3. PostgreSQL 字元集**

<table border="1" class="table" summary="PostgreSQL 字元集"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/><col class="col6"/><col class="col7"/></colgroup><thead><tr><th>名稱</th><th>說明</th><th>語言</th><th>伺服器？</th><th>ICU？</th><th>位元組/​字元</th><th>別名</th></tr></thead><tbody><tr><td><code class="literal">BIG5</code></td><td>Big Five</td><td>正體中文</td><td>否</td><td>否</td><td>1–2</td><td><code class="literal">WIN950</code>, <code class="literal">Windows950</code></td></tr><tr><td><code class="literal">EUC_CN</code></td><td>Extended UNIX Code-CN</td><td>簡體中文</td><td>是</td><td>是</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_JP</code></td><td>Extended UNIX Code-JP</td><td>日文</td><td>是</td><td>是</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_JIS_2004</code></td><td>Extended UNIX Code-JP, JIS X 0213</td><td>日文</td><td>是</td><td>否</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_KR</code></td><td>Extended UNIX Code-KR</td><td>韓文</td><td>是</td><td>是</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_TW</code></td><td>Extended UNIX Code-TW</td><td>正體中文、台灣話</td><td>是</td><td>是</td><td>1–4</td><td> </td></tr><tr><td><code class="literal">GB18030</code></td><td>國家標準</td><td>中文</td><td>否</td><td>否</td><td>1–4</td><td> </td></tr><tr><td><code class="literal">GBK</code></td><td>延伸國家標準</td><td>簡體中文</td><td>否</td><td>否</td><td>1–2</td><td><code class="literal">WIN936</code>, <code class="literal">Windows936</code></td></tr><tr><td><code class="literal">ISO_8859_5</code></td><td>ISO 8859-5, <acronym class="acronym">ECMA</acronym> 113</td><td>拉丁／西里爾</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">ISO_8859_6</code></td><td>ISO 8859-6, <acronym class="acronym">ECMA</acronym> 114</td><td>拉丁／阿拉伯</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">ISO_8859_7</code></td><td>ISO 8859-7, <acronym class="acronym">ECMA</acronym> 118</td><td>拉丁／希臘</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">ISO_8859_8</code></td><td>ISO 8859-8, <acronym class="acronym">ECMA</acronym> 121</td><td>拉丁／希伯來</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">JOHAB</code></td><td><acronym class="acronym">JOHAB</acronym></td><td>韓文（諺文）</td><td>否</td><td>否</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">KOI8R</code></td><td><acronym class="acronym">KOI</acronym>8-R</td><td>西里爾文（俄文）</td><td>是</td><td>是</td><td>1</td><td><code class="literal">KOI8</code></td></tr><tr><td><code class="literal">KOI8U</code></td><td><acronym class="acronym">KOI</acronym>8-U</td><td>西里爾文（烏克蘭文）</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">LATIN1</code></td><td>ISO 8859-1, <acronym class="acronym">ECMA</acronym> 94</td><td>西歐</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO88591</code></td></tr><tr><td><code class="literal">LATIN2</code></td><td>ISO 8859-2, <acronym class="acronym">ECMA</acronym> 94</td><td>中歐</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO88592</code></td></tr><tr><td><code class="literal">LATIN3</code></td><td>ISO 8859-3, <acronym class="acronym">ECMA</acronym> 94</td><td>南歐</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO88593</code></td></tr><tr><td><code class="literal">LATIN4</code></td><td>ISO 8859-4, <acronym class="acronym">ECMA</acronym> 94</td><td>北歐</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO88594</code></td></tr><tr><td><code class="literal">LATIN5</code></td><td>ISO 8859-9, <acronym class="acronym">ECMA</acronym> 128</td><td>土耳其文</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO88599</code></td></tr><tr><td><code class="literal">LATIN6</code></td><td>ISO 8859-10, <acronym class="acronym">ECMA</acronym> 144</td><td>北歐地區（Nordic）</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO885910</code></td></tr><tr><td><code class="literal">LATIN7</code></td><td>ISO 8859-13</td><td>波羅的海</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO885913</code></td></tr><tr><td><code class="literal">LATIN8</code></td><td>ISO 8859-14</td><td>凱爾特</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO885914</code></td></tr><tr><td><code class="literal">LATIN9</code></td><td>ISO 8859-15</td><td>LATIN1 加上歐元符號與重音符號</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ISO885915</code></td></tr><tr><td><code class="literal">LATIN10</code></td><td>ISO 8859-16, <acronym class="acronym">ASRO</acronym> SR 14111</td><td>羅馬尼亞文</td><td>是</td><td>否</td><td>1</td><td><code class="literal">ISO885916</code></td></tr><tr><td><code class="literal">MULE_INTERNAL</code></td><td>Mule 內部編碼</td><td>多語言 Emacs</td><td>是</td><td>否</td><td>1–4</td><td> </td></tr><tr><td><code class="literal">SJIS</code></td><td>Shift JIS</td><td>日文</td><td>否</td><td>否</td><td>1–2</td><td><code class="literal">Mskanji</code>, <code class="literal">ShiftJIS</code>, <code class="literal">WIN932</code>, <code class="literal">Windows932</code></td></tr><tr><td><code class="literal">SHIFT_JIS_2004</code></td><td>Shift JIS，JIS X 0213</td><td>日文</td><td>否</td><td>否</td><td>1–2</td><td> </td></tr><tr><td><code class="literal">SQL_ASCII</code></td><td>未指定（請參閱內文）</td><td><span class="emphasis"><em>任何</em></span></td><td>是</td><td>否</td><td>1</td><td> </td></tr><tr><td><code class="literal">UHC</code></td><td>統一諺文編碼（Unified Hangul Code）</td><td>韓文</td><td>否</td><td>否</td><td>1–2</td><td><code class="literal">WIN949</code>, <code class="literal">Windows949</code></td></tr><tr><td><code class="literal">UTF8</code></td><td>Unicode，8 位元</td><td><span class="emphasis"><em>全部</em></span></td><td>是</td><td>是</td><td>1–4</td><td><code class="literal">Unicode</code></td></tr><tr><td><code class="literal">WIN866</code></td><td>Windows CP866</td><td>西里爾文</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ALT</code></td></tr><tr><td><code class="literal">WIN874</code></td><td>Windows CP874</td><td>泰文</td><td>是</td><td>否</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1250</code></td><td>Windows CP1250</td><td>中歐</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1251</code></td><td>Windows CP1251</td><td>西里爾文</td><td>是</td><td>是</td><td>1</td><td><code class="literal">WIN</code></td></tr><tr><td><code class="literal">WIN1252</code></td><td>Windows CP1252</td><td>西歐</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1253</code></td><td>Windows CP1253</td><td>希臘文</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1254</code></td><td>Windows CP1254</td><td>土耳其文</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1255</code></td><td>Windows CP1255</td><td>希伯來文</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1256</code></td><td>Windows CP1256</td><td>阿拉伯文</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1257</code></td><td>Windows CP1257</td><td>波羅的海</td><td>是</td><td>是</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1258</code></td><td>Windows CP1258</td><td>越南文</td><td>是</td><td>是</td><td>1</td><td><code class="literal">ABC</code>, <code class="literal">TCVN</code>, <code class="literal">TCVN5712</code>, <code class="literal">VSCII</code></td></tr></tbody></table>

<br class="table-break" />

並非所有用戶端 API 都支援上述所列的所有字元集。舉例來說，
PostgreSQL
JDBC 驅動程式就不支援 `MULE_INTERNAL`、`LATIN6`、
`LATIN8` 及 `LATIN10`。

`SQL_ASCII` 設定的行為與其他設定
有相當大的不同。當伺服器字元集為
`SQL_ASCII` 時，伺服器會依照 ASCII 標準解讀
位元組值 0–127，而位元組值 128–255 則會被
視為未經解讀的字元。當設定為 `SQL_ASCII` 時，
不會進行任何編碼轉換。因此，與其說這個設定是在宣告
使用了某種特定編碼，不如說它是在宣告
對編碼一無所知。在大多數情況下，如果你要
處理任何非 ASCII 資料，使用
`SQL_ASCII` 設定並非明智之舉，因為
PostgreSQL 將無法藉由
轉換或驗證非 ASCII 字元來提供協助。

<a id="MULTIBYTE-SETTING"></a>

### 23.3.2. 設定字元集 [#](#multibyte-setting) <a href="#multibyte-setting" id="multibyte-setting"></a>

`initdb` 定義了
PostgreSQL 叢集的預設字元集（編碼）。例如，

```

initdb -E EUC_JP
```

會將預設字元集設定為
`EUC_JP`（日文的 Extended Unix Code）。若你偏好較長的選項字串，
可以使用 `--encoding`
取代 `-E`。
如果未指定 `-E` 或 `--encoding` 選項，
`initdb` 會嘗試根據所指定或預設的區域設定，
判斷應使用的適當編碼。

你可以在建立資料庫時指定非預設的編碼，
前提是該編碼必須與所選擇的區域設定相容：

```

createdb -E EUC_KR -T template0 --lc-collate=ko_KR.euckr --lc-ctype=ko_KR.euckr korean
```

這會建立一個名為 `korean` 的資料庫，
使用字元集 `EUC_KR`，區域設定為 `ko_KR`。
要達成此目的，另一種方式是使用以下 SQL 指令：

```

CREATE DATABASE korean WITH ENCODING 'EUC_KR' LC_COLLATE='ko_KR.euckr' LC_CTYPE='ko_KR.euckr' TEMPLATE=template0;
```

請注意，上述指令都指定要複製 `template0`
資料庫。當複製其他任何資料庫時，編碼與區域設定
都無法變更為與來源資料庫不同的設定，因為這樣
可能導致資料損毀。詳情請參閱
[第 22.3 節](../managing-databases/manage-ag-templatedbs.md)。

資料庫的編碼會儲存在系統目錄
`pg_database` 中。你可以使用
`psql` 的 `-l` 選項，或
`\l` 指令來查看。

```

$ psql -l
                                         List of databases
   Name    |  Owner   | Encoding  |  Collation  |    Ctype    |          Access Privileges
-----------+----------+-----------+-------------+-------------+-------------------------------------
 clocaledb | hlinnaka | SQL_ASCII | C           | C           |
 englishdb | hlinnaka | UTF8      | en_GB.UTF8  | en_GB.UTF8  |
 japanese  | hlinnaka | UTF8      | ja_JP.UTF8  | ja_JP.UTF8  |
 korean    | hlinnaka | EUC_KR    | ko_KR.euckr | ko_KR.euckr |
 postgres  | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  |
 template0 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
 template1 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
(7 rows)
```

### 重要

在大多數現代作業系統上，PostgreSQL
可以判斷 `LC_CTYPE` 設定所隱含的字元集，
並會強制要求只能使用相符的資料庫編碼。在較舊的系統上，
確保所使用的編碼與所選區域設定相符便是你的責任。在這方面若有失誤，
很可能導致依賴區域設定的操作（例如排序）出現異常行為。

即使 `LC_CTYPE` 不是 `C` 或 `POSIX`，
PostgreSQL 仍會允許超級使用者建立
使用 `SQL_ASCII` 編碼的資料庫。如上所述，
`SQL_ASCII` 並不會強制要求資料庫中儲存的資料具有任何特定編碼，
因此這項選擇會帶來依賴區域設定而產生異常行為的風險。這種組合設定
已不建議使用，未來某天可能會被完全禁止。

<a id="MULTIBYTE-AUTOMATIC-CONVERSION"></a>

### 23.3.3. 伺服器與用戶端間的自動字元集轉換 [#](#multibyte-automatic-conversion) <a href="#multibyte-automatic-conversion" id="multibyte-automatic-conversion"></a>

PostgreSQL 支援在許多字元
集組合之間，於伺服器與用戶端之間進行自動字元集轉換
（[第 23.3.4 節](multibyte.md#multibyte-conversions-supported)
顯示了具體有哪些組合）。

若要啟用自動字元集轉換，你必須
告知 PostgreSQL 你想在用戶端使用的字元集
（編碼）。有幾種方式可以達成此目的：

* 在 psql 中使用
  `\encoding` 指令。
  `\encoding` 讓你可以即時變更用戶端
  編碼。例如，
  若要將編碼變更為 `SJIS`，請輸入：

  ```

  \encoding SJIS
  ```
* libpq（[第 32.11 節](../../client-interfaces/libpq/libpq-control.md)）提供了控制用戶端編碼的函式。
* 使用 `SET client_encoding TO`。
  可以使用以下 SQL 指令設定用戶端編碼：

  ```

  SET CLIENT_ENCODING TO 'value';
  ```

  你也可以使用標準 SQL 語法 `SET NAMES`
  來達成同樣的目的：

  ```

  SET NAMES 'value';
  ```

  若要查詢目前的用戶端編碼：

  ```

  SHOW client_encoding;
  ```

  若要回復為預設編碼：

  ```

  RESET client_encoding;
  ```
* 使用 `PGCLIENTENCODING`。若用戶端
  環境中定義了環境變數
  `PGCLIENTENCODING`，則在連線到伺服器時，
  會自動選用該用戶端編碼。（後續仍可
  使用上述任一其他方法覆寫此設定。）
* 使用組態變數 [client_encoding](../runtime-config/runtime-config-client.md#GUC-CLIENT-ENCODING)。若設定了
  `client_encoding` 變數，則在連線到
  伺服器時，會自動選用該用戶端編碼。（後續仍可
  使用上述任一其他方法覆寫此設定。）

若無法轉換某個特定字元——
假設你為伺服器選用了 `EUC_JP`，
而用戶端選用 `LATIN1`，且回傳了某些
在 `LATIN1` 中沒有對應表示法的
日文字元——則會回報錯誤。

若用戶端字元集被定義為 `SQL_ASCII`，
則無論伺服器的字元集為何，都會停用編碼轉換。
（不過，若伺服器的字元集
不是 `SQL_ASCII`，伺服器仍會檢查
傳入的資料對該編碼而言是否有效；因此實際效果
就如同用戶端字元集與伺服器相同一樣。）
與伺服器端的情況相同，除非你要處理的是全 ASCII 資料，
否則使用 `SQL_ASCII` 並非明智之舉。

<a id="MULTIBYTE-CONVERSIONS-SUPPORTED"></a>

### 23.3.4. 可用的字元集轉換 [#](#multibyte-conversions-supported) <a href="#multibyte-conversions-supported" id="multibyte-conversions-supported"></a>

只要轉換函式列於
[`pg_conversion`](../../internals/catalogs/catalog-pg-conversion.md)
系統目錄中，PostgreSQL 就允許在任意
兩種字元集之間進行轉換。PostgreSQL
內建了一些預先定義的轉換，摘要列於
[表 23.4](multibyte.md#MULTIBYTE-TRANSLATION-TABLE)，並在
[表 23.5](multibyte.md#BUILTIN-CONVERSIONS-TABLE) 中有更詳細的說明。你可以使用 SQL 指令
[CREATE CONVERSION](../../reference/sql-commands/sql-createconversion.md) 建立新的轉換。（若要用於自動的
用戶端／伺服器轉換，該轉換必須被標記
為其字元集配對的「default（預設）」。）

<a id="MULTIBYTE-TRANSLATION-TABLE"></a>

**表 23.4. 內建的用戶端／伺服器字元集轉換**

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

**表 23.5. 所有內建的字元集轉換**

<table border="1" class="table" summary="所有內建的字元集轉換"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>轉換名稱
         <a class="footnote" href="#ftn.id-1.6.10.5.8.4.2.4.1.1.1"><sup class="footnote" id="id-1.6.10.5.8.4.2.4.1.1.1">[a]</sup></a>
</th><th>來源編碼</th><th>目的編碼</th></tr></thead><tbody><tr><td><code class="literal">big5_to_euc_tw</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">big5_to_mic</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">big5_to_utf8</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_cn_to_mic</code></td><td><code class="literal">EUC_CN</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_cn_to_utf8</code></td><td><code class="literal">EUC_CN</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_jp_to_mic</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_jp_to_sjis</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">euc_jp_to_utf8</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_kr_to_mic</code></td><td><code class="literal">EUC_KR</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_kr_to_utf8</code></td><td><code class="literal">EUC_KR</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_tw_to_big5</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">euc_tw_to_mic</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_tw_to_utf8</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">gb18030_to_utf8</code></td><td><code class="literal">GB18030</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">gbk_to_utf8</code></td><td><code class="literal">GBK</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_10_to_utf8</code></td><td><code class="literal">LATIN6</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_13_to_utf8</code></td><td><code class="literal">LATIN7</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_14_to_utf8</code></td><td><code class="literal">LATIN8</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_15_to_utf8</code></td><td><code class="literal">LATIN9</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_16_to_utf8</code></td><td><code class="literal">LATIN10</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_1_to_mic</code></td><td><code class="literal">LATIN1</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_1_to_utf8</code></td><td><code class="literal">LATIN1</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_2_to_mic</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_2_to_utf8</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_2_to_windows_1250</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">iso_8859_3_to_mic</code></td><td><code class="literal">LATIN3</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_3_to_utf8</code></td><td><code class="literal">LATIN3</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_4_to_mic</code></td><td><code class="literal">LATIN4</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_4_to_utf8</code></td><td><code class="literal">LATIN4</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_5_to_koi8_r</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">iso_8859_5_to_mic</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_5_to_utf8</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_5_to_windows_1251</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">iso_8859_5_to_windows_866</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">iso_8859_6_to_utf8</code></td><td><code class="literal">ISO_8859_6</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_7_to_utf8</code></td><td><code class="literal">ISO_8859_7</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_8_to_utf8</code></td><td><code class="literal">ISO_8859_8</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_9_to_utf8</code></td><td><code class="literal">LATIN5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">johab_to_utf8</code></td><td><code class="literal">JOHAB</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">koi8_r_to_iso_8859_5</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">koi8_r_to_mic</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">koi8_r_to_utf8</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">koi8_r_to_windows_1251</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">koi8_r_to_windows_866</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">koi8_u_to_utf8</code></td><td><code class="literal">KOI8U</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">mic_to_big5</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">mic_to_euc_cn</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_CN</code></td></tr><tr><td><code class="literal">mic_to_euc_jp</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">mic_to_euc_kr</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_KR</code></td></tr><tr><td><code class="literal">mic_to_euc_tw</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_1</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN1</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_2</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_3</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN3</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_4</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN4</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_5</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">mic_to_koi8_r</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">mic_to_sjis</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">mic_to_windows_1250</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">mic_to_windows_1251</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">mic_to_windows_866</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">sjis_to_euc_jp</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">sjis_to_mic</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">sjis_to_utf8</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1258_to_utf8</code></td><td><code class="literal">WIN1258</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">uhc_to_utf8</code></td><td><code class="literal">UHC</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_big5</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">utf8_to_euc_cn</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_CN</code></td></tr><tr><td><code class="literal">utf8_to_euc_jp</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">utf8_to_euc_kr</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_KR</code></td></tr><tr><td><code class="literal">utf8_to_euc_tw</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">utf8_to_gb18030</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">GB18030</code></td></tr><tr><td><code class="literal">utf8_to_gbk</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">GBK</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_1</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN1</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_10</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN6</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_13</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN7</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_14</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN8</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_15</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN9</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_16</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN10</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_2</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_3</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN3</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_4</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN4</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_5</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_6</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_6</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_7</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_7</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_8</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_8</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_9</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN5</code></td></tr><tr><td><code class="literal">utf8_to_johab</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">JOHAB</code></td></tr><tr><td><code class="literal">utf8_to_koi8_r</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">utf8_to_koi8_u</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">KOI8U</code></td></tr><tr><td><code class="literal">utf8_to_sjis</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">utf8_to_windows_1258</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1258</code></td></tr><tr><td><code class="literal">utf8_to_uhc</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">UHC</code></td></tr><tr><td><code class="literal">utf8_to_windows_1250</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">utf8_to_windows_1251</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">utf8_to_windows_1252</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1252</code></td></tr><tr><td><code class="literal">utf8_to_windows_1253</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1253</code></td></tr><tr><td><code class="literal">utf8_to_windows_1254</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1254</code></td></tr><tr><td><code class="literal">utf8_to_windows_1255</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1255</code></td></tr><tr><td><code class="literal">utf8_to_windows_1256</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1256</code></td></tr><tr><td><code class="literal">utf8_to_windows_1257</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1257</code></td></tr><tr><td><code class="literal">utf8_to_windows_866</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">utf8_to_windows_874</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN874</code></td></tr><tr><td><code class="literal">windows_1250_to_iso_8859_2</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">windows_1250_to_mic</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_1250_to_utf8</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1251_to_iso_8859_5</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">windows_1251_to_koi8_r</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">windows_1251_to_mic</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_1251_to_utf8</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1251_to_windows_866</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">windows_1252_to_utf8</code></td><td><code class="literal">WIN1252</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1256_to_utf8</code></td><td><code class="literal">WIN1256</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_866_to_iso_8859_5</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">windows_866_to_koi8_r</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">windows_866_to_mic</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_866_to_utf8</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_866_to_windows_1251</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">WIN</code></td></tr><tr><td><code class="literal">windows_874_to_utf8</code></td><td><code class="literal">WIN874</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_jis_2004_to_utf8</code></td><td><code class="literal">EUC_JIS_2004</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_euc_jis_2004</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_JIS_2004</code></td></tr><tr><td><code class="literal">shift_jis_2004_to_utf8</code></td><td><code class="literal">SHIFT_JIS_2004</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_shift_jis_2004</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">SHIFT_JIS_2004</code></td></tr><tr><td><code class="literal">euc_jis_2004_to_shift_jis_2004</code></td><td><code class="literal">EUC_JIS_2004</code></td><td><code class="literal">SHIFT_JIS_2004</code></td></tr><tr><td><code class="literal">shift_jis_2004_to_euc_jis_2004</code></td><td><code class="literal">SHIFT_JIS_2004</code></td><td><code class="literal">EUC_JIS_2004</code></td></tr></tbody><tbody class="footnotes"><tr><td colspan="3"><div class="footnote" id="ftn.id-1.6.10.5.8.4.2.4.1.1.1"><p><a class="para" href="#id-1.6.10.5.8.4.2.4.1.1.1"><sup class="para">[a] </sup></a>轉換名稱遵循一套標準命名方式：來源編碼的
           正式名稱，將所有非英數字元替換為底線，接著加上
           <code class="literal">_to_</code>，再接上經過相同處理的
           目的編碼名稱。因此，這些名稱有時候會與
           <a class="xref" href="multibyte.md#CHARSET-TABLE">表 23.3</a> 中所顯示的慣用編碼名稱不同。
          </p></div></td></tr></tbody></table>

<br class="table-break" />

譯註：表 23.5 中 windows_866_to_windows_1251 一列的目的編碼，原文誤植為 WIN；正確應為 WIN1251（可由表 23.4 中 WIN866 一列的可轉換編碼佐證）。表格內容依原文保留。

<a id="MULTIBYTE-FURTHER-READING"></a>

### 23.3.5. 延伸閱讀 [#](#multibyte-further-reading) <a href="#multibyte-further-reading" id="multibyte-further-reading"></a>

以下是開始學習各種編碼系統的優良參考資料。

*CJKV Information Processing: Chinese, Japanese, Korean & Vietnamese Computing*
:   內含 `EUC_JP`、
    `EUC_CN`、`EUC_KR`、
    `EUC_TW` 的詳細說明。

<https://www.unicode.org/>
:   Unicode 協會的網站。

[RFC 3629](https://datatracker.ietf.org/doc/html/rfc3629)
:   UTF-8（8 位元 UCS／Unicode 轉換
    格式）即定義於此。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/multibyte.html)（原文版本：18.6；核對日期：2026-10-23）
