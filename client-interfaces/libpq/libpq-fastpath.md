<a id="LIBPQ-FASTPATH"></a>

## 32.8. 快速路徑介面 [#](#libpq-fastpath) <a href="#libpq-fastpath" id="libpq-fastpath"></a>

<a id="id-1.7.3.15.2"></a>

PostgreSQL 提供一個快速路徑（fast-path）介面，用來向伺服器送出簡單的函式呼叫。

### 警告

此介面並不安全，不應該使用。當 *`result_is_int`* 設為 `0` 時，不論緩衝區是否有足夠空間容納所要求的位元組數，`PQfn` 都可能寫入超出 *`result_buf`* 結尾的資料。此外，此介面已經過時，因為設定一個預備陳述式來定義該函式呼叫，就能達到相近的效能與更多的功能。之後，以參數與結果的二進位傳輸來執行該陳述式，即可取代快速路徑函式呼叫。

函式 <a id="LIBPQ-PQFN"></a>`PQfn`<a id="id-1.7.3.15.5.2"></a>
透過快速路徑介面要求執行伺服器函式：

```

PGresult *PQfn(PGconn *conn,
               int fnid,
               int *result_buf,
               int *result_len,
               int result_is_int,
               const PQArgBlock *args,
               int nargs);

typedef struct
{
    int len;
    int isint;
    union
    {
        int *ptr;
        int integer;
    } u;
} PQArgBlock;
```

*`fnid`* 引數是要執行之函式的 OID。*`args`* 與 *`nargs`* 定義要傳給函式的參數；它們必須與函式宣告的引數列表相符。當參數結構的 *`isint`* 欄位為真時，*`u.integer`* 值會以指定長度的整數送到伺服器（長度必須是 2 或 4 個位元組），並會進行適當的位元組交換（byte-swapping）。當 *`isint`* 為假時，*`*u.ptr`* 所指的指定數量位元組會不經任何處理直接送出；這些資料必須符合伺服器以二進位傳輸該函式引數資料型別時所預期的格式。（將 *`u.ptr`* 宣告為 `int *` 型別是歷史因素；將它視為 `void *` 會比較好。）*`result_buf`* 指向用來存放函式傳回值的緩衝區。呼叫端必須已配置足夠的空間來存放傳回值。（這裡沒有任何檢查！）實際的結果長度（以位元組為單位）會傳回到 *`result_len`* 所指的整數中。若預期結果是 2 或 4 位元組的整數，請將 *`result_is_int`* 設為 1，否則設為 0。將 *`result_is_int`* 設為 1 會使 libpq 在必要時對該值進行位元組交換，使其以用戶端機器上正確的 `int` 值傳回；請注意，不論是哪一種允許的結果大小，傳入 *`*result_buf`* 的都是 4 位元組整數。當 *`result_is_int`* 為 0 時，伺服器送出的二進位格式位元組字串會原封不動傳回。（在這種情況下，最好將 *`result_buf`* 視為 `void *` 型別。）

`PQfn` 一律傳回有效的 `PGresult` 指標，成功時狀態為 `PGRES_COMMAND_OK`，若遇到任何問題則為 `PGRES_FATAL_ERROR`。使用結果之前應該先檢查結果狀態。不再需要該 `PGresult` 時，呼叫端負責以 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 釋放它。

要將 NULL 引數傳給函式，請將該參數結構的 *`len`* 欄位設為 `-1`；此時 *`isint`* 與 *`u`* 欄位便無關緊要。

若函式傳回 NULL，*`*result_len`* 會被設為 `-1`，而 *`*result_buf`* 不會被修改。

請注意，使用此介面時無法處理集合值（set-valued）結果。此外，該函式必須是一般函式，不能是彙總函式、視窗函式或程序。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-fastpath.html)（原文版本：18.6；核對日期：2026-10-18）
