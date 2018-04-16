# 5.1. 認識資料表

「資料表」（table）在關連式資料庫中的角色很接近在紙上畫一個「資料表」：包含了列與欄。欄的數量與次序是固定的，而每個欄位都有一個名稱。列的數量是變動的—它表示在當下有多少資料被存在資料庫中。SQL 並不保證列在資料表中的次序。當讀取資料表的時候，除非明確要求要排序，不然列與列之間是不存在固定的次序。這些將在[第 7 章](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/queries.md)中進一步說明。進一步來說，SQL 並沒有給每一列一個唯一性的識別，所以在資料表中是有可能存在有完全相同內容的列。這是 SQL 架構下的數學模型結果，通常不是理想的結果。在這章之後，我們會說明如何處理這個問題。

每一個欄位都有一個資料型別。資料型別限制了儲存於該欄位的資料內容，同時也設定了資料儲存的型態，使得該資料可以直接用於計算。舉個例子，一個被宣告為數字型別的欄位，就不能放進任何文字字串，而儲存於此欄位中的資料，可用於數學計算。相反地，一個被宣告為字元字串的欄位，可以儲存任何型能的資料，但就無法用於數學計算了，雖然也有其他操作可以進行字串串接。

PostgreSQL 擁有許多內建的資料型別，可以適應許多應用系統。使用者也可以自訂他們所需的資料型別。大多數內建的資料型別都有顯而易見的名稱與用法，所以我們打算在[第 8 章](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/data-types.md)再做詳細的說明。有一些常用的資料型別，像是 interger 用於整數，numeric 用於浮點數，text 用於字串，date 則是日期，time 是時間，而 timestamp 則同時包含日期和時間。

要建立一個資料表，你可以使用 [CREATE TABLE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-table.md) 指令。這個指令你至少要指定一個名稱給新的資料表，還有每一個欄位的名稱與資料型別。例如：

```text
CREATE TABLE my_first_table (
    first_column text,
    second_column integer
);
```

這個建立一個叫作 my\_first\_table 的資料表，它包含了兩個欄位。第一個欄位叫作 first\_column，其資料型別為 text；第二個欄位名稱為 second\_column，資料型別為 integer。表格與欄位名稱的規則依 [4.1.1 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/sql-syntax/41-lexical-structure.md)中所介紹的識別字語法，但也有一些例外。注意欄位列表是用逗號分隔，並且包含於括號之中。

當然，前面的例子明顯只是做做樣子而已。一般來說，你會將你的資料表欄位以實際用途來命名，所以我們來看一下更實際的例子：

```text
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);
```

（numeric 資料型別可以儲存浮點數，用於典型的貨幣計量。）

> ## 小技巧
>
> 當你建立了許多相關的資料表時，建立最好選擇一個用於命名表格及欄位的規則。舉例來說，有一個規則是使用單數或複數名詞來取名表格，兩者都有些人喜歡使用。

一個資料表中有多少欄位是有限制的，依欄位型別而定，上限通常是 250 個到 1600 個之間。不過，宣告到這麼多的欄位是非常罕見，而且應該是有問題的設定。

如果你不再需要某個資料表，你可以移除它。請使用 [DROP TABLE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/drop-table.md) 指令，如下所示：

```text
DROP TABLE my_first_table;
DROP TABLE products;
```

企圖要移除一個不存在的資料表，會產生錯誤。不過，在 SQL 腳本中，在建立資料表前嘗試移除是很常見的，通常會忽略錯誤訊息，所以不論資料表是否已經存在，腳本都能如預期執行。（如果你需要的話，你也可以使用 DROP TABLE IF EXISTS 來避免產生錯誤訊息，但這並不是標準 SQL 語法。）

如果你需要變更資料表的結構的話，請參閱本章的 [5.5 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/data-definition/55-modifying-tables.md)。

到目前為止，你已經可以利用工具建立完整功能的資料表。本章接下來的部份會針對附加的功能介紹，像是確保資料完整性、安全性、或方便性。如果你現在急著要將資料存入你的資料表的話，你可以暫時跳過本章，到[第 6 章](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/data-manipulation.md)繼續操作。

