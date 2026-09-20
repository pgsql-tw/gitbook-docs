<a id="PLPGSQL-PORTING"></a>

## 41.13. 從 Oracle PL/SQL 移植 [#](#PLPGSQL-PORTING)

[41.13.1. 移植範例](plpgsql-porting.md#PLPGSQL-PORTING-EXAMPLES)

[41.13.2. 其他需要注意的事項](plpgsql-porting.md#PLPGSQL-PORTING-OTHER)

[41.13.3. 附錄](plpgsql-porting.md#PLPGSQL-PORTING-APPENDIX)

<a id="id-1.8.8.15.2"></a><a id="id-1.8.8.15.3"></a>

本節說明 PostgreSQL 的 PL/pgSQL 語言與 Oracle 的 PL/SQL 語言之間的差異，以協助將應用程式從 Oracle® 移植到 PostgreSQL 的開發人員。

PL/pgSQL 在許多方面都與 PL/SQL 相似。它是一種區塊結構式的命令式語言，而且所有變數都必須先宣告。指派、迴圈與條件式也都很類似。從 PL/SQL 移植到 PL/pgSQL 時，你應該謹記在心的主要差異如下：

* 如果 SQL 指令中所使用的某個名稱，既可能是該指令中所用資料表的欄位名稱，也可能是對函式某個變數的引用，PL/SQL 會把它當作欄位名稱。而 PL/pgSQL 在預設情況下會拋出錯誤，指出該名稱有歧義。你可以指定 `plpgsql.variable_conflict` = `use_column`，把這個行為改成與 PL/SQL 一致，如[第 41.11.1 節](plpgsql-implementation.md#PLPGSQL-VAR-SUBST)所述。通常最好一開始就避免這類歧義，但如果你必須移植大量倚賴這種行為的程式碼，設定 `variable_conflict` 可能會是最好的解法。
* 在 PostgreSQL 中，函式本文必須寫成字串常數。因此你需要使用錢字號引號（dollar quoting），或是把函式本文中的單引號跳脫掉。（參閱[第 41.12.1 節](plpgsql-development-tips.md#PLPGSQL-QUOTE-TIPS)。）
* 資料型別的名稱常常需要轉換。例如在 Oracle 中，字串值通常宣告為 `varchar2` 型別，這是一個非 SQL 標準的型別。在 PostgreSQL 中，請改用 `varchar` 或 `text` 型別。同樣地，請把 `number` 型別換成 `numeric`，或是在有更合適的選擇時改用其他數值資料型別。
* 請改用綱要（而非套件）來把你的函式組織成群組。
* 由於沒有套件，也就沒有套件層級的變數。這點有些惱人。你可以改用暫存資料表來保存每個工作階段的狀態。
* 帶有 `REVERSE` 的整數 `FOR` 迴圈運作方式不同：PL/SQL 是從第二個數字往下數到第一個數字，而 PL/pgSQL 則是從第一個數字往下數到第二個數字，因此移植時必須把迴圈的界限對調。這種不相容雖然令人遺憾，但不太可能會被更改。（參閱[第 41.6.5.5 節](plpgsql-control-structures.md#PLPGSQL-INTEGER-FOR)。）
* 走訪查詢（游標以外）的 `FOR` 迴圈運作方式也不同：目標變數必須事先宣告，而 PL/SQL 則一律隱含地宣告它們。這樣做的好處是，迴圈結束之後仍然可以存取這些變數的值。
* 在游標變數的使用上，有各式各樣的表示法差異。

<a id="PLPGSQL-PORTING-EXAMPLES"></a>

### 41.13.1. 移植範例 [#](#PLPGSQL-PORTING-EXAMPLES)

[範例 41.9](plpgsql-porting.md#PGSQL-PORTING-EX1) 展示如何把一個簡單的函式從 PL/SQL 移植到 PL/pgSQL。

<a id="PGSQL-PORTING-EX1"></a>

**範例 41.9. 把一個簡單的函式從 PL/SQL 移植到 PL/pgSQL**

以下是一個 Oracle PL/SQL 函式：

```

CREATE OR REPLACE FUNCTION cs_fmt_browser_version(v_name varchar2,
                                                  v_version varchar2)
RETURN varchar2 IS
BEGIN
    IF v_version IS NULL THEN
        RETURN v_name;
    END IF;
    RETURN v_name || '/' || v_version;
END;
/
show errors;
```

讓我們逐一檢視這個函式，看看它與 PL/pgSQL 相比有哪些差異：

* 型別名稱 `varchar2` 必須改成 `varchar` 或 `text`。在本節的範例中，我們會使用 `varchar`，但如果你不需要特定的字串長度限制，`text` 通常是更好的選擇。
* 函式原型（而非函式本文）中的 `RETURN` 關鍵字，在 PostgreSQL 中會變成 `RETURNS`。此外，`IS` 會變成 `AS`，而且你需要加上 `LANGUAGE` 子句，因為 PL/pgSQL 並不是唯一可用的函式語言。
* 在 PostgreSQL 中，函式本文被視為字串常數，因此你需要在它外面加上引號或錢字號引號。這取代了 Oracle 做法中結尾的 `/`。
* PostgreSQL 中不存在 `show errors` 指令，而且也不需要，因為錯誤會自動回報。

以下是這個函式移植到 PostgreSQL 之後的樣子：

```

CREATE OR REPLACE FUNCTION cs_fmt_browser_version(v_name varchar,
                                                  v_version varchar)
RETURNS varchar AS $$
BEGIN
    IF v_version IS NULL THEN
        RETURN v_name;
    END IF;
    RETURN v_name || '/' || v_version;
END;
$$ LANGUAGE plpgsql;
```

<br>

[範例 41.10](plpgsql-porting.md#PLPGSQL-PORTING-EX2) 展示如何移植一個會建立另一個函式的函式，以及如何處理隨之而來的引號問題。

<a id="PLPGSQL-PORTING-EX2"></a>

**範例 41.10. 把一個會建立另一個函式的函式從 PL/SQL 移植到 PL/pgSQL**

為了效率起見，以下這個程序會從一個 `SELECT` 陳述式取出資料列，並用其結果在 `IF` 陳述式中建構出一個龐大的函式。

這是 Oracle 版本：

```

CREATE OR REPLACE PROCEDURE cs_update_referrer_type_proc IS
    CURSOR referrer_keys IS
        SELECT * FROM cs_referrer_keys
        ORDER BY try_order;
    func_cmd VARCHAR(4000);
BEGIN
    func_cmd := 'CREATE OR REPLACE FUNCTION cs_find_referrer_type(v_host IN VARCHAR2,
                 v_domain IN VARCHAR2, v_url IN VARCHAR2) RETURN VARCHAR2 IS BEGIN';

    FOR referrer_key IN referrer_keys LOOP
        func_cmd := func_cmd ||
          ' IF v_' || referrer_key.kind
          || ' LIKE ''' || referrer_key.key_string
          || ''' THEN RETURN ''' || referrer_key.referrer_type
          || '''; END IF;';
    END LOOP;

    func_cmd := func_cmd || ' RETURN NULL; END;';

    EXECUTE IMMEDIATE func_cmd;
END;
/
show errors;
```

以下是這個函式在 PostgreSQL 中最後的樣子：

```

CREATE OR REPLACE PROCEDURE cs_update_referrer_type_proc() AS $func$
DECLARE
    referrer_keys CURSOR IS
        SELECT * FROM cs_referrer_keys
        ORDER BY try_order;
    func_body text;
    func_cmd text;
BEGIN
    func_body := 'BEGIN';

    FOR referrer_key IN referrer_keys LOOP
        func_body := func_body ||
          ' IF v_' || referrer_key.kind
          || ' LIKE ' || quote_literal(referrer_key.key_string)
          || ' THEN RETURN ' || quote_literal(referrer_key.referrer_type)
          || '; END IF;' ;
    END LOOP;

    func_body := func_body || ' RETURN NULL; END;';

    func_cmd :=
      'CREATE OR REPLACE FUNCTION cs_find_referrer_type(v_host varchar,
                                                        v_domain varchar,
                                                        v_url varchar)
        RETURNS varchar AS '
      || quote_literal(func_body)
      || ' LANGUAGE plpgsql;' ;

    EXECUTE func_cmd;
END;
$func$ LANGUAGE plpgsql;
```

請注意這個函式的本文是如何另外建構出來，並且通過 `quote_literal` 來把其中的引號都加倍。之所以需要這項技巧，是因為我們無法安全地使用錢字號引號來定義這個新函式：我們無法確知會有哪些字串從 `referrer_key.key_string` 欄位被內插進來。（我們在此假設 `referrer_key.kind` 可以被信任一律是 `host`、`domain` 或 `url`，但 `referrer_key.key_string` 則可能是任何內容，特別是它可能含有錢字號。）這個函式其實比 Oracle 原版更好，因為當 `referrer_key.key_string` 或 `referrer_key.referrer_type` 含有引號時，它不會產生出壞掉的程式碼。

<br>

[範例 41.11](plpgsql-porting.md#PLPGSQL-PORTING-EX3) 展示如何移植一個帶有 `OUT` 參數並進行字串處理的函式。PostgreSQL 沒有內建的 `instr` 函式，但你可以結合其他函式自行建立一個。在[第 41.13.3 節](plpgsql-porting.md#PLPGSQL-PORTING-APPENDIX)中有一份 `instr` 的 PL/pgSQL 實作，你可以拿來讓移植工作更輕鬆。

<a id="PLPGSQL-PORTING-EX3"></a>

**範例 41.11. 把一個帶有字串處理與 `OUT` 參數的程序從 PL/SQL 移植到 PL/pgSQL**

以下這個 Oracle PL/SQL 程序用來剖析一個 URL，並回傳數個元素（host、path 與 query）。

這是 Oracle 版本：

```

CREATE OR REPLACE PROCEDURE cs_parse_url(
    v_url IN VARCHAR2,
    v_host OUT VARCHAR2,  -- This will be passed back
    v_path OUT VARCHAR2,  -- This one too
    v_query OUT VARCHAR2) -- And this one
IS
    a_pos1 INTEGER;
    a_pos2 INTEGER;
BEGIN
    v_host := NULL;
    v_path := NULL;
    v_query := NULL;
    a_pos1 := instr(v_url, '//');

    IF a_pos1 = 0 THEN
        RETURN;
    END IF;
    a_pos2 := instr(v_url, '/', a_pos1 + 2);
    IF a_pos2 = 0 THEN
        v_host := substr(v_url, a_pos1 + 2);
        v_path := '/';
        RETURN;
    END IF;

    v_host := substr(v_url, a_pos1 + 2, a_pos2 - a_pos1 - 2);
    a_pos1 := instr(v_url, '?', a_pos2 + 1);

    IF a_pos1 = 0 THEN
        v_path := substr(v_url, a_pos2);
        RETURN;
    END IF;

    v_path := substr(v_url, a_pos2, a_pos1 - a_pos2);
    v_query := substr(v_url, a_pos1 + 1);
END;
/
show errors;
```

以下是一種可能的 PL/pgSQL 翻譯版本：

```

CREATE OR REPLACE FUNCTION cs_parse_url(
    v_url IN VARCHAR,
    v_host OUT VARCHAR,  -- This will be passed back
    v_path OUT VARCHAR,  -- This one too
    v_query OUT VARCHAR) -- And this one
AS $$
DECLARE
    a_pos1 INTEGER;
    a_pos2 INTEGER;
BEGIN
    v_host := NULL;
    v_path := NULL;
    v_query := NULL;
    a_pos1 := instr(v_url, '//');

    IF a_pos1 = 0 THEN
        RETURN;
    END IF;
    a_pos2 := instr(v_url, '/', a_pos1 + 2);
    IF a_pos2 = 0 THEN
        v_host := substr(v_url, a_pos1 + 2);
        v_path := '/';
        RETURN;
    END IF;

    v_host := substr(v_url, a_pos1 + 2, a_pos2 - a_pos1 - 2);
    a_pos1 := instr(v_url, '?', a_pos2 + 1);

    IF a_pos1 = 0 THEN
        v_path := substr(v_url, a_pos2);
        RETURN;
    END IF;

    v_path := substr(v_url, a_pos2, a_pos1 - a_pos2);
    v_query := substr(v_url, a_pos1 + 1);
END;
$$ LANGUAGE plpgsql;
```

這個函式可以這樣使用：

```

SELECT * FROM cs_parse_url('http://foobar.com/query.cgi?baz');
```

<br>

[範例 41.12](plpgsql-porting.md#PLPGSQL-PORTING-EX4) 展示如何移植一個使用了許多 Oracle 特有功能的程序。

<a id="PLPGSQL-PORTING-EX4"></a>

**範例 41.12. 把一個程序從 PL/SQL 移植到 PL/pgSQL**

Oracle 版本：

```

CREATE OR REPLACE PROCEDURE cs_create_job(v_job_id IN INTEGER) IS
    a_running_job_count INTEGER;
BEGIN
    LOCK TABLE cs_jobs IN EXCLUSIVE MODE;

    SELECT count(*) INTO a_running_job_count FROM cs_jobs WHERE end_stamp IS NULL;

    IF a_running_job_count > 0 THEN
        COMMIT; -- free lock
        raise_application_error(-20000,
                 'Unable to create a new job: a job is currently running.');
    END IF;

    DELETE FROM cs_active_job;
    INSERT INTO cs_active_job(job_id) VALUES (v_job_id);

    BEGIN
        INSERT INTO cs_jobs (job_id, start_stamp) VALUES (v_job_id, now());
    EXCEPTION
        WHEN dup_val_on_index THEN NULL; -- don't worry if it already exists
    END;
    COMMIT;
END;
/
show errors
```

以下是我們可以如何把這個程序移植到 PL/pgSQL：

```

CREATE OR REPLACE PROCEDURE cs_create_job(v_job_id integer) AS $$
DECLARE
    a_running_job_count integer;
BEGIN
    LOCK TABLE cs_jobs IN EXCLUSIVE MODE;

    SELECT count(*) INTO a_running_job_count FROM cs_jobs WHERE end_stamp IS NULL;

    IF a_running_job_count > 0 THEN
        COMMIT; -- free lock
        RAISE EXCEPTION 'Unable to create a new job: a job is currently running'; -- (1)
    END IF;

    DELETE FROM cs_active_job;
    INSERT INTO cs_active_job(job_id) VALUES (v_job_id);

    BEGIN
        INSERT INTO cs_jobs (job_id, start_stamp) VALUES (v_job_id, now());
    EXCEPTION
        WHEN unique_violation THEN -- (2)
            -- don't worry if it already exists
    END;
    COMMIT;
END;
$$ LANGUAGE plpgsql;
```

<a id="co.plpgsql-porting-raise"></a><a id="co.plpgsql-porting-exception"></a>

<table border="0" summary="Callout list"><tr><td align="left" valign="top" width="5%"><p><a href="#co.plpgsql-porting-raise">(1)</a> </p></td><td align="left" valign="top"><p>
       <code class="literal">RAISE</code> 的語法與 Oracle 的陳述式有相當大的差異，不過基本形式 <code class="literal">RAISE</code> <em class="replaceable"><code>exception_name</code></em> 的運作方式類似。
      </p></td></tr><tr><td align="left" valign="top" width="5%"><p><a href="#co.plpgsql-porting-exception">(2)</a> </p></td><td align="left" valign="top"><p>
       <span class="application">PL/pgSQL</span> 所支援的例外名稱與 Oracle 的並不相同。內建例外名稱的集合大得多（參閱 <a class="xref" href="../../appendixes/errcodes-appendix/README.md">附錄 A</a>）。目前並沒有辦法宣告使用者自訂的例外名稱，不過你可以改為拋出使用者自選的 SQLSTATE 值。
      </p></td></tr></table>

<br>

<a id="PLPGSQL-PORTING-OTHER"></a>

### 41.13.2. 其他需要注意的事項 [#](#PLPGSQL-PORTING-OTHER)

本節說明把 Oracle PL/SQL 函式移植到 PostgreSQL 時，另外幾件需要注意的事情。

<a id="PLPGSQL-PORTING-EXCEPTIONS"></a>

#### 41.13.2.1. 例外之後的隱含回復 [#](#PLPGSQL-PORTING-EXCEPTIONS)

在 PL/pgSQL 中，當例外被 `EXCEPTION` 子句攔截時，自該區塊的 `BEGIN` 以來的所有資料庫變更都會自動回復。也就是說，這個行為等同於你在 Oracle 中以下面的寫法所得到的結果：

```

BEGIN
    SAVEPOINT s1;
    ... code here ...
EXCEPTION
    WHEN ... THEN
        ROLLBACK TO s1;
        ... code here ...
    WHEN ... THEN
        ROLLBACK TO s1;
        ... code here ...
END;
```

如果你要轉換的 Oracle 程序是以這種風格使用 `SAVEPOINT` 與 `ROLLBACK TO`，你的工作就很輕鬆：只要把 `SAVEPOINT` 與 `ROLLBACK TO` 省略即可。如果你的程序是以不同的方式使用 `SAVEPOINT` 與 `ROLLBACK TO`，那就需要實際動點腦筋了。

<a id="PLPGSQL-PORTING-OTHER-EXECUTE"></a>

#### 41.13.2.2. `EXECUTE` [#](#PLPGSQL-PORTING-OTHER-EXECUTE)

PL/pgSQL 版本的 `EXECUTE` 運作方式與 PL/SQL 版本類似，但你必須記得依照[第 41.5.4 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)所述使用 `quote_literal` 與 `quote_ident`。除非你使用這些函式，否則 `EXECUTE 'SELECT * FROM $1';` 這類寫法並不能可靠地運作。

<a id="PLPGSQL-PORTING-OPTIMIZATION"></a>

#### 41.13.2.3. 最佳化 PL/pgSQL 函式 [#](#PLPGSQL-PORTING-OPTIMIZATION)

PostgreSQL 提供了兩個建立函式時可用的修飾詞來最佳化執行：「變動性」（volatility，亦即該函式在給定相同引數時是否一律回傳相同結果）與「嚴格性」（strictness，亦即當任何引數為 null 時該函式是否回傳 null）。詳情請參閱 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md) 參考頁面。

當你利用這些最佳化屬性時，你的 `CREATE FUNCTION` 陳述式可能看起來會像這樣：

```

CREATE FUNCTION foo(...) RETURNS integer AS $$
...
$$ LANGUAGE plpgsql STRICT IMMUTABLE;
```

<a id="PLPGSQL-PORTING-APPENDIX"></a>

### 41.13.3. 附錄 [#](#PLPGSQL-PORTING-APPENDIX)

本節包含一組與 Oracle 相容的 `instr` 函式的程式碼，你可以用它們來簡化移植工作。

<a id="id-1.8.8.15.8.3"></a>

```

--
-- instr functions that mimic Oracle's counterpart
-- Syntax: instr(string1, string2 [, n [, m]])
-- where [] denotes optional parameters.
--
-- Search string1, beginning at the nth character, for the mth occurrence
-- of string2.  If n is negative, search backwards, starting at the abs(n)'th
-- character from the end of string1.
-- If n is not passed, assume 1 (search starts at first character).
-- If m is not passed, assume 1 (find first occurrence).
-- Returns starting index of string2 in string1, or 0 if string2 is not found.
--

CREATE FUNCTION instr(varchar, varchar) RETURNS integer AS $$
BEGIN
    RETURN instr($1, $2, 1);
END;
$$ LANGUAGE plpgsql STRICT IMMUTABLE;


CREATE FUNCTION instr(string varchar, string_to_search_for varchar,
                      beg_index integer)
RETURNS integer AS $$
DECLARE
    pos integer NOT NULL DEFAULT 0;
    temp_str varchar;
    beg integer;
    length integer;
    ss_length integer;
BEGIN
    IF beg_index > 0 THEN
        temp_str := substring(string FROM beg_index);
        pos := position(string_to_search_for IN temp_str);

        IF pos = 0 THEN
            RETURN 0;
        ELSE
            RETURN pos + beg_index - 1;
        END IF;
    ELSIF beg_index < 0 THEN
        ss_length := char_length(string_to_search_for);
        length := char_length(string);
        beg := length + 1 + beg_index;

        WHILE beg > 0 LOOP
            temp_str := substring(string FROM beg FOR ss_length);
            IF string_to_search_for = temp_str THEN
                RETURN beg;
            END IF;

            beg := beg - 1;
        END LOOP;

        RETURN 0;
    ELSE
        RETURN 0;
    END IF;
END;
$$ LANGUAGE plpgsql STRICT IMMUTABLE;


CREATE FUNCTION instr(string varchar, string_to_search_for varchar,
                      beg_index integer, occur_index integer)
RETURNS integer AS $$
DECLARE
    pos integer NOT NULL DEFAULT 0;
    occur_number integer NOT NULL DEFAULT 0;
    temp_str varchar;
    beg integer;
    i integer;
    length integer;
    ss_length integer;
BEGIN
    IF occur_index <= 0 THEN
        RAISE 'argument ''%'' is out of range', occur_index
          USING ERRCODE = '22003';
    END IF;

    IF beg_index > 0 THEN
        beg := beg_index - 1;
        FOR i IN 1..occur_index LOOP
            temp_str := substring(string FROM beg + 1);
            pos := position(string_to_search_for IN temp_str);
            IF pos = 0 THEN
                RETURN 0;
            END IF;
            beg := beg + pos;
        END LOOP;

        RETURN beg;
    ELSIF beg_index < 0 THEN
        ss_length := char_length(string_to_search_for);
        length := char_length(string);
        beg := length + 1 + beg_index;

        WHILE beg > 0 LOOP
            temp_str := substring(string FROM beg FOR ss_length);
            IF string_to_search_for = temp_str THEN
                occur_number := occur_number + 1;
                IF occur_number = occur_index THEN
                    RETURN beg;
                END IF;
            END IF;

            beg := beg - 1;
        END LOOP;

        RETURN 0;
    ELSE
        RETURN 0;
    END IF;
END;
$$ LANGUAGE plpgsql STRICT IMMUTABLE;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-porting.html)（原文版本：18.6；核對日期：2026-09-15）
