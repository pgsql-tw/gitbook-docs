<a id="ECPG-PGTYPES-DECIMAL"></a>

## 34.6.6. decimal 型別 [#](#ecpg-pgtypes-decimal) <a href="#ecpg-pgtypes-decimal" id="ecpg-pgtypes-decimal"></a>

decimal 型別與 numeric 型別相似，但其精確度上限為 30 位有效數字。numeric 型別只能建立在堆積上；相對地，decimal 型別既可以建立在堆疊上，也可以建立在堆積上（透過 `PGTYPESdecimal_new` 與 `PGTYPESdecimal_free` 函式）。在[第 34.15 節](ecpg-informix-compat.md)所述的 Informix 相容模式中，還有許多其他處理 decimal 型別的函式。

下列函式可用來處理 decimal 型別，而且不只包含在 `libcompat` 函式庫中。

<a id="ECPG-PGTYPES-DECIMAL-NEW"></a>

### `PGTYPESdecimal_new` [#](#ecpg-pgtypes-decimal-new) <a href="#ecpg-pgtypes-decimal-new" id="ecpg-pgtypes-decimal-new"></a>

取得指向新配置之 decimal 變數的指標。

```

    decimal *PGTYPESdecimal_new(void);
```

<a id="ECPG-PGTYPES-DECIMAL-FREE"></a>

### `PGTYPESdecimal_free` [#](#ecpg-pgtypes-decimal-free) <a href="#ecpg-pgtypes-decimal-free" id="ecpg-pgtypes-decimal-free"></a>

釋放 decimal 型別，釋放它所有的記憶體。

```

    void PGTYPESdecimal_free(decimal *var);
```

[返回 34.6. pgtypes 函式庫](ecpg-pgtypes.md#ecpg-pgtypes)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
