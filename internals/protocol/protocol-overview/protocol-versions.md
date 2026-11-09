# 54.1.4. 協定版本

<a id="PROTOCOL-VERSIONS"></a>

## 54.1.4. 協定版本 [#](#protocol-versions) <a href="#protocol-versions" id="protocol-versions"></a>

協定目前最新的版本是 3.2 版。然而，為了與尚未支援版本協商的舊版伺服器及中介軟體保持向後相容，libpq 預設仍使用協定 3.0 版。

單一伺服器可以支援多個協定版本。最初的啟動請求訊息會告訴伺服器用戶端正嘗試使用哪個協定版本。若伺服器不支援用戶端所請求的主要版本，連線就會被拒絕（例如，若用戶端請求協定 4.0 版就會發生這種情況，在撰寫本文時該版本並不存在）。若伺服器不支援用戶端所請求的次要版本（例如，用戶端請求 3.2 版，但伺服器只支援 3.0 版），伺服器可以拒絕連線，也可以回應一則 NegotiateProtocolVersion 訊息，其中包含它所支援的最高次要協定版本。接著，用戶端可以選擇使用所指定的協定版本繼續連線，或是中止連線。

協定協商是在 PostgreSQL 9.3.21 版引入的。較早的版本在用戶端請求伺服器不支援的次要版本時，會拒絕連線。

[表 54.1](#protocol-versions-table) 列出目前支援的協定版本。

<a id="PROTOCOL-VERSIONS-TABLE"></a>

### 表 54.1. 協定版本 [#](#protocol-versions-table) <a href="#protocol-versions-table" id="protocol-versions-table"></a>

<table border="1" class="table" summary="協定版本"><colgroup><col/><col/><col/></colgroup><thead><tr><th>版本</th><th>支援版本</th><th>說明</th></tr></thead><tbody><tr><td>3.2</td><td>PostgreSQL 18 及之後版本</td><td>目前最新的版本。查詢取消所使用的祕密金鑰已從 4 位元組擴大為可變長度的欄位。BackendKeyData 訊息已隨之修改，CancelRequest 訊息也已重新定義為具有可變長度的酬載。
      </td></tr><tr><td>3.1</td><td>-</td><td>保留。3.1 版從未被任何 PostgreSQL 版本使用；之所以跳過它，是因為熱門的 pgbouncer 應用程式的舊版本在協定協商中有一個錯誤，會錯誤地宣稱它支援 3.1 版。
      </td></tr><tr><td>3.0</td><td>PostgreSQL 7.4 及之後版本</td><td class="auto-generated"> </td></tr><tr><td>2.0</td><td>至 PostgreSQL 13 為止</td><td>詳細資訊請參閱 <span class="productname">PostgreSQL</span> 文件的先前版本</td></tr></tbody></table>

<br>

[返回 54.1. 概觀](../protocol-overview.md#protocol-overview)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-overview.html)（原文版本：18.6；核對日期：2026-10-12）
