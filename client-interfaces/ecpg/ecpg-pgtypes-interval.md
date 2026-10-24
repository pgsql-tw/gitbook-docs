<a id="ECPG-PGTYPES-INTERVAL"></a>

## 34.6.5. interval 型別 [#](#ecpg-pgtypes-interval) <a href="#ecpg-pgtypes-interval" id="ecpg-pgtypes-interval"></a>

C 中的 interval 型別讓你的程式能夠處理 SQL 型別 interval 的資料。PostgreSQL 伺服器中對應的型別請參閱[第 8.5 節](../../the-sql-language/datatype/datatype-datetime.md)。

下列函式可用來處理 interval 型別：

<a id="PGTYPESINTERVALNEW"></a>

### `PGTYPESinterval_new` [#](#pgtypesintervalnew) <a href="#pgtypesintervalnew" id="pgtypesintervalnew"></a>

傳回指向新配置之 interval 變數的指標。

```

    interval *PGTYPESinterval_new(void);
```

<a id="PGTYPESINTERVALFREE"></a>

### `PGTYPESinterval_free` [#](#pgtypesintervalfree) <a href="#pgtypesintervalfree" id="pgtypesintervalfree"></a>

釋放先前配置之 interval 變數的記憶體。

```

    void PGTYPESinterval_free(interval *intvl);
```

<a id="PGTYPESINTERVALFROMASC"></a>

### `PGTYPESinterval_from_asc` [#](#pgtypesintervalfromasc) <a href="#pgtypesintervalfromasc" id="pgtypesintervalfromasc"></a>

從文字表示法剖析出 interval。

```

    interval *PGTYPESinterval_from_asc(char *str, char **endptr);
```

此函式剖析輸入字串 `str`，並傳回指向已配置之 interval 變數的指標。
目前 ECPG 一律剖析整個字串，因此目前不支援將第一個無效字元的位址存放到 `*endptr` 中。
你可以放心地將 `endptr` 設為 NULL。

<a id="PGTYPESINTERVALTOASC"></a>

### `PGTYPESinterval_to_asc` [#](#pgtypesintervaltoasc) <a href="#pgtypesintervaltoasc" id="pgtypesintervaltoasc"></a>

將 interval 型別的變數轉換為它的文字表示法。

```

    char *PGTYPESinterval_to_asc(interval *span);
```

此函式將 `span` 所指的 interval 變數轉換為 C char\*。輸出看起來像這個範例：
`@ 1 day 12 hours 59 mins 10 secs`。
結果必須以 `PGTYPESchar_free()` 釋放。

<a id="PGTYPESINTERVALCOPY"></a>

### `PGTYPESinterval_copy` [#](#pgtypesintervalcopy) <a href="#pgtypesintervalcopy" id="pgtypesintervalcopy"></a>

複製 interval 型別的變數。

```

    int PGTYPESinterval_copy(interval *intvlsrc, interval *intvldest);
```

此函式將 `intvlsrc` 所指的 interval 變數複製到 `intvldest` 所指的變數中。請注意，你必須事先為目的變數配置記憶體。

[返回 34.6. pgtypes 函式庫](ecpg-pgtypes.md#ecpg-pgtypes)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
