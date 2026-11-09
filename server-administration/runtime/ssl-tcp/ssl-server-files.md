# 18.9.4. SSL 伺服器檔案的使用

<a id="SSL-SERVER-FILES"></a>

## 18.9.4. SSL 伺服器檔案的使用 [#](#ssl-server-files) <a href="#ssl-server-files" id="ssl-server-files"></a>

[表 18.2](#ssl-file-usage) 彙整了與伺服器上
SSL 設定相關的檔案。（所示的檔案名稱為預設名稱，
本機設定的名稱可能有所不同。）

<a id="SSL-FILE-USAGE"></a>

### 表 18.2. SSL 伺服器檔案的使用 [#](#ssl-file-usage) <a href="#ssl-file-usage" id="ssl-file-usage"></a>

<table border="1" class="table" summary="SSL Server File Usage"><colgroup><col/><col/><col/></colgroup><thead><tr><th>檔案</th><th>內容</th><th>作用</th></tr></thead><tbody><tr><td><a class="xref" href="../../runtime-config/runtime-config-connection.md#GUC-SSL-CERT-FILE">ssl_cert_file</a> (<code class="filename">$PGDATA/server.crt</code>)</td><td>伺服器憑證</td><td>傳送給用戶端，用以表明伺服器的身分</td></tr><tr><td><a class="xref" href="../../runtime-config/runtime-config-connection.md#GUC-SSL-KEY-FILE">ssl_key_file</a> (<code class="filename">$PGDATA/server.key</code>)</td><td>伺服器私密金鑰</td><td>證明伺服器憑證確實是由擁有者傳送的；但不代表
      該憑證擁有者值得信任</td></tr><tr><td><a class="xref" href="../../runtime-config/runtime-config-connection.md#GUC-SSL-CA-FILE">ssl_ca_file</a></td><td>受信任的憑證授權單位</td><td>檢查用戶端憑證
      是否由受信任的憑證授權單位所簽署</td></tr><tr><td><a class="xref" href="../../runtime-config/runtime-config-connection.md#GUC-SSL-CRL-FILE">ssl_crl_file</a></td><td>已由憑證授權單位撤銷的憑證</td><td>用戶端憑證不得出現在此清單中</td></tr></tbody></table>

<br>

伺服器會在啟動時，以及每次重新載入伺服器組態時，
讀取這些檔案。在 Windows 系統上，
每當為新的用戶端連線衍生出新的後端程序時，
這些檔案也會被重新讀取。

若在伺服器啟動時，偵測到這些檔案中有錯誤，
伺服器將拒絕啟動。但若是在組態重新載入期間，
偵測到錯誤，則會忽略這些檔案，繼續使用舊有的
SSL 組態。在 Windows 系統上，若在後端啟動時，
偵測到這些檔案中有錯誤，該後端將無法
建立 SSL 連線。在所有這些情況下，
錯誤狀況都會記錄於伺服器日誌中。

[返回 18.9. 使用 SSL 的安全 TCP/IP 連線](../ssl-tcp.md#ssl-tcp)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ssl-tcp.html)（原文版本：18.6；核對日期：2026-09-24）
