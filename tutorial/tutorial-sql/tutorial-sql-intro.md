<a id="TUTORIAL-SQL-INTRO"></a>

## 2.1. 簡介 [#](#TUTORIAL-SQL-INTRO)

本章概要說明如何使用 SQL 執行簡單的操作。本教學只是入門介紹，絕非完整的 SQL 教學。坊間已有許多關於 SQL 的書籍，包括 [[melt93]](../../bibliography.md#MELT93) 與 [[date97]](../../bibliography.md#DATE97)。請注意，PostgreSQL 的部分語言功能是標準的延伸。

在接下來的範例中，我們假設你已如上一章所述建立名為 `mydb` 的資料庫，並且能夠啟動 psql。

本手冊中的範例也可以在 PostgreSQL 原始碼發行版本的 `src/tutorial/` 目錄中找到。（PostgreSQL 的二進位發行版本可能不提供這些檔案。）要使用這些檔案，請先切換到該目錄並執行 make：

```

$ cd .../src/tutorial
$ make
```

這會建立腳本，並編譯包含使用者自訂函式與型別的 C 檔案。接著，依下列方式開始教學：

```

$ psql -s mydb

...

mydb=> \i basics.sql
```

`\i` 指令會從指定的檔案讀入指令。`psql` 的 `-s` 選項會讓你進入單步模式，在每個陳述式送往伺服器之前暫停。本節使用的指令都在 `basics.sql` 檔案中。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-sql-intro.html)（原文版本：18.6；核對日期：2026-09-11）
