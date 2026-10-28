<a id="SQL-CREATESEQUENCE"></a><a id="id-1.9.3.81.1"></a>

## CREATE SEQUENCE

CREATE SEQUENCE — 定義新的序列產生器

<a id="id-1.9.3.81.4"></a>

## 語法

```

CREATE [ { TEMPORARY | TEMP } | UNLOGGED ] SEQUENCE [ IF NOT EXISTS ] name
    [ AS data_type ]
    [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ [ NO ] CYCLE ]
    [ START [ WITH ] start ]
    [ CACHE cache ]
    [ OWNED BY { table_name.column_name | NONE } ]
```

<a id="id-1.9.3.81.5"></a>

## 說明

`CREATE SEQUENCE` 會建立一個新的序號
產生器。這包括建立並初始化一個名為 *`name`* 的新的特殊
單列資料表。該產生器的擁有者將是
執行此命令的使用者。

若指定了綱要名稱，序列就會建立在
指定的綱要中；否則會建立在目前的綱要中。
暫存序列存在於一個特殊的綱要中，因此建立暫存序列時不能指定綱要名稱。
序列名稱必須與同一綱要中任何其他關聯
（資料表、序列、索引、檢視表、具體化檢視表或外部資料表）的名稱不同。

序列建立之後，你可以使用函式
`nextval`、
`currval` 與
`setval`
來操作該序列。這些函式記載於
[第 9.17 節](../../the-sql-language/functions/functions-sequence.md)。

雖然你不能直接更新序列，但可以使用如下的查詢：

```

SELECT * FROM name;
```

來檢視序列的參數與目前狀態。特別是，
序列的 `last_value` 欄位會顯示任何工作階段
最後配置的值。（當然，若其他工作階段正在積極地執行
`nextval` 呼叫，這個值在印出時可能就已經過時了。）

<a id="id-1.9.3.81.6"></a>

## 參數

`TEMPORARY` 或 `TEMP`
:   若有指定，序列物件只會為此
    工作階段建立，並在工作階段結束時自動移除。當暫存序列存在時，
    同名的現有永久序列（在此
    工作階段中）將不可見，除非以
    綱要限定的名稱參照它們。

`UNLOGGED`

若有指定，序列會建立為無日誌（unlogged）序列。對
無日誌序列的變更不會寫入預寫式日誌（write-ahead log）。它們
不具備當機安全性：無日誌序列在當機或非正常關閉之後，會自動重設為
初始狀態。無日誌序列也
不會被複寫到備用伺服器。

與無日誌資料表不同，無日誌序列並不會帶來顯著的
效能優勢。此選項主要是供
透過識別欄位或 serial 欄位與無日誌資料表相關聯的序列使用。
在這些情況下，讓序列
寫入 WAL 並被複寫、而其相關聯的資料表卻沒有，通常並不合理。

`IF NOT EXISTS`
:   若已存在同名的關聯，不擲出錯誤。
    此情況會發出 notice。請注意，並不保證
    現有的關聯與原本將建立的序列有任何相似之處——它甚至可能根本不是序列。

*`name`*
:   要建立的序列名稱（可選擇以綱要限定）。

*`data_type`*
:   選用的
    子句 `AS data_type`
    指定序列的資料型別。有效的型別為
    `smallint`、`integer`
    與 `bigint`。`bigint` 是
    預設值。資料型別決定了序列的預設最小值與最大值。

*`increment`*
:   選用的子句 `INCREMENT BY increment` 指定
    要將哪個值加到目前的序列值上以產生
    新值。正值會產生遞增序列，
    負值則產生遞減序列。預設值為 1。

*`minvalue`*<br>`NO MINVALUE`
:   選用的子句 `MINVALUE minvalue` 決定
    序列能產生的最小值。若未提供此子句，
    或指定了 `NO MINVALUE`，則
    會使用預設值。遞增序列的預設值為 1。
    遞減序列的預設值為該資料型別的最小值。

*`maxvalue`*<br>`NO MAXVALUE`
:   選用的子句 `MAXVALUE maxvalue` 決定
    序列的最大值。若未提供此子句，
    或指定了 `NO MAXVALUE`，則
    會使用預設值。遞增序列的預設值為
    該資料型別的最大值。遞減
    序列的預設值為 -1。

`CYCLE`<br>`NO CYCLE`

`CYCLE` 選項允許遞增序列與遞減序列分別在達到 *`maxvalue`* 與 *`minvalue`* 時
循環回繞。若達到
界限，下一個產生的數字將分別是 *`minvalue`* 與 *`maxvalue`*。

