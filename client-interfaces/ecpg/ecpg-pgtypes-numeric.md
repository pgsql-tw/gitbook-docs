<a id="ECPG-PGTYPES-NUMERIC"></a>

## 34.6.2. numeric 型別 [#](#ecpg-pgtypes-numeric) <a href="#ecpg-pgtypes-numeric" id="ecpg-pgtypes-numeric"></a>

numeric 型別可以進行任意精確度的計算。PostgreSQL 伺服器中對應的型別請參閱[第 8.1 節](../../the-sql-language/datatype/datatype-numeric.md)。由於精確度任意，這種變數必須能夠動態地擴大與縮小。因此你只能透過 `PGTYPESnumeric_new` 與 `PGTYPESnumeric_free` 函式在堆積（heap）上建立 numeric 變數。decimal 型別與它相似但精確度有限，既可以建立在堆疊（stack）上，也可以建立在堆積上。

下列函式可用來處理 numeric 型別：

<a id="ECPG-PGTYPES-NUMERIC-NEW"></a>

### `PGTYPESnumeric_new` [#](#ecpg-pgtypes-numeric-new) <a href="#ecpg-pgtypes-numeric-new" id="ecpg-pgtypes-numeric-new"></a>

取得指向新配置之 numeric 變數的指標。

```

    numeric *PGTYPESnumeric_new(void);
```

<a id="ECPG-PGTYPES-NUMERIC-FREE"></a>

### `PGTYPESnumeric_free` [#](#ecpg-pgtypes-numeric-free) <a href="#ecpg-pgtypes-numeric-free" id="ecpg-pgtypes-numeric-free"></a>

釋放 numeric 型別，釋放它所有的記憶體。

```

    void PGTYPESnumeric_free(numeric *var);
```

<a id="ECPG-PGTYPES-NUMERIC-FROM-ASC"></a>

### `PGTYPESnumeric_from_asc` [#](#ecpg-pgtypes-numeric-from-asc) <a href="#ecpg-pgtypes-numeric-from-asc" id="ecpg-pgtypes-numeric-from-asc"></a>

從字串表示法剖析出 numeric 型別。

```

    numeric *PGTYPESnumeric_from_asc(char *str, char **endptr);
```

有效格式的例子如：
`-2`、
`.794`、
`+3.44`、
`592.49E07` 或
`-32.84e-4`。
若值能成功剖析，會傳回有效的指標，否則傳回 NULL 指標。目前 ECPG 一律剖析整個字串，因此目前不支援將第一個無效字元的位址存放到 `*endptr` 中。你可以放心地將 `endptr` 設為 NULL。

<a id="ECPG-PGTYPES-NUMERIC-TO-ASC"></a>

### `PGTYPESnumeric_to_asc` [#](#ecpg-pgtypes-numeric-to-asc) <a href="#ecpg-pgtypes-numeric-to-asc" id="ecpg-pgtypes-numeric-to-asc"></a>

傳回一個指標，指向由 `malloc` 配置、內含 numeric 型別 `num` 之字串表示法的字串。

```

    char *PGTYPESnumeric_to_asc(numeric *num, int dscale);
```

numeric 值會以 `dscale` 位小數輸出，必要時會進行捨入。
結果必須以 `PGTYPESchar_free()` 釋放。

<a id="ECPG-PGTYPES-NUMERIC-ADD"></a>

### `PGTYPESnumeric_add` [#](#ecpg-pgtypes-numeric-add) <a href="#ecpg-pgtypes-numeric-add" id="ecpg-pgtypes-numeric-add"></a>

將兩個 numeric 變數相加，結果存入第三個變數。

```

    int PGTYPESnumeric_add(numeric *var1, numeric *var2, numeric *result);
```

此函式將變數 `var1` 與 `var2` 相加，結果存入結果變數 `result`。
此函式成功時傳回 0，發生錯誤時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-SUB"></a>

### `PGTYPESnumeric_sub` [#](#ecpg-pgtypes-numeric-sub) <a href="#ecpg-pgtypes-numeric-sub" id="ecpg-pgtypes-numeric-sub"></a>

將兩個 numeric 變數相減，並在第三個變數中傳回結果。

