---
description: 版本：10
---

# 5.10. 分割資料表

PostgreSQL 支援基礎的分割資料表。本節描述如何讓分割資料表成為資料庫設計的一部份。

## 5.10.1. 概論

資料表的分割，指的是把一個邏輯上很大的資料表，分割為數個實體的小資料表。分割資料表可以獲得幾點好處：

* 資料查詢的效能在某些情況下會大幅改善，特別是資料表中有一些資料列是時常被存取的，而它們只存在於某一個單一的分割區，或某一小群分割區。分割資料表的優勢在於大幅降低欄位索引的大小，而當其大小縮小到可以完全在記憶體中執行時，那就會獲得相當大的效能改善。
* 當資料查詢或更新時，它可能牽連到某一分割區大部份的資料列，效能同樣會獲得改善，它可以直接掃描存取整個「小」區域，而不是在「大」資料表中，以索引逐筆搜尋分散的資料列。
* 大量載入或移除資料的話，可以直接對整個分割區操作，當然這些資料要能符合分割資料表的設計。使用 ALTER TABLE DETACH PARTITION 或是 DROP TABLE 移除特定的分割資料表，都比進行大量的 DELETE 要快非常多。因為這些指令不會進行資料表的整理，而大量的 DELETE 會引發 VACUUM 的啓動。 
* 少用的資料可以搬到較便宜或比較慢的儲存媒體。

這些優勢通常是在原來資料表特別大是會很明顯，不過實際上會獲得什麼樣的改善，還是要視應用程式而定。一個基本的概念是資料表的大小，如果超過了資料庫主機的記憶體上限，那就最好進行資料表的分割。

PostgreSQL 內建提供的資料表分割方式：

**Range Partitioning**

資料表是以某個欄位或某些欄位的資料內容範圍來分割，所謂的範圍，就表示彼此之間沒有重疊的部份。舉例來說，你可以以資料的範圍做分割，或是以指定的公司資料 ID 的範圍來分割。

**List Partitioning**

明確列出有哪些資料的值要被分配在哪些資料表。

如果你的應用需要使用上述兩種以外的分割方式，還有其他方式，像是繼承，UNION ALL views，也可以使用。這些方式提供更多的彈性，但都不如內建分割方式所提升的效能。

## 5.10.2. **分割資料表宣告**

PostgreSQL 提供一個方式，可以指定如何將資料表分割為較小的資料表，這些小資料表稱作為分割區（partitions）。被分割的資料表，稱作分割資料表。分割主鍵包含了分割方法與一些欄位內容或是表示式。

所有新插入的資料列將會依分割主鍵的規則，轉送至分割區中。每一個分割區都是所有資料列的子集合，範圍由其定義的資料邊界而定。目前支援的分割方法有 Range 及 List 分割法，也就是每一個分割區都需要指定一個區段或是一個列表。

分割區本身也可以是分割資料表，這稱作為次分割（sub-partitioning）。分割區會擁有它們自己的索引，限制條件，以及預設值，是獨立於其他分割區的。索引必須要分別為每個分割區建立。請參閱 [CREATE TABLE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-table.md) 進一步瞭解建立分割資料表及分割區的指令。

一般資料表和分割資料表是無法互相轉換的，但你可以使一個已存放資料的一般資料表或分割資料表成為某個分割資料表的新分割區；或是從某個分割資料表移出某個分割區，使其成為獨立的一般資料表。請參閱 [ALTER TABLE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/alter-table.md) 瞭解 ATTACH PARTITION 及 DETACH PARTITION 的使用方式。

分割資料表和個別的分割區之間，隱含著繼承的關係；不過它們並無法使用先前章節所介紹過的繼承功能。舉例來說，分割區不能同時是其他分割資料表的子資料表，一般資料表也不能繼承分割資料表。簡單來說，分割資料表及其分割區，都不能和一般資料表有任何繼承的關係。分割區與分割資料表是階層關係，而其分割區也是繼承的階層，所以所有一般的繼承規則，在 [5.9 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/data-definition/59-inheritance.md)中介紹的，都會成立，除了有一些例外，比較重要的如下：

