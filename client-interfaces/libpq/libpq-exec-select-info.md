<a id="LIBPQ-EXEC-SELECT-INFO"></a>

## 32.3.2. 取得查詢結果資訊 [#](#libpq-exec-select-info) <a href="#libpq-exec-select-info" id="libpq-exec-select-info"></a>

這些函式用來從代表成功查詢結果（也就是狀態為 `PGRES_TUPLES_OK`、`PGRES_SINGLE_TUPLE` 或 `PGRES_TUPLES_CHUNK` 的結果）的 `PGresult` 物件中擷取資訊。它們也可以用來從成功的 Describe 操作中擷取資訊：Describe 的結果具有與實際執行該查詢時所提供的完全相同的欄位資訊，但沒有任何資料列。對於其他狀態值的物件，這些函式的行為會如同結果有零筆資料列與零個欄位。

<a id="LIBPQ-PQNTUPLES"></a>

### `PQntuples`<a id="id-1.7.3.10.4.3.1.1.2"></a> [#](#libpq-pqntuples) <a href="#libpq-pqntuples" id="libpq-pqntuples"></a>

傳回查詢結果中的資料列（元組）數。（請注意，`PGresult` 物件最多只能有 `INT_MAX` 筆資料列，因此 `int` 型別的結果就足夠了。）

```

    int PQntuples(const PGresult *res);
```

<a id="LIBPQ-PQNFIELDS"></a>

### `PQnfields`<a id="id-1.7.3.10.4.3.2.1.2"></a> [#](#libpq-pqnfields) <a href="#libpq-pqnfields" id="libpq-pqnfields"></a>

傳回查詢結果中每筆資料列的欄位數。

```

    int PQnfields(const PGresult *res);
```

<a id="LIBPQ-PQFNAME"></a>

### `PQfname`<a id="id-1.7.3.10.4.3.3.1.2"></a> [#](#libpq-pqfname) <a href="#libpq-pqfname" id="libpq-pqfname"></a>

傳回與給定欄位編號相關聯的欄位名稱。欄位編號從 0 開始。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec-main.md#libpq-pqclear) 時，它就會被釋放。

```

    char *PQfname(const PGresult *res,
                  int column_number);
```

若欄位編號超出範圍，則傳回 `NULL`。

<a id="LIBPQ-PQFNUMBER"></a>

### `PQfnumber`<a id="id-1.7.3.10.4.3.4.1.2"></a> [#](#libpq-pqfnumber) <a href="#libpq-pqfnumber" id="libpq-pqfnumber"></a>

傳回與給定欄位名稱相關聯的欄位編號。

```

    int PQfnumber(const PGresult *res,
                  const char *column_name);
```

若給定的名稱不符合任何欄位，則傳回 -1。

給定的名稱會被視為 SQL 命令中的識別字，也就是說，除非加上雙引號，否則會轉為小寫。例如，給定由下列 SQL 命令產生的查詢結果：

```

    SELECT 1 AS FOO, 2 AS "BAR";
```

會得到下列結果：

```

    PQfname(res, 0)              foo
    PQfname(res, 1)              BAR
    PQfnumber(res, "FOO")        0
    PQfnumber(res, "foo")        0
    PQfnumber(res, "BAR")        -1
    PQfnumber(res, "\"BAR\"")    1
```

<a id="LIBPQ-PQFTABLE"></a>

### `PQftable`<a id="id-1.7.3.10.4.3.5.1.2"></a> [#](#libpq-pqftable) <a href="#libpq-pqftable" id="libpq-pqftable"></a>

傳回給定欄位所擷取自的資料表的 OID。欄位編號從 0 開始。

```

    Oid PQftable(const PGresult *res,
                 int column_number);
```

若欄位編號超出範圍，或指定的欄位不是對資料表欄位的單純參照，則傳回 `InvalidOid`。你可以查詢系統資料表 `pg_class`，以確切判斷所參照的是哪個資料表。

引入 libpq 標頭檔時，就會定義型別 `Oid` 與常數 `InvalidOid`。兩者都會是某種整數型別。

<a id="LIBPQ-PQFTABLECOL"></a>

### `PQftablecol`<a id="id-1.7.3.10.4.3.6.1.2"></a> [#](#libpq-pqftablecol) <a href="#libpq-pqftablecol" id="libpq-pqftablecol"></a>

傳回構成指定查詢結果欄位的那個欄位（在其資料表內）的欄位編號。查詢結果的欄位編號從 0 開始，但資料表欄位的編號不為零。

```

    int PQftablecol(const PGresult *res,
                    int column_number);
```

若欄位編號超出範圍，或指定的欄位不是對資料表欄位的單純參照，則傳回零。

