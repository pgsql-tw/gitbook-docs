<a id="DDL-PARTITIONING"></a>

## 5.12. 資料表分割 [#](#DDL-PARTITIONING)

[5.12.1. 概觀](ddl-partitioning.md#DDL-PARTITIONING-OVERVIEW)

[5.12.2. 宣告式分割](ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE)

[5.12.3. 使用繼承進行分割](ddl-partitioning.md#DDL-PARTITIONING-USING-INHERITANCE)

[5.12.4. 分割區修剪](ddl-partitioning.md#DDL-PARTITION-PRUNING)

[5.12.5. 分割與限制條件排除](ddl-partitioning.md#DDL-PARTITIONING-CONSTRAINT-EXCLUSION)

[5.12.6. 宣告式分割的最佳實務](ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES)

<a id="id-1.5.4.14.2"></a><a id="id-1.5.4.14.3"></a><a id="id-1.5.4.14.4"></a>

PostgreSQL 支援基本的資料表分割。本節說明為什麼以及如何在資料庫設計中實作分割。

<a id="DDL-PARTITIONING-OVERVIEW"></a>

### 5.12.1. 概觀 [#](#DDL-PARTITIONING-OVERVIEW)

分割（partitioning）是指將邏輯上的一個大型資料表拆分成較小的實體片段。分割可以帶來幾項好處：

* 在某些情況下可以大幅提升查詢效能，特別是當資料表中大部分經常被存取的資料列，都位於單一分割區或少數幾個分割區中時。分割實際上取代了索引樹的上層，使得索引中經常使用的部分更有可能放得進記憶體。
* 當查詢或更新存取單一分割區的很大比例時，可以對該分割區使用循序掃描而不是使用索引來提升效能，因為使用索引需要散布在整個資料表中的隨機存取讀取。
* 如果在分割設計中考慮到使用模式，就可以藉由加入或移除分割區來完成大量的載入與刪除。使用 `DROP TABLE` 刪除個別的分割區，或執行 `ALTER TABLE DETACH PARTITION`，都比大量操作快得多。這些命令也完全避免了大量 `DELETE` 所造成的 `VACUUM` 額外負擔。
* 很少使用的資料可以遷移到較便宜、較慢的儲存媒體上。

通常只有在資料表原本會非常大時，這些好處才值得。資料表在什麼程度下才會從分割中受益，確切的界線取決於應用程式，不過一個經驗法則是，資料表的大小應該超過資料庫伺服器的實體記憶體。

PostgreSQL 為下列幾種分割形式提供內建支援：

<a id="DDL-PARTITIONING-OVERVIEW-RANGE"></a>

範圍分割 [#](#DDL-PARTITIONING-OVERVIEW-RANGE)
:   資料表依一個鍵欄位或一組欄位所定義的「範圍」進行分割，指派給不同分割區的值範圍之間沒有重疊。例如，可以依日期範圍，或依特定業務物件之識別碼的範圍進行分割。每個範圍的界限都被理解為下限包含、上限不包含。例如，如果某個分割區的範圍是從 `1` 到 `10`，而下一個分割區的範圍是從 `10` 到 `20`，那麼值 `10` 屬於第二個分割區，而不是第一個。
<a id="DDL-PARTITIONING-OVERVIEW-LIST"></a>

清單分割 [#](#DDL-PARTITIONING-OVERVIEW-LIST)
:   藉由明確列出每個分割區中會出現哪些鍵值來分割資料表。
<a id="DDL-PARTITIONING-OVERVIEW-HASH"></a>

雜湊分割 [#](#DDL-PARTITIONING-OVERVIEW-HASH)
:   藉由為每個分割區指定一個模數與一個餘數來分割資料表。每個分割區會保存那些分割鍵的雜湊值除以指定模數之後，會產生指定餘數的資料列。

如果你的應用程式需要使用上面沒有列出的其他分割形式，可以改用繼承與 `UNION ALL` 檢視表等替代方法。這些方法提供了彈性，但不具備內建宣告式分割的某些效能優勢。

<a id="DDL-PARTITIONING-DECLARATIVE"></a>

### 5.12.2. 宣告式分割 [#](#DDL-PARTITIONING-DECLARATIVE)

PostgreSQL 允許你宣告一個資料表被劃分為多個分割區。被劃分的資料表稱為*分割資料表*（partitioned table）。這項宣告包含如上所述的*分割方法*（partitioning method），再加上一份用作*分割鍵*（partition key）的欄位或運算式清單。

分割資料表本身是一個沒有自己儲存空間的「虛擬」資料表。儲存空間屬於*分割區*（partition），它們是與分割資料表相關聯、在其他方面都與一般資料表無異的資料表。每個分割區儲存由其*分割區界限*（partition bounds）所定義的資料子集。所有插入分割資料表的資料列，都會依據分割鍵欄位的值，被導向到適當的分割區。更新資料列的分割鍵時，如果它不再滿足原本所屬分割區的分割區界限，就會使該資料列被移動到另一個分割區。

分割區本身也可以定義為分割資料表，形成*子分割*（sub-partitioning）。雖然所有分割區都必須與其分割父資料表具有相同的欄位，但分割區可以有自己的索引、限制條件與預設值，且可與其他分割區的對應物不同。關於建立分割資料表與分割區的更多細節，請參閱 [CREATE TABLE](../../reference/sql-commands/sql-createtable.md)。

無法將一般資料表轉換為分割資料表，反之亦然。不過，可以將現有的一般資料表或分割資料表加入為某個分割資料表的分割區，或是從分割資料表移除某個分割區，使它成為獨立的資料表；這可以簡化並加快許多維護程序。關於 `ATTACH PARTITION` 與 `DETACH PARTITION` 子命令的更多資訊，請參閱 [ALTER TABLE](../../reference/sql-commands/sql-altertable.md)。

分割區也可以是[外部資料表](ddl-foreign-data.md)，不過需要相當謹慎，因為此時確保外部資料表的內容滿足分割規則，就成了使用者的責任。此外還有其他一些限制。更多資訊請參閱 [CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md)。

<a id="DDL-PARTITIONING-DECLARATIVE-EXAMPLE"></a>

#### 5.12.2.1. 範例 [#](#DDL-PARTITIONING-DECLARATIVE-EXAMPLE)

假設我們正在為一家大型冰淇淋公司建構資料庫。這家公司每天都會量測各地區的最高氣溫以及冰淇淋銷售量。概念上，我們想要一個像這樣的資料表：

```

CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
);
```

我們知道大多數查詢只會存取最近一週、一個月或一季的資料，因為這個資料表的主要用途，是為管理階層準備線上報表。為了減少需要儲存的舊資料量，我們決定只保留最近 3 年的資料。每個月初，我們會移除最舊一個月的資料。在這種情況下，我們可以使用分割來幫助我們滿足量測資料表的各種不同需求。

要在這種情況下使用宣告式分割，請依照下列步驟：

1. 藉由指定 `PARTITION BY` 子句，將 `measurement` 資料表建立為分割資料表；這個子句包含分割方法（在這個例子中是 `RANGE`），以及要用作分割鍵的欄位清單。

   ```

   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   ) PARTITION BY RANGE (logdate);
   ```
2. 建立分割區。每個分割區的定義都必須指定與父資料表之分割方法及分割鍵相對應的界限。請注意，如果指定的界限使新分割區的值與一個或多個現有分割區的值重疊，就會引發錯誤。

   以這種方式建立的分割區，在各方面都是一般的 PostgreSQL 資料表（或者也可能是外部資料表）。可以為每個分割區分別指定資料表空間與儲存參數。

   在我們的範例中，每個分割區應該保存一個月的資料，以符合一次刪除一個月資料的需求。所以命令可能如下所示：

   ```

   CREATE TABLE measurement_y2006m02 PARTITION OF measurement
       FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');

   CREATE TABLE measurement_y2006m03 PARTITION OF measurement
       FOR VALUES FROM ('2006-03-01') TO ('2006-04-01');

   ...
   CREATE TABLE measurement_y2007m11 PARTITION OF measurement
       FOR VALUES FROM ('2007-11-01') TO ('2007-12-01');

   CREATE TABLE measurement_y2007m12 PARTITION OF measurement
       FOR VALUES FROM ('2007-12-01') TO ('2008-01-01')
       TABLESPACE fasttablespace;

   CREATE TABLE measurement_y2008m01 PARTITION OF measurement
       FOR VALUES FROM ('2008-01-01') TO ('2008-02-01')
       WITH (parallel_workers = 4)
       TABLESPACE fasttablespace;
   ```

   （回想一下，相鄰的分割區可以共用同一個界限值，因為範圍的上限被視為不包含的界限。）

   如果你想要實作子分割，同樣在用來建立個別分割區的命令中指定 `PARTITION BY` 子句，例如：

   ```

   CREATE TABLE measurement_y2006m02 PARTITION OF measurement
       FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')
       PARTITION BY RANGE (peaktemp);
   ```

   在建立 `measurement_y2006m02` 的分割區之後，任何插入 `measurement` 中、且對應到 `measurement_y2006m02` 的資料（或直接插入 `measurement_y2006m02` 的資料，只要滿足其分割區限制條件就是允許的），都會依據 `peaktemp` 欄位，進一步被重新導向到它的其中一個分割區。所指定的分割鍵可以與父資料表的分割鍵重疊，不過在指定子分割區的界限時應該小心，使它所接受的資料集合構成該分割區本身界限所允許之資料的子集；系統並不會嘗試檢查實際上是否如此。

   將無法對應到任何現有分割區的資料插入父資料表，會引發錯誤；必須手動加入適當的分割區。

   不需要為分割區手動建立描述分割區邊界條件的資料表限制條件。這類限制條件會自動建立。
3. 在分割資料表的鍵欄位上建立索引，以及你可能想要的任何其他索引。（鍵索引並非絕對必要，但在大多數情境下都很有幫助。）這會自動在每個分割區上建立相對應的索引，而且之後建立或附加的任何分割區也都會有這樣的索引。在分割資料表上宣告的索引或唯一限制條件，就像分割資料表一樣是「虛擬」的：實際的資料位於個別分割區資料表上的子索引中。

   ```

   CREATE INDEX ON measurement (logdate);
   ```
4. 確認 [enable_partition_pruning](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING) 組態參數沒有在 `postgresql.conf` 中被停用。如果被停用了，查詢就不會如預期般被最佳化。

在上面的範例中，我們每個月都會建立一個新的分割區，所以撰寫一個自動產生所需 DDL 的指令碼可能是明智的做法。

<a id="DDL-PARTITIONING-DECLARATIVE-MAINTENANCE"></a>

#### 5.12.2.2. 分割區維護 [#](#DDL-PARTITIONING-DECLARATIVE-MAINTENANCE)

通常，在最初定義資料表時所建立的分割區集合，並不打算一直保持不變。移除保存舊資料的分割區，並定期為新資料加入新的分割區，是很常見的需求。分割最重要的優點之一，正是它讓這項原本很麻煩的工作，可以藉由操作分割結構而幾乎在瞬間完成，而不必實際搬移大量的資料。

移除舊資料最簡單的做法，是刪除不再需要的分割區：

```

DROP TABLE measurement_y2006m02;
```

這可以非常快速地刪除數百萬筆記錄，因為它不必逐筆刪除每一筆記錄。不過請注意，上面的命令需要在父資料表上取得 `ACCESS EXCLUSIVE` 鎖定。

另一種往往更可取的做法，是將分割區從分割資料表中移除，但保留以獨立資料表的形式存取它。這有兩種形式：

```

ALTER TABLE measurement DETACH PARTITION measurement_y2006m02;
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02 CONCURRENTLY;
```

這讓你可以在該分割區資料表被刪除之前，先對其中的資料進行進一步操作。例如，這通常是使用 `COPY`、pg_dump 或類似工具備份資料的好時機。這也可能是將資料彙總成較小格式、進行其他資料操作或產生報表的好時機。第一種形式的命令需要父資料表上的 `ACCESS EXCLUSIVE` 鎖定。如第二種形式那樣加上 `CONCURRENTLY` 修飾詞，可以讓分離操作只需要父資料表上的 `SHARE UPDATE EXCLUSIVE` 鎖定，但關於其限制的細節，請參閱 [`ALTER TABLE ... DETACH PARTITION`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-DETACH-PARTITION)。

同樣地，我們可以加入一個新的分割區來處理新的資料。我們可以像上面建立原始分割區那樣，在分割資料表中建立一個空的分割區：

```

CREATE TABLE measurement_y2008m02 PARTITION OF measurement
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01')
    TABLESPACE fasttablespace;
```

除了建立新的分割區之外，有時候先在分割結構之外建立一個新的資料表，之後再把它附加為分割區，會比較方便。這讓新資料可以在出現於分割資料表之前，先進行載入、檢查與轉換。此外，`ATTACH PARTITION` 操作只需要分割資料表上的 `SHARE UPDATE EXCLUSIVE` 鎖定，而不是 `CREATE TABLE ... PARTITION OF` 所需要的 `ACCESS EXCLUSIVE` 鎖定，因此它對分割資料表上的並行操作比較友善；更多細節請參閱 [`ALTER TABLE ... ATTACH PARTITION`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-ATTACH-PARTITION)。[`CREATE TABLE ... LIKE`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-LIKE) 選項可以幫助避免繁瑣地重複父資料表的定義；例如：

```

CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS)
  TABLESPACE fasttablespace;

ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' );

\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work

ALTER TABLE measurement ATTACH PARTITION measurement_y2008m02
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01' );
```

請注意，執行 `ATTACH PARTITION` 命令時，會在持有該分割區上之 `ACCESS EXCLUSIVE` 鎖定的情況下掃描資料表，以驗證分割區限制條件。如上所示，建議在附加資料表之前，先在該資料表上建立一個符合預期分割區限制條件的 `CHECK` 限制條件，以避免這次掃描。`ATTACH PARTITION` 完成之後，建議刪除現在已經多餘的 `CHECK` 限制條件。如果要附加的資料表本身是一個分割資料表，那麼它的每個子分割區都會被遞迴地鎖定與掃描，直到遇到合適的 `CHECK` 限制條件或抵達葉分割區為止。

同樣地，如果分割資料表有 `DEFAULT` 分割區，建議建立一個排除即將附加之分割區限制條件的 `CHECK` 限制條件。如果不這麼做，就會掃描 `DEFAULT` 分割區，以確認其中不包含應該位於即將附加之分割區中的記錄。這項操作會在持有 `DEFAULT` 分割區上之 `ACCESS EXCLUSIVE` 鎖定的情況下進行。如果 `DEFAULT` 分割區本身是一個分割資料表，那麼它的每個分割區都會以與上述附加資料表相同的方式被遞迴檢查。

如前所述，可以在分割資料表上建立索引，使它們自動套用到整個階層。這非常方便，因為不只所有現有的分割區會建立索引，未來的任何分割區也都會。不過，在分割資料表上建立新索引的一項限制是，無法使用 `CONCURRENTLY` 修飾詞，而這可能導致長時間的鎖定。為了避免這種情況，你可以在分割資料表上使用 `CREATE INDEX ON ONLY`，它會建立一個被標記為無效的新索引，防止自動套用到現有的分割區。接著，可以使用 `CONCURRENTLY` 在每個分割區上個別建立索引，並使用 `ALTER INDEX ... ATTACH PARTITION` 將它們*附加*到父資料表上的分割索引。一旦所有分割區的索引都附加到父索引之後，父索引就會自動被標記為有效。例如：

```

CREATE INDEX measurement_usls_idx ON ONLY measurement (unitsales);

CREATE INDEX CONCURRENTLY measurement_usls_200602_idx
    ON measurement_y2006m02 (unitsales);
ALTER INDEX measurement_usls_idx
    ATTACH PARTITION measurement_usls_200602_idx;
...
```

這項技巧也可以搭配 `UNIQUE` 與 `PRIMARY KEY` 限制條件使用；在建立限制條件時，索引會被隱含地建立。例如：

```

ALTER TABLE ONLY measurement ADD UNIQUE (city_id, logdate);

ALTER TABLE measurement_y2006m02 ADD UNIQUE (city_id, logdate);
ALTER INDEX measurement_city_id_logdate_key
    ATTACH PARTITION measurement_y2006m02_city_id_logdate_key;
...
```

<a id="DDL-PARTITIONING-DECLARATIVE-LIMITATIONS"></a>

#### 5.12.2.3. 限制 [#](#DDL-PARTITIONING-DECLARATIVE-LIMITATIONS)

分割資料表有下列限制：

* 要在分割資料表上建立唯一或主鍵限制條件，分割鍵不得包含任何運算式或函式呼叫，而且限制條件的欄位必須包含所有分割鍵欄位。之所以有這項限制，是因為構成該限制條件的個別索引，只能直接在各自的分割區內強制唯一性；因此，分割結構本身必須保證不同的分割區之間不會有重複。
* 同樣地，排除限制條件必須包含所有分割鍵欄位。此外，限制條件必須以相等比較這些欄位（而不是例如 `&&`）。同樣地，這項限制源自於無法強制執行跨分割區的限制。限制條件可以包含不屬於分割鍵的其他欄位，並且可以用任何你喜歡的運算子比較這些欄位。
* `INSERT` 上的 `BEFORE ROW` 觸發程序，無法改變新資料列最終要放入哪一個分割區。
* 不允許在同一棵分割樹中混用暫時性與永久性關聯。因此，如果分割資料表是永久性的，它的分割區也必須是永久性的；分割資料表是暫時性時亦然。使用暫時性關聯時，分割樹的所有成員都必須來自同一個工作階段。

在幕後，個別的分割區是透過繼承與其分割資料表相連結的。不過，如下所述，並非所有繼承的一般功能都能用於宣告式分割資料表或其分割區。值得注意的是，分割區除了它所屬的分割資料表之外，不能有任何其他父資料表，而且一個資料表也不能同時繼承分割資料表與一般資料表。這表示分割資料表及其分割區永遠不會與一般資料表共用同一個繼承階層。

由於由分割資料表及其分割區組成的分割階層仍然是一個繼承階層，因此 `tableoid` 以及繼承的所有一般規則都適用，如[第 5.11 節](ddl-inherit.md)所述，但有少數例外：

* 分割區不能有父資料表中不存在的欄位。使用 `CREATE TABLE` 建立分割區時無法指定欄位，也無法在事後使用 `ALTER TABLE` 為分割區加入欄位。只有當資料表的欄位與父資料表完全相符時，才能以 `ALTER TABLE ... ATTACH PARTITION` 將它加入為分割區。
* 分割資料表的 `CHECK` 與 `NOT NULL` 限制條件，一律會被其所有分割區繼承；不允許建立這些類型的 `NO INHERIT` 限制條件。如果父資料表中存在相同的限制條件，你就無法刪除這些類型的限制條件。
* 只要還沒有任何分割區，就支援使用 `ONLY` 只在分割資料表上加入或刪除限制條件。一旦分割區存在，對 `UNIQUE` 與 `PRIMARY KEY` 以外的任何限制條件使用 `ONLY`，都會導致錯誤。取而代之的是，可以在分割區本身加入限制條件，並（在父資料表中不存在該限制條件時）刪除它們。
* 由於分割資料表本身沒有任何資料，嘗試對分割資料表使用 `TRUNCATE` `ONLY` 一律會回傳錯誤。

<a id="DDL-PARTITIONING-USING-INHERITANCE"></a>

### 5.12.3. 使用繼承進行分割 [#](#DDL-PARTITIONING-USING-INHERITANCE)

雖然內建的宣告式分割適用於大多數常見的使用情境，但在某些情況下，更有彈性的做法可能會很有用。可以使用資料表繼承來實作分割，這可以支援一些宣告式分割不支援的功能，例如：

* 在宣告式分割中，分割區必須與分割資料表具有完全相同的欄位集合；而使用資料表繼承時，子資料表可以有父資料表中不存在的額外欄位。
* 資料表繼承允許多重繼承。
* 宣告式分割只支援範圍、清單與雜湊分割；而資料表繼承則允許以使用者選擇的方式劃分資料。（不過請注意，如果限制條件排除無法有效地修剪子資料表，查詢效能可能會很差。）

<a id="DDL-PARTITIONING-INHERITANCE-EXAMPLE"></a>

#### 5.12.3.1. 範例 [#](#DDL-PARTITIONING-INHERITANCE-EXAMPLE)

這個範例會建立一個與上面宣告式分割範例等價的分割結構。請依照下列步驟：

1. 建立「根」資料表，所有「子」資料表都將繼承自它。這個資料表不會包含任何資料。除非你打算讓檢查限制條件同樣地套用到所有子資料表，否則不要在這個資料表上定義任何檢查限制條件。在它上面定義任何索引或唯一限制條件也沒有意義。在我們的範例中，根資料表就是最初定義的 `measurement` 資料表：

   ```

   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   );
   ```
2. 建立數個各自繼承自根資料表的「子」資料表。通常，這些資料表不會在從根資料表繼承的欄位集合之外再加入任何欄位。就像宣告式分割一樣，這些資料表在各方面都是一般的 PostgreSQL 資料表（或外部資料表）。

   ```

   CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
   CREATE TABLE measurement_y2006m03 () INHERITS (measurement);
   ...
   CREATE TABLE measurement_y2007m11 () INHERITS (measurement);
   CREATE TABLE measurement_y2007m12 () INHERITS (measurement);
   CREATE TABLE measurement_y2008m01 () INHERITS (measurement);
   ```
3. 為子資料表加入互不重疊的資料表限制條件，定義每個子資料表中允許的鍵值。

   典型的例子如下：

   ```

   CHECK ( x = 1 )
   CHECK ( county IN ( 'Oxfordshire', 'Buckinghamshire', 'Warwickshire' ))
   CHECK ( outletID >= 100 AND outletID < 200 )
   ```

   請確保這些限制條件保證不同子資料表所允許的鍵值之間沒有重疊。一個常見的錯誤是設定像這樣的範圍限制條件：

   ```

   CHECK ( outletID BETWEEN 100 AND 200 )
   CHECK ( outletID BETWEEN 200 AND 300 )
   ```

   這是錯的，因為無法確定鍵值 200 屬於哪一個子資料表。範圍應該改為以這種方式定義：

   ```

   CREATE TABLE measurement_y2006m02 (
       CHECK ( logdate >= DATE '2006-02-01' AND logdate < DATE '2006-03-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2006m03 (
       CHECK ( logdate >= DATE '2006-03-01' AND logdate < DATE '2006-04-01' )
   ) INHERITS (measurement);

   ...
   CREATE TABLE measurement_y2007m11 (
       CHECK ( logdate >= DATE '2007-11-01' AND logdate < DATE '2007-12-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2007m12 (
       CHECK ( logdate >= DATE '2007-12-01' AND logdate < DATE '2008-01-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2008m01 (
       CHECK ( logdate >= DATE '2008-01-01' AND logdate < DATE '2008-02-01' )
   ) INHERITS (measurement);
   ```
4. 為每個子資料表在鍵欄位上建立索引，以及你可能想要的任何其他索引。

   ```

   CREATE INDEX measurement_y2006m02_logdate ON measurement_y2006m02 (logdate);
   CREATE INDEX measurement_y2006m03_logdate ON measurement_y2006m03 (logdate);
   CREATE INDEX measurement_y2007m11_logdate ON measurement_y2007m11 (logdate);
   CREATE INDEX measurement_y2007m12_logdate ON measurement_y2007m12 (logdate);
   CREATE INDEX measurement_y2008m01_logdate ON measurement_y2008m01 (logdate);
   ```
5. 我們希望應用程式可以直接執行 `INSERT INTO measurement ...`，並讓資料被重新導向到適當的子資料表。我們可以藉由在根資料表上附加一個合適的觸發程序函式來做到這一點。如果資料只會加入到最新的子資料表中，我們可以使用一個非常簡單的觸發程序函式：

   ```

   CREATE OR REPLACE FUNCTION measurement_insert_trigger()
   RETURNS TRIGGER AS $$
   BEGIN
       INSERT INTO measurement_y2008m01 VALUES (NEW.*);
       RETURN NULL;
   END;
   $$
   LANGUAGE plpgsql;
   ```

   建立函式之後，我們建立一個呼叫該觸發程序函式的觸發程序：

   ```

   CREATE TRIGGER insert_measurement_trigger
       BEFORE INSERT ON measurement
       FOR EACH ROW EXECUTE FUNCTION measurement_insert_trigger();
   ```

   我們必須每個月重新定義觸發程序函式，讓它一律插入到目前的子資料表中。不過，觸發程序的定義不需要更新。

   我們可能希望插入資料時，由伺服器自動找出應該加入該資料列的子資料表。我們可以用一個更複雜的觸發程序函式來做到這一點，例如：

   ```

   CREATE OR REPLACE FUNCTION measurement_insert_trigger()
   RETURNS TRIGGER AS $$
   BEGIN
       IF ( NEW.logdate >= DATE '2006-02-01' AND
            NEW.logdate < DATE '2006-03-01' ) THEN
           INSERT INTO measurement_y2006m02 VALUES (NEW.*);
       ELSIF ( NEW.logdate >= DATE '2006-03-01' AND
               NEW.logdate < DATE '2006-04-01' ) THEN
           INSERT INTO measurement_y2006m03 VALUES (NEW.*);
       ...
       ELSIF ( NEW.logdate >= DATE '2008-01-01' AND
               NEW.logdate < DATE '2008-02-01' ) THEN
           INSERT INTO measurement_y2008m01 VALUES (NEW.*);
       ELSE
           RAISE EXCEPTION 'Date out of range.  Fix the measurement_insert_trigger() function!';
       END IF;
       RETURN NULL;
   END;
   $$
   LANGUAGE plpgsql;
   ```

   觸發程序的定義與之前相同。請注意，每個 `IF` 測試都必須與其子資料表的 `CHECK` 限制條件完全相符。

   雖然這個函式比單一月份的情況更複雜，但它不需要那麼頻繁地更新，因為可以在需要之前預先加入分支。

   ### 注意

   在實務上，如果大部分的插入都進入最新的子資料表，最好先檢查最新的子資料表。為了簡單起見，我們以與本範例其他部分相同的順序列出觸發程序的測試。

   將插入重新導向到適當子資料表的另一種做法，是在根資料表上設定規則，而不是觸發程序。例如：

   ```

   CREATE RULE measurement_insert_y2006m02 AS
   ON INSERT TO measurement WHERE
       ( logdate >= DATE '2006-02-01' AND logdate < DATE '2006-03-01' )
   DO INSTEAD
       INSERT INTO measurement_y2006m02 VALUES (NEW.*);
   ...
   CREATE RULE measurement_insert_y2008m01 AS
   ON INSERT TO measurement WHERE
       ( logdate >= DATE '2008-01-01' AND logdate < DATE '2008-02-01' )
   DO INSTEAD
       INSERT INTO measurement_y2008m01 VALUES (NEW.*);
   ```

   規則的額外負擔明顯比觸發程序大，但這項額外負擔是每個查詢支付一次，而不是每筆資料列支付一次，因此這種方法在大量插入的情況下可能比較有利。不過，在大多數情況下，觸發程序的方法會提供更好的效能。

   請注意，`COPY` 會忽略規則。如果你想用 `COPY` 插入資料，就必須複製到正確的子資料表中，而不是直接複製到根資料表。`COPY` 確實會觸發觸發程序，因此如果你使用觸發程序的做法，就可以正常使用它。

   規則做法的另一個缺點是，當規則集合沒有涵蓋插入的日期時，沒有簡單的方法可以強制引發錯誤；資料會默默地進入根資料表。
6. 確認 [constraint_exclusion](../../server-administration/runtime-config/runtime-config-query.md#GUC-CONSTRAINT-EXCLUSION) 組態參數沒有在 `postgresql.conf` 中被停用；否則可能會不必要地存取子資料表。

如我們所見，複雜的資料表階層可能需要相當大量的 DDL。在上面的範例中，我們每個月都會建立一個新的子資料表，所以撰寫一個自動產生所需 DDL 的指令碼可能是明智的做法。

<a id="DDL-PARTITIONING-INHERITANCE-MAINTENANCE"></a>

#### 5.12.3.2. 繼承式分割的維護 [#](#DDL-PARTITIONING-INHERITANCE-MAINTENANCE)

要快速移除舊資料，只要刪除不再需要的子資料表即可：

```

DROP TABLE measurement_y2006m02;
```

要將子資料表從繼承階層中移除，但保留以獨立資料表的形式存取它：

```

ALTER TABLE measurement_y2006m02 NO INHERIT measurement;
```

要加入新的子資料表來處理新資料，請像上面建立原始子資料表那樣，建立一個空的子資料表：

```

CREATE TABLE measurement_y2008m02 (
    CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' )
) INHERITS (measurement);
```

另外，也可能希望先建立新的子資料表並填入資料，再將它加入資料表階層。這讓資料可以在對父資料表的查詢中變得可見之前，先進行載入、檢查與轉換。

```

CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' );
\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work
ALTER TABLE measurement_y2008m02 INHERIT measurement;
```

<a id="DDL-PARTITIONING-INHERITANCE-CAVEATS"></a>

#### 5.12.3.3. 注意事項 [#](#DDL-PARTITIONING-INHERITANCE-CAVEATS)

使用繼承實作的分割，有下列注意事項：

* 沒有自動的方法可以驗證所有的 `CHECK` 限制條件都是互斥的。撰寫程式碼來產生子資料表並建立和／或修改相關聯的物件，會比逐一手寫更安全。
* 索引與外鍵限制條件只適用於單一資料表，而不適用於其繼承子資料表，因此有一些需要注意的[注意事項](ddl-inherit.md#DDL-INHERIT-CAVEATS)。
* 這裡所展示的方案，假設資料列的鍵欄位值永遠不會改變，或者至少不會改變到需要將它移動到另一個分割區的程度。嘗試這麼做的 `UPDATE` 會因為 `CHECK` 限制條件而失敗。如果你需要處理這類情況，可以在子資料表上設置合適的更新觸發程序，但這會使結構的管理複雜得多。
* 手動執行的 `VACUUM` 與 `ANALYZE` 命令會自動處理所有繼承子資料表。如果不希望這樣，可以使用 `ONLY` 關鍵字。像這樣的命令：

  ```

  ANALYZE ONLY measurement;
  ```

  只會處理根資料表。
* 帶有 `ON CONFLICT` 子句的 `INSERT` 陳述式不太可能如預期般運作，因為 `ON CONFLICT` 動作只會在指定的目標關聯上發生唯一性違反時才執行，而不會在其子關聯上執行。
* 除非應用程式明確知道分割方案，否則需要觸發程序或規則來將資料列導向到所需的子資料表。觸發程序可能寫起來很複雜，而且會比宣告式分割在內部進行的資料列路由慢得多。

<a id="DDL-PARTITION-PRUNING"></a>

### 5.12.4. 分割區修剪 [#](#DDL-PARTITION-PRUNING)

<a id="id-1.5.4.14.9.2"></a>

*分割區修剪*（partition pruning）是一種查詢最佳化技術，可以提升宣告式分割資料表的效能。舉例來說：

```

SET enable_partition_pruning = on;                 -- the default
SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
```

如果沒有分割區修剪，上面的查詢會掃描 `measurement` 資料表的每一個分割區。啟用分割區修剪時，規劃器會檢查每個分割區的定義，並證明某個分割區不需要被掃描，因為它不可能包含任何符合查詢 `WHERE` 子句的資料列。當規劃器能夠證明這一點時，就會將該分割區從查詢計畫中排除（*修剪*）。

使用 EXPLAIN 命令與 [enable_partition_pruning](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING) 組態參數，就可以顯示分割區已被修剪的計畫與未被修剪的計畫之間的差異。這類資料表設定的典型未最佳化計畫如下：

```

SET enable_partition_pruning = off;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-------------------------------------------------------------------​----------------
 Aggregate  (cost=188.76..188.77 rows=1 width=8)
   ->  Append  (cost=0.00..181.05 rows=3085 width=0)
         ->  Seq Scan on measurement_y2006m02  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2006m03  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
...
         ->  Seq Scan on measurement_y2007m11  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2007m12  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2008m01  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
```

部分或全部的分割區可能會使用索引掃描，而不是全資料表的循序掃描，但這裡的重點是，要回答這個查詢，根本不需要掃描較舊的分割區。當我們啟用分割區修剪時，會得到一個便宜得多、但會提供相同答案的計畫：

```

SET enable_partition_pruning = on;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-------------------------------------------------------------------​----------------
 Aggregate  (cost=37.75..37.76 rows=1 width=8)
   ->  Seq Scan on measurement_y2008m01  (cost=0.00..33.12 rows=617 width=0)
         Filter: (logdate >= '2008-01-01'::date)
```

請注意，分割區修剪只由分割鍵隱含定義的限制條件所驅動，而不是由索引的存在與否驅動。因此，不需要在鍵欄位上定義索引。是否需要為某個分割區建立索引，取決於你預期掃描該分割區的查詢，通常是掃描該分割區的大部分，還是只掃描一小部分。在後者的情況下索引會有幫助，在前者則不會。

分割區修剪不只可以在規劃給定查詢時進行，也可以在執行查詢時進行。這很有用，因為當子句包含在查詢規劃時無法得知其值的運算式時，它可以讓更多的分割區被修剪，例如 `PREPARE` 陳述式中定義的參數、使用從子查詢取得的值，或在巢狀迴圈聯結的內側使用參數化的值。執行期間的分割區修剪可以在下列任一時機進行：

* 在查詢計畫初始化期間。對於在執行的初始化階段就已知的參數值，可以在這裡進行分割區修剪。在這個階段被修剪的分割區，不會出現在查詢的 `EXPLAIN` 或 `EXPLAIN ANALYZE` 中。可以藉由觀察 `EXPLAIN` 輸出中的「Subplans Removed」屬性，得知在這個階段被移除的分割區數量。重要的是要注意，在這個階段藉由分割區修剪移除的任何分割區，在執行開始時仍然會被鎖定。
* 在實際執行查詢計畫期間。也可以在這裡進行分割區修剪，使用只有在實際執行查詢時才能得知的值來移除分割區。這包括來自子查詢的值，以及來自執行時期參數（例如參數化巢狀迴圈聯結的參數）的值。由於這些參數的值在查詢執行期間可能會改變許多次，因此每當分割區修剪所使用的某個執行參數改變時，就會進行分割區修剪。要判斷在這個階段是否有分割區被修剪，需要仔細檢查 `EXPLAIN ANALYZE` 輸出中的 `loops` 屬性。對應到不同分割區的子計畫，視各自在執行期間被修剪了多少次，可能會有不同的值。如果某些子計畫每次都被修剪，它們可能會顯示為 `(never executed)`。

可以使用 [enable_partition_pruning](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING) 設定來停用分割區修剪。

<a id="DDL-PARTITIONING-CONSTRAINT-EXCLUSION"></a>

### 5.12.5. 分割與限制條件排除 [#](#DDL-PARTITIONING-CONSTRAINT-EXCLUSION)

<a id="id-1.5.4.14.10.2"></a>

*限制條件排除*（constraint exclusion）是一種類似於分割區修剪的查詢最佳化技術。雖然它主要用於以舊有的繼承方法實作的分割，但它也可以用於其他目的，包括搭配宣告式分割使用。

限制條件排除的運作方式與分割區修剪非常相似，只是它使用的是每個資料表的 `CHECK` 限制條件——這也是它名稱的由來——而分割區修剪使用的是資料表的分割區界限，而分割區界限只存在於宣告式分割的情況中。另一個差別是，限制條件排除只在規劃時套用；它不會嘗試在執行時移除分割區。

限制條件排除使用 `CHECK` 限制條件這個事實，使它比分割區修剪慢，但有時這也可以成為一項優勢：由於即使在宣告式分割資料表上，除了其內部的分割區界限之外，也可以定義限制條件，因此限制條件排除或許能從查詢計畫中省略額外的分割區。

[constraint_exclusion](../../server-administration/runtime-config/runtime-config-query.md#GUC-CONSTRAINT-EXCLUSION) 的預設（也是建議的）設定既不是 `on` 也不是 `off`，而是一個稱為 `partition` 的中間設定，它使這項技術只套用於可能作用在繼承分割資料表上的查詢。`on` 設定會使規劃器在所有查詢中檢查 `CHECK` 限制條件，即使是不太可能從中受益的簡單查詢也一樣。

限制條件排除有下列注意事項：

* 限制條件排除只在查詢規劃期間套用，不像分割區修剪也可以在查詢執行期間套用。
* 只有當查詢的 `WHERE` 子句包含常數（或外部提供的參數）時，限制條件排除才會發揮作用。例如，與 `CURRENT_TIMESTAMP` 這類非 immutable 函式進行的比較無法被最佳化，因為規劃器無法得知該函式的值在執行時會落在哪一個子資料表中。
* 讓分割限制條件保持簡單，否則規劃器可能無法證明子資料表不需要被存取。對清單分割使用簡單的相等條件，對範圍分割使用簡單的範圍測試，如前面的範例所示。一個好的經驗法則是，分割限制條件應該只包含使用可由 B-tree 索引的運算子，將分割欄位與常數進行比較，因為分割鍵中只允許可由 B-tree 索引的欄位。
* 在限制條件排除期間，會檢查父資料表所有子資料表上的所有限制條件，因此大量的子資料表很可能會大幅增加查詢規劃時間。所以，基於舊有繼承的分割，大概可以在子資料表數量達到約一百個左右時仍運作良好；不要嘗試使用成千上萬個子資料表。

<a id="DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES"></a>

### 5.12.6. 宣告式分割的最佳實務 [#](#DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES)

如何分割資料表的選擇應該謹慎進行，因為不良的設計可能對查詢規劃與執行的效能產生負面影響。

最關鍵的設計決策之一，是要依哪一個或哪些欄位來分割你的資料。通常最好的選擇，是依在分割資料表上執行之查詢的 `WHERE` 子句中最常出現的欄位或欄位集合來分割。與分割區界限限制條件相容的 `WHERE` 子句，可以用來修剪不需要的分割區。不過，`PRIMARY KEY` 或 `UNIQUE` 限制條件的需求，可能會迫使你做出其他決定。移除不需要的資料，也是規劃分割策略時要考量的因素。整個分割區可以相當快速地被分離，因此將分割策略設計成讓所有要一次移除的資料都位於單一分割區中，可能會很有好處。

選擇資料表應該劃分成多少個分割區，也是一項關鍵的決策。分割區不夠多，可能表示索引仍然太大，而且資料的區域性仍然很差，可能導致快取命中率偏低。不過，將資料表劃分成太多分割區也可能造成問題。太多分割區可能意味著更長的查詢規劃時間，以及在查詢規劃與執行期間更高的記憶體消耗，如下文進一步說明。在選擇如何分割資料表時，考慮未來可能發生哪些變化也很重要。例如，如果你選擇每位客戶一個分割區，而你目前只有少數幾個大客戶，那麼請考慮幾年後如果你反而擁有大量小客戶會有什麼影響。在這種情況下，選擇依 `HASH` 分割並選擇合理數量的分割區，可能會比嘗試依 `LIST` 分割、並期望客戶數量不會增加到超出分割資料的實際可行範圍更好。

子分割可以用來進一步劃分預期會比其他分割區更大的分割區。另一種做法是使用在分割鍵中具有多個欄位的範圍分割。這兩種做法都很容易導致分割區數量過多，因此建議有所節制。

考慮分割在查詢規劃與執行期間所帶來的額外負擔是很重要的。只要典型的查詢能讓查詢規劃器修剪掉除了少數幾個之外的所有分割區，查詢規劃器一般就能相當好地處理具有多達數千個分割區的分割階層。當規劃器進行分割區修剪之後剩下的分割區越多，規劃時間就會越長，記憶體消耗也會越高。另一個需要擔心分割區數量過多的原因是，伺服器的記憶體消耗可能會隨著時間顯著增加，特別是當許多工作階段都存取大量分割區時。這是因為每個分割區都需要將其中繼資料載入到存取它之每個工作階段的本機記憶體中。

在資料倉儲類型的工作負載中，使用比 OLTP 類型工作負載更多的分割區可能是合理的。一般而言，在資料倉儲中，查詢規劃時間比較不是問題，因為大部分的處理時間都花在查詢執行上。無論是這兩種工作負載中的哪一種，及早做出正確的決策都很重要，因為重新分割大量資料可能慢得令人痛苦。模擬預期的工作負載，通常有助於最佳化分割策略。千萬不要只是假設分割區越多越好，反之亦然。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-partitioning.html)（原文版本：18.6；核對日期：2026-09-15）
