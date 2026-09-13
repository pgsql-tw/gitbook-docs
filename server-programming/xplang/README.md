## 第 40 章 程序語言

**目錄**

[40.1. 安裝程序語言](xplang-install.md)

<a id="id-1.8.7.2"></a>

PostgreSQL 允許使用者定義的函式以 SQL 與 C 以外的其他語言撰寫。這些其他語言統稱為*程序語言*（procedural languages，PLs）。對於以程序語言撰寫的函式，資料庫伺服器並沒有內建關於如何解讀該函式原始碼文字的知識，而是把這項工作交給一個了解該語言細節的特殊處理常式。這個處理常式可以自行完成剖析、語法分析、執行等所有工作，也可以作為 PostgreSQL 與某個既有程式語言實作之間的「膠水」。處理常式本身是一個以 C 語言撰寫的函式，編譯成共用物件並依需要載入，就和其他任何 C 函式一樣。

PostgreSQL 標準發行版目前提供四種程序語言：PL/pgSQL（[第 41 章](../plpgsql/README.md)）、PL/Tcl（[第 42 章](../pltcl/README.md)）、PL/Perl（[第 43 章](../plperl/README.md)）與 PL/Python（[第 44 章](../plpython/README.md)）。另外還有一些未包含在核心發行版中的程序語言可供使用，[附錄 H](../../appendixes/external-projects/README.md) 有如何找到它們的資訊。此外，使用者也可以自行定義其他語言；開發新程序語言的基礎知識涵蓋於[第 57 章](../../internals/plhandler/README.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xplang.html)（原文版本：18.6；核對日期：2026-09-13）