* 分割資料表的 CHECK 及 NOT NULL 限制條件，會被其分割區所繼承。 在分割資料區中，把 CHECK 標示為 NO INHERIT 是不被允許的。
* 在分割資料表新增或移除限制條件時使用 ONLY 的話，只有在其還沒有分割區時是允許的。一旦其下有分割區存在，使用 ONLY 就會產生錯誤。換句話說，當有分割區時，這個執行方式是不被允許的。但是你可以新增或移除分割區裡的限制條件，只要它們並沒有在分割資料表中存在就好。在分割資料表嘗試執行 TRUNCATE ONLY 指令，也會產生錯誤，因為分割資料表並未實際存放資料。
* 分割區不能有分割資料表裡沒有的欄位。不能在 CREATE TABLE 時建立，也不能使用 ALTER TABLE 增加。資料表能成為一個分割區，它的欄位必須和分割資料表完全吻全，包含 OIDs。
* 你無法移除分割區中的 NOT NULL 限制條件，如果它是定義在分割資料表中的話。

分割區可以是外部資料表（參閱 [CREATE FOREIGN TABLE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-foreign-table.md)），雖然它會有一些使用上的限制。舉例來說，插入資料到分割資料表，資料並不會轉送到外部資料表的分割區處理。

### 5.10.2.1. 範例

假設我們為一家大型冰淇淋公司建構一個資料庫。這家公司每天測量最高溫度，同時也統計各區域的銷售情況。概念上，我們需要像這樣的資料表：

```text
CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
);
```

我們知道大多數都是在進行近期的資料查詢，如最近一週、最近一個月、或最近一季的資料，這個資料表用於產生管理用的線上報表之用。為了降低需要儲存的資料量，我們決定只保存 3 年內有價值的資料。每一個月開始時，我們就會移除最舊那個月的資料。在這種情況下，我們可以使用分割資料表來幫助我們滿足所有需求。

在這個例子中，使用下列步驟來宣告分割資料表：

1. 建立 measurement 資料表時，使用 PARTITION BY 子句，在本例子使用 RANGE 的分割方法，然後以 logdate 作為分割主鍵。

   ```text
   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   ) PARTITION BY RANGE (logdate);
   ```

   你也可以使用多個欄位作為分割主鍵來依範圍分割，當然，這會產生相當多的分割區，它可以分割得更小一些。也就是說，使用較少的分割主鍵欄位，是較為粗略的分割。當分割資料表被查詢時，就可以減少分割區存取的數量，如果條件是遍及數個欄位時。舉例來說，可以想像一下一個以範圍分割的資料表，同時以 lastname 及 firstname 兩個欄位作為分割主鍵的情況。

2. 建立分割區時，每一個分割區的定義都必須指定其分割方式的規則與分割主鍵。需要注意的是，如果指定的規則，造成某些分割主鍵的值會落在多個分割區中的話，將會產生錯誤。從分割資料表插入資料時，如果沒有對應到任何一個分割區的話，也會產生錯誤；適當擺放資料的分割區必須要手動加入。

分割區的建立就如同一般的 PostgreSQL 資料表一樣（也可以是外部資料表），也可以指定各自的 tablespace 和儲存參數。

不需要為分割規則設定分割區的限制條件，而是在設定分割方式及規則時，其限制條件就已經隱含在內了。

```text
CREATE TABLE measurement_y2006m02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')

CREATE TABLE measurement_y2006m03 PARTITION OF measurement
    FOR VALUES FROM ('2006-03-01') TO ('2006-04-01')

...
CREATE TABLE measurement_y2007m11 PARTITION OF measurement
    FOR VALUES FROM ('2007-11-01') TO ('2007-12-01')

CREATE TABLE measurement_y2007m12 PARTITION OF measurement
    FOR VALUES FROM ('2007-12-01') TO ('2008-01-01')
    TABLESPACE fasttablespace;

CREATE TABLE measurement_y2008m01 PARTITION OF measurement
    FOR VALUES FROM ('2008-01-01') TO ('2008-02-01')
    TABLESPACE fasttablespace
    WITH (parallel_workers = 4);
```

要實現子分割時，使用 PARTITION BY 子句來建立個別的分割區。舉例來說：

```text
CREATE TABLE measurement_y2006m02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')
    PARTITION BY RANGE (peaktemp);
```

