<a id="EXTEND"></a>

## 第 36 章 擴充 SQL

**目錄**

- [36.1. 可擴充性如何運作](extend-how.md)

- [36.2. PostgreSQL 型別系統](extend-type-system.md)
  - [36.2.1. 基礎型別](extend-type-system.md#extend-type-system-base)

  - [36.2.2. 容器型別](extend-type-system.md#extend-type-system-container)

  - [36.2.3. 網域](extend-type-system.md#extend-type-system-domains)

  - [36.2.4. 虛擬型別](extend-type-system.md#extend-type-system-pseudo)

  - [36.2.5. 多型型別](extend-type-system.md#extend-types-polymorphic)

- [36.3. 使用者定義函式](xfunc.md)

- [36.4. 使用者定義程序](xproc.md)

- [36.5. 查詢語言（SQL）函式](xfunc-sql.md)
  - [36.5.1. SQL 函式的引數](xfunc-sql.md#xfunc-sql-function-arguments)

  - [36.5.2. 基礎型別上的 SQL 函式](xfunc-sql.md#xfunc-sql-base-functions)

  - [36.5.3. 複合型別上的 SQL 函式](xfunc-sql.md#xfunc-sql-composite-functions)

  - [36.5.4. 具有輸出參數的 SQL 函式](xfunc-sql.md#xfunc-output-parameters)

  - [36.5.5. 具有輸出參數的 SQL 程序](xfunc-sql.md#xfunc-output-parameters-proc)

  - [36.5.6. 引數數量可變的 SQL 函式](xfunc-sql.md#xfunc-sql-variadic-functions)

  - [36.5.7. 具有引數預設值的 SQL 函式](xfunc-sql.md#xfunc-sql-parameter-defaults)

  - [36.5.8. 作為資料表來源的 SQL 函式](xfunc-sql.md#xfunc-sql-table-functions)

  - [36.5.9. 傳回集合的 SQL 函式](xfunc-sql.md#xfunc-sql-functions-returning-set)

  - [36.5.10. 傳回 `TABLE` 的 SQL 函式](xfunc-sql.md#xfunc-sql-functions-returning-table)

  - [36.5.11. 多型 SQL 函式](xfunc-sql.md#xfunc-sql-polymorphic-functions)

  - [36.5.12. 具有定序的 SQL 函式](xfunc-sql.md#xfunc-sql-collations)

- [36.6. 函式多載](xfunc-overload.md)

- [36.7. 函式揮發性類別](xfunc-volatility.md)

- [36.8. 程序語言函式](xfunc-pl.md)

- [36.9. 內部函式](xfunc-internal.md)

- [36.10. C 語言函式](xfunc-c.md)
  - [36.10.1. 動態載入](xfunc-c.md#xfunc-c-dynload)

  - [36.10.2. C 語言函式中的基礎型別](xfunc-c.md#xfunc-c-basetype)

  - [36.10.3. 第 1 版呼叫慣例](xfunc-c.md#xfunc-c-v1-call-conv)

  - [36.10.4. 撰寫程式碼](xfunc-c.md#xfunc-c-code)

  - [36.10.5. 編譯與連結動態載入的函式](xfunc-c.md#dfunc)

  - [36.10.6. 伺服器 API 與 ABI 穩定性指引](xfunc-c.md#xfunc-api-abi-stability-guidance)

  - [36.10.7. 複合型別引數](xfunc-c.md#xfunc-c-composite-type-args)

  - [36.10.8. 傳回資料列（複合型別）](xfunc-c.md#xfunc-c-returning-rows)

  - [36.10.9. 傳回集合](xfunc-c.md#xfunc-c-return-set)

  - [36.10.10. 多型引數與傳回型別](xfunc-c.md#xfunc-c-polymorphic)

  - [36.10.11. 共享記憶體](xfunc-c.md#xfunc-shared-addin)

  - [36.10.12. LWLocks](xfunc-c.md#xfunc-addin-lwlocks)

  - [36.10.13. 自訂等待事件](xfunc-c.md#xfunc-addin-wait-events)

  - [36.10.14. 注入點](xfunc-c.md#xfunc-addin-injection-points)

  - [36.10.15. 自訂累積統計資訊](xfunc-c.md#xfunc-addin-custom-cumulative-statistics)

  - [36.10.16. 使用 C++ 進行擴充](xfunc-c.md#extend-cpp)

- [36.11. 函式最佳化資訊](xfunc-optimization.md)

- [36.12. 使用者定義聚合函式](xaggr.md)
  - [36.12.1. 移動聚合模式](xaggr.md#xaggr-moving-aggregates)

  - [36.12.2. 多型與可變數量聚合函式](xaggr.md#xaggr-polymorphic-aggregates)

  - [36.12.3. 有序集合聚合函式](xaggr.md#xaggr-ordered-set-aggregates)

  - [36.12.4. 部分聚合](xaggr.md#xaggr-partial-aggregates)

  - [36.12.5. 聚合函式的支援函式](xaggr.md#xaggr-support-functions)

- [36.13. 使用者定義型別](xtypes.md)
  - [36.13.1. TOAST 考量事項](xtypes.md#xtypes-toast)

- [36.14. 使用者定義運算子](xoper.md)

- [36.15. 運算子最佳化資訊](xoper-optimization.md)
  - [36.15.1. `COMMUTATOR`](xoper-optimization.md#xoper-commutator)

  - [36.15.2. `NEGATOR`](xoper-optimization.md#xoper-negator)

  - [36.15.3. `RESTRICT`](xoper-optimization.md#xoper-restrict)

  - [36.15.4. `JOIN`](xoper-optimization.md#xoper-join)

  - [36.15.5. `HASHES`](xoper-optimization.md#xoper-hashes)

  - [36.15.6. `MERGES`](xoper-optimization.md#xoper-merges)

- [36.16. 將擴充功能與索引介接](xindex.md)
  - [36.16.1. 索引方法與運算子類別](xindex.md#xindex-opclass)

  - [36.16.2. 索引方法策略](xindex.md#xindex-strategies)

  - [36.16.3. 索引方法支援常式](xindex.md#xindex-support)

  - [36.16.4. 範例](xindex.md#xindex-example)

  - [36.16.5. 運算子類別與運算子家族](xindex.md#xindex-opfamily)

  - [36.16.6. 系統對運算子類別的相依性](xindex.md#xindex-opclass-dependencies)

  - [36.16.7. 排序運算子](xindex.md#xindex-ordering-ops)

  - [36.16.8. 運算子類別的特殊功能](xindex.md#xindex-opclass-features)

- [36.17. 將相關物件封裝為擴充功能](extend-extensions.md)
  - [36.17.1. 擴充功能檔案](extend-extensions.md#extend-extensions-files)

  - [36.17.2. 擴充功能可重新定位性](extend-extensions.md#extend-extensions-relocation)

  - [36.17.3. 擴充功能組態資料表](extend-extensions.md#extend-extensions-config-tables)

  - [36.17.4. 擴充功能更新](extend-extensions.md#extend-extensions-updates)

  - [36.17.5. 使用更新指令碼安裝擴充功能](extend-extensions.md#extend-extensions-update-scripts)

  - [36.17.6. 擴充功能的安全考量](extend-extensions.md#extend-extensions-security)

  - [36.17.7. 擴充功能範例](extend-extensions.md#extend-extensions-example)

- [36.18. 擴充功能建置基礎架構](extend-pgxs.md)

<a id="id-1.8.3.2"></a>

在接下來的各節中，我們將討論如何透過加入下列項目，來擴充 PostgreSQL
的 SQL 查詢語言：

* 函式（從[36.3 節](xfunc.md)開始）
* 聚合函式（從[36.12 節](xaggr.md)開始）
* 資料型別（從[36.13 節](xtypes.md)開始）
* 運算子（從[36.14 節](xoper.md)開始）
* 索引用的運算子類別（從[36.16 節](xindex.md)開始）
* 相關物件的套件（從[36.17 節](extend-extensions.md)開始）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/extend.html)（原文版本：18.6；核對日期：2026-09-15）
