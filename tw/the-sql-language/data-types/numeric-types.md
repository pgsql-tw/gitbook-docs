# 8.1. 數字型別

數字型別由兩位數，四位數和八位數整數，四位元組和八位元組的浮點數以及可調式精確度的小數組成。[表格 8.2 ](numeric-types.md#table-8-2-numeric-types)列出了可用的類型。

### **Table 8.2. Numeric Types**

| Name | Storage Size | Description | Range |
| :--- | :--- | :--- | :--- |
| `smallint` | 2 bytes | small-range integer | -32768 to +32767 |
| `integer` | 4 bytes | typical choice for integer | -2147483648 to +2147483647 |
| `bigint` | 8 bytes | large-range integer | -9223372036854775808 to +9223372036854775807 |
| `decimal` | variable | user-specified precision, exact | up to 131072 digits before the decimal point; up to 16383 digits after the decimal point |
| `numeric` | variable | user-specified precision, exact | up to 131072 digits before the decimal point; up to 16383 digits after the decimal point |
| `real` | 4 bytes | variable-precision, inexact | 6 decimal digits precision |
| `double precision` | 8 bytes | variable-precision, inexact | 15 decimal digits precision |
| `smallserial` | 2 bytes | small autoincrementing integer | 1 to 32767 |
| `serial` | 4 bytes | autoincrementing integer | 1 to 2147483647 |
| `bigserial` | 8 bytes | large autoincrementing integer | 1 to 9223372036854775807 |

[4.1.2 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/sql-syntax/41-lexical-structure.md)描述了數字型別常數的語法。 數字型別有一整套相應的算術運算元和函數。有關更多訊息，請參閱第 9 章。 以下各節將詳細介紹這些型別。

## 8.1.1. 整數型別（Integer Types）

smallint、integer 和 bigint 型別儲存整數，即不包含小數部分的各種範圍的數字。嘗試儲存在允許的範圍之外的數值將會導致錯誤。

「integer」型別是常見的選擇，因為它提供了數值範圍、儲存空間及效能之間的最佳平衡。「smallint」 列別通常只在磁碟空間不足的情況下使用。「bigint」 型別被設計用於整數型別的範圍不足時。

SQL僅指定整數型別 integer（或 int）、smallint 和 bigint。 型別名稱 int2、int4 和 int8 則是延伸型別，也有一些其他 SQL 資料庫系統使用。

## 8.1.2. 可調式精確度數值型別（NUMERIC Type）

數字型別可以儲存很多位數的數字。特別建議使用在要求正確性的地方，像是儲存貨幣金額或其他數量。使用數值的計算在可能需要的情況下得到確切的結果，例如 加法、減法、乘法。但是，與整數型別或下一節中介紹的浮點型別相比，對數值的計算速度非常緩慢。

我們使用下面的術語：數字的「scale」是小數點右邊的小數部分，也就是小數的位數。數字的「precision」是整數中有效位數的總數，即小數點兩邊的位數總合。所以 23.5141 的 precision 是 6，scale 是 4。整數可以被認為是 scale 為 0。

可以配置數字欄位的最大 precision 和最大 scale。要宣告數字型別的欄位，請使用以下語法：

```text
NUMERIC(precision, scale)
```

precision 必須是正值，scale 為零或正值。或是：

```text
NUMERIC(precision)
```

選擇 0 為 scale。這樣使用：

```text
NUMERIC
```

沒有任何 precision 或 scale 的話，就會建立一個欄位，其欄位中可以儲存任何 precision 和 scale 的數字值，直到達到 precision 的極限。這種型別的欄位不會將輸入值強制轉為任何特定的 scale，其中具有聲明比例的數字欄位會將輸入值強制為該 scale。 （SQL 標準需要預設 scale 為 0，即強制為整數精度，我們發現這樣做有點無用。如果你擔心可移植性，請務必明確指定 precision 和 scale。

> ## 注意
>
> 在型別宣告中明確指定時允許的最大 precision 為 1000；沒有指定 precision 的NUMERIC 為 Table 8.2 中所述的限制。

如果要儲存的小數位數大於欄位所宣告的 scale，則係統會將值四捨五入到宣告所指定的小數位數。然後，如果小數點左邊的位數超過宣告的 precise 減去聲明的 scale 的話，則會產生錯誤。

數字內容的實體儲存不會有任何額外的前導位數或補零。因此，欄位宣告的 precise 和 scale 是最大值，而不是固定的分配。（在這個意義上，數字型別更像是 varchar\(n\) 而不是 char\(n\)。） 實際儲存的要求是每四個十進制數字組加兩個位元組，再加上三到八個位元組的額外配置。

除了普通的數值之外，數字型別還允許特殊值 NaN，意思是「不是一個數字」。 NaN 的任何操作都會產生另一個 NaN。在 SQL 指令中將此值作為常數寫入時，必須在其中使用單引號，例如 UPDATE table SET x = 'NaN'。 在輸入時，字串 NaN 識別是不區分大小寫的。

> ## 注意
>
> 「非數字」的概念在大多數實作中，NaN 不被視為等於任何其他數值（包括 NaN）。為了允許數值在樹狀索引中排序和使用，PostgreSQL 將 NaN 值視為相等或大於所有的非 NaN 值。

decimal 和 numeric 的型別是相同的。 這兩種型別都是 SQL 標準的一部分。

當需要四捨五入時，數字型別會往離零較遠的值調整，而（在大多數機器上）實數和雙精度型別會調整到最接近的偶數。 例如：

```text
SELECT x,
  round(x::numeric) AS num_round,
  round(x::double precision) AS dbl_round
FROM generate_series(-3.5, 3.5, 1) as x;
  x   | num_round | dbl_round
------+-----------+-----------
 -3.5 |        -4 |        -4
 -2.5 |        -3 |        -2
 -1.5 |        -2 |        -2
 -0.5 |        -1 |        -0
  0.5 |         1 |         0
  1.5 |         2 |         2
  2.5 |         3 |         2
  3.5 |         4 |         4
(8 rows)
```

## 8.1.3. 浮點數型別（Floating-Point Types）

資料型別中 real 和 double 是非精確的、可變精確度的數字型別。在實務上，這些型別通常是針對二進制浮點數運算（分別為單精度和雙精度）的IEEE 754標準的實作，需要底層的中央處理器、作業系統和編譯器支持。

非精確意味著某些值不能完全轉換為內部格式，並以近似值儲存，因此儲存和檢索值可能會表現出輕微的差異。管理這些誤差以及它們如何計算傳遞是數學和計算機科學分支的主題，除了以下幾點之外，這裡不再討論：

* 如果你需要精確的儲存和計算（例如貨幣金額），請改為使用 numeric 型別。
* 如果你想對這些型別做任何重要的複雜計算，特別是如果你依賴邊界情況下的某些行為（極大極小值或超過上下限），你應該仔細評估實作方式。
* 比較兩個相等的浮點數值可能並不總是按預期中直覺的方式運作。

在大多數平台上，real 型別的範圍至少為 1E-37 至 1E + 37，精確度至少為 6 位數十進制數字。double 型別的範圍通常在 1E-307 至 1E + 308 之間，精確度至少為 15 位數。數值太大或太小都會導致錯誤。如果輸入數字的精確度太高，四捨五入的情況則可能會發生。數字太接近於零，卻不能表示為零的話，將導致 underflow 超過下限的錯誤。

> ## 注意
>
> [extra\_float\_digits](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/iii-server-administration/server-configuration/1911-client-connection-defaults.md) 參數設定控制浮點數轉換為文字輸出時所包含的額外有效位數。使用預設值 0 時，PostgreSQL 支援的每個平台上的輸出都是相同的。增加它的話，能更精確地輸出儲存值，但可能在不同平台間是不同的結果。

除了普通的數值之外，浮點型別還有幾個特殊的值：

`Infinity`  
`-Infinity`  
`NaN`

這些分別代表 IEEE 754 特殊值「無限大」、「負無限大」和「非數字」。（在浮點數計算不符合 IEEE 754 標準的機器上，這些值可能無法如期運作。）在 SQL 指令中將這些值作為常數寫入時，必須在其放入單引號中，例如 UPDATE table SET x = '-Infinity'。 在輸入時，這些字串識別是不區分大小寫的。

> ## 注意
>
> IEEE 754 規定 NaN 不應與任何其他浮點數值（包括NaN）相等。為了允許浮點值在樹狀索引中排序和使用，PostgreSQL 將 NaN 視為相等或大於所有非 NaN 的數值。

PostgreSQL 也支援 SQL 標準的 float 和 float\(p\) 來表示非精確的數字型別。這裡，p 指的是二進位數字的最小可接受的精確度。PostgreSQL 接受 float\(1\) 到 float\(24\) 選擇視為 real 型別，而 float\(25\) 到 float\(53\) 則視為 double。p 超出允許範圍的話會產生錯誤。沒有指定精確度的浮點數意味著 double。

> ## 注意
>
> 假設 real 和 double 的尾數分別為 24 位和 53 位，以 IEEE 標準浮點數實作而言是正確的。在非 IEEE 平台上，它可能會有一些小問題，但為了簡單起見，最好在所有平台上都使用相同的 p 範圍。

## 8.1.4. 序列型別（Serial Types）

> ## 注意
>
> 本節介紹的是 PostgreSQL 專屬建立自動增量（auto-incrementing）欄位的方式。另一種方式是使用 [CREATE TABLE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-table.md) 中描述的 SQL 標準識別欄位功能。

資料型別 smallserial、serial 和 bigserial 都不是真正的型別，而僅僅是建立唯一識別欄位（類似於某些其他資料庫所支援的 AUTO\_INCREMENT 屬性）的方便型別語法。以目前的實作方式，請使用：

```text
CREATE TABLE tablename (
   colname SERIAL
);
```

相當於以下的指令：

```text
CREATE SEQUENCE tablename_colname_seq;
CREATE TABLE tablename (
   colname integer NOT NULL DEFAULT nextval('tablename_colname_seq')
);
ALTER SEQUENCE tablename_colname_seq OWNED BY tablename.colname;
```

因此，我們建立了一個整數欄位，並將其預設值設定為序列數字產生器。使用 NOT NULL 限制條件來確保無法插入空值。（在大多數情況下，你還需要附加一個 UNIQUE 或 PRIMARY KEY 限制條件來防止偶然插入重複值，但這不是自動的。） 最後，這個序列被標記為「owned by」欄位，以便在欄位或資料表被刪除時一併被刪除。

> ## 注意
>
> smallserial、serial 和 bigserial，被實作來實現序列數字，即使沒有資料列被刪除，在欄位中出現的值在序列中仍可能會有「漏洞」或缺口。即使包含該值的資料列從未成功插入資料表中，從序列中分配的值仍然會用完。例如，如果資料插入的交易回溯了，則可能發生這種情況。有關詳細訊息，請參閱[第 9.16 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/functions-and-operators/916-sequence-manipulation-functions.md)中的 nextval\(\)。

要將序列的下一個值插入到序列欄位中，請指定序列欄位應被分配其預設值。這可以透過從 INSERT 語句中欄位列表中排除欄位或使用DEFAULT關鍵字來完成。

型別名稱 serial 和 serial4 是等價的：都是建立整數（integer）欄位。型別名稱 bigserial 和 serial8 也以相同的方式作用，差別是他們建立一個 bigint 的欄位。如果你預期在資料表的整個生命週期中使用超過 2^31 個標識符，則應使用 bigserial。型別名稱 smallserial 和 serial2 也是以相同的，而除了它們是建立一個 smallint 欄位。

當擁有的欄位被刪除時，為序列欄位創建的序列也將自動刪除。但你可以刪除序列而不刪除欄位，這會強制刪除欄位的預設表示式。