```

    int PGTYPESnumeric_sub(numeric *var1, numeric *var2, numeric *result);
```

此函式將變數 `var1` 減去變數 `var2`。運算結果存放在變數 `result` 中。
此函式成功時傳回 0，發生錯誤時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-MUL"></a>

### `PGTYPESnumeric_mul` [#](#ecpg-pgtypes-numeric-mul) <a href="#ecpg-pgtypes-numeric-mul" id="ecpg-pgtypes-numeric-mul"></a>

將兩個 numeric 變數相乘，並在第三個變數中傳回結果。

```

    int PGTYPESnumeric_mul(numeric *var1, numeric *var2, numeric *result);
```

此函式將變數 `var1` 與 `var2` 相乘。運算結果存放在變數 `result` 中。
此函式成功時傳回 0，發生錯誤時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-DIV"></a>

### `PGTYPESnumeric_div` [#](#ecpg-pgtypes-numeric-div) <a href="#ecpg-pgtypes-numeric-div" id="ecpg-pgtypes-numeric-div"></a>

將兩個 numeric 變數相除，並在第三個變數中傳回結果。

```

    int PGTYPESnumeric_div(numeric *var1, numeric *var2, numeric *result);
```

此函式將變數 `var1` 除以 `var2`。運算結果存放在變數 `result` 中。
此函式成功時傳回 0，發生錯誤時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-CMP"></a>

### `PGTYPESnumeric_cmp` [#](#ecpg-pgtypes-numeric-cmp) <a href="#ecpg-pgtypes-numeric-cmp" id="ecpg-pgtypes-numeric-cmp"></a>

比較兩個 numeric 變數。

```

    int PGTYPESnumeric_cmp(numeric *var1, numeric *var2)
```

譯註：上方函式宣告依原文保留，原文漏了結尾的分號；正確的 C 宣告應以分號結尾。

此函式比較兩個 numeric 變數。發生錯誤時，傳回 `INT_MAX`。成功時，此函式傳回三種可能結果之一：

* 1，若 `var1` 大於 `var2`
* -1，若 `var1` 小於 `var2`
* 0，若 `var1` 與 `var2` 相等

<a id="ECPG-PGTYPES-NUMERIC-FROM-INT"></a>

### `PGTYPESnumeric_from_int` [#](#ecpg-pgtypes-numeric-from-int) <a href="#ecpg-pgtypes-numeric-from-int" id="ecpg-pgtypes-numeric-from-int"></a>

將 int 變數轉換為 numeric 變數。

```

    int PGTYPESnumeric_from_int(signed int int_val, numeric *var);
```

此函式接受一個 signed int 型別的變數，並將它存放在 numeric 變數 `var` 中。成功時傳回 0，失敗時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-FROM-LONG"></a>

### `PGTYPESnumeric_from_long` [#](#ecpg-pgtypes-numeric-from-long) <a href="#ecpg-pgtypes-numeric-from-long" id="ecpg-pgtypes-numeric-from-long"></a>

將 long int 變數轉換為 numeric 變數。

```

    int PGTYPESnumeric_from_long(signed long int long_val, numeric *var);
```

此函式接受一個 signed long int 型別的變數，並將它存放在 numeric 變數 `var` 中。成功時傳回 0，失敗時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-COPY"></a>

### `PGTYPESnumeric_copy` [#](#ecpg-pgtypes-numeric-copy) <a href="#ecpg-pgtypes-numeric-copy" id="ecpg-pgtypes-numeric-copy"></a>

將一個 numeric 變數複製到另一個變數。

```

    int PGTYPESnumeric_copy(numeric *src, numeric *dst);
```

此函式將 `src` 所指變數的值複製到 `dst` 所指的變數中。成功時傳回 0，發生錯誤時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-FROM-DOUBLE"></a>

### `PGTYPESnumeric_from_double` [#](#ecpg-pgtypes-numeric-from-double) <a href="#ecpg-pgtypes-numeric-from-double" id="ecpg-pgtypes-numeric-from-double"></a>

將 double 型別的變數轉換為 numeric。

```

    int  PGTYPESnumeric_from_double(double d, numeric *dst);
```

