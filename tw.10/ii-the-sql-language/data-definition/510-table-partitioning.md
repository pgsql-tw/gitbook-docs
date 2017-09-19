# 5.10. 分割表格[^1]

PostgreSQL 支援基礎的分散式資料表。

PostgreSQLsupports basic table partitioning. This section describes why and how to implement partitioning as part of your database design.

### 5.10.1. Overview

Partitioning refers to splitting what is logically one large table into smaller physical pieces. Partitioning can provide several benefits:

* Query performance can be improved dramatically in certain situations, particularly when most of the heavily accessed rows of the table are in a single partition or a small number of partitions. The partitioning substitutes for leading columns of indexes, reducing index size and making it more likely that the heavily-used parts of the indexes fit in memory.

* When queries or updates access a large percentage of a single partition, performance can be improved by taking advantage of sequential scan of that partition instead of using an index and random access reads scattered across the whole table.

* Bulk loads and deletes can be accomplished by adding or removing partitions, if that requirement is planned into the partitioning design. Doing`ALTER TABLE DETACH PARTITION`or dropping an individual partition using`DROP TABLE`is far faster than a bulk operation. These commands also entirely avoid the`VACUUM`overhead caused by a bulk`DELETE`.

* Seldom-used data can be migrated to cheaper and slower storage media.

The benefits will normally be worthwhile only when a table would otherwise be very large. The exact point at which a table will benefit from partitioning depends on the application, although a rule of thumb is that the size of the table should exceed the physical memory of the database server.

PostgreSQLoffers built-in support for the following forms of partitioning:

Range Partitioning

The table is partitioned into“ranges”defined by a key column or set of columns, with no overlap between the ranges of values assigned to different partitions. For example, one might partition by date ranges, or by ranges of identifiers for particular business objects.

List Partitioning

The table is partitioned by explicitly listing which key values appear in each partition.

If your application needs to use other forms of partitioning not listed above, alternative methods such as inheritance and`UNION ALL`views can be used instead. Such methods offer flexibility but do not have some of the performance benefits of built-in declarative partitioning.

### 5.10.2. Declarative Partitioning

PostgreSQLoffers a way to specify how to divide a table into pieces called partitions. The table that is divided is referred to as a_partitioned table_. The specification consists of the_partitioning method\_and a list of columns or expressions to be used as the\_partition key_.

All rows inserted into a partitioned table will be routed to one of the_partitions\_based on the value of the partition key. Each partition has a subset of the data defined by its\_partition bounds_. Currently supported partitioning methods include range and list, where each partition is assigned a range of keys and a list of keys, respectively.

Partitions may themselves be defined as partitioned tables, using what is called_sub-partitioning_. Partitions may have their own indexes, constraints and default values, distinct from those of other partitions. Indexes must be created separately for each partition. See[CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html)for more details on creating partitioned tables and partitions.

It is not possible to turn a regular table into a partitioned table or vice versa. However, it is possible to add a regular or partitioned table containing data as a partition of a partitioned table, or remove a partition from a partitioned table turning it into a standalone table; see[ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html)to learn more about the`ATTACH PARTITION`and`DETACH PARTITION`sub-commands.

Individual partitions are linked to the partitioned table with inheritance behind-the-scenes; however, it is not possible to use some of the inheritance features discussed in the previous section with partitioned tables and partitions. For example, a partition cannot have any parents other than the partitioned table it is a partition of, nor can a regular table inherit from a partitioned table making the latter its parent. That means partitioned tables and partitions do not participate in inheritance with regular tables. Since a partition hierarchy consisting of the partitioned table and its partitions is still an inheritance hierarchy, all the normal rules of inheritance apply as described in[Section 5.9](https://www.postgresql.org/docs/10/static/ddl-inherit.html)with some exceptions, most notably:

* Both`CHECK`and`NOT NULL`constraints of a partitioned table are always inherited by all its partitions.`CHECK`constraints that are marked`NO INHERIT`are not allowed to be created on partitioned tables.

* Using`ONLY`to add or drop a constraint on only the partitioned table is supported when there are no partitions. Once partitions exist, using`ONLY`will result in an error as adding or dropping constraints on only the partitioned table, when partitions exist, is not supported. Instead, constraints can be added or dropped, when they are not present in the parent table, directly on the partitions. As a partitioned table does not have any data directly, attempts to use`TRUNCATEONLY`on a partitioned table will always return an error.

* Partitions cannot have columns that are not present in the parent. It is neither possible to specify columns when creating partitions with`CREATE TABLE`nor is it possible to add columns to partitions after-the-fact using`ALTER TABLE`. Tables may be added as a partition with`ALTER TABLE ... ATTACH PARTITION`only if their columns exactly match the parent, including oids.

* You cannot drop the`NOT NULL`constraint on a partition's column if the constraint is present in the parent table.

Partitions can also be foreign tables \(see[CREATE FOREIGN TABLE](https://www.postgresql.org/docs/10/static/sql-createforeigntable.html)\), although these have some limitations that normal tables do not. For example, data inserted into the partitioned table is not routed to foreign table partitions.

#### 5.10.2.1. Example

Suppose we are constructing a database for a large ice cream company. The company measures peak temperatures every day as well as ice cream sales in each region. Conceptually, we want a table like:

```
CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
);
```

We know that most queries will access just the last week's, month's or quarter's data, since the main use of this table will be to prepare online reports for management. To reduce the amount of old data that needs to be stored, we decide to only keep the most recent 3 years worth of data. At the beginning of each month we will remove the oldest month's data. In this situation we can use partitioning to help us meet all of our different requirements for the measurements table.

To use declarative partitioning in this case, use the following steps:

1. Create`measurement`table as a partitioned table by specifying the`PARTITION BY`clause, which includes the partitioning method \(`RANGE`in this case\) and the list of column\(s\) to use as the partition key.

   ```
   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   ) PARTITION BY RANGE (logdate);
   ```

   You may decide to use multiple columns in the partition key for range partitioning, if desired. Of course, this will often result in a larger number of partitions, each of which is individually smaller. On the other hand, using fewer columns may lead to a coarser-grained partitioning criteria with smaller number of partitions. A query accessing the partitioned table will have to scan fewer partitions if the conditions involve some or all of these columns. For example, consider a table range partitioned using columns`lastname`and`firstname`\(in that order\) as the partition key.

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

