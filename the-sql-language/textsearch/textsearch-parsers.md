<a id="TEXTSEARCH-PARSERS"></a>

## 12.5. 剖析器 [#](#TEXTSEARCH-PARSERS)

文字搜尋剖析器負責將原始文件文字切分為*語彙單元*（token），並識別每個語彙單元的類型，而可能的類型集合是由剖析器本身定義的。請注意，剖析器完全不會修改文字，它只是找出可能的單字邊界。由於職責範圍有限，針對特定應用自訂剖析器的需求，比自訂字典的需求要少。目前 PostgreSQL 只提供一個內建剖析器，而它已被證明適用於各式各樣的應用。

內建剖析器的名稱是 `pg_catalog.default`。它可以辨識 23 種語彙單元類型，如[表 12.1](textsearch-parsers.md#TEXTSEARCH-DEFAULT-PARSER) 所示。

<a id="TEXTSEARCH-DEFAULT-PARSER"></a>

**表 12.1. 預設剖析器的語彙單元類型**

<table border="1" class="table" summary="Default Parser's Token Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>別名</th><th>說明</th><th>範例</th></tr></thead><tbody><tr><td><code class="literal">asciiword</code></td><td>單字，全為 ASCII 字母</td><td><code class="literal">elephant</code></td></tr><tr><td><code class="literal">word</code></td><td>單字，全為字母</td><td><code class="literal">mañana</code></td></tr><tr><td><code class="literal">numword</code></td><td>單字，包含字母與數字</td><td><code class="literal">beta1</code></td></tr><tr><td><code class="literal">asciihword</code></td><td>連字號複合詞，全為 ASCII</td><td><code class="literal">up-to-date</code></td></tr><tr><td><code class="literal">hword</code></td><td>連字號複合詞，全為字母</td><td><code class="literal">lógico-matemática</code></td></tr><tr><td><code class="literal">numhword</code></td><td>連字號複合詞，包含字母與數字</td><td><code class="literal">postgresql-beta1</code></td></tr><tr><td><code class="literal">hword_asciipart</code></td><td>連字號複合詞的組成部分，全為 ASCII</td><td><code class="literal">postgresql</code> 於 <code class="literal">postgresql-beta1</code> 中的情境</td></tr><tr><td><code class="literal">hword_part</code></td><td>連字號複合詞的組成部分，全為字母</td><td><code class="literal">lógico</code> 或 <code class="literal">matemática</code>
       於 <code class="literal">lógico-matemática</code> 中的情境</td></tr><tr><td><code class="literal">hword_numpart</code></td><td>連字號複合詞的組成部分，包含字母與數字</td><td><code class="literal">beta1</code> 於
       <code class="literal">postgresql-beta1</code> 中的情境</td></tr><tr><td><code class="literal">email</code></td><td>電子郵件地址</td><td><code class="literal">foo@example.com</code></td></tr><tr><td><code class="literal">protocol</code></td><td>協定開頭</td><td><code class="literal">http://</code></td></tr><tr><td><code class="literal">url</code></td><td>URL</td><td><code class="literal">example.com/stuff/index.html</code></td></tr><tr><td><code class="literal">host</code></td><td>主機</td><td><code class="literal">example.com</code></td></tr><tr><td><code class="literal">url_path</code></td><td>URL 路徑</td><td><code class="literal">/stuff/index.html</code>，在 URL 的情境中</td></tr><tr><td><code class="literal">file</code></td><td>檔案或路徑名稱</td><td><code class="literal">/usr/local/foo.txt</code>，如果不在 URL 之中</td></tr><tr><td><code class="literal">sfloat</code></td><td>科學記號</td><td><code class="literal">-1.234e56</code></td></tr><tr><td><code class="literal">float</code></td><td>十進位記號</td><td><code class="literal">-1.234</code></td></tr><tr><td><code class="literal">int</code></td><td>有號整數</td><td><code class="literal">-1234</code></td></tr><tr><td><code class="literal">uint</code></td><td>無號整數</td><td><code class="literal">1234</code></td></tr><tr><td><code class="literal">version</code></td><td>版本號碼</td><td><code class="literal">8.3.0</code></td></tr><tr><td><code class="literal">tag</code></td><td>XML 標籤</td><td><code class="literal">&lt;a href="dictionaries.html"&gt;</code></td></tr><tr><td><code class="literal">entity</code></td><td>XML 實體</td><td><code class="literal">&amp;amp;</code></td></tr><tr><td><code class="literal">blank</code></td><td>空白符號</td><td>（任何未被辨識為其他類型的空白或標點符號）</td></tr></tbody></table>

<br>

### 注意

剖析器對「字母」的認定是由資料庫的 locale 設定決定的，具體來說是 `lc_ctype`。只包含基本 ASCII 字母的單字會被回報為獨立的語彙單元類型，因為有時區分它們很有用。在大多數歐洲語言中，語彙單元類型 `word` 與 `asciiword` 應該以相同方式處理。

`email` 並不支援 [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322) 所定義的所有有效電子郵件字元。具體來說，電子郵件使用者名稱中唯一支援的非英數字元是句點、破折號與底線。

`tag` 並不支援 [W3C Recommendation, XML](https://www.w3.org/TR/xml/) 所定義的所有有效標籤名稱。具體來說，只支援以 ASCII 字母、底線或冒號開頭，且只包含字母、數字、連字號、底線、句點與冒號的標籤名稱。`tag` 也包含以 `<!--` 開頭、以 `-->` 結尾的 XML 註解，以及 XML 宣告（但請注意，這包括任何以 `<?x` 開頭、以 `>` 結尾的內容）。

剖析器有可能從同一段文字產生重疊的語彙單元。例如，連字號複合詞會同時被回報為整個單字以及其中的每個組成部分：

```

SELECT alias, description, token FROM ts_debug('foo-bar-beta1');
      alias      |               description                |     token
-----------------+------------------------------------------+---------------
 numhword        | Hyphenated word, letters and digits      | foo-bar-beta1
 hword_asciipart | Hyphenated word part, all ASCII          | foo
 blank           | Space symbols                            | -
 hword_asciipart | Hyphenated word part, all ASCII          | bar
 blank           | Space symbols                            | -
 hword_numpart   | Hyphenated word part, letters and digits | beta1
```

這種行為是理想的，因為它讓搜尋對整個複合詞以及其組成部分都能運作。以下是另一個具有啟發性的範例：

```

SELECT alias, description, token FROM ts_debug('http://example.com/stuff/index.html');
  alias   |  description  |            token
----------+---------------+------------------------------
 protocol | Protocol head | http://
 url      | URL           | example.com/stuff/index.html
 host     | Host          | example.com
 url_path | URL path      | /stuff/index.html
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-parsers.html)（原文版本：18.6；核對日期：2026-09-11）