若指定了 `NO CYCLE`，則序列達到其
界限之後（遞增序列為最大值、遞減序列為最小值），任何對
`nextval` 的呼叫都會傳回錯誤。若
`CYCLE` 與 `NO CYCLE` 都未
指定，則預設為 `NO CYCLE`。

*`start`*
:   選用的子句 `START WITH start` 允許
    序列從任何位置開始。預設的起始值，
    遞增序列為 *`minvalue`*，
    遞減序列為 *`maxvalue`*。

*`cache`*
:   選用的子句 `CACHE cache` 指定
    要預先配置多少個序號並存放在
    記憶體中以加快存取。最小值為 1（一次只能
    產生一個值，也就是不使用快取），這也是
    預設值。

`OWNED BY` *`table_name`*.*`column_name`*<br>`OWNED BY NONE`
:   `OWNED BY` 選項會使序列與
    特定的資料表欄位相關聯，如此一來，若該欄位
    （或其整個資料表）被移除，序列也會自動
    一併移除。指定的資料表必須與序列有相同的擁有者，且位於
    相同的綱要中。
    預設的 `OWNED BY NONE` 指定
    不建立此種關聯。

<a id="id-1.9.3.81.7"></a>

## 注意事項

使用 `DROP SEQUENCE` 來移除序列。

序列是以 `bigint` 算術為基礎，因此其範圍
不能超過八位元組整數的範圍
（-9223372036854775808 到 9223372036854775807）。

由於 `nextval` 與 `setval` 呼叫永遠不會
被回滾，若需要「無間隙」地
指派序號，就不能使用序列物件。可以透過
對一個包含計數器的資料表使用排他鎖定來實作
無間隙的指派；但這種做法比序列
物件昂貴得多，特別是在許多交易需要同時取得序號的情況下。

若對一個將由多個工作階段同時使用的序列物件，
使用大於 1 的 *`cache`* 設定，
可能會得到非預期的結果。每個工作階段在存取序列物件一次時，
會配置並快取連續的
序列值，並相應地
增加序列物件的 `last_value`。
接著，該工作階段中接下來 *`cache`*-1
次的 `nextval` 使用，只會直接傳回
預先配置的值，而不會動到序列物件。因此，任何
在工作階段中已配置但未使用的數字，都會在
該工作階段結束時遺失，導致序列中出現「空洞」。

此外，雖然保證多個工作階段會配置
不同的序列值，但若綜觀所有工作階段，
這些值可能不是依序產生的。例如，
在 *`cache`* 設定為 10 的情況下，
工作階段 A 可能保留值 1..10 並傳回
`nextval`=1，接著工作階段 B 可能保留值
11..20，並在工作階段 A
產生 `nextval`=2 之前就傳回 `nextval`=11。因此，在
*`cache`* 設定為 1 的情況下，
可以安全地假設 `nextval` 的值是依序產生的；
在 *`cache`* 設定大於 1 的情況下，你
應該只假設 `nextval` 的值全都
互不相同，而不要假設它們完全依序產生。此外，
`last_value` 會反映任何工作階段
所保留的最新值，無論該值是否已由
`nextval` 傳回。

另一個需要考量的是，在
這樣的序列上執行的 `setval`，在其他工作階段
用完它們已快取的所有預先配置值之前，不會被它們察覺。

<a id="id-1.9.3.81.8"></a>

## 範例

建立一個名為 `serial`、從 101 開始的遞增序列：

```

CREATE SEQUENCE serial START 101;
```

從此序列中取得下一個數字：

```

SELECT nextval('serial');

 nextval
---------
     101
```

從此序列中取得下一個數字：

```

SELECT nextval('serial');

 nextval
---------
     102
```

在 `INSERT` 命令中使用此序列：

```

INSERT INTO distributors VALUES (nextval('serial'), 'nothing');
```

在 `COPY FROM` 之後更新序列值：

```

BEGIN;
COPY distributors FROM 'input_file';
SELECT setval('serial', max(id)) FROM distributors;
END;
```

<a id="id-1.9.3.81.9"></a>

## 相容性

`CREATE SEQUENCE` 符合 SQL
標準，但有以下例外：

* 取得下一個值是使用 `nextval()`
  函式，而不是標準的 `NEXT VALUE FOR`
  運算式。
* `OWNED BY` 子句是 PostgreSQL
  的擴充語法。

<a id="id-1.9.3.81.10"></a>

## 另請參閱

[ALTER SEQUENCE](sql-altersequence.md)、[DROP SEQUENCE](sql-dropsequence.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createsequence.html)（原文版本：18.6；核對日期：2026-10-04）
