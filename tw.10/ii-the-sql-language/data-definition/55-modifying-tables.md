# 5.5. 表格變更[^1]

當你建立了一個表格，而你發現出了點錯，或者應用需求有一些改變，那麼你可以移除它再重新建立。但這可能不會一個好的選擇，當表格中已經儲存了許多資料時，或者表格正在被其他的資料庫物件所參考中（例如外部鍵參考）。所以 PostgreSQL 提供了一系列的指令來修改現存的表格。注意到這和更新表格內資料的概念是不同的：在這裡，我們主要針對的是調整表格的定義或結構。

你可以：

* 加入欄位
* 移除欄位
* 加入限制條件
* 移除限制條件
* 改變預設值
* 改變欄位資料型別
* 變更欄位名稱
* 變更表格名稱

所有這些動作都透過 [ALTER TABLE](/vi-reference/i-sql-commands/alter-table.md) 指令來進行，你可以參考該頁面取得詳細資訊。

### 5.5.1. 加入欄位

要加入一個新欄位，請使用下面的指令：

```
ALTER TABLE products ADD COLUMN description text;
```

這個新的欄位預設會以預設值填入（如果你沒有使用 DEFAULT 子句來宣告的話，那會使用 NULL）。

你也可以在新增同時建立限制條件：

```
ALTER TABLE products ADD COLUMN description text CHECK (description <> '');
```

事實上，所有在 CREATE TABLE 的選項都可以在這裡使用。要記得的是，預設值必須要符合限制條件的設定，否則這個欄位會無法加入。順帶一提的是，你也可以隨後再加入限制條件（隨後說明），在你更新好新的欄位資料內容後。

### 小技巧

> 加入一個欄位，並且設定預設值，會更新表格的裡的每一個資料列（為了存入新的欄位內容）。然而，無預設值的話，PostgreSQL 就不會在實體上真正進行更新的動行。所以如果你的新欄位大多數的內容都不是預設值的話，那麼就建議不要在加入欄位時設定預設值。之後再使用 UPDATE 來分別更新其內容，然後再以隨後的介紹來更新預設值的設定。

### 5.5.2. 移除欄位

要移除一個欄位，請使用下列指令：

```
ALTER TABLE products DROP COLUMN description;
```

不論資料在該欄位是否消滅，表格的限制條件都會同步再次啓動檢查。所以，如果欄位是被外部鍵所參考的話，PostgreSQL 不會就這樣移除它。你可以宣告同步刪去與此欄位相關的物件，加上 CASCADE：

```
ALTER TABLE products DROP COLUMN description CASCADE;
```

請參閱 [5.13 節](/ii-the-sql-language/data-definition/513-dependency-tracking.md)，瞭解詳細的處理機制。

### 5.5.3. 加入限制條件

要加入限制條件，請使用表格限制條件的語法，例如：

```
ALTER TABLE products ADD CHECK (name <> '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
```

要加入 NOT NULL 限制條件的話，就不能寫成表格的限制條件，請使用這樣的語法：

```
ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

加入的限制條件會立即開始檢查，所以當下的資料內容必須要能符合條件才能加入成功。

### 5.5.4. 移除限制條件

要移除限制條件，你需要先知道它的名稱。如果你在宣告時有命名的話，那就使用那個名稱，否則你得找出系統自動命名的名稱。其所使用的指令為「\d tablename」，會列出表格相關的資訊。或使用其他的資料庫工具應該也可以找到它。找到之後請使用下列指令來移除限制條件：

```
ALTER TABLE products DROP CONSTRAINT some_name;
```

（如果你的限制條件名稱像是「$2」這樣的，不要忘記使用雙引號括住，使其可以正確地被識別為是名稱。）

在移除欄位時，你需要加入 CASCADE，如果你需要同步移除相關的限制條件的話。像是外部鍵就會依賴另一個唯一性限制或主鍵的限制條件。

下面這可以用在移除 NOT NULL 限制的欄位：

```
ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

\(記得 NOT NULL 是沒有名稱的。\)

### 5.5.5. 變更欄位預設值

要設定新的欄位預設值，請使用下面指令：

```
ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

注意這並不會影響到已經存在的資料，只有隨後新增的資料才會使用。

要移除任何預設值，請使用：

```
ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

這個指令會把預設值設為空值。因為預設值本來就設為空值，所以即使刪去一個未設定預設值欄位的預設值，也不會是一種錯誤。

### 5.5.6. 變更欄位資料型別

要變更欄位成為另一個資料型別，請使用下列指令：

```
ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

這只有在欄位內容可以被自動轉換型別時才會成功。如果存在比較複雜的轉換時，你需要加上 USING 子句來指示如何轉換資料內容。

PostgreSQL 會企圖轉換欄位預設值到任何新的型別，而所有的限制條件也會啓動檢查機制。但這些轉換可能會失敗，也可以產生意外的結果。比較好的作法是，先移除限制條件，再變更資料型別，最後再重新加入適當調整後的限制條件。

### 5.5.7. 變更欄位名稱

要變更某個欄位的名稱：

```
ALTER TABLE products RENAME COLUMN product_no TO product_number;
```

### 5.5.8. 變更表格名稱

要變更表格的名稱：

```
ALTER TABLE products RENAME TO items;
```

---

[^1]: [PostgreSQL: Documentation: 10: 5.5. Modifying Tables](https://www.postgresql.org/docs/10/static/ddl-alter.html)

