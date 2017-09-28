# 5.10. 分割資料表[^1]

PostgreSQL 支援基礎的分割資料表。本節描述如何讓分割資料表成為資料庫設計的一部份。

### 5.10.1. 概論

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

### 5.10.2. **分割資料表宣告**

PostgreSQL 提供一個方式，可以指定如何將資料表分割為較小的資料表，這些小資料表稱作為分割區（partitions）。被分割的資料表，稱作分割資料表。分割主鍵包含了分割方法與一些欄位內容或是表示式。

所有新插入的資料列將會依分割主鍵的規則，轉送至分割區中。每一個分割區都是所有資料列的子集合，範圍由其定義的資料邊界而定。目前支援的分割方法有 Range 及 List 分割法，也就是每一個分割區都需要指定一個區段或是一個列表。

分割區本身也可以是分割資料表，這稱作為次分割（sub-partitioning）。分割區會擁有它們自己的索引，限制條件，以及預設值，是獨立於其他分割區的。索引必須要分別為每個分割區建立。請參閱 [CREATE TABLE](/vi-reference/i-sql-commands/create-table.md) 進一步瞭解建立分割資料表及分割區的指令。

一般資料表和分割資料表是無法互相轉換的，但你可以使一個已存放資料的一般資料表或分割資料表成為某個分割資料表的新分割區；或是從某個分割資料表移出某個分割區，使其成為獨立的一般資料表。請參閱 [ALTER TABLE](/vi-reference/i-sql-commands/alter-table.md) 瞭解 ATTACH PARTITION 及 DETACH PARTITION 的使用方式。

分割資料表和個別的分割區之間，隱含著繼承的關係；不過它們並無法使用先前章節所介紹過的繼承功能。舉例來說，分割區不能同時是其他分割資料表的子資料表，一般資料表也不能繼承分割資料表。簡單來說，分割資料表及其分割區，都不能和一般資料表有任何繼承的關係。分割區與分割資料表是階層關係，而其分割區也是繼承的階層，所以所有一般的繼承規則，在 [5.9 節](/ii-the-sql-language/data-definition/59-inheritance.md)中介紹的，都會成立，除了有一些例外，比較重要的如下：

* 分割資料表的 CHECK 及 NOT NULL 限制條件，會被其分割區所繼承。 在分割資料區中，把 CHECK 標示為 NO INHERIT 是不被允許的。
* 在分割資料表新增或移除限制條件時使用 ONLY 的話，只有在其還沒有分割區時是允許的。一旦其下有分割區存在，使用 ONLY 就會產生錯誤。換句話說，當有分割區時，這個執行方式是不被允許的。但是你可以新增或移除分割區裡的限制條件，只要它們並沒有在分割資料表中存在就好。在分割資料表嘗試執行 TRUNCATE ONLY 指令，也會產生錯誤，因為分割資料表並未實際存放資料。
* 分割區不能有分割資料表裡沒有的欄位。不能在 CREATE TABLE 時建立，也不能使用 ALTER TABLE 增加。資料表能成為一個分割區，它的欄位必須和分割資料表完全吻全，包含 OIDs。
* 你無法移除分割區中的 NOT NULL 限制條件，如果它是定義在分割資料表中的話。

分割區可以是外部資料表（參閱 [CREATE FOREIGN TABLE](/vi-reference/i-sql-commands/create-foreign-table.md)），雖然它會有一些使用上的限制。舉例來說，插入資料到分割資料表，資料並不會轉送到外部資料表的分割區處理。

#### 5.10.2.1. 範例

假設我們為一家大型冰淇淋公司建構一個資料庫。這家公司每天測量最高溫度，同時也統計各區域的銷售情況。概念上，我們需要像這樣的資料表：

