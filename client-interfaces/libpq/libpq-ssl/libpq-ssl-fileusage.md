# 32.19.4. SSL 用戶端檔案用途

<a id="LIBPQ-SSL-FILEUSAGE"></a>

## 32.19.4. SSL 用戶端檔案用途 [#](#libpq-ssl-fileusage) <a href="#libpq-ssl-fileusage" id="libpq-ssl-fileusage"></a>

[表 32.2](#libpq-ssl-file-usage) 彙整了與用戶端
SSL 設定相關的檔案。

<a id="LIBPQ-SSL-FILE-USAGE"></a>

### 表 32.2. Libpq／用戶端 SSL 檔案用途 [#](#libpq-ssl-file-usage) <a href="#libpq-ssl-file-usage" id="libpq-ssl-file-usage"></a>

<table border="1" class="table" summary="表 32.2. Libpq／用戶端 SSL 檔案用途"><colgroup><col/><col/><col/></colgroup><thead><tr><th>檔案</th><th>內容</th><th>作用</th></tr></thead><tbody><tr><td><code class="filename">~/.postgresql/postgresql.crt</code></td><td>用戶端憑證</td><td>傳送給伺服器</td></tr><tr><td><code class="filename">~/.postgresql/postgresql.key</code></td><td>用戶端私密金鑰</td><td>證明用戶端憑證確實是由擁有者傳送的；但不代表
      該憑證擁有者值得信任</td></tr><tr><td><code class="filename">~/.postgresql/root.crt</code></td><td>受信任的憑證授權單位</td><td>檢查伺服器憑證是否由受信任的憑證
      授權單位所簽署</td></tr><tr><td><code class="filename">~/.postgresql/root.crl</code></td><td>已被憑證授權單位撤銷的憑證</td><td>伺服器憑證不得出現在此清單中</td></tr></tbody></table>

<br>

[返回 32.19. SSL 支援](../libpq-ssl.md#libpq-ssl)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-ssl.html)（原文版本：18.6；核對日期：2026-10-17）
