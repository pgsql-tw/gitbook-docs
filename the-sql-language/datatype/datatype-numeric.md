<a id="DATATYPE-NUMERIC"></a>

## 8.1. 數值型別 [#](#DATATYPE-NUMERIC)

[8.1.1. 整數型別](datatype-numeric.md#DATATYPE-INT)

[8.1.2. 任意精度數值](datatype-numeric.md#DATATYPE-NUMERIC-DECIMAL)

[8.1.3. 浮點數型別](datatype-numeric.md#DATATYPE-FLOAT)

[8.1.4. Serial 型別](datatype-numeric.md#DATATYPE-SERIAL)

<a id="id-1.5.7.9.2"></a>

數值型別包含 2 個位元組、4 個位元組與 8 個位元組的整數，4 個位元組與 8 個位元組的浮點數，以及可選精度的十進位數。[表 8.2](datatype-numeric.md#DATATYPE-NUMERIC-TABLE) 列出了可用的型別。

<a id="DATATYPE-NUMERIC-TABLE"></a>

**表 8.2. 數值型別**

<table border="1" class="table" summary="數值型別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>名稱</th><th>儲存空間大小</th><th>說明</th><th>範圍</th></tr></thead><tbody><tr><td><code class="type">smallint</code></td><td>2 個位元組</td><td>小範圍整數</td><td>-32768 至 +32767</td></tr><tr><td><code class="type">integer</code></td><td>4 個位元組</td><td>整數的典型選擇</td><td>-2147483648 至 +2147483647</td></tr><tr><td><code class="type">bigint</code></td><td>8 個位元組</td><td>大範圍整數</td><td>-9223372036854775808 至 +9223372036854775807</td></tr><tr><td><code class="type">decimal</code></td><td>可變動</td><td>使用者指定精度，精確</td><td>小數點前最多 131072 位數；小數點後最多 16383 位數</td></tr><tr><td><code class="type">numeric</code></td><td>可變動</td><td>使用者指定精度，精確</td><td>小數點前最多 131072 位數；小數點後最多 16383 位數</td></tr><tr><td><code class="type">real</code></td><td>4 個位元組</td><td>可變精度，不精確</td><td>6 位十進位數字的精度</td></tr><tr><td><code class="type">double precision</code></td><td>8 個位元組</td><td>可變精度，不精確</td><td>15 位十進位數字的精度</td></tr><tr><td><code class="type">smallserial</code></td><td>2 個位元組</td><td>小範圍自動遞增整數</td><td>1 至 32767</td></tr><tr><td><code class="type">serial</code></td><td>4 個位元組</td><td>自動遞增整數</td><td>1 至 2147483647</td></tr><tr><td><code class="type">bigserial</code></td><td>8 個位元組</td><td>大範圍自動遞增整數</td><td>1 至 9223372036854775807</td></tr></tbody></table>

<br>

數值型別的常數語法說明於[第 4.1.2 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS)。數值型別具備一整套對應的算術運算子與函式。更多資訊請參閱[第 9 章](../functions/README.md)。以下各節會詳細說明這些型別。

<a id="DATATYPE-INT"></a>

### 8.1.1. 整數型別 [#](#DATATYPE-INT)

<a id="id-1.5.7.9.6.2"></a><a id="id-1.5.7.9.6.3"></a><a id="id-1.5.7.9.6.4"></a><a id="id-1.5.7.9.6.5"></a><a id="id-1.5.7.9.6.6"></a><a id="id-1.5.7.9.6.7"></a>

`smallint`、`integer` 與 `bigint` 型別儲存整數，也就是不含小數部分的數，各自有不同的範圍。若嘗試儲存超出允許範圍的值，將會產生錯誤。

`integer` 型別是常見的選擇，因為它在範圍、儲存空間大小與效能之間取得了最好的平衡。`smallint` 型別通常只在磁碟空間非常寶貴時才會使用。`bigint` 型別則是設計給 `integer` 型別的範圍不敷使用時所用。

SQL 只規定了 `integer`（或 `int`）、`smallint` 與 `bigint` 這幾種整數型別。型別名稱 `int2`、`int4` 與 `int8` 是擴充功能，其他一些 SQL 資料庫系統也使用這些名稱。

<a id="DATATYPE-NUMERIC-DECIMAL"></a>

### 8.1.2. 任意精度數值 [#](#DATATYPE-NUMERIC-DECIMAL)

<a id="id-1.5.7.9.7.2"></a><a id="id-1.5.7.9.7.3"></a><a id="id-1.5.7.9.7.4"></a>

`numeric` 型別可以儲存位數非常多的數值。它特別適合用來儲存金額，以及其他要求精確的數量。使用 `numeric` 值的計算在可能的情況下會產生精確的結果，例如加法、減法、乘法。不過，`numeric` 值的計算與整數型別、或是下一節所描述的浮點數型別相比非常慢。

以下我們會使用這些術語：`numeric` 的*精度*（precision）是整個數中有效數字的總個數，也就是小數點兩側的位數總和。`numeric` 的*小數位數*（scale）是小數部分、也就是小數點右側的十進位位數個數。所以數值 23.5141 的精度為 6，小數位數為 4。整數可以視為小數位數為零。

`numeric` 欄位的最大精度與最大小數位數都可以設定。要宣告 `numeric` 型別的欄位，請使用以下語法：

```

NUMERIC(precision, scale)
```

精度必須是正數，而小數位數可以是正數或負數（見下文）。或者寫成：

```

NUMERIC(precision)
```

這會選用 0 的小數位數。若指定：

```

NUMERIC
```

而不帶任何精度或小數位數，則會建立一個「不受限的 numeric」欄位，其中可以儲存任何長度的數值，直到實作上的限制為止。這種欄位不會把輸入值強制轉換為任何特定的小數位數，而有宣告小數位數的 `numeric` 欄位則會把輸入值強制轉換為該小數位數。（SQL 標準要求預設的小數位數為 0，也就是強制轉換為整數精度。我們認為這樣有點沒用。如果你在意可攜性，請一律明確指定精度與小數位數。）

### 注意

在 `numeric` 型別宣告中可以明確指定的最大精度為 1000。不受限的 `numeric` 欄位則受到[表 8.2](datatype-numeric.md#DATATYPE-NUMERIC-TABLE) 所述限制的規範。

如果要儲存的值其小數位數大於欄位所宣告的小數位數，系統會把該值四捨五入到指定的小數位數。接著，如果小數點左側的位數超過所宣告的精度減去所宣告的小數位數，就會引發錯誤。例如，宣告為

```

NUMERIC(3, 1)
```

的欄位會把值四捨五入到小數點後 1 位，並且可以儲存 -99.9 到 99.9（含端點）之間的值。

從 PostgreSQL 15 開始，允許宣告小數位數為負值的 `numeric` 欄位。這時值會在小數點左側被四捨五入。精度仍然代表未被四捨五入之位數的最大個數。因此，宣告為

```

NUMERIC(2, -3)
```

的欄位會把值四捨五入到最接近的千位，並且可以儲存 -99000 到 99000（含端點）之間的值。也允許宣告比所宣告精度更大的小數位數。這樣的欄位只能存放小數值，而且它要求小數點右側緊接著的零位數至少要有「所宣告的小數位數減去所宣告的精度」那麼多。例如，宣告為

```

NUMERIC(3, 5)
```

的欄位會把值四捨五入到小數點後 5 位，並且可以儲存 -0.00999 到 0.00999（含端點）之間的值。

### 注意

PostgreSQL 允許 `numeric` 型別宣告中的小數位數為 -1000 到 1000 範圍內的任何值。然而，SQL 標準要求小數位數必須落在 0 到 *`precision`* 的範圍內。使用該範圍之外的小數位數，可能無法移植到其他資料庫系統。

數值在實體儲存時不會帶有任何額外的前導零或尾端零。因此，欄位所宣告的精度與小數位數是最大值，而不是固定的配置量。（就這個意義而言，`numeric` 型別比較像 `varchar(n)` 而不像 `char(n)`。）實際的儲存需求是每四個十進位位數一組佔兩個位元組，再加上三到八個位元組的額外負擔。

<a id="id-1.5.7.9.7.13"></a><a id="id-1.5.7.9.7.14"></a><a id="id-1.5.7.9.7.15"></a>

除了一般的數值之外，`numeric` 型別還有幾個特殊值：

<br>
`Infinity`<br>
`-Infinity`<br>
`NaN`<br>

這些是沿用自 IEEE 754 標準，分別代表「無限大」、「負無限大」與「非數值」（not-a-number）。在 SQL 指令中把這些值寫成常數時，必須用引號括起來，例如 `UPDATE table SET x = '-Infinity'`。在輸入時，這些字串的辨識不區分大小寫。無限大的值也可以改寫成 `inf` 與 `-inf`。

無限大的值的行為符合數學上的預期。例如，`Infinity` 加上任何有限值等於 `Infinity`，`Infinity` 加上 `Infinity` 也是如此；但是 `Infinity` 減去 `Infinity` 會得到 `NaN`（非數值），因為它沒有明確定義的解釋。請注意，無限大只能儲存在不受限的 `numeric` 欄位中，因為它在概念上超過了任何有限的精度限制。

`NaN`（非數值）這個值是用來表示未定義的計算結果。一般而言，任何以 `NaN` 為輸入的運算都會得到另一個 `NaN`。唯一的例外是：當運算的其他輸入使得「即使把 `NaN` 換成任何有限或無限的數值也會得到相同的輸出」時，那個輸出值也會被用作 `NaN` 的結果。（這個原則的一個例子是 `NaN` 的零次方會得到 1。）

### 注意

在大多數「非數值」概念的實作中，`NaN` 不會被視為等於任何其他數值（包括 `NaN` 本身）。為了讓 `numeric` 值可以被排序，並用在以樹狀結構為基礎的索引中，PostgreSQL 把 `NaN` 值視為彼此相等，且大於所有非 `NaN` 的值。

`decimal` 與 `numeric` 型別是等價的。這兩種型別都是 SQL 標準的一部分。

在對值進行四捨五入時，`numeric` 型別對於剛好在中間的值會捨入成遠離零的方向，而（在大多數機器上）`real` 與 `double precision` 型別則會把剛好在中間的值捨入成最接近的偶數。例如：

```

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

<a id="DATATYPE-FLOAT"></a>

### 8.1.3. 浮點數型別 [#](#DATATYPE-FLOAT)

<a id="id-1.5.7.9.8.2"></a><a id="id-1.5.7.9.8.3"></a><a id="id-1.5.7.9.8.4"></a><a id="id-1.5.7.9.8.5"></a><a id="id-1.5.7.9.8.6"></a>

`real` 與 `double precision` 資料型別是不精確、可變精度的數值型別。在目前所有支援的平台上，這些型別都是 IEEE 754 二進位浮點數運算標準的實作（分別為單精度與雙精度），其程度取決於底層的處理器、作業系統與編譯器的支援。

不精確的意思是，有些值無法被精確地轉換為內部格式，而是以近似值的形式儲存，因此儲存再取回一個值時，可能會出現些微的差異。如何管理這些誤差，以及它們如何在計算過程中傳遞，是數學與電腦科學中一整個分支的主題，在此不予討論，僅說明以下幾點：

* 如果你需要精確的儲存與計算（例如金額），請改用 `numeric` 型別。
* 如果你要用這些型別進行任何重要的複雜計算，尤其是當你依賴邊界情況（無限大、下溢）的某些特定行為時，你應該仔細評估其實作。
* 比較兩個浮點數是否相等，可能不一定會如預期般運作。

在目前所有支援的平台上，`real` 型別的範圍大約是 1E-37 到 1E+37，精度至少有 6 位十進位數字。`double precision` 型別的範圍大約是 1E-307 到 1E+308，精度至少有 15 位數字。太大或太小的值會造成錯誤。如果輸入數值的精度太高，可能會發生四捨五入。太接近零、無法與零區分開來表示的數值，會造成下溢錯誤。

在預設情況下，浮點數值會以最短且精確的十進位表示法輸出為文字形式；所產生的十進位值，比起其他任何以相同二進位精度可表示的值，都更接近實際儲存的二進位值。（不過，目前輸出的值永遠不會*剛好*落在兩個可表示的值的正中間，這是為了避免一個常見的錯誤：某些輸入常式並未正確遵守四捨五入到最接近偶數的規則。）這個值對 `float8` 值最多會使用 17 位有效十進位數字，對 `float4` 值則最多 9 位數字。

### 注意

這種最短精確輸出格式的產生速度，比以往的四捨五入格式快得多。

為了與較舊版本 PostgreSQL 所產生的輸出相容，以及為了能夠降低輸出的精度，可以使用 [extra_float_digits](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) 參數來改為選用四捨五入的十進位輸出。將它設為 0，會恢復先前的預設行為，也就是把值四捨五入到 6 位（對 `float4`）或 15 位（對 `float8`）有效十進位數字。設為負值會進一步減少位數；例如 -2 會分別把輸出四捨五入到 4 位或 13 位數字。

任何大於 0 的 [extra_float_digits](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) 值，都會選用最短精確格式。

### 注意

過去，想要取得精確值的應用程式必須把 [extra_float_digits](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) 設為 3 才能取得。為了在各版本之間有最大的相容性，它們應該繼續這麼做。

<a id="id-1.5.7.9.8.15"></a><a id="id-1.5.7.9.8.16"></a>

除了一般的數值之外，浮點數型別還有幾個特殊值：

<br>
`Infinity`<br>
`-Infinity`<br>
`NaN`<br>

這些分別代表 IEEE 754 的特殊值「無限大」、「負無限大」與「非數值」。在 SQL 指令中把這些值寫成常數時，必須用引號括起來，例如 `UPDATE table SET x = '-Infinity'`。在輸入時，這些字串的辨識不區分大小寫。無限大的值也可以改寫成 `inf` 與 `-inf`。

### 注意

IEEE 754 規定 `NaN` 不應與任何其他浮點數值（包括 `NaN` 本身）比較為相等。為了讓浮點數值可以被排序，並用在以樹狀結構為基礎的索引中，PostgreSQL 把 `NaN` 值視為彼此相等，且大於所有非 `NaN` 的值。

PostgreSQL 也支援 SQL 標準的 `float` 與 `float(p)` 表示法來指定不精確的數值型別。在這裡，*`p`* 指定的是以*二進位*位數計算的最低可接受精度。PostgreSQL 接受 `float(1)` 到 `float(24)` 作為選用 `real` 型別，而 `float(25)` 到 `float(53)` 則選用 `double precision`。*`p`* 的值若超出允許的範圍會引發錯誤。未指定精度的 `float` 會被視為 `double precision`。

<a id="DATATYPE-SERIAL"></a>

### 8.1.4. Serial 型別 [#](#DATATYPE-SERIAL)

<a id="id-1.5.7.9.9.2"></a><a id="id-1.5.7.9.9.3"></a><a id="id-1.5.7.9.9.4"></a><a id="id-1.5.7.9.9.5"></a><a id="id-1.5.7.9.9.6"></a><a id="id-1.5.7.9.9.7"></a><a id="id-1.5.7.9.9.8"></a><a id="id-1.5.7.9.9.9"></a>

### 注意

本節描述的是 PostgreSQL 特有的自動遞增欄位建立方式。另一種方式是使用 SQL 標準的識別欄位（identity column）功能，說明於[第 5.3 節](../ddl/ddl-identity-columns.md)。

`smallserial`、`serial` 與 `bigserial` 資料型別並不是真正的型別，而只是建立唯一識別欄位時的一種標記上的便利寫法（類似某些其他資料庫所支援的 `AUTO_INCREMENT` 屬性）。在目前的實作中，指定：

```

CREATE TABLE tablename (
    colname SERIAL
);
```

等同於指定：

```

CREATE SEQUENCE tablename_colname_seq AS integer;
CREATE TABLE tablename (
    colname integer NOT NULL DEFAULT nextval('tablename_colname_seq')
);
ALTER SEQUENCE tablename_colname_seq OWNED BY tablename.colname;
```

因此，我們建立了一個整數欄位，並安排它的預設值由一個序列（sequence）產生器來指派。這裡套用了 `NOT NULL` 限制條件，以確保不能插入 NULL 值。（在大多數情況下，你也會想要加上 `UNIQUE` 或 `PRIMARY KEY` 限制條件，以防止不小心插入重複的值，但這並不會自動發生。）最後，該序列會被標記為由該欄位所「擁有」，因此當該欄位或資料表被刪除時，這個序列也會一併被刪除。

### 注意

由於 `smallserial`、`serial` 與 `bigserial` 是以序列來實作的，即使從未刪除過任何資料列，該欄位中出現的值序列仍可能會有「洞」或空隙。從序列取得的值即使從未成功插入資料表欄位中，仍然算是被「用掉」了。舉例來說，當進行插入的交易被回復時，就可能發生這種情況。詳情請參閱[第 9.17 節](../functions/functions-sequence.md)中的 `nextval()`。

要把序列的下一個值插入 `serial` 欄位，請指定該 `serial` 欄位應被指派其預設值。做法是在 `INSERT` 陳述式的欄位清單中排除該欄位，或是使用 `DEFAULT` 關鍵字。

型別名稱 `serial` 與 `serial4` 是等價的：兩者都會建立 `integer` 欄位。型別名稱 `bigserial` 與 `serial8` 的運作方式相同，差別在於它們建立的是 `bigint` 欄位。如果你預期在資料表的生命週期內會使用超過 2 的 31 次方個識別碼，就應該使用 `bigserial`。型別名稱 `smallserial` 與 `serial2` 的運作方式也相同，差別在於它們建立的是 `smallint` 欄位。

為 `serial` 欄位所建立的序列，會在擁有它的欄位被刪除時自動被刪除。你可以在不刪除欄位的情況下刪除該序列，但這會強制移除該欄位的預設值運算式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-numeric.html)（原文版本：18.6；核對日期：2026-09-13）
