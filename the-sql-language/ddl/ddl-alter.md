<a id="DDL-ALTER"></a>

## 5.7. 修改資料表 [#](#DDL-ALTER)

[5.7.1. 新增欄位](ddl-alter.md#DDL-ALTER-ADDING-A-COLUMN)

[5.7.2. 移除欄位](ddl-alter.md#DDL-ALTER-REMOVING-A-COLUMN)

[5.7.3. 新增限制條件](ddl-alter.md#DDL-ALTER-ADDING-A-CONSTRAINT)

[5.7.4. 移除限制條件](ddl-alter.md#DDL-ALTER-REMOVING-A-CONSTRAINT)

[5.7.5. 變更欄位的預設值](ddl-alter.md#DDL-ALTER-COLUMN-DEFAULT)

[5.7.6. 變更欄位的資料型別](ddl-alter.md#DDL-ALTER-COLUMN-TYPE)

[5.7.7. 重新命名欄位](ddl-alter.md#DDL-ALTER-RENAMING-COLUMN)

[5.7.8. 重新命名資料表](ddl-alter.md#DDL-ALTER-RENAMING-TABLE)

<a id="id-1.5.4.9.2"></a>

當你建立了一個資料表，卻發現自己犯了錯，或是應用程式的需求改變了，你可以把這個資料表移除再重新建立。但如果資料表中已經填滿了資料，或者這個資料表被其他資料庫物件所參照（例如外鍵限制條件），這就不是個方便的選擇了。因此，PostgreSQL 提供了一系列的指令來修改既有的資料表。請注意，這在概念上與變更資料表中所含的資料是不同的：這裡我們關注的是變更資料表的定義，也就是它的結構。

你可以：

* 新增欄位
* 移除欄位
* 新增限制條件
* 移除限制條件
* 變更預設值
* 變更欄位資料型別
* 重新命名欄位
* 重新命名資料表

所有這些動作都是使用 [ALTER TABLE](../../reference/sql-commands/sql-altertable.md) 指令來完成的，該指令的參考頁面包含了比這裡所述更詳盡的細節。

<a id="DDL-ALTER-ADDING-A-COLUMN"></a>

### 5.7.1. 新增欄位 [#](#DDL-ALTER-ADDING-A-COLUMN)

<a id="id-1.5.4.9.5.2"></a>

要新增欄位，請使用像這樣的指令：

```

ALTER TABLE products ADD COLUMN description text;
```

新欄位一開始會填入所給定的預設值（如果你沒有指定 `DEFAULT` 子句，就是 NULL）。

### 提示

以常數預設值新增欄位時，並不需要在執行 `ALTER TABLE` 陳述式時更新資料表的每一筆資料列。取而代之的是，下次存取該資料列時才會回傳這個預設值，並在資料表被重寫時才實際套用，這使得 `ALTER TABLE` 即使在大型資料表上也非常快速。

如果預設值是易變的（例如 `clock_timestamp()`），那麼每一筆資料列都需要以執行 `ALTER TABLE` 當時所計算出的值來更新。為了避免可能耗時很久的更新作業，尤其是當你本來就打算在該欄位中填入大多為非預設值的資料時，比較好的做法或許是先不帶預設值新增欄位，使用 `UPDATE` 填入正確的值，然後再依照下面所述加入你想要的預設值。

你也可以同時使用一般的語法，為該欄位定義限制條件：

```

ALTER TABLE products ADD COLUMN description text CHECK (description <> '');
```

事實上，所有能夠套用在 `CREATE TABLE` 欄位描述中的選項，在這裡都可以使用。不過請記住，預設值必須滿足所給定的限制條件，否則 `ADD` 會失敗。或者，你也可以在正確地填好新欄位之後，稍後再加入限制條件（見下文）。

<a id="DDL-ALTER-REMOVING-A-COLUMN"></a>

### 5.7.2. 移除欄位 [#](#DDL-ALTER-REMOVING-A-COLUMN)

<a id="id-1.5.4.9.6.2"></a>

要移除欄位，請使用像這樣的指令：

```

ALTER TABLE products DROP COLUMN description;
```

該欄位中原本的資料都會消失。牽涉到這個欄位的資料表限制條件也會被移除。不過，如果這個欄位被另一個資料表的外鍵限制條件所參照，PostgreSQL 不會默默地移除該限制條件。你可以加上 `CASCADE` 來授權移除所有相依於這個欄位的東西：

```

ALTER TABLE products DROP COLUMN description CASCADE;
```

這背後的一般性機制說明，請參閱[第 5.15 節](ddl-depend.md)。

<a id="DDL-ALTER-ADDING-A-CONSTRAINT"></a>

### 5.7.3. 新增限制條件 [#](#DDL-ALTER-ADDING-A-CONSTRAINT)

<a id="id-1.5.4.9.7.2"></a>

要新增限制條件，要使用資料表限制條件的語法。例如：

```

ALTER TABLE products ADD CHECK (name <> '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
```

若要新增非空值限制條件（它通常不會寫成資料表限制條件），可以使用這個特別的語法：

```

ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

如果該欄位已經有非空值限制條件，這個指令會默默地不做任何事。

限制條件會立刻被檢查，因此資料表中的資料必須先滿足該限制條件，才能加入這個限制條件。

<a id="DDL-ALTER-REMOVING-A-CONSTRAINT"></a>

### 5.7.4. 移除限制條件 [#](#DDL-ALTER-REMOVING-A-CONSTRAINT)

<a id="id-1.5.4.9.8.2"></a>

要移除限制條件，你必須知道它的名稱。如果你當初有為它命名，那就很容易。否則系統會指派一個自動產生的名稱，而你必須把它找出來。psql 指令 `\d tablename` 在這裡會很有幫助；其他介面可能也提供了檢視資料表細節的方法。接著指令是：

```

ALTER TABLE products DROP CONSTRAINT some_name;
```

就像移除欄位一樣，如果你要移除的限制條件有其他東西相依於它，你就需要加上 `CASCADE`。舉例來說，外鍵限制條件會相依於被參照欄位上的唯一或主鍵限制條件。

移除非空值限制條件有簡化的語法可以使用：

```

ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

這對應於新增非空值限制條件所用的 `SET NOT NULL` 語法。如果該欄位並沒有非空值限制條件，這個指令會默默地不做任何事。（請回想一下，一個欄位最多只能有一個非空值限制條件，因此這個指令要作用在哪一個限制條件上絕不會有歧義。）

<a id="DDL-ALTER-COLUMN-DEFAULT"></a>

### 5.7.5. 變更欄位的預設值 [#](#DDL-ALTER-COLUMN-DEFAULT)

<a id="id-1.5.4.9.9.2"></a>

要為欄位設定新的預設值，請使用像這樣的指令：

```

ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

請注意，這並不會影響資料表中任何既有的資料列，它只是改變了後續 `INSERT` 指令所使用的預設值。

要移除任何預設值，請使用：

```

ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

這實際上與把預設值設為 NULL 是一樣的。因此，對一個本來就沒有定義預設值的欄位移除預設值並不會產生錯誤，因為它的預設值隱含就是空值。

<a id="DDL-ALTER-COLUMN-TYPE"></a>

### 5.7.6. 變更欄位的資料型別 [#](#DDL-ALTER-COLUMN-TYPE)

<a id="id-1.5.4.9.10.2"></a>

要把欄位轉換成不同的資料型別，請使用像這樣的指令：

```

ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

只有在該欄位中每一筆既有的項目都能藉由隱含的型別轉換轉成新型別時，這才會成功。如果需要更複雜的轉換，你可以加上 `USING` 子句，指定如何從舊值計算出新值。

PostgreSQL 會嘗試把該欄位的預設值（如果有的話）以及所有牽涉到這個欄位的限制條件一併轉換成新型別。但這些轉換可能會失敗，或者產生令人意外的結果。通常最好的做法是在變更欄位型別之前先移除該欄位上的所有限制條件，然後在之後再加回經過適當修改的限制條件。

<a id="DDL-ALTER-RENAMING-COLUMN"></a>

### 5.7.7. 重新命名欄位 [#](#DDL-ALTER-RENAMING-COLUMN)

<a id="id-1.5.4.9.11.2"></a>

要重新命名欄位：

```

ALTER TABLE products RENAME COLUMN product_no TO product_number;
```

<a id="DDL-ALTER-RENAMING-TABLE"></a>

### 5.7.8. 重新命名資料表 [#](#DDL-ALTER-RENAMING-TABLE)

<a id="id-1.5.4.9.12.2"></a>

要重新命名資料表：

```

ALTER TABLE products RENAME TO items;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-alter.html)（原文版本：18.6；核對日期：2026-09-13）