<a id="LIBPQ-PQFFORMAT"></a>

### `PQfformat`<a id="id-1.7.3.10.4.3.7.1.2"></a> [#](#libpq-pqfformat) <a href="#libpq-pqfformat" id="libpq-pqfformat"></a>

傳回表示給定欄位格式的格式代碼。欄位編號從 0 開始。

```

    int PQfformat(const PGresult *res,
                  int column_number);
```

格式代碼 0 表示文字資料表示法，格式代碼 1 則表示二進位表示法。（其他代碼保留供未來定義。）

<a id="LIBPQ-PQFTYPE"></a>

### `PQftype`<a id="id-1.7.3.10.4.3.8.1.2"></a> [#](#libpq-pqftype) <a href="#libpq-pqftype" id="libpq-pqftype"></a>

傳回與給定欄位編號相關聯的資料型別。傳回的整數是該型別的內部 OID 編號。欄位編號從 0 開始。

```

    Oid PQftype(const PGresult *res,
                int column_number);
```

你可以查詢系統資料表 `pg_type`，以取得各種資料型別的名稱與屬性。內建資料型別的 OID 定義在 PostgreSQL 安裝目錄的 `include` 目錄中的 `catalog/pg_type_d.h` 檔案裡。

<a id="LIBPQ-PQFMOD"></a>

### `PQfmod`<a id="id-1.7.3.10.4.3.9.1.2"></a> [#](#libpq-pqfmod) <a href="#libpq-pqfmod" id="libpq-pqfmod"></a>

傳回與給定欄位編號相關聯之欄位的型別修飾詞。欄位編號從 0 開始。

```

    int PQfmod(const PGresult *res,
               int column_number);
```

修飾詞值的解讀方式依型別而定；它們通常表示精確度或大小限制。值 -1 用來表示「沒有可用的資訊」。大多數資料型別不使用修飾詞，此時該值一律為 -1。

<a id="LIBPQ-PQFSIZE"></a>

### `PQfsize`<a id="id-1.7.3.10.4.3.10.1.2"></a> [#](#libpq-pqfsize) <a href="#libpq-pqfsize" id="libpq-pqfsize"></a>

傳回與給定欄位編號相關聯之欄位的大小（以位元組為單位）。欄位編號從 0 開始。

```

    int PQfsize(const PGresult *res,
                int column_number);
```

