# 2.1. 簡介

在這一章之中，提供了一個如何使用 SQL 進行簡易操作的大致概念。這裡主要讓你有基本的認識，但無法提供 SQL 完整且巨細靡遺的說明。許多書籍詳細介紹了 SQL，例如「Understanding the New SQL. A complete quide.」及「A Guide to the SQL Standard. A user's guid to the standard database language SQL.」。你應該瞭解的是，一些 PostgreSQL 語法來自於標準 SQL 的延伸。

在下面的例子當中，我們假設你已經建立了一個資料庫 mydb，如同前面章節所述，你也能夠使用 psql 了。

這些例子也放在 PostgreSQL 的原始碼之中，你可以在目錄 src/tutorial/ 下找到他們。（PostgreSQL的可執行套件可能未包含這些檔案）想要使用這些檔案的話，首先請切換到該目錄之下，然後執行 make：

```
$ cd ..../src/tutorial
$ make
```

這將會建立編譯 C 語言的程序，包含了使用者自訂的函式及型別。接下來，進行下列動作，以開始這個導覽：

```
$ cd ..../tutorial
$ psql -s mydb
...

mydb=> \i basics.sql
```

\i 指令會去指定的檔案讀取內容，並且執行。而在 psql 的 -s 選項則可以使用單步模式執行，也就是在每一個與伺服器互動的指令之後暫停。這個指令被使用在本節的檔案 basics.sql 之中。
