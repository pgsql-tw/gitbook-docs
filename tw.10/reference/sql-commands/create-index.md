---
description: 版本：10
---

# CREATE INDEX

CREATE INDEX — 定義一個新的索引

### 語法

```text
CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ] name ] ON table_name [ USING method ]
    ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
    [ WITH ( storage_parameter = value [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    [ WHERE predicate ]
```

### 說明

CREATE INDEX 在指定關連的指定欄位上建構索引，該索引可以是資料表或具體化檢視表。索引主要用於增強資料庫效能（儘管不恰當的使用會導致效能降低）。

索引的主要欄位指定欄位名稱，或者作為括號中的表示式指定。如果索引方法支援多欄位索引，則可以指定多個欄位。

索引欄位可以是根據資料表的一個欄位或多個欄位的計算表示式。此功能可用於基於對基本資料的某些轉換來快速存取資料。例如，在 upper\(col\) 上計算的索引將允許子句 WHERE upper\(col\) = 'JIM' 使用索引。

PostgreSQL 提供索引方法 B-tree，hash，GiST，SP-GiST，GIN 和 BRIN。使用者也可以定義自己的索引方法，但這相當複雜。

WHERE子句存在時，將建立部分索引。部分索引是一個索引，它只包含資料表的一部分項目，通常是比索引的其餘部分更有用的索引部分。例如，如果您的資料表包含已開票和未開單的訂單，其中未開單的訂單佔據總資料表的一小部分，但這是一個經常使用的部分，您可以透過僅在該部分上建立索引來提高效能。另一個可能的應用是使用帶有 UNIQUE 的 WHERE 來強制資料表子集的唯一性。有關更多討論，請參閱[第 11.8 節](../../the-sql-language/index/partial-indexes.md)。

WHERE 子句中使用的表示式只能引用基礎資料表的欄位，但它可以使用所有欄位，而不僅僅是被索引的欄位。目前，WHERE 中也禁止使用子查詢和彙總資料表示式。相同的限制適用於作為表示式的索引欄位。

索引定義中使用的所有函數和運算符必須是「immutable」，也就是說，它們的結果必須僅依賴於它們的參數，而不是任何外部影響（例如另一個資料表的內容或目前時間）。此限制可確保明確定義索引的行為。要在索引表示式或 WHERE 子句中使用使用者定義的函數，請記住在建立函數時將該函數標記為 immutable。

### 參數

`UNIQUE`

在建立索引時（如果資料已存在）並且每次插入資料時，系統都會檢查資料表中的重複值。嘗試插入或更新如果導致重複項目的資料將產生錯誤。

`CONCURRENTLY`