在建立了 measurement\_y\_\_2006m02 資料表之後，所有新增到 measurement 資料表中符合分割規則而被派送到 measurementy\_2006m02 的資料（或是符合條件的資料直接新增到 measurement\_y2006m02），都會再進一步依據 peaktemp 欄位的內容轉存到它的子分割區。這個分割主鍵是可以和其父資料表分割主鍵有重疊的，不過要注意的是，指定子分割區的規則時，資料真的會分配到該子分割區，資料庫系統不會去檢查該分配是不是真的會發生。

1. 為每一個分割區資料表的分割主鍵建立索引。（這並不是一定要做的事，不過對大多數的情況是好的。如果你需要這些值俱備唯一性，那你應該建立唯一索引或是主鍵。）

   ```text
   CREATE INDEX ON measurement_y2006m02 (logdate);
   CREATE INDEX ON measurement_y2006m03 (logdate);
   ...
   CREATE INDEX ON measurement_y2007m11 (logdate);
   CREATE INDEX ON measurement_y2007m12 (logdate);
   CREATE INDEX ON measurement_y2008m01 (logdate);
   ```

2. 確定 postgresql.conf 中的 [constrain\_exclusion](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/iii-server-administration/server-configuration/197-query-planning.md) 設定並未被關閉。如果是關閉狀態的話，查詢最佳化就不會進行。

在上面的例子中，我們需要每個月建立一個分割區，所以如果能再有程序自動建立這些資料表就更好了。

### 5.10.2.2. 分割區管理

一般來說，分割區在初始建立時，會假設其會不斷地變動。通常會需要定期移除舊的分割區，然後為新的資料加入新的分割區。使用分割資料表時，其中一件很重要的事，就是要能夠很明確地做到這個管理動作，否則大量地實體資料變更，會嚴重拖累資料庫系統的效率。

最簡易移除資料的方式，就是移除分割區：

```text
DROP TABLE measurement_y2006m02;
```

這可以非常快地移除數百萬筆資料，因為它並不是單獨去移除每一筆資料。注意到的是，這個動作需要父資料表取得 ACCESS EXCLUSIVE 的鎖定。

另一個方式也很常使用，就是把某個分割區從分割資料表中卸載，但仍然保存該分割區的資料表：

```text
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02;
```

這樣可以在資料被移除之前再進行一些其他的操作。舉例來說，很常見的使用情況是備份資料，利用 COPY 指令、pg\_dump、或相關的工具；把資料以小單位進行彙總計算產生報表，也是很常用的方式。

接下來，要處理新的資料也是類似的動作，我們可以建立新的資料表，並宣告為分割區來使用，就如同先前我們介紹的設定方式一樣：

```text
CREATE TABLE measurement_y2008m02 PARTITION OF measurement
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01')
    TABLESPACE fasttablespace;
```

另一種更方便的方式是先建立新的資料表，然後再將它掛載為分割區。好處是這樣可以在掛載前先進行資料的載入、檢查和轉換：

