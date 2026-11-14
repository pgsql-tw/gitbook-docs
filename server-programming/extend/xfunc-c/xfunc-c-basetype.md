# 36.10.2. C 語言函式中的基礎型別

<a id="XFUNC-C-BASETYPE"></a>

## 36.10.2. C 語言函式中的基礎型別 [#](#xfunc-c-basetype) <a href="#xfunc-c-basetype" id="xfunc-c-basetype"></a>

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
[表 36.2](#xfunc-c-type-table)。）

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
[36.12 節](../xaggr.md)中。

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

[表 36.2](#xfunc-c-type-table)顯示了 PostgreSQL
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

### 表 36.2. 內建 SQL 型別對應的 C 型別 [#](#xfunc-c-type-table) <a href="#xfunc-c-type-table" id="xfunc-c-type-table"></a>

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

[返回 36.10. C 語言函式](../xfunc-c.md#xfunc-c)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xfunc-c.html)（原文版本：18.6；核對日期：2026-09-25）
