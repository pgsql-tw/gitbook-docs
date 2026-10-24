<a id="ECPG-SQLDA-SQLDA"></a>

## 34.7.2.1.1. sqlda_t 結構 [#](#ecpg-sqlda-sqlda) <a href="#ecpg-sqlda-sqlda" id="ecpg-sqlda-sqlda"></a>

結構型別 `sqlda_t` 是實際 SQLDA 的型別。它存放一筆記錄。兩個或更多 `sqlda_t` 結構可以透過 `desc_next` 欄位中的指標連成鏈結串列，藉此表示有序的資料列集合。因此，擷取到兩個或更多資料列時，應用程式可以沿著每個 `sqlda_t` 節點中的 `desc_next` 指標讀取這些資料列。

`sqlda_t` 的定義如下：

```

struct sqlda_struct
{
    char            sqldaid[8];
    long            sqldabc;
    short           sqln;
    short           sqld;
    struct sqlda_struct *desc_next;
    struct sqlvar_struct sqlvar[1];
};

typedef struct sqlda_struct sqlda_t;
```

各欄位的意義如下：

<a id="ECPG-SQLDA-SQLDA-SQLDAID"></a>

### `sqldaid` [#](#ecpg-sqlda-sqlda-sqldaid) <a href="#ecpg-sqlda-sqlda-sqldaid" id="ecpg-sqlda-sqlda-sqldaid"></a>

包含字串常數 `"SQLDA "`。

<a id="ECPG-SQLDA-SQLDA-SQLDABC"></a>

### `sqldabc` [#](#ecpg-sqlda-sqlda-sqldabc) <a href="#ecpg-sqlda-sqlda-sqldabc" id="ecpg-sqlda-sqlda-sqldabc"></a>

包含已配置空間的大小（以位元組計）。

<a id="ECPG-SQLDA-SQLDA-SQLN"></a>

### `sqln` [#](#ecpg-sqlda-sqlda-sqln) <a href="#ecpg-sqlda-sqlda-sqln" id="ecpg-sqlda-sqlda-sqln"></a>

若此 SQLDA 是以 `USING` 關鍵字傳入 `OPEN`、`DECLARE` 或 `EXECUTE` 陳述式，此欄位包含參數化查詢的輸入參數數目。若此 SQLDA 用作 `SELECT`、`EXECUTE` 或 `FETCH` 陳述式的輸出，其值與 `sqld` 相同（原文此處在 sqld 之後多了一個 statement 字樣，屬贅字）。

<a id="ECPG-SQLDA-SQLDA-SQLD"></a>

### `sqld` [#](#ecpg-sqlda-sqlda-sqld) <a href="#ecpg-sqlda-sqlda-sqld" id="ecpg-sqlda-sqlda-sqld"></a>

包含結果集中的欄位數。

<a id="ECPG-SQLDA-SQLDA-DESC-NEXT"></a>

### `desc_next` [#](#ecpg-sqlda-sqlda-desc-next) <a href="#ecpg-sqlda-sqlda-desc-next" id="ecpg-sqlda-sqlda-desc-next"></a>

若查詢傳回超過一筆記錄，就會傳回多個相互鏈結的 SQLDA 結構，而 `desc_next` 存放指向串列中下一個項目的指標。

<a id="ECPG-SQLDA-SQLDA-SQLVAR"></a>

### `sqlvar` [#](#ecpg-sqlda-sqlda-sqlvar) <a href="#ecpg-sqlda-sqlda-sqlvar" id="ecpg-sqlda-sqlda-sqlvar"></a>

這是結果集中各欄位的陣列。

[返回 34.7.2.1. SQLDA 資料結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-descriptors-sqlda)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
