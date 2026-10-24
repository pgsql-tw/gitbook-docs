<a id="ECPG-SQLDA-SQLNAME"></a>

## 34.7.2.1.3. struct sqlname 結構 [#](#ecpg-sqlda-sqlname) <a href="#ecpg-sqlda-sqlname" id="ecpg-sqlda-sqlname"></a>

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

### `length` [#](#ecpg-sqlda-sqlname-length) <a href="#ecpg-sqlda-sqlname-length" id="ecpg-sqlda-sqlname-length"></a>

包含欄位名稱的長度。

<a id="ECPG-SQLDA-SQLNAME-DATA"></a>

### `data` [#](#ecpg-sqlda-sqlname-data) <a href="#ecpg-sqlda-sqlname-data" id="ecpg-sqlda-sqlname-data"></a>

包含實際的欄位名稱。

[返回 34.7.2. SQLDA 描述區](ecpg-sqlda-descriptors.md#ecpg-sqlda-descriptors)

[返回 34.7.2.1. SQLDA 資料結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-descriptors-sqlda)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
