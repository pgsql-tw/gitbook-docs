# 8.18. Domain Types

Domain 是基於另一個基本型別的使用者定義資料型別。可以選擇性將其有效值限制為基本型別的子集。否則，它的行為類似於基本型別 — 例如，可以應用於基本型別的任何運算子或函數都將在 domain 型別上以相同的行為運作。基本型別可以是任何內建或其他使用者定義的基本型別、列舉型別、陣列型別、複合型別、範圍型別或其他的 domain。

例如，我們可以整數型別上建立一個 domain，其僅接受正數：

```
CREATE DOMAIN posint AS integer CHECK (VALUE > 0);
CREATE TABLE mytable (id posint);
INSERT INTO mytable VALUES(1);   -- works
INSERT INTO mytable VALUES(-1);  -- fails
```

當基本型別的運算子或函數運作於 domain 的值時，該 domain 會自動向下轉換為基本型別。因此，例如，mytable.id - 1 的結果被認為是整數型別而不是 posint 型別。 我們可以使用 (mytable.id - 1)::posint 將結果轉換回 posint，使其重新檢查 domain 的條件。在這種情況下，如果將表示式於 ID 值 1 做運算，則會產生錯誤。可以在不明確寫出強制型別轉換的情況下，將基本型別的值寫入到 domain 型別的欄位或變數，但是將會檢查該 domain 的限制條件。

有關更多資訊，請參閱 [CREATE DOMAIN](../../reference/sql-commands/create-domain.md)。
