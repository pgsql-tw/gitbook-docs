# 5.11. 分割資料表

PostgreSQL 支援基本的分割資料表。本節描述了為什麼以及如何在資料庫設計中實現分割資料表。

## 5.11.1. 概念

分割資料表指的是將一個大型資料表以邏輯規則實體拆分為較小的資料庫。分割資料表可以帶來以下好處：

* 在某些情況下，尤其是當資料表中大多數被頻繁存取的資料位於單個分割區或少量的分割區之中時，查詢效能可以顯著地提高。分割區替代了索引的前幾個欄位，從而縮減了索引的大小，並使索引中頻繁使用的部分更有可能都放入記憶體之中。
* 當查詢或更新存取單個分割區的很大一部分時，可以透過對該分割區進行循序掃描而不是使用索引和遍及整個資料表的隨機讀取來提高效能。
* 如果計劃程序將這種需求計劃在分割區的設計中，則可以透過增加或刪除分區來完成批次加入和刪除。使用 ALTER TABLE DETACH PARTITION 或使用 DROP TABLE 刪除單個分割區比批次操作要快得多。這些命令還完全避免了由批次 DELETE 所增加的 VACUUM 成本。
* 很少使用的資料可以遷移到慢一些，但更便宜的儲存媒體上。

通常只有在資料表很大的情況下，這些好處才是值得的。資料表可以從分割區中受益的確切評估點取決於應用程式，儘管經驗法則是資料表的大小超過資料庫伺服器的記憶體大小的時候。

PostgreSQL 內建支援以下形式的分割方式：

### Range Partitioning

此資料庫表的分割區以一個欄位為鍵或一組欄位定義的「range」來分配，分配給不同分割區的範圍之間沒有重疊。例如，可以按日期範圍或特定業務對象的標識範圍進行分割。

### List Partitioning

透過明確列出哪些鍵值出現應該在哪個分割區中來對資料表進行分割。

### Hash Partitioning

透過為每個分割區指定除數和餘數來對資料表進行分割。每個分割區將保留其分割鍵的雜湊值除以指定的除數所產生指定的餘數的資料列。

如果您的應用程式需要使用上面未列出的其他分割區形式，則可以使用替代方法，例如繼承和 UNION ALL 檢視表。此類方法提供了靈活性，但沒有內建宣告分割區的效能優勢。

## 5.11.2. 宣告分割資料表

你可以在 PostgreSQL 上宣告一個資料表實際上被劃分為多個分割區。被劃分的資料表稱為分割資料表。此宣告包括如上所述的分割區方法，以及要用作分割區主鍵的欄位或表示式的列表。

分割資料表本身是一個「虛擬」資料表，沒有自己的儲存空間。而是儲存屬於分割區，分割區是與分割資料表相關聯的基本資料表。每個分割區都儲存由其分割區範圍定義的資料子集合。插入分割區資料表中的所有的資料都將根據分割主鍵欄位的值被重新導向到相應的其中一個分割區之中。如果某筆資料的分割主鍵不再滿足其原始分割區的分割區範圍，所以 UPDATE 該筆資料將可能導致其遷移至其他分割區。

分割區本身也可以定義為分割資料表，從而形成子分割區。儘管所有分割區都必須與其分割區的父親具有相同的欄位，但是分割區可以擁有自己的索引、限制條件和預設值，與其他分割區的索引、限制條件和預設值不同。有關建立分割區表和分割區的更多詳細說明，請參閱 [CREATE TABLE](../../reference/sql-commands/create-table.md)。

