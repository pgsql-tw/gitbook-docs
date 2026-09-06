## 22.5. 刪除資料庫 [#](#MANAGE-AG-DROPDB)

使用 [DROP DATABASE](../../reference/sql-commands/sql-dropdatabase.md) 命令刪除資料庫：<a id="id-1.6.9.8.2.2"></a>

```

DROP DATABASE name;
```

只有資料庫擁有者或超級使用者可以刪除資料庫。刪除資料庫會移除其中包含的所有物件，而且此操作無法復原。

連線至要刪除的資料庫時，不能執行 `DROP DATABASE` 命令。不過，你可以連線至任何其他資料庫，包括 `template1`。若要刪除某個叢集中的最後一個使用者資料庫，`template1` 就是唯一選擇。

為了方便使用，也提供了用來刪除資料庫的 shell 程式 [dropdb](../../reference/reference-client/app-dropdb.md)：<a id="id-1.6.9.8.4.2"></a>

```

dropdb dbname
```

（與 `createdb` 不同，它預設不會刪除與目前使用者同名的資料庫。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-dropdb.html)（原文版本：18.6；核對日期：2026-09-07）