```text
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

在進行 ATTACH PARTITION 指令前，建議最好先設定 CHECK 限制條件，同分割資料表的條件，這樣的話，系統就會跳過隱含的資料檢查過程。如果沒有先設定限制條件的話，資料表會被 ACCESS EXCLUSIVE 鎖定，然後進行全資料掃描以檢查其合法性。最後我們在掛載分割區之後再移除該 CHECK 設定，因為它已經不再需要了。

### 5.10.2.3. 使用限制

使用分割資料表是會有下面的受限制的使用情況：

* 沒有方法可以自動在所有分割區建立需要的索引。每個分割區的索引都需要個別建立。這也代表了，沒有任何方式可以建立主鍵、唯一性限制條件、或其他跨分割區的限制條件需求；只能個別分割區自行維護。
* 因為分割資料表無法建立主鍵，所以外部鍵就無法支援了，無論是參考其他資料表或被參考，都不支援。
* 在分割資料表使用 ON CONFLICT 子句的話，會產生錯誤訊息，因為沒有唯一性及除外限制可以使用。目前不支援跨所有分割區的唯一性限制，也包含其他除外限制。
* 想要利用 UPDATE 改變欄位值，使資料移動到另一個分割區是行不通的。因為隱含的資料限制條件會造成其更新失敗。
* 資料列的事件觸發函數，必須定義在個別分割區的資料表中，而非分割資料表。

## 5.10.3. 使用繼承來分割資料表

使用內建的分割資料表，基本上適用於大多數的應用情境，也可以使用一些彈性的技巧會更有幫助。分割資料庫也可以用資料表繼承的方式來達成，好處是可以支援一些本來有限制的使用情況，例如：

* 分割資料表會強制使所有分割區都必須要與父資料表完全一樣的資料結構，但使用繼承的話，就可以允許分割區各自擁有額外的資料欄位。
* 資料表的繼承可以是多重繼承。
* 內建的分割資料表只支援列表（list）和範圍（range）兩種資料對應方式，而繼承則可以用自訂的方式來對應資料分區。（注意，如果你的資料對應方式無法適當地利用每個分割區的話，那麼查詢將會很沒有效率。）
* 內建的分割資料表相對於資料表繼承時，有一些操作需要較嚴格的資料鎖定（lock）。舉例來說，分割資料表在新增或移除分割區時，會使用 ACCESS EXCLUSIVE 等級的資料鎖定，但實際上在資料表繼承維護時，只需要 SHARE UPDATE EXCLUSIVE 等級即可。

### 5.10.3.1. 範例

以先前使用過的 measurement 資料表作為範例說明，我們要使用繼承功能來完成分割資料表。請參考下列步驟：

1. 建立主資料表（master），所有的分割區將會繼承它，而這個資料表不會儲存任何資料。請不要在這個資料表上定義任何限制條件，除非你希望每一個分割區都要有相等的限制條件。同樣地，也不要定義任何索引或唯一性限制。在這個例子裡，資料表 measurement 就如同先前一開始宣告的一樣。
2. 建立幾個子資料表（child），由主資料表繼承而得。一般來說，這些資料表並不增加額多的欄位。就如同內建的分割資料表一樣，這些子資料表就是一般的 PostgreSQL 資料表（或是外部資料表）。

   ```text
   CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
   CREATE TABLE measurement_y2006m03 () INHERITS (measurement);
   ...
   CREATE TABLE measurement_y2007m11 () INHERITS (measurement);
   CREATE TABLE measurement_y2007m12 () INHERITS (measurement);
   CREATE TABLE measurement_y2008m01 () INHERITS (measurement);
   ```

3. 在每個子資料表（分割區）中，加入明確分隔的欄位值限制條件。

   典型的範例如下：

   ```text
   CHECK ( x = 1 )
   CHECK ( county IN ( 'Oxfordshire', 'Buckinghamshire', 'Warwickshire' ))
   CHECK ( outletID >= 100 AND outletID < 200 )
   ```

   請確認這些限制條件是明確的且彼此不會重疊的。下面是使用範圍分割時常見的錯誤：

   ```text
   CHECK ( outletID BETWEEN 100 AND 200 )
   CHECK ( outletID BETWEEN 200 AND 300 )
   ```

   這裡的錯誤來自於「200」同時符合兩個分割區的條件。

   下面是比較好的寫法：

   ```text
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

4. 對每一個分割區，對分割主鍵欄位建立索引，就如同一般的索引建立一樣。

   ```text
   CREATE INDEX measurement_y2006m02_logdate ON measurement_y2006m02 (logdate);
   CREATE INDEX measurement_y2006m03_logdate ON measurement_y2006m03 (logdate);
   CREATE INDEX measurement_y2007m11_logdate ON measurement_y2007m11 (logdate);
   CREATE INDEX measurement_y2007m12_logdate ON measurement_y2007m12 (logdate);
   CREATE INDEX measurement_y2008m01_logdate ON measurement_y2008m01 (logdate);
   ```

