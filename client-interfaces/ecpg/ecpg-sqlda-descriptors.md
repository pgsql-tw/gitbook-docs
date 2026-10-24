<a id="ECPG-SQLDA-DESCRIPTORS"></a>

## 34.7.2. SQLDA 描述區 [#](#ecpg-sqlda-descriptors) <a href="#ecpg-sqlda-descriptors" id="ecpg-sqlda-descriptors"></a>

SQLDA 描述區是一種 C 語言結構，同樣可以用來取得查詢的結果集與中繼資料。一個結構儲存結果集中的一筆記錄。

```

EXEC SQL include sqlda.h;
sqlda_t         *mysqlda;

EXEC SQL FETCH 3 FROM mycursor INTO DESCRIPTOR mysqlda;
```

請注意，這裡省略了 `SQL` 關鍵字。[第 34.7.1 節](ecpg-named-descriptors.md#ecpg-named-descriptors)中關於 `INTO` 與 `USING` 關鍵字使用情境的段落也適用於此，另外還有一點補充：在 `DESCRIBE` 陳述式中，若使用 `INTO` 關鍵字，則可以完全省略 `DESCRIPTOR` 關鍵字：

```

EXEC SQL DESCRIBE prepared_statement INTO mysqlda;
```

使用 SQLDA 的程式，一般流程如下：

1. 準備查詢，並為它宣告游標。
2. 為結果資料列宣告 SQLDA。
3. 為輸入參數宣告 SQLDA，並將其初始化（配置記憶體、設定參數）。
4. 以輸入 SQLDA 開啟游標。
5. 從游標擷取資料列，並存入輸出 SQLDA。
6. 從輸出 SQLDA 將值讀入主機變數（必要時進行轉換）。
7. 關閉游標。
8. 釋放為輸入 SQLDA 配置的記憶體區域。

<a id="ECPG-SQLDA-DESCRIPTORS-SQLDA"></a>

### 34.7.2.1. SQLDA 資料結構 [#](#ecpg-sqlda-descriptors-sqlda) <a href="#ecpg-sqlda-descriptors-sqlda" id="ecpg-sqlda-descriptors-sqlda"></a>

本節內容請參閱[34.7.2.1. SQLDA 資料結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-descriptors-sqlda)。

<a id="ECPG-SQLDA-OUTPUT"></a>

### 34.7.2.2. 使用 SQLDA 取得結果集 [#](#ecpg-sqlda-output) <a href="#ecpg-sqlda-output" id="ecpg-sqlda-output"></a>

透過 SQLDA 取得查詢結果集的一般步驟如下：

1. 宣告一個 `sqlda_t` 結構來接收結果集。
2. 執行指定了所宣告 SQLDA 的 `FETCH`／`EXECUTE`／`DESCRIBE` 命令來處理查詢。
3. 查看 `sqlda_t` 結構的成員 `sqln`，以檢查結果集中的記錄數（原文此處寫作「記錄數」；但依上文 sqln 與 sqld 的欄位說明，用於輸出時 sqln 的值與 sqld 相同，表示的是結果集的欄位數，而不是記錄數；各筆記錄須沿著 desc_next 指標逐一走訪）。
4. 從 `sqlda_t` 結構的成員 `sqlvar[0]`、`sqlvar[1]` 等取得各欄位的值。
5. 沿著 `sqlda_t` 結構的成員 `desc_next` 指標，移到下一個資料列（`sqlda_t` 結構）。
6. 視需要重複上述步驟。

以下是透過 SQLDA 取得結果集的範例。

首先，宣告一個 `sqlda_t` 結構來接收結果集。

```

sqlda_t *sqlda1;
```

接著，在命令中指定該 SQLDA。這是一個 `FETCH` 命令的範例。

```

EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;
```

執行迴圈，沿著鏈結串列取得各資料列。

```

sqlda_t *cur_sqlda;

for (cur_sqlda = sqlda1;
     cur_sqlda != NULL;
     cur_sqlda = cur_sqlda->desc_next)
{
    ...
}
```

在該迴圈內，再執行另一個迴圈，取得該資料列的每個欄位資料（`sqlvar_t` 結構）。

```

for (i = 0; i < cur_sqlda->sqld; i++)
{
    sqlvar_t v = cur_sqlda->sqlvar[i];
    char *sqldata = v.sqldata;
    short sqllen  = v.sqllen;
    ...
}
```

若要取得欄位值，請檢查 `sqlvar_t` 結構的成員 `sqltype` 的值。接著依欄位型別切換到適當的方式，將資料從 `sqlvar` 欄位複製到主機變數。

```

char var_buf[1024];

switch (v.sqltype)
{
    case ECPGt_char:
        memset(&var_buf, 0, sizeof(var_buf));
        memcpy(&var_buf, sqldata, (sizeof(var_buf) <= sqllen ? sizeof(var_buf) - 1 : sqllen));
        break;

    case ECPGt_int: /* integer */
        memcpy(&intval, sqldata, sqllen);
        snprintf(var_buf, sizeof(var_buf), "%d", intval);
        break;

    ...
}
```

<a id="ECPG-SQLDA-INPUT"></a>

### 34.7.2.3. 使用 SQLDA 傳遞查詢參數 [#](#ecpg-sqlda-input) <a href="#ecpg-sqlda-input" id="ecpg-sqlda-input"></a>

使用 SQLDA 將輸入參數傳給預備查詢的一般步驟如下：

1. 建立預備查詢（預備陳述式）
2. 宣告一個 sqlda_t 結構作為輸入 SQLDA。
3. 為輸入 SQLDA 配置記憶體區域（作為 sqlda_t 結構）。
4. 在已配置的記憶體中設定（複製）輸入值。
5. 指定輸入 SQLDA 來開啟游標。

以下是一個範例。

首先，建立預備陳述式。

```

EXEC SQL BEGIN DECLARE SECTION;
char query[1024] = "SELECT d.oid, * FROM pg_database d, pg_stat_database s WHERE d.oid = s.datid AND (d.datname = ? OR d.oid = ?)";
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE stmt1 FROM :query;
```

接著，為 SQLDA 配置記憶體，並在 `sqlda_t` 結構的成員變數 `sqln` 中設定輸入參數的數目。當預備查詢需要兩個或更多輸入參數時，應用程式必須配置額外的記憶體空間，其大小的計算方式為 (參數數目 - 1) \* sizeof(sqlvar_t)。此處所示的範例為兩個輸入參數配置記憶體空間。

```

sqlda_t *sqlda2;

sqlda2 = (sqlda_t *) malloc(sizeof(sqlda_t) + sizeof(sqlvar_t));
memset(sqlda2, 0, sizeof(sqlda_t) + sizeof(sqlvar_t));

sqlda2->sqln = 2; /* number of input variables */
```

配置記憶體之後，將參數值存入 `sqlvar[]` 陣列。（SQLDA 接收結果集時，用來取得欄位值的也是同一個陣列。）在此範例中，輸入參數為字串型別的 `"postgres"`，以及整數型別的 `1`。

```

sqlda2->sqlvar[0].sqltype = ECPGt_char;
sqlda2->sqlvar[0].sqldata = "postgres";
sqlda2->sqlvar[0].sqllen  = 8;

int intval = 1;
sqlda2->sqlvar[1].sqltype = ECPGt_int;
sqlda2->sqlvar[1].sqldata = (char *) &intval;
sqlda2->sqlvar[1].sqllen  = sizeof(intval);
```

開啟游標並指定事先設定好的 SQLDA，輸入參數就會傳給預備陳述式。

```

EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;
```

最後，使用完輸入 SQLDA 之後，必須明確釋放所配置的記憶體空間；這一點與用來接收查詢結果的 SQLDA 不同。

```

free(sqlda2);
```

<a id="ECPG-SQLDA-EXAMPLE"></a>

### 34.7.2.4. 使用 SQLDA 的範例應用程式 [#](#ecpg-sqlda-example) <a href="#ecpg-sqlda-example" id="ecpg-sqlda-example"></a>

以下是一個範例程式，說明如何從系統目錄擷取由輸入參數所指定之資料庫的存取統計資訊。

此應用程式以資料庫 OID 連接 pg_database 與 pg_stat_database 這兩個系統資料表，並擷取及顯示依兩個輸入參數（資料庫 `postgres` 與 OID `1`）取得的資料庫統計資訊。

首先，宣告一個輸入用的 SQLDA 與一個輸出用的 SQLDA。

```

EXEC SQL include sqlda.h;

sqlda_t *sqlda1; /* an output descriptor */
sqlda_t *sqlda2; /* an input descriptor  */
```

接著，連線到資料庫、準備陳述式，並為該預備陳述式宣告游標。

```

int
main(void)
{
    EXEC SQL BEGIN DECLARE SECTION;
    char query[1024] = "SELECT d.oid,* FROM pg_database d, pg_stat_database s WHERE d.oid=s.datid AND ( d.datname=? OR d.oid=? )";
    EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL PREPARE stmt1 FROM :query;
    EXEC SQL DECLARE cur1 CURSOR FOR stmt1;
```

接著，在輸入 SQLDA 中放入輸入參數的值。為輸入 SQLDA 配置記憶體，並將輸入參數的數目設定到 `sqln`。將型別、值與值的長度存入 `sqlvar` 結構中的 `sqltype`、`sqldata` 與 `sqllen`。

```

    /* Create SQLDA structure for input parameters. */
    sqlda2 = (sqlda_t *) malloc(sizeof(sqlda_t) + sizeof(sqlvar_t));
    memset(sqlda2, 0, sizeof(sqlda_t) + sizeof(sqlvar_t));
    sqlda2->sqln = 2; /* number of input variables */

    sqlda2->sqlvar[0].sqltype = ECPGt_char;
    sqlda2->sqlvar[0].sqldata = "postgres";
    sqlda2->sqlvar[0].sqllen  = 8;

    intval = 1;
    sqlda2->sqlvar[1].sqltype = ECPGt_int;
    sqlda2->sqlvar[1].sqldata = (char *)&intval;
    sqlda2->sqlvar[1].sqllen  = sizeof(intval);
```

設定好輸入 SQLDA 之後，以該輸入 SQLDA 開啟游標。

```

    /* Open a cursor with input parameters. */
    EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;
```

從已開啟的游標將資料列擷取到輸出 SQLDA。（一般而言，你必須在迴圈中重複呼叫 `FETCH`，才能擷取結果集中的所有資料列。）

```

    while (1)
    {
        sqlda_t *cur_sqlda;

        /* Assign descriptor to the cursor  */
        EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;
```

接著，沿著 `sqlda_t` 結構的鏈結串列，從 SQLDA 取出已擷取的記錄。

```

    for (cur_sqlda = sqlda1 ;
         cur_sqlda != NULL ;
         cur_sqlda = cur_sqlda->desc_next)
    {
        ...
```

讀取第一筆記錄中的每個欄位。欄位數存放在 `sqld`，第一個欄位的實際資料存放在 `sqlvar[0]`，兩者都是 `sqlda_t` 結構的成員。

```

        /* Print every column in a row. */
        for (i = 0; i < sqlda1->sqld; i++)
        {
            sqlvar_t v = sqlda1->sqlvar[i];
            char *sqldata = v.sqldata;
            short sqllen  = v.sqllen;

            strncpy(name_buf, v.sqlname.data, v.sqlname.length);
            name_buf[v.sqlname.length] = '\0';
```

譯註：上方程式片段依原文保留。它位於走訪 cur_sqlda 的迴圈內，卻讀取 sqlda1->sqld 與 sqlda1->sqlvar[i]，因此每一輪都只會讀到第一筆記錄；若要依序處理每一筆記錄，應改用 cur_sqlda->sqld 與 cur_sqlda->sqlvar[i]，範例 34.1 的完整程式即是如此。

現在，欄位資料已存放在變數 `v` 中。請依據 `v.sqltype` 判斷欄位的型別，將每個資料值複製到主機變數。

```

            switch (v.sqltype) {
                int intval;
                double doubleval;
                unsigned long long int longlongval;

                case ECPGt_char:
                    memset(&var_buf, 0, sizeof(var_buf));
                    memcpy(&var_buf, sqldata, (sizeof(var_buf) <= sqllen ? sizeof(var_buf)-1 : sqllen));
                    break;

                case ECPGt_int: /* integer */
                    memcpy(&intval, sqldata, sqllen);
                    snprintf(var_buf, sizeof(var_buf), "%d", intval);
                    break;

                ...

                default:
                    ...
            }

            printf("%s = %s (type: %d)\n", name_buf, var_buf, v.sqltype);
        }
```

處理完所有記錄後，關閉游標並中斷與資料庫的連線。

```

    EXEC SQL CLOSE cur1;
    EXEC SQL COMMIT;

    EXEC SQL DISCONNECT ALL;
```

完整的程式請見[範例 34.1](ecpg-sqlda-descriptors.md#ECPG-SQLDA-EXAMPLE-EXAMPLE)。

<a id="ECPG-SQLDA-EXAMPLE-EXAMPLE"></a>

**範例 34.1. SQLDA 範例程式**

```

#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

EXEC SQL include sqlda.h;

sqlda_t *sqlda1; /* descriptor for output */
sqlda_t *sqlda2; /* descriptor for input */

EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER SQLERROR STOP;

int
main(void)
{
    EXEC SQL BEGIN DECLARE SECTION;
    char query[1024] = "SELECT d.oid,* FROM pg_database d, pg_stat_database s WHERE d.oid=s.datid AND ( d.datname=? OR d.oid=? )";

    int intval;
    unsigned long long int longlongval;
    EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO uptimedb AS con1 USER uptime;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL PREPARE stmt1 FROM :query;
    EXEC SQL DECLARE cur1 CURSOR FOR stmt1;

    /* Create an SQLDA structure for an input parameter */
    sqlda2 = (sqlda_t *)malloc(sizeof(sqlda_t) + sizeof(sqlvar_t));
    memset(sqlda2, 0, sizeof(sqlda_t) + sizeof(sqlvar_t));
    sqlda2->sqln = 2; /* a number of input variables */

    sqlda2->sqlvar[0].sqltype = ECPGt_char;
    sqlda2->sqlvar[0].sqldata = "postgres";
    sqlda2->sqlvar[0].sqllen  = 8;

    intval = 1;
    sqlda2->sqlvar[1].sqltype = ECPGt_int;
    sqlda2->sqlvar[1].sqldata = (char *) &intval;
    sqlda2->sqlvar[1].sqllen  = sizeof(intval);

    /* Open a cursor with input parameters. */
    EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;

    while (1)
    {
        sqlda_t *cur_sqlda;

        /* Assign descriptor to the cursor  */
        EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;

        for (cur_sqlda = sqlda1 ;
             cur_sqlda != NULL ;
             cur_sqlda = cur_sqlda->desc_next)
        {
            int i;
            char name_buf[1024];
            char var_buf[1024];

            /* Print every column in a row. */
            for (i=0 ; i<cur_sqlda->sqld ; i++)
            {
                sqlvar_t v = cur_sqlda->sqlvar[i];
                char *sqldata = v.sqldata;
                short sqllen  = v.sqllen;

                strncpy(name_buf, v.sqlname.data, v.sqlname.length);
                name_buf[v.sqlname.length] = '\0';

                switch (v.sqltype)
                {
                    case ECPGt_char:
                        memset(&var_buf, 0, sizeof(var_buf));
                        memcpy(&var_buf, sqldata, (sizeof(var_buf)<=sqllen ? sizeof(var_buf)-1 : sqllen) );
                        break;

                    case ECPGt_int: /* integer */
                        memcpy(&intval, sqldata, sqllen);
                        snprintf(var_buf, sizeof(var_buf), "%d", intval);
                        break;

                    case ECPGt_long_long: /* bigint */
                        memcpy(&longlongval, sqldata, sqllen);
                        snprintf(var_buf, sizeof(var_buf), "%lld", longlongval);
                        break;

                    default:
                    {
                        int i;
                        memset(var_buf, 0, sizeof(var_buf));
                        for (i = 0; i < sqllen; i++)
                        {
                            char tmpbuf[16];
                            snprintf(tmpbuf, sizeof(tmpbuf), "%02x ", (unsigned char) sqldata[i]);
                            strncat(var_buf, tmpbuf, sizeof(var_buf));
                        }
                    }
                        break;
                }

                printf("%s = %s (type: %d)\n", name_buf, var_buf, v.sqltype);
            }

            printf("\n");
        }
    }

    EXEC SQL CLOSE cur1;
    EXEC SQL COMMIT;

    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

譯註：上方範例程式依原文保留，僅在此說明三點：

- 程式在 main 之前就宣告了 EXEC SQL WHENEVER NOT FOUND DO BREAK;，此設定會作用於其後的所有 SQL 陳述式。ecpg 會在 SELECT 等陳述式之後，產生「sqlca.sqlcode 等於 ECPG_NOT_FOUND 時執行 break」的檢查程式碼，而 main 開頭的 EXEC SQL SELECT pg_catalog.set_config(...) 並不在迴圈內，因此經前置處理後的 C 程式會因 break 不在迴圈或 switch 之中而無法編譯。應將 WHENEVER NOT FOUND DO BREAK 移到 while 迴圈之前（例如 OPEN 之後）。
- default 分支中的 strncat(var_buf, tmpbuf, sizeof(var_buf)) 以整個緩衝區大小作為上限，並未扣除 var_buf 已使用的長度，當 sqllen 很大時可能寫出緩衝區範圍；上限應為 sizeof(var_buf) - strlen(var_buf) - 1。
- 程式將 longlongval 宣告為無號（unsigned）的長整數型別，卻以 %lld 格式輸出；%lld 對應的是有號整數，型別與格式不符。應使用相符的格式，例如改用 %llu 輸出無號值。

此範例的輸出應該類似下列內容（部分數字會有所不同）。

```

oid = 1 (type: 1)
datname = template1 (type: 1)
datdba = 10 (type: 1)
encoding = 0 (type: 5)
datistemplate = t (type: 1)
datallowconn = t (type: 1)
dathasloginevt = f (type: 1)
datconnlimit = -1 (type: 5)
datfrozenxid = 379 (type: 1)
dattablespace = 1663 (type: 1)
datconfig =  (type: 1)
datacl = {=c/uptime,uptime=CTc/uptime} (type: 1)
datid = 1 (type: 1)
datname = template1 (type: 1)
numbackends = 0 (type: 5)
xact_commit = 113606 (type: 9)
xact_rollback = 0 (type: 9)
blks_read = 130 (type: 9)
blks_hit = 7341714 (type: 9)
tup_returned = 38262679 (type: 9)
tup_fetched = 1836281 (type: 9)
tup_inserted = 0 (type: 9)
tup_updated = 0 (type: 9)
tup_deleted = 0 (type: 9)

oid = 11511 (type: 1)
datname = postgres (type: 1)
datdba = 10 (type: 1)
encoding = 0 (type: 5)
datistemplate = f (type: 1)
datallowconn = t (type: 1)
dathasloginevt = f (type: 1)
datconnlimit = -1 (type: 5)
datfrozenxid = 379 (type: 1)
dattablespace = 1663 (type: 1)
datconfig =  (type: 1)
datacl =  (type: 1)
datid = 11511 (type: 1)
datname = postgres (type: 1)
numbackends = 0 (type: 5)
xact_commit = 221069 (type: 9)
xact_rollback = 18 (type: 9)
blks_read = 1176 (type: 9)
blks_hit = 13943750 (type: 9)
tup_returned = 77410091 (type: 9)
tup_fetched = 3253694 (type: 9)
tup_inserted = 0 (type: 9)
tup_updated = 0 (type: 9)
tup_deleted = 0 (type: 9)
```

譯註：上方輸出依原文保留，但其中的 datconfig 欄位在 PostgreSQL 18 的 pg_database 目錄中已不存在（資料庫層級的設定改存於 pg_db_role_setting）。這是官方文件沿用舊版的輸出範例，並非在 PostgreSQL 18 上執行此程式的實際完整輸出；實際輸出的欄位會依 PostgreSQL 18 的 pg_database 定義而有所不同。

[返回 34.7. 使用描述區](ecpg-descriptors.md#ecpg-descriptors)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
