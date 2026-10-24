<a id="ECPG-DYNAMIC"></a>

## 34.5. 動態 SQL [#](#ECPG-DYNAMIC)

[34.5.1. 執行不傳回結果集的陳述式](ecpg-dynamic.md#ecpg-dynamic-without-result)

[34.5.2. 執行帶有輸入參數的陳述式](ecpg-dynamic.md#ecpg-dynamic-input)

[34.5.3. 執行傳回結果集的陳述式](ecpg-dynamic.md#ecpg-dynamic-with-result)

在許多情況下，應用程式必須執行的特定 SQL 陳述式在撰寫應用程式時就已經知道。然而，在某些情況下，SQL 陳述式是在執行時期才組成，或是由外部來源提供。在這些情況下，你無法將 SQL 陳述式直接嵌入 C 原始碼中，但有一項機制可以讓你呼叫你在字串變數中提供的任意 SQL 陳述式。

<a id="ECPG-DYNAMIC-WITHOUT-RESULT"></a>

### 34.5.1. 執行不傳回結果集的陳述式 [#](#ecpg-dynamic-without-result) <a href="#ecpg-dynamic-without-result" id="ecpg-dynamic-without-result"></a>

執行任意 SQL 陳述式最簡單的方式，是使用 `EXECUTE IMMEDIATE` 命令。例如：

```

EXEC SQL BEGIN DECLARE SECTION;
const char *stmt = "CREATE TABLE test1 (...);";
EXEC SQL END DECLARE SECTION;

EXEC SQL EXECUTE IMMEDIATE :stmt;
```

`EXECUTE IMMEDIATE` 可用於不傳回結果集的 SQL 陳述式（例如 DDL、`INSERT`、`UPDATE`、`DELETE`）。你無法以這種方式執行擷取資料的陳述式（例如 `SELECT`）。下一節會說明該怎麼做。

<a id="ECPG-DYNAMIC-INPUT"></a>

### 34.5.2. 執行帶有輸入參數的陳述式 [#](#ecpg-dynamic-input) <a href="#ecpg-dynamic-input" id="ecpg-dynamic-input"></a>

執行任意 SQL 陳述式更強大的方式，是先將它們預備一次，然後依需要多次執行該預備陳述式。也可以預備一個通用版本的陳述式，再透過代入參數來執行它的特定版本。預備陳述式時，在稍後要代入參數的位置寫上問號。例如：

```

EXEC SQL BEGIN DECLARE SECTION;
const char *stmt = "INSERT INTO test1 VALUES(?, ?);";
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE mystmt FROM :stmt;
 ...
EXEC SQL EXECUTE mystmt USING 42, 'foobar';
```

當你不再需要該預備陳述式時，應該將它釋放：

```

EXEC SQL DEALLOCATE PREPARE name;
```

<a id="ECPG-DYNAMIC-WITH-RESULT"></a>

### 34.5.3. 執行傳回結果集的陳述式 [#](#ecpg-dynamic-with-result) <a href="#ecpg-dynamic-with-result" id="ecpg-dynamic-with-result"></a>

要執行只有單一結果資料列的 SQL 陳述式，可以使用 `EXECUTE`。要儲存結果，請加上 `INTO` 子句。

```

EXEC SQL BEGIN DECLARE SECTION;
const char *stmt = "SELECT a, b, c FROM test1 WHERE a > ?";
int v1, v2;
VARCHAR v3[50];
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE mystmt FROM :stmt;
 ...
EXEC SQL EXECUTE mystmt INTO :v1, :v2, :v3 USING 37;
```

譯註：上方範例假設查詢只會傳回單一資料列；但其條件 a > ? 並不保證如此。若 test1 中有超過一個資料列符合條件，此 EXECUTE ... INTO 會因結果超過一列而出錯（ECPG_TOO_MANY_MATCHES，請參閱第 34.8.3 節），此時應改用下文所述的游標。範例程式碼依原文保留。

`EXECUTE` 命令可以有 `INTO` 子句、`USING` 子句、兩者皆有，或兩者皆無。

若預期查詢會傳回超過一個結果資料列，應該使用游標，如下列範例所示。（關於游標的詳細資訊，請參閱[第 34.3.2 節](ecpg-commands.md#ecpg-cursors)。）

```

EXEC SQL BEGIN DECLARE SECTION;
char dbaname[128];
char datname[128];
char *stmt = "SELECT u.usename as dbaname, d.datname "
             "  FROM pg_database d, pg_user u "
             "  WHERE d.datdba = u.usesysid";
EXEC SQL END DECLARE SECTION;

EXEC SQL CONNECT TO testdb AS con1 USER testuser;
EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

EXEC SQL PREPARE stmt1 FROM :stmt;

EXEC SQL DECLARE cursor1 CURSOR FOR stmt1;
EXEC SQL OPEN cursor1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH cursor1 INTO :dbaname,:datname;
    printf("dbaname=%s, datname=%s\n", dbaname, datname);
}

EXEC SQL CLOSE cursor1;

EXEC SQL COMMIT;
EXEC SQL DISCONNECT ALL;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-dynamic.html)（原文版本：18.6；核對日期：2026-10-22）