5. 我們希望應用程式可以使用 `INSERT INTO measurement ...`的語法，資料則自動轉送到適當的資料表。我們可以在主資料表建立適當的 Trigger 來完成此事。如果資料都會被新增到最新的子資料表中，我們可以建立很簡單的事件觸發函數：

   ```text
   CREATE OR REPLACE FUNCTION measurement_insert_trigger()
   RETURNS TRIGGER AS $$
   BEGIN
       INSERT INTO measurement_y2008m01 VALUES (NEW.*);
       RETURN NULL;
   END;
   $$
   LANGUAGE plpgsql;
   ```

   建立這個函數之後，再建立 Trigger：

   ```text
   CREATE TRIGGER insert_measurement_trigger
       BEFORE INSERT ON measurement
       FOR EACH ROW EXECUTE PROCEDURE measurement_insert_trigger();
   ```

   我們必須每個月都重新定義這個函數，使其都指向最新的分割區，但 Trigger 宣告並不需要更新。

   我們也可以在新增資料時，讓它們自動找到適當的分割區，那就需要宣告一個比較複雜的函數，如下：

   ```text
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

   Trigger 本身的定義仍然是一樣的。要注意的是，每一個 IF 判斷式，都必須要完全符合 CHECK 限制條件的宣告。

   這個函數比前一個函數要複雜許多，但它就不需要時常更新了，只要分割區在需要前就被建立就好。

## 注意

實務上，最好是可以先檢查新建立的分割區，在它要掛載之前。簡化來看，我們在這個例子中使用事件觸發函數（Trigger）來處理這個動作。

另一個作法是在主要的資料表上設定規則，來取代事件觸發函數。例如：

```text
CREATE RULE measurement_insert_y2006m02 AS
ON INSERT TO measurement WHERE
    ( logdate >= DATE '2006-02-01' AND logdate < DATE '2006-03-01' )j水
DO INSTEAD
    INSERT INTO measurement_y2006m02 VALUES (NEW.*);
...
CREATE RULE measurement_insert_y2008m01 AS
ON INSERT TO measurement WHERE
    ( logdate >= DATE '2008-01-01' AND logdate < DATE '2008-02-01' )
DO INSTEAD
    INSERT INTO measurement_y2008m01 VALUES (NEW.*);
```

基本上，設定規則對資料庫的負擔是比事件觸發函數更重一點，但其負擔是在於每一次查詢，而非每一個資料列，所以這個方式比較適合一次大量插入資料的情況。不過，在大多數的情況，事件觸發函數會有比較好的效能。

但要注意的是 COPY 指令會忽略規則。如果你要使用 COPY 來插入資料，你應該要從父資料表插入。而 COPY 會觸發事件觸發函數，所以你如果使用 Trigger 的話，那就像一般使用的方式使用就好了。

另一個使用 rule 的缺點是，沒有比較簡單的方法可以強制產生錯誤，如果設定的規則錯誤的話；那些出錯的資料，只會靜靜地留在父資料表中而已。

確認一下 postgresql.conf 中的 [constraint\_exclusion](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/iii-server-administration/server-configuration/197-query-planning.md) 並沒有被關閉。如果被關閉的話，查詢就不會最佳化處理。

就如同我們看到的，複雜的分割區結構，可能會需要相當數量的 DDL 宣告。在先前的例子，我們每個月建立一個新的分割區，所以比較聰明的作法是寫一小段程式來自動產生那些指令。

### 5.10.3.2. 分割區管理

要快速刪除舊資料，可以簡單地移除不再使用的分割區資料表即可：

```text
DROP TABLE measurement_y2006m02;
```

將一個分割區從分割資料表中卸載，仍然留存該資料表：

```text
ALTER TABLE measurement_y2006m02 NO INHERIT measurement;
```

要新增一個分割區來處理新的資料，建立一個空的分割區，就如同先前介紹的方式：

```text
CREATE TABLE measurement_y2008m02 (
    CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' )
) INHERITS (measurement);
```

另一種更方便的方式是先建立新的資料表，然後再將它掛載為分割區。好處是這樣可以在掛載前先進行資料的載入、檢查和轉換：

```text
CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' );
\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work
ALTER TABLE measurement_y2008m02 INHERIT measurement;
```

### 5.10.3.3. 提醒

如果你使用繼承在實現分割資料表的話，請注意下列項目：

* 沒有任何自動的方式可以檢驗 CHECK 子句之間是否矛盾。比較建議的作法是程式化控制分割區的建立和維護，而非手動處理。
* 在這裡所展示的方法都是假設分割主鍵欄位不會改變，也不會需要把某個資料列在分割區間移動。如果你企圖使用 UPDATE 指令，而期待資料列自動移到另一個分割區的話，那將會得到失敗的結果，因為會先被 CHECK 限制條件擋下來。如果你需要做到這樣的效果，那麼你可以建立 UPDATE 事件的觸發函數，但這可能會造成你的資料庫管理更加複雜。
* 如果你手動執行 VACUUM 或 ANALYZE 指令，不要忘了你需要在每個分割區資料表分別執行。 例如：`ANALYZE measurement;`將只會在父資料表執行。
* INSERT 指令裡的 ON CONFLICT 子句將無法運作，因為它只能在父資料表產生作用，而不會到子資料表中執行。
* 事件觸發函數（Trigger）需要建立，負責把資料放在設計好的資料表中，除非應用程式很清楚分割區的結構。事件觸發函數可能會不太好寫，而且也會比使用內建的分割資料表時慢很多。

## 5.10.4. 分割資料表與除外限制（Constraint Exclusion）

除外限制（Constraint exclusion）是一種查詢最佳化的技術，用來改善分割資料表的效能。（包含內建分割資料表的方式，以及繼承式的分割資料表）舉個例子如下：

```text
SET constraint_exclusion = on;
SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
```

如果沒有除外限制的話，上面的查詢語句將會掃描每一個 measurement 資料表的分割區。而開啓了除外限制的話，查詢前就會先測試限制條件，確認該分割區是否需要掃描，因為有些分割區可能完全沒有資料符合該條件。如果確實有不需要掃描的分割區，那麼它就會在實際查詢時排除在外。

你可以使用 EXPLAIN 指令來比較除外查詢開啓與否的差異。下面是未最佳化的例子：

```text
SET constraint_exclusion = off;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';

                                          QUERY PLAN