此函式接受一個 double 型別的變數，並將結果存放在 `dst` 所指的變數中。成功時傳回 0，發生錯誤時傳回 -1。

<a id="ECPG-PGTYPES-NUMERIC-TO-DOUBLE"></a>

### `PGTYPESnumeric_to_double` [#](#ecpg-pgtypes-numeric-to-double) <a href="#ecpg-pgtypes-numeric-to-double" id="ecpg-pgtypes-numeric-to-double"></a>

將 numeric 型別的變數轉換為 double。

```

    int PGTYPESnumeric_to_double(numeric *nv, double *dp)
```

譯註：上方函式宣告依原文保留，原文漏了結尾的分號；正確的 C 宣告應以分號結尾。

此函式將 `nv` 所指變數中的 numeric 值轉換到 `dp` 所指的 double 變數中。成功時傳回 0，發生錯誤（包括溢位）時傳回 -1。溢位時，另外還會將全域變數 `errno` 設為 `PGTYPES_NUM_OVERFLOW`。

<a id="ECPG-PGTYPES-NUMERIC-TO-INT"></a>

### `PGTYPESnumeric_to_int` [#](#ecpg-pgtypes-numeric-to-int) <a href="#ecpg-pgtypes-numeric-to-int" id="ecpg-pgtypes-numeric-to-int"></a>

將 numeric 型別的變數轉換為 int。

```

    int PGTYPESnumeric_to_int(numeric *nv, int *ip);
```

此函式將 `nv` 所指變數中的 numeric 值轉換到 `ip` 所指的整數變數中。成功時傳回 0，發生錯誤（包括溢位）時傳回 -1。溢位時，另外還會將全域變數 `errno` 設為 `PGTYPES_NUM_OVERFLOW`。

<a id="ECPG-PGTYPES-NUMERIC-TO-LONG"></a>

### `PGTYPESnumeric_to_long` [#](#ecpg-pgtypes-numeric-to-long) <a href="#ecpg-pgtypes-numeric-to-long" id="ecpg-pgtypes-numeric-to-long"></a>

將 numeric 型別的變數轉換為 long。

```

    int PGTYPESnumeric_to_long(numeric *nv, long *lp);
```

此函式將 `nv` 所指變數中的 numeric 值轉換到 `lp` 所指的長整數變數中。成功時傳回 0，發生錯誤（包括溢位與下溢）時傳回 -1。溢位時，全域變數 `errno` 會被設為 `PGTYPES_NUM_OVERFLOW`；下溢時，`errno` 會被設為 `PGTYPES_NUM_UNDERFLOW`。

<a id="ECPG-PGTYPES-NUMERIC-TO-DECIMAL"></a>

### `PGTYPESnumeric_to_decimal` [#](#ecpg-pgtypes-numeric-to-decimal) <a href="#ecpg-pgtypes-numeric-to-decimal" id="ecpg-pgtypes-numeric-to-decimal"></a>

將 numeric 型別的變數轉換為 decimal。

```

    int PGTYPESnumeric_to_decimal(numeric *src, decimal *dst);
```

此函式將 `src` 所指變數中的 numeric 值轉換到 `dst` 所指的 decimal 變數中。成功時傳回 0，發生錯誤（包括溢位）時傳回 -1。溢位時，另外還會將全域變數 `errno` 設為 `PGTYPES_NUM_OVERFLOW`。

<a id="ECPG-PGTYPES-NUMERIC-FROM-DECIMAL"></a>

### `PGTYPESnumeric_from_decimal` [#](#ecpg-pgtypes-numeric-from-decimal) <a href="#ecpg-pgtypes-numeric-from-decimal" id="ecpg-pgtypes-numeric-from-decimal"></a>

將 decimal 型別的變數轉換為 numeric。

```

    int PGTYPESnumeric_from_decimal(decimal *src, numeric *dst);
```

此函式將 `src` 所指變數中的 decimal 值轉換到 `dst` 所指的 numeric 變數中。成功時傳回 0，發生錯誤時傳回 -1。由於 decimal 型別是以 numeric 型別的受限版本實作，這項轉換不可能發生溢位。

[返回 34.6. pgtypes 函式庫](ecpg-pgtypes.md#ecpg-pgtypes)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
