<a id="SQL-CREATEDOMAIN"></a><a id="id-1.9.3.62.1"></a>

## CREATE DOMAIN

CREATE DOMAIN — 定義新的網域

<a id="id-1.9.3.62.4"></a>

## 語法

```

CREATE DOMAIN name [ AS ] data_type
    [ COLLATE collation ]
    [ DEFAULT expression ]
    [ domain_constraint [ ... ] ]

where domain_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL | NULL | CHECK (expression) }
```

<a id="id-1.9.3.62.5"></a>

## 說明

`CREATE DOMAIN` 會建立新的網域。網域本質上是一種帶有選用限制條件（對允許的值集合所加的限制）的資料型別。定義網域的使用者會成為其擁有者。

若指定了綱要名稱（例如 `CREATE DOMAIN
myschema.mydomain ...`），網域就會建立在指定的綱要中；否則會建立在目前的綱要中。網域名稱在其綱要中現有的型別與網域之間必須是唯一的。

網域適合用來將欄位上常見的限制條件抽象化，集中在單一位置維護。例如，數個資料表可能都含有電子郵件地址欄位，而且全都需要相同的 CHECK 限制條件來驗證地址的語法。請定義一個網域，而不要個別為每個資料表設定限制條件。

若要能夠建立網域，你必須擁有底層型別的 `USAGE` 權限。

<a id="id-1.9.3.62.6"></a>

## 參數

*`name`*
:   要建立的網域名稱（可選擇以綱要限定）。

*`data_type`*
:   網域的底層資料型別。這可以包含陣列指定符。

*`collation`*
:   網域的選用定序。若未指定定序，網域會具有與其底層資料型別相同的定序行為。若指定了 `COLLATE`，底層型別必須是可定序的。

`DEFAULT expression`
:   `DEFAULT` 子句為網域資料型別的欄位指定預設值。其值為任何不含變數的運算式（但不允許子查詢）。預設運算式的資料型別必須與網域的資料型別相符。若未指定預設值，則預設值為 null 值。

    預設運算式會用於任何未為該欄位指定值的插入操作。若為特定欄位定義了預設值，它會覆寫與網域相關聯的任何預設值。而網域的預設值又會覆寫與底層資料型別相關聯的任何預設值。

`CONSTRAINT constraint_name`
:   限制條件的選用名稱。若未指定，系統會產生一個名稱。

`NOT NULL`
:   禁止此網域的值為 null（但請參閱下方的注意事項）。

`NULL`
:   允許此網域的值為 null。這是預設行為。

    此子句僅用於與非標準 SQL 資料庫相容。不建議在新的應用程式中使用。

`CHECK (expression)`
:   `CHECK` 子句指定網域的值必須滿足的完整性限制條件或測試。每個限制條件都必須是產生布林結果的運算式。它應該使用關鍵字 `VALUE` 來參照受測試的值。求值為 TRUE 或 UNKNOWN 的運算式即為通過。若運算式產生 FALSE 結果，就會回報錯誤，且不允許將該值轉換為網域型別。

    目前，`CHECK` 運算式既不能包含子查詢，也不能參照 `VALUE` 以外的變數。

    當網域有多個 `CHECK` 限制條件時，它們會依名稱的字母順序進行測試。（9.5 之前的 PostgreSQL 版本並未遵循 `CHECK` 限制條件的任何特定觸發順序。）

<a id="SQL-CREATEDOMAIN-NOTES"></a>

## 注意事項

網域限制條件，特別是 `NOT NULL`，會在將值轉換為網域型別時進行檢查。名義上屬於網域型別的欄位，即使有這類限制條件，仍有可能讀出 null。例如，在外部連接查詢中，若網域欄位位於外部連接中可為 null 的一側，就可能發生這種情況。一個更微妙的例子是

```

INSERT INTO tab (domcol) VALUES ((SELECT domcol FROM tab WHERE false));
```

空的純量子 SELECT 會產生一個被視為屬於該網域型別的 null 值，因此不會再對它套用任何限制條件檢查，插入也會成功。

這類問題非常難以避免，因為 SQL 普遍假定 null 值是每一種資料型別的有效值。因此，最佳做法是將網域的限制條件設計為允許 null 值，然後視需要對網域型別的欄位套用欄位的 `NOT NULL` 限制條件，而不是直接套用到網域型別上。

PostgreSQL 假定 `CHECK` 限制條件的條件是不可變的（immutable），也就是說，對於相同的輸入值，它們一律會產生相同的結果。正是這個假定，使得只在值第一次被轉換為網域型別時檢查 `CHECK` 限制條件、而不在其他時候檢查，成為合理的做法。（這在本質上與資料表 `CHECK` 限制條件的處理方式相同，如[第 5.5.1 節](../../the-sql-language/ddl/ddl-constraints.md#ddl-constraints-check-constraints)所述。）

打破這項假定的一種常見方式，是在 `CHECK` 運算式中參照使用者定義的函式，然後變更該函式的行為。PostgreSQL 並不禁止這麼做，但它不會察覺是否有已儲存的網域型別值現在違反了該 `CHECK` 限制條件。這會導致之後的資料庫傾印與還原失敗。處理這類變更的建議做法是：先移除限制條件（使用 `ALTER
DOMAIN`），調整函式定義，再重新加入限制條件，藉此針對已儲存的資料重新檢查它。

確保網域的 `CHECK` 運算式不會擲出錯誤，也是良好的做法。

<a id="id-1.9.3.62.8"></a>

## 範例

此範例建立 `us_postal_code` 資料型別，然後在資料表定義中使用該型別。這裡使用正規表示式測試來驗證值看起來是否為有效的美國郵遞區號：

```

CREATE DOMAIN us_postal_code AS TEXT
CHECK(
   VALUE ~ '^\d{5}$'
OR VALUE ~ '^\d{5}-\d{4}$'
);

CREATE TABLE us_snail_addy (
  address_id SERIAL PRIMARY KEY,
  street1 TEXT NOT NULL,
  street2 TEXT,
  street3 TEXT,
  city TEXT NOT NULL,
  postal us_postal_code NOT NULL
);
```

<a id="SQL-CREATEDOMAIN-COMPATIBILITY"></a>

## 相容性

`CREATE DOMAIN` 命令符合 SQL 標準。

此命令中的 `NOT NULL` 語法是 PostgreSQL 的擴充語法。（對於非複合資料型別，符合標準的同等寫法是 `CHECK (VALUE IS NOT
NULL)`。不過，依據[「注意事項」一節](sql-createdomain.md#SQL-CREATEDOMAIN-NOTES)，實務上無論如何最好避免使用這類限制條件。）`NULL`「限制條件」是 PostgreSQL 的擴充語法（另請參閱[相容性](sql-createtable.md#SQL-CREATETABLE-COMPATIBILITY)）。

<a id="SQL-CREATEDOMAIN-SEE-ALSO"></a>

## 另請參閱

[ALTER DOMAIN](sql-alterdomain.md), [DROP DOMAIN](sql-dropdomain.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createdomain.html)（原文版本：18.6；核對日期：2026-10-04）
