<a id="PROTOCOL"></a>

## 第 54 章 前端／後端協定

**目錄**

- [54.1. 概觀](protocol-overview.md)
  - [54.1.1. 訊息傳遞概觀](protocol-overview.md#protocol-message-concepts)

  - [54.1.2. 延伸查詢概觀](protocol-overview.md#protocol-query-concepts)

  - [54.1.3. 格式與格式代碼](protocol-overview.md#protocol-format-codes)

  - [54.1.4. 協定版本](protocol-overview.md#protocol-versions)

- [54.2. 訊息流程](protocol-flow.md)
  - [54.2.1. 啟動](protocol-flow.md#protocol-flow-start-up)

  - [54.2.2. 簡單查詢](protocol-flow.md#protocol-flow-simple-query)

  - [54.2.3. 延伸查詢](protocol-flow.md#protocol-flow-ext-query)

  - [54.2.4. 管線化](protocol-flow.md#protocol-flow-pipelining)

  - [54.2.5. 函式呼叫](protocol-flow.md#protocol-flow-function-call)

  - [54.2.6. COPY 操作](protocol-flow.md#protocol-copy)

  - [54.2.7. 非同步操作](protocol-flow.md#protocol-async)

  - [54.2.8. 取消進行中的請求](protocol-flow.md#protocol-flow-canceling-requests)

  - [54.2.9. 終止](protocol-flow.md#protocol-flow-termination)

  - [54.2.10. SSL 工作階段加密](protocol-flow.md#protocol-flow-ssl)

  - [54.2.11. GSSAPI 工作階段加密](protocol-flow.md#protocol-flow-gssapi)

- [54.3. SASL 認證](sasl-authentication.md)
  - [54.3.1. SCRAM-SHA-256 認證](sasl-authentication.md#sasl-scram-sha-256)

  - [54.3.2. OAUTHBEARER 認證](sasl-authentication.md#sasl-oauthbearer)

- [54.4. 串流複寫協定](protocol-replication.md)

- [54.5. 邏輯串流複寫協定](protocol-logical-replication.md)
  - [54.5.1. 邏輯串流複寫參數](protocol-logical-replication.md#protocol-logical-replication-params)

  - [54.5.2. 邏輯複寫協定訊息](protocol-logical-replication.md#protocol-logical-messages)

  - [54.5.3. 邏輯複寫協定訊息流程](protocol-logical-replication.md#protocol-logical-messages-flow)

- [54.6. 訊息資料型別](protocol-message-types.md)

- [54.7. 訊息格式](protocol-message-formats.md)

- [54.8. 錯誤與通知訊息欄位](protocol-error-fields.md)

- [54.9. 邏輯複寫訊息格式](protocol-logicalrep-message-formats.md)

- [54.10. 自協定 2.0 以來的變更摘要](protocol-changes.md)

<a id="id-1.10.6.2"></a>

PostgreSQL 使用以訊息為基礎的協定，在前端與後端（用戶端與伺服器）之間進行通訊。此協定可透過 TCP/IP 使用，也可透過 Unix 網域通訊端使用。連接埠號碼 5432 已向 IANA 註冊，作為支援此協定之伺服器的慣用 TCP 連接埠號碼，但實務上可以使用任何非特權連接埠號碼。

本文件說明此協定的 3.2 版，此版本於 PostgreSQL 18 版引入。伺服器與 libpq 用戶端函式庫向後相容於協定 3.0 版，後者實作於 PostgreSQL 7.4 及之後的版本。

為了有效率地服務多個用戶端，伺服器會為每個用戶端啟動一個新的「後端」程序。在目前的實作中，偵測到有連入的連線後，就會立即建立一個新的子程序。不過，這對協定而言是透明的。就協定而言，「後端」與「伺服器」這兩個詞可以互換；同樣地，「前端」與「用戶端」也可以互換。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol.html)（原文版本：18.6；核對日期：2026-10-12）
