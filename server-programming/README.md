# 第五部分：伺服器程式設計

<a id="id-1.8.2"></a>

本篇說明如何以使用者定義函式、資料型別、觸發程序等方式擴充伺服器功能。
這些是進階主題，應僅在已理解 PostgreSQL 其他所有使用手冊的內容之後，
才開始閱讀本篇。本篇後續章節說明 PostgreSQL 發行版中提供的伺服器端
程式語言，以及伺服器端程式設計的一般性議題。在深入研究伺服器端
程式設計的內容之前，務必至少先閱讀[第 36 章](extend/README.md)
（說明函式）的前幾節。

**目錄**

[36. 擴充 SQL](extend/README.md)
:   [36.1. 可擴充性如何運作](extend/extend-how.md)

    [36.2. PostgreSQL 型別系統](extend/extend-type-system.md)

    [36.3. 使用者定義函式](extend/xfunc.md)

    [36.4. 使用者定義程序](extend/xproc.md)

    [36.5. 查詢語言（SQL）函式](extend/xfunc-sql.md)

    [36.6. 函式多載](extend/xfunc-overload.md)

    [36.7. 函式揮發性分類](extend/xfunc-volatility.md)

    [36.8. 程序語言函式](extend/xfunc-pl.md)

    [36.9. 內部函式](extend/xfunc-internal.md)

    [36.10. C 語言函式](extend/xfunc-c.md)

    [36.11. 函式最佳化資訊](extend/xfunc-optimization.md)

    [36.12. 使用者定義聚合](extend/xaggr.md)

    [36.13. 使用者定義型別](extend/xtypes.md)

    [36.14. 使用者定義運算子](extend/xoper.md)

    [36.15. 運算子最佳化資訊](extend/xoper-optimization.md)

    [36.16. 將擴充功能介接到索引](extend/xindex.md)

    [36.17. 將相關物件封裝為擴充功能](extend/extend-extensions.md)

    [36.18. 擴充功能建置基礎架構](extend/extend-pgxs.md)

[37. 觸發程序](triggers/README.md)
:   [37.1. 觸發程序行為概述](triggers/trigger-definition.md)

    [37.2. 資料異動的可見性](triggers/trigger-datachanges.md)

    [37.3. 以 C 撰寫觸發程序函式](triggers/trigger-interface.md)

    [37.4. 完整的觸發程序範例](triggers/trigger-example.md)

[38. 事件觸發程序](event-triggers/README.md)
:   [38.1. 事件觸發程序行為概觀](event-triggers/event-trigger-definition.md)

    [38.2. 以 C 撰寫事件觸發程序函式](event-triggers/event-trigger-interface.md)

    [38.3. 完整的事件觸發程序範例](event-triggers/event-trigger-example.md)

    [38.4. 資料表重寫事件觸發程序範例](event-triggers/event-trigger-table-rewrite-example.md)

    [38.5. 資料庫登入事件觸發程序範例](event-triggers/event-trigger-database-login-example.md)

[39. 規則系統](rules/README.md)
:   [39.1. 查詢樹](rules/querytree.md)

    [39.2. 檢視表與規則系統](rules/rules-views.md)

    [39.3. 具體化檢視表](rules/rules-materializedviews.md)

    [39.4. `INSERT`、`UPDATE` 與 `DELETE` 上的規則](rules/rules-update.md)

    [39.5. 規則與權限](rules/rules-privileges.md)

    [39.6. 規則與指令狀態](rules/rules-status.md)

    [39.7. 規則與觸發程序的比較](rules/rules-triggers.md)

[40. 程序語言](xplang/README.md)
:   [40.1. 安裝程序語言](xplang/xplang-install.md)

[41. PL/pgSQL — SQL 程序語言](plpgsql/README.md)
:   [41.1. 概觀](plpgsql/plpgsql-overview.md)

    [41.2. PL/pgSQL 的結構](plpgsql/plpgsql-structure.md)

    [41.3. 宣告](plpgsql/plpgsql-declarations.md)

    [41.4. 運算式](plpgsql/plpgsql-expressions.md)

    [41.5. 基本陳述式](plpgsql/plpgsql-statements.md)

    [41.6. 控制結構](plpgsql/plpgsql-control-structures.md)

    [41.7. 游標](plpgsql/plpgsql-cursors.md)

    [41.8. 交易管理](plpgsql/plpgsql-transactions.md)

    [41.9. 錯誤與訊息](plpgsql/plpgsql-errors-and-messages.md)

    [41.10. 觸發程序函式](plpgsql/plpgsql-trigger.md)

    [41.11. PL/pgSQL 內部運作原理](plpgsql/plpgsql-implementation.md)

    [41.12. PL/pgSQL 開發技巧](plpgsql/plpgsql-development-tips.md)

    [41.13. 從 Oracle PL/SQL 移植](plpgsql/plpgsql-porting.md)

