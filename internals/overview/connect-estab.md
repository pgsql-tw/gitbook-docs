<a id="CONNECT-ESTAB"></a>

## 51.2. 如何建立連線 [#](#connect-estab) <a href="#connect-estab" id="connect-estab"></a>

PostgreSQL 實作的是「每個使用者一個程序」的用戶端／伺服器模型。在這個模型中，每個[*用戶端程序*](../../appendixes/glossary/README.md#glossary-client)都恰好連線到一個[*後端程序*](../../appendixes/glossary/README.md#glossary-backend)。由於我們無法事先知道會建立多少個連線，因此必須使用一個「監督程序」，在每次有連線請求時產生一個新的後端程序。這個監督程序稱為 [*postmaster*](../../appendixes/glossary/README.md#glossary-postmaster)，它會在指定的 TCP/IP 通訊埠上監聽傳入的連線。每當偵測到連線請求時，它就會產生一個新的後端程序。這些後端程序彼此之間，以及與[*執行個體*](../../appendixes/glossary/README.md#glossary-instance)的其他程序之間，會使用<em>號誌（semaphore）</em>與[*共享記憶體*](../../appendixes/glossary/README.md#glossary-shared-memory)進行通訊，以確保並行存取資料時的資料完整性。

用戶端程序可以是任何理解[第 54 章](../protocol/README.md)所述 PostgreSQL 協定的程式。許多用戶端是以 C 語言函式庫 libpq 為基礎，但也有數個獨立的協定實作，例如 Java JDBC 驅動程式。

連線建立之後，用戶端程序就可以將查詢傳送給它所連線的後端程序。查詢是以純文字傳輸，也就是說，用戶端不會進行任何剖析。後端程序會剖析查詢、建立*執行計畫*、執行該計畫，並透過已建立的連線將取得的資料列傳回給用戶端。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/connect-estab.html)（原文版本：18.6；核對日期：2026-10-12）
