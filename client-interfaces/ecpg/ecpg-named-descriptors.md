<a id="ECPG-NAMED-DESCRIPTORS"></a>

## 34.7.1. 具名 SQL 描述區 [#](#ecpg-named-descriptors) <a href="#ecpg-named-descriptors" id="ecpg-named-descriptors"></a>

具名 SQL 描述區由一個標頭，以及一個或多個項目描述區組成；標頭包含與整個描述區有關的資訊，而每個項目描述區基本上描述結果資料列中的一個欄位。

使用 SQL 描述區之前，你需要先配置一個：

```

EXEC SQL ALLOCATE DESCRIPTOR identifier;
```

該識別字的作用相當於描述區的「變數名稱」。不再需要該描述區時，你應該將它釋放：

```

EXEC SQL DEALLOCATE DESCRIPTOR identifier;
```

若要使用描述區，請在 `INTO` 子句中將它指定為儲存目標，而不是列出主機變數：

```

EXEC SQL FETCH NEXT FROM mycursor INTO SQL DESCRIPTOR mydesc;
```

若結果集是空的，描述區仍然會包含查詢的中繼資料，也就是欄位名稱。

對於尚未執行的預備查詢，可以使用 `DESCRIBE` 陳述式取得結果集的中繼資料：

```

EXEC SQL BEGIN DECLARE SECTION;
char *sql_stmt = "SELECT * FROM table1";
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE stmt1 FROM :sql_stmt;
EXEC SQL DESCRIBE stmt1 INTO SQL DESCRIPTOR mydesc;
```

