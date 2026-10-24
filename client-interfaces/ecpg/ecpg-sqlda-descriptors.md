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

本節內容請參閱[34.7.2.4. 使用 SQLDA 的範例應用程式](ecpg-sqlda-example.md#ecpg-sqlda-example)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
