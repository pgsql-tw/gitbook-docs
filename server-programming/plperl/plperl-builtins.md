<a id="PLPERL-BUILTINS"></a>
## 43.3. 內建函式 [#](#PLPERL-BUILTINS)

[43.3.1. 從 PL/Perl 存取資料庫](plperl-builtins.md#PLPERL-DATABASE)

[43.3.2. PL/Perl 中的公用函式](plperl-builtins.md#PLPERL-UTILITY-FUNCTIONS)

<a id="PLPERL-DATABASE"></a>

### 43.3.1. 從 PL/Perl 存取資料庫 [#](#PLPERL-DATABASE)

要從您的 Perl 函式存取資料庫本身，
可以透過以下函式來完成：

`spi_exec_query(query [, limit])` <a id="id-1.8.10.11.2.3.1.1.2"></a>
:   `spi_exec_query` 會執行一個 SQL 指令，
    並將整個資料列集合以雜湊參照陣列的參照形式傳回。
    若指定了 *`limit`* 且其值大於零，
    則 `spi_exec_query` 最多會取回
    *`limit`* 列，效果就如同查詢中包含了
    `LIMIT` 子句一樣。省略 *`limit`*
    或將其指定為零，則不會有資料列數量的限制。

    *您只應該在知道結果集會相對較小時，才使用這個指令。*
    以下是一個帶有選擇性列數上限的查詢
    （`SELECT` 指令）範例：

    ```

    $rv = spi_exec_query('SELECT * FROM my_table', 5);
    ```

    這會從資料表 `my_table`
    傳回最多 5 列。若 `my_table`
    有一個欄位 `my_column`，您可以像這樣
    取得結果中第 `$i` 列的該欄位值：

    ```

    $foo = $rv->{rows}[$i]->{my_column};
    ```

    可以像這樣取得 `SELECT`
    查詢所傳回的總列數：

    ```

    $nrows = $rv->{processed}
    ```

    以下是使用另一種指令類型的範例：

    ```

    $query = "INSERT INTO my_table VALUES (1, 'test')";
    $rv = spi_exec_query($query);
    ```

    接著您可以像這樣取得指令狀態（例如
    `SPI_OK_INSERT`）：

    ```

    $res = $rv->{status};
    ```

    若要取得受影響的列數，請執行：

    ```

    $nrows = $rv->{processed};
    ```

    以下是一個完整的範例：

    ```

    CREATE TABLE test (
        i int,
        v varchar
    );

    INSERT INTO test (i, v) VALUES (1, 'first line');
    INSERT INTO test (i, v) VALUES (2, 'second line');
    INSERT INTO test (i, v) VALUES (3, 'third line');
    INSERT INTO test (i, v) VALUES (4, 'immortal');

    CREATE OR REPLACE FUNCTION test_munge() RETURNS SETOF test AS $$
        my $rv = spi_exec_query('select i, v from test;');
        my $status = $rv->{status};
        my $nrows = $rv->{processed};
        foreach my $rn (0 .. $nrows - 1) {
            my $row = $rv->{rows}[$rn];
            $row->{i} += 200 if defined($row->{i});
            $row->{v} =~ tr/A-Za-z/a-zA-Z/ if (defined($row->{v}));
            return_next($row);
        }
        return undef;
    $$ LANGUAGE plperl;

    SELECT * FROM test_munge();
    ```

`spi_query(command)` <a id="id-1.8.10.11.2.3.2.1.2"></a> <br> `spi_fetchrow(cursor)` <a id="id-1.8.10.11.2.3.2.2.2"></a> <br> `spi_cursor_close(cursor)` <a id="id-1.8.10.11.2.3.2.3.2"></a>
:   `spi_query` 與 `spi_fetchrow`
    搭配運作，可用於處理可能很大的資料列集合，或用於
    您希望在資料列到達時就逐一傳回的情況。
    `spi_fetchrow` *只能* 與
    `spi_query` 搭配使用。以下範例說明了
    如何一起使用它們：

    ```

    CREATE TYPE foo_type AS (the_num INTEGER, the_text TEXT);

    CREATE OR REPLACE FUNCTION lotsa_md5 (INTEGER) RETURNS SETOF foo_type AS $$
        use Digest::MD5 qw(md5_hex);
        my $file = '/usr/share/dict/words';
        my $t = localtime;
        elog(NOTICE, "opening file $file at $t" );
        open my $fh, '<', $file # ooh, it's a file access!
            or elog(ERROR, "cannot open $file for reading: $!");
        my @words = <$fh>;
        close $fh;
        $t = localtime;
        elog(NOTICE, "closed file $file at $t");
        chomp(@words);
        my $row;
        my $sth = spi_query("SELECT * FROM generate_series(1,$_[0]) AS b(a)");
        while (defined ($row = spi_fetchrow($sth))) {
            return_next({
                the_num => $row->{a},
                the_text => md5_hex($words[rand @words])
            });
        }
        return;
    $$ LANGUAGE plperlu;

    SELECT * from lotsa_md5(500);
    ```

    正常情況下，`spi_fetchrow` 應該反覆呼叫，
    直到它傳回 `undef` 為止，這表示已經
    沒有更多資料列可讀取。`spi_query`
    所傳回的游標，會在
    `spi_fetchrow` 傳回 `undef` 時自動釋放。
    若您不希望讀取所有資料列，可改為呼叫
    `spi_cursor_close` 來釋放游標。
    若未這麼做，將會導致記憶體洩漏。

`spi_prepare(command, argument types)` <a id="id-1.8.10.11.2.3.3.1.2"></a> <br> `spi_query_prepared(plan, arguments)` <a id="id-1.8.10.11.2.3.3.2.2"></a> <br> `spi_exec_prepared(plan [, attributes], arguments)` <a id="id-1.8.10.11.2.3.3.3.2"></a> <br> `spi_freeplan(plan)` <a id="id-1.8.10.11.2.3.3.4.2"></a>
:   `spi_prepare`、`spi_query_prepared`、`spi_exec_prepared`
    與 `spi_freeplan` 實作了相同的功能，但用於預備（prepared）查詢。
    `spi_prepare` 接受一個含有編號引數佔位符（$1、$2 等）的查詢字串，
    以及一份引數型別的字串清單：

    ```

    $plan = spi_prepare('SELECT * FROM test WHERE id > $1 AND name = $2',
                                                         'INTEGER', 'TEXT');
    ```

    一旦透過呼叫 `spi_prepare` 準備好查詢計畫後，
    就可以使用該計畫來取代字串查詢，可以用於
    `spi_exec_prepared`（其結果與 `spi_exec_query`
    傳回的結果相同），也可以用於 `spi_query_prepared`
    （其傳回的游標與 `spi_query` 完全相同，
    可以稍後傳給 `spi_fetchrow`）。
    `spi_exec_prepared` 選用的第二個參數，是一個屬性的雜湊參照；
    目前唯一支援的屬性是 `limit`，
    用於設定查詢傳回的最大列數。
    省略 `limit` 或將其指定為零，則不會有
    列數限制。

    預備查詢的優點在於，可以將一個預備好的計畫用於
    多次查詢執行。當不再需要該計畫時，可以使用
    `spi_freeplan` 將其釋放：

    ```

    CREATE OR REPLACE FUNCTION init() RETURNS VOID AS $$
            $_SHARED{my_plan} = spi_prepare('SELECT (now() + $1)::date AS now',
                                            'INTERVAL');
    $$ LANGUAGE plperl;

    CREATE OR REPLACE FUNCTION add_time( INTERVAL ) RETURNS TEXT AS $$
            return spi_exec_prepared(
                    $_SHARED{my_plan},
                    $_[0]
            )->{rows}->[0]->{now};
    $$ LANGUAGE plperl;

    CREATE OR REPLACE FUNCTION done() RETURNS VOID AS $$
            spi_freeplan( $_SHARED{my_plan});
            undef $_SHARED{my_plan};
    $$ LANGUAGE plperl;

    SELECT init();
    SELECT add_time('1 day'), add_time('2 days'), add_time('3 days');
    SELECT done();

      add_time  |  add_time  |  add_time
    ------------+------------+------------
     2005-12-10 | 2005-12-11 | 2005-12-12
    ```

    請注意，`spi_prepare` 中的參數下標是透過
    $1、$2、$3 等來定義的，因此請避免以雙引號宣告查詢字串，
    否則可能很容易導致難以察覺的錯誤。

    另一個範例說明了 `spi_exec_prepared` 中選用參數的用法：

    ```

    CREATE TABLE hosts AS SELECT id, ('192.168.1.'||id)::inet AS address
                          FROM generate_series(1,3) AS id;

    CREATE OR REPLACE FUNCTION init_hosts_query() RETURNS VOID AS $$
            $_SHARED{plan} = spi_prepare('SELECT * FROM hosts
                                          WHERE address << $1', 'inet');
    $$ LANGUAGE plperl;

    CREATE OR REPLACE FUNCTION query_hosts(inet) RETURNS SETOF hosts AS $$
            return spi_exec_prepared(
                    $_SHARED{plan},
                    {limit => 2},
                    $_[0]
            )->{rows};
    $$ LANGUAGE plperl;

    CREATE OR REPLACE FUNCTION release_hosts_query() RETURNS VOID AS $$
            spi_freeplan($_SHARED{plan});
            undef $_SHARED{plan};
    $$ LANGUAGE plperl;

    SELECT init_hosts_query();
    SELECT query_hosts('192.168.1.0/30');
    SELECT release_hosts_query();

        query_hosts
    -----------------
     (1,192.168.1.1)
     (2,192.168.1.2)
    (2 rows)
    ```

`spi_commit()` <a id="id-1.8.10.11.2.3.4.1.2"></a> <br> `spi_rollback()` <a id="id-1.8.10.11.2.3.4.2.2"></a>
:   提交（commit）或回復（roll back）目前的交易。這只能在
    從最上層呼叫的程序（procedure）或匿名程式碼區塊
    （`DO` 指令）中呼叫。（請注意，
    無法透過 `spi_exec_query` 或類似的方式來執行
    SQL 指令 `COMMIT` 或 `ROLLBACK`。
    必須使用這些函式來完成。）交易結束後，
    會自動啟動一個新的交易，因此不需要另外
    提供相對應的函式。

    以下是一個範例：

    ```

    CREATE PROCEDURE transaction_test1()
    LANGUAGE plperl
    AS $$
    foreach my $i (0..9) {
        spi_exec_query("INSERT INTO test1 (a) VALUES ($i)");
        if ($i % 2 == 0) {
            spi_commit();
        } else {
            spi_rollback();
        }
    }
    $$;

    CALL transaction_test1();
    ```

<a id="PLPERL-UTILITY-FUNCTIONS"></a>

### 43.3.2. PL/Perl 中的公用函式 [#](#PLPERL-UTILITY-FUNCTIONS)

`elog(level, msg)` <a id="id-1.8.10.11.3.2.1.1.2"></a>
:   發出一則記錄或錯誤訊息。可用的層級有
    `DEBUG`、`LOG`、`INFO`、
    `NOTICE`、`WARNING` 與 `ERROR`。
    `ERROR`
    會引發一個錯誤情況；若周圍的
    Perl 程式碼未攔截此錯誤，該錯誤會向外傳播到
    呼叫方的查詢，導致目前的交易或子交易被中止。這
    實質上等同於 Perl 的 `die` 指令。
    其他層級只會產生不同優先順序層級的訊息。
    特定優先順序的訊息是否會回報給用戶端、
    寫入伺服器日誌，或兩者皆是，是由
    [log_min_messages](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) 與
    [client_min_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 這兩個組態
    變數所控制。詳情請參閱[第 19 章](../../server-administration/runtime-config/README.md)。

`quote_literal(string)` <a id="id-1.8.10.11.3.2.2.1.2"></a>
:   傳回經過適當引號處理的字串，可用作 SQL
    陳述式字串中的字串常值。內嵌的單引號與反斜線會被正確地加倍。
    請注意，若輸入為 undef，`quote_literal` 會傳回 undef；若引數
    有可能是 undef，通常使用 `quote_nullable` 較為合適。

`quote_nullable(string)` <a id="id-1.8.10.11.3.2.3.1.2"></a>
:   傳回經過適當引號處理的字串，可用作 SQL
    陳述式字串中的字串常值；若引數為 undef，則傳回未加引號的字串 "NULL"。
    內嵌的單引號與反斜線會被正確地加倍。

`quote_ident(string)` <a id="id-1.8.10.11.3.2.4.1.2"></a>
:   傳回經過適當引號處理的字串，可用作
    SQL 陳述式字串中的識別字。只有在必要時
    （亦即該字串包含非識別字字元，或大小寫會被摺疊）才會加上引號。
    內嵌的引號會被正確地加倍。

`decode_bytea(string)` <a id="id-1.8.10.11.3.2.5.1.2"></a>
:   傳回由給定字串內容所表示的未逸出二進位資料，
    該字串應以 `bytea` 編碼。

`encode_bytea(string)` <a id="id-1.8.10.11.3.2.6.1.2"></a>
:   傳回給定字串所含二進位資料內容的 `bytea` 編碼形式。

`encode_array_literal(array)` <a id="id-1.8.10.11.3.2.7.1.2"></a> <br> `encode_array_literal(array, delimiter)`
:   以陣列常值格式（請參閱[8.15.2 節](../../the-sql-language/datatype/arrays.md#ARRAYS-INPUT)），
    將所參照陣列的內容以字串形式傳回。
    若引數不是陣列的參照，則會原封不動地傳回該引數值。
    陣列常值中各元素之間所使用的分隔符號，若未指定或為 undef，
    預設為 "`,` "。

`encode_typed_literal(value, typename)` <a id="id-1.8.10.11.3.2.8.1.2"></a>
:   將一個 Perl 變數轉換為第二個引數所傳入的資料型別的值，
    並傳回該值的字串表示形式。
    能正確處理巢狀陣列以及複合型別的值。

`encode_array_constructor(array)` <a id="id-1.8.10.11.3.2.9.1.2"></a>
:   以陣列建構子格式（請參閱[4.2.12 節](../../the-sql-language/sql-syntax/sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)），
    將所參照陣列的內容以字串形式傳回。
    各個值會使用 `quote_nullable` 加上引號。
    若引數不是陣列的參照，則會傳回該引數值，並以
    `quote_nullable` 加上引號。

`looks_like_number(string)` <a id="id-1.8.10.11.3.2.10.1.2"></a>
:   若給定字串的內容在 Perl 看來像是一個
    數字，則傳回一個真值，否則傳回假值。
    若引數為 undef，則傳回 undef。開頭與結尾的空白
    會被忽略。`Inf` 與 `Infinity` 會被視為數字。

`is_array_ref(argument)` <a id="id-1.8.10.11.3.2.11.1.2"></a>
:   若給定的引數可被視為陣列參照，
    亦即該引數的 ref 為 `ARRAY` 或
    `PostgreSQL::InServer::ARRAY`，則傳回一個真值。否則傳回假值。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-builtins.html)（原文版本：18.6；核對日期：2026-09-16）
