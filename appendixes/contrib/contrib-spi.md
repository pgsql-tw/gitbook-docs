## F.41. spi — Server Programming Interface 功能與範例 [#](#CONTRIB-SPI)

[F.41.1. refint — 實作參考完整性的函式](contrib-spi.md#CONTRIB-SPI-REFINT)

[F.41.2. autoinc — 自動遞增欄位的函式](contrib-spi.md#CONTRIB-SPI-AUTOINC)

[F.41.3. insert_username — 追蹤誰變更資料表的函式](contrib-spi.md#CONTRIB-SPI-INSERT-USERNAME)

[F.41.4. moddatetime — 追蹤最後修改時間的函式](contrib-spi.md#CONTRIB-SPI-MODDATETIME)

<a id="id-1.11.7.51.2"></a>

spi 模組提供數個使用 [Server Programming Interface](../../server-programming/spi/README.md)
（SPI）及觸發程序的可行範例。這些函式本身雖有一些價值，但作為可依你自身
目的修改的範例更為實用。這些函式足夠通用，可搭配任何資料表使用；但建立
觸發程序時，必須指定資料表及欄位名稱（如下所述）。

下列每一組函式都作為可個別安裝的擴充功能提供。

<a id="CONTRIB-SPI-REFINT"></a>

### F.41.1. refint — 實作參考完整性的函式 [#](#CONTRIB-SPI-REFINT)

`check_primary_key()` 和 `check_foreign_key()` 用於檢查外部索引鍵限制條件。
（此功能早已由內建的外部索引鍵機制取代，但此模組仍可作為範例使用。此模組
將在 PostgreSQL 20 移除。）

### 注意事項

`refint` 需要[安全的 schema 使用模式](../../the-sql-language/ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS)，
以及等號運算子名稱為 `=` 的資料型別。

`check_primary_key()` 檢查參照資料表。若要使用，請在參照另一個資料表的
資料表上，使用此函式建立 `AFTER INSERT OR UPDATE` 觸發程序。觸發程序引數
應指定：組成外部索引鍵的參照資料表欄位名稱、被參照資料表名稱，以及被參照
資料表中組成主鍵／唯一值索引鍵的欄位名稱。若要處理多個外部索引鍵，請為每個
參照建立一個觸發程序。

### 注意事項

傳給 `check_primary_key()` 的*被參照*資料表名稱與欄位名稱引數，會原樣複製
至內部產生的 SQL 陳述式，因此使用者必須視需要在 `CREATE TRIGGER` 命令中
以雙引號引住它們。SQL 識別字的引號詳情請參閱[第 4.1.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS)。
相反地，*參照*資料表的欄位名稱引數不應以雙引號引住。下列為正確使用
`check_primary_key()` 的模擬範例：

```

CREATE TRIGGER mytrigger
AFTER INSERT OR UPDATE ON referencing_table
FOR EACH ROW EXECUTE PROCEDURE
check_primary_key (
    'column A', 'column B',         -- referencing table columns
    'myschema."referenced table"',  -- referenced table
    '"column A"', '"column B"'      -- referenced table columns
);
```

`check_foreign_key()` 檢查被參照資料表。若要使用，請在被其他資料表參照的
資料表上，使用此函式建立 `AFTER DELETE OR UPDATE` 觸發程序。觸發程序引數
應指定：函式必須檢查的參照資料表數目、找到參照索引鍵時採取的動作
（`cascade` — 刪除參照資料列、`restrict` — 若有參照索引鍵則中止交易、
`setnull` — 將參照索引鍵欄位設為 null）、組成主鍵／唯一值索引鍵的被參照
資料表欄位名稱，接著是參照資料表名稱與欄位名稱（依第一個引數指定的參照
資料表數目重複）。請注意，主鍵／唯一值索引鍵欄位應標記為 NOT NULL，且應
具有唯一值索引。

### 注意事項

傳給 `check_foreign_key()` 的*參照*資料表名稱與欄位名稱引數，會原樣複製至
內部產生的 SQL 陳述式，因此使用者必須視需要在 `CREATE TRIGGER` 命令中以
雙引號引住它們。SQL 識別字的引號詳情請參閱[第 4.1.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS)。
相反地，*被參照*資料表的欄位名稱引數不應以雙引號引住。下列為正確使用
`check_foreign_key()` 的模擬範例：

```

CREATE TRIGGER mytrigger
AFTER DELETE OR UPDATE ON referenced_table
FOR EACH ROW EXECUTE PROCEDURE
check_foreign_key (
    1,                              -- number of referencing tables
    'cascade',                      -- action
    'column A', 'column B',         -- referenced table columns
    'myschema."referencing table"', -- referencing table
    '"column A"', '"column B"'      -- referencing table columns
);
```

請注意，若這些觸發程序由另一個 `BEFORE` 觸發程序執行，可能會意外失敗。
例如，使用者插入 row1，然後 `BEFORE` 觸發程序插入 row2 並呼叫具有
`check_foreign_key()` 的觸發程序時，`check_foreign_key()` 函式看不到 row1，
因而失敗。

`refint.example` 中有範例。

<a id="CONTRIB-SPI-AUTOINC"></a>

### F.41.2. autoinc — 自動遞增欄位的函式 [#](#CONTRIB-SPI-AUTOINC)

`autoinc()` 是將序列的下一個值儲存至整數欄位的觸發程序。此功能與內建的
「serial 欄位」功能有一些重疊，但並不相同。此觸發程序僅在欄位的初始值為
零或 null 時（插入或更新資料列的 SQL 陳述式動作之後）才會取代該欄位值。
此外，若序列的下一個值為零，會第二次呼叫 `nextval()` 以取得非零值。

若要使用，請以此函式建立 `BEFORE INSERT`（或可選擇的 `BEFORE INSERT OR UPDATE`）
觸發程序。指定兩個觸發程序引數：要修改的整數欄位名稱，以及提供值的序列
物件名稱。（實際上，若要更新多個自動遞增欄位，你可以指定任意數量的這類
名稱配對。）

`autoinc.example` 中有範例。

<a id="CONTRIB-SPI-INSERT-USERNAME"></a>

### F.41.3. insert_username — 追蹤誰變更資料表的函式 [#](#CONTRIB-SPI-INSERT-USERNAME)

`insert_username()` 是將目前使用者名稱儲存至 text 欄位的觸發程序。這可用於
追蹤誰最後修改資料表中的特定資料列。

若要使用，請以此函式建立 `BEFORE INSERT` 及／或 `UPDATE` 觸發程序。指定
一個觸發程序引數：要修改的 text 欄位名稱。

`insert_username.example` 中有範例。

<a id="CONTRIB-SPI-MODDATETIME"></a>

### F.41.4. moddatetime — 追蹤最後修改時間的函式 [#](#CONTRIB-SPI-MODDATETIME)

`moddatetime()` 是將目前時間儲存至 `timestamp` 欄位的觸發程序。這可用於
追蹤資料表中某一資料列的最後修改時間。

若要使用，請以此函式建立 `BEFORE UPDATE` 觸發程序。指定一個觸發程序引數：
要修改的欄位名稱。該欄位必須為 `timestamp` 或 `timestamp with time zone` 型別。

`moddatetime.example` 中有範例。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-spi.html)
