<a id="LIBPQ-EXEC-ESCAPE-STRING"></a>

## 32.3.4. 跳脫要放入 SQL 命令的字串 [#](#libpq-exec-escape-string) <a href="#libpq-exec-escape-string" id="libpq-exec-escape-string"></a>

<a id="id-1.7.3.10.6.2"></a>

<a id="LIBPQ-PQESCAPELITERAL"></a>

### `PQescapeLiteral`<a id="id-1.7.3.10.6.3.1.1.2"></a> [#](#libpq-pqescapeliteral) <a href="#libpq-pqescapeliteral" id="libpq-pqescapeliteral"></a>

```

    char *PQescapeLiteral(PGconn *conn, const char *str, size_t length);
```

[`PQescapeLiteral`](libpq-exec-escape-string.md#libpq-pqescapeliteral) 會跳脫字串，以便在 SQL 命令中使用。在 SQL 命令中以字面常數插入資料值時，這很有用。某些字元（例如引號與反斜線）必須跳脫，以避免被 SQL 剖析器做特殊解讀。[`PQescapeLiteral`](libpq-exec-escape-string.md#libpq-pqescapeliteral) 就是執行這項操作。

[`PQescapeLiteral`](libpq-exec-escape-string.md#libpq-pqescapeliteral) 在以 `malloc()` 配置的記憶體中傳回 *`str`* 參數的跳脫版本。不再需要該結果時，應該使用 `PQfreemem()` 釋放這塊記憶體。結尾的零位元組不是必要的，也不應計入 *`length`*。（若在處理完 *`length`* 個位元組之前就遇到結尾的零位元組，[`PQescapeLiteral`](libpq-exec-escape-string.md#libpq-pqescapeliteral) 會在該零位元組處停止；因此其行為與 `strncpy` 相當類似。）傳回的字串中所有特殊字元都已被替換，因此能被 PostgreSQL 字串字面值剖析器正確處理。結尾也會加上零位元組。PostgreSQL 字串字面值兩側必須加上的單引號也包含在結果字串中。

發生錯誤時，[`PQescapeLiteral`](libpq-exec-escape-string.md#libpq-pqescapeliteral) 會傳回 `NULL`，並在 *`conn`* 物件中存入適當的訊息。

#### 提示

處理從不可信來源收到的字串時，進行適當的跳脫尤其重要。否則會有安全風險：你容易遭受「SQL 注入」攻擊，也就是有不想要的 SQL 命令被送進你的資料庫。

請注意，當資料值以 [`PQexecParams`](libpq-exec-main.md#libpq-pqexecparams) 或其同類常式中的獨立參數傳遞時，進行跳脫既不必要，也不正確。

<a id="LIBPQ-PQESCAPEIDENTIFIER"></a>

### `PQescapeIdentifier`<a id="id-1.7.3.10.6.3.2.1.2"></a> [#](#libpq-pqescapeidentifier) <a href="#libpq-pqescapeidentifier" id="libpq-pqescapeidentifier"></a>

```

    char *PQescapeIdentifier(PGconn *conn, const char *str, size_t length);
```

[`PQescapeIdentifier`](libpq-exec-escape-string.md#libpq-pqescapeidentifier) 會跳脫字串，以便作為 SQL 識別字使用，例如資料表、欄位或函式名稱。當使用者提供的識別字可能含有特殊字元，而這些字元原本不會被 SQL 剖析器解讀為識別字的一部分時，或是當識別字可能含有應保留大小寫的大寫字元時，這很有用。

[`PQescapeIdentifier`](libpq-exec-escape-string.md#libpq-pqescapeidentifier) 在以 `malloc()` 配置的記憶體中，傳回 *`str`* 參數跳脫為 SQL 識別字後的版本。不再需要該結果時，必須使用 `PQfreemem()` 釋放這塊記憶體。結尾的零位元組不是必要的，也不應計入 *`length`*。（若在處理完 *`length`* 個位元組之前就遇到結尾的零位元組，[`PQescapeIdentifier`](libpq-exec-escape-string.md#libpq-pqescapeidentifier) 會在該零位元組處停止；因此其行為與 `strncpy` 相當類似。）傳回的字串中所有特殊字元都已被替換，因此能被正確地當作 SQL 識別字處理。結尾也會加上零位元組。傳回的字串兩側也會加上雙引號。

發生錯誤時，[`PQescapeIdentifier`](libpq-exec-escape-string.md#libpq-pqescapeidentifier) 會傳回 `NULL`，並在 *`conn`* 物件中存入適當的訊息。

#### 提示

與字串字面值相同，為了防止 SQL 注入攻擊，從不可信來源收到的 SQL 識別字必須加以跳脫。

<a id="LIBPQ-PQESCAPESTRINGCONN"></a>

### `PQescapeStringConn`<a id="id-1.7.3.10.6.3.3.1.2"></a> [#](#libpq-pqescapestringconn) <a href="#libpq-pqescapestringconn" id="libpq-pqescapestringconn"></a>

```

    size_t PQescapeStringConn(PGconn *conn,
                              char *to, const char *from, size_t length,
                              int *error);
```

[`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn) 會跳脫字串字面值，與 [`PQescapeLiteral`](libpq-exec-escape-string.md#libpq-pqescapeliteral) 非常類似。與 [`PQescapeLiteral`](libpq-exec-escape-string.md#libpq-pqescapeliteral) 不同的是，呼叫者必須負責提供大小適當的緩衝區。此外，[`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn) 不會產生 PostgreSQL 字串字面值兩側必須加上的單引號；這些單引號應該由要插入該結果的 SQL 命令提供。參數 *`from`* 指向要跳脫之字串的第一個字元，而參數 *`length`* 則給出此字串的位元組數。結尾的零位元組不是必要的，也不應計入 *`length`*。（若在處理完 *`length`* 個位元組之前就遇到結尾的零位元組，[`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn) 會在該零位元組處停止；因此其行為與 `strncpy` 相當類似。）*`to`* 必須指向一個至少能容納比 *`length`* 值的兩倍再多一個位元組的緩衝區，否則行為未定義。若 *`to`* 與 *`from`* 字串互相重疊，行為同樣未定義。

若 *`error`* 參數不是 `NULL`，則成功時 `*error` 會設為零，發生錯誤時設為非零。目前唯一可能的錯誤狀況是來源字串中有無效的多位元組編碼。發生錯誤時仍會產生輸出字串，但可以預期伺服器會因格式錯誤而拒絕它。發生錯誤時，無論 *`error`* 是否為 `NULL`，都會在 *`conn`* 物件中存入適當的訊息。

[`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn) 傳回寫入 *`to`* 的位元組數，不包括結尾的零位元組。

<a id="LIBPQ-PQESCAPESTRING"></a>

### `PQescapeString`<a id="id-1.7.3.10.6.3.4.1.2"></a> [#](#libpq-pqescapestring) <a href="#libpq-pqescapestring" id="libpq-pqescapestring"></a>

[`PQescapeString`](libpq-exec-escape-string.md#libpq-pqescapestring) 是 [`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn) 較舊且已不建議使用的版本。

```

    size_t PQescapeString (char *to, const char *from, size_t length);
```

與 [`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn) 唯一的差別在於 [`PQescapeString`](libpq-exec-escape-string.md#libpq-pqescapestring) 不接受 `PGconn` 或 *`error`* 參數。因此，它無法依據連線屬性（例如字元編碼）調整其行為，所以*可能產生錯誤的結果*。此外，它也無法回報錯誤狀況。

在一次只使用一個 PostgreSQL 連線的用戶端程式中，可以安全地使用 [`PQescapeString`](libpq-exec-escape-string.md#libpq-pqescapestring)（此時它可以在「幕後」查出它需要知道的資訊）。在其他情況下，它是一種安全隱患，應該避免使用，改用 [`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn)。

<a id="LIBPQ-PQESCAPEBYTEACONN"></a>

### `PQescapeByteaConn`<a id="id-1.7.3.10.6.3.5.1.2"></a> [#](#libpq-pqescapebyteaconn) <a href="#libpq-pqescapebyteaconn" id="libpq-pqescapebyteaconn"></a>

跳脫二進位資料，以便在 SQL 命令中以 `bytea` 型別使用。與 [`PQescapeStringConn`](libpq-exec-escape-string.md#libpq-pqescapestringconn) 相同，只有在將資料直接插入 SQL 命令字串時才會使用它。

```

    unsigned char *PQescapeByteaConn(PGconn *conn,
                                     const unsigned char *from,
                                     size_t from_length,
                                     size_t *to_length);
```

在 SQL 陳述式中作為 `bytea` 字面值的一部分使用時，某些位元組值必須加以跳脫。[`PQescapeByteaConn`](libpq-exec-escape-string.md#libpq-pqescapebyteaconn) 會使用十六進位編碼或反斜線跳脫來跳脫位元組。更多資訊請參閱[第 8.4 節](../../the-sql-language/datatype/datatype-binary.md)。

參數 *`from`* 指向要跳脫之字串的第一個位元組，而參數 *`from_length`* 則給出此二進位字串的位元組數。（結尾的零位元組既不必要，也不計入。）參數 *`to_length`* 指向一個變數，用來存放跳脫後字串的長度。此結果字串長度包含結果結尾的零位元組。

[`PQescapeByteaConn`](libpq-exec-escape-string.md#libpq-pqescapebyteaconn) 在以 `malloc()` 配置的記憶體中傳回 *`from`* 參數二進位字串的跳脫版本。不再需要該結果時，應該使用 `PQfreemem()` 釋放這塊記憶體。傳回的字串中所有特殊字元都已被替換，因此能被 PostgreSQL 字串字面值剖析器以及 `bytea` 輸入函式正確處理。結尾也會加上零位元組。PostgreSQL 字串字面值兩側必須加上的單引號不屬於結果字串的一部分。

發生錯誤時，會傳回空指標，並在 *`conn`* 物件中存入適當的錯誤訊息。目前唯一可能的錯誤是記憶體不足以容納結果字串。

<a id="LIBPQ-PQESCAPEBYTEA"></a>

### `PQescapeBytea`<a id="id-1.7.3.10.6.3.6.1.2"></a> [#](#libpq-pqescapebytea) <a href="#libpq-pqescapebytea" id="libpq-pqescapebytea"></a>

[`PQescapeBytea`](libpq-exec-escape-string.md#libpq-pqescapebytea) 是 [`PQescapeByteaConn`](libpq-exec-escape-string.md#libpq-pqescapebyteaconn) 較舊且已不建議使用的版本。

```

    unsigned char *PQescapeBytea(const unsigned char *from,
                                 size_t from_length,
                                 size_t *to_length);
```

與 [`PQescapeByteaConn`](libpq-exec-escape-string.md#libpq-pqescapebyteaconn) 唯一的差別在於 [`PQescapeBytea`](libpq-exec-escape-string.md#libpq-pqescapebytea) 不接受 `PGconn` 參數。因此，只有在一次只使用單一 PostgreSQL 連線的用戶端程式中，才能安全地使用 [`PQescapeBytea`](libpq-exec-escape-string.md#libpq-pqescapebytea)（此時它可以在「幕後」查出它需要知道的資訊）。若在使用多個資料庫連線的程式中使用，它*可能產生錯誤的結果*（這種情況請使用 [`PQescapeByteaConn`](libpq-exec-escape-string.md#libpq-pqescapebyteaconn)）。

<a id="LIBPQ-PQUNESCAPEBYTEA"></a>

### `PQunescapeBytea`<a id="id-1.7.3.10.6.3.7.1.2"></a> [#](#libpq-pqunescapebytea) <a href="#libpq-pqunescapebytea" id="libpq-pqunescapebytea"></a>

將二進位資料的字串表示法轉換為二進位資料——與 [`PQescapeBytea`](libpq-exec-escape-string.md#libpq-pqescapebytea) 相反。以文字格式取得 `bytea` 資料時需要這麼做，但以二進位格式取得時則不需要。

```

    unsigned char *PQunescapeBytea(const unsigned char *from, size_t *to_length);
```

參數 *`from`* 指向一個字串，例如對 `bytea` 欄位套用 [`PQgetvalue`](libpq-exec-select-info.md#libpq-pqgetvalue) 時可能傳回的字串。[`PQunescapeBytea`](libpq-exec-escape-string.md#libpq-pqunescapebytea) 會將此字串表示法轉換為其二進位表示法。它傳回一個指向以 `malloc()` 配置之緩衝區的指標，發生錯誤時則傳回 `NULL`，並將緩衝區的大小放入 *`to_length`*。不再需要該結果時，必須使用 [`PQfreemem`](libpq-misc.md#libpq-pqfreemem) 將它釋放。

此轉換並非 [`PQescapeBytea`](libpq-exec-escape-string.md#libpq-pqescapebytea) 的完全逆運算，因為從 [`PQgetvalue`](libpq-exec-select-info.md#libpq-pqgetvalue) 收到的字串並不預期是「已跳脫」的。特別是，這表示不需要考慮字串的引號處理，因此也不需要 `PGconn` 參數。

[返回 32.3. 命令執行函式](libpq-exec.md#libpq-exec)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-exec.html)（原文版本：18.6；核對日期：2026-10-18）
