## 22.4. 資料庫設定 [#](#MANAGE-AG-CONFIG)

如[第 19 章](../runtime-config/README.md)所述，PostgreSQL 伺服器提供許多執行時期設定變數。其中許多設定都可以指定個別資料庫的預設值。

例如，若基於某種原因，想為某個資料庫停用 GEQO 最佳化器，通常必須對所有資料庫都停用它，或確保每個連線的用戶端都確實執行 `SET geqo TO off`。若要讓此設定成為特定資料庫的預設值，可以執行：

```

ALTER DATABASE mydb SET geqo TO off;
```

這會儲存設定（但不會立即套用）。之後連線至此資料庫時，效果就如同在工作階段開始前執行了 `SET geqo TO off;`。請注意，使用者仍可在工作階段中變更此設定；它只是預設值。若要取消這類設定，請使用 `ALTER DATABASE dbname RESET varname`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-config.html)（原文版本：18.6；核對日期：2026-09-07）
