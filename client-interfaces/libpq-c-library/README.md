# 34. libpq - C Library

libpq 是 C 應用程式設計師對 PostgreSQL 的介面。libpq 是一組函式庫，提供用戶端程序可以將查詢傳遞給 PostgreSQL 後端伺務器並接收這些查詢的結果。

libpq 也是其他幾個 PostgreSQL 應用程序接口的底層引擎，包括為 C++、Perl、Python、Tcl 和 ECPG 程式的介面。因此，如果您使用其中一個軟體套件，libpq 行為的某些方面對您很重要。特別是，[第 33.14 節](environment-variables.md)，[第 33.15 節](libpq-pgpass.md)和[第 33.18 節](33.18.-ssl-support.md)描述了使用 libpq 應用程式的用戶可見行為。

本章末尾包含一些簡短的程式（[第 33.21 節](example-programs.md)），以展示如何撰寫使用 libpq 的程式。在原始碼的目錄 src/test/examples 中還有幾個完整的 libpq 應用程式範例。

使用 libpq 的用戶端程式必須包含標頭檔 libpq-fe.h，並且必須與 libpq 函式庫連接。
