# 27. 監控資料庫活動

資料庫管理員經常會想：「系統現在正在做什麼？」本章討論如何回答這個問題。

有幾種工具可用於監控資料庫活動和分析效能。本章的大部分內容都致力於描述 PostgreSQL 的統計收集器，但不應忽視普通的 Unix 監控程序，如 ps、top、iostat 和 vmstat。而且，一旦發現查詢效率不佳，可能需要使用 PostgreSQL 的 [EXPLAIN](../../reference/sql-commands/explain.md) 指令進一步調查。[第 14.1 節](../../the-sql-language/performance-tips/using-explain.md)討論了 EXPLAIN 和其他方法來解析單個查詢的行為。

