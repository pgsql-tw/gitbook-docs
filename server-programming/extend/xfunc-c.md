<a id="XFUNC-C"></a>
## 36.10. C 語言函式 [#](#XFUNC-C)

[36.10.1. 動態載入](xfunc-c.md#XFUNC-C-DYNLOAD)

[36.10.2. C 語言函式中的基礎型別](xfunc-c.md#XFUNC-C-BASETYPE)

[36.10.3. 版本 1 呼叫慣例](xfunc-c.md#XFUNC-C-V1-CALL-CONV)

[36.10.4. 撰寫程式碼](xfunc-c.md#XFUNC-C-CODE)

[36.10.5. 編譯與連結動態載入的函式](xfunc-c.md#DFUNC)

[36.10.6. 伺服器 API 與 ABI 穩定性指引](xfunc-c.md#XFUNC-API-ABI-STABILITY-GUIDANCE)

[36.10.7. 複合型別引數](xfunc-c.md#XFUNC-C-COMPOSITE-TYPE-ARGS)

[36.10.8. 傳回資料列（複合型別）](xfunc-c.md#XFUNC-C-RETURNING-ROWS)

[36.10.9. 傳回集合](xfunc-c.md#XFUNC-C-RETURN-SET)

[36.10.10. 多型引數與傳回型別](xfunc-c.md#XFUNC-C-POLYMORPHIC)

[36.10.11. 共享記憶體](xfunc-c.md#XFUNC-SHARED-ADDIN)

[36.10.12. LWLocks](xfunc-c.md#XFUNC-ADDIN-LWLOCKS)

[36.10.13. 自訂等待事件](xfunc-c.md#XFUNC-ADDIN-WAIT-EVENTS)

[36.10.14. 注入點（Injection Points）](xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)

[36.10.15. 自訂累計統計資訊](xfunc-c.md#XFUNC-ADDIN-CUSTOM-CUMULATIVE-STATISTICS)

[36.10.16. 使用 C++ 來擴充功能](xfunc-c.md#EXTEND-CPP)

<a id="id-1.8.3.13.2"></a>

使用者定義函式可以用 C（或是可以與 C 相容的語言，
例如 C++）撰寫。這類函式會被
編譯成可動態載入的物件（也稱為共享
函式庫），並由伺服器依需要載入。動態
載入這項特性，是「C 語言」函式與「內部」（internal）函式
之間的區別——兩者實際的撰碼慣例
本質上是相同的。（因此，標準內部
函式庫，是使用者定義 C 函式撰碼範例的豐富來源。）

目前 C 函式只使用一種呼叫慣例
（「版本 1」）。對此呼叫慣例的支援，
是透過為函式撰寫一個 `PG_FUNCTION_INFO_V1()`
巨集呼叫來表示的，如下所示。

<a id="XFUNC-C-DYNLOAD"></a>

### 36.10.1. 動態載入 [#](#XFUNC-C-DYNLOAD)

<a id="id-1.8.3.13.5.2"></a>

當某個工作階段第一次呼叫特定可載入物件檔案
中的使用者定義函式時，
動態載入器會將該物件檔案載入記憶體，
以便呼叫該函式。因此，使用者定義 C 函式的
`CREATE FUNCTION` 必須為此函式指定兩項
資訊：可載入物件檔案的名稱，
以及要在該物件檔案中呼叫之特定函式的 C 名稱（連結符號）。若未明確指定
C 名稱，則會假設其與 SQL 函式名稱相同。

以下演算法會依據 `CREATE FUNCTION`
指令中所給的名稱，用來找出共享物件檔案：

1. 若該名稱是絕對路徑，就會載入所指定的檔案。
2. 若該名稱以字串 `$libdir` 開頭，
   這部分會被替換為 PostgreSQL 套件
   函式庫目錄
   名稱，這是在建置時決定的。<a id="id-1.8.3.13.5.4.2.2.1.3"></a>
3. 若該名稱不含目錄部分，就會在組態變數
   [dynamic_library_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH)所指定的路徑中
   搜尋該檔案。<a id="id-1.8.3.13.5.4.2.3.1.2"></a>
4. 否則（在路徑中找不到該檔案，或它含有
   非絕對路徑的目錄部分），動態載入器就會嘗試
   直接使用所給的名稱，這很可能會失敗。（依賴
   目前工作目錄是不可靠的。）

若這個順序都不成功，系統會在所給的名稱後面
附加特定平台的共享函式庫檔案名稱副檔名
（通常是 `.so`），並再次嘗試
這個順序。若這樣仍然失敗，
載入就會失敗。

建議將共享函式庫的位置，設定為相對於
`$libdir`，或透過動態函式庫路徑來指定。
如此一來，若新安裝的位置不同，就能簡化
版本升級的作業。`$libdir`
實際所代表的目錄，可以透過
`pg_config --pkglibdir` 指令查出。

執行 PostgreSQL 伺服器的使用者 ID
必須能夠走訪到您打算載入之檔案的路徑。
讓該檔案或更上層的目錄，對 postgres
使用者而言不可讀取及／或不可執行，是常見的
錯誤。

無論如何，`CREATE FUNCTION` 指令中所給定的
檔案名稱，都會被逐字記錄在系統目錄中，
因此若該檔案需要再次載入，系統就會採用
相同的程序。

### 注意

PostgreSQL 不會自動編譯 C
函式。物件檔案必須先編譯完成，才能在 `CREATE
FUNCTION` 指令中參照它。詳情請參閱
[36.10.5 節](xfunc-c.md#DFUNC)。

<a id="id-1.8.3.13.5.9"></a><a id="id-1.8.3.13.5.10"></a>

為確保動態載入的物件檔案不會被載入到
不相容的伺服器中，PostgreSQL 會檢查
該檔案是否包含具有適當內容的「魔術區塊」（magic block）。
這讓伺服器能夠偵測到明顯的不相容情況，例如程式碼是
為不同的 PostgreSQL 主要版本
編譯的。若要加入魔術區塊，
請在納入標頭檔 `fmgr.h` 之後，
於模組原始碼檔案中的其中一個（且僅限一個）檔案中，寫入以下內容：

```

PG_MODULE_MAGIC;
```

或

```

PG_MODULE_MAGIC_EXT(parameters);
```

`PG_MODULE_MAGIC_EXT` 這個變體，允許
指定關於此模組的額外資訊；目前可以加入
名稱及／或版本字串。（未來可能會允許更多欄位。）
請寫成類似這樣：

```

PG_MODULE_MAGIC_EXT(
    .name = "my_module_name",
    .version = "1.2.3"
);
```

之後可以透過
`pg_get_loaded_modules()` 函式來檢視此名稱與版本。
版本字串的意義並不受
PostgreSQL 所限制，但建議使用語意化版本
（semantic versioning）規則。

動態載入的物件檔案在第一次使用之後，
會被保留在記憶體中。同一個工作階段中，日後對該檔案中
函式的呼叫，只會產生查詢符號表這種
小額的額外開銷。若您需要強制重新載入物件
檔案，舉例來說在重新編譯之後，請開始一個新的
工作階段。

<a id="id-1.8.3.13.5.14"></a><a id="id-1.8.3.13.5.15"></a>

動態載入的檔案可以選擇性地包含一個初始化
函式。若該檔案包含一個名為
`_PG_init` 的函式，該函式會在載入此檔案之後
立即被呼叫。此函式不接受任何參數，且應該
傳回 void。目前沒有辦法卸載已動態載入的檔案。

<a id="XFUNC-C-BASETYPE"></a>

### 36.10.2. C 語言函式中的基礎型別 [#](#XFUNC-C-BASETYPE)

<a id="id-1.8.3.13.6.2"></a>

要知道如何撰寫 C 語言函式，您需要了解
PostgreSQL 內部如何表示基礎
資料型別，以及如何將它們傳入函式與從函式傳出。
在內部，PostgreSQL 把基礎
型別視為一個「記憶體區塊」（blob of memory）。您在某個型別上
定義的使用者定義函式，接著就定義了
PostgreSQL 能夠如何操作該型別。也就
是說，PostgreSQL 只會將資料
儲存到磁碟、從磁碟取出，並使用您所定義的使用者定義函式
來輸入、處理及輸出資料。

基礎型別可以採用以下三種內部格式之一：

* 依值傳遞，固定長度
* 依參照傳遞，固定長度
* 依參照傳遞，可變長度

依值傳遞的型別，長度只能是 1、2 或 4 個位元組
（若您機器上 `sizeof(Datum)` 為 8，則也可以是 8 個位元組）。
您應該小心地定義您的型別，讓它們在所有架構上
的（位元組）大小都相同。舉例來說，
`long` 型別就相當危險，因為它在某些機器上是 4 個位元組，
在其他機器上則是 8 個位元組，而 `int` 型別
在大多數 Unix 機器上是 4 個位元組。在 Unix 機器上，
`int4` 型別的一種合理實作方式可能是：

```

/* 4-byte integer, passed by value */
typedef int int4;
```

（實際的 PostgreSQL C 程式碼將此型別稱為 `int32`，
因為在 C 語言中有一項慣例，`intXX`
代表*`XX`* *位元*。因此也請注意，
C 型別 `int8` 的大小是 1 個位元組。SQL
型別 `int8` 在 C 中稱為 `int64`。另請參閱
[表 36.2](xfunc-c.md#XFUNC-C-TYPE-TABLE)。）

另一方面，任何大小的固定長度型別，都可以
依參照傳遞。舉例來說，以下是一個
PostgreSQL 型別的實作範例：

```

/* 16-byte structure, passed by reference */
typedef struct
{
    double  x, y;
} Point;
```

在 PostgreSQL 函式中傳入與傳出
這類型別時，只能使用指向它們的指標。
若要傳回此類型別的值，請用
`palloc` 配置適當大小的記憶體，
填入所配置的記憶體，然後傳回指向它的指標。（此外，
若您只是想傳回與您某個輸入引數相同資料型別的相同值，
可以省略額外的 `palloc`，直接傳回指向
輸入值的指標。）

最後，所有可變長度的型別，也都必須
依參照傳遞。所有可變長度型別的開頭，都必須是
恰好 4 個位元組的不透明長度欄位，該欄位會由
`SET_VARSIZE` 設定；請絕對不要直接設定這個欄位！所有要
儲存在該型別中的資料，都必須位於緊接在
該長度欄位之後的記憶體中。這個
長度欄位包含此結構的總長度，
也就是說，它也包含了長度欄位
本身的大小。

另一個重點是，要避免在資料型別的值中
留下任何未初始化的位元；舉例來說，請小心地將
結構中可能出現的任何對齊填補位元組清零。
若不這麼做，規劃器可能會將您資料型別中
邏輯上相等的常數視為不相等，
導致（雖然不算錯誤，但）效率不佳的執行計畫。

<a id="id-1.8.3.13.6.3"></a>

### 警告

*絕對不要*修改依參照傳遞之輸入值的內容。
若您這麼做，很可能會損毀磁碟上的資料，
因為您取得的指標，可能直接指向磁碟緩衝區。
此規則唯一的例外，說明於
[36.12 節](xaggr.md)中。

舉例來說，我們可以像這樣定義 `text`
型別：

```

typedef struct {
    int32 length;
    char data[FLEXIBLE_ARRAY_MEMBER];
} text;
```

`[FLEXIBLE_ARRAY_MEMBER]` 表示法，代表資料部分的實際
長度，並未由此宣告所指定。

在操作
可變長度型別時，我們必須小心地配置
正確數量的記憶體，並正確設定長度欄位。
舉例來說，若我們想要在 `text`
結構中儲存 40 個位元組，可以使用類似以下的程式碼片段：

```

#include "postgres.h"
...
char buffer[40]; /* our source data */
...
text *destination = (text *) palloc(VARHDRSZ + 40);
SET_VARSIZE(destination, VARHDRSZ + 40);
memcpy(destination->data, buffer, 40);
...
```

`VARHDRSZ` 與 `sizeof(int32)` 相同，但
使用巨集 `VARHDRSZ` 來表示可變長度型別的額外開銷大小，
被視為是比較好的寫法。
此外，長度欄位*必須*使用
`SET_VARSIZE` 巨集來設定，而不能用簡單的賦值。

[表 36.2](xfunc-c.md#XFUNC-C-TYPE-TABLE)顯示了 PostgreSQL
許多內建 SQL 資料型別
所對應的 C 型別。
「定義於」欄位給出了要取得該型別定義
所需要納入的標頭檔。（實際的
定義可能位於該所列檔案所納入的另一個檔案中。建議使用者
遵循已定義的介面。）請注意，您在伺服器程式碼的任何原始碼檔案中，
都應該永遠先納入
`postgres.h`，因為它宣告了許多
您無論如何都會需要用到的內容，而且先納入其他
標頭檔可能會造成可攜性問題。

<a id="XFUNC-C-TYPE-TABLE"></a>

**表 36.2. 內建 SQL 型別對應的 C 型別**

<table border="1" class="table" summary="Equivalent C Types for Built-in SQL Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>
          SQL 型別
         </th><th>
          C 型別
         </th><th>
          定義於
         </th></tr></thead><tbody><tr><td><code class="type">boolean</code></td><td><code class="type">bool</code></td><td><code class="filename">postgres.h</code>（可能是編譯器內建）</td></tr><tr><td><code class="type">box</code></td><td><code class="type">BOX*</code></td><td><code class="filename">utils/geo_decls.h</code></td></tr><tr><td><code class="type">bytea</code></td><td><code class="type">bytea*</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">"char"</code></td><td><code class="type">char</code></td><td>（編譯器內建）</td></tr><tr><td><code class="type">character</code></td><td><code class="type">BpChar*</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">cid</code></td><td><code class="type">CommandId</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">date</code></td><td><code class="type">DateADT</code></td><td><code class="filename">utils/date.h</code></td></tr><tr><td><code class="type">float4</code>（<code class="type">real</code>）</td><td><code class="type">float4</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">float8</code>（<code class="type">double precision</code>）</td><td><code class="type">float8</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">int2</code>（<code class="type">smallint</code>）</td><td><code class="type">int16</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">int4</code>（<code class="type">integer</code>）</td><td><code class="type">int32</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">int8</code>（<code class="type">bigint</code>）</td><td><code class="type">int64</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">interval</code></td><td><code class="type">Interval*</code></td><td><code class="filename">datatype/timestamp.h</code></td></tr><tr><td><code class="type">lseg</code></td><td><code class="type">LSEG*</code></td><td><code class="filename">utils/geo_decls.h</code></td></tr><tr><td><code class="type">name</code></td><td><code class="type">Name</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">numeric</code></td><td><code class="type">Numeric</code></td><td><code class="filename">utils/numeric.h</code></td></tr><tr><td><code class="type">oid</code></td><td><code class="type">Oid</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">oidvector</code></td><td><code class="type">oidvector*</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">path</code></td><td><code class="type">PATH*</code></td><td><code class="filename">utils/geo_decls.h</code></td></tr><tr><td><code class="type">point</code></td><td><code class="type">POINT*</code></td><td><code class="filename">utils/geo_decls.h</code></td></tr><tr><td><code class="type">regproc</code></td><td><code class="type">RegProcedure</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">text</code></td><td><code class="type">text*</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">tid</code></td><td><code class="type">ItemPointer</code></td><td><code class="filename">storage/itemptr.h</code></td></tr><tr><td><code class="type">time</code></td><td><code class="type">TimeADT</code></td><td><code class="filename">utils/date.h</code></td></tr><tr><td><code class="type">time with time zone</code></td><td><code class="type">TimeTzADT</code></td><td><code class="filename">utils/date.h</code></td></tr><tr><td><code class="type">timestamp</code></td><td><code class="type">Timestamp</code></td><td><code class="filename">datatype/timestamp.h</code></td></tr><tr><td><code class="type">timestamp with time zone</code></td><td><code class="type">TimestampTz</code></td><td><code class="filename">datatype/timestamp.h</code></td></tr><tr><td><code class="type">varchar</code></td><td><code class="type">VarChar*</code></td><td><code class="filename">postgres.h</code></td></tr><tr><td><code class="type">xid</code></td><td><code class="type">TransactionId</code></td><td><code class="filename">postgres.h</code></td></tr></tbody></table>

<br>

現在我們已經介紹完基礎型別所有可能的
結構，接著可以展示一些實際函式的範例了。

<a id="XFUNC-C-V1-CALL-CONV"></a>

### 36.10.3. 版本 1 呼叫慣例 [#](#XFUNC-C-V1-CALL-CONV)

版本 1 的呼叫慣例，依靠巨集來隱藏傳遞引數與結果時
大部分的複雜性。版本 1 函式的 C
宣告永遠是：

```

Datum funcname(PG_FUNCTION_ARGS)
```

此外，以下巨集呼叫：

```

PG_FUNCTION_INFO_V1(funcname);
```

必須出現在同一個原始碼檔案中。（依照慣例，
它會寫在函式本身之前。）`internal`
語言函式不需要這個巨集呼叫，因為
PostgreSQL 會假設所有內部函式
都使用版本 1 慣例。然而，動態載入的函式
則需要它。

在版本 1 函式中，每個實際引數都是使用對應於
該引數資料型別的
`PG_GETARG_xxx()`
巨集來取得的。（在非嚴格函式中，需要事先使用
`PG_ARGISNULL()` 檢查引數是否為 null；
詳見下文。）
結果則是使用對應於傳回型別的
`PG_RETURN_xxx()`
巨集來傳回。
`PG_GETARG_xxx()`
的引數，是要取得的函式引數編號，
編號從 0 開始。
`PG_RETURN_xxx()`
的引數，則是要傳回的實際值。

要呼叫另一個版本 1 函式，您可以使用
`DirectFunctionCalln(func,
arg1, ..., argn)`。當您想要透過類似其 SQL 簽章
的介面，來呼叫標準內部函式庫中定義的函式時，
這特別有用。

這些便利函式及類似的函式，可以在
`fmgr.h` 中找到。
`DirectFunctionCalln`
系列函式，其第一個引數預期是 C 函式名稱。此外還有
`OidFunctionCalln`，
它接受目標函式的 OID，以及其他一些變體。所有
這些函式，都預期函式的引數是以
`Datum` 的形式提供，同樣地，它們也會傳回 `Datum`。
請注意，使用這些便利函式時，引數與結果都不允許是 NULL。

舉例來說，若要從 C 呼叫 `starts_with(text, text)`
函式，您可以搜尋目錄（catalog），找出它的
C 實作為
`Datum text_starts_with(PG_FUNCTION_ARGS)`
函式。通常您會
使用 `DirectFunctionCall2(text_starts_with, ...)` 來
呼叫這樣的函式。不過，`starts_with(text,
text)` 需要定序（collation）資訊，因此若這樣呼叫，
就會失敗並出現「could not determine which collation to use for string
comparison」的錯誤。您必須改為
使用 `DirectFunctionCall2Coll(text_starts_with, ...)`，
並提供所需要的定序，這通常就是直接從
`PG_GET_COLLATION()` 傳入，如下面的範例所示。

`fmgr.h` 也提供了一些巨集，方便在
C 型別與 `Datum` 之間轉換。舉例來說，若要
將 `Datum` 轉換為 `text*`，您可以
使用 `DatumGetTextPP(X)`。雖然有些型別具有名為
`TypeGetDatum(X)` 這類的巨集，可用於反向
轉換，但 `text*` 並沒有；直接使用
通用巨集 `PointerGetDatum(X)` 即可。
若您的擴充功能定義了額外的型別，通常也很方便
為您的型別定義類似的巨集。

以下是一些使用版本 1 呼叫慣例的範例：

```

#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"
#include "varatt.h"

PG_MODULE_MAGIC;

/* by value */

PG_FUNCTION_INFO_V1(add_one);

Datum
add_one(PG_FUNCTION_ARGS)
{
    int32   arg = PG_GETARG_INT32(0);

    PG_RETURN_INT32(arg + 1);
}

/* by reference, fixed length */

PG_FUNCTION_INFO_V1(add_one_float8);

Datum
add_one_float8(PG_FUNCTION_ARGS)
{
    /* The macros for FLOAT8 hide its pass-by-reference nature. */
    float8   arg = PG_GETARG_FLOAT8(0);

    PG_RETURN_FLOAT8(arg + 1.0);
}

PG_FUNCTION_INFO_V1(makepoint);

Datum
makepoint(PG_FUNCTION_ARGS)
{
    /* Here, the pass-by-reference nature of Point is not hidden. */
    Point     *pointx = PG_GETARG_POINT_P(0);
    Point     *pointy = PG_GETARG_POINT_P(1);
    Point     *new_point = (Point *) palloc(sizeof(Point));

    new_point->x = pointx->x;
    new_point->y = pointy->y;

    PG_RETURN_POINT_P(new_point);
}

/* by reference, variable length */

PG_FUNCTION_INFO_V1(copytext);

Datum
copytext(PG_FUNCTION_ARGS)
{
    text     *t = PG_GETARG_TEXT_PP(0);

    /*
     * VARSIZE_ANY_EXHDR is the size of the struct in bytes, minus the
     * VARHDRSZ or VARHDRSZ_SHORT of its header.  Construct the copy with a
     * full-length header.
     */
    text     *new_t = (text *) palloc(VARSIZE_ANY_EXHDR(t) + VARHDRSZ);
    SET_VARSIZE(new_t, VARSIZE_ANY_EXHDR(t) + VARHDRSZ);

    /*
     * VARDATA is a pointer to the data region of the new struct.  The source
     * could be a short datum, so retrieve its data through VARDATA_ANY.
     */
    memcpy(VARDATA(new_t),          /* destination */
           VARDATA_ANY(t),          /* source */
           VARSIZE_ANY_EXHDR(t));   /* how many bytes */
    PG_RETURN_TEXT_P(new_t);
}

PG_FUNCTION_INFO_V1(concat_text);

Datum
concat_text(PG_FUNCTION_ARGS)
{
    text  *arg1 = PG_GETARG_TEXT_PP(0);
    text  *arg2 = PG_GETARG_TEXT_PP(1);
    int32 arg1_size = VARSIZE_ANY_EXHDR(arg1);
    int32 arg2_size = VARSIZE_ANY_EXHDR(arg2);
    int32 new_text_size = arg1_size + arg2_size + VARHDRSZ;
    text *new_text = (text *) palloc(new_text_size);

    SET_VARSIZE(new_text, new_text_size);
    memcpy(VARDATA(new_text), VARDATA_ANY(arg1), arg1_size);
    memcpy(VARDATA(new_text) + arg1_size, VARDATA_ANY(arg2), arg2_size);
    PG_RETURN_TEXT_P(new_text);
}

/* A wrapper around starts_with(text, text) */

PG_FUNCTION_INFO_V1(t_starts_with);

Datum
t_starts_with(PG_FUNCTION_ARGS)
{
    text       *t1 = PG_GETARG_TEXT_PP(0);
    text       *t2 = PG_GETARG_TEXT_PP(1);
    Oid         collid = PG_GET_COLLATION();
    bool        result;

    result = DatumGetBool(DirectFunctionCall2Coll(text_starts_with,
                                                  collid,
                                                  PointerGetDatum(t1),
                                                  PointerGetDatum(t2)));
    PG_RETURN_BOOL(result);
}
```

假設上述程式碼已準備在
`funcs.c` 檔案中，並編譯成共享物件，
我們就可以用類似這樣的指令，向 PostgreSQL
定義這些函式：

```

CREATE FUNCTION add_one(integer) RETURNS integer
     AS 'DIRECTORY/funcs', 'add_one'
     LANGUAGE C STRICT;

-- note overloading of SQL function name "add_one"
CREATE FUNCTION add_one(double precision) RETURNS double precision
     AS 'DIRECTORY/funcs', 'add_one_float8'
     LANGUAGE C STRICT;

CREATE FUNCTION makepoint(point, point) RETURNS point
     AS 'DIRECTORY/funcs', 'makepoint'
     LANGUAGE C STRICT;

CREATE FUNCTION copytext(text) RETURNS text
     AS 'DIRECTORY/funcs', 'copytext'
     LANGUAGE C STRICT;

CREATE FUNCTION concat_text(text, text) RETURNS text
     AS 'DIRECTORY/funcs', 'concat_text'
     LANGUAGE C STRICT;

CREATE FUNCTION t_starts_with(text, text) RETURNS boolean
     AS 'DIRECTORY/funcs', 't_starts_with'
     LANGUAGE C STRICT;
```

這裡的 *`DIRECTORY`* 代表
共享函式庫檔案所在的目錄（舉例來說，
PostgreSQL 教學目錄，其中
包含本節範例所使用的程式碼）。
（比較好的寫法是，在將
*`DIRECTORY`* 加入搜尋路徑之後，在
`AS` 子句中只使用 `'funcs'`。無論
如何，我們都可以省略共享函式庫特定於系統的副檔名，
通常是 `.so`。）

請注意，我們已將這些函式指定為「strict」，
意思是
系統應該自動假設，若任何輸入值為 null，
結果就是 null。這樣一來，我們就不需要在函式程式碼中
檢查空值輸入了。若不這樣做，我們就必須
明確地使用 `PG_ARGISNULL()` 檢查空值。

巨集 `PG_ARGISNULL(n)`
可以讓函式測試每個輸入是否為 null。（當然，這樣做
只有在函式未被宣告為「strict」時才有必要。）
與
`PG_GETARG_xxx()` 巨集一樣，
輸入引數也是從零開始計算的。請注意，
在確認引數不是 null 之前，
應避免執行
`PG_GETARG_xxx()`。
若要傳回 null 結果，請執行 `PG_RETURN_NULL()`；
這在嚴格與非嚴格函式中都可以運作。

乍看之下，相較於使用一般的 `C` 呼叫慣例，
版本 1 的撰碼慣例，可能顯得只是毫無意義的
晦澀難懂。然而，它們確實讓
我們能夠處理可為 `NULL` 的引數／傳回值，
以及「toasted」（壓縮或外部儲存）的值。

版本 1 介面所提供的其他選項，還有
`PG_GETARG_xxx()`
巨集的兩種變體。其中第一種，
`PG_GETARG_xxx_COPY()`，
保證會傳回指定引數的一份副本，該副本
可以安全地寫入。（一般的巨集，有時會傳回一個
指向實際儲存於資料表中之值的指標，
這是不可以被寫入的。使用
`PG_GETARG_xxx_COPY()`
巨集，則能保證傳回的結果是可寫入的。）
第二種變體則是
`PG_GETARG_xxx_SLICE()`
巨集，它接受三個引數。第一個是
函式引數的編號（如上所述）。第二個與第三個，
是要傳回之片段的偏移量與長度。偏移量從
零開始計算，長度為負值則表示要求傳回
剩餘的值。在儲存型別為「external」的情況下，
這些巨集提供了更有效率的方式，來存取
大型值的一部分。（欄位的儲存型別，可以使用
`ALTER TABLE tablename ALTER
COLUMN colname SET STORAGE
storagetype` 來指定。*`storagetype`* 可以是
`plain`、`external`、`extended`
或 `main` 其中之一。）

最後，版本 1 的函式呼叫慣例，讓
傳回集合結果（[36.10.9 節](xfunc-c.md#XFUNC-C-RETURN-SET)）、
實作觸發程序函式（[第 37 章](../triggers/README.md)），以及
程序語言呼叫處理常式（[第 57 章](../../internals/plhandler/README.md)）都成為可能。詳情
請參閱原始碼發行套件中的
`src/backend/utils/fmgr/README`。

<a id="XFUNC-C-CODE"></a>

### 36.10.4. 撰寫程式碼 [#](#XFUNC-C-CODE)

在進入更進階的主題之前，我們應該先討論一些
PostgreSQL C 語言函式的撰寫程式碼
規則。雖然要將以 C 以外語言撰寫的函式
載入 PostgreSQL 或許是可行的，
但這通常相當困難（如果真的可行的話），因為
C++、FORTRAN 或 Pascal 等其他語言，往往
不遵循與 C 相同的呼叫慣例。也就是說，
其他語言在函式之間傳遞引數
與傳回值的方式並不相同。基於這個
原因，我們會假設您的 C 語言函式，
確實是以 C 撰寫的。

撰寫與建置 C 函式的基本規則如下：

* 使用 `pg_config
  --includedir-server`<a id="id-1.8.3.13.8.3.1.1.1.2"></a>
  來找出您系統（或您使用者實際執行的系統）上，
  PostgreSQL 伺服器標頭
  檔的安裝位置。
* 編譯並連結您的程式碼，使其可以動態
  載入 PostgreSQL 中，永遠
  需要特殊的旗標。關於如何在您特定的
  作業系統上完成這項工作，詳細說明請參閱[36.10.5 節](xfunc-c.md#DFUNC)。
* 請記得為您的共享函式庫定義一個「魔術區塊」，
  如[36.10.1 節](xfunc-c.md#XFUNC-C-DYNLOAD)所述。
* 配置記憶體時，請使用
  PostgreSQL 的函式
  `palloc`<a id="id-1.8.3.13.8.3.1.4.1.3"></a> 與 `pfree`<a id="id-1.8.3.13.8.3.1.4.1.5"></a>，
  而不要使用對應的 C 函式庫函式
  `malloc` 與 `free`。
  由 `palloc` 所配置的記憶體，
  會在每個交易結束時自動釋放，以避免
  記憶體洩漏。
* 請務必使用 `memset` 將您結構的位元組全部清零
  （或者一開始就用 `palloc0` 來配置它們）。
  即使您為結構的每個欄位都賦值，
  結構中仍可能存在對齊填補（結構中的空隙），
  裡面含有垃圾值。若不這樣做，將難以
  支援雜湊索引或雜湊連接，因為您必須挑出
  資料結構中真正有意義的位元，才能計算出雜湊值。
  規劃器有時也會依賴以位元方式比較常數
  是否相等，因此若邏輯上相等的值在位元層級
  不相等，可能會得到不理想的規劃結果。
* 大多數 PostgreSQL 內部
  型別都宣告於 `postgres.h` 中，而
  函式管理員介面
  （`PG_FUNCTION_ARGS` 等）則位於
  `fmgr.h` 中，因此您至少需要納入
  這兩個檔案。基於可攜性的考量，最好
  將 `postgres.h` 放在*最前面*納入，
  優先於任何其他系統或使用者標頭檔。納入
  `postgres.h` 也會一併為您納入
  `elog.h` 與 `palloc.h`。
* 物件檔案中所定義的符號名稱，彼此之間，
  以及與 PostgreSQL 伺服器
  可執行檔中所定義的符號之間，都不得衝突。若您
  收到這方面的錯誤訊息，就必須重新命名您的
  函式或變數。

<a id="DFUNC"></a>

### 36.10.5. 編譯與連結動態載入的函式 [#](#DFUNC)

在您能夠使用以
C 撰寫的 PostgreSQL 擴充功能函式之前，
必須以特殊的方式編譯並連結它們，才能產生一個
可由伺服器動態載入的檔案。更精確地說，
需要建立一個*共享函式庫*。<a id="id-1.8.3.13.9.2.3"></a>

關於本節未涵蓋的資訊，
您應該閱讀您作業系統的說明文件，
特別是 C 編譯器 `cc`，以及連結編輯器
`ld` 的操作手冊頁面。
此外，PostgreSQL 原始碼中，
`contrib` 目錄還包含了幾個可運作的範例。
不過，若您依賴這些範例，會讓您的模組
依賴於是否能取得 PostgreSQL 原始碼。

建立共享函式庫，大致類似於連結
可執行檔：首先將原始碼檔案編譯成物件檔案，
然後再將這些物件檔案連結在一起。這些物件檔案必須
被建立為*位置無關程式碼*
（position-independent code，PIC）<a id="id-1.8.3.13.9.4.3"></a>，
概念上這表示，當它們被可執行檔載入時，
可以放置在記憶體中的任意位置。（用於可執行檔的物件檔案，
通常不會以這種方式編譯。）用來連結共享函式庫
的指令，含有特殊的旗標，
以與連結可執行檔區別（至少在理論上是如此
——在某些系統上，實際做法遠比這醜陋許多）。

在以下範例中，我們假設您的原始碼位於
`foo.c` 檔案中，我們將會建立一個共享函式庫
`foo.so`。除非另有說明，
中介物件檔案將被稱為 `foo.o`。共享
函式庫可以包含一個以上的物件檔案，但我們在這裡只使用
一個。

FreeBSD <a id="id-1.8.3.13.9.6.1.1.2"></a>
:   用來建立 PIC 的編譯器旗標
    是 `-fPIC`。要建立共享函式庫，編譯器
    旗標則是 `-shared`。

    ```

    cc -fPIC -c foo.c
    cc -shared -o foo.so foo.o
    ```

    自 FreeBSD 13.0
    版起皆適用，較舊的版本則是使用
    `gcc` 編譯器。

Linux <a id="id-1.8.3.13.9.6.2.1.2"></a>
:   用來建立 PIC 的編譯器旗標
    是 `-fPIC`。
    用來建立共享函式庫的編譯器旗標
    是 `-shared`。一個完整的範例如下：

    ```

    cc -fPIC -c foo.c
    cc -shared -o foo.so foo.o
    ```

macOS <a id="id-1.8.3.13.9.6.3.1.2"></a>
:   以下是一個範例。這假設已安裝了開發工具。

    ```

    cc -c foo.c
    cc -bundle -flat_namespace -undefined suppress -o foo.so foo.o
    ```

NetBSD <a id="id-1.8.3.13.9.6.4.1.2"></a>
:   用來建立 PIC 的編譯器旗標
    是 `-fPIC`。對於 ELF 系統，
    連結共享函式庫時，會使用帶有 `-shared` 旗標的
    編譯器。在較舊的非 ELF 系統上，則會使用 `ld
    -Bshareable`。

    ```

    gcc -fPIC -c foo.c
    gcc -shared -o foo.so foo.o
    ```

OpenBSD <a id="id-1.8.3.13.9.6.5.1.2"></a>
:   用來建立 PIC 的編譯器旗標
    是 `-fPIC`。連結共享函式庫時，
    會使用 `ld -Bshareable`。

    ```

    gcc -fPIC -c foo.c
    ld -Bshareable -o foo.so foo.o
    ```

Solaris <a id="id-1.8.3.13.9.6.6.1.2"></a>
:   用來建立 PIC 的編譯器旗標，在 Sun
    編譯器中是 `-KPIC`，在 GCC 中則是
    `-fPIC`。要
    連結共享函式庫，這兩種編譯器的編譯器選項都可以是
    `-G`，若使用 GCC，則也可以
    改用 `-shared`。

    ```

    cc -KPIC -c foo.c
    cc -G -o foo.so foo.o
    ```

    或者

    ```

    gcc -fPIC -c foo.c
    gcc -G -o foo.so foo.o
    ```

### 提示

若您覺得這太複雜，可以考慮使用
[GNU Libtool](https://www.gnu.org/software/libtool/)，
它會將平台之間的差異隱藏在一個統一的介面之後。

產生的共享函式庫檔案，接著就可以被載入
PostgreSQL 中。在向 `CREATE FUNCTION`
指令指定檔案名稱時，必須給出共享函式庫檔案的名稱，
而不是中介物件檔案的名稱。
請注意，系統標準的共享函式庫副檔名（通常是
`.so` 或 `.sl`），可以在
`CREATE FUNCTION` 指令中省略，而且為了
達到最佳的可攜性，通常也應該省略。

關於伺服器預期在哪裡找到共享函式庫檔案，
請回頭參閱[36.10.1 節](xfunc-c.md#XFUNC-C-DYNLOAD)。

<a id="XFUNC-API-ABI-STABILITY-GUIDANCE"></a>

### 36.10.6. 伺服器 API 與 ABI 穩定性指引 [#](#XFUNC-API-ABI-STABILITY-GUIDANCE)

本節針對擴充功能與其他伺服器外掛程式的作者，
提供了關於
PostgreSQL 伺服器 API 與 ABI 穩定性的
指引。

<a id="XFUNC-GUIDANCE-GENERAL"></a>

#### 36.10.6.1. 概述 [#](#XFUNC-GUIDANCE-GENERAL)

PostgreSQL 伺服器針對伺服器外掛程式，
提供了幾個界線清楚的 API，例如函式管理員
（fmgr，本章已有說明）、
SPI（[第 45 章](../spi/README.md)），以及各種
專為擴充功能設計的掛鉤（hook）。這些介面經過
細心管理，以確保長期的穩定性與相容性。不過，
伺服器中整組全域函式與變數，實際上
構成了可公開使用的 API，而其中大部分
在設計時，並未考量到擴充性與長期
穩定性。

因此，雖然利用這些介面是合理的做法，但
偏離這條廣為採用的成熟路徑越遠，就越有可能
在某個時候遇到 API 或 ABI 相容性問題。
鼓勵擴充功能的作者提供關於其需求的
意見回饋，如此一來，隨著時間推移，
當出現新的使用模式時，某些介面就能被視為更加穩定，
或者可以加入新的、設計更完善的
介面。

<a id="XFUNC-GUIDANCE-API-COMPATIBILITY"></a>

#### 36.10.6.2. API 相容性 [#](#XFUNC-GUIDANCE-API-COMPATIBILITY)

API，也就是應用程式設計介面（application programming interface），
是在編譯時期所使用的介面。

<a id="XFUNC-GUIDANCE-API-MAJOR-VERSIONS"></a>

##### 36.10.6.2.1. 主要版本 [#](#XFUNC-GUIDANCE-API-MAJOR-VERSIONS)

PostgreSQL 主要版本之間，*並不*保證
API 的相容性。因此，擴充功能的程式碼
可能需要修改原始碼，才能在多個主要
版本上運作。這通常可以透過前置處理器條件式
來處理，例如 `#if PG_VERSION_NUM >= 160000`。
使用超出界定清楚介面範圍的複雜擴充功能，
通常每個主要伺服器版本都需要進行一些這類的
變更。

<a id="XFUNC-GUIDANCE-API-MNINOR-VERSIONS"></a>

##### 36.10.6.2.2. 次要版本 [#](#XFUNC-GUIDANCE-API-MNINOR-VERSIONS)

PostgreSQL 會努力避免在次要
發行版中破壞伺服器 API。一般而言，在某個次要
發行版中可以編譯並運作的擴充功能程式碼，也應該
能在同一個主要版本的任何其他次要發行版中（不論是
較舊或較新的）順利編譯並運作。

當*確實*需要變更時，系統會審慎
管理這項變更，並將擴充功能的需求納入考量。這類
變更會在發行說明（[附錄 E](../../appendixes/release/README.md)）中說明。

<a id="XFUNC-GUIDANCE-ABI-COMPATIBILITY"></a>

#### 36.10.6.3. ABI 相容性 [#](#XFUNC-GUIDANCE-ABI-COMPATIBILITY)

ABI，也就是應用程式二進位介面（application binary interface），
是在執行時期所使用的介面。

<a id="XFUNC-GUIDANCE-ABI-MAJOR-VERSIONS"></a>

##### 36.10.6.3.1. 主要版本 [#](#XFUNC-GUIDANCE-ABI-MAJOR-VERSIONS)

不同主要版本的伺服器，其 ABI 刻意設計為不相容。
因此，使用伺服器 API 的擴充功能，必須
針對每個主要發行版重新編譯。納入
`PG_MODULE_MAGIC`
（請參閱[36.10.1 節](xfunc-c.md#XFUNC-C-DYNLOAD)），可以確保為
某個主要版本所編譯的程式碼，會被其他主要版本
拒絕。

<a id="XFUNC-GUIDANCE-ABI-MNINOR-VERSIONS"></a>

##### 36.10.6.3.2. 次要版本 [#](#XFUNC-GUIDANCE-ABI-MNINOR-VERSIONS)

PostgreSQL 會努力避免在次要
發行版中破壞伺服器 ABI。一般而言，針對某個次要
發行版所編譯的擴充功能，應該能在同一個主要版本的
任何其他次要發行版（不論是較舊或較新的）上運作。

當*確實*需要變更時，
PostgreSQL 會選擇可能造成最小影響的
變更方式，舉例來說，將新欄位塞入填補
空間，或將其附加到結構的末端。這類
變更通常不會影響擴充功能，除非它們使用了
相當不尋常的程式碼模式。

然而，在極少數情況下，即使是這種非侵入性的
變更也可能不切實際或無法實現。若發生這種情況，
系統會審慎管理這項變更，並將擴充功能的需求
納入考量。這類變更同樣會記載於發行說明
（[附錄 E](../../appendixes/release/README.md)）中。

不過請注意，伺服器的許多部分，
在設計或維護時，並未將其視為可公開使用的
API（而且在大多數情況下，實際的界線
也並不明確）。若出現緊急需求，
這些部分的變更，自然會比在定義明確
且廣泛使用的介面中所做的變更，較少考量到
擴充功能的程式碼。

此外，由於缺乏對此類變更的自動偵測機制，這並
不是一項保證，但就歷史經驗而言，這類破壞性
變更極為罕見。

<a id="XFUNC-C-COMPOSITE-TYPE-ARGS"></a>

### 36.10.7. 複合型別引數 [#](#XFUNC-C-COMPOSITE-TYPE-ARGS)

複合型別並不像 C 結構那樣具有固定的配置方式。
複合型別的實例，可以含有空值（null）欄位。此外，
屬於繼承階層一部分的複合型別，
可能會與同一個繼承階層中的其他成員
具有不同的欄位。因此，
PostgreSQL 提供了一組函式
介面，讓您能從 C 中存取複合型別的欄位。

假設我們想要撰寫一個函式，來回答以下查詢：

```

SELECT name, c_overpaid(emp, 1500) AS overpaid
    FROM emp
    WHERE name = 'Bill' OR name = 'Sam';
```

使用版本 1 呼叫慣例，我們可以將
`c_overpaid` 定義為：

```

#include "postgres.h"
#include "executor/executor.h"  /* for GetAttributeByName() */

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(c_overpaid);

Datum
c_overpaid(PG_FUNCTION_ARGS)
{
    HeapTupleHeader  t = PG_GETARG_HEAPTUPLEHEADER(0);
    int32            limit = PG_GETARG_INT32(1);
    bool isnull;
    Datum salary;

    salary = GetAttributeByName(t, "salary", &isnull);
    if (isnull)
        PG_RETURN_BOOL(false);
    /* Alternatively, we might prefer to do PG_RETURN_NULL() for null salary. */

    PG_RETURN_BOOL(DatumGetInt32(salary) > limit);
}
```

`GetAttributeByName` 是
PostgreSQL 的系統函式，
用來從指定的資料列中傳回屬性。它有
三個引數：傳入此函式之
`HeapTupleHeader` 型別的引數、所需要之屬性的名稱，
以及一個用來表示該屬性
是否為 null 的傳回參數。`GetAttributeByName` 會傳回一個
`Datum` 值，您可以使用適當的
`DatumGetXXX()`
函式，將其轉換為正確的資料型別。請注意，
若已設定 null 旗標，傳回值就毫無意義；在嘗試對結果
進行任何操作之前，請務必先檢查 null 旗標。

此外還有 `GetAttributeByNum`，它是依欄位編號、
而不是依名稱來選取目標屬性。

以下指令會在 SQL 中宣告
`c_overpaid` 函式：

```

CREATE FUNCTION c_overpaid(emp, integer) RETURNS boolean
    AS 'DIRECTORY/funcs', 'c_overpaid'
    LANGUAGE C STRICT;
```

請注意，我們使用了 `STRICT`，因此不需要
檢查輸入引數是否為 NULL。

<a id="XFUNC-C-RETURNING-ROWS"></a>

### 36.10.8. 傳回資料列（複合型別） [#](#XFUNC-C-RETURNING-ROWS)

要從 C 語言函式傳回資料列或複合型別的值，
您可以使用一組特殊的 API，其中提供了巨集與
函式，可以隱藏建構複合
資料型別時大部分的複雜性。要使用此 API，
原始碼檔案必須納入：

```

#include "funcapi.h"
```

有兩種方式可以建構一個複合資料值（以下
簡稱「tuple」）：您可以從一個 Datum 值陣列來
建構它，或者從一個可傳遞給該 tuple 各欄位資料型別
輸入轉換函式的 C 字串陣列來建構它。無論
哪一種方式，您都必須先取得或建構此 tuple 結構的
`TupleDesc` 描述元。若使用 Datum 來處理，
您要將 `TupleDesc` 傳給 `BlessTupleDesc`，
然後為每一列呼叫 `heap_form_tuple`。若使用 C 字串
來處理，您要將 `TupleDesc` 傳給
`TupleDescGetAttInMetadata`，然後為每一列呼叫
`BuildTupleFromCStrings`。對於傳回一組
tuple 的函式，所有這些設定步驟，都可以在函式第一次
呼叫時就一次完成。

系統提供了幾個輔助函式，用來設定所需要的
`TupleDesc`。在大多數傳回複合值的
函式中，建議的做法是呼叫：

```

TypeFuncClass get_call_result_type(FunctionCallInfo fcinfo,
                                   Oid *resultTypeId,
                                   TupleDesc *resultTupleDesc)
```

並傳入與傳給呼叫函式本身相同的 `fcinfo`
結構。（這當然要求您使用版本 1 的
呼叫慣例。）`resultTypeId` 可以指定
為 `NULL`，或指定為某個本地變數的位址，
以接收此函式結果型別的 OID。`resultTupleDesc`
則應該是某個本地 `TupleDesc` 變數的位址。請
檢查結果是否為 `TYPEFUNC_COMPOSITE`；若是，
則 `resultTupleDesc` 已被填入所需要的
`TupleDesc`。（若不是，您可以回報類似
「function returning record called in context that
cannot accept type record」這樣的錯誤。）

### 提示

`get_call_result_type` 可以解析多型
函式結果的實際型別；因此，它不僅適用於傳回複合型別的
函式，對於傳回純量多型結果的函式也相當有用。
`resultTypeId` 輸出主要用於傳回
多型純量的函式。

### 注意

`get_call_result_type` 有一個姊妹函式
`get_expr_result_type`，可用於解析
以運算式樹表示之函式呼叫的預期輸出型別。這可以在
嘗試從函式本身之外判斷結果型別時使用。此外還有
`get_func_result_type`，可在只有
函式 OID 可用時使用。不過，這些函式都無法
處理宣告為傳回 `record` 的函式，而且
`get_func_result_type` 也無法解析多型
型別，因此您應該優先使用 `get_call_result_type`。

較舊、現已淘汰的取得
`TupleDesc` 的函式有：

```

TupleDesc RelationNameGetTupleDesc(const char *relname)
```

可用來取得某個具名關聯之資料列型別的 `TupleDesc`，
以及：

```

TupleDesc TypeGetTupleDesc(Oid typeoid, List *colaliases)
```

可用來依型別 OID 取得 `TupleDesc`。這可以
用於取得基礎型別或
複合型別的 `TupleDesc`。不過，它無法用於
傳回 `record` 的函式，也無法解析多型
型別。

一旦您取得了 `TupleDesc`，就呼叫：

```

TupleDesc BlessTupleDesc(TupleDesc tupdesc)
```

（若您打算使用 Datum 來處理），或者：

```

AttInMetadata *TupleDescGetAttInMetadata(TupleDesc tupdesc)
```

（若您打算使用 C 字串來處理）。若您正在撰寫
一個傳回集合的函式，可以將這些函式的結果，
儲存在 `FuncCallContext` 結構中——分別
使用 `tuple_desc` 或 `attinmeta`
欄位。

若使用 Datum 來處理，請使用：

```

HeapTuple heap_form_tuple(TupleDesc tupdesc, Datum *values, bool *isnull)
```

以 Datum 形式的使用者資料，建構一個 `HeapTuple`。

若使用 C 字串來處理，請使用：

```

HeapTuple BuildTupleFromCStrings(AttInMetadata *attinmeta, char **values)
```

以 C 字串形式的使用者資料，
建構一個 `HeapTuple`。*`values`* 是一個 C 字串陣列，
傳回資料列的每個屬性各對應一個字串。每個 C 字串，
都應該是該屬性資料型別輸入函式所預期的
形式。若要為某個屬性傳回 null 值，
*`values`* 陣列中對應的指標，
應設定為 `NULL`。對於您要傳回的每一列，
都需要再次呼叫此函式。

一旦您建構了要從函式傳回的 tuple，
就必須將其轉換為 `Datum`。請使用：

```

HeapTupleGetDatum(HeapTuple tuple)
```

將 `HeapTuple` 轉換為有效的 Datum。若您打算只
傳回單一列，這個 `Datum` 可以直接傳回；
或者，在傳回集合的函式中，也可以將其
用作目前的傳回值。

下一節會提供一個範例。

<a id="XFUNC-C-RETURN-SET"></a>

### 36.10.9. 傳回集合 [#](#XFUNC-C-RETURN-SET)

C 語言函式在傳回集合（多筆資料列）時，
有兩種選擇。其中一種方法稱為 *ValuePerCall*
模式，這種傳回集合的函式會被重複呼叫（每次傳入
相同的引數），並在每次呼叫時傳回一筆新的資料列，
直到沒有更多資料列可傳回為止，並透過傳回 NULL
來表示這一點。因此，這種傳回集合的函式（SRF）
必須在多次呼叫之間，保存足夠的狀態，
以記住它上次做到哪裡，並在每次呼叫時傳回正確的
下一個項目。
另一種方法稱為 *Materialize* 模式，
SRF 會填入並傳回一個包含其
全部結果的 tuplestore 物件；然後整個結果只會發生
一次呼叫，也不需要跨呼叫的狀態。

使用 ValuePerCall 模式時，重要的是要記住，
系統並不保證查詢會被執行到完成；
也就是說，由於諸如 `LIMIT` 之類的選項，
執行器可能會在尚未取得所有資料列之前，
就停止呼叫這個傳回集合的函式。這表示
在最後一次呼叫中執行清理動作並不安全，
因為那次呼叫可能根本不會發生。建議
對於需要存取外部資源（例如檔案描述元）的函式，
使用 Materialize 模式。

本節其餘部分，記載了一組常用（但並非
必須使用）於採用 ValuePerCall 模式之 SRF 的輔助
巨集。關於 Materialize 模式的額外詳情，可以在
`src/backend/utils/fmgr/README` 中找到。此外，
PostgreSQL 原始碼發行套件中的
`contrib` 模組，也包含許多同時使用
ValuePerCall 與 Materialize 模式的 SRF 範例。

要使用這裡所描述的 ValuePerCall 支援巨集，
請納入 `funcapi.h`。這些巨集會搭配一個
`FuncCallContext` 結構使用，該結構包含
需要在多次呼叫之間保存的狀態。在
正在被呼叫、傳回集合的 SRF 內部，會使用 `fcinfo->flinfo->fn_extra`
來在多次呼叫之間，保存一個指向
`FuncCallContext` 的指標。這些巨集會在
第一次使用時自動填入該欄位，並且
預期在後續使用時，在該處找到相同的指標。

```

typedef struct FuncCallContext
{
    /*
     * Number of times we've been called before
     *
     * call_cntr is initialized to 0 for you by SRF_FIRSTCALL_INIT(), and
     * incremented for you every time SRF_RETURN_NEXT() is called.
     */
    uint64 call_cntr;

    /*
     * OPTIONAL maximum number of calls
     *
     * max_calls is here for convenience only and setting it is optional.
     * If not set, you must provide alternative means to know when the
     * function is done.
     */
    uint64 max_calls;

    /*
     * OPTIONAL pointer to miscellaneous user-provided context information
     *
     * user_fctx is for use as a pointer to your own data to retain
     * arbitrary context information between calls of your function.
     */
    void *user_fctx;

    /*
     * OPTIONAL pointer to struct containing attribute type input metadata
     *
     * attinmeta is for use when returning tuples (i.e., composite data types)
     * and is not used when returning base data types. It is only needed
     * if you intend to use BuildTupleFromCStrings() to create the return
     * tuple.
     */
    AttInMetadata *attinmeta;

    /*
     * memory context used for structures that must live for multiple calls
     *
     * multi_call_memory_ctx is set by SRF_FIRSTCALL_INIT() for you, and used
     * by SRF_RETURN_DONE() for cleanup. It is the most appropriate memory
     * context for any memory that is to be reused across multiple calls
     * of the SRF.
     */
    MemoryContext multi_call_memory_ctx;

    /*
     * OPTIONAL pointer to struct containing tuple description
     *
     * tuple_desc is for use when returning tuples (i.e., composite data types)
     * and is only needed if you are going to build the tuples with
     * heap_form_tuple() rather than with BuildTupleFromCStrings().  Note that
     * the TupleDesc pointer stored here should usually have been run through
     * BlessTupleDesc() first.
     */
    TupleDesc tuple_desc;

} FuncCallContext;
```

SRF 若使用這套基礎架構，可以使用以下巨集：

```

SRF_IS_FIRSTCALL()
```

用來判斷您的函式是第一次被呼叫，還是後續的
呼叫。（只在）第一次呼叫時，呼叫：

```

SRF_FIRSTCALL_INIT()
```

來初始化 `FuncCallContext`。在每一次函式
呼叫中（包括第一次），都呼叫：

```

SRF_PERCALL_SETUP()
```

以設定好要使用 `FuncCallContext`。

若您的函式在目前這次呼叫中有資料要傳回，請使用：

```

SRF_RETURN_NEXT(funcctx, result)
```

將其傳回給呼叫端。（`result` 必須是
`Datum` 型別，可以是單一值，或是如上所述
準備好的 tuple。）最後，當您的函式已完成
傳回資料時，請使用：

```

SRF_RETURN_DONE(funcctx)
```

來清理並結束此 SRF。

呼叫 SRF 時，目前所在的記憶體上下文
是一個暫時性的上下文，會在每次呼叫之間被清除。這表示
您不需要對每一個以 `palloc` 配置的物件
呼叫 `pfree`；反正它們都會被釋放。
不過，若您想要配置任何需要跨呼叫存活的
資料結構，就需要把它們放到其他地方。
`multi_call_memory_ctx` 所參照的記憶體上下文，
就是任何需要存活到 SRF 執行完畢之資料的
合適位置。在大多數情況下，這表示您應該
在進行第一次呼叫的設定時，切換到
`multi_call_memory_ctx`。
請使用 `funcctx->user_fctx`，來保存一個指向
任何這類跨呼叫資料結構的指標。
（您在 `multi_call_memory_ctx`
中所配置的資料，會在查詢結束時自動
消失，因此也不需要手動釋放
這些資料。）

<a id="XFUNC-C-WARNING-VALUEPERCALL-ARGS"></a>

### 警告

雖然函式的實際引數，在多次呼叫之間
保持不變，但若您在暫時性的上下文中對引數值
去除 toast（這通常是由
`PG_GETARG_xxx` 巨集透明地完成的），
則去除 toast 後的副本，會在每個循環中被釋放。
因此，若您在 `user_fctx` 中保留了對這類值的
參照，就必須在去除 toast 之後，將它們複製到
`multi_call_memory_ctx` 中，或者確保
您只在該上下文中對這些值去除 toast。

一個完整的偽程式碼範例如下：

```

Datum
my_set_returning_function(PG_FUNCTION_ARGS)
{
    FuncCallContext  *funcctx;
    Datum             result;
    further declarations as needed

    if (SRF_IS_FIRSTCALL())
    {
        MemoryContext oldcontext;

        funcctx = SRF_FIRSTCALL_INIT();
        oldcontext = MemoryContextSwitchTo(funcctx->multi_call_memory_ctx);
        /* One-time setup code appears here: */
        user code
        if returning composite
            build TupleDesc, and perhaps AttInMetadata
        endif returning composite
        user code
        MemoryContextSwitchTo(oldcontext);
    }

    /* Each-time setup code appears here: */
    user code
    funcctx = SRF_PERCALL_SETUP();
    user code

    /* this is just one way we might test whether we are done: */
    if (funcctx->call_cntr < funcctx->max_calls)
    {
        /* Here we want to return another item: */
        user code
        obtain result Datum
        SRF_RETURN_NEXT(funcctx, result);
    }
    else
    {
        /* Here we are done returning items, so just report that fact. */
        /* (Resist the temptation to put cleanup code here.) */
        SRF_RETURN_DONE(funcctx);
    }
}
```

一個傳回複合型別之簡單 SRF 的完整範例，
如下所示：

```

PG_FUNCTION_INFO_V1(retcomposite);

Datum
retcomposite(PG_FUNCTION_ARGS)
{
    FuncCallContext     *funcctx;
    int                  call_cntr;
    int                  max_calls;
    TupleDesc            tupdesc;
    AttInMetadata       *attinmeta;

    /* stuff done only on the first call of the function */
    if (SRF_IS_FIRSTCALL())
    {
        MemoryContext   oldcontext;

        /* create a function context for cross-call persistence */
        funcctx = SRF_FIRSTCALL_INIT();

        /* switch to memory context appropriate for multiple function calls */
        oldcontext = MemoryContextSwitchTo(funcctx->multi_call_memory_ctx);

        /* total number of tuples to be returned */
        funcctx->max_calls = PG_GETARG_INT32(0);

        /* Build a tuple descriptor for our result type */
        if (get_call_result_type(fcinfo, NULL, &tupdesc) != TYPEFUNC_COMPOSITE)
            ereport(ERROR,
                    (errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
                     errmsg("function returning record called in context "
                            "that cannot accept type record")));

        /*
         * generate attribute metadata needed later to produce tuples from raw
         * C strings
         */
        attinmeta = TupleDescGetAttInMetadata(tupdesc);
        funcctx->attinmeta = attinmeta;

        MemoryContextSwitchTo(oldcontext);
    }

    /* stuff done on every call of the function */
    funcctx = SRF_PERCALL_SETUP();

    call_cntr = funcctx->call_cntr;
    max_calls = funcctx->max_calls;
    attinmeta = funcctx->attinmeta;

    if (call_cntr < max_calls)    /* do when there is more left to send */
    {
        char       **values;
        HeapTuple    tuple;
        Datum        result;

        /*
         * Prepare a values array for building the returned tuple.
         * This should be an array of C strings which will
         * be processed later by the type input functions.
         */
        values = (char **) palloc(3 * sizeof(char *));
        values[0] = (char *) palloc(16 * sizeof(char));
        values[1] = (char *) palloc(16 * sizeof(char));
        values[2] = (char *) palloc(16 * sizeof(char));

        snprintf(values[0], 16, "%d", 1 * PG_GETARG_INT32(1));
        snprintf(values[1], 16, "%d", 2 * PG_GETARG_INT32(1));
        snprintf(values[2], 16, "%d", 3 * PG_GETARG_INT32(1));

        /* build a tuple */
        tuple = BuildTupleFromCStrings(attinmeta, values);

        /* make the tuple into a datum */
        result = HeapTupleGetDatum(tuple);

        /* clean up (this is not really necessary) */
        pfree(values[0]);
        pfree(values[1]);
        pfree(values[2]);
        pfree(values);

        SRF_RETURN_NEXT(funcctx, result);
    }
    else    /* do when there is no more left */
    {
        SRF_RETURN_DONE(funcctx);
    }
}
```

其中一種在 SQL 中宣告此函式的方式是：

```

CREATE TYPE __retcomposite AS (f1 integer, f2 integer, f3 integer);

CREATE OR REPLACE FUNCTION retcomposite(integer, integer)
    RETURNS SETOF __retcomposite
    AS 'filename', 'retcomposite'
    LANGUAGE C IMMUTABLE STRICT;
```

另一種方式，則是使用 OUT 參數：

```

CREATE OR REPLACE FUNCTION retcomposite(IN integer, IN integer,
    OUT f1 integer, OUT f2 integer, OUT f3 integer)
    RETURNS SETOF record
    AS 'filename', 'retcomposite'
    LANGUAGE C IMMUTABLE STRICT;
```

請注意，在這種方式中，此函式的輸出型別，
形式上是一個匿名的 `record` 型別。

<a id="XFUNC-C-POLYMORPHIC"></a>

### 36.10.10. 多型引數與傳回型別 [#](#XFUNC-C-POLYMORPHIC)

C 語言函式可以被宣告為接受並
傳回[36.2.5 節](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)中所述的多型型別。
當某個函式的引數或傳回型別
被定義為多型型別時，函式的作者無法
事先知道它會被以哪種資料型別呼叫，或
需要傳回哪種資料型別。`fmgr.h` 中提供了兩個
常式，讓版本 1 的 C 函式能夠找出其引數
的實際資料型別，以及預期要傳回的型別。這些常式
分別是 `get_fn_expr_rettype(FmgrInfo *flinfo)` 與
`get_fn_expr_argtype(FmgrInfo *flinfo, int argnum)`。
它們會傳回結果或引數型別的 OID，若無法取得該
資訊，則傳回 `InvalidOid`。
`flinfo` 結構通常是透過
`fcinfo->flinfo` 來存取。參數 `argnum`
是從零開始計算的。也可以使用
`get_call_result_type` 作為 `get_fn_expr_rettype`
的替代方案。
此外還有 `get_fn_expr_variadic`，可用來
判斷可變參數的引數是否已被合併為一個陣列。
這主要用於 `VARIADIC "any"` 函式，
因為對於採用一般陣列型別的可變參數函式而言，
這種合併永遠都會發生。

舉例來說，假設我們想撰寫一個函式，接受任意
型別的單一元素，並傳回該型別的一維陣列：

```

PG_FUNCTION_INFO_V1(make_array);
Datum
make_array(PG_FUNCTION_ARGS)
{
    ArrayType  *result;
    Oid         element_type = get_fn_expr_argtype(fcinfo->flinfo, 0);
    Datum       element;
    bool        isnull;
    int16       typlen;
    bool        typbyval;
    char        typalign;
    int         ndims;
    int         dims[MAXDIM];
    int         lbs[MAXDIM];

    if (!OidIsValid(element_type))
        elog(ERROR, "could not determine data type of input");

    /* get the provided element, being careful in case it's NULL */
    isnull = PG_ARGISNULL(0);
    if (isnull)
        element = (Datum) 0;
    else
        element = PG_GETARG_DATUM(0);

    /* we have one dimension */
    ndims = 1;
    /* and one element */
    dims[0] = 1;
    /* and lower bound is 1 */
    lbs[0] = 1;

    /* get required info about the element type */
    get_typlenbyvalalign(element_type, &typlen, &typbyval, &typalign);

    /* now build the array */
    result = construct_md_array(&element, &isnull, ndims, dims, lbs,
                                element_type, typlen, typbyval, typalign);

    PG_RETURN_ARRAYTYPE_P(result);
}
```

以下指令會在 SQL 中宣告
`make_array` 函式：

```

CREATE FUNCTION make_array(anyelement) RETURNS anyarray
    AS 'DIRECTORY/funcs', 'make_array'
    LANGUAGE C IMMUTABLE;
```

有一種多型的變體，只有 C 語言函式才能使用：
它們可以被宣告為接受
`"any"` 型別的參數。（請注意，這個型別名稱
必須加上雙引號，因為它同時也是 SQL 的保留字。）
這與 `anyelement` 類似，差別在於它並不要求
不同的 `"any"` 引數必須屬於相同型別，
它們也無助於判斷函式的結果型別。C 語言函式
也可以將其最後一個參數宣告為
`VARIADIC "any"`。這會比對一個或多個任意型別
（不一定是相同型別）的實際引數。這些引數
*不會*像一般可變參數函式那樣被收集到一個陣列
中；它們只會分別被傳遞給
函式。使用這項功能時，必須使用
`PG_NARGS()` 巨集以及上述方法，
來判斷實際引數的數量及其型別。此外，這類
函式的使用者，可能會希望在其函式呼叫中使用
`VARIADIC` 關鍵字，並期望此函式會將
陣列元素當作各自獨立的引數來處理。若想要這種行為，
函式本身就必須在使用 `get_fn_expr_variadic` 偵測到
實際引數已被標記為 `VARIADIC` 之後，實作
這項行為。

<a id="XFUNC-SHARED-ADDIN"></a>

### 36.10.11. 共享記憶體 [#](#XFUNC-SHARED-ADDIN)

<a id="XFUNC-SHARED-ADDIN-AT-STARTUP"></a>

#### 36.10.11.1. 在啟動時要求共享記憶體 [#](#XFUNC-SHARED-ADDIN-AT-STARTUP)

附加元件（add-in）可以在伺服器啟動時保留共享記憶體。要做到
這一點，該附加元件的共享函式庫，必須透過在
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)<a id="id-1.8.3.13.15.2.2.2"></a>
中指定它來預先載入。
此共享函式庫還應該在其
`_PG_init` 函式中，註冊一個
`shmem_request_hook`。這個
`shmem_request_hook` 可以透過呼叫以下函式，
來保留共享記憶體：

```

void RequestAddinShmemSpace(Size size)
```

每個後端程序，都應該透過呼叫以下函式，
取得指向所保留共享記憶體的指標：

```

void *ShmemInitStruct(const char *name, Size size, bool *foundPtr)
```

若此函式將 `foundPtr` 設為
`false`，呼叫端就應該接著初始化
所保留共享記憶體的內容。若 `foundPtr`
被設為 `true`，就表示這塊共享記憶體
已經由另一個後端程序初始化過了，呼叫端就不需要
進一步初始化。

為了避免競爭情況（race condition），每個後端程序在初始化
其所配置的共享記憶體時，都應該使用 LWLock
`AddinShmemInitLock`，如下所示：

```

static mystruct *ptr = NULL;
bool        found;

LWLockAcquire(AddinShmemInitLock, LW_EXCLUSIVE);
ptr = ShmemInitStruct("my struct name", size, &found);
if (!found)
{
    ... initialize contents of shared memory ...
    ptr->locks = GetNamedLWLockTranche("my tranche name");
}
LWLockRelease(AddinShmemInitLock);
```

`shmem_startup_hook` 為初始化程式碼提供了
一個方便的位置，但並不是嚴格要求所有這類程式碼
都必須放在這個掛鉤中。在 Windows（以及任何其他
有定義 `EXEC_BACKEND` 的環境）上，每個後端程序，
會在附加到共享記憶體之後不久，執行
已註冊的 `shmem_startup_hook`，因此附加元件
仍然應該如上面的範例所示，在這個掛鉤中取得
`AddinShmemInitLock`。在其他平台上，
只有 postmaster 程序會執行
`shmem_startup_hook`，而每個後端程序都會
自動繼承指向共享記憶體的指標。

在 PostgreSQL 原始碼樹中的
`contrib/pg_stat_statements/pg_stat_statements.c`，
可以找到 `shmem_request_hook` 與
`shmem_startup_hook` 的範例。

<a id="XFUNC-SHARED-ADDIN-AFTER-STARTUP"></a>

#### 36.10.11.2. 在啟動之後要求共享記憶體 [#](#XFUNC-SHARED-ADDIN-AFTER-STARTUP)

還有另一種更有彈性的方法，可以在伺服器啟動之後、
且在 `shmem_request_hook` 之外，
保留共享記憶體。要做到這一點，每個要使用
此共享記憶體的後端程序，都應該透過呼叫以下函式，
取得指向它的指標：

```

void *GetNamedDSMSegment(const char *name, size_t size,
                         void (*init_callback) (void *ptr),
                         bool *found)
```

若具有給定名稱的動態共享記憶體區段尚不存在，
此函式將會配置它，並使用所提供的
`init_callback` 回呼函式來初始化它。若此區段
已由另一個後端程序配置並初始化過，此函式
只會將現有的動態共享記憶體區段附加到目前的
後端程序。

與伺服器啟動時所保留的共享記憶體不同，
使用 `GetNamedDSMSegment` 保留共享記憶體時，
不需要取得
`AddinShmemInitLock`，也不需要採取其他動作
來避免競爭情況。這個函式會確保
只有一個後端程序會配置並初始化該
區段，且所有其他後端程序，都會取得指向已完整
配置並初始化之區段的指標。

在 PostgreSQL 原始碼樹中的
`src/test/modules/test_dsm_registry/test_dsm_registry.c`，
可以找到 `GetNamedDSMSegment` 的完整使用
範例。

<a id="XFUNC-ADDIN-LWLOCKS"></a>

### 36.10.12. LWLocks [#](#XFUNC-ADDIN-LWLOCKS)

<a id="XFUNC-ADDIN-LWLOCKS-AT-STARTUP"></a>

#### 36.10.12.1. 在啟動時要求 LWLocks [#](#XFUNC-ADDIN-LWLOCKS-AT-STARTUP)

附加元件可以在伺服器啟動時保留 LWLocks。與
伺服器啟動時保留共享記憶體的方式相同，此附加元件的
共享函式庫，必須透過在
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)<a id="id-1.8.3.13.16.2.2.2"></a>
中指定它來預先載入，
且此共享函式庫，應該在其
`_PG_init` 函式中，註冊一個
`shmem_request_hook`。這個
`shmem_request_hook`，可以透過呼叫以下函式，
來保留 LWLocks：

```

void RequestNamedLWLockTranche(const char *tranche_name, int num_lwlocks)
```

這可以確保有一個包含 `num_lwlocks` 個 LWLocks 的
陣列，可以用名稱 `tranche_name` 來取用。
可以透過呼叫以下函式，
取得指向此陣列的指標：

```

LWLockPadded *GetNamedLWLockTranche(const char *tranche_name)
```

<a id="XFUNC-ADDIN-LWLOCKS-AFTER-STARTUP"></a>

#### 36.10.12.2. 在啟動之後要求 LWLocks [#](#XFUNC-ADDIN-LWLOCKS-AFTER-STARTUP)

還有另一種更有彈性的方法，可以在伺服器啟動之後、
且在 `shmem_request_hook` 之外，
取得 LWLocks。要做到這一點，首先透過呼叫以下函式，
配置一個 `tranche_id`：

```

int LWLockNewTrancheId(void)
```

接著，初始化每一個 LWLock，並傳入新的
`tranche_id` 作為引數：

```

void LWLockInitialize(LWLock *lock, int tranche_id)
```

與共享記憶體類似，每個後端程序都應該確保
只有一個程序配置新的 `tranche_id`，
並初始化每一個新的 LWLock。做到這一點的其中一種方式，
是只在持有排他鎖定的
`AddinShmemInitLock` 情況下，於您的共享記憶體初始化
程式碼中呼叫這些函式。若使用
`GetNamedDSMSegment`，則在
`init_callback` 回呼函式中呼叫這些函式，
就足以避免競爭情況。

最後，每個使用 `tranche_id` 的後端程序，
都應該透過呼叫以下函式，將其與
`tranche_name` 建立關聯：

```

void LWLockRegisterTranche(int tranche_id, const char *tranche_name)
```

在 PostgreSQL 原始碼樹中的
`contrib/pg_prewarm/autoprewarm.c`，
可以找到 `LWLockNewTrancheId`、
`LWLockInitialize` 與
`LWLockRegisterTranche` 的完整使用範例。

<a id="XFUNC-ADDIN-WAIT-EVENTS"></a>

### 36.10.13. 自訂等待事件 [#](#XFUNC-ADDIN-WAIT-EVENTS)

附加元件可以透過呼叫以下函式，
在 `Extension` 這個等待事件類型下，
定義自訂的等待事件：

```

uint32 WaitEventExtensionNew(const char *wait_event_name)
```

此等待事件會與一個提供給使用者查看的自訂字串相關聯。
在 PostgreSQL 原始碼樹的
`src/test/modules/worker_spi` 中，可以找到一個
範例。

可以在
[`pg_stat_activity`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)中，
檢視自訂的等待事件：

```

=# SELECT wait_event_type, wait_event FROM pg_stat_activity
     WHERE backend_type ~ 'worker_spi';
 wait_event_type |  wait_event
-----------------+---------------
 Extension       | WorkerSpiMain
(1 row)
```

<a id="XFUNC-ADDIN-INJECTION-POINTS"></a>

### 36.10.14. 注入點（Injection Points） [#](#XFUNC-ADDIN-INJECTION-POINTS)

具有給定 `name` 的注入點，是使用以下巨集
來宣告的：

```

INJECTION_POINT(name, arg);
```

伺服器程式碼中的幾個關鍵位置，已經宣告了一些
注入點。加入新的注入點之後，必須重新編譯程式碼，
該注入點才能在執行檔中使用。以 C 語言撰寫的
附加元件，可以使用相同的巨集，在自己的程式碼中
宣告注入點。注入點的名稱應使用
小寫字元，各個詞語之間以連字號分隔。
`arg` 是一個選擇性的引數值，會在執行期間
提供給回呼函式。

執行一個注入點，可能需要配置少量的
記憶體，而這可能會失敗。若您需要在不允許
動態配置記憶體的關鍵區段（critical section）中
使用注入點，可以使用以下巨集，
採取兩步驟的做法：

```

INJECTION_POINT_LOAD(name);
INJECTION_POINT_CACHED(name, arg);
```

在進入關鍵區段之前，
呼叫 `INJECTION_POINT_LOAD`。它會檢查共享
記憶體狀態，若該回呼函式為啟用狀態，就將其
載入後端程序私有的記憶體中。在關鍵區段內，
使用 `INJECTION_POINT_CACHED` 來執行此回呼
函式。

附加元件可以透過呼叫以下函式，
將回呼函式附加到某個已宣告的注入點：

```

extern void InjectionPointAttach(const char *name,
                                 const char *library,
                                 const char *function,
                                 const void *private_data,
                                 int private_data_size);
```

`name` 是此注入點的名稱，當執行期間
到達此處時，就會執行從 `library` 載入的
`function`。`private_data`
是一塊私有資料區域，大小為 `private_data_size`，
會在執行時作為引數提供給此回呼函式。

以下是一個
`InjectionPointCallback` 的回呼函式範例：

```

static void
custom_injection_callback(const char *name,
                          const void *private_data,
                          void *arg)
{
    uint32 wait_event_info = WaitEventInjectionPointNew(name);

    pgstat_report_wait_start(wait_event_info);
    elog(NOTICE, "%s: executed custom callback", name);
    pgstat_report_wait_end();
}
```

這個回呼函式會以 `NOTICE` 的嚴重性層級，
在伺服器錯誤記錄檔中印出一則訊息，不過回呼函式
也可以實作更複雜的邏輯。

定義到達注入點時所要採取動作的另一種方式，
是將測試程式碼加入一般的原始碼中。舉例來說，
若這項動作依賴於已載入模組無法存取的
本地變數，這種做法會很有用。接著就可以使用
`IS_INJECTION_POINT_ATTACHED` 巨集，
來檢查是否已附加某個注入點，舉例來說：

```

#ifdef USE_INJECTION_POINTS
if (IS_INJECTION_POINT_ATTACHED("before-foobar"))
{
    /* change a local variable if injection point is attached */
    local_var = 123;

    /* also execute the callback */
    INJECTION_POINT_CACHED("before-foobar", NULL);
}
#endif
```

請注意，`IS_INJECTION_POINT_ATTACHED`
巨集並不會執行附加到該注入點的回呼函式。若您
想要執行此回呼函式，也必須像上述範例那樣，呼叫
`INJECTION_POINT_CACHED`。

您也可以選擇透過呼叫以下函式，
來卸除（detach）某個注入點：

```

extern bool InjectionPointDetach(const char *name);
```

成功時會傳回 `true`，否則
傳回 `false`。

附加到某個注入點的回呼函式，可以在所有
後端程序中使用，包括在呼叫
`InjectionPointAttach` 之後才啟動的後端程序。只要
伺服器持續執行，或直到該注入點使用
`InjectionPointDetach` 卸除為止，它都會保持
附加狀態。

在 PostgreSQL 原始碼樹的
`src/test/modules/injection_points` 中，可以找到
一個範例。

若要啟用注入點，需要在使用 `configure`
時加上 `--enable-injection-points`，
或在使用 Meson 時加上
`-Dinjection_points=true`。

<a id="XFUNC-ADDIN-CUSTOM-CUMULATIVE-STATISTICS"></a>

### 36.10.15. 自訂累計統計資訊 [#](#XFUNC-ADDIN-CUSTOM-CUMULATIVE-STATISTICS)

以 C 語言撰寫的附加元件，可以使用
在[累計統計資訊系統](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-SETUP)中
所註冊的自訂累計統計資訊型別。

首先，定義一個 `PgStat_KindInfo`，其中包含
與所註冊自訂型別相關的所有資訊。舉例來說：

```

static const PgStat_KindInfo custom_stats = {
    .name = "custom_stats",
    .fixed_amount = false,
    .shared_size = sizeof(PgStatShared_Custom),
    .shared_data_off = offsetof(PgStatShared_Custom, stats),
    .shared_data_len = sizeof(((PgStatShared_Custom *) 0)->stats),
    .pending_size = sizeof(PgStat_StatCustomEntry),
}
```

接著，每個需要使用此自訂型別的後端程序，
都需要使用 `pgstat_register_kind`，以及用於儲存
與此統計資訊型別相關項目的唯一 ID，
來進行註冊：

```

extern PgStat_Kind pgstat_register_kind(PgStat_Kind kind,
                                        const PgStat_KindInfo *kind_info);
```

在開發新的擴充功能時，請將
*`kind`* 設為
`PGSTAT_KIND_EXPERIMENTAL`。當您準備好要將此擴充功能
發行給使用者時，請在
[Custom Cumulative Statistics](https://wiki.postgresql.org/wiki/CustomCumulativeStats) 頁面上
保留一個 kind ID。

`PgStat_KindInfo` API 的詳情，可以在
`src/include/utils/pgstat_internal.h` 中找到。

所註冊的統計資訊型別，會與一個名稱，
以及在共享記憶體中、整個伺服器共用的唯一 ID
建立關聯。每個使用自訂統計資訊型別的後端程序，
都會維護一個本地快取，儲存每個自訂
`PgStat_KindInfo` 的資訊。

請將實作此自訂累計統計資訊型別的擴充功能模組，
放入
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)中，
以便在 PostgreSQL 啟動期間，
及早載入它。

在 `src/test/modules/injection_points` 中，
可以找到一個說明如何註冊並使用自訂統計資訊的
範例。

<a id="EXTEND-CPP"></a>

### 36.10.16. 使用 C++ 來擴充功能 [#](#EXTEND-CPP)

<a id="id-1.8.3.13.20.2"></a>

雖然 PostgreSQL 後端是以
C 撰寫的，但若遵循以下指引，仍然可以用 C++
撰寫擴充功能：

* 後端所存取的所有函式，都必須向後端
  提供 C 介面；這些 C 函式接著可以呼叫 C++
  函式。舉例來說，後端所存取的函式，
  需要使用 `extern C` 連結方式。任何
  以指標形式在後端與
  C++ 程式碼之間傳遞的函式，也同樣需要這樣做。
* 請使用適當的釋放方法，來釋放記憶體。舉例來說，
  大多數後端記憶體都是使用 `palloc()` 配置的，因此請使用
  `pfree()` 來釋放它。在這類情況下使用 C++ 的
  `delete`，將會失敗。
* 防止例外狀況擴散到 C 程式碼中（在所有
  `extern C` 函式的最上層，使用一個攔截所有例外的
  區塊）。即使 C++ 程式碼並未明確拋出任何
  例外，這也是必要的，因為記憶體不足之類的事件，
  仍然可能拋出例外。任何例外都必須被攔截，
  並將適當的錯誤傳回給 C 介面。若可能的話，
  請以 `-fno-exceptions` 選項編譯 C++，以徹底消除
  例外；在這種情況下，您必須在您的 C++ 程式碼中
  檢查是否發生失敗，舉例來說，檢查
  `new()` 是否傳回 NULL。
* 若要從 C++ 程式碼呼叫後端函式，請務必確保
  C++ 的呼叫堆疊中，只包含純粹的資料
  結構（POD，plain old data structures）。這是必要的，
  因為後端錯誤會產生一個非本地的（distant）
  `longjmp()`，這無法正確地展開
  含有非 POD 物件的 C++ 呼叫堆疊。

總而言之，最好的做法是將 C++ 程式碼，
放在一道與後端介接、以
`extern C` 函式構成的牆之後，
並避免例外、記憶體以及呼叫堆疊的洩漏。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xfunc-c.html)（原文版本：18.6；核對日期：2026-09-25）