```
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

   ```
   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   ) PARTITION BY RANGE (logdate);
   ```

   你也可以使用多個欄位作為分割主鍵來依範圍分割，當然，這會產生相當多的分割區，它可以分割得更小一些。也就是說，使用較少的分割主鍵欄位，是較為粗略的分割。當分割資料表被查詢時，就可以減少分割區存取的數量，如果條件是遍及數個欄位時。舉例來說，可以想像一下一個以範圍分割的資料表，同時以 lastname 及 firstname 兩個欄位作為分割主鍵的情況。

2. Create partitions. Each partition's definition must specify the bounds that correspond to the partitioning method and partition key of the parent. Note that specifying bounds such that the new partition's values will overlap with those in one or more existing partitions will cause an error. Inserting data into the parent table that does not map to one of the existing partitions will cause an error; appropriate partition must be added manually.

   Partitions thus created are in every way normalPostgreSQLtables \(or, possibly, foreign tables\). It is possible to specify a tablespace and storage parameters for each partition separately.

   It is not necessary to create table constraints describing partition boundary condition for partitions. Instead, partition constraints are generated implicitly from the partition bound specification whenever there is need to refer to them.

   ```
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

   To implement sub-partitioning, specify the`PARTITION BY`clause in the commands used to create individual partitions, for example:

   ```
   CREATE TABLE measurement_y2006m02 PARTITION OF measurement
       FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')
       PARTITION BY RANGE (peaktemp);
   ```

   After creating partitions of`measurement_y2006m02`, any data inserted into`measurement`that is mapped to`measurement_y2006m02`\(or data that is directly inserted into`measurement_y2006m02`, provided it satisfies its partition constraint\) will be further redirected to one of its partitions based on the`peaktemp`column. The partition key specified may overlap with the parent's partition key, although care should be taken when specifying the bounds of a sub-partition such that the set of data it accepts constitutes a subset of what the partition's own bounds allows; the system does not try to check whether that's really the case.

3. Create an index on the key column\(s\), as well as any other indexes you might want for every partition. \(The key index is not strictly necessary, but in most scenarios it is helpful. If you intend the key values to be unique then you should always create a unique or primary-key constraint for each partition.\)

   ```
   CREATE INDEX ON measurement_y2006m02 (logdate);
   CREATE INDEX ON measurement_y2006m03 (logdate);
   ...
   CREATE INDEX ON measurement_y2007m11 (logdate);
   CREATE INDEX ON measurement_y2007m12 (logdate);
   CREATE INDEX ON measurement_y2008m01 (logdate);
   ```

