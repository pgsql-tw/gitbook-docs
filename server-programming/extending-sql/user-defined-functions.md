---
description: 版本：11
---

# 37.3. 使用者自訂函數

PostgreSQL 提供了四種形態的函數：

* 查詢語言函數（用 SQL 語言撰寫的函數）（[第 38.5 節](query-language-sql-functions.md)）
* 程序語言函數（例如，用 PL/pgSQL 或 PL/Tcl 撰寫的函數）（[第 38.8 節](procedural-language-functions.md)）
* 內部函數（[第 38.9 節](internal-functions.md)）
* C 語言函數（[第 38.10 節](c-language-functions.md)）

每種函數都可以將基本型別、複合類型或它們的組合型別作為參數。 另外，每種函數都可以回傳一個基本型別或一個複合型別。函數也可以定義為回傳基本或複合值的集合。

許多函數可以接受或回傳某些虛擬型別 pseudo type（如多態型別 polymorphic type），但可用的方式會有所不同。有關更多詳細訊息，請參閱各種函數的說明。

定義 SQL 函數最簡單，所以我們先討論這些。為 SQL 函數提供的大多數概念將轉入其他類型的函數。

在本章中，查看 [CREATE FUNCTION](../../reference/sql-commands/create-function.md) 指令的參考頁面可以更好地理解這些範例。本章中的一些範例可以在 PostgreSQL 原始碼發行版的 src/tutorial 目錄中的 funcs.sql 和 funcs.c 中找到。
