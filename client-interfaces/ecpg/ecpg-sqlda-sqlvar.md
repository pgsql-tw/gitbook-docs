<a id="ECPG-SQLDA-SQLVAR"></a>

## 34.7.2.1.2. sqlvar_t 結構 [#](#ecpg-sqlda-sqlvar) <a href="#ecpg-sqlda-sqlvar" id="ecpg-sqlda-sqlvar"></a>

結構型別 `sqlvar_t` 存放一個欄位的值，以及型別與長度等中繼資料。此型別的定義如下：

```

struct sqlvar_struct
{
    short          sqltype;
    short          sqllen;
    char          *sqldata;
    short         *sqlind;
    struct sqlname sqlname;
};

typedef struct sqlvar_struct sqlvar_t;
```

各欄位的意義如下：

<a id="ECPG-SQLDA-SQLVAR-SQLTYPE"></a>

### `sqltype` [#](#ecpg-sqlda-sqlvar-sqltype) <a href="#ecpg-sqlda-sqlvar-sqltype" id="ecpg-sqlda-sqlvar-sqltype"></a>

包含欄位的型別識別碼。可能的值請參閱 `ecpgtype.h` 中的 `enum ECPGttype`。

<a id="ECPG-SQLDA-SQLVAR-SQLLEN"></a>

### `sqllen` [#](#ecpg-sqlda-sqlvar-sqllen) <a href="#ecpg-sqlda-sqlvar-sqllen" id="ecpg-sqlda-sqlvar-sqllen"></a>

包含欄位的二進位長度，例如 `ECPGt_int` 為 4 個位元組。

<a id="ECPG-SQLDA-SQLVAR-SQLDATA"></a>

### `sqldata` [#](#ecpg-sqlda-sqlvar-sqldata) <a href="#ecpg-sqlda-sqlvar-sqldata" id="ecpg-sqlda-sqlvar-sqldata"></a>

指向資料。資料的格式說明請參閱[第 34.4.4 節](ecpg-variables-type-mapping.md#ecpg-variables-type-mapping)。

<a id="ECPG-SQLDA-SQLVAR-SQLIND"></a>

### `sqlind` [#](#ecpg-sqlda-sqlvar-sqlind) <a href="#ecpg-sqlda-sqlvar-sqlind" id="ecpg-sqlda-sqlvar-sqlind"></a>

指向空值指示值。0 表示非空值，-1 表示空值。

<a id="ECPG-SQLDA-SQLVAR-SQLNAME"></a>

### `sqlname` [#](#ecpg-sqlda-sqlvar-sqlname) <a href="#ecpg-sqlda-sqlvar-sqlname" id="ecpg-sqlda-sqlvar-sqlname"></a>

欄位的名稱。

[返回 34.7.2.1. SQLDA 資料結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-descriptors-sqlda)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
