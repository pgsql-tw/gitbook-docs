# 52.2. How Connections Are Established

PostgreSQL採用了一種“每個使用者一個程序”的客戶端/伺服器模型。在這種模型中，每個客戶端程序(client process)只連接到一個後端程序(backend process)。由於我們事先不知道會有多少連線，所以我們必須使用一個「監督程序」，每次收到連線請求時，它就產生一個新的後端程序。這個監督程序叫做postmaster，它在指定的 TCP/IP 連線埠上監聽傳入的連線。每當它檢測到一個連線請求，它就產生一個新的後端程序。這些後端程序之間以及與實例(instance)的其他程序使用 _semaphores_ 和共享記憶體來溝通，以確保在同時間進行資料存取中的資料完整性

客戶端程序可以是任何理解 PostgreSQL 協定的程式，該協定說明在[第 55 章](../52.-frontend-backend-protocol/)中。許多客戶端是基於 C 語言函式庫 libpq，但也有一些是獨立實作該協定的程式，例如 Java 的 JDBC 驅動程式。

Once a connection is established, the client process can send a query to the backend process it's connected to. The query is transmitted using plain text, i.e., there is no parsing done in the client. The backend process parses the query, creates an _execution plan_, executes the plan, and returns the retrieved rows to the client by transmitting them over the established connection.
