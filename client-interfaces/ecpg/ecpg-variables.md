<a id="ECPG-VARIABLES"></a>

## 34.4. 使用主機變數 [#](#ecpg-variables) <a href="#ecpg-variables" id="ecpg-variables"></a>

[34.4.1. 概觀](ecpg-variables.md#ecpg-variables-overview)

[34.4.2. 宣告區段](ecpg-variables.md#ecpg-declare-sections)

[34.4.3. 取得查詢結果](ecpg-variables.md#ecpg-retrieving)

[34.4.4. 型別對應](ecpg-variables.md#ecpg-variables-type-mapping)

[34.4.5. 處理非基本 SQL 資料型別](ecpg-variables.md#ecpg-variables-nonprimitive-sql)

[34.4.6. 指示變數](ecpg-variables.md#ecpg-indicators)

在[第 34.3 節](ecpg-commands.md)中，你已經看到如何從嵌入式 SQL 程式執行 SQL 陳述式。其中有些陳述式只使用固定的值，無法把使用者提供的值放進陳述式，也無法讓程式處理查詢傳回的值。這類陳述式在實際的應用程式中並不實用。本節將詳細說明如何透過一種稱為*主機變數*的簡單機制，在 C 程式與嵌入式 SQL 陳述式之間傳遞資料。在嵌入式 SQL 程式中，我們把 SQL 陳述式視為 C 程式碼中的*客人*，而 C 程式碼則是*主機語言*。因此，C 程式的變數稱為*主機變數*。

在 PostgreSQL 後端與 ECPG 應用程式之間交換值的另一種方式是使用 SQL 描述區，詳見[第 34.7 節](ecpg-descriptors.md)。

<a id="ECPG-VARIABLES-OVERVIEW"></a>

### 34.4.1. 概觀 [#](#ecpg-variables-overview) <a href="#ecpg-variables-overview" id="ecpg-variables-overview"></a>

在嵌入式 SQL 中，於 C 程式與 SQL 陳述式之間傳遞資料特別簡單。你不必讓程式把資料貼進陳述式（這會帶來各種麻煩，例如必須正確地為值加上引號），只要把 C 變數的名稱加上冒號前綴寫進 SQL 陳述式即可。例如：

```

EXEC SQL INSERT INTO sometable VALUES (:v1, 'foo', :v2);
```

這個陳述式參照了兩個名為 `v1` 與 `v2` 的 C 變數，同時也使用了一般的 SQL 字串常數，以說明你並不受限於只能使用其中一種資料。

這種在 SQL 陳述式中插入 C 變數的寫法，在 SQL 陳述式中任何預期出現值表示式的地方都可以使用。

<a id="ECPG-DECLARE-SECTIONS"></a>

### 34.4.2. 宣告區段 [#](#ecpg-declare-sections) <a href="#ecpg-declare-sections" id="ecpg-declare-sections"></a>

若要把資料從程式傳給資料庫（例如作為查詢的參數），或把資料從資料庫傳回程式，用來存放這些資料的 C 變數必須宣告在特別標示的區段中，讓嵌入式 SQL 前置處理器得以知道它們。

這個區段以下列敘述開始：

```

EXEC SQL BEGIN DECLARE SECTION;
```

並以下列敘述結束：

```

EXEC SQL END DECLARE SECTION;
```

在這兩行之間必須是一般的 C 變數宣告，例如：

```

int   x = 4;
char  foo[16], bar[16];
```

如你所見，你可以選擇為變數指定初始值。變數的作用範圍取決於其宣告區段在程式中的位置。你也可以使用下列語法宣告變數，這會隱含地建立一個宣告區段：

```

EXEC SQL int i = 4;
```

一個程式中可以有任意多個宣告區段。

這些宣告也會以一般 C 變數的形式輸出到輸出檔案中，因此不需要再宣告一次。不打算在 SQL 命令中使用的變數，可以在這些特殊區段之外以一般方式宣告。

結構（struct）或聯合（union）的定義也必須列在 `DECLARE` 區段之內。否則前置處理器無法處理這些型別，因為它不知道其定義。

<a id="ECPG-RETRIEVING"></a>

### 34.4.3. 取得查詢結果 [#](#ecpg-retrieving) <a href="#ecpg-retrieving" id="ecpg-retrieving"></a>

現在你應該已經能把程式產生的資料傳入 SQL 命令了。但要如何取得查詢的結果呢？為此，嵌入式 SQL 提供了常用命令 `SELECT` 與 `FETCH` 的特殊變體。這些命令有一個特殊的 `INTO` 子句，用來指定取得的值要存放到哪些主機變數中。`SELECT` 用於只傳回單一資料列的查詢，而 `FETCH` 則搭配游標，用於傳回多筆資料列的查詢。

以下是一個範例：

```

/*
 * assume this table:
 * CREATE TABLE test1 (a int, b varchar(50));
 */

EXEC SQL BEGIN DECLARE SECTION;
int v1;
VARCHAR v2;
EXEC SQL END DECLARE SECTION;

 ...

EXEC SQL SELECT a, b INTO :v1, :v2 FROM test;
```

譯註：原文範例註解假設的資料表名稱為 test1，但 SELECT 陳述式查詢的是 test；範例程式碼依原文保留，實際使用時兩者應一致。

所以 `INTO` 子句出現在選取清單與 `FROM` 子句之間。選取清單中的元素數目必須與 `INTO` 之後的清單（也稱為目標清單）的元素數目相等。

以下是使用 `FETCH` 命令的範例：

```

EXEC SQL BEGIN DECLARE SECTION;
int v1;
VARCHAR v2;
EXEC SQL END DECLARE SECTION;

 ...

EXEC SQL DECLARE foo CURSOR FOR SELECT a, b FROM test;

 ...

do
{
    ...
    EXEC SQL FETCH NEXT FROM foo INTO :v1, :v2;
    ...
} while (...);
```

這裡的 `INTO` 子句出現在所有一般子句之後。

<a id="ECPG-VARIABLES-TYPE-MAPPING"></a>

### 34.4.4. 型別對應 [#](#ecpg-variables-type-mapping) <a href="#ecpg-variables-type-mapping" id="ecpg-variables-type-mapping"></a>

當 ECPG 應用程式在 PostgreSQL 伺服器與 C 應用程式之間交換值時，例如從伺服器取得查詢結果，或執行帶有輸入參數的 SQL 陳述式時，這些值需要在 PostgreSQL 資料型別與主機語言變數型別（具體而言就是 C 語言資料型別）之間轉換。ECPG 的重點之一，就是在大多數情況下會自動處理這件事。

就這方面而言，資料型別分為兩類：一些簡單的 PostgreSQL 資料型別，例如 `integer` 與 `text`，應用程式可以直接讀寫。其他 PostgreSQL 資料型別，例如 `timestamp` 與 `numeric`，則只能透過特殊的函式庫函式存取；請參閱[第 34.4.4.2 節](ecpg-variables.md#ecpg-special-types)。

[表 34.1](ecpg-variables.md#ECPG-DATATYPE-HOSTVARS-TABLE) 列出哪些 PostgreSQL 資料型別對應到哪些 C 資料型別。當你想要傳送或接收某個 PostgreSQL 資料型別的值時，應該在宣告區段中宣告對應 C 資料型別的 C 變數。

<a id="ECPG-DATATYPE-HOSTVARS-TABLE"></a>

**表 34.1. PostgreSQL 資料型別與 C 變數型別之間的對應**

<table border="1" class="table" summary="PostgreSQL 資料型別與 C 變數型別之間的對應"><colgroup><col/><col/></colgroup><thead><tr><th>PostgreSQL 資料型別</th><th>主機變數型別</th></tr></thead><tbody><tr><td><code class="type">smallint</code></td><td><code class="type">short</code></td></tr><tr><td><code class="type">integer</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">bigint</code></td><td><code class="type">long long int</code></td></tr><tr><td><code class="type">decimal</code></td><td><code class="type">decimal</code><a class="footnote" href="#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnote" id="ECPG-DATATYPE-TABLE-FN">[a]</sup></a></td></tr><tr><td><code class="type">numeric</code></td><td><code class="type">numeric</code><a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">real</code></td><td><code class="type">float</code></td></tr><tr><td><code class="type">double precision</code></td><td><code class="type">double</code></td></tr><tr><td><code class="type">smallserial</code></td><td><code class="type">short</code></td></tr><tr><td><code class="type">serial</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">bigserial</code></td><td><code class="type">long long int</code></td></tr><tr><td><code class="type">oid</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">character(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">varchar(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">text</code></td><td><code class="type">char[<em class="replaceable"><code>n</code></em>+1]</code>, <code class="type">VARCHAR[<em class="replaceable"><code>n</code></em>+1]</code></td></tr><tr><td><code class="type">name</code></td><td><code class="type">char[NAMEDATALEN]</code></td></tr><tr><td><code class="type">timestamp</code></td><td><code class="type">timestamp</code><a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">interval</code></td><td><code class="type">interval</code><a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">date</code></td><td><code class="type">date</code><a class="footnoteref" href="ecpg-variables.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">boolean</code></td><td><code class="type">bool</code><a class="footnote" href="#ftn.id-1.7.5.10.7.5.2.2.17.2.2"><sup class="footnote" id="id-1.7.5.10.7.5.2.2.17.2.2">[b]</sup></a></td></tr><tr><td><code class="type">bytea</code></td><td><code class="type">char *</code>, <code class="type">bytea[<em class="replaceable"><code>n</code></em>]</code></td></tr></tbody><tbody class="footnotes"><tr><td colspan="2"><div class="footnote" id="ftn.ECPG-DATATYPE-TABLE-FN"><p><a class="para" href="#ECPG-DATATYPE-TABLE-FN"><sup class="para">[a] </sup></a>此型別只能透過特殊的函式庫函式存取；請參閱<a class="xref" href="ecpg-variables.md#ECPG-SPECIAL-TYPES">第 34.4.4.2 節</a>。</p></div><div class="footnote" id="ftn.id-1.7.5.10.7.5.2.2.17.2.2"><p><a class="para" href="#id-1.7.5.10.7.5.2.2.17.2.2"><sup class="para">[b] </sup></a>若非原生型別，則宣告於 <code class="filename">ecpglib.h</code></p></div></td></tr></tbody></table>

<br>

<a id="ECPG-CHAR"></a>

#### 34.4.4.1. 處理字元字串 [#](#ecpg-char) <a href="#ecpg-char" id="ecpg-char"></a>

若要處理 SQL 字元字串資料型別，例如 `varchar` 與 `text`，宣告主機變數有兩種可行的方式。

一種是使用 `char[]`，也就是 `char` 的陣列，這是 C 語言中處理字元資料最常見的方式。

```

EXEC SQL BEGIN DECLARE SECTION;
    char str[50];
EXEC SQL END DECLARE SECTION;
```

請注意，你必須自行處理長度。如果你把這個主機變數用作某個查詢的目標變數，而該查詢傳回超過 49 個字元的字串，就會發生緩衝區溢位。

另一種方式是使用 `VARCHAR` 型別，這是 ECPG 提供的特殊型別。`VARCHAR` 型別陣列的定義，會針對每個變數轉換成一個具名的 `struct`。像這樣的宣告：

```

VARCHAR var[180];
```

會被轉換成：

```

struct varchar_var { int len; char arr[180]; } var;
```

成員 `arr` 存放字串，包含結尾的零位元組。因此，若要在 `VARCHAR` 主機變數中存放字串，宣告該主機變數時，長度必須把零位元組結尾符號也算進去。成員 `len` 存放 `arr` 中所儲存字串的長度，不含結尾的零位元組。當主機變數用作查詢的輸入時，若 `strlen(arr)` 與 `len` 不同，會使用較短的那一個。

`VARCHAR` 可以全部大寫或全部小寫，但不能大小寫混用。

`char` 與 `VARCHAR` 主機變數也可以存放其他 SQL 型別的值，這些值會以字串形式儲存。

<a id="ECPG-SPECIAL-TYPES"></a>

#### 34.4.4.2. 存取特殊資料型別 [#](#ecpg-special-types) <a href="#ecpg-special-types" id="ecpg-special-types"></a>

ECPG 包含一些特殊型別，可以幫助你輕鬆地與 PostgreSQL 伺服器的某些特殊資料型別互動。具體而言，它已實作對 `numeric`、`decimal`、`date`、`timestamp` 與 `interval` 型別的支援。這些資料型別因為內部結構複雜，無法有效地對應到基本的主機變數型別（例如 `int`、`long long int` 或 `char[]`）。應用程式處理這些型別的方式，是以特殊型別宣告主機變數，並使用 pgtypes 函式庫中的函式來存取它們。pgtypes 函式庫（詳見[第 34.6 節](ecpg-pgtypes.md)）包含處理這些型別的基本函式，例如，你不必只為了把一段時間間隔加到時間戳記上，就向 SQL 伺服器傳送查詢。

以下各小節說明這些特殊資料型別。關於 pgtypes 函式庫函式的更多細節，請參閱[第 34.6 節](ecpg-pgtypes.md)。

<a id="ECPG-SPECIAL-TYPES-TIMESTAMP-DATE"></a>

##### 34.4.4.2.1. timestamp、date [#](#ecpg-special-types-timestamp-date) <a href="#ecpg-special-types-timestamp-date" id="ecpg-special-types-timestamp-date"></a>

以下是在 ECPG 主機應用程式中處理 `timestamp` 變數的模式。

首先，程式必須引入 `timestamp` 型別的標頭檔：

```

#include <pgtypes_timestamp.h>
```

接著，在宣告區段中把主機變數宣告為 `timestamp` 型別：

```

EXEC SQL BEGIN DECLARE SECTION;
timestamp ts;
EXEC SQL END DECLARE SECTION;
```

把值讀入主機變數之後，再使用 pgtypes 函式庫函式處理它。在下列範例中，`timestamp` 值會以 `PGTYPEStimestamp_to_asc()` 函式轉換成文字（ASCII）形式：

```

EXEC SQL SELECT now()::timestamp INTO :ts;

printf("ts = %s\n", PGTYPEStimestamp_to_asc(ts));
```

這個範例會顯示類似下面的結果：

```

ts = 2010-06-27 18:03:56.949343
```

此外，DATE 型別也可以用相同方式處理。程式必須引入 `pgtypes_date.h`，把主機變數宣告為 date 型別，並使用 `PGTYPESdate_to_asc()` 函式把 DATE 值轉換成文字形式。關於 pgtypes 函式庫函式的更多細節，請參閱[第 34.6 節](ecpg-pgtypes.md)。

<a id="ECPG-TYPE-INTERVAL"></a>

##### 34.4.4.2.2. interval [#](#ecpg-type-interval) <a href="#ecpg-type-interval" id="ecpg-type-interval"></a>

`interval` 型別的處理方式也與 `timestamp` 和 `date` 型別類似。不過，必須明確地為 `interval` 型別的值配置記憶體。換句話說，變數的記憶體空間必須配置在堆積記憶體中，而不是堆疊記憶體中。

以下是一個範例程式：

```

#include <stdio.h>
#include <stdlib.h>
#include <pgtypes_interval.h>

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    interval *in;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    in = PGTYPESinterval_new();
    EXEC SQL SELECT '1 min'::interval INTO :in;
    printf("interval = %s\n", PGTYPESinterval_to_asc(in));
    PGTYPESinterval_free(in);

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

<a id="ECPG-TYPE-NUMERIC-DECIMAL"></a>

##### 34.4.4.2.3. numeric、decimal [#](#ecpg-type-numeric-decimal) <a href="#ecpg-type-numeric-decimal" id="ecpg-type-numeric-decimal"></a>

`numeric` 與 `decimal` 型別的處理方式與 `interval` 型別類似：需要定義指標、在堆積上配置記憶體空間，並使用 pgtypes 函式庫函式存取該變數。關於 pgtypes 函式庫函式的更多細節，請參閱[第 34.6 節](ecpg-pgtypes.md)。

並沒有專門為 `decimal` 型別提供的函式。應用程式必須使用 pgtypes 函式庫函式把它轉換成 `numeric` 變數，才能做進一步處理。

以下是一個處理 `numeric` 與 `decimal` 型別變數的範例程式。

```

#include <stdio.h>
#include <stdlib.h>
#include <pgtypes_numeric.h>

EXEC SQL WHENEVER SQLERROR STOP;

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    numeric *num;
    numeric *num2;
    decimal *dec;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    num = PGTYPESnumeric_new();
    dec = PGTYPESdecimal_new();

    EXEC SQL SELECT 12.345::numeric(4,2), 23.456::decimal(4,2) INTO :num, :dec;

    printf("numeric = %s\n", PGTYPESnumeric_to_asc(num, 0));
    printf("numeric = %s\n", PGTYPESnumeric_to_asc(num, 1));
    printf("numeric = %s\n", PGTYPESnumeric_to_asc(num, 2));

    /* Convert decimal to numeric to show a decimal value. */
    num2 = PGTYPESnumeric_new();
    PGTYPESnumeric_from_decimal(dec, num2);

    printf("decimal = %s\n", PGTYPESnumeric_to_asc(num2, 0));
    printf("decimal = %s\n", PGTYPESnumeric_to_asc(num2, 1));
    printf("decimal = %s\n", PGTYPESnumeric_to_asc(num2, 2));

    PGTYPESnumeric_free(num2);
    PGTYPESdecimal_free(dec);
    PGTYPESnumeric_free(num);

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

<a id="ECPG-SPECIAL-TYPES-BYTEA"></a>

##### 34.4.4.2.4. bytea [#](#ecpg-special-types-bytea) <a href="#ecpg-special-types-bytea" id="ecpg-special-types-bytea"></a>

`bytea` 型別的處理方式與 `VARCHAR` 類似。`bytea` 型別陣列的定義，會針對每個變數轉換成一個具名的結構。像這樣的宣告：

```

bytea var[180];
```

會被轉換成：

```

struct bytea_var { int len; char arr[180]; } var;
```

成員 `arr` 存放二進位格式的資料。與 `VARCHAR` 不同，它也能把 `'\0'` 當作資料的一部分處理。資料由 ecpglib 轉換為十六進位格式或從十六進位格式轉換回來，並進行傳送與接收。

### 注意

只有在 [bytea_output](../../server-administration/runtime-config/runtime-config-client.md#GUC-BYTEA-OUTPUT) 設定為 `hex` 時，才能使用 `bytea` 變數。

<a id="ECPG-VARIABLES-NONPRIMITIVE-C"></a>

#### 34.4.4.3. 非基本型別的主機變數 [#](#ecpg-variables-nonprimitive-c) <a href="#ecpg-variables-nonprimitive-c" id="ecpg-variables-nonprimitive-c"></a>

你也可以使用陣列、typedef、結構與指標作為主機變數。

<a id="ECPG-VARIABLES-ARRAYS"></a>

##### 34.4.4.3.1. 陣列 <a href="#ecpg-variables-arrays" id="ecpg-variables-arrays">#</a>

陣列作為主機變數有兩種使用情境。第一種是把文字字串存放在 `char[]` 或 `VARCHAR[]` 中，如[第 34.4.4.1 節](ecpg-variables.md#ecpg-char)所述。第二種使用情境是不使用游標，就從查詢結果中取得多筆資料列。如果不使用陣列，要處理由多筆資料列組成的查詢結果，就必須使用游標與 `FETCH` 命令。但使用陣列主機變數時，可以一次接收多筆資料列。陣列的長度必須定義得足以容納所有資料列，否則很可能會發生緩衝區溢位。

下列範例會掃描 `pg_database` 系統資料表，並顯示所有可用資料庫的 OID 與名稱：

```

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    int dbid[8];
    char dbname[8][16];
    int i;
EXEC SQL END DECLARE SECTION;

    memset(dbname, 0, sizeof(char)* 16 * 8);
    memset(dbid, 0, sizeof(int) * 8);

    EXEC SQL CONNECT TO testdb;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    /* Retrieve multiple rows into arrays at once. */
    EXEC SQL SELECT oid,datname INTO :dbid, :dbname FROM pg_database;

    for (i = 0; i < 8; i++)
        printf("oid=%d, dbname=%s\n", dbid[i], dbname[i]);

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

這個範例會顯示下列結果。（確切的值取決於本機環境。）

```

oid=1, dbname=template1
oid=11510, dbname=template0
oid=11511, dbname=postgres
oid=313780, dbname=testdb
oid=0, dbname=
oid=0, dbname=
oid=0, dbname=
```

譯註：範例程式的迴圈會印出 8 行（i 從 0 到 7），但原文的輸出範例只列出 7 行；輸出範例依原文保留。

<a id="ECPG-VARIABLES-STRUCT"></a>

##### 34.4.4.3.2. 結構 [#](#ecpg-variables-struct) <a href="#ecpg-variables-struct" id="ecpg-variables-struct"></a>

成員名稱與查詢結果欄位名稱相符的結構，可以用來一次取得多個欄位。結構讓你能在單一主機變數中處理多個欄位的值。

下列範例從 `pg_database` 系統資料表並使用 `pg_database_size()` 函式，取得可用資料庫的 OID、名稱與大小。在此範例中，使用了結構型別 `dbinfo_t` 的結構變數 dbval（原文此處寫作「結構變數 dbinfo_t」，但 dbinfo_t 是以 typedef 定義的型別名稱，實際的結構變數是 dbval）（其成員名稱與 `SELECT` 結果的各欄位相符）來取得一筆結果資料列，而不必在 `FETCH` 陳述式中放入多個主機變數。

```

EXEC SQL BEGIN DECLARE SECTION;
    typedef struct
    {
       int oid;
       char datname[65];
       long long int size;
    } dbinfo_t;

    dbinfo_t dbval;
EXEC SQL END DECLARE SECTION;

    memset(&dbval, 0, sizeof(dbinfo_t));

    EXEC SQL DECLARE cur1 CURSOR FOR SELECT oid, datname, pg_database_size(oid) AS size FROM pg_database;
    EXEC SQL OPEN cur1;

    /* when end of result set reached, break out of while loop */
    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        /* Fetch multiple columns into one structure. */
        EXEC SQL FETCH FROM cur1 INTO :dbval;

        /* Print members of the structure. */
        printf("oid=%d, datname=%s, size=%lld\n", dbval.oid, dbval.datname, dbval.size);
    }

    EXEC SQL CLOSE cur1;
```

這個範例會顯示下列結果。（確切的值取決於本機環境。）

```

oid=1, datname=template1, size=4324580
oid=11510, datname=template0, size=4243460
oid=11511, datname=postgres, size=4324580
oid=313780, datname=testdb, size=8183012
```

結構主機變數會「吸收」與結構欄位數目相同的欄位。其他的欄位可以指派給其他主機變數。例如，上面的程式也可以改寫成下面這樣，把 `size` 變數放在結構之外：

```

EXEC SQL BEGIN DECLARE SECTION;
    typedef struct
    {
       int oid;
       char datname[65];
    } dbinfo_t;

    dbinfo_t dbval;
    long long int size;
EXEC SQL END DECLARE SECTION;

    memset(&dbval, 0, sizeof(dbinfo_t));

    EXEC SQL DECLARE cur1 CURSOR FOR SELECT oid, datname, pg_database_size(oid) AS size FROM pg_database;
    EXEC SQL OPEN cur1;

    /* when end of result set reached, break out of while loop */
    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        /* Fetch multiple columns into one structure. */
        EXEC SQL FETCH FROM cur1 INTO :dbval, :size;

        /* Print members of the structure. */
        printf("oid=%d, datname=%s, size=%lld\n", dbval.oid, dbval.datname, size);
    }

    EXEC SQL CLOSE cur1;
```

<a id="ECPG-VARIABLES-NONPRIMITIVE-C-TYPEDEFS"></a>

##### 34.4.4.3.3. 型別定義（typedef） [#](#ecpg-variables-nonprimitive-c-typedefs) <a href="#ecpg-variables-nonprimitive-c-typedefs" id="ecpg-variables-nonprimitive-c-typedefs"></a>

<a id="id-1.7.5.10.7.8.5.2"></a>

使用 `typedef` 關鍵字把新型別對應到既有的型別。

```

EXEC SQL BEGIN DECLARE SECTION;
    typedef char mychartype[40];
    typedef long serial_t;
EXEC SQL END DECLARE SECTION;
```

請注意，你也可以使用：

```

EXEC SQL TYPE serial_t IS long;
```

這個宣告不需要放在宣告區段中；也就是說，你也可以把 typedef 寫成一般的 C 陳述式。

你宣告為 `typedef` 的任何字詞，之後在同一程式的 `EXEC SQL` 命令中都不能當作 SQL 關鍵字使用。例如，下面的寫法無法運作：

```

EXEC SQL BEGIN DECLARE SECTION;
    typedef int start;
EXEC SQL END DECLARE SECTION;
...
EXEC SQL START TRANSACTION;
```

ECPG 會對 `START
TRANSACTION` 回報語法錯誤，因為它不再把 `START` 視為 SQL 關鍵字，而只視為 typedef。（如果遇到這種衝突，而重新命名該 typedef 又不太實際，你可以改用[動態 SQL](ecpg-dynamic.md) 撰寫該 SQL 命令。）

### 注意

在 v16 之前的 PostgreSQL 版本中，把 SQL 關鍵字用作 typedef 名稱，很可能會在使用該 typedef 本身時產生語法錯誤，而不是在把該名稱當作 SQL 關鍵字使用時才產生。新的行為在既有的 ECPG 應用程式於新增了關鍵字的新版 PostgreSQL 中重新編譯時，比較不容易造成問題。

<a id="ECPG-VARIABLES-NONPRIMITIVE-C-POINTERS"></a>

##### 34.4.4.3.4. 指標 [#](#ecpg-variables-nonprimitive-c-pointers) <a href="#ecpg-variables-nonprimitive-c-pointers" id="ecpg-variables-nonprimitive-c-pointers"></a>

你可以宣告指向最常見型別的指標。不過請注意，若沒有自動配置，就不能把指標用作查詢的目標變數。關於自動配置的更多資訊，請參閱[第 34.7 節](ecpg-descriptors.md)。

```

EXEC SQL BEGIN DECLARE SECTION;
    int   *intp;
    char **charp;
EXEC SQL END DECLARE SECTION;
```

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL"></a>

### 34.4.5. 處理非基本 SQL 資料型別 [#](#ecpg-variables-nonprimitive-sql) <a href="#ecpg-variables-nonprimitive-sql" id="ecpg-variables-nonprimitive-sql"></a>

本節說明如何在 ECPG 應用程式中處理非純量與使用者自訂的 SQL 層級資料型別。請注意，這與上一節所述的非基本型別主機變數的處理方式不同。

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL-ARRAYS"></a>

#### 34.4.5.1. 陣列 [#](#ecpg-variables-nonprimitive-sql-arrays) <a href="#ecpg-variables-nonprimitive-sql-arrays" id="ecpg-variables-nonprimitive-sql-arrays"></a>

ECPG 並不直接支援多維的 SQL 層級陣列。一維的 SQL 層級陣列可以對應到 C 陣列主機變數，反之亦然。不過，在建立陳述式時，ecpg 並不知道欄位的型別，因此無法檢查 C 陣列是否輸入到對應的 SQL 層級陣列中。在處理 SQL 陳述式的輸出時，ecpg 擁有必要的資訊，因此會檢查兩者是否都是陣列。

如果查詢分別存取陣列的各個*元素*，就可以避免在 ECPG 中使用陣列。此時應該使用型別可以對應到元素型別的主機變數。例如，若欄位型別是 `integer` 陣列，可以使用 `int` 型別的主機變數。另外，若元素型別是 `varchar` 或 `text`，可以使用 `char[]` 或 `VARCHAR[]` 型別的主機變數。

以下是一個範例。假設有下列資料表：

```

CREATE TABLE t3 (
    ii integer[]
);

testdb=> SELECT * FROM t3;
     ii
-------------
 {1,2,3,4,5}
(1 row)
```

下列範例程式取得陣列的第 4 個元素，並把它存放到 `int` 型別的主機變數中：

```

EXEC SQL BEGIN DECLARE SECTION;
int ii;
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii[4] FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH FROM cur1 INTO :ii ;
    printf("ii=%d\n", ii);
}

EXEC SQL CLOSE cur1;
```

這個範例會顯示下列結果：

```

ii=4
```

若要把多個陣列元素對應到陣列型別主機變數中的多個元素，陣列欄位的每個元素與主機變數陣列的每個元素都必須分別處理，例如：

```

EXEC SQL BEGIN DECLARE SECTION;
int ii_a[8];
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii[1], ii[2], ii[3], ii[4] FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH FROM cur1 INTO :ii_a[0], :ii_a[1], :ii_a[2], :ii_a[3];
    ...
}
```

再次提醒，

```

EXEC SQL BEGIN DECLARE SECTION;
int ii_a[8];
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* WRONG */
    EXEC SQL FETCH FROM cur1 INTO :ii_a;
    ...
}
```

在這種情況下無法正確運作，因為你不能把陣列型別的欄位直接對應到陣列主機變數。

另一種變通方法是把陣列以其外部字串表示形式存放在 `char[]` 或 `VARCHAR[]` 型別的主機變數中。關於這種表示形式的更多細節，請參閱[第 8.15.2 節](../../the-sql-language/datatype/arrays.md#ARRAYS-INPUT)。請注意，這表示在主機程式中無法自然地把該陣列當作陣列來存取（除非再做剖析文字表示形式的進一步處理）。

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL-COMPOSITE"></a>

#### 34.4.5.2. 複合型別 [#](#ecpg-variables-nonprimitive-sql-composite) <a href="#ecpg-variables-nonprimitive-sql-composite" id="ecpg-variables-nonprimitive-sql-composite"></a>

ECPG 並不直接支援複合型別，但可以採用簡單的變通方法。可用的變通方法與上面針對陣列所述的方法類似：分別存取每個屬性，或使用外部字串表示形式。

在下列範例中，假設有下列型別與資料表：

```

CREATE TYPE comp_t AS (intval integer, textval varchar(32));
CREATE TABLE t4 (compval comp_t);
INSERT INTO t4 VALUES ( (256, 'PostgreSQL') );
```

最直接的解法是分別存取每個屬性。下列程式分別選取 `comp_t` 型別的每個屬性，從範例資料表取得資料：

```

EXEC SQL BEGIN DECLARE SECTION;
int intval;
varchar textval[33];
EXEC SQL END DECLARE SECTION;

/* Put each element of the composite type column in the SELECT list. */
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).intval, (compval).textval FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Fetch each element of the composite type column into host variables. */
    EXEC SQL FETCH FROM cur1 INTO :intval, :textval;

    printf("intval=%d, textval=%s\n", intval, textval.arr);
}

EXEC SQL CLOSE cur1;
```

為了改進這個範例，可以把用來存放 `FETCH` 命令中值的主機變數集中到一個結構中。關於結構形式主機變數的更多細節，請參閱[第 34.4.4.3.2 節](ecpg-variables.md#ecpg-variables-struct)。若要改用結構，可以把範例修改如下。兩個主機變數 `intval` 與 `textval` 成為 `comp_t` 結構的成員，並在 `FETCH` 命令中指定該結構。

```

EXEC SQL BEGIN DECLARE SECTION;
typedef struct
{
    int intval;
    varchar textval[33];
} comp_t;

comp_t compval;
EXEC SQL END DECLARE SECTION;

/* Put each element of the composite type column in the SELECT list. */
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).intval, (compval).textval FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Put all values in the SELECT list into one structure. */
    EXEC SQL FETCH FROM cur1 INTO :compval;

    printf("intval=%d, textval=%s\n", compval.intval, compval.textval.arr);
}

EXEC SQL CLOSE cur1;
```

雖然 `FETCH` 命令中使用了結構，但 `SELECT` 子句中的屬性名稱仍是逐一指定的。這可以改用 `*` 來要求取得複合型別值的所有屬性，加以改進。

```

...
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).* FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Put all values in the SELECT list into one structure. */
    EXEC SQL FETCH FROM cur1 INTO :compval;

    printf("intval=%d, textval=%s\n", compval.intval, compval.textval.arr);
}
...
```

如此一來，即使 ECPG 本身並不理解複合型別，複合型別也幾乎可以無縫地對應到結構。

最後，也可以把複合型別的值以其外部字串表示形式存放在 `char[]` 或 `VARCHAR[]` 型別的主機變數中。但用這種方式，從主機程式存取該值的各個欄位就不太容易。

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL-USER-DEFINED-BASE-TYPES"></a>

#### 34.4.5.3. 使用者自訂基本型別 [#](#ecpg-variables-nonprimitive-sql-user-defined-base-types) <a href="#ecpg-variables-nonprimitive-sql-user-defined-base-types" id="ecpg-variables-nonprimitive-sql-user-defined-base-types"></a>

ECPG 並不直接支援新的使用者自訂基本型別。你可以使用外部字串表示形式與 `char[]` 或 `VARCHAR[]` 型別的主機變數，而這個解法對許多型別而言確實恰當且足夠。

以下範例使用[第 36.13 節](../../server-programming/extend/xtypes.md)範例中的 `complex` 資料型別。該型別的外部字串表示形式是 `(%f,%f)`，定義於[第 36.13 節](../../server-programming/extend/xtypes.md)中的函式 `complex_in()` 與 `complex_out()`。下列範例把 complex 型別的值 `(1,1)` 與 `(3,3)` 插入欄位 `a` 與 `b`，之後再從資料表中把它們選取出來。

```

