<a id="LIBPQ-MISC"></a>

## 32.12. 其他函式 [#](#libpq-misc) <a href="#libpq-misc" id="libpq-misc"></a>

一如往常，總有一些函式不適合歸入任何類別。

<a id="LIBPQ-PQFREEMEM"></a>

### `PQfreemem`<a id="id-1.7.3.19.3.1.1.2"></a> [#](#libpq-pqfreemem) <a href="#libpq-pqfreemem" id="libpq-pqfreemem"></a>

釋放由 libpq 配置的記憶體。

```

    void PQfreemem(void *ptr);
```

釋放由 libpq 配置的記憶體，特別是由 [`PQescapeByteaConn`](libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN)、[`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA)、[`PQunescapeBytea`](libpq-exec.md#LIBPQ-PQUNESCAPEBYTEA) 與 `PQnotifies` 所配置的記憶體。在 Microsoft Windows 上，使用此函式而非 `free()` 尤其重要。這是因為只有在 DLL 與應用程式的多執行緒／單執行緒、發行／除錯以及靜態／動態旗標都相同時，在 DLL 中配置記憶體再於應用程式中釋放才能正常運作。在非 Microsoft Windows 的平台上，此函式與標準函式庫函式 `free()` 相同。

<a id="LIBPQ-PQCONNINFOFREE"></a>

### `PQconninfoFree`<a id="id-1.7.3.19.3.2.1.2"></a> [#](#libpq-pqconninfofree) <a href="#libpq-pqconninfofree" id="libpq-pqconninfofree"></a>

釋放由 [`PQconndefaults`](libpq-connect.md#LIBPQ-PQCONNDEFAULTS) 或 [`PQconninfoParse`](libpq-connect.md#LIBPQ-PQCONNINFOPARSE) 配置的資料結構。

```

    void PQconninfoFree(PQconninfoOption *connOptions);
```

若引數為 `NULL` 指標，則不執行任何操作。

單純使用 [`PQfreemem`](libpq-misc.md#libpq-pqfreemem) 無法完成這項工作，因為該陣列中含有對附屬字串的參照。

<a id="LIBPQ-PQENCRYPTPASSWORDCONN"></a>

### `PQencryptPasswordConn`<a id="id-1.7.3.19.3.3.1.2"></a> [#](#libpq-pqencryptpasswordconn) <a href="#libpq-pqencryptpasswordconn" id="libpq-pqencryptpasswordconn"></a>

產生 PostgreSQL 密碼的加密形式。

```

    char *PQencryptPasswordConn(PGconn *conn, const char *passwd, const char *user, const char *algorithm);
```

此函式供想要送出 `ALTER USER joe PASSWORD
'pwd'` 之類命令的用戶端應用程式使用。在這類命令中不送出原始明文密碼是良好的做法，因為密碼可能會暴露在命令日誌、活動顯示等處。請改用此函式，在送出之前先將密碼轉換為加密形式。

*`passwd`* 與 *`user`* 引數分別是明文密碼，以及該密碼所屬使用者的 SQL 名稱。*`algorithm`* 指定用來加密密碼的加密演算法。目前支援的演算法為 `md5` 與 `scram-sha-256`（為了與舊版伺服器相容，也接受 `on` 與 `off` 作為 `md5` 的別名）。請注意，`scram-sha-256` 的支援是在 PostgreSQL 第 10 版引入的，與更舊版本的伺服器搭配時將無法正常運作。若 *`algorithm`* 為 `NULL`，此函式會向伺服器查詢 [password_encryption](../../server-administration/runtime-config/runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION) 設定的目前值。這可能會造成阻塞；並且若目前交易已中止，或連線正忙於執行另一個查詢，則會失敗。若你想使用伺服器的預設演算法，但又想避免阻塞，請在呼叫 [`PQencryptPasswordConn`](libpq-misc.md#libpq-pqencryptpasswordconn) 之前自行查詢 `password_encryption`，並將該值作為 *`algorithm`* 傳入。

傳回值是以 `malloc` 配置的字串。呼叫端可以假設該字串不含任何需要跳脫的特殊字元。用完結果後，請使用 [`PQfreemem`](libpq-misc.md#libpq-pqfreemem) 釋放它。發生錯誤時傳回 `NULL`，並將適當的訊息存放在連線物件中。

<a id="LIBPQ-PQCHANGEPASSWORD"></a>

### `PQchangePassword`<a id="id-1.7.3.19.3.4.1.2"></a> [#](#libpq-pqchangepassword) <a href="#libpq-pqchangepassword" id="libpq-pqchangepassword"></a>

變更 PostgreSQL 密碼。

```

    PGresult *PQchangePassword(PGconn *conn, const char *user, const char *passwd);
```

此函式使用 `PQencryptPasswordConn` 建構並執行命令 `ALTER USER ... PASSWORD
'...'`，藉此變更使用者的密碼。它存在的理由與 `PQencryptPasswordConn` 相同，但更為方便，因為它會替你建構並執行該命令。傳給 [`PQencryptPasswordConn`](libpq-misc.md#libpq-pqencryptpasswordconn) 的演算法引數為 `NULL`，因此會依照伺服器的 [password_encryption](../../server-administration/runtime-config/runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION) 設定進行加密。

*`user`* 與 *`passwd`* 引數分別是目標使用者的 SQL 名稱，以及新的明文密碼。

傳回一個 `PGresult` 指標，代表 `ALTER USER` 命令的結果；若此常式在發出任何命令之前就失敗，則傳回空指標。應該呼叫 [`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) 函式檢查傳回值是否有任何錯誤（包括空指標的情況，此時它會傳回 `PGRES_FATAL_ERROR`）。請使用 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 取得這類錯誤的更多資訊。

