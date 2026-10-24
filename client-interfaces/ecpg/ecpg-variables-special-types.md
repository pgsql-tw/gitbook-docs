<a id="ECPG-SPECIAL-TYPES"></a>

## 34.4.4.2. 存取特殊資料型別 [#](#ecpg-special-types) <a href="#ecpg-special-types" id="ecpg-special-types"></a>

ECPG 包含一些特殊型別，可以幫助你輕鬆地與 PostgreSQL 伺服器的某些特殊資料型別互動。具體而言，它已實作對 `numeric`、`decimal`、`date`、`timestamp` 與 `interval` 型別的支援。這些資料型別因為內部結構複雜，無法有效地對應到基本的主機變數型別（例如 `int`、`long long int` 或 `char[]`）。應用程式處理這些型別的方式，是以特殊型別宣告主機變數，並使用 pgtypes 函式庫中的函式來存取它們。pgtypes 函式庫（詳見[第 34.6 節](ecpg-pgtypes.md)）包含處理這些型別的基本函式，例如，你不必只為了把一段時間間隔加到時間戳記上，就向 SQL 伺服器傳送查詢。

以下各小節說明這些特殊資料型別。關於 pgtypes 函式庫函式的更多細節，請參閱[第 34.6 節](ecpg-pgtypes.md)。

<a id="ECPG-SPECIAL-TYPES-TIMESTAMP-DATE"></a>

### 34.4.4.2.1. timestamp、date [#](#ecpg-special-types-timestamp-date) <a href="#ecpg-special-types-timestamp-date" id="ecpg-special-types-timestamp-date"></a>

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

### 34.4.4.2.2. interval [#](#ecpg-type-interval) <a href="#ecpg-type-interval" id="ecpg-type-interval"></a>

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

### 34.4.4.2.3. numeric、decimal [#](#ecpg-type-numeric-decimal) <a href="#ecpg-type-numeric-decimal" id="ecpg-type-numeric-decimal"></a>

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

### 34.4.4.2.4. bytea [#](#ecpg-special-types-bytea) <a href="#ecpg-special-types-bytea" id="ecpg-special-types-bytea"></a>

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

[返回 34.4.4. 型別對應](ecpg-variables-type-mapping.md#ecpg-variables-type-mapping)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-variables.html)（原文版本：18.6；核對日期：2026-10-18）
