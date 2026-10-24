<a id="ECPG-SQLDA-DESCRIPTORS-SQLDA"></a>

## 34.7.2.1. SQLDA 資料結構 [#](#ecpg-sqlda-descriptors-sqlda) <a href="#ecpg-sqlda-descriptors-sqlda" id="ecpg-sqlda-descriptors-sqlda"></a>

SQLDA 使用三種資料結構型別：`sqlda_t`、`sqlvar_t` 與 `struct sqlname`。

### 提示

PostgreSQL 的 SQLDA 與 IBM DB2 Universal Database 中的 SQLDA 資料結構相似，因此一些關於 DB2 SQLDA 的技術資訊，可能有助於更深入理解 PostgreSQL 的 SQLDA。

<a id="ECPG-SQLDA-SQLDA"></a>

### 34.7.2.1.1. sqlda_t 結構 [#](#ecpg-sqlda-sqlda) <a href="#ecpg-sqlda-sqlda" id="ecpg-sqlda-sqlda"></a>

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

`sqldaid` [#](#ECPG-SQLDA-SQLDA-SQLDAID)
:   包含字串常數 `"SQLDA "`。
<a id="ECPG-SQLDA-SQLDA-SQLDABC"></a>

`sqldabc` [#](#ECPG-SQLDA-SQLDA-SQLDABC)
:   包含已配置空間的大小（以位元組計）。
<a id="ECPG-SQLDA-SQLDA-SQLN"></a>

`sqln` [#](#ECPG-SQLDA-SQLDA-SQLN)
:   若此 SQLDA 是以 `USING` 關鍵字傳入 `OPEN`、`DECLARE` 或 `EXECUTE` 陳述式，此欄位包含參數化查詢的輸入參數數目。若此 SQLDA 用作 `SELECT`、`EXECUTE` 或 `FETCH` 陳述式的輸出，其值與 `sqld` 相同（原文此處在 sqld 之後多了一個 statement 字樣，屬贅字）。
<a id="ECPG-SQLDA-SQLDA-SQLD"></a>

`sqld` [#](#ECPG-SQLDA-SQLDA-SQLD)
:   包含結果集中的欄位數。
<a id="ECPG-SQLDA-SQLDA-DESC-NEXT"></a>

`desc_next` [#](#ECPG-SQLDA-SQLDA-DESC-NEXT)
:   若查詢傳回超過一筆記錄，就會傳回多個相互鏈結的 SQLDA 結構，而 `desc_next` 存放指向串列中下一個項目的指標。
<a id="ECPG-SQLDA-SQLDA-SQLVAR"></a>

`sqlvar` [#](#ECPG-SQLDA-SQLDA-SQLVAR)
:   這是結果集中各欄位的陣列。

<a id="ECPG-SQLDA-SQLVAR"></a>

### 34.7.2.1.2. sqlvar_t 結構 [#](#ecpg-sqlda-sqlvar) <a href="#ecpg-sqlda-sqlvar" id="ecpg-sqlda-sqlvar"></a>

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

`sqltype` [#](#ECPG-SQLDA-SQLVAR-SQLTYPE)
:   包含欄位的型別識別碼。可能的值請參閱 `ecpgtype.h` 中的 `enum ECPGttype`。
<a id="ECPG-SQLDA-SQLVAR-SQLLEN"></a>

`sqllen` [#](#ECPG-SQLDA-SQLVAR-SQLLEN)
:   包含欄位的二進位長度，例如 `ECPGt_int` 為 4 個位元組。
<a id="ECPG-SQLDA-SQLVAR-SQLDATA"></a>

`sqldata` [#](#ECPG-SQLDA-SQLVAR-SQLDATA)
:   指向資料。資料的格式說明請參閱[第 34.4.4 節](ecpg-variables-type-mapping.md#ecpg-variables-type-mapping)。
<a id="ECPG-SQLDA-SQLVAR-SQLIND"></a>

`sqlind` [#](#ECPG-SQLDA-SQLVAR-SQLIND)
:   指向空值指示值。0 表示非空值，-1 表示空值。
<a id="ECPG-SQLDA-SQLVAR-SQLNAME"></a>

`sqlname` [#](#ECPG-SQLDA-SQLVAR-SQLNAME)
:   欄位的名稱。

<a id="ECPG-SQLDA-SQLNAME"></a>

### 34.7.2.1.3. struct sqlname 結構 [#](#ecpg-sqlda-sqlname) <a href="#ecpg-sqlda-sqlname" id="ecpg-sqlda-sqlname"></a>

`struct sqlname` 結構存放一個欄位名稱。它用作 `sqlvar_t` 結構的成員。此結構的定義如下：

```

#define NAMEDATALEN 64

struct sqlname
{
        short           length;
        char            data[NAMEDATALEN];
};
```

各欄位的意義如下：

<a id="ECPG-SQLDA-SQLNAME-LENGTH"></a>

`length` [#](#ECPG-SQLDA-SQLNAME-LENGTH)
:   包含欄位名稱的長度。
<a id="ECPG-SQLDA-SQLNAME-DATA"></a>

`data` [#](#ECPG-SQLDA-SQLNAME-DATA)
:   包含實際的欄位名稱。

[返回 34.7.2. SQLDA 描述區](ecpg-sqlda-descriptors.md#ecpg-sqlda-descriptors)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
