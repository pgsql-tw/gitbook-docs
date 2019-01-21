---
description: 版本：11
---

# 2.3. 創建一個新的資料表

你可以創建一個新的資料表，為它取一個名字，並且宣告所有的欄位名稱與其資料型別：

```text
CREATE TABLE weather (
    city            varchar(80),
    temp_lo         int,           -- low temperature
    temp_hi         int,           -- high temperature
    prcp            real,          -- precipitation
    date            date
);
```

你可以把上述內容在 psql 中輸入，包含換行字元不會影響判讀。psql 是以分號作為指令結束的判定。

空白（包含「空白」、「定位符號」和「換行符號」）都可以自由使用在 SQL 指令當中。這表示你可以將指令以不同的形式排版，甚至全部寫都在一行也沒問題。使用破折號，連續2個（＂--＂），表示緊接的內容只是註解，直到該行結束為止。PostgreSQL 是不分大小寫字母的，包括各類關鍵字和描述語，除非是使用雙引號括起來的文字。（更精確地說，沒有被雙引號括起來的識別字，都會轉為小寫字母進行識別）

varchar\(80\) 表示指定一個資料型別，它可以儲放任意 80 個字元以內的字串。int 是一般認知的整數型別。real 表示資料是單精確度的浮點數。date 顧名思義，就是日期時間型別。（本例中欄位名稱和型別都使用 date，這可能是方便，也可能是困擾，端看你如何使用。）

PostgreSQL 支援標準的資料型別 int, smallint, real, double precision, char\(N\), varchar\(N\), date, time, timestamp, interval，也支援了複合型的地理資料型別。PostgreSQL 可以自訂組合任意數量的資料型別。語法上，資料型別名稱並不是保留關鍵字的範圍，除非特定的標準 SQL 支援需求之外。

第二個例子用來儲存城市及其所在的地理位置：

```text
CREATE TABLE cities (
    name            varchar(80),
    location        point
);
```

point 型別是一個 PostgreSQL專屬資料型別的範例。

最後，應該被點出來的是，如果你不再需要一個表格，或者想要重新以別的方式創建它，那麼你可以以下列的指令來移除它：

```text
DROP TABLE tablename;
```

