<a id="SQL-DISCARD"></a><a id="id-1.9.3.101.1"></a>

## DISCARD

DISCARD — 捨棄工作階段狀態

<a id="id-1.9.3.101.4"></a>

## 語法

```

DISCARD { ALL | PLANS | SEQUENCES | TEMPORARY | TEMP }
```

<a id="id-1.9.3.101.5"></a>

## 說明

`DISCARD` 會釋放與資料庫工作階段相關聯的內部資源。此命令可用於部分或完全重設工作階段的狀態。有數個子命令可分別釋放不同類型的資源；`DISCARD ALL` 這個變體涵蓋了其他所有子命令，並且還會重設額外的狀態。

<a id="id-1.9.3.101.6"></a>

## 參數

`PLANS`
:   釋放所有快取的查詢計畫，迫使下次使用相關聯的預備陳述式時重新進行規劃。

`SEQUENCES`
:   捨棄所有快取的序列相關狀態，包括 `currval()`/`lastval()` 資訊，以及任何已預先配置但尚未由 `nextval()` 傳回的序列值。（預先配置序列值的說明請參閱 [CREATE SEQUENCE](sql-createsequence.md)。）

`TEMPORARY` 或 `TEMP`
:   移除目前工作階段中建立的所有暫存資料表。

`ALL`
:   釋放與目前工作階段相關聯的所有暫時性資源，並將工作階段重設為其初始狀態。目前，這與執行下列陳述式序列的效果相同：

    ```

    CLOSE ALL;
    SET SESSION AUTHORIZATION DEFAULT;
    RESET ALL;
    DEALLOCATE ALL;
    UNLISTEN *;
    SELECT pg_advisory_unlock_all();
    DISCARD PLANS;
    DISCARD TEMP;
    DISCARD SEQUENCES;
    ```

<a id="id-1.9.3.101.7"></a>

## 注意事項

`DISCARD ALL` 不能在交易區塊內執行。

<a id="id-1.9.3.101.8"></a>

## 相容性

`DISCARD` 是 PostgreSQL 擴充功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-discard.html)（原文版本：18.6；核對日期：2026-10-03）