[`PQfsize`](libpq-exec-select-info.md#libpq-pqfsize) 傳回資料庫資料列中為此欄位配置的空間，換句話說，就是該資料型別在伺服器內部表示法的大小。（因此，它對用戶端其實沒有太大用處。）負值表示該資料型別為變動長度。

<a id="LIBPQ-PQBINARYTUPLES"></a>

### `PQbinaryTuples`<a id="id-1.7.3.10.4.3.11.1.2"></a> [#](#libpq-pqbinarytuples) <a href="#libpq-pqbinarytuples" id="libpq-pqbinarytuples"></a>

若 `PGresult` 包含二進位資料，則傳回 1；若包含文字資料，則傳回 0。

```

    int PQbinaryTuples(const PGresult *res);
```

此函式已不建議使用（但與 `COPY` 搭配使用的情況除外），因為單一個 `PGresult` 可能在某些欄位中包含文字資料，而在其他欄位中包含二進位資料。建議改用 [`PQfformat`](libpq-exec-select-info.md#libpq-pqfformat)。只有在結果的所有欄位都是二進位（格式 1）時，[`PQbinaryTuples`](libpq-exec-select-info.md#libpq-pqbinarytuples) 才會傳回 1。

<a id="LIBPQ-PQGETVALUE"></a>

### `PQgetvalue`<a id="id-1.7.3.10.4.3.12.1.2"></a> [#](#libpq-pqgetvalue) <a href="#libpq-pqgetvalue" id="libpq-pqgetvalue"></a>

傳回 `PGresult` 中某一筆資料列的單一欄位值。資料列與欄位編號從 0 開始。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec-main.md#libpq-pqclear) 時，它就會被釋放。

```

    char *PQgetvalue(const PGresult *res,
                     int row_number,
                     int column_number);
```

對於文字格式的資料，[`PQgetvalue`](libpq-exec-select-info.md#libpq-pqgetvalue) 傳回的值是該欄位值以 null 結尾的字元字串表示法。對於二進位格式的資料，該值採用由該資料型別的 `typsend` 與 `typreceive` 函式所決定的二進位表示法。（在此情況下，該值後面其實也會接著一個零位元組，但這通常沒有用處，因為該值很可能含有內嵌的 null。）

若欄位值為 null，則傳回空字串。要區分 null 值與空字串值，請參閱 [`PQgetisnull`](libpq-exec-select-info.md#libpq-pqgetisnull)。

[`PQgetvalue`](libpq-exec-select-info.md#libpq-pqgetvalue) 傳回的指標指向屬於 `PGresult` 結構一部分的儲存空間。不應修改它所指向的資料，而且若要在 `PGresult` 結構本身的生命週期之後繼續使用這些資料，必須明確地將它們複製到其他儲存空間。

<a id="LIBPQ-PQGETISNULL"></a>

### `PQgetisnull`<a id="id-1.7.3.10.4.3.13.1.2"></a><a id="id-1.7.3.10.4.3.13.1.3"></a> [#](#libpq-pqgetisnull) <a href="#libpq-pqgetisnull" id="libpq-pqgetisnull"></a>

測試欄位是否為 null 值。資料列與欄位編號從 0 開始。

```

    int PQgetisnull(const PGresult *res,
                    int row_number,
                    int column_number);
```

若欄位為 null，此函式傳回 1；若包含非 null 值，則傳回 0。（請注意，對於 null 欄位，[`PQgetvalue`](libpq-exec-select-info.md#libpq-pqgetvalue) 會傳回空字串，而不是空指標。）

<a id="LIBPQ-PQGETLENGTH"></a>

### `PQgetlength`<a id="id-1.7.3.10.4.3.14.1.2"></a> [#](#libpq-pqgetlength) <a href="#libpq-pqgetlength" id="libpq-pqgetlength"></a>

傳回欄位值的實際長度（以位元組為單位）。資料列與欄位編號從 0 開始。

```

    int PQgetlength(const PGresult *res,
                    int row_number,
                    int column_number);
```

這是該特定資料值的實際資料長度，也就是 [`PQgetvalue`](libpq-exec-select-info.md#libpq-pqgetvalue) 所指向之物件的大小。對於文字資料格式，此值與 `strlen()` 相同。對於二進位格式，這是不可或缺的資訊。請注意，*不*應該依賴 [`PQfsize`](libpq-exec-select-info.md#libpq-pqfsize) 來取得實際的資料長度。

<a id="LIBPQ-PQNPARAMS"></a>

### `PQnparams`<a id="id-1.7.3.10.4.3.15.1.2"></a> [#](#libpq-pqnparams) <a href="#libpq-pqnparams" id="libpq-pqnparams"></a>

傳回預備陳述式的參數個數。

```

    int PQnparams(const PGresult *res);
```

此函式只有在檢視 [`PQdescribePrepared`](libpq-exec-main.md#libpq-pqdescribeprepared) 的結果時才有用。對於其他類型的結果，它會傳回零。

<a id="LIBPQ-PQPARAMTYPE"></a>

### `PQparamtype`<a id="id-1.7.3.10.4.3.16.1.2"></a> [#](#libpq-pqparamtype) <a href="#libpq-pqparamtype" id="libpq-pqparamtype"></a>

傳回指定陳述式參數的資料型別。參數編號從 0 開始。

```

    Oid PQparamtype(const PGresult *res, int param_number);
```

此函式只有在檢視 [`PQdescribePrepared`](libpq-exec-main.md#libpq-pqdescribeprepared) 的結果時才有用。對於其他類型的結果，它會傳回零。

<a id="LIBPQ-PQPRINT"></a>

### `PQprint`<a id="id-1.7.3.10.4.3.17.1.2"></a> [#](#libpq-pqprint) <a href="#libpq-pqprint" id="libpq-pqprint"></a>

將所有資料列，以及可選擇的欄位名稱，輸出到指定的輸出串流。

```

    void PQprint(FILE *fout,      /* output stream */
                 const PGresult *res,
                 const PQprintOpt *po);
    typedef struct
    {
        pqbool  header;      /* print output field headings and row count */
        pqbool  align;       /* fill align the fields */
        pqbool  standard;    /* old brain dead format */
        pqbool  html3;       /* output HTML tables */
        pqbool  expanded;    /* expand tables */
        pqbool  pager;       /* use pager for output if needed */
        char    *fieldSep;   /* field separator */
        char    *tableOpt;   /* attributes for HTML table element */
        char    *caption;    /* HTML table caption */
        char    **fieldName; /* null-terminated array of replacement field names */
    } PQprintOpt;
```

此函式以前被 psql 用來輸出查詢結果，但現在已不是如此。請注意，它假定所有資料都是文字格式。


[返回 32.3. 命令執行函式](libpq-exec.md#libpq-exec)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-exec.html)（原文版本：18.6；核對日期：2026-10-18）