EXEC SQL BEGIN DECLARE SECTION;
    varchar a[64];
    varchar b[64];
EXEC SQL END DECLARE SECTION;

    EXEC SQL INSERT INTO test_complex VALUES ('(1,1)', '(3,3)');

    EXEC SQL DECLARE cur1 CURSOR FOR SELECT a, b FROM test_complex;
    EXEC SQL OPEN cur1;

    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        EXEC SQL FETCH FROM cur1 INTO :a, :b;
        printf("a=%s, b=%s\n", a.arr, b.arr);
    }

    EXEC SQL CLOSE cur1;
```

這個範例會顯示下列結果：

```

a=(1,1), b=(3,3)
```

另一種變通方法是避免在 ECPG 中直接使用使用者自訂型別，改為建立一個函式或型別轉換，在使用者自訂型別與 ECPG 能處理的基本型別之間進行轉換。不過請注意，型別轉換（尤其是隱含轉換）應該非常謹慎地引入型別系統。

例如：

```

CREATE FUNCTION create_complex(r double, i double) RETURNS complex
LANGUAGE SQL
IMMUTABLE
AS $$ SELECT $1 * complex '(1,0')' + $2 * complex '(0,1)' $$;
```

譯註：原文此範例有兩處問題，範例程式碼依原文保留：一是字串常數 '(1,0')' 引號位置有誤，正確應為 '(1,0)'；二是 create_complex 的參數型別寫作 double，但 PostgreSQL 內建的 SQL 型別名稱是 double precision（SQL 中沒有單獨的 double 型別），正確寫法為 create_complex(r double precision, i double precision)。

在這個定義之後，下列程式

```

