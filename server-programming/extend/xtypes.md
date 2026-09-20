<a id="XTYPES"></a>
## 36.13. 使用者自訂型別 [#](#XTYPES)

[36.13.1. TOAST 相關考量](xtypes.md#XTYPES-TOAST)

<a id="id-1.8.3.16.2"></a>

如[36.2 節](extend-type-system.md)所述，
PostgreSQL 可以擴充以支援新的
資料型別。本節說明如何定義新的基礎型別（base type），
也就是定義在 SQL
語言層次之下的資料型別。建立新的基礎型別，需要
以低階語言（通常是 C）實作用來操作該型別的函式。

本節中的範例可以在原始碼發行套件的
`src/tutorial` 目錄下的
`complex.sql` 與 `complex.c` 中找到。
關於如何執行這些範例的說明，請參閱該目錄下的 `README` 檔。

<a id="id-1.8.3.16.5.1"></a>
<a id="id-1.8.3.16.5.2"></a>
使用者自訂型別一定要具備輸入與輸出函式。
這些函式決定了該型別在字串中呈現的方式（供使用者輸入
以及輸出給使用者），以及該型別在記憶體中的組織方式。輸入函式
接受一個以 null 結尾的字元字串作為其引數，並傳回該型別的內部
（記憶體中）表示法。輸出函式接受該型別的內部表示法
作為引數，並傳回一個以 null 結尾的字元
字串。若我們想要對該型別做的不只是單純儲存它，
則必須提供額外的函式，以實作我們想要提供給該型別的
各種運算。

假設我們想要定義一個代表複數的型別
`complex`。在記憶體中表示複數的一種
自然做法，是使用以下的 C 結構：

```

typedef struct Complex {
    double      x;
    double      y;
} Complex;
```

我們需要將它做成傳址（pass-by-reference）型別，因為它
太大，無法容納在單一 `Datum` 值中。

作為該型別的外部字串表示法，我們選擇形式為
`(x,y)` 的字串。

輸入與輸出函式通常不難撰寫，
輸出函式尤其如此。但在定義型別的外部
字串表示法時，請記得，您最終必須為您的輸入函式
撰寫一個完整且穩健的剖析器，來剖析該表示法。舉例來說：

```

PG_FUNCTION_INFO_V1(complex_in);

Datum
complex_in(PG_FUNCTION_ARGS)
{
    char       *str = PG_GETARG_CSTRING(0);
    double      x,
                y;
    Complex    *result;

    if (sscanf(str, " ( %lf , %lf )", &x, &y) != 2)
        ereport(ERROR,
                (errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
                 errmsg("invalid input syntax for type %s: \"%s\"",
                        "complex", str)));

    result = (Complex *) palloc(sizeof(Complex));
    result->x = x;
    result->y = y;
    PG_RETURN_POINTER(result);
}
```

輸出函式則可以簡單地寫成：

```

PG_FUNCTION_INFO_V1(complex_out);

Datum
complex_out(PG_FUNCTION_ARGS)
{
    Complex    *complex = (Complex *) PG_GETARG_POINTER(0);
    char       *result;

    result = psprintf("(%g,%g)", complex->x, complex->y);
    PG_RETURN_CSTRING(result);
}
```

您應該小心確保輸入與輸出函式互為反函式。
若做不到這一點，當您需要將資料傾印到檔案，
再讀回來時，就會遇到嚴重的問題。當涉及
浮點數時，這是一個特別常見的問題。

使用者自訂型別也可以選擇性地提供二進位輸入與輸出
常式。二進位輸出入通常比文字輸出入更快，但可移植性較低。
與文字輸出入一樣，要精確定義外部的二進位
表示法是什麼，由您自行決定。大多數內建的資料型別
都會盡量提供與機器無關的二進位表示法。對於
`complex`，我們將搭便車，使用
`float8` 型別的二進位輸出入轉換器：

```

PG_FUNCTION_INFO_V1(complex_recv);

Datum
complex_recv(PG_FUNCTION_ARGS)
{
    StringInfo  buf = (StringInfo) PG_GETARG_POINTER(0);
    Complex    *result;

    result = (Complex *) palloc(sizeof(Complex));
    result->x = pq_getmsgfloat8(buf);
    result->y = pq_getmsgfloat8(buf);
    PG_RETURN_POINTER(result);
}

PG_FUNCTION_INFO_V1(complex_send);

Datum
complex_send(PG_FUNCTION_ARGS)
{
    Complex    *complex = (Complex *) PG_GETARG_POINTER(0);
    StringInfoData buf;

    pq_begintypsend(&buf);
    pq_sendfloat8(&buf, complex->x);
    pq_sendfloat8(&buf, complex->y);
    PG_RETURN_BYTEA_P(pq_endtypsend(&buf));
}
```

一旦我們撰寫好了輸出入函式，並將它們編譯成一個共享
程式庫，就可以在 SQL 中定義 `complex` 型別。
首先，我們將它宣告為一個殼層型別（shell type）：

```

CREATE TYPE complex;
```

這是一個佔位符，讓我們在定義其輸出入函式時，能夠參照該型別。
現在我們可以定義輸出入函式：

```

CREATE FUNCTION complex_in(cstring)
    RETURNS complex
    AS 'filename'
    LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION complex_out(complex)
    RETURNS cstring
    AS 'filename'
    LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION complex_recv(internal)
   RETURNS complex
   AS 'filename'
   LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION complex_send(complex)
   RETURNS bytea
   AS 'filename'
   LANGUAGE C IMMUTABLE STRICT;
```

最後，我們可以提供該資料型別的完整定義：

```

CREATE TYPE complex (
   internallength = 16,
   input = complex_in,
   output = complex_out,
   receive = complex_recv,
   send = complex_send,
   alignment = double
);
```

<a id="id-1.8.3.16.13.1"></a>
當您定義一個新的基礎型別時，
PostgreSQL 會自動提供對該型別
陣列的支援。陣列型別的名稱，通常
與基礎型別相同，只是前面加上底線字元
（`_`）。

一旦該資料型別存在，我們就可以宣告額外的函式，
來提供該資料型別上有用的運算。接著就可以在這些函式之上
定義運算子，若有需要，還可以建立運算子類別（operator class），
以支援該資料型別的索引。這些額外的
層次，將在後續章節中討論。

若資料型別的內部表示法是可變長度的，則該
內部表示法必須遵循可變長度資料的標準版面配置：
前四個位元組必須是一個 `char[4]` 欄位，
且絕不會被直接存取（習慣上命名為 `vl_len_`）。您
必須使用 `SET_VARSIZE()` 巨集，將該
datum 的總大小（包含長度欄位本身）儲存在此欄位中，
並使用 `VARSIZE()` 來取得該值。（之所以有這些巨集，
是因為長度欄位可能會依平台而有不同的編碼方式。）

更多詳情請參閱
[CREATE TYPE](../../reference/sql-commands/sql-createtype.md) 指令的說明。

<a id="XTYPES-TOAST"></a>

### 36.13.1. TOAST 相關考量 [#](#XTYPES-TOAST)

<a id="id-1.8.3.16.17.2"></a>

若您資料型別的值（在內部形式中）大小會有所變化，
通常會希望讓該資料型別可支援 TOAST
（請參閱[66.2 節](../../internals/storage/storage-toast.md)）。即使該值
永遠太小，無法被壓縮或儲存於外部，您也應該這麼做，因為
TOAST 也能透過降低標頭額外負擔，
為小型資料節省空間。

為了支援 TOAST 儲存，操作該資料型別的 C 函式
必須永遠小心，使用 `PG_DETOAST_DATUM` 來解包收到的任何
已 TOAST 化的值。（這個細節通常會透過定義
特定型別的 `GETARG_DATATYPE_P` 巨集來隱藏。）
接著，在執行 `CREATE TYPE` 指令時，請將
內部長度指定為 `variable`，並選擇某種適當的
儲存選項，而非 `plain`。

若資料對齊並不重要（可能只是針對特定函式而言，或者是
因為該資料型別本身就是採用位元組對齊），則可以
避免部分 `PG_DETOAST_DATUM` 所帶來的額外負擔。您可以改用
`PG_DETOAST_DATUM_PACKED`（通常會透過定義
`GETARG_DATATYPE_PP` 巨集來隱藏），並使用巨集
`VARSIZE_ANY_EXHDR` 與 `VARDATA_ANY` 來存取
可能已打包的 datum。
同樣地，即使該資料型別的定義指定了對齊方式，
這些巨集所傳回的資料也不會經過對齊。若對齊方式很重要，
您必須透過一般的 `PG_DETOAST_DATUM` 介面來處理。

### 注意

較舊的程式碼經常將 `vl_len_` 宣告為
`int32` 欄位，而非 `char[4]`。只要
該結構定義中還有其他欄位具備至少 `int32` 的
對齊方式，這樣做是可以的。但在處理可能未對齊的 datum 時，
使用這樣的結構定義是危險的；編譯器可能會據此
假定該 datum 實際上是已對齊的，在對齊要求嚴格的
架構上，就可能導致核心傾印（core dump）。

TOAST 支援所啟用的另一項特色，是能夠擁有
一種比磁碟上所儲存格式更方便使用的
記憶體內*展開（expanded）*資料表示法。
一般或「扁平（flat）」的 varlena 儲存格式
終究只是一堆位元組；舉例來說，它不能包含
指標，因為它可能會被複製到記憶體中的其他位置。
對於複雜的資料型別而言，處理扁平格式的成本可能相當高，
因此 PostgreSQL 提供了一種方式，可以將
扁平格式「展開」成更適合運算的表示法，
再將該格式以記憶體內形式在該資料型別的各個函式之間傳遞。

若要使用展開儲存，資料型別必須定義一種遵循
`src/include/utils/expandeddatum.h` 中所述規則的展開格式，
並提供函式，將扁平的 varlena 值「展開」為
展開格式，以及將展開格式「壓平」回
一般的 varlena 表示法。接著，請確保該資料型別的所有 C 函式
都能接受這兩種表示法，可以透過在收到值時，
立即將其中一種轉換為另一種來達成。這並不需要一次性
修正該資料型別的所有既有函式，因為標準的
`PG_DETOAST_DATUM` 巨集本身就定義為會將展開格式的輸入
轉換為一般的扁平格式。因此，既有的、處理
扁平 varlena 格式的函式，在收到展開格式的輸入時，
仍然可以繼續運作，只是效率會稍差；只有在效能
真的重要時，才需要進行轉換。

懂得處理展開表示法的 C 函式，
通常可分為兩類：只能處理展開格式的函式，
以及既能處理展開格式、也能處理扁平 varlena 輸入的函式。
前者較容易撰寫，但整體而言效率可能較低，因為
為了讓單一函式使用，而將扁平輸入轉換為展開格式，
其成本可能超過在展開格式上運算所省下的成本。
當只需要處理展開格式時，可以將扁平輸入轉換為
展開格式的動作，隱藏在一個擷取引數的巨集中，
如此一來，該函式看起來並不會比處理傳統
varlena 輸入的函式更複雜。
若要同時處理這兩種輸入類型，請撰寫一個擷取引數的函式，
用來對外部、短標頭與已壓縮的 varlena 輸入進行去 TOAST 化，但
不處理展開格式的輸入。這樣的函式，可以定義為傳回一個
指向扁平 varlena 格式與展開格式聯集（union）的指標。
呼叫方可以使用 `VARATT_IS_EXPANDED_HEADER()` 巨集
來判斷自己收到的是哪一種格式。

TOAST 基礎架構不僅能區分一般的 varlena
值與展開值，也能區分指向展開值的
「可讀寫」與「唯讀」指標。只需要檢視展開
值、或只會以安全且不會對外顯露語意的方式修改該值的 C 函式，
不需要在意自己收到的是哪一種指標。產生輸入值修改版本的
C 函式，若收到的是可讀寫指標，則可以就地修改
展開輸入值；但若收到的是唯讀指標，則
不得修改該輸入；在這種情況下，它們必須先複製該值，
再產生一個新的值來進行修改。
已建構出新展開值的 C 函式，應該永遠傳回一個
指向該值的可讀寫指標。此外，就地修改
可讀寫展開值的 C 函式，應該小心確保，
若中途失敗，該值仍會保持在合理的狀態。

關於展開值的使用範例，請參閱標準陣列
基礎架構，特別是
`src/backend/utils/adt/array_expanded.c`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xtypes.html)（原文版本：18.6；核對日期：2026-09-16）
