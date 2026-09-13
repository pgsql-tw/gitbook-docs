<a id="PLPGSQL-TRIGGER"></a>

## 41.10. 觸發程序函式 [#](#PLPGSQL-TRIGGER)

[41.10.1. 資料異動的觸發程序](plpgsql-trigger.md#PLPGSQL-DML-TRIGGER)

[41.10.2. 事件的觸發程序](plpgsql-trigger.md#PLPGSQL-EVENT-TRIGGER)

<a id="id-1.8.8.12.2"></a>

PL/pgSQL 可以用來定義因資料異動或資料庫事件而執行的觸發程序函式。觸發程序函式是以 `CREATE FUNCTION` 指令建立的，宣告時不帶任何引數，回傳型別為 `trigger`（用於資料異動的觸發程序）或 `event_trigger`（用於資料庫事件的觸發程序）。系統會自動定義名為 `TG_something` 的特殊區域變數，用來描述觸發這次呼叫的條件。

<a id="PLPGSQL-DML-TRIGGER"></a>

### 41.10.1. 資料異動的觸發程序 [#](#PLPGSQL-DML-TRIGGER)

[資料異動觸發程序](../triggers/README.md)宣告為一個不帶引數、回傳型別為 `trigger` 的函式。請注意，即使該函式預期會收到在 `CREATE TRIGGER` 中指定的一些引數，它仍然必須宣告為不帶引數——這類引數是透過 `TG_ARGV` 傳入的，如下所述。

當 PL/pgSQL 函式被當成觸發程序呼叫時，會在最上層區塊中自動建立幾個特殊變數。它們是：

<a id="PLPGSQL-DML-TRIGGER-NEW"></a>

`NEW` `record` [#](#PLPGSQL-DML-TRIGGER-NEW)
:   資料列層級觸發程序中，`INSERT`/`UPDATE` 操作所產生的新資料庫資料列。在陳述式層級的觸發程序中，以及在 `DELETE` 操作中，這個變數為 null。
<a id="PLPGSQL-DML-TRIGGER-OLD"></a>

`OLD` `record` [#](#PLPGSQL-DML-TRIGGER-OLD)
:   資料列層級觸發程序中，`UPDATE`/`DELETE` 操作所對應的舊資料庫資料列。在陳述式層級的觸發程序中，以及在 `INSERT` 操作中，這個變數為 null。
<a id="PLPGSQL-DML-TRIGGER-TG-NAME"></a>

`TG_NAME` `name` [#](#PLPGSQL-DML-TRIGGER-TG-NAME)
:   被觸發的那個觸發程序的名稱。
<a id="PLPGSQL-DML-TRIGGER-TG-WHEN"></a>

`TG_WHEN` `text` [#](#PLPGSQL-DML-TRIGGER-TG-WHEN)
:   `BEFORE`、`AFTER` 或 `INSTEAD OF`，視該觸發程序的定義而定。
<a id="PLPGSQL-DML-TRIGGER-TG-LEVEL"></a>

`TG_LEVEL` `text` [#](#PLPGSQL-DML-TRIGGER-TG-LEVEL)
:   `ROW` 或 `STATEMENT`，視該觸發程序的定義而定。
<a id="PLPGSQL-DML-TRIGGER-TG-OP"></a>

`TG_OP` `text` [#](#PLPGSQL-DML-TRIGGER-TG-OP)
:   觸發此觸發程序的操作：`INSERT`、`UPDATE`、`DELETE` 或 `TRUNCATE`。
<a id="PLPGSQL-DML-TRIGGER-TG-RELID"></a>

`TG_RELID` `oid`（參照 [`pg_class`](../../internals/catalogs/catalog-pg-class.md).`oid`） [#](#PLPGSQL-DML-TRIGGER-TG-RELID)
:   引發此觸發程序呼叫的資料表之物件 ID。
<a id="PLPGSQL-DML-TRIGGER-TG-RELNAME"></a>

`TG_RELNAME` `name` [#](#PLPGSQL-DML-TRIGGER-TG-RELNAME)
:   引發此觸發程序呼叫的資料表。此變數現已不建議使用，並可能在未來的版本中消失。請改用 `TG_TABLE_NAME`。
<a id="PLPGSQL-DML-TRIGGER-TG-TABLE-NAME"></a>

`TG_TABLE_NAME` `name` [#](#PLPGSQL-DML-TRIGGER-TG-TABLE-NAME)
:   引發此觸發程序呼叫的資料表。
<a id="PLPGSQL-DML-TRIGGER-TG-TABLE-SCHEMA"></a>

`TG_TABLE_SCHEMA` `name` [#](#PLPGSQL-DML-TRIGGER-TG-TABLE-SCHEMA)
:   引發此觸發程序呼叫的資料表所屬的綱要。
<a id="PLPGSQL-DML-TRIGGER-TG-NARGS"></a>

`TG_NARGS` `integer` [#](#PLPGSQL-DML-TRIGGER-TG-NARGS)
:   在 `CREATE TRIGGER` 陳述式中傳給觸發程序函式的引數個數。
<a id="PLPGSQL-DML-TRIGGER-TG-ARGV"></a>

`TG_ARGV` `text[]` [#](#PLPGSQL-DML-TRIGGER-TG-ARGV)
:   來自 `CREATE TRIGGER` 陳述式的引數。索引由 0 開始計算。無效的索引（小於 0，或大於等於 `tg_nargs`）會得到 null 值。

觸發程序函式必須回傳 `NULL`，或是一個結構與該觸發程序所屬資料表完全相同的 record／資料列值。

以 `BEFORE` 觸發的資料列層級觸發程序可以回傳 null，藉此告知觸發程序管理員跳過這筆資料列後續的其餘操作（亦即後續的觸發程序不會被觸發，而這筆資料列的 `INSERT`/`UPDATE`/`DELETE` 也不會發生）。如果回傳的是非 null 值，則該操作會以這個資料列值繼續進行。回傳與 `NEW` 原本的值不同的資料列值，會改變即將被新增或更新的資料列。因此，如果觸發程序函式希望讓觸發它的動作正常完成而不改變資料列的值，就必須回傳 `NEW`（或是與其相等的值）。若要改變即將被儲存的資料列，可以直接在 `NEW` 中替換個別的值並回傳修改後的 `NEW`，或是建立一筆完整的新 record／資料列來回傳。至於 `DELETE` 上的 before 觸發程序，其回傳值沒有直接的作用，但必須是非 null，才能讓觸發它的動作繼續進行。請注意，在 `DELETE` 的觸發程序中 `NEW` 為 null，因此回傳它通常並不合理。在 `DELETE` 的觸發程序中，慣用的寫法是回傳 `OLD`。

`INSTEAD OF` 觸發程序（一律為資料列層級的觸發程序，且只能用在檢視表上）可以回傳 null，以表示它並未執行任何更新，且這筆資料列後續的其餘操作應該被跳過（亦即後續的觸發程序不會被觸發，而這筆資料列也不會被計入外層 `INSERT`/`UPDATE`/`DELETE` 的受影響資料列數中）。否則就應該回傳非 null 值，以表示該觸發程序已執行了所要求的操作。對於 `INSERT` 與 `UPDATE` 操作，回傳值應該是 `NEW`，而觸發程序函式可以修改它，以支援 `INSERT RETURNING` 與 `UPDATE RETURNING`（這也會影響傳給任何後續觸發程序的資料列值，或是在帶有 `ON CONFLICT DO
UPDATE` 子句的 `INSERT` 陳述式中，傳給特殊的 `EXCLUDED` 別名參照的資料列值）。對於 `DELETE` 操作，回傳值應該是 `OLD`。

以 `AFTER` 觸發的資料列層級觸發程序，或是以 `BEFORE` 或 `AFTER` 觸發的陳述式層級觸發程序，其回傳值一律會被忽略；回傳 null 也無妨。不過，這幾類觸發程序仍然可以藉由拋出錯誤來中止整個操作。

[範例 41.3](plpgsql-trigger.md#PLPGSQL-TRIGGER-EXAMPLE) 展示了一個以 PL/pgSQL 撰寫的觸發程序函式範例。

<a id="PLPGSQL-TRIGGER-EXAMPLE"></a>

**範例 41.3. 一個 PL/pgSQL 觸發程序函式**

這個範例觸發程序可確保每當資料表中有資料列被新增或更新時，目前的使用者名稱與時間都會被標記到該資料列中。它同時也會檢查員工的姓名有被填寫，而且薪資是正數。

```

CREATE TABLE emp (
    empname           text,
    salary            integer,
    last_date         timestamp,
    last_user         text
);

CREATE FUNCTION emp_stamp() RETURNS trigger AS $emp_stamp$
    BEGIN
        -- Check that empname and salary are given
        IF NEW.empname IS NULL THEN
            RAISE EXCEPTION 'empname cannot be null';
        END IF;
        IF NEW.salary IS NULL THEN
            RAISE EXCEPTION '% cannot have null salary', NEW.empname;
        END IF;

        -- Who works for us when they must pay for it?
        IF NEW.salary < 0 THEN
            RAISE EXCEPTION '% cannot have a negative salary', NEW.empname;
        END IF;

        -- Remember who changed the payroll when
        NEW.last_date := current_timestamp;
        NEW.last_user := current_user;
        RETURN NEW;
    END;
$emp_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER emp_stamp BEFORE INSERT OR UPDATE ON emp
    FOR EACH ROW EXECUTE FUNCTION emp_stamp();
```

<br>

另一種記錄資料表異動的方式，是建立一個新的資料表，為每一次發生的新增、更新或刪除各保存一筆資料列。這種做法可以視為對資料表異動的稽核。[範例 41.4](plpgsql-trigger.md#PLPGSQL-TRIGGER-AUDIT-EXAMPLE) 展示了一個以 PL/pgSQL 撰寫的稽核觸發程序函式範例。

<a id="PLPGSQL-TRIGGER-AUDIT-EXAMPLE"></a>

**範例 41.4. 一個用於稽核的 PL/pgSQL 觸發程序函式**

這個範例觸發程序可確保 `emp` 資料表中任何資料列的新增、更新或刪除，都會被記錄（亦即稽核）到 `emp_audit` 資料表中。目前的時間與使用者名稱會被標記到該資料列裡，並一併記下對它所執行的操作類型。

```

CREATE TABLE emp (
    empname           text NOT NULL,
    salary            integer
);

CREATE TABLE emp_audit(
    operation         char(1)   NOT NULL,
    stamp             timestamp NOT NULL,
    userid            text      NOT NULL,
    empname           text      NOT NULL,
    salary            integer
);

CREATE OR REPLACE FUNCTION process_emp_audit() RETURNS TRIGGER AS $emp_audit$
    BEGIN
        --
        -- Create a row in emp_audit to reflect the operation performed on emp,
        -- making use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO emp_audit SELECT 'D', now(), current_user, OLD.*;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO emp_audit SELECT 'U', now(), current_user, NEW.*;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO emp_audit SELECT 'I', now(), current_user, NEW.*;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$emp_audit$ LANGUAGE plpgsql;

CREATE TRIGGER emp_audit
AFTER INSERT OR UPDATE OR DELETE ON emp
    FOR EACH ROW EXECUTE FUNCTION process_emp_audit();
```

<br>

前一個範例的一種變化，是使用一個將主資料表與稽核資料表聯結起來的檢視表，以顯示每一筆項目最後被修改的時間。這種做法仍然會完整記錄資料表異動的稽核軌跡，但同時也提供了稽核軌跡的簡化檢視，只呈現由稽核軌跡推導出的、每一筆項目最後修改的時間戳記。[範例 41.5](plpgsql-trigger.md#PLPGSQL-VIEW-TRIGGER-AUDIT-EXAMPLE) 展示了一個以 PL/pgSQL 撰寫、建立在檢視表上的稽核觸發程序範例。

<a id="PLPGSQL-VIEW-TRIGGER-AUDIT-EXAMPLE"></a>

**範例 41.5. 一個用於稽核的 PL/pgSQL 檢視表觸發程序函式**

這個範例在檢視表上使用觸發程序，使該檢視表成為可更新的，並確保檢視表中任何資料列的新增、更新或刪除，都會被記錄（亦即稽核）到 `emp_audit` 資料表中。目前的時間與使用者名稱會被記錄下來，並一併記下所執行的操作類型，而該檢視表會顯示每一筆資料列最後修改的時間。

```

CREATE TABLE emp (
    empname           text PRIMARY KEY,
    salary            integer
);

CREATE TABLE emp_audit(
    operation         char(1)   NOT NULL,
    userid            text      NOT NULL,
    empname           text      NOT NULL,
    salary            integer,
    stamp             timestamp NOT NULL
);

CREATE VIEW emp_view AS
    SELECT e.empname,
           e.salary,
           max(ea.stamp) AS last_updated
      FROM emp e
      LEFT JOIN emp_audit ea ON ea.empname = e.empname
     GROUP BY 1, 2;

CREATE OR REPLACE FUNCTION update_emp_view() RETURNS TRIGGER AS $$
    BEGIN
        --
        -- Perform the required operation on emp, and create a row in emp_audit
        -- to reflect the change made to emp.
        --
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM emp WHERE empname = OLD.empname;
            IF NOT FOUND THEN RETURN NULL; END IF;

            OLD.last_updated = now();
            INSERT INTO emp_audit VALUES('D', current_user, OLD.*);
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE emp SET salary = NEW.salary WHERE empname = OLD.empname;
            IF NOT FOUND THEN RETURN NULL; END IF;

            NEW.last_updated = now();
            INSERT INTO emp_audit VALUES('U', current_user, NEW.*);
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO emp VALUES(NEW.empname, NEW.salary);

            NEW.last_updated = now();
            INSERT INTO emp_audit VALUES('I', current_user, NEW.*);
            RETURN NEW;
        END IF;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER emp_audit
INSTEAD OF INSERT OR UPDATE OR DELETE ON emp_view
    FOR EACH ROW EXECUTE FUNCTION update_emp_view();
```

<br>

觸發程序的用途之一，是維護另一個資料表的彙總資料表。所得到的彙總結果，在某些查詢中可以用來取代原本的資料表——通常執行時間會大幅縮短。這項技巧常用於資料倉儲，因為其中存放實際量測或觀測資料的資料表（稱為事實資料表）可能極為龐大。[範例 41.6](plpgsql-trigger.md#PLPGSQL-TRIGGER-SUMMARY-EXAMPLE) 展示了一個以 PL/pgSQL 撰寫的觸發程序函式範例，用來為資料倉儲中的事實資料表維護彙總資料表。

<a id="PLPGSQL-TRIGGER-SUMMARY-EXAMPLE"></a>

**範例 41.6. 一個用於維護彙總資料表的 PL/pgSQL 觸發程序函式**

此處詳述的綱要，部分是根據 Ralph Kimball 所著 *The Data Warehouse Toolkit* 一書中的 *Grocery Store* 範例。

```

--
-- Main tables - time dimension and sales fact.
--
CREATE TABLE time_dimension (
    time_key                    integer NOT NULL,
    day_of_week                 integer NOT NULL,
    day_of_month                integer NOT NULL,
    month                       integer NOT NULL,
    quarter                     integer NOT NULL,
    year                        integer NOT NULL
);
CREATE UNIQUE INDEX time_dimension_key ON time_dimension(time_key);

CREATE TABLE sales_fact (
    time_key                    integer NOT NULL,
    product_key                 integer NOT NULL,
    store_key                   integer NOT NULL,
    amount_sold                 numeric(12,2) NOT NULL,
    units_sold                  integer NOT NULL,
    amount_cost                 numeric(12,2) NOT NULL
);
CREATE INDEX sales_fact_time ON sales_fact(time_key);

--
-- Summary table - sales by time.
--
CREATE TABLE sales_summary_bytime (
    time_key                    integer NOT NULL,
    amount_sold                 numeric(15,2) NOT NULL,
    units_sold                  numeric(12) NOT NULL,
    amount_cost                 numeric(15,2) NOT NULL
);
CREATE UNIQUE INDEX sales_summary_bytime_key ON sales_summary_bytime(time_key);

--
-- Function and trigger to amend summarized column(s) on UPDATE, INSERT, DELETE.
--
CREATE OR REPLACE FUNCTION maint_sales_summary_bytime() RETURNS TRIGGER
AS $maint_sales_summary_bytime$
    DECLARE
        delta_time_key          integer;
        delta_amount_sold       numeric(15,2);
        delta_units_sold        numeric(12);
        delta_amount_cost       numeric(15,2);
    BEGIN

        -- Work out the increment/decrement amount(s).
        IF (TG_OP = 'DELETE') THEN

            delta_time_key = OLD.time_key;
            delta_amount_sold = -1 * OLD.amount_sold;
            delta_units_sold = -1 * OLD.units_sold;
            delta_amount_cost = -1 * OLD.amount_cost;

        ELSIF (TG_OP = 'UPDATE') THEN

            -- forbid updates that change the time_key -
            -- (probably not too onerous, as DELETE + INSERT is how most
            -- changes will be made).
            IF ( OLD.time_key != NEW.time_key) THEN
                RAISE EXCEPTION 'Update of time_key : % -> % not allowed',
                                                      OLD.time_key, NEW.time_key;
            END IF;

            delta_time_key = OLD.time_key;
            delta_amount_sold = NEW.amount_sold - OLD.amount_sold;
            delta_units_sold = NEW.units_sold - OLD.units_sold;
            delta_amount_cost = NEW.amount_cost - OLD.amount_cost;

        ELSIF (TG_OP = 'INSERT') THEN

            delta_time_key = NEW.time_key;
            delta_amount_sold = NEW.amount_sold;
            delta_units_sold = NEW.units_sold;
            delta_amount_cost = NEW.amount_cost;

        END IF;


        -- Insert or update the summary row with the new values.
        <<insert_update>>
        LOOP
            UPDATE sales_summary_bytime
                SET amount_sold = amount_sold + delta_amount_sold,
                    units_sold = units_sold + delta_units_sold,
                    amount_cost = amount_cost + delta_amount_cost
                WHERE time_key = delta_time_key;

            EXIT insert_update WHEN found;

            BEGIN
                INSERT INTO sales_summary_bytime (
                            time_key,
                            amount_sold,
                            units_sold,
                            amount_cost)
                    VALUES (
                            delta_time_key,
                            delta_amount_sold,
                            delta_units_sold,
                            delta_amount_cost
                           );

                EXIT insert_update;

            EXCEPTION
                WHEN UNIQUE_VIOLATION THEN
                    -- do nothing
            END;
        END LOOP insert_update;

        RETURN NULL;

    END;
$maint_sales_summary_bytime$ LANGUAGE plpgsql;

CREATE TRIGGER maint_sales_summary_bytime
AFTER INSERT OR UPDATE OR DELETE ON sales_fact
    FOR EACH ROW EXECUTE FUNCTION maint_sales_summary_bytime();

INSERT INTO sales_fact VALUES(1,1,1,10,3,15);
INSERT INTO sales_fact VALUES(1,2,1,20,5,35);
INSERT INTO sales_fact VALUES(2,2,1,40,15,135);
INSERT INTO sales_fact VALUES(2,3,1,10,1,13);
SELECT * FROM sales_summary_bytime;
DELETE FROM sales_fact WHERE product_key = 1;
SELECT * FROM sales_summary_bytime;
UPDATE sales_fact SET units_sold = units_sold * 2;
SELECT * FROM sales_summary_bytime;
```

<br>

`AFTER` 觸發程序也可以利用*轉換資料表*來檢視觸發它的陳述式所異動的整組資料列。`CREATE TRIGGER` 指令會為其中一個或兩個轉換資料表指定名稱，接著函式就可以引用這些名稱，彷彿它們是唯讀的暫存資料表一般。[範例 41.7](plpgsql-trigger.md#PLPGSQL-TRIGGER-AUDIT-TRANSITION-EXAMPLE) 展示了一個例子。

<a id="PLPGSQL-TRIGGER-AUDIT-TRANSITION-EXAMPLE"></a>

**範例 41.7. 使用轉換資料表進行稽核**

這個範例產生的結果與[範例 41.4](plpgsql-trigger.md#PLPGSQL-TRIGGER-AUDIT-EXAMPLE) 相同，但它不是使用對每一筆資料列都觸發的觸發程序，而是先在轉換資料表中收集相關資訊，再使用每個陳述式只觸發一次的觸發程序。當觸發它的陳述式異動了許多資料列時，這種做法會比資料列觸發程序的做法快上許多。請注意，我們必須為每一種事件各自撰寫一段觸發程序宣告，因為每種情況的 `REFERENCING` 子句必須不同。但這並不妨礙我們選擇只使用單一個觸發程序函式。（實務上，或許使用三個各自獨立的函式、避免在執行期檢測 `TG_OP`，會是比較好的做法。）

```

CREATE TABLE emp (
    empname           text NOT NULL,
    salary            integer
);

CREATE TABLE emp_audit(
    operation         char(1)   NOT NULL,
    stamp             timestamp NOT NULL,
    userid            text      NOT NULL,
    empname           text      NOT NULL,
    salary            integer
);

CREATE OR REPLACE FUNCTION process_emp_audit() RETURNS TRIGGER AS $emp_audit$
    BEGIN
        --
        -- Create rows in emp_audit to reflect the operations performed on emp,
        -- making use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO emp_audit
                SELECT 'D', now(), current_user, o.* FROM old_table o;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO emp_audit
                SELECT 'U', now(), current_user, n.* FROM new_table n;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO emp_audit
                SELECT 'I', now(), current_user, n.* FROM new_table n;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$emp_audit$ LANGUAGE plpgsql;

CREATE TRIGGER emp_audit_ins
    AFTER INSERT ON emp
    REFERENCING NEW TABLE AS new_table
    FOR EACH STATEMENT EXECUTE FUNCTION process_emp_audit();
CREATE TRIGGER emp_audit_upd
    AFTER UPDATE ON emp
    REFERENCING OLD TABLE AS old_table NEW TABLE AS new_table
    FOR EACH STATEMENT EXECUTE FUNCTION process_emp_audit();
CREATE TRIGGER emp_audit_del
    AFTER DELETE ON emp
    REFERENCING OLD TABLE AS old_table
    FOR EACH STATEMENT EXECUTE FUNCTION process_emp_audit();
```

<br>

<a id="PLPGSQL-EVENT-TRIGGER"></a>

### 41.10.2. 事件的觸發程序 [#](#PLPGSQL-EVENT-TRIGGER)

PL/pgSQL 可以用來定義[事件觸發程序](../event-triggers/README.md)。PostgreSQL 要求，要被當成事件觸發程序呼叫的函式，必須宣告為不帶引數、回傳型別為 `event_trigger` 的函式。

當 PL/pgSQL 函式被當成事件觸發程序呼叫時，會在最上層區塊中自動建立幾個特殊變數。它們是：

<a id="PLPGSQL-EVENT-TRIGGER-TG-EVENT"></a>

`TG_EVENT` `text` [#](#PLPGSQL-EVENT-TRIGGER-TG-EVENT)
:   觸發此觸發程序的事件。
<a id="PLPGSQL-EVENT-TRIGGER-TG-TAG"></a>

`TG_TAG` `text` [#](#PLPGSQL-EVENT-TRIGGER-TG-TAG)
:   觸發此觸發程序的指令標籤。

[範例 41.8](plpgsql-trigger.md#PLPGSQL-EVENT-TRIGGER-EXAMPLE) 展示了一個以 PL/pgSQL 撰寫的事件觸發程序函式範例。

<a id="PLPGSQL-EVENT-TRIGGER-EXAMPLE"></a>

**範例 41.8. 一個 PL/pgSQL 事件觸發程序函式**

這個範例觸發程序只是在每次執行受支援的指令時，拋出一則 `NOTICE` 訊息。

```

CREATE OR REPLACE FUNCTION snitch() RETURNS event_trigger AS $$
BEGIN
    RAISE NOTICE 'snitch: % %', tg_event, tg_tag;
END;
$$ LANGUAGE plpgsql;

CREATE EVENT TRIGGER snitch ON ddl_command_start EXECUTE FUNCTION snitch();
```

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-trigger.html)（原文版本：18.6；核對日期：2026-09-13）