在 PostgreSQL 9.0 之前，`SQL` 關鍵字是選用的，因此使用 `DESCRIPTOR` 與 `SQL DESCRIPTOR` 都會產生具名 SQL 描述區。現在它是必要的；省略 `SQL` 關鍵字會產生 SQLDA 描述區，請參閱[第 34.7.2 節](ecpg-sqlda-descriptors.md#ecpg-sqlda-descriptors)。

在 `DESCRIBE` 與 `FETCH` 陳述式中，`INTO` 與 `USING` 關鍵字可以同樣地使用：它們會在描述區中產生結果集與中繼資料。

那麼，要如何從描述區取出資料呢？你可以把描述區想成一個具有具名欄位的結構。若要從標頭取得某個欄位的值並存入主機變數，請使用下列命令：

```

EXEC SQL GET DESCRIPTOR name :hostvar = field;
```

目前只定義了一個標頭欄位：*`COUNT`*，它表示有多少個項目描述區（也就是結果中包含多少個欄位）。主機變數需要是整數型別。若要從項目描述區取得某個欄位，請使用下列命令：

```

EXEC SQL GET DESCRIPTOR name VALUE num :hostvar = field;
```

*`num`* 可以是整數常數，或內容為整數的主機變數。可用的欄位如下：

<a id="ECPG-NAMED-DESCRIPTORS-CARDINALITY"></a>

### `CARDINALITY`（整數） [#](#ecpg-named-descriptors-cardinality) <a href="#ecpg-named-descriptors-cardinality" id="ecpg-named-descriptors-cardinality"></a>

結果集中的資料列數

<a id="ECPG-NAMED-DESCRIPTORS-DATA"></a>

### `DATA` [#](#ecpg-named-descriptors-data) <a href="#ecpg-named-descriptors-data" id="ecpg-named-descriptors-data"></a>

實際的資料項目（因此，此欄位的資料型別取決於查詢）

<a id="ECPG-NAMED-DESCRIPTORS-DATETIME-INTERVAL-CODE"></a>

### `DATETIME_INTERVAL_CODE`（整數） [#](#ecpg-named-descriptors-datetime-interval-code) <a href="#ecpg-named-descriptors-datetime-interval-code" id="ecpg-named-descriptors-datetime-interval-code"></a>

當 `TYPE` 為 `9` 時，`DATETIME_INTERVAL_CODE` 的值為：`DATE` 是 `1`、`TIME` 是 `2`、`TIMESTAMP` 是 `3`、`TIME WITH TIME ZONE` 是 `4`，或 `TIMESTAMP WITH TIME ZONE` 是 `5`。

<a id="ECPG-NAMED-DESCRIPTORS-DATETIME-INTERVAL-PRECISION"></a>

### `DATETIME_INTERVAL_PRECISION`（整數） [#](#ecpg-named-descriptors-datetime-interval-precision) <a href="#ecpg-named-descriptors-datetime-interval-precision" id="ecpg-named-descriptors-datetime-interval-precision"></a>

未實作

<a id="ECPG-NAMED-DESCRIPTORS-INDICATOR"></a>

### `INDICATOR`（整數） [#](#ecpg-named-descriptors-indicator) <a href="#ecpg-named-descriptors-indicator" id="ecpg-named-descriptors-indicator"></a>

指示值（表示空值或值遭到截斷）

<a id="ECPG-NAMED-DESCRIPTORS-KEY-MEMBER"></a>

### `KEY_MEMBER`（整數） [#](#ecpg-named-descriptors-key-member) <a href="#ecpg-named-descriptors-key-member" id="ecpg-named-descriptors-key-member"></a>

未實作

<a id="ECPG-NAMED-DESCRIPTORS-LENGTH"></a>

### `LENGTH`（整數） [#](#ecpg-named-descriptors-length) <a href="#ecpg-named-descriptors-length" id="ecpg-named-descriptors-length"></a>

資料值的長度（以字元計）

<a id="ECPG-NAMED-DESCRIPTORS-NAME"></a>

### `NAME`（字串） [#](#ecpg-named-descriptors-name) <a href="#ecpg-named-descriptors-name" id="ecpg-named-descriptors-name"></a>

欄位名稱

<a id="ECPG-NAMED-DESCRIPTORS-NULLABLE"></a>

### `NULLABLE`（整數） [#](#ecpg-named-descriptors-nullable) <a href="#ecpg-named-descriptors-nullable" id="ecpg-named-descriptors-nullable"></a>

未實作

<a id="ECPG-NAMED-DESCRIPTORS-OCTET-LENGTH"></a>

### `OCTET_LENGTH`（整數） [#](#ecpg-named-descriptors-octet-length) <a href="#ecpg-named-descriptors-octet-length" id="ecpg-named-descriptors-octet-length"></a>

資料值之字元表示法的長度（以位元組計）

<a id="ECPG-NAMED-DESCRIPTORS-PRECISION"></a>

### `PRECISION`（整數） [#](#ecpg-named-descriptors-precision) <a href="#ecpg-named-descriptors-precision" id="ecpg-named-descriptors-precision"></a>

精確度（用於 `numeric` 型別）

<a id="ECPG-NAMED-DESCRIPTORS-RETURNED-LENGTH"></a>

### `RETURNED_LENGTH`（整數） [#](#ecpg-named-descriptors-returned-length) <a href="#ecpg-named-descriptors-returned-length" id="ecpg-named-descriptors-returned-length"></a>

資料值的長度（以字元計）

<a id="ECPG-NAMED-DESCRIPTORS-RETURNED-OCTET-LENGTH"></a>

### `RETURNED_OCTET_LENGTH`（整數） [#](#ecpg-named-descriptors-returned-octet-length) <a href="#ecpg-named-descriptors-returned-octet-length" id="ecpg-named-descriptors-returned-octet-length"></a>

資料值之字元表示法的長度（以位元組計）

<a id="ECPG-NAMED-DESCRIPTORS-SCALE"></a>

### `SCALE`（整數） [#](#ecpg-named-descriptors-scale) <a href="#ecpg-named-descriptors-scale" id="ecpg-named-descriptors-scale"></a>

小數位數（用於 `numeric` 型別）

<a id="ECPG-NAMED-DESCRIPTORS-TYPE"></a>

### `TYPE`（整數） [#](#ecpg-named-descriptors-type) <a href="#ecpg-named-descriptors-type" id="ecpg-named-descriptors-type"></a>

欄位資料型別的數值代碼

在 `EXECUTE`、`DECLARE` 與 `OPEN` 陳述式中，`INTO` 與 `USING` 關鍵字的作用不同。描述區也可以手動建立，用來為查詢或游標提供輸入參數，而 `USING SQL DESCRIPTOR name` 就是將輸入參數傳入參數化查詢的方式。建立具名 SQL 描述區的陳述式如下：

```

EXEC SQL SET DESCRIPTOR name VALUE num field = :hostvar;
```

PostgreSQL 支援在一個 `FETCH` 陳述式中擷取超過一筆記錄；在這種情況下，將資料存入主機變數時，會假設該變數是陣列。例如：

```

EXEC SQL BEGIN DECLARE SECTION;
int id[5];
EXEC SQL END DECLARE SECTION;

EXEC SQL FETCH 5 FROM mycursor INTO SQL DESCRIPTOR mydesc;

EXEC SQL GET DESCRIPTOR mydesc VALUE 1 :id = DATA;
```

[返回 34.7. 使用描述區](ecpg-descriptors.md#ecpg-descriptors)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
