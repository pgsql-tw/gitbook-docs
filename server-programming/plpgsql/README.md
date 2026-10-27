<a id="PLPGSQL"></a>

## 第 41 章 PL/pgSQL — SQL 程序語言

**目錄**

- [41.1. 概觀](plpgsql-overview.md)
  - [41.1.1. 使用 PL/pgSQL 的優點](plpgsql-overview.md#plpgsql-advantages)

  - [41.1.2. 支援的引數與結果資料型別](plpgsql-overview.md#plpgsql-args-results)

- [41.2. PL/pgSQL 的結構](plpgsql-structure.md)

- [41.3. 宣告](plpgsql-declarations.md)
  - [41.3.1. 宣告函式參數](plpgsql-declarations.md#plpgsql-declaration-parameters)

  - [41.3.2. `ALIAS`](plpgsql-declarations.md#plpgsql-declaration-alias)

  - [41.3.3. 複製型別](plpgsql-declarations.md#plpgsql-declaration-type)

  - [41.3.4. 資料列型別](plpgsql-declarations.md#plpgsql-declaration-rowtypes)

  - [41.3.5. Record 型別](plpgsql-declarations.md#plpgsql-declaration-records)

  - [41.3.6. PL/pgSQL 變數的定序](plpgsql-declarations.md#plpgsql-declaration-collation)

- [41.4. 運算式](plpgsql-expressions.md)

- [41.5. 基本陳述式](plpgsql-statements.md)
  - [41.5.1. 指派](plpgsql-statements.md#plpgsql-statements-assignment)

  - [41.5.2. 執行 SQL 指令](plpgsql-statements.md#plpgsql-statements-general-sql)

  - [41.5.3. 執行只回傳單一資料列的指令](plpgsql-statements.md#plpgsql-statements-sql-onerow)

  - [41.5.4. 執行動態指令](plpgsql-statements.md#plpgsql-statements-executing-dyn)

  - [41.5.5. 取得結果狀態](plpgsql-statements.md#plpgsql-statements-diagnostics)

  - [41.5.6. 什麼都不做](plpgsql-statements.md#plpgsql-statements-null)

- [41.6. 控制結構](plpgsql-control-structures.md)
  - [41.6.1. 從函式回傳](plpgsql-control-structures.md#plpgsql-statements-returning)

  - [41.6.2. 從程序回傳](plpgsql-control-structures.md#plpgsql-statements-returning-procedure)

  - [41.6.3. 呼叫程序](plpgsql-control-structures.md#plpgsql-statements-calling-procedure)

  - [41.6.4. 條件判斷](plpgsql-control-structures.md#plpgsql-conditionals)

  - [41.6.5. 簡單迴圈](plpgsql-control-structures.md#plpgsql-control-structures-loops)

  - [41.6.6. 走訪查詢結果](plpgsql-control-structures.md#plpgsql-records-iterating)

  - [41.6.7. 走訪陣列](plpgsql-control-structures.md#plpgsql-foreach-array)

  - [41.6.8. 攔截錯誤](plpgsql-control-structures.md#plpgsql-error-trapping)

  - [41.6.9. 取得執行位置資訊](plpgsql-control-structures.md#plpgsql-call-stack)

- [41.7. 游標](plpgsql-cursors.md)
  - [41.7.1. 宣告游標變數](plpgsql-cursors.md#plpgsql-cursor-declarations)

  - [41.7.2. 開啟游標](plpgsql-cursors.md#plpgsql-cursor-opening)

  - [41.7.3. 使用游標](plpgsql-cursors.md#plpgsql-cursor-using)

  - [41.7.4. 走訪游標的結果](plpgsql-cursors.md#plpgsql-cursor-for-loop)

- [41.8. 交易管理](plpgsql-transactions.md)

- [41.9. 錯誤與訊息](plpgsql-errors-and-messages.md)
  - [41.9.1. 回報錯誤與訊息](plpgsql-errors-and-messages.md#plpgsql-statements-raise)

  - [41.9.2. 檢查斷言](plpgsql-errors-and-messages.md#plpgsql-statements-assert)

- [41.10. 觸發程序函式](plpgsql-trigger.md)
  - [41.10.1. 資料變更的觸發程序](plpgsql-trigger.md#plpgsql-dml-trigger)

  - [41.10.2. 事件的觸發程序](plpgsql-trigger.md#plpgsql-event-trigger)

- [41.11. PL/pgSQL 的內部運作](plpgsql-implementation.md)
  - [41.11.1. 變數替換](plpgsql-implementation.md#plpgsql-var-subst)

  - [41.11.2. 執行計畫快取](plpgsql-implementation.md#plpgsql-plan-caching)

- [41.12. PL/pgSQL 開發技巧](plpgsql-development-tips.md)
  - [41.12.1. 引號的處理](plpgsql-development-tips.md#plpgsql-quote-tips)

  - [41.12.2. 額外的編譯期與執行期檢查](plpgsql-development-tips.md#plpgsql-extra-checks)

- [41.13. 從 Oracle PL/SQL 移植](plpgsql-porting.md)
  - [41.13.1. 移植範例](plpgsql-porting.md#plpgsql-porting-examples)

  - [41.13.2. 其他需要注意的事項](plpgsql-porting.md#plpgsql-porting-other)

  - [41.13.3. 附錄](plpgsql-porting.md#plpgsql-porting-appendix)

<a id="id-1.8.8.2"></a>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql.html)（原文版本：18.6；核對日期：2026-09-13）
