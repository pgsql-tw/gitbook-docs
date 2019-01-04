# 5.13. 相依性追蹤

當你建立了一個複雜的資料庫結構，包含了許多資料表，也設計了許多外部索引鍵、檢視表、觸發事件、函數.....等等。也就是說，其實你建立了一堆物件之間的關連性。舉例來說，資料表的外部索引鍵就與另一個資料表有著參考的關連性。

要維護整個資料庫結構的完整性，PostgreSQL 得確保你不能在有關連性的情況下，隨意刪去物件。舉例來說，企圖刪去在 [5.3.5 節](constraints.md#5-3-5-wai-bu-foreign-keys)中，我們所使用過的產品資料表，而訂單資料表與其有相依的關連性，那就會產生如下的錯誤訊息：

```text
DROP TABLE products;

ERROR:  cannot drop table products because other objects depend on it
DETAIL:  constraint orders_product_no_fkey on table orders depends on table products
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

這個錯誤訊息包含了很有用的指引：如果你不想要一個個處理其相依關連性，那可以一次刪去他們：

```text
DROP TABLE products CASCADE;
```

如此所有相依的物件就會被刪除了，所有相互依存的物件都會，是遞迴式的處理流程。在這個例子中，它不會移除訂單資料表，只會移除外部索引鍵的限制條件，因為沒有其他物件與該外部索引鍵相依。（如果你要確認 DROP ... CASCADE 會處理哪些物件，你可以用 **DETAIL** 取代 CASCADE，就會輸出其相依的物件。）

幾乎所有 PostgreSQL 的 DROP 指令都支援 CASCADE 的用法。當然，有些自然的關連性是和物件型別有關。你也可以使用 RESTRICT 來取代 CASCADE 的位置，以強制以預設的行為來處理，也就是絕對不會刪去其他相關的物件。

## 注意

根據 SQL 標準，不論是 RESTRICT 或 CASCADE，都必須要在 DROP 指令中明確表示，但沒有任何一套資料庫系統真的這樣設計。不過，都會內定預設行為是 RESTRICT 或 CASCADE，每個資料庫不同。

如果 DROP 指令列出了多個物件，CASCADE 只有在這些物件之外還有相依性時才會需要。舉個例子，當執行「DROP TABLE tab1, tab2」時，即使 tab1 與 tab2 之間有外部索引鍵的相依關係，而沒有指定 CASCADE，這個操作也會完成。

對於使用者自訂的函數來說，PostgreSQL 會引用函數的外顯屬性來判斷其相依性，例如函數的參數或輸出型態，但函數內部執行的相依關係就無法追蹤了。舉個列子：

```text
CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow',
                             'green', 'blue', 'purple');

CREATE TABLE my_colors (color rainbow, note text);

CREATE FUNCTION get_color_note (rainbow) RETURNS text AS
  'SELECT note FROM my_colors WHERE color = $1'
  LANGUAGE SQL;
```

（參閱 [37.4 節](../../server-programming/extending-sql/user-defined-procedures.md)，瞭解 SQL 語言的函數。）PostgreSQL 會知道 get\_color\_note 函數相依於 rainbow 資料型別：也就是刪去該資料型別時，也會強制要刪去該函數，因為它的參數將不再合法。但 PostgreSQL 就無法發現 get\_color\_note 和 my\_colors 之間的關連性，當該資料表被移除時，此函數並不會跟著被移除。這種情況有好有壞，函數基本上還是合法的，即使內含的資料表不存在的話，頂多就是執行會出錯就是了，只要再建立該名稱的資料表就可以讓這個函數重新正常運作。