4. Ensure that the[constraint\_exclusion](https://www.postgresql.org/docs/10/static/runtime-config-query.html#guc-constraint-exclusion)configuration parameter is not disabled in`postgresql.conf`. If it is, queries will not be optimized as desired.

In the above example we would be creating a new partition each month, so it might be wise to write a script that generates the required DDL automatically.

#### 5.10.2.2. Partition Maintenance

Normally the set of partitions established when initially defining the the table are not intended to remain static. It is common to want to remove old partitions of data and periodically add new partitions for new data. One of the most important advantages of partitioning is precisely that it allows this otherwise painful task to be executed nearly instantaneously by manipulating the partition structure, rather than physically moving large amounts of data around.

The simplest option for removing old data is to drop the partition that is no longer necessary:

```
DROP TABLE measurement_y2006m02;
```

This can very quickly delete millions of records because it doesn't have to individually delete every record. Note however that the above command requires taking an`ACCESS EXCLUSIVE`lock on the parent table.

Another option that is often preferable is to remove the partition from the partitioned table but retain access to it as a table in its own right:

```
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02;
```

This allows further operations to be performed on the data before it is dropped. For example, this is often a useful time to back up the data using`COPY`,pg\_dump, or similar tools. It might also be a useful time to aggregate data into smaller formats, perform other data manipulations, or run reports.

Similarly we can add a new partition to handle new data. We can create an empty partition in the partitioned table just as the original partitions were created above:

```
CREATE TABLE measurement_y2008m02 PARTITION OF measurement
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01')
    TABLESPACE fasttablespace;
```

As an alternative, it is sometimes more convenient to create the new table outside the partition structure, and make it a proper partition later. This allows the data to be loaded, checked, and transformed prior to it appearing in the partitioned table:

```
CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS)
  TABLESPACE fasttablespace;

ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate 
>
= DATE '2008-02-01' AND logdate 
<
 DATE '2008-03-01' );

\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work

ALTER TABLE measurement ATTACH PARTITION measurement_y2008m02
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01' );
```

Before running the`ATTACH PARTITION`command, it is recommended to create a`CHECK`constraint on the table to be attached describing the desired partition constraint. That way, the system will be able to skip the scan to validate the implicit partition constraint. Without such a constraint, the table will be scanned to validate the partition constraint while holding an`ACCESS EXCLUSIVE`lock on the parent table. One may then drop the constraint after`ATTACH PARTITION`is finished, because it is no longer necessary.

#### 5.10.2.3. Limitations

The following limitations apply to partitioned tables:

* There is no facility available to create the matching indexes on all partitions automatically. Indexes must be added to each partition with separate commands. This also means that there is no way to create a primary key, unique constraint, or exclusion constraint spanning all partitions; it is only possible to constrain each leaf partition individually.

* Since primary keys are not supported on partitioned tables, foreign keys referencing partitioned tables are not supported, nor are foreign key references from a partitioned table to some other table.

* Using the`ON CONFLICT`clause with partitioned tables will cause an error, because unique or exclusion constraints can only be created on individual partitions. There is no support for enforcing uniqueness \(or an exclusion constraint\) across an entire partitioning hierarchy.

* An`UPDATE`that causes a row to move from one partition to another fails, because the new value of the row fails to satisfy the implicit partition constraint of the original partition.

* Row triggers, if necessary, must be defined on individual partitions, not the partitioned table.

### 5.10.3. Implementation Using Inheritance

While the built-in declarative partitioning is suitable for most common use cases, there are some circumstances where a more flexible approach may be useful. Partitioning can be implemented using table inheritance, which allows for several features which are not supported by declarative partitioning, such as:

* Partitioning enforces a rule that all partitions must have exactly the same set of columns as the parent, but table inheritance allows children to have extra columns not present in the parent.

* Table inheritance allows for multiple inheritance.

* Declarative partitioning only supports list and range partitioning, whereas table inheritance allows data to be divided in a manner of the user's choosing. \(Note, however, that if constraint exclusion is unable to prune partitions effectively, query performance will be very poor.\)

* Some operations require a stronger lock when using declarative partitioning than when using table inheritance. For example, adding or removing a partition to or from a partitioned table requires taking an`ACCESS EXCLUSIVE`lock on the parent table, whereas a`SHARE UPDATE EXCLUSIVE`lock is enough in the case of regular inheritance.

#### 5.10.3.1. Example

We use the same`measurement`table we used above. To implement it as a partitioned table using inheritance, use the following steps:

1. Create the“master”table, from which all of the partitions will inherit. This table will contain no data. Do not define any check constraints on this table, unless you intend them to be applied equally to all partitions. There is no point in defining any indexes or unique constraints on it, either. For our example, master table is the`measurement`table as originally defined.

2. Create several“child”tables that each inherit from the master table. Normally, these tables will not add any columns to the set inherited from the master. Just as with declarative partitioning, these partitions are in every way normalPostgreSQLtables \(or foreign tables\).

   ```
   CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
   CREATE TABLE measurement_y2006m03 () INHERITS (measurement);
   ...
   CREATE TABLE measurement_y2007m11 () INHERITS (measurement);
   CREATE TABLE measurement_y2007m12 () INHERITS (measurement);
   CREATE TABLE measurement_y2008m01 () INHERITS (measurement);
   ```

3. Add non-overlapping table constraints to the partition tables to define the allowed key values in each partition.

   Typical examples would be:

   ```
   CHECK ( x = 1 )
   CHECK ( county IN ( 'Oxfordshire', 'Buckinghamshire', 'Warwickshire' ))
   CHECK ( outletID 
   >
   = 100 AND outletID 
   <
    200 )
   ```

   Ensure that the constraints guarantee that there is no overlap between the key values permitted in different partitions. A common mistake is to set up range constraints like:

   ```
   CHECK ( outletID BETWEEN 100 AND 200 )
   CHECK ( outletID BETWEEN 200 AND 300 )
   ```

   This is wrong since it is not clear which partition the key value 200 belongs in.

   It would be better to instead create partitions as follows:

   ```
   CREATE TABLE measurement_y2006m02 (
       CHECK ( logdate 
   >
   = DATE '2006-02-01' AND logdate 
   <
    DATE '2006-03-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2006m03 (
       CHECK ( logdate 
   >
   = DATE '2006-03-01' AND logdate 
   <
    DATE '2006-04-01' )
   ) INHERITS (measurement);

   ...
   CREATE TABLE measurement_y2007m11 (
       CHECK ( logdate 
   >
   = DATE '2007-11-01' AND logdate 
   <
    DATE '2007-12-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2007m12 (
       CHECK ( logdate 
   >
   = DATE '2007-12-01' AND logdate 
   <
    DATE '2008-01-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2008m01 (
       CHECK ( logdate 
   >
   = DATE '2008-01-01' AND logdate 
   <
    DATE '2008-02-01' )
   ) INHERITS (measurement);
   ```

4. For each partition, create an index on the key column\(s\), as well as any other indexes you might want.

   ```
   CREATE INDEX measurement_y2006m02_logdate ON measurement_y2006m02 (logdate);
   CREATE INDEX measurement_y2006m03_logdate ON measurement_y2006m03 (logdate);
   CREATE INDEX measurement_y2007m11_logdate ON measurement_y2007m11 (logdate);
   CREATE INDEX measurement_y2007m12_logdate ON measurement_y2007m12 (logdate);
   CREATE INDEX measurement_y2008m01_logdate ON measurement_y2008m01 (logdate);
   ```

5. We want our application to be able to say`INSERT INTO measurement ...`and have the data be redirected into the appropriate partition table. We can arrange that by attaching a suitable trigger function to the master table. If data will be added only to the latest partition, we can use a very simple trigger function:

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

   After creating the function, we create a trigger which calls the trigger function:

   ```
   CREATE TRIGGER insert_measurement_trigger
       BEFORE INSERT ON measurement
       FOR EACH ROW EXECUTE PROCEDURE measurement_insert_trigger();
   ```

   We must redefine the trigger function each month so that it always points to the current partition. The trigger definition does not need to be updated, however.

   We might want to insert data and have the server automatically locate the partition into which the row should be added. We could do this with a more complex trigger function, for example:

   ```
   CREATE OR REPLACE FUNCTION measurement_insert_trigger()
   RETURNS TRIGGER AS $$
   BEGIN
       IF ( NEW.logdate 
   >
   = DATE '2006-02-01' AND
            NEW.logdate 
   <
    DATE '2006-03-01' ) THEN
           INSERT INTO measurement_y2006m02 VALUES (NEW.*);
       ELSIF ( NEW.logdate 
   >
   = DATE '2006-03-01' AND
               NEW.logdate 
   <
    DATE '2006-04-01' ) THEN
           INSERT INTO measurement_y2006m03 VALUES (NEW.*);
       ...
       ELSIF ( NEW.logdate 
   >
   = DATE '2008-01-01' AND
               NEW.logdate 
   <
    DATE '2008-02-01' ) THEN
           INSERT INTO measurement_y2008m01 VALUES (NEW.*);
       ELSE
           RAISE EXCEPTION 'Date out of range.  Fix the measurement_insert_trigger() function!';
       END IF;
       RETURN NULL;
   END;
   $$
   LANGUAGE plpgsql;
   ```

   The trigger definition is the same as before. Note that each`IF`test must exactly match the`CHECK`constraint for its partition.

   While this function is more complex than the single-month case, it doesn't need to be updated as often, since branches can be added in advance of being needed.

   ### Note

   In practice it might be best to check the newest partition first, if most inserts go into that partition. For simplicity we have shown the trigger's tests in the same order as in other parts of this example.

   A different approach to redirecting inserts into the appropriate partition table is to set up rules, instead of a trigger, on the master table. For example:

   ```
   CREATE RULE measurement_insert_y2006m02 AS
   ON INSERT TO measurement WHERE
       ( logdate 
   >
   = DATE '2006-02-01' AND logdate 
   <
    DATE '2006-03-01' )
   DO INSTEAD
       INSERT INTO measurement_y2006m02 VALUES (NEW.*);
   ...
   CREATE RULE measurement_insert_y2008m01 AS
   ON INSERT TO measurement WHERE
       ( logdate 
   >
   = DATE '2008-01-01' AND logdate 
   <
    DATE '2008-02-01' )
   DO INSTEAD
       INSERT INTO measurement_y2008m01 VALUES (NEW.*);
   ```

   A rule has significantly more overhead than a trigger, but the overhead is paid once per query rather than once per row, so this method might be advantageous for bulk-insert situations. In most cases, however, the trigger method will offer better performance.

   Be aware that`COPY`ignores rules. If you want to use`COPY`to insert data, you'll need to copy into the correct partition table rather than into the master.`COPY`does fire triggers, so you can use it normally if you use the trigger approach.

   Another disadvantage of the rule approach is that there is no simple way to force an error if the set of rules doesn't cover the insertion date; the data will silently go into the master table instead.

6. Ensure that the[constraint\_exclusion](https://www.postgresql.org/docs/10/static/runtime-config-query.html#guc-constraint-exclusion)configuration parameter is not disabled in`postgresql.conf`. If it is, queries will not be optimized as desired.

As we can see, a complex partitioning scheme could require a substantial amount of DDL. In the above example we would be creating a new partition each month, so it might be wise to write a script that generates the required DDL automatically.

#### 5.10.3.2. Partition Maintenance

To remove old data quickly, simply drop the partition that is no longer necessary:

```
DROP TABLE measurement_y2006m02;
```

To remove the partition from the partitioned table but retain access to it as a table in its own right:

```
ALTER TABLE measurement_y2006m02 NO INHERIT measurement;
```

To add a new partition to handle new data, create an empty partition just as the original partitions were created above:

```
CREATE TABLE measurement_y2008m02 (
    CHECK ( logdate 
>
= DATE '2008-02-01' AND logdate 
<
 DATE '2008-03-01' )
) INHERITS (measurement);
```

Alternatively, one may want to create the new table outside the partition structure, and make it a partition after the data is loaded, checked, and transformed.

```
CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate 
>
= DATE '2008-02-01' AND logdate 
<
 DATE '2008-03-01' );
\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work
ALTER TABLE measurement_y2008m02 INHERIT measurement;
```

#### 5.10.3.3. Caveats

The following caveats apply to partitioned tables implemented using inheritance:

* There is no automatic way to verify that all of the`CHECK`constraints are mutually exclusive. It is safer to create code that generates partitions and creates and/or modifies associated objects than to write each by hand.

* The schemes shown here assume that the partition key column\(s\) of a row never change, or at least do not change enough to require it to move to another partition. An`UPDATE`that attempts to do that will fail because of the`CHECK`constraints. If you need to handle such cases, you can put suitable update triggers on the partition tables, but it makes management of the structure much more complicated.

* If you are using manual`VACUUM`or`ANALYZE`commands, don't forget that you need to run them on each partition individually. A command like:

  ```
  ANALYZE measurement;
  ```

  will only process the master table.

* `INSERT`statements with`ON CONFLICT`clauses are unlikely to work as expected, as the`ON CONFLICT`action is only taken in case of unique violations on the specified target relation, not its child relations.

* Triggers or rules will be needed to route rows to the desired partition, unless the application is explicitly aware of the partitioning scheme. Triggers may be complicated to write, and will be much slower than the tuple routing performed internally by declarative partitioning.

### 5.10.4. Partitioning and Constraint Exclusion

\_Constraint exclusion\_is a query optimization technique that improves performance for partitioned tables defined in the fashion described above \(both declaratively partitioned tables and those implemented using inheritance\). As an example:

```
SET constraint_exclusion = on;
SELECT count(*) FROM measurement WHERE logdate 
>
= DATE '2008-01-01';
```

Without constraint exclusion, the above query would scan each of the partitions of the`measurement`table. With constraint exclusion enabled, the planner will examine the constraints of each partition and try to prove that the partition need not be scanned because it could not contain any rows meeting the query's`WHERE`clause. When the planner can prove this, it excludes the partition from the query plan.

You can use the`EXPLAIN`command to show the difference between a plan with`constraint_exclusion`on and a plan with it off. A typical unoptimized plan for this type of table setup is:

```
SET constraint_exclusion = off;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate 
>
= DATE '2008-01-01';

                                          QUERY PLAN
-----------------------------------------------------------------------------------------------
 Aggregate  (cost=158.66..158.68 rows=1 width=0)
   -
>
  Append  (cost=0.00..151.88 rows=2715 width=0)
         -
>
  Seq Scan on measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate 
>
= '2008-01-01'::date)
         -
>
  Seq Scan on measurement_y2006m02 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate 
>
= '2008-01-01'::date)
         -
>
  Seq Scan on measurement_y2006m03 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate 
>
= '2008-01-01'::date)
...
         -
>
  Seq Scan on measurement_y2007m12 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate 
>
= '2008-01-01'::date)
         -
>
  Seq Scan on measurement_y2008m01 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate 
>
= '2008-01-01'::date)
```

Some or all of the partitions might use index scans instead of full-table sequential scans, but the point here is that there is no need to scan the older partitions at all to answer this query. When we enable constraint exclusion, we get a significantly cheaper plan that will deliver the same answer:

```
SET constraint_exclusion = on;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate 
>
= DATE '2008-01-01';
                                          QUERY PLAN
-----------------------------------------------------------------------------------------------
 Aggregate  (cost=63.47..63.48 rows=1 width=0)
   -
>
  Append  (cost=0.00..60.75 rows=1086 width=0)
         -
>
  Seq Scan on measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate 
>
= '2008-01-01'::date)
         -
>
  Seq Scan on measurement_y2008m01 measurement  (cost=0.00..30.38 rows=543 width=0)
               Filter: (logdate 
>
= '2008-01-01'::date)
```

Note that constraint exclusion is driven only by`CHECK`constraints, not by the presence of indexes. Therefore it isn't necessary to define indexes on the key columns. Whether an index needs to be created for a given partition depends on whether you expect that queries that scan the partition will generally scan a large part of the partition or just a small part. An index will be helpful in the latter case but not the former.

The default \(and recommended\) setting of[constraint\_exclusion](https://www.postgresql.org/docs/10/static/runtime-config-query.html#guc-constraint-exclusion)is actually neither`on`nor`off`, but an intermediate setting called`partition`, which causes the technique to be applied only to queries that are likely to be working on partitioned tables. The`on`setting causes the planner to examine`CHECK`constraints in all queries, even simple ones that are unlikely to benefit.

The following caveats apply to constraint exclusion, which is used by both inheritance and partitioned tables:

* Constraint exclusion only works when the query's`WHERE`clause contains constants \(or externally supplied parameters\). For example, a comparison against a non-immutable function such as`CURRENT_TIMESTAMP`cannot be optimized, since the planner cannot know which partition the function value might fall into at run time.

* Keep the partitioning constraints simple, else the planner may not be able to prove that partitions don't need to be visited. Use simple equality conditions for list partitioning, or simple range tests for range partitioning, as illustrated in the preceding examples. A good rule of thumb is that partitioning constraints should contain only comparisons of the partitioning column\(s\) to constants using B-tree-indexable operators, which applies even to partitioned tables, because only B-tree-indexable column\(s\) are allowed in the partition key. \(This is not a problem when using declarative partitioning, since the automatically generated constraints are simple enough to be understood by the planner.\)

* All constraints on all partitions of the master table are examined during constraint exclusion, so large numbers of partitions are likely to increase query planning time considerably. Partitioning using these techniques will work well with up to perhaps a hundred partitions; don't try to use many thousands of partitions.

---

[^1]: [PostgreSQL: Documentation: 10: 5.10. Table Partitioning](https://www.postgresql.org/docs/10/static/ddl-partitioning.html)

