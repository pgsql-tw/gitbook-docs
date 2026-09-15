<a id="INDEXES-PARTIAL"></a>

## 11.8. 部分索引 [#](#INDEXES-PARTIAL)

<a id="id-1.5.10.11.2"></a>

*部分索引*（partial index）是建立在資料表某個子集上的索引；這個子集由一個條件運算式（稱為部分索引的*述詞*，predicate）定義。索引只包含滿足該述詞之資料表資料列的項目。部分索引是一項特殊的功能，但在好幾種情況下都很有用。

使用部分索引的一個主要理由，是避免為常見值建立索引。由於搜尋常見值（占所有資料表資料列超過數個百分比的值）的查詢無論如何都不會使用索引，因此根本沒有必要把這些資料列保留在索引中。這會縮小索引的大小，從而加快確實會使用該索引的查詢。它也會加快許多資料表更新操作，因為並非所有情況都需要更新索引。[範例 11.1](indexes-partial.md#INDEXES-PARTIAL-EX1) 展示了這個想法的一種可能應用。

<a id="INDEXES-PARTIAL-EX1"></a>

**範例 11.1. 建立排除常見值的部分索引**

假設你將網頁伺服器的存取紀錄儲存在資料庫中。大多數存取來自你組織的 IP 位址範圍，但有些來自其他地方（例如使用撥接連線的員工）。如果你依 IP 進行的搜尋主要是針對外部存取，那麼你大概不需要為對應到組織子網路的 IP 範圍建立索引。

假設有一個像這樣的資料表：

```

CREATE TABLE access_log (
    url varchar,
    client_ip inet,
    ...
);
```

要建立適合我們範例的部分索引，可以使用像這樣的命令：

```

CREATE INDEX access_log_client_ip_ix ON access_log (client_ip)
WHERE NOT (client_ip > inet '192.168.100.0' AND
           client_ip < inet '192.168.100.255');
```

一個可以使用這個索引的典型查詢如下：

```

SELECT *
FROM access_log
WHERE url = '/index.html' AND client_ip = inet '212.78.10.32';
```

在這裡，查詢的 IP 位址涵蓋在部分索引之內。下面的查詢無法使用這個部分索引，因為它使用的 IP 位址被排除在索引之外：

```

SELECT *
FROM access_log
WHERE url = '/index.html' AND client_ip = inet '192.168.100.23';
```

請注意，這種部分索引要求事先決定常見值，因此這類部分索引最適合用於不會改變的資料分布。這類索引可以偶爾重新建立，以因應新的資料分布，但這會增加維護的工作量。

<br>

部分索引的另一種可能用途，是將典型查詢工作負載不感興趣的值排除在索引之外；這展示於[範例 11.2](indexes-partial.md#INDEXES-PARTIAL-EX2)。這會帶來與上面所列相同的好處，但它會防止透過該索引存取「不感興趣」的值，即使在這種情況下索引掃描可能是划算的。顯然，為這類情境建立部分索引需要非常謹慎並多加實驗。

<a id="INDEXES-PARTIAL-EX2"></a>

**範例 11.2. 建立排除不感興趣之值的部分索引**

如果你有一個同時包含已開帳單與未開帳單訂單的資料表，其中未開帳單的訂單只占整個資料表的一小部分，但卻是最常被存取的資料列，那麼只為未開帳單的資料列建立索引就可以提升效能。建立該索引的命令如下所示：

```

CREATE INDEX orders_unbilled_index ON orders (order_nr)
    WHERE billed is not true;
```

一個可能使用這個索引的查詢如下：

```

SELECT * FROM orders WHERE billed is not true AND order_nr < 10000;
```

不過，這個索引也可以用於完全不涉及 `order_nr` 的查詢，例如：

```

SELECT * FROM orders WHERE billed is not true AND amount > 5000.00;
```

這不如在 `amount` 欄位上建立部分索引那樣有效率，因為系統必須掃描整個索引。然而，如果未開帳單的訂單相對較少，只用這個部分索引來找出未開帳單的訂單，可能還是划算的。

請注意，下面這個查詢無法使用這個索引：

```

SELECT * FROM orders WHERE order_nr = 3501;
```

訂單 3501 可能屬於已開帳單的訂單，也可能屬於未開帳單的訂單。

<br>

[範例 11.2](indexes-partial.md#INDEXES-PARTIAL-EX2) 也說明了被索引的欄位與述詞中使用的欄位不需要相同。PostgreSQL 支援具有任意述詞的部分索引，只要只涉及被索引之資料表的欄位即可。不過，請記住，述詞必須與那些應該從索引受益的查詢中所使用的條件相符。確切地說，只有在系統能夠辨識出查詢的 `WHERE` 條件在數學上蘊含索引的述詞時，部分索引才能用於該查詢。PostgreSQL 並沒有能夠辨識以不同形式寫出之數學等價運算式的精密定理證明器。（這樣的通用定理證明器不僅極難建立，而且大概也會慢到沒有實際用處。）系統能夠辨識簡單的不等式蘊含關係，例如「x < 1」蘊含「x < 2」；除此之外，述詞條件必須與查詢 `WHERE` 條件的某一部分完全相符，否則該索引不會被認定為可用。比對是在查詢規劃時進行的，而不是在執行時。因此，參數化的查詢子句無法搭配部分索引使用。例如，帶有參數的預備查詢可能指定「x < ?」，但對於參數所有可能的值而言，它永遠不會蘊含「x < 2」。

部分索引的第三種可能用途，完全不需要在查詢中使用該索引。這裡的想法是在資料表的某個子集上建立唯一值索引，如[範例 11.3](indexes-partial.md#INDEXES-PARTIAL-EX3) 所示。這會在滿足索引述詞的資料列之間強制唯一性，而不會限制不滿足述詞的資料列。

<a id="INDEXES-PARTIAL-EX3"></a>

**範例 11.3. 建立部分唯一值索引**

假設我們有一個描述測試結果的資料表。我們希望確保對於給定的受測對象與目標組合，只有一筆「成功」的項目，但「不成功」的項目可以有任意多筆。以下是一種做法：

```

CREATE TABLE tests (
    subject text,
    target text,
    success boolean,
    ...
);

CREATE UNIQUE INDEX tests_success_constraint ON tests (subject, target)
    WHERE success;
```

當成功的測試很少而不成功的測試很多時，這是一種特別有效率的做法。也可以藉由建立帶有 `IS NULL` 限制的唯一部分索引，讓某個欄位只允許一個 null 值。

<br>

最後，部分索引也可以用來覆寫系統的查詢計畫選擇。此外，具有特殊分布的資料集，可能會導致系統在其實不應該使用索引時使用了索引。在這種情況下，可以將索引設定成對出問題的查詢不可用。通常，PostgreSQL 對索引的使用會做出合理的選擇（例如，在擷取常見值時它會避免使用索引，因此前面的範例其實只是節省了索引的大小，並不是為了避免使用索引所必需的），而嚴重錯誤的計畫選擇則應該提出錯誤回報。

請記住，建立部分索引意味著你所知道的至少和查詢規劃器一樣多，特別是你知道什麼時候使用索引可能划算。形成這樣的知識，需要經驗以及對 PostgreSQL 索引運作方式的了解。在大多數情況下，部分索引相對於一般索引的優勢會很小。在某些情況下，它們甚至會適得其反，如[範例 11.4](indexes-partial.md#INDEXES-PARTIAL-EX4) 所示。

<a id="INDEXES-PARTIAL-EX4"></a>

**範例 11.4. 不要用部分索引取代分割**

你可能會想建立一大組互不重疊的部分索引，例如

```

CREATE INDEX mytable_cat_1 ON mytable (data) WHERE category = 1;
CREATE INDEX mytable_cat_2 ON mytable (data) WHERE category = 2;
CREATE INDEX mytable_cat_3 ON mytable (data) WHERE category = 3;
...
CREATE INDEX mytable_cat_N ON mytable (data) WHERE category = N;
```

這是個壞主意！幾乎可以肯定，使用一個像這樣宣告的非部分索引會比較好

```

CREATE INDEX mytable_cat_data ON mytable (category, data);
```

（把分類欄位放在前面，理由如[第 11.3 節](indexes-multicolumn.md)所述。）雖然在這個較大的索引中搜尋，可能比在較小的索引中搜尋多往下走幾層樹，但這幾乎可以肯定會比規劃器從部分索引中選出適當的那一個所需的工作便宜。問題的核心在於，系統並不了解這些部分索引之間的關係，因此會費力地逐一測試每個索引，看它是否適用於目前的查詢。

如果你的資料表大到單一索引真的不是好主意，你應該改為考慮使用分割（請參閱[第 5.12 節](../ddl/ddl-partitioning.md)）。透過這個機制，系統確實能夠了解資料表與索引之間互不重疊，因此可能獲得好得多的效能。

<br>

關於部分索引的更多資訊，可以在 [[ston89b]](../../bibliography.md#STON89B)、[[olson93]](../../bibliography.md#OLSON93) 與 [[seshadri95]](../../bibliography.md#SESHADRI95) 中找到。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-partial.html)（原文版本：18.6；核對日期：2026-09-13）