[42. PL/Tcl — Tcl 程序語言](pltcl/README.md)
:   [42.1. 概述](pltcl/pltcl-overview.md)

    [42.2. PL/Tcl 函式與引數](pltcl/pltcl-functions.md)

    [42.3. PL/Tcl 中的資料值](pltcl/pltcl-data.md)

    [42.4. PL/Tcl 中的全域資料](pltcl/pltcl-global.md)

    [42.5. 從 PL/Tcl 存取資料庫](pltcl/pltcl-dbaccess.md)

    [42.6. PL/Tcl 中的觸發程序函式](pltcl/pltcl-trigger.md)

    [42.7. PL/Tcl 中的事件觸發程序函式](pltcl/pltcl-event-trigger.md)

    [42.8. PL/Tcl 中的錯誤處理](pltcl/pltcl-error-handling.md)

    [42.9. PL/Tcl 中明確的子交易](pltcl/pltcl-subtransactions.md)

    [42.10. 交易管理](pltcl/pltcl-transactions.md)

    [42.11. PL/Tcl 設定](pltcl/pltcl-config.md)

    [42.12. Tcl 程序名稱](pltcl/pltcl-procnames.md)

[43. PL/Perl — Perl 程序語言](plperl/README.md)
:   [43.1. PL/Perl 函式與引數](plperl/plperl-funcs.md)

    [43.2. PL/Perl 中的資料值](plperl/plperl-data.md)

    [43.3. 內建函式](plperl/plperl-builtins.md)

    [43.4. PL/Perl 中的全域值](plperl/plperl-global.md)

    [43.5. 受信任與不受信任的 PL/Perl](plperl/plperl-trusted.md)

    [43.6. PL/Perl 觸發程序](plperl/plperl-triggers.md)

    [43.7. PL/Perl 事件觸發程序](plperl/plperl-event-triggers.md)

    [43.8. PL/Perl 內部運作原理](plperl/plperl-under-the-hood.md)

[44. PL/Python — Python 程序語言](plpython/README.md)
:   [44.1. PL/Python 函式](plpython/plpython-funcs.md)

    [44.2. 資料值](plpython/plpython-data.md)

    [44.3. 共用資料](plpython/plpython-sharing.md)

    [44.4. 匿名程式碼區塊](plpython/plpython-do.md)

    [44.5. 觸發程序函式](plpython/plpython-trigger.md)

    [44.6. 資料庫存取](plpython/plpython-database.md)

    [44.7. 明確的子交易](plpython/plpython-subtransaction.md)

    [44.8. 交易管理](plpython/plpython-transactions.md)

    [44.9. 工具函式](plpython/plpython-util.md)

    [44.10. Python 2 與 Python 3 的比較](plpython/plpython-python23.md)

    [44.11. 環境變數](plpython/plpython-envar.md)

[45. 伺服器程式設計介面](spi/README.md)
:   [45.1. 介面函式](spi/spi-interface.md)

    [45.2. 介面支援函式](spi/spi-interface-support.md)

    [45.3. 記憶體管理](spi/spi-memory.md)

    [45.4. 交易管理](spi/spi-transaction.md)

    [45.5. 資料異動的可見性](spi/spi-visibility.md)

    [45.6. 範例](spi/spi-examples.md)

[46. 背景工作程序](bgworker/README.md)

[47. 邏輯解碼](logicaldecoding/README.md)
:   [47.1. 邏輯解碼範例](logicaldecoding/logicaldecoding-example.md)

    [47.2. 邏輯解碼概念](logicaldecoding/logicaldecoding-explanation.md)

    [47.3. 串流複寫協定介面](logicaldecoding/logicaldecoding-walsender.md)

    [47.4. 邏輯解碼 SQL 介面](logicaldecoding/logicaldecoding-sql.md)

    [47.5. 與邏輯解碼相關的系統目錄](logicaldecoding/logicaldecoding-catalogs.md)

    [47.6. 邏輯解碼輸出外掛](logicaldecoding/logicaldecoding-output-plugin.md)

    [47.7. 邏輯解碼輸出寫入器](logicaldecoding/logicaldecoding-writer.md)

    [47.8. 邏輯解碼的同步複寫支援](logicaldecoding/logicaldecoding-synchronous.md)

    [47.9. 邏輯解碼的大型交易串流](logicaldecoding/logicaldecoding-streaming.md)

    [47.10. 邏輯解碼的兩階段提交支援](logicaldecoding/logicaldecoding-two-phase-commits.md)

[48. 複寫進度追蹤](replication-origins/README.md)

[49. 封存模組](archive-modules/README.md)
:   [49.1. 初始化函式](archive-modules/archive-module-init.md)

    [49.2. 封存模組回呼](archive-modules/archive-module-callbacks.md)

[50. OAuth 驗證器模組](oauth-validators/README.md)
:   [50.1. 安全地設計驗證器模組](oauth-validators/oauth-validator-design.md)

    [50.2. 初始化函式](oauth-validators/oauth-validator-init.md)

    [50.3. OAuth 驗證器回呼](oauth-validators/oauth-validator-callbacks.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/server-programming.html)（原文版本：18.6；核對日期：2026-09-26）