-----------------------------------------------------------------------------------------------
 Aggregate  (cost=158.66..158.68 rows=1 width=0)
   ->  Append  (cost=0.00..151.88 rows=2715 width=0)
         ->  Seq Scan on measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2006m02 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2006m03 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate >= '2008-01-01'::date)
...
         ->  Seq Scan on measurement_y2007m12 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2008m01 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate >= '2008-01-01'::date)
```

可以看到有些分割區可能會使用索引掃描來取代全資料表掃描，但這裡的重點是，有些分割區是完全不需要掃描的。當我們開啓除外限制時，很明顯可以得到一個更簡潔的查詢計畫：

```text
SET constraint_exclusion = on;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                          QUERY PLAN
-----------------------------------------------------------------------------------------------
 Aggregate  (cost=63.47..63.48 rows=1 width=0)
   ->  Append  (cost=0.00..60.75 rows=1086 width=0)
         ->  Seq Scan on measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2008m01 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate >= '2008-01-01'::date)
```

要注意的是，除外限制只檢查 CHECK 子句，而不是索引，所以不一定要對主鍵欄位定義索引。索引是否需要在分割區建立，是依據你希望查詢在該分割區大範圍或小範圍被查詢。索引的用處在後者會比較明顯，而不是前者。預設也是建議的選項不是 on 也不是 off，而是使用 partition 子句，讓查詢只在需要執行的分割區執行。設定除外限制為「on」的話，對於大範圍的查詢很有用，但簡單查詢就不見得有好處了。

下面還有幾點注意事項，繼承和分割資料表都適用：

* 除外限制只適用於 WHERE 子句是常數的條件（或外部引用的參數）。舉例來說，和一個不確定結果的函數比較的話，如 CURRENT\_TIMESTAMP，那就無法最佳化，因為查詢計畫無法事先得知執行時的值。
* 保持分割區限制條件簡潔一些，否則查詢計畫無從查驗該分割區是否需要處理。請在列舉分割時，使用簡單的等式；或在範圍分割時使用簡單的比較式，就如同先前的例子一樣。一個好的規則是只包含分割主鍵的欄位，並且使用 B-tree 可以索引的運算子，也同時宣告在主資料表中，只允許適用於 B-tree 的欄位宣告為分割主鍵。（如果使用內建分割語法的話，這不會有什麼問題，因為系統會自動宣告適合查詢計畫的限制條件。）
* 由於除外限制會在查詢前檢查所有分割區的限制條件，所以大量的分割區可能會增加查詢計畫的時間。所謂的「大量」，通常幾百個分割區還是可以接受的範圍，但最好不要用於上千個分割區的情境中。

