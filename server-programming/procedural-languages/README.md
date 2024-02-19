# 42. Procedural Languages（程序語言）

PostgreSQL 可以讓使用者自行定義的函數除了 SQL 和 C 之外還能用其他語言編寫。這些其他語言通常稱為程序語言（PL）。對於用程序語言編寫的函數，資料庫伺服器並沒有關於如何解釋函數原始程式碼的能力。所以相關的任務會被傳遞給一個瞭解語言細節的特殊處理程序來處理。處理程序可以自己完成內容過濾，語法分析，程序執行等所有工作，也可以作為 PostgreSQL 與現有程序語言實作之間的「粘合劑」。處理程序本身是一個 C 語言函數，編譯成一個共享物件並按需要載入，就像任何其他 C 函數一樣。

目前標準的 PostgreSQL 發行版中有四種可用的程序語言：PL/pgSQL（[第 43 章](../pl-pgsql-sql-procedural-language/)），PL/Tcl（[第 44 章](../pl-tcl-tcl-procedural-language.md)），PL/Perl（[第 45 章](../pl-python-python-procedural-language-1/)）和 PL/Python（[第 46 章](https://github.com/pgsql-tw/gitbook-docs/blob/master/tw/server-programming/procedural-languages/broken-reference/README.md)）。 還有其他可用的程序語言未包含在主要發行版中。[附錄 H](https://github.com/pgsql-tw/gitbook-docs/tree/67cc71691219133f37b9a33df9c691a2dd9c2642/tw/appendixes/h.-wai-bu-zhuan-an) 包含相關的其他訊息。此外，使用者可以定義其他語言；[第 58 章](../../internals/writing-a-procedural-language-handler.md)介紹了開發新程序語言的基礎知識。