使用此選項時，PostgreSQL 將在建立索引時，不會採取任何阻止資料表上同時的插入，更新或刪除的鎖定；而標準索引建立會鎖定資料表上的寫入（但不是讀取），直到完成為止。使用此選項時需要注意幾點 - 請參閱[同步建立索引](create-index.md#tong-bu-jian-li-suo-yin)。

`IF NOT EXISTS`

如果已存在具有相同名稱的關連，請不要拋出錯誤，在這種情況下發出 NOTICE。請注意，無法保證現有索引與已建立的索引類似。指定 IF NOT EXISTS 時需要索引名稱。

_`name`_

要建立的索引名稱。這裡不能包含綱要名稱；索引始終在與其父資料表相同的綱要中創建。如果省略該名稱，PostgreSQL會根據父資料表的名稱和索引的欄位名稱選擇合適的名稱。

_`table_name`_

要編制索引的資料表名稱（可以加上綱要名稱）。

_`method`_

要使用的索引方法的名稱。選項是 btree，hash，gist，spgist，gin 和 brin。預設方法是 btree。

_`column_name`_

資料表欄位的名稱。

_`expression`_

基於資料表的一個欄位或多個欄位的表示式。表示式通常必須與周圍的括號一起填寫，如語法中所示。但是，如果表示式具有函數呼叫的形式，則可以省略括號。

_`collation`_

用於索引的排序規則的名稱。預設情況下，索引使用為要索引的欄位宣告排序規則或要索引的表示式結果排序規則。具有非預設排序規則的索引對於涉及使用非預設排序規則的表示式查詢非常有用。

_`opclass`_

運算子類的名稱。請參閱下文了解詳情。

`ASC`

指定遞增排序順序（預設值）。

`DESC`

指定遞減排序。

`NULLS FIRST`

指定 nulls 排在非 null 之前。這是指定 DESC 時的預設值。

`NULLS LAST`

指定 nulls 排在非 null 之後。這是未指定 DESC 時的預設值。

_`storage_parameter`_

特定於索引方法的儲存參數的名稱。有關詳情，請參見[索引儲存參數](create-index.md#suo-yin-cun)。

_`tablespace_name`_

用於建立索引的資料表空間。如果未指定，則查詢 [default\_tablespace](../../server-administration/server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#default_tablespace-string)，或臨時資料表 [temp\_tablespaces](../../server-administration/server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#temp_tablespaces-string)。

_`predicate`_

部分索引的限制條件表示式。

#### 索引儲存參數

選擇性的 WITH 子句指定索引的儲存參數。每個索引方法都有自己的一組允許的儲存參數。B-tree，hash，GiST 和 SP-GiST 索引方法都接受此參數：

`fillfactor`

索引的 fillfactor 一個百分比，用於確定索引方法嘗試填充索引頁面的程度。對於B-tree，在初始索引建構期間以及在右側擴展索引時（在插入新的最大索引值時），葉子頁面將填充到此百分比。 如果頁面隨後變得完整，它們將被拆分，導致索引效率逐漸下降。B-tree 使用預設的 fillfactor 為90，但可以選擇 10 到 100 之間的任何整數值。如果資料表是靜態的，那麼 fillfactor 100 能最小化索引的實體大小，但是對於大量更新的資料表，較小的 fillfactor 能最小化頁面拆分的需要。其他索引方法以不同但大致類似的方式使用 fillfactor；預設的 fillfactor 會因方法而異。

GiST 索引另外接受此參數：

`buffering`

確定是否使用[第 62.4.1 節](../../internals/gist-indexes/implementation.md#62-4-1-gist-buffering-build)中描述的緩衝建構技術來建構索引。使用 OFF 時，它被停用，ON 時啟用。當使用 AUTO 時，它最初被停用，但一旦索引大小達到 [effective\_cache\_size](../../server-administration/server-configuration/query-planning.md#19-7-2-planner-cost-constants)，就會立即打開。預設值為 AUTO。

GIN 索引接受不同的參數：

`fastupdate`

此設定控制[第 64.4.1 節](../../internals/64.-gin-suo-yin/64.4.-implementation.md#64-4-1-gin-fast-update-technique)中描述的快速更新技術的運用。它是一個布林參數：ON 啟用快速更新，OFF 停用它。 （如[第 19.1 節](../../server-administration/server-configuration/19.1.-setting-parameters.md)所述，允許使用 ON 和 OFF 的替代拼寫。）預設為 ON。

#### 提醒

透過 ALTER INDEX 關閉 fastupdate 可防止將來的插入進入擱置的索引項目列表，但本身不會更新以前的項目。您可能希望 VACUUM 資料表或之後呼叫 gin\_clean\_pending\_list 函數以確保清空擱置列表。

`gin_pending_list_limit`

自定義 [gin\_pending\_list\_limit](../../server-administration/server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#gin_pending_list_limit-integer) 參數。此值以 KB 為單位。

BRIN 索引接受不同的參數：

`pages_per_range`

定義構成 BRIN 索引每個項目的一個區塊範圍的資料表區塊數（有關更多詳細訊息，請參閱[第 65.1 節](../../internals/brin/introduction.md)）。預設值為 128。

`autosummarize`

定義每當在下一個頁面上檢測到插入時是否為前一頁面範圍進行摘要。

#### 同步建立索引

建立索引可能會干擾資料庫的日常操作。通常，PostgreSQL 會鎖定要對寫入進行索引的資料表，並通過對資料的單次掃描來執行整個索引建構。其他事務仍然可以讀取資料表，但如果它們嘗試插入，更新或刪除資料表中的資料列，它們將被阻擋，直到索引建構完成。如果系統是線上正式資料庫，這可能會產生嚴重影響。非常大的資料表可能需要很長時間才能被編入索引，即使對於較小的資料表，索引建構也可能會鎖定寫入程序，這些時間對於線上正式系統來說是不可接受的。

PostgreSQL 支援建構索引而不會鎖定寫入。透過指定 CREATE INDEX 的 CONCURRENTLY 選項來呼叫此方法。使用此選項時，PostgreSQL 必須對資料執行兩次掃描，此外，它必須等待可能修改或使用索引的所有事務。因此，這種方法比標準索引建構需要更多的工作，也需要更長的時間來完成。但是，由於它允許在建構索引時繼續正常操作，因此此方法對於在正式環境中增加新的索引很有用。當然，索引建立帶來的額外 CPU 和 I/O 負載可能會減慢其他操作。

在同步索引建構時，索引實際上在一個交易事務中輸入到系統目錄，然後在另外兩個事務中産生兩個資料表掃描。在每次掃描資料表之前，索引建構必須等待已修改資料表的現有事務結束。在第二次掃描之後，索引建構必須等待具有快照（參閱[第 13 章](../../the-sql-language/concurrency-control/)）的任何事務在第二次掃描之前結束。最後，索引可以標記為可以使用，然後 CREATE INDEX 指令完成。但是，即使這樣，索引也可能無法立即用於查詢：在最壞的情況下，只要在索引建構開始之前存在事務，都不能使用它。

如果在掃描資料表時出現問題，例如鎖死或唯一索引中的唯一性違規，則 CREATE INDEX 指令將會失敗但留下「無效」索引。出於查詢目的，該索引將被忽略，因為它可能不完整；但它仍然會消耗更新成本。psql \d 指令將回報此類索引為 INVALID：

```text
postgres=# \d tab
       Table "public.tab"
 Column |  Type   | Collation | Nullable | Default 
--------+---------+-----------+----------+---------
 col    | integer |           |          | 
Indexes:
    "idx" btree (col) INVALID
```

在這種情況下，建議的恢復方法是刪除索引並再次嘗試同時執行 CREATE INDEX。（另一種可能性是使用 REINDEX 重建索引。但是，由於 REINDEX 不支持同步建構，因此該選項看起來不太有吸引力。）

同時建構唯一索引時的另一個警告是，當第二個資料表掃描開始時，已經對其他事務強制加上唯一性限制條件。這意味著在索引可供使用之前，甚至在索引建構最終失敗的情況下，可以在其他查詢中回報違反限制條件。此外，如果在第二次掃描中確實發生了故障，則「無效」索引將繼續強制執行其唯一性約束。

表示式索引和部分索引的同步建構也是支援的。在評估這些表示式時發生的錯誤可能導致類似於上面針對唯一性違規所描述的行為。

一般索引建立允許同一資料表上的其他一般索引建立同時執行，但一次只能在一個資料表上進行一個同步索引構立。在這兩種情況下，同時不允許在資料表上進行其他類型的結構變更。另一個區別是可以在事務塊中執行一般的 CREATE INDEX 指令，但 CREATE INDEX CONCURRENTLY 不能。

### 注意

有關何時可以使用索引，何時不使用索引以及哪些特定情況可以使用索引的訊息，請參閱[第 11 章](../../the-sql-language/index/)。

目前，只有B-tree，GiST，GIN 和 BRIN 索引方法支持多欄位索引。預設情況下最多可以指定 32 個欄位。（編譯 PostgreSQL 時可以變更此限制。）只有 B-tree 目前支援唯一索引。

可以為索引的每個欄位指定運算子類。運算子類識別該欄位的索引要使用的運算子。例如，4 bytes 整數的 B-tree 索引將使用 int4\_ops 類；此運算子類包括 4 bytes 整數的比較函數。實際上，欄位資料型別的預設運算子類通常就足夠了。擁有運算子類的要點是，對於某些資料型別，可能存在多個有意義的排序。例如，我們可能希望按絕對值或複數資料型別的實部進行排序。我們可以透過為資料型別定義兩個運算子類，然後在建立索引時選擇適當的類。有關運算子類的更多訊息，請參閱[第 11.9 節](../../the-sql-language/index/operator-classes-and-operator-families.md)和[第 37.14 節](../../server-programming/extending-sql/interfacing-extensions-to-indexes.md)。

對於支援有序掃描的索引方法（目前只有 B-tree），可以指定選擇性子句 ASC，DESC，NULLS FIRST 和 NULLS LAST 來修改索引的排序順序。由於可以向前或向後掃描有序索引，因此建立單欄位 DESC 索引並不常用 - 排序順序已經可用於一般性索引。這些選項的值是可以建立多欄位索引，該索引搭配混合排序查詢所請求的排序順序，例如 SELECT ... ORDER BY x ASC, y DESC。如果您需要在依賴於索引以避免排序步驟的查詢中支援「nulls sort low」行為而不是預設的「nulls sort high」，那麼 NULLS 選項很有用。

對於大多數索引方法，建立索引的速度取決於 [maintenance\_work\_mem](../../server-administration/server-configuration/resource-consumption.md#19-4-1) 的設定。較大的值將減少索引建立所需的時間，只要您不要使其大於真正可用的記憶體大小，否則將驅使主機使用 SWAP。

使用 [DROP INDEX](drop-index.md) 移除索引。

PostgreSQL 的早期版本也有一個 R-tree 索引方法。此方法已被移除，因為它沒有 GiST 方法的顯著優勢。如果指定了 USING rtree，CREATE INDEX 會將其解釋為USING gist，以簡化舊資料庫到 GiST 的轉換。

### 範例

要在資料表中的欄位 title 上建立 B-tree 索引：

```text
CREATE UNIQUE INDEX title_idx ON films (title);
```

要在表示式 lower\(title\) 上建立索引，允許有效的不分大小寫搜尋：

```text
CREATE INDEX ON films ((lower(title)));
```

（在此範例中，我們選擇省略索引名稱，因此系統將選擇一個名稱，通常為 films\_lower\_idx。）

要使用非預設排序規則建立索引：

```text
CREATE INDEX title_idx_german ON films (title COLLATE "de_DE");
```

要建立具有空值的非預設排序順序索引：

```text
CREATE INDEX title_idx_nulls_low ON films (title NULLS FIRST);
```

要使用非預設 fill factor 建立索引：

```text
CREATE UNIQUE INDEX title_idx ON films (title) WITH (fillfactor = 70);
```

要建立停用快速更新的 GIN 索引：

```text
CREATE INDEX gin_idx ON documents_table USING GIN (locations) WITH (fastupdate = off);
```

要在資料表 film 中的欄位 code 上建立索引，並將索引放在資料表空間 indexspace 中：

```text
CREATE INDEX code_idx ON films (code) TABLESPACE indexspace;
```

要在 point 屬性上建立 GiST 索引，以便我們可以在轉換函數的結果上有效地使用 box 運算子：

```text
CREATE INDEX pointloc
    ON points USING gist (box(location,location));
SELECT * FROM points
    WHERE box(location,location) && '(0,0),(1,1)'::box;
```

要建立索引但不鎖定對資料表的寫入：

```text
CREATE INDEX CONCURRENTLY sales_quantity_index ON sales_table (quantity);
```

### 相容性

CREATE INDEX 是 PostgreSQL 延伸語法。SQL 標準中沒有索引的規定。

### 參閱

[ALTER INDEX](alter-index.md), [DROP INDEX](drop-index.md)

