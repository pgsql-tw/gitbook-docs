# 19.8.5. 使用 JSON 格式日誌輸出

<a id="RUNTIME-CONFIG-LOGGING-JSONLOG"></a>

## 19.8.5. 使用 JSON 格式日誌輸出 [#](#runtime-config-logging-jsonlog) <a href="#runtime-config-logging-jsonlog" id="runtime-config-logging-jsonlog"></a>

在 `log_destination` 清單中包含
`jsonlog`，能提供一種方便的方式，
將日誌檔案匯入許多不同的程式。此選項會以
JSON 格式輸出日誌行。

值為 null 的字串欄位不會出現在輸出中。
未來可能會加入更多欄位。處理
`jsonlog` 輸出的使用者應用程式，
應忽略未知的欄位。

每一行日誌都會序列化為一個 JSON 物件，其中包含
[表 19.4](#runtime-config-logging-jsonlog-keys-values)
所示的鍵集合及其對應的值。

<a id="RUNTIME-CONFIG-LOGGING-JSONLOG-KEYS-VALUES"></a>

### 表 19.4. JSON 日誌項目的鍵與值 [#](#runtime-config-logging-jsonlog-keys-values) <a href="#runtime-config-logging-jsonlog-keys-values" id="runtime-config-logging-jsonlog-keys-values"></a>

<table border="1" class="table" summary="JSON 日誌項目的鍵與值"><colgroup><col/><col/><col/></colgroup><thead><tr><th>鍵名稱</th><th>類型</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">timestamp</code></td><td>string</td><td>含毫秒的時間戳記</td></tr><tr><td><code class="literal">user</code></td><td>string</td><td>使用者名稱</td></tr><tr><td><code class="literal">dbname</code></td><td>string</td><td>資料庫名稱</td></tr><tr><td><code class="literal">pid</code></td><td>number</td><td>程序 ID</td></tr><tr><td><code class="literal">remote_host</code></td><td>string</td><td>用戶端主機</td></tr><tr><td><code class="literal">remote_port</code></td><td>number</td><td>用戶端連接埠</td></tr><tr><td><code class="literal">session_id</code></td><td>string</td><td>工作階段 ID</td></tr><tr><td><code class="literal">line_num</code></td><td>number</td><td>每個工作階段的行編號</td></tr><tr><td><code class="literal">ps</code></td><td>string</td><td>目前的 ps 顯示內容</td></tr><tr><td><code class="literal">session_start</code></td><td>string</td><td>工作階段開始時間</td></tr><tr><td><code class="literal">vxid</code></td><td>string</td><td>虛擬交易 ID</td></tr><tr><td><code class="literal">txid</code></td><td>string</td><td>一般交易 ID</td></tr><tr><td><code class="literal">error_severity</code></td><td>string</td><td>錯誤嚴重性</td></tr><tr><td><code class="literal">state_code</code></td><td>string</td><td>SQLSTATE 代碼</td></tr><tr><td><code class="literal">message</code></td><td>string</td><td>錯誤訊息</td></tr><tr><td><code class="literal">detail</code></td><td>string</td><td>錯誤訊息詳情</td></tr><tr><td><code class="literal">hint</code></td><td>string</td><td>錯誤訊息提示</td></tr><tr><td><code class="literal">internal_query</code></td><td>string</td><td>導致此錯誤的內部查詢</td></tr><tr><td><code class="literal">internal_position</code></td><td>number</td><td>內部查詢中的游標索引</td></tr><tr><td><code class="literal">context</code></td><td>string</td><td>錯誤上下文</td></tr><tr><td><code class="literal">statement</code></td><td>string</td><td>用戶端提供的查詢字串</td></tr><tr><td><code class="literal">cursor_position</code></td><td>number</td><td>查詢字串中的游標索引</td></tr><tr><td><code class="literal">func_name</code></td><td>string</td><td>錯誤位置的函式名稱</td></tr><tr><td><code class="literal">file_name</code></td><td>string</td><td>錯誤位置的檔案名稱</td></tr><tr><td><code class="literal">file_line_num</code></td><td>number</td><td>錯誤位置的檔案行號</td></tr><tr><td><code class="literal">application_name</code></td><td>string</td><td>用戶端應用程式名稱</td></tr><tr><td><code class="literal">backend_type</code></td><td>string</td><td>後端類型</td></tr><tr><td><code class="literal">leader_pid</code></td><td>number</td><td>作用中平行工作者之領導者的程序 ID</td></tr><tr><td><code class="literal">query_id</code></td><td>number</td><td>查詢 ID</td></tr></tbody></table>

<br>

[返回 19.8. 錯誤回報與日誌記錄](../runtime-config-logging.md#runtime-config-logging)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-logging.html)（原文版本：18.6；核對日期：2026-10-23）