EXEC SQL BEGIN DECLARE SECTION;
double a, b, c, d;
EXEC SQL END DECLARE SECTION;

a = 1;
b = 2;
c = 3;
d = 4;

EXEC SQL INSERT INTO test_complex VALUES (create_complex(:a, :b), create_complex(:c, :d));
```

的效果等同於

```

EXEC SQL INSERT INTO test_complex VALUES ('(1,2)', '(3,4)');
```

<a id="ECPG-INDICATORS"></a>

### 34.4.6. 指示變數 [#](#ecpg-indicators) <a href="#ecpg-indicators" id="ecpg-indicators"></a>

上面的範例都沒有處理空值。事實上，如果取得資料的範例從資料庫取得空值，就會引發錯誤。為了能把空值傳給資料庫，或從資料庫取得空值，你需要為每個存放資料的主機變數再附加第二個主機變數規格。這第二個主機變數稱為*指示變數*（indicator），其中包含一個旗標，指出該資料是否為空值；若為空值，實際主機變數的值會被忽略。以下是一個正確處理取得空值的範例：

```

EXEC SQL BEGIN DECLARE SECTION;
VARCHAR val;
int val_ind;
EXEC SQL END DECLARE SECTION:

 ...

EXEC SQL SELECT b INTO :val :val_ind FROM test1;
```

譯註：原文此範例中 END DECLARE SECTION 之後的冒號應為分號；範例程式碼依原文保留。

若值不是空值，指示變數 `val_ind` 會是零；若值是空值，則會是負數。（若要啟用 Oracle 特有的行為，請參閱[第 34.16 節](ecpg-oracle-compat.md)。）

指示變數還有另一項功能：若指示變數的值為正數，表示該值不是空值，但在存入主機變數時被截斷了。

如果把引數 `-r no_indicator` 傳給前置處理器 `ecpg`，它會以「無指示變數」模式運作。在無指示變數模式下，若未指定指示變數，空值會（在輸入與輸出時）以下列方式表示：字元字串型別以空字串表示，整數型別則以該型別可能的最小值表示（例如 `int` 的 `INT_MIN`）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-variables.html)（原文版本：18.6；核對日期：2026-10-18）