<a id="LIBPQ-PQENCRYPTPASSWORD"></a>

### `PQencryptPassword`<a id="id-1.7.3.19.3.5.1.2"></a> [#](#libpq-pqencryptpassword) <a href="#libpq-pqencryptpassword" id="libpq-pqencryptpassword"></a>

產生 PostgreSQL 密碼的 md5 加密形式。

```

    char *PQencryptPassword(const char *passwd, const char *user);
```

[`PQencryptPassword`](libpq-misc.md#libpq-pqencryptpassword) 是 [`PQencryptPasswordConn`](libpq-misc.md#libpq-pqencryptpasswordconn) 較舊且已棄用的版本。兩者的差別在於 [`PQencryptPassword`](libpq-misc.md#libpq-pqencryptpassword) 不需要連線物件，而且一律使用 `md5` 作為加密演算法。

<a id="LIBPQ-PQMAKEEMPTYPGRESULT"></a>

### `PQmakeEmptyPGresult`<a id="id-1.7.3.19.3.6.1.2"></a> [#](#libpq-pqmakeemptypgresult) <a href="#libpq-pqmakeemptypgresult" id="libpq-pqmakeemptypgresult"></a>

以指定的狀態建構一個空的 `PGresult` 物件。

```

    PGresult *PQmakeEmptyPGresult(PGconn *conn, ExecStatusType status);
```

這是 libpq 用來配置並初始化空 `PGresult` 物件的內部函式。若無法配置記憶體，此函式會傳回 `NULL`。之所以將它匯出，是因為有些應用程式認為自行產生結果物件（特別是帶有錯誤狀態的物件）很有用。若 *`conn`* 不是空指標且 *`status`* 表示錯誤，則會將指定連線目前的錯誤訊息複製到該 `PGresult` 中。此外，若 *`conn`* 不是空指標，在該連線中註冊的所有事件程序都會被複製到該 `PGresult` 中。（它們不會收到 `PGEVT_RESULTCREATE` 呼叫，但請參閱 [`PQfireResultCreateEvents`](libpq-misc.md#libpq-pqfireresultcreateevents)。）請注意，最終應該對該物件呼叫 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR)，就如同對 libpq 本身傳回的 `PGresult` 一樣。

<a id="LIBPQ-PQFIRERESULTCREATEEVENTS"></a>

### `PQfireResultCreateEvents`<a id="id-1.7.3.19.3.7.1.2"></a> [#](#libpq-pqfireresultcreateevents) <a href="#libpq-pqfireresultcreateevents" id="libpq-pqfireresultcreateevents"></a>

對 `PGresult` 物件中註冊的每個事件程序觸發 `PGEVT_RESULTCREATE` 事件（請參閱[第 32.14 節](libpq-events.md)）。成功時傳回非零值，若有任何事件程序失敗則傳回零。

```

    int PQfireResultCreateEvents(PGconn *conn, PGresult *res);
```

`conn` 引數會傳遞給事件程序，但不會被直接使用。若事件程序不會用到它，可以為 `NULL`。

對於已經針對此物件收到 `PGEVT_RESULTCREATE` 或 `PGEVT_RESULTCOPY` 事件的事件程序，不會再次觸發。

此函式之所以與 [`PQmakeEmptyPGresult`](libpq-misc.md#libpq-pqmakeemptypgresult) 分開，主要原因是通常適合先建立 `PGresult` 並填入資料，再呼叫事件程序。

<a id="LIBPQ-PQCOPYRESULT"></a>

### `PQcopyResult`<a id="id-1.7.3.19.3.8.1.2"></a> [#](#libpq-pqcopyresult) <a href="#libpq-pqcopyresult" id="libpq-pqcopyresult"></a>

製作 `PGresult` 物件的複本。該複本與來源結果之間沒有任何關聯，不再需要該複本時必須呼叫 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR)。若函式失敗，則傳回 `NULL`。

```

    PGresult *PQcopyResult(const PGresult *src, int flags);
```

此函式並不打算製作完全相同的複本。傳回的結果一律處於 `PGRES_TUPLES_OK` 狀態，而且不會複製來源中的任何錯誤訊息。（不過，它會複製命令狀態字串。）*`flags`* 引數決定還要複製哪些內容，它是數個旗標的位元 OR。`PG_COPYRES_ATTRS` 指定複製來源結果的屬性（欄位定義）。`PG_COPYRES_TUPLES` 指定複製來源結果的元組。（這也隱含複製屬性。）`PG_COPYRES_NOTICEHOOKS` 指定複製來源結果的通知掛鉤（notify hooks）。`PG_COPYRES_EVENTS` 指定複製來源結果的事件。（但不會複製與來源相關聯的任何執行個體資料。）事件程序會收到 `PGEVT_RESULTCOPY` 事件。

<a id="LIBPQ-PQSETRESULTATTRS"></a>

### `PQsetResultAttrs`<a id="id-1.7.3.19.3.9.1.2"></a> [#](#libpq-pqsetresultattrs) <a href="#libpq-pqsetresultattrs" id="libpq-pqsetresultattrs"></a>

設定 `PGresult` 物件的屬性。

```

    int PQsetResultAttrs(PGresult *res, int numAttributes, PGresAttDesc *attDescs);
```

所提供的 *`attDescs`* 會被複製到結果中。若 *`attDescs`* 指標為 `NULL`，或 *`numAttributes`* 小於一，則忽略此請求，且函式視為成功。若 *`res`* 已經含有屬性，函式將會失敗。若函式失敗，傳回值為零；若函式成功，傳回值為非零。

<a id="LIBPQ-PQSETVALUE"></a>

### `PQsetvalue`<a id="id-1.7.3.19.3.10.1.2"></a> [#](#libpq-pqsetvalue) <a href="#libpq-pqsetvalue" id="libpq-pqsetvalue"></a>

設定 `PGresult` 物件中某個元組欄位的值。

```

    int PQsetvalue(PGresult *res, int tup_num, int field_num, char *value, int len);
```

此函式會視需要自動擴增結果內部的元組陣列。不過，*`tup_num`* 引數必須小於或等於 [`PQntuples`](libpq-exec.md#LIBPQ-PQNTUPLES)，這表示此函式一次只能將元組陣列擴增一個元組。但任何既有元組的任何欄位都可以依任意順序修改。若 *`field_num`* 位置已經有值，該值會被覆寫。若 *`len`* 為 -1 或 *`value`* 為 `NULL`，欄位值會被設為 SQL 空值。*`value`* 會被複製到結果的私有儲存空間中，因此函式返回後就不再需要它。若函式失敗，傳回值為零；若函式成功，傳回值為非零。

<a id="LIBPQ-PQRESULTALLOC"></a>

### `PQresultAlloc`<a id="id-1.7.3.19.3.11.1.2"></a> [#](#libpq-pqresultalloc) <a href="#libpq-pqresultalloc" id="libpq-pqresultalloc"></a>

為 `PGresult` 物件配置附屬儲存空間。

```

    void *PQresultAlloc(PGresult *res, size_t nBytes);
```

以此函式配置的任何記憶體，都會在 *`res`* 被清除時一併釋放。若函式失敗，傳回值為 `NULL`。其結果保證對任何型別的資料都有適當的對齊，就如同 `malloc` 一樣。

<a id="LIBPQ-PQRESULTMEMORYSIZE"></a>

### `PQresultMemorySize`<a id="id-1.7.3.19.3.12.1.2"></a> [#](#libpq-pqresultmemorysize) <a href="#libpq-pqresultmemorysize" id="libpq-pqresultmemorysize"></a>

取得為 `PGresult` 物件配置的位元組數。

```

    size_t PQresultMemorySize(const PGresult *res);
```

這個值是與該 `PGresult` 物件相關聯的所有 `malloc` 請求的總和，也就是 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 將會釋放的所有記憶體。此資訊可用於管理記憶體用量。

<a id="LIBPQ-PQLIBVERSION"></a>

### `PQlibVersion`<a id="id-1.7.3.19.3.13.1.2"></a> [#](#libpq-pqlibversion) <a href="#libpq-pqlibversion" id="libpq-pqlibversion"></a>

傳回目前使用的 libpq 版本。

```

    int PQlibVersion(void);
```

此函式的結果可用來在執行時判斷目前載入的 libpq 版本是否提供特定功能。例如，可以用此函式判斷 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 可使用哪些連線選項。

結果的組成方式是將函式庫的主要版本號乘以 10000，再加上次要版本號。例如，版本 10.1 會傳回 100001，版本 11.0 會傳回 110000。

在主要版本 10 之前，PostgreSQL 使用由三部分組成的版本號，其中前兩部分合起來代表主要版本。對於這些版本，[`PQlibVersion`](libpq-misc.md#libpq-pqlibversion) 每一部分各使用兩位數字；例如版本 9.1.5 會傳回 90105，版本 9.2.0 會傳回 90200。

因此，為了判斷功能相容性，應用程式應該將 [`PQlibVersion`](libpq-misc.md#libpq-pqlibversion) 的結果除以 100（而非 10000）來得出邏輯上的主要版本號。在所有發行系列中，次要版本（錯誤修正版本）之間只有最後兩位數字不同。

#### 注意

此函式是在 PostgreSQL 9.1 版出現的，因此無法用來偵測更早版本是否具備所需功能，因為呼叫它會產生對 9.1 或更新版本的連結相依性。

<a id="LIBPQ-PQGETCURRENTTIMEUSEC"></a>

### `PQgetCurrentTimeUSec`<a id="id-1.7.3.19.3.14.1.2"></a> [#](#libpq-pqgetcurrenttimeusec) <a href="#libpq-pqgetcurrenttimeusec" id="libpq-pqgetcurrenttimeusec"></a>

取得目前時間，以自 Unix 紀元以來的微秒數表示（也就是 `time_t` 乘以 100 萬）。

```

    pg_usec_time_t PQgetCurrentTimeUSec(void);
```

這主要用於計算要搭配 [`PQsocketPoll`](libpq-connect.md#LIBPQ-PQSOCKETPOLL) 使用的逾時值。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-misc.html)（原文版本：18.6；核對日期：2026-10-18）
