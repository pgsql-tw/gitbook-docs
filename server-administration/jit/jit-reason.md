<a id="JIT-REASON"></a>

## 30.1. 什麼是 JIT 編譯？ [#](#JIT-REASON)

[30.1.1. JIT 可加速的操作](jit-reason.md#JIT-ACCELERATED-OPERATIONS)

[30.1.2. 內嵌（Inlining）](jit-reason.md#JIT-INLINING)

[30.1.3. 最佳化](jit-reason.md#JIT-OPTIMIZATION)

即時編譯（Just-in-Time，JIT）是一種在執行期將某種形式的
直譯式程式求值，轉換為原生程式的過程，並且是在執行期進行的。
舉例來說，與其使用可以求值任意 SQL 運算式的通用程式碼，來求值像
`WHERE a.col = 3` 這樣的特定 SQL 判斷式，不如產生一個
專門針對該運算式的函式，讓 CPU 能夠原生執行，藉此提升速度。

當 PostgreSQL 是以
[`--with-llvm`](../installation/install-make.md#CONFIGURE-WITH-LLVM) 建置時，PostgreSQL 內建支援使用
[LLVM](https://llvm.org/) 進行
JIT 編譯。

詳情請見 `src/backend/jit/README`。

<a id="JIT-ACCELERATED-OPERATIONS"></a>

### 30.1.1. JIT 可加速的操作 [#](#JIT-ACCELERATED-OPERATIONS)

目前 PostgreSQL 的 JIT
實作支援加速運算式求值與
tuple 解構。未來可能還會加速其他幾種操作。

運算式求值用於求值 `WHERE`
子句、目標清單、聚合與投影。透過針對每種情況產生
專屬程式碼，可以加速這個過程。

tuple 解構是將磁碟上的 tuple（見[第 66.6.1 節](../../internals/storage/storage-page-layout.md#STORAGE-TUPLE-LAYOUT)）轉換為其記憶體內表示形式的過程。
可以透過建立一個專屬於資料表結構
與要擷取欄位數量的函式，來加速這個過程。

<a id="JIT-INLINING"></a>

### 30.1.2. 內嵌（Inlining） [#](#JIT-INLINING)

PostgreSQL 具有高度可擴充性，允許定義新的
資料型別、函式、運算子與其他資料庫物件；見[第 36 章](../../server-programming/extend/README.md)。事實上，內建物件也是以幾乎
相同的機制實作的。這種可擴充性隱含了一些額外負擔，例如函式呼叫所帶來的負擔（見[第 36.3 節](../../server-programming/extend/xfunc.md)）。
為了降低這種額外負擔，JIT 編譯可以將小型函式的
內容內嵌到使用它們的運算式中。這樣一來，就能將
相當大比例的額外負擔最佳化掉。

<a id="JIT-OPTIMIZATION"></a>

### 30.1.3. 最佳化 [#](#JIT-OPTIMIZATION)

LLVM 支援對產生的
程式碼進行最佳化。部分最佳化的成本很低，只要使用
JIT 就會執行；而其他最佳化則只有在執行時間較長的查詢中
才有幫助。
更多有關最佳化的細節，請見 <https://llvm.org/docs/Passes.html#transform-passes>。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/jit-reason.html)（原文版本：18.6；核對日期：2026-09-25）
