<a id="ECPG-INFORMIX-SQLDA"></a>

## 34.15.3. 與 Informix 相容的 SQLDA 描述區 [#](#ecpg-informix-sqlda) <a href="#ecpg-informix-sqlda" id="ecpg-informix-sqlda"></a>

Informix 相容模式支援的結構與[第 34.7.2 節](ecpg-sqlda-descriptors.md#ecpg-sqlda-descriptors)所述的結構不同。請見下方：

```

struct sqlvar_compat
{
    short   sqltype;
    int     sqllen;
    char   *sqldata;
    short  *sqlind;
    char   *sqlname;
    char   *sqlformat;
    short   sqlitype;
    short   sqlilen;
    char   *sqlidata;
    int     sqlxid;
    char   *sqltypename;
    short   sqltypelen;
    short   sqlownerlen;
    short   sqlsourcetype;
    char   *sqlownername;
    int     sqlsourceid;
    char   *sqlilongdata;
    int     sqlflags;
    void   *sqlreserved;
};

struct sqlda_compat
{
    short  sqld;
    struct sqlvar_compat *sqlvar;
    char   desc_name[19];
    short  desc_occ;
    struct sqlda_compat *desc_next;
    void  *reserved;
};

typedef struct sqlvar_compat    sqlvar_t;
typedef struct sqlda_compat     sqlda_t;
```

整體屬性如下：

<a id="ECPG-INFORMIX-SQLDA-SQLD"></a>

### `sqld` [#](#ecpg-informix-sqlda-sqld) <a href="#ecpg-informix-sqlda-sqld" id="ecpg-informix-sqlda-sqld"></a>

`SQLDA` 描述區中的欄位數。

<a id="ECPG-INFORMIX-SQLDA-SQLVAR"></a>

### `sqlvar` [#](#ecpg-informix-sqlda-sqlvar) <a href="#ecpg-informix-sqlda-sqlvar" id="ecpg-informix-sqlda-sqlvar"></a>

指向各欄位屬性的指標。

<a id="ECPG-INFORMIX-SQLDA-DESC-NAME"></a>

### `desc_name` [#](#ecpg-informix-sqlda-desc-name) <a href="#ecpg-informix-sqlda-desc-name" id="ecpg-informix-sqlda-desc-name"></a>

未使用，以零位元組填滿。

<a id="ECPG-INFORMIX-SQLDA-DESC-OCC"></a>

### `desc_occ` [#](#ecpg-informix-sqlda-desc-occ) <a href="#ecpg-informix-sqlda-desc-occ" id="ecpg-informix-sqlda-desc-occ"></a>

已配置結構的大小。

<a id="ECPG-INFORMIX-SQLDA-DESC-NEXT"></a>

### `desc_next` [#](#ecpg-informix-sqlda-desc-next) <a href="#ecpg-informix-sqlda-desc-next" id="ecpg-informix-sqlda-desc-next"></a>

若結果集包含超過一筆記錄，則為指向下一個 SQLDA 結構的指標。

<a id="ECPG-INFORMIX-SQLDA-RESERVED"></a>

### `reserved` [#](#ecpg-informix-sqlda-reserved) <a href="#ecpg-informix-sqlda-reserved" id="ecpg-informix-sqlda-reserved"></a>

未使用的指標，內容為 NULL。為了與 Informix 相容而保留。

各欄位的屬性如下，它們儲存在 `sqlvar` 陣列中：

<a id="ECPG-INFORMIX-SQLDA-SQLTYPE"></a>

### `sqltype` [#](#ecpg-informix-sqlda-sqltype) <a href="#ecpg-informix-sqlda-sqltype" id="ecpg-informix-sqlda-sqltype"></a>

欄位的型別。常數定義在 `sqltypes.h` 中

<a id="ECPG-INFORMIX-SQLDA-SQLLEN"></a>

### `sqllen` [#](#ecpg-informix-sqlda-sqllen) <a href="#ecpg-informix-sqlda-sqllen" id="ecpg-informix-sqlda-sqllen"></a>

欄位資料的長度。

<a id="ECPG-INFORMIX-SQLDA-SQLDATA"></a>

### `sqldata` [#](#ecpg-informix-sqlda-sqldata) <a href="#ecpg-informix-sqlda-sqldata" id="ecpg-informix-sqlda-sqldata"></a>

指向欄位資料的指標。此指標的型別為 `char *`，它所指向的資料採二進位格式。範例：

```

    int intval;

    switch (sqldata->sqlvar[i].sqltype)
    {
        case SQLINTEGER:
            intval = *(int *)sqldata->sqlvar[i].sqldata;
            break;
      ...
    }
```

<a id="ECPG-INFORMIX-SQLDA-SQLIND"></a>

### `sqlind` [#](#ecpg-informix-sqlda-sqlind) <a href="#ecpg-informix-sqlda-sqlind" id="ecpg-informix-sqlda-sqlind"></a>

指向 NULL 指示變數的指標。若是由 DESCRIBE 或 FETCH 傳回，它一律是有效的指標。若用作 `EXECUTE ... USING sqlda;` 的輸入，則 NULL 指標值表示此欄位的值不是 NULL。否則，必須正確設定有效的指標與 `sqlitype`。範例：

```

    if (*(int2 *)sqldata->sqlvar[i].sqlind != 0)
        printf("value is NULL\n");
```

<a id="ECPG-INFORMIX-SQLDA-SQLNAME"></a>

### `sqlname` [#](#ecpg-informix-sqlda-sqlname) <a href="#ecpg-informix-sqlda-sqlname" id="ecpg-informix-sqlda-sqlname"></a>

欄位的名稱。以 0 結尾的字串。

<a id="ECPG-INFORMIX-SQLDA-SQLFORMAT"></a>

### `sqlformat` [#](#ecpg-informix-sqlda-sqlformat) <a href="#ecpg-informix-sqlda-sqlformat" id="ecpg-informix-sqlda-sqlformat"></a>

在 Informix 中為保留欄位；此處為該欄位的 [`PQfformat`](../libpq/libpq-exec.md#LIBPQ-PQFFORMAT) 值。

<a id="ECPG-INFORMIX-SQLDA-SQLITYPE"></a>

### `sqlitype` [#](#ecpg-informix-sqlda-sqlitype) <a href="#ecpg-informix-sqlda-sqlitype" id="ecpg-informix-sqlda-sqlitype"></a>

NULL 指示變數資料的型別。從伺服器傳回資料時，它一律是 SQLSMINT。當 `SQLDA` 用於參數化查詢時，資料會依所設定的型別處理。

<a id="ECPG-INFORMIX-SQLDA-SQLILEN"></a>

### `sqlilen` [#](#ecpg-informix-sqlda-sqlilen) <a href="#ecpg-informix-sqlda-sqlilen" id="ecpg-informix-sqlda-sqlilen"></a>

NULL 指示變數資料的長度。

<a id="ECPG-INFORMIX-SQLDA-SQLXID"></a>

### `sqlxid` [#](#ecpg-informix-sqlda-sqlxid) <a href="#ecpg-informix-sqlda-sqlxid" id="ecpg-informix-sqlda-sqlxid"></a>

欄位的擴充型別，即 [`PQftype`](../libpq/libpq-exec.md#LIBPQ-PQFTYPE) 的結果。

<a id="ECPG-INFORMIX-SQLDA-SQLTYPENAME"></a>

### `sqltypename`<br>`sqltypelen`<br>`sqlownerlen`<br>`sqlsourcetype`<br>`sqlownername`<br>`sqlsourceid`<br>`sqlflags`<br>`sqlreserved` [#](#ecpg-informix-sqlda-sqltypename) <a href="#ecpg-informix-sqlda-sqltypename" id="ecpg-informix-sqlda-sqltypename"></a>

未使用。

<a id="ECPG-INFORMIX-SQLDA-SQLILONGDATA"></a>

### `sqlilongdata` [#](#ecpg-informix-sqlda-sqlilongdata) <a href="#ecpg-informix-sqlda-sqlilongdata" id="ecpg-informix-sqlda-sqlilongdata"></a>

若 `sqllen` 大於 32kB，它會等於 `sqldata`。

範例：

```

EXEC SQL INCLUDE sqlda.h;

    sqlda_t        *sqlda; /* This doesn't need to be under embedded DECLARE SECTION */

    EXEC SQL BEGIN DECLARE SECTION;
    char *prep_stmt = "select * from table1";
    int i;
    EXEC SQL END DECLARE SECTION;

    ...

    EXEC SQL PREPARE mystmt FROM :prep_stmt;

    EXEC SQL DESCRIBE mystmt INTO sqlda;

    printf("# of fields: %d\n", sqlda->sqld);
    for (i = 0; i < sqlda->sqld; i++)
      printf("field %d: \"%s\"\n", sqlda->sqlvar[i]->sqlname);

    EXEC SQL DECLARE mycursor CURSOR FOR mystmt;
    EXEC SQL OPEN mycursor;
    EXEC SQL WHENEVER NOT FOUND GOTO out;

    while (1)
    {
      EXEC SQL FETCH mycursor USING sqlda;
    }

    EXEC SQL CLOSE mycursor;

    free(sqlda); /* The main structure is all to be free(),
                  * sqlda and sqlda->sqlvar is in one allocated area */
```

譯註：上方範例程式碼依原文保留，僅在此說明幾點：一是迴圈中 printf 的格式字串含有兩個轉換規格（%d 與 %s），卻只傳入一個引數，缺少欄位序號 i；二是 sqlvar 是指向 struct sqlvar_compat 的指標，sqlda->sqlvar[i] 本身是結構而非指標，因此應寫作 sqlda->sqlvar[i].sqlname（與前文 sqldata 範例的寫法一致），而不是 sqlda->sqlvar[i]->sqlname；也就是說，該行應以 i 與 sqlda->sqlvar[i].sqlname 兩個引數呼叫 printf。此外，WHENEVER NOT FOUND GOTO out 所指的標籤 out 並未出現在摘錄中，實際使用時須自行定義。

更多資訊請參閱 `sqlda.h` 標頭檔與 `src/interfaces/ecpg/test/compat_informix/sqlda.pgc` 迴歸測試。

[返回 34.15. Informix 相容模式](ecpg-informix-compat.md#ecpg-informix-compat)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-informix-compat.html)（原文版本：18.6；核對日期：2026-10-22）