It is not possible to turn a regular table into a partitioned table or vice versa. However, it is possible to add an existing regular or partitioned table as a partition of a partitioned table, or remove a partition from a partitioned table turning it into a standalone table; this can simplify and speed up many maintenance processes. See [ALTER TABLE](https://www.postgresql.org/docs/13/sql-altertable.html) to learn more about the `ATTACH PARTITION` and `DETACH PARTITION` sub-commands.

Partitions can also be foreign tables, although they have some limitations that normal tables do not; see [CREATE FOREIGN TABLE](https://www.postgresql.org/docs/13/sql-createforeigntable.html) for more information.

### **5.11.2.1. Example**

Suppose we are constructing a database for a large ice cream company. The company measures peak temperatures every day as well as ice cream sales in each region. Conceptually, we want a table like:

```text
CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
);
```

We know that most queries will access just the last week's, month's or quarter's data, since the main use of this table will be to prepare online reports for management. To reduce the amount of old data that needs to be stored, we decide to only keep the most recent 3 years worth of data. At the beginning of each month we will remove the oldest month's data. In this situation we can use partitioning to help us meet all of our different requirements for the measurements table.

To use declarative partitioning in this case, use the following steps:

1. Create `measurement` table as a partitioned table by specifying the `PARTITION BY` clause, which includes the partitioning method \(`RANGE` in this case\) and the list of column\(s\) to use as the partition key.

   ```text
   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   ) PARTITION BY RANGE (logdate);
   ```

   You may decide to use multiple columns in the partition key for range partitioning, if desired. Of course, this will often result in a larger number of partitions, each of which is individually smaller. On the other hand, using fewer columns may lead to a coarser-grained partitioning criteria with smaller number of partitions. A query accessing the partitioned table will have to scan fewer partitions if the conditions involve some or all of these columns. For example, consider a table range partitioned using columns `lastname` and `firstname` \(in that order\) as the partition key.

2. Create partitions. Each partition's definition must specify the bounds that correspond to the partitioning method and partition key of the parent. Note that specifying bounds such that the new partition's values will overlap with those in one or more existing partitions will cause an error. Inserting data into the parent table that does not map to one of the existing partitions will cause an error; an appropriate partition must be added manually.

   Partitions thus created are in every way normal PostgreSQL tables \(or, possibly, foreign tables\). It is possible to specify a tablespace and storage parameters for each partition separately.

   It is not necessary to create table constraints describing partition boundary condition for partitions. Instead, partition constraints are generated implicitly from the partition bound specification whenever there is need to refer to them.

   ```text
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

   To implement sub-partitioning, specify the `PARTITION BY` clause in the commands used to create individual partitions, for example:

   ```text
   CREATE TABLE measurement_y2006m02 PARTITION OF measurement
       FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')
       PARTITION BY RANGE (peaktemp);
   ```

   After creating partitions of `measurement_y2006m02`, any data inserted into `measurement` that is mapped to `measurement_y2006m02` \(or data that is directly inserted into `measurement_y2006m02`, provided it satisfies its partition constraint\) will be further redirected to one of its partitions based on the `peaktemp` column. The partition key specified may overlap with the parent's partition key, although care should be taken when specifying the bounds of a sub-partition such that the set of data it accepts constitutes a subset of what the partition's own bounds allows; the system does not try to check whether that's really the case.

3. Create an index on the key column\(s\), as well as any other indexes you might want, on the partitioned table. \(The key index is not strictly necessary, but in most scenarios it is helpful.\) This automatically creates one index on each partition, and any partitions you create or attach later will also contain the index.

   ```text
   CREATE INDEX ON measurement (logdate);
   ```

4. Ensure that the [enable\_partition\_pruning](https://www.postgresql.org/docs/12/runtime-config-query.html#GUC-ENABLE-PARTITION-PRUNING) configuration parameter is not disabled in `postgresql.conf`. If it is, queries will not be optimized as desired.

In the above example we would be creating a new partition each month, so it might be wise to write a script that generates the required DDL automatically.

### **5.11.2.2. Partition Maintenance**

Normally the set of partitions established when initially defining the table are not intended to remain static. It is common to want to remove old partitions of data and periodically add new partitions for new data. One of the most important advantages of partitioning is precisely that it allows this otherwise painful task to be executed nearly instantaneously by manipulating the partition structure, rather than physically moving large amounts of data around.

The simplest option for removing old data is to drop the partition that is no longer necessary:

```text
DROP TABLE measurement_y2006m02;
```

This can very quickly delete millions of records because it doesn't have to individually delete every record. Note however that the above command requires taking an `ACCESS EXCLUSIVE` lock on the parent table.

Another option that is often preferable is to remove the partition from the partitioned table but retain access to it as a table in its own right:

```text
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02;
```

This allows further operations to be performed on the data before it is dropped. For example, this is often a useful time to back up the data using `COPY`, pg\_dump, or similar tools. It might also be a useful time to aggregate data into smaller formats, perform other data manipulations, or run reports.

Similarly we can add a new partition to handle new data. We can create an empty partition in the partitioned table just as the original partitions were created above:

```text
CREATE TABLE measurement_y2008m02 PARTITION OF measurement
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01')
    TABLESPACE fasttablespace;
```

As an alternative, it is sometimes more convenient to create the new table outside the partition structure, and make it a proper partition later. This allows the data to be loaded, checked, and transformed prior to it appearing in the partitioned table:

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

Before running the `ATTACH PARTITION` command, it is recommended to create a `CHECK` constraint on the table to be attached matching the desired partition constraint. That way, the system will be able to skip the scan to validate the implicit partition constraint. Without the `CHECK` constraint, the table will be scanned to validate the partition constraint while holding an `ACCESS EXCLUSIVE` lock on that partition and a `SHARE UPDATE EXCLUSIVE` lock on the parent table. It may be desired to drop the redundant `CHECK` constraint after `ATTACH PARTITION` is finished.

As explained above, it is possible to create indexes on partitioned tables and they are applied automatically to the entire hierarchy. This is very convenient, as not only the existing partitions will become indexed, but also any partitions that are created in the future will. One limitation is that it's not possible to use the `CONCURRENTLY` qualifier when creating such a partitioned index. To overcome long lock times, it is possible to use `CREATE INDEX ON ONLY` the partitioned table; such an index is marked invalid, and the partitions do not get the index applied automatically. The indexes on partitions can be created separately using `CONCURRENTLY`, and later _attached_ to the index on the parent using `ALTER INDEX .. ATTACH PARTITION`. Once indexes for all partitions are attached to the parent index, the parent index is marked valid automatically. Example:

```text
CREATE INDEX measurement_usls_idx ON ONLY measurement (unitsales);

CREATE INDEX measurement_usls_200602_idx
    ON measurement_y2006m02 (unitsales);
ALTER INDEX measurement_usls_idx
    ATTACH PARTITION measurement_usls_200602_idx;
...
```

This technique can be used with `UNIQUE` and `PRIMARY KEY` constraints too; the indexes are created implicitly when the constraint is created. Example:

```text
ALTER TABLE ONLY measurement ADD UNIQUE (city_id, logdate);

ALTER TABLE measurement_y2006m02 ADD UNIQUE (city_id, logdate);
ALTER INDEX measurement_city_id_logdate_key
    ATTACH PARTITION measurement_y2006m02_city_id_logdate_key;
...
```

### **5.11.2.3. Limitations**

以下是分割區資料表的限制：

* 無法建立跨所有分割區的限制條件。只能單獨對每個分割區設定。
* 分割區資料表上的唯一性限制條件必須包含所有分割主鍵欄位。存在此限制是因為 PostgreSQL 只能在每個分割區中個別實施唯一性。
* 必要時，必須在單個分割區（而不是分割資料表）上定義 BEFORE ROW 觸發器。
* 不允許在同一分割區中混合臨時和永久關連。因此，如果分割資料表是永久性的，則分割區也必須是永久性的，或者都臨時的。使用臨時關連時，分割資料表的所有成員必須來自同一個資料庫連線。

## 5.11.3. Implementation Using Inheritance

While the built-in declarative partitioning is suitable for most common use cases, there are some circumstances where a more flexible approach may be useful. Partitioning can be implemented using table inheritance, which allows for several features not supported by declarative partitioning, such as:

* For declarative partitioning, partitions must have exactly the same set of columns as the partitioned table, whereas with table inheritance, child tables may have extra columns not present in the parent.
* Table inheritance allows for multiple inheritance.
* Declarative partitioning only supports range, list and hash partitioning, whereas table inheritance allows data to be divided in a manner of the user's choosing. \(Note, however, that if constraint exclusion is unable to prune child tables effectively, query performance might be poor.\)
* Some operations require a stronger lock when using declarative partitioning than when using table inheritance. For example, adding or removing a partition to or from a partitioned table requires taking an `ACCESS EXCLUSIVE` lock on the parent table, whereas a `SHARE UPDATE EXCLUSIVE` lock is enough in the case of regular inheritance.

### **5.11.3.1. Example**

We use the same `measurement` table we used above. To implement partitioning using inheritance, use the following steps:

1. Create the “master” table, from which all of the “child” tables will inherit. This table will contain no data. Do not define any check constraints on this table, unless you intend them to be applied equally to all child tables. There is no point in defining any indexes or unique constraints on it, either. For our example, the master table is the `measurement` table as originally defined.
2. Create several “child” tables that each inherit from the master table. Normally, these tables will not add any columns to the set inherited from the master. Just as with declarative partitioning, these tables are in every way normal PostgreSQL tables \(or foreign tables\).

   ```text
   CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
   CREATE TABLE measurement_y2006m03 () INHERITS (measurement);
   ...
   CREATE TABLE measurement_y2007m11 () INHERITS (measurement);
   CREATE TABLE measurement_y2007m12 () INHERITS (measurement);
   CREATE TABLE measurement_y2008m01 () INHERITS (measurement);
   ```

3. Add non-overlapping table constraints to the child tables to define the allowed key values in each.

   Typical examples would be:

   ```text
   CHECK ( x = 1 )
   CHECK ( county IN ( 'Oxfordshire', 'Buckinghamshire', 'Warwickshire' ))
   CHECK ( outletID >= 100 AND outletID < 200 )
   ```

   Ensure that the constraints guarantee that there is no overlap between the key values permitted in different child tables. A common mistake is to set up range constraints like:

   ```text
   CHECK ( outletID BETWEEN 100 AND 200 )
   CHECK ( outletID BETWEEN 200 AND 300 )
   ```

   This is wrong since it is not clear which child table the key value 200 belongs in.

   It would be better to instead create child tables as follows:

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

4. For each child table, create an index on the key column\(s\), as well as any other indexes you might want.

   ```text
   CREATE INDEX measurement_y2006m02_logdate ON measurement_y2006m02 (logdate);
   CREATE INDEX measurement_y2006m03_logdate ON measurement_y2006m03 (logdate);
   CREATE INDEX measurement_y2007m11_logdate ON measurement_y2007m11 (logdate);
   CREATE INDEX measurement_y2007m12_logdate ON measurement_y2007m12 (logdate);
   CREATE INDEX measurement_y2008m01_logdate ON measurement_y2008m01 (logdate);
   ```

5. We want our application to be able to say `INSERT INTO measurement ...` and have the data be redirected into the appropriate child table. We can arrange that by attaching a suitable trigger function to the master table. If data will be added only to the latest child, we can use a very simple trigger function:

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

   After creating the function, we create a trigger which calls the trigger function:

   ```text
   CREATE TRIGGER insert_measurement_trigger
       BEFORE INSERT ON measurement
       FOR EACH ROW EXECUTE FUNCTION measurement_insert_trigger();
   ```

   We must redefine the trigger function each month so that it always points to the current child table. The trigger definition does not need to be updated, however.

   We might want to insert data and have the server automatically locate the child table into which the row should be added. We could do this with a more complex trigger function, for example:

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

   The trigger definition is the same as before. Note that each `IF` test must exactly match the `CHECK` constraint for its child table.

   While this function is more complex than the single-month case, it doesn't need to be updated as often, since branches can be added in advance of being needed.

   **Note**

   In practice, it might be best to check the newest child first, if most inserts go into that child. For simplicity, we have shown the trigger's tests in the same order as in other parts of this example.

   A different approach to redirecting inserts into the appropriate child table is to set up rules, instead of a trigger, on the master table. For example:

   ```text
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

   A rule has significantly more overhead than a trigger, but the overhead is paid once per query rather than once per row, so this method might be advantageous for bulk-insert situations. In most cases, however, the trigger method will offer better performance.

   Be aware that `COPY` ignores rules. If you want to use `COPY` to insert data, you'll need to copy into the correct child table rather than directly into the master. `COPY` does fire triggers, so you can use it normally if you use the trigger approach.

   Another disadvantage of the rule approach is that there is no simple way to force an error if the set of rules doesn't cover the insertion date; the data will silently go into the master table instead.

6. Ensure that the [constraint\_exclusion](https://www.postgresql.org/docs/12/runtime-config-query.html#GUC-CONSTRAINT-EXCLUSION) configuration parameter is not disabled in `postgresql.conf`; otherwise child tables may be accessed unnecessarily.

As we can see, a complex table hierarchy could require a substantial amount of DDL. In the above example we would be creating a new child table each month, so it might be wise to write a script that generates the required DDL automatically.

### **5.11.3.2. Maintenance For Inheritance Partitioning**

To remove old data quickly, simply drop the child table that is no longer necessary:

```text
DROP TABLE measurement_y2006m02;
```

To remove the child table from the inheritance hierarchy table but retain access to it as a table in its own right:

```text
ALTER TABLE measurement_y2006m02 NO INHERIT measurement;
```

To add a new child table to handle new data, create an empty child table just as the original children were created above:

```text
CREATE TABLE measurement_y2008m02 (
    CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' )
) INHERITS (measurement);
```

Alternatively, one may want to create and populate the new child table before adding it to the table hierarchy. This could allow data to be loaded, checked, and transformed before being made visible to queries on the parent table.

```text
CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' );
\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work
ALTER TABLE measurement_y2008m02 INHERIT measurement;
```

### **5.11.3.3. Caveats**

The following caveats apply to partitioning implemented using inheritance:

* There is no automatic way to verify that all of the `CHECK` constraints are mutually exclusive. It is safer to create code that generates child tables and creates and/or modifies associated objects than to write each by hand.
* Indexes and foreign key constraints apply to single tables and not to their inheritance children, hence they have some [caveats](https://www.postgresql.org/docs/12/ddl-inherit.html#DDL-INHERIT-CAVEATS) to be aware of.
* The schemes shown here assume that the values of a row's key column\(s\) never change, or at least do not change enough to require it to move to another partition. An `UPDATE` that attempts to do that will fail because of the `CHECK` constraints. If you need to handle such cases, you can put suitable update triggers on the child tables, but it makes management of the structure much more complicated.
* If you are using manual `VACUUM` or `ANALYZE` commands, don't forget that you need to run them on each child table individually. A command like:

  ```text
  ANALYZE measurement;
  ```

  will only process the master table.

* `INSERT` statements with `ON CONFLICT` clauses are unlikely to work as expected, as the `ON CONFLICT` action is only taken in case of unique violations on the specified target relation, not its child relations.
* Triggers or rules will be needed to route rows to the desired child table, unless the application is explicitly aware of the partitioning scheme. Triggers may be complicated to write, and will be much slower than the tuple routing performed internally by declarative partitioning.

## 5.11.4. Partition Pruning

Partition pruning \(分割區修剪\)是一種查詢最佳化技術，可提高分割資料表的效能。 舉個例子：

```text
SET enable_partition_pruning = on;                 -- the default
SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
```

如果不進行分割區修剪，則上面的查詢將掃描 measurement 資料表的每個分割區。啟用分割區修剪後，計劃程序將檢查每個分割區的定義並證明不需要掃描該分割區，因為該分割區不會包含滿足查詢 WHERE 子句的資料。當計劃程序可以證明這一點時，它將從查詢計劃中排除（修剪）分割區。

透過使用 EXPLAIN 指令和 [enable\_partition\_pruning](../../server-administration/server-configuration/query-planning.md#enable_partition_pruning-boolean) 組態參數，可以顯示已修剪分割區的計劃與未修剪分割區的計劃之間差異。對於這種類型的資料表設定，典型未最佳化的計劃是：

```text
SET enable_partition_pruning = off;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-----------------------------------------------------------------------------------
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

有一部份的分割區可能使用索引掃描而不是全資料表的循序掃描，但是這裡的要點是根本不需要掃描較舊的分區來回應此查詢。啟用 partition pruning 之後，我們將獲得更為簡單的查詢計劃，該計劃能夠提供相同的回應：

```text
SET enable_partition_pruning = on;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Aggregate  (cost=37.75..37.76 rows=1 width=8)
   ->  Seq Scan on measurement_y2008m01  (cost=0.00..33.12 rows=617 width=0)
         Filter: (logdate >= '2008-01-01'::date)
```

請注意，partition pruning 僅由分割主鍵隱含定義的內容而來，而不會參考索引。因此，不需要在相關欄位上定義索引。是否需要為該分割區建立索引取決於您是否希望掃描分割區的查詢會掃描大部分分割區還是僅掃描一小部分。在後者情況下，索引將有所幫助，但對於前者則無濟於事。

Partition pruning can be performed not only during the planning of a given query, but also during its execution. This is useful as it can allow more partitions to be pruned when clauses contain expressions whose values are not known at query planning time, for example, parameters defined in a `PREPARE` statement, using a value obtained from a subquery, or using a parameterized value on the inner side of a nested loop join. Partition pruning during execution can be performed at any of the following times:

* During initialization of the query plan. Partition pruning can be performed here for parameter values which are known during the initialization phase of execution. Partitions which are pruned during this stage will not show up in the query's `EXPLAIN` or `EXPLAIN ANALYZE`. It is possible to determine the number of partitions which were removed during this phase by observing the “Subplans Removed” property in the `EXPLAIN` output.
* During actual execution of the query plan. Partition pruning may also be performed here to remove partitions using values which are only known during actual query execution. This includes values from subqueries and values from execution-time parameters such as those from parameterized nested loop joins. Since the value of these parameters may change many times during the execution of the query, partition pruning is performed whenever one of the execution parameters being used by partition pruning changes. Determining if partitions were pruned during this phase requires careful inspection of the `loops` property in the `EXPLAIN ANALYZE` output. Subplans corresponding to different partitions may have different values for it depending on how many times each of them was pruned during execution. Some may be shown as `(never executed)` if they were pruned every time.

可以使用 [enable\_partition\_pruning](../../server-administration/server-configuration/query-planning.md#enable_partition_pruning-boolean) 設定來停用 partition pruning。

{% hint style="info" %}
目前僅會在 Append 和 MergeAppend 節點類型上執行 partition pruning。尚未為 ModifyTable 節點類型實作此功能，但是在將來的 PostgreSQL 版本中可能會有所改進。
{% endhint %}

## 5.11.5. Partitioning and Constraint Exclusion

_Constraint exclusion_ is a query optimization technique similar to partition pruning. While it is primarily used for partitioning implemented using the legacy inheritance method, it can be used for other purposes, including with declarative partitioning.

Constraint exclusion works in a very similar way to partition pruning, except that it uses each table's `CHECK` constraints — which gives it its name — whereas partition pruning uses the table's partition bounds, which exist only in the case of declarative partitioning. Another difference is that constraint exclusion is only applied at plan time; there is no attempt to remove partitions at execution time.

The fact that constraint exclusion uses `CHECK` constraints, which makes it slow compared to partition pruning, can sometimes be used as an advantage: because constraints can be defined even on declaratively-partitioned tables, in addition to their internal partition bounds, constraint exclusion may be able to elide additional partitions from the query plan.

The default \(and recommended\) setting of [constraint\_exclusion](https://www.postgresql.org/docs/12/runtime-config-query.html#GUC-CONSTRAINT-EXCLUSION) is neither `on` nor `off`, but an intermediate setting called `partition`, which causes the technique to be applied only to queries that are likely to be working on inheritance partitioned tables. The `on` setting causes the planner to examine `CHECK` constraints in all queries, even simple ones that are unlikely to benefit.

The following caveats apply to constraint exclusion:

* Constraint exclusion is only applied during query planning, unlike partition pruning, which can also be applied during query execution.
* Constraint exclusion only works when the query's `WHERE` clause contains constants \(or externally supplied parameters\). For example, a comparison against a non-immutable function such as `CURRENT_TIMESTAMP` cannot be optimized, since the planner cannot know which child table the function's value might fall into at run time.
* Keep the partitioning constraints simple, else the planner may not be able to prove that child tables might not need to be visited. Use simple equality conditions for list partitioning, or simple range tests for range partitioning, as illustrated in the preceding examples. A good rule of thumb is that partitioning constraints should contain only comparisons of the partitioning column\(s\) to constants using B-tree-indexable operators, because only B-tree-indexable column\(s\) are allowed in the partition key.
* All constraints on all children of the parent table are examined during constraint exclusion, so large numbers of children are likely to increase query planning time considerably. So the legacy inheritance based partitioning will work well with up to perhaps a hundred child tables; don't try to use many thousands of children.

## 5.11.6. Declarative Partitioning Best Practices

The choice of how to partition a table should be made carefully as the performance of query planning and execution can be negatively affected by poor design.

One of the most critical design decisions will be the column or columns by which you partition your data. Often the best choice will be to partition by the column or set of columns which most commonly appear in `WHERE` clauses of queries being executed on the partitioned table. `WHERE` clause items that match and are compatible with the partition key can be used to prune unneeded partitions. However, you may be forced into making other decisions by requirements for the `PRIMARY KEY` or a `UNIQUE` constraint. Removal of unwanted data is also a factor to consider when planning your partitioning strategy. An entire partition can be detached fairly quickly, so it may be beneficial to design the partition strategy in such a way that all data to be removed at once is located in a single partition.

Choosing the target number of partitions that the table should be divided into is also a critical decision to make. Not having enough partitions may mean that indexes remain too large and that data locality remains poor which could result in low cache hit ratios. However, dividing the table into too many partitions can also cause issues. Too many partitions can mean longer query planning times and higher memory consumption during both query planning and execution. When choosing how to partition your table, it's also important to consider what changes may occur in the future. For example, if you choose to have one partition per customer and you currently have a small number of large customers, consider the implications if in several years you instead find yourself with a large number of small customers. In this case, it may be better to choose to partition by `HASH` and choose a reasonable number of partitions rather than trying to partition by `LIST` and hoping that the number of customers does not increase beyond what it is practical to partition the data by.

Sub-partitioning can be useful to further divide partitions that are expected to become larger than other partitions, although excessive sub-partitioning can easily lead to large numbers of partitions and can cause the same problems mentioned in the preceding paragraph.

It is also important to consider the overhead of partitioning during query planning and execution. The query planner is generally able to handle partition hierarchies with up to a few thousand partitions fairly well, provided that typical queries allow the query planner to prune all but a small number of partitions. Planning times become longer and memory consumption becomes higher when more partitions remain after the planner performs partition pruning. This is particularly true for the `UPDATE` and `DELETE` commands. Another reason to be concerned about having a large number of partitions is that the server's memory consumption may grow significantly over a period of time, especially if many sessions touch large numbers of partitions. That's because each partition requires its metadata to be loaded into the local memory of each session that touches it.

With data warehouse type workloads, it can make sense to use a larger number of partitions than with an OLTP type workload. Generally, in data warehouses, query planning time is less of a concern as the majority of processing time is spent during query execution. With either of these two types of workload, it is important to make the right decisions early, as re-partitioning large quantities of data can be painfully slow. Simulations of the intended workload are often beneficial for optimizing the partitioning strategy. Never assume that more partitions are better than fewer partitions and vice-versa.  


