# 8.3. 字串型別

**Table 8.4. Character Types**

| Name | Description |
| :--- | :--- |
| `character varying(n)`, `varchar(n)` | 可變長度，但有限制 |
| `character(n)`, `char(n)` | 固定長度，空白填充 |
| `text` | 可變且無限長度 |

Table 8.4 列出了 PostgreSQL 中可用的通用字串型別。

SQL 定義了兩種主要字串型別：character varying\(n\) 和 character\(n\)，其中 n 是正整數。這兩種型別都可以儲存長度最多為 n 個字元（不是位元組）的字串。嘗試將較長的字串儲存到這些型別的欄位中將産生錯誤，除非多餘的字元都是空格，在這種情況下，字串將被截斷為最大長度。（這個有點奇怪的異常是 SQL 標準所要求的。）如果要儲存的字串比宣告的長度短，則 character 型別的值將被空格填充；character varying 的值將只儲存較短的字串。

如果明確地將值轉換為 character varying\(n\) 或 character\(n\)，則超長值將被截斷為 n 個字元而不會引發錯誤。（這也是 SQL 標準所要求的。）

型別 varchar\(n\) 和 char\(n\) 分別是 character varying\(n\) 和 character\(n\) 的別名。沒有長度的 character 等同於 character\(1\)。如果在沒有長度的情況下使用 character varying，則該型別接受任何長度的字串。後者是 PostgreSQL 延伸功能。

另外，PostgreSQL 提供了 text 型別，它儲存任意長度的字串。雖然型別 text 不在 SQL 標準中，但是其他幾個 SQL 資料庫管理系統也支援它。

character 的值用空格填充到指定的長度 n，並以這種方式儲存和顯示。但是，在比較兩個型別字串時，尾隨空格在語義上無關緊要會被忽略。在空格很重要的排序規則中，這種行為會產生意想不到的結果; 例如 `SELECT 'a '::CHAR(2) collate "C"<E'a\n'::CHAR(2)` 會回傳 true，即使 C 語言環境會認為空格大於換行符。將字串轉換為其他字串型別之一時，將刪除尾隨的空格。請注意，尾隨空格在 character varying 和 text 方面具有語義重要性，尤其在使用樣式匹配時，即 LIKE 和正規表示式。

短字串（126 個位元組以下）的儲存要求是 1 個位元組加上實際字串，其中包括字串空間填充。較長的字串有 4 個位元組的開銷而不是 1。長字串由系統自動壓縮，因此磁碟上的物理需求可能更少。非常長的值也儲存在後台的資料表中，這樣它們就不會干擾對較短欄位的快速存取。在任何情況下，可儲存的最長字串大約為 1 GB。（資料型別宣告中 n 允許的最大值小於此值。更改此值沒有用，因為使用多位元組字串編碼時，位元組數和字元數可能完全不同。如果您希望儲存沒有特定上限的長字串，使用不帶長度的 text 或 character varying，而不是隨便設定長度限制。）

#### 小提醒

這三種型別之間並沒有效能差異，除了使用空白填充類型時增加的儲存空間之外，以及一些額外的 CPU 週期來檢查儲存長度與欄位中的長度。雖然 character\(n\) 在其他一些資料庫系統中具有效能優勢，但 PostgreSQL 中並沒有這樣的優勢；事實上，由於額外的儲存成本，character\(n\) 通常是三者中最慢的。在大多數情況下，應使用 text 或 character varying。

有關字串文字語法的資訊，請參閱[第 4.1.2.1 節](../sql-syntax/lexical-structure.md#4-1-2-1-zi-chuan-chang)；有關可用運算子和函數的資訊，請參閱[第 9 章](../functions-and-operators/)。資料庫字元集決定用於儲存文字的字元集；有關字元集支援的更多訊息，請參閱[第 23.3 節](../../server-administration/localization/character-set-support.md)。

**Example 8.1. Using the Character Types**

```text
CREATE TABLE test1 (a character(4));
INSERT INTO test1 VALUES ('ok');
SELECT a, char_length(a) FROM test1; -- (1)
  a   | char_length
------+-------------
 ok   |           2

CREATE TABLE test2 (b varchar(5));
INSERT INTO test2 VALUES ('ok');
INSERT INTO test2 VALUES ('good      ');
INSERT INTO test2 VALUES ('too long');
ERROR:  value too long for type character varying(5)
INSERT INTO test2 VALUES ('too long'::varchar(5)); -- explicit truncation
SELECT b, char_length(b) FROM test2;
   b   | char_length
-------+-------------
 ok    |           2
 good  |           5
 tool  |           5
```

| \(1\) | char\_length 函數在 [9.4 節](../functions-and-operators/string-functions-and-operators.md)中討論。 |
| :--- | :--- |


PostgreSQL 中還有另外兩種固定長度的字串型別，如 Table 8.5 所示。name 型別僅用於在內部系統目錄中儲存指標，並非供一般使用者使用。它的長度目前定義為 64 個位元組（63 個可用字元加結尾符號），但應視 C 原始碼中的常數 NAMEDATALEN 而定。長度在編譯時設定（因此可以根據特殊用途進行調整）; 預設的最大長度可能會在將來的版本中變更。型別「“char”」（注意雙引號）與 char\(1\) 的不同之處在於它僅使用一個位元組的儲存空間。它在系統目錄中作為簡單內部使用的列舉型別。

**Table 8.5. Special Character Types**

| Name | Storage Size | Description |
| :--- | :--- | :--- |
| `"char"` | 1 byte | 單位元組內部型別 |
| `name` | 64 bytes | 物件名稱的內部型別 |

