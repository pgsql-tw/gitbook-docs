<a id="ECPG-VARIABLES-NONPRIMITIVE-C"></a>

## 34.4.4.3. 非基本型別的主機變數 [#](#ecpg-variables-nonprimitive-c) <a href="#ecpg-variables-nonprimitive-c" id="ecpg-variables-nonprimitive-c"></a>

你也可以使用陣列、typedef、結構與指標作為主機變數。

<a id="ECPG-VARIABLES-ARRAYS"></a>

### 34.4.4.3.1. 陣列 [#](#ecpg-variables-arrays) <a href="#ecpg-variables-arrays" id="ecpg-variables-arrays"></a>

陣列作為主機變數有兩種使用情境。第一種是把文字字串存放在 `char[]` 或 `VARCHAR[]` 中，如[第 34.4.4.1 節](ecpg-variables-type-mapping.md#ecpg-char)所述。第二種使用情境是不使用游標，就從查詢結果中取得多筆資料列。如果不使用陣列，要處理由多筆資料列組成的查詢結果，就必須使用游標與 `FETCH` 命令。但使用陣列主機變數時，可以一次接收多筆資料列。陣列的長度必須定義得足以容納所有資料列，否則很可能會發生緩衝區溢位。

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

### 34.4.4.3.2. 結構 [#](#ecpg-variables-struct) <a href="#ecpg-variables-struct" id="ecpg-variables-struct"></a>

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

### 34.4.4.3.3. 型別定義（typedef） [#](#ecpg-variables-nonprimitive-c-typedefs) <a href="#ecpg-variables-nonprimitive-c-typedefs" id="ecpg-variables-nonprimitive-c-typedefs"></a>

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

### 34.4.4.3.4. 指標 [#](#ecpg-variables-nonprimitive-c-pointers) <a href="#ecpg-variables-nonprimitive-c-pointers" id="ecpg-variables-nonprimitive-c-pointers"></a>

你可以宣告指向最常見型別的指標。不過請注意，若沒有自動配置，就不能把指標用作查詢的目標變數。關於自動配置的更多資訊，請參閱[第 34.7 節](ecpg-descriptors.md)。

```

EXEC SQL BEGIN DECLARE SECTION;
    int   *intp;
    char **charp;
EXEC SQL END DECLARE SECTION;
```

[返回 34.4.4. 型別對應](ecpg-variables-type-mapping.md#ecpg-variables-type-mapping)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-variables.html)（原文版本：18.6；核對日期：2026-10-18）
