<a id="DDL"></a>

## 第 5 章 資料定義

**目錄**

- [5.1. 資料表基礎](ddl-basics.md)

- [5.2. 預設值](ddl-default.md)

- [5.3. 識別欄位](ddl-identity-columns.md)

- [5.4. 產生欄位](ddl-generated-columns.md)

- [5.5. 限制條件](ddl-constraints.md)
  - [5.5.1. 檢查限制條件](ddl-constraints.md#ddl-constraints-check-constraints)

  - [5.5.2. 非空值限制條件](ddl-constraints.md#ddl-constraints-not-null)

  - [5.5.3. 唯一限制條件](ddl-constraints.md#ddl-constraints-unique-constraints)

  - [5.5.4. 主鍵](ddl-constraints.md#ddl-constraints-primary-keys)

  - [5.5.5. 外鍵](ddl-constraints.md#ddl-constraints-fk)

  - [5.5.6. 排除限制條件](ddl-constraints.md#ddl-constraints-exclusion)

- [5.6. 系統欄位](ddl-system-columns.md)

- [5.7. 修改資料表](ddl-alter.md)
  - [5.7.1. 新增欄位](ddl-alter.md#ddl-alter-adding-a-column)

  - [5.7.2. 移除欄位](ddl-alter.md#ddl-alter-removing-a-column)

  - [5.7.3. 新增限制條件](ddl-alter.md#ddl-alter-adding-a-constraint)

  - [5.7.4. 移除限制條件](ddl-alter.md#ddl-alter-removing-a-constraint)

  - [5.7.5. 變更欄位的預設值](ddl-alter.md#ddl-alter-column-default)

  - [5.7.6. 變更欄位的資料型別](ddl-alter.md#ddl-alter-column-type)

  - [5.7.7. 重新命名欄位](ddl-alter.md#ddl-alter-renaming-column)

  - [5.7.8. 重新命名資料表](ddl-alter.md#ddl-alter-renaming-table)

- [5.8. 權限](ddl-priv.md)

- [5.9. 資料列安全政策](ddl-rowsecurity.md)

- [5.10. 綱要](ddl-schemas.md)
  - [5.10.1. 建立綱要](ddl-schemas.md#ddl-schemas-create)

  - [5.10.2. public 綱要](ddl-schemas.md#ddl-schemas-public)

  - [5.10.3. 綱要搜尋路徑](ddl-schemas.md#ddl-schemas-path)

  - [5.10.4. 綱要與權限](ddl-schemas.md#ddl-schemas-priv)

  - [5.10.5. 系統目錄綱要](ddl-schemas.md#ddl-schemas-catalog)

  - [5.10.6. 使用模式](ddl-schemas.md#ddl-schemas-patterns)

  - [5.10.7. 可攜性](ddl-schemas.md#ddl-schemas-portability)

- [5.11. 繼承](ddl-inherit.md)
  - [5.11.1. 注意事項](ddl-inherit.md#ddl-inherit-caveats)

- [5.12. 資料表分割](ddl-partitioning.md)
  - [5.12.1. 概觀](ddl-partitioning.md#ddl-partitioning-overview)

  - [5.12.2. 宣告式分割](ddl-partitioning.md#ddl-partitioning-declarative)

  - [5.12.3. 使用繼承進行分割](ddl-partitioning.md#ddl-partitioning-using-inheritance)

  - [5.12.4. 分割區修剪](ddl-partitioning.md#ddl-partition-pruning)

  - [5.12.5. 分割與限制條件排除](ddl-partitioning.md#ddl-partitioning-constraint-exclusion)

  - [5.12.6. 宣告式分割的最佳實務](ddl-partitioning.md#ddl-partitioning-declarative-best-practices)

- [5.13. 外部資料](ddl-foreign-data.md)

- [5.14. 其他資料庫物件](ddl-others.md)

- [5.15. 相依性追蹤](ddl-depend.md)

本章說明如何建立用來存放資料的資料庫結構。在關聯式資料庫中，原始資料存放在資料表裡，因此本章大部分的篇幅都用來說明資料表要如何建立與修改，以及有哪些功能可以用來控制資料表中所存放的資料。接著，我們會討論如何將資料表整理到綱要之中，以及如何為資料表指派權限。最後，我們會簡要地介紹其他會影響資料儲存的功能，例如繼承、資料表分割、檢視表、函式與觸發程序。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl.html)（原文版本：18.6；核對日期：2026-09-15）
