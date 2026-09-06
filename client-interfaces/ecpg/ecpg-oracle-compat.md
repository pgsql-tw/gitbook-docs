## 34.16. Oracle 相容模式 [#](#ECPG-ORACLE-COMPAT)

`ecpg` 可以在所謂的 *Oracle 相容模式*下執行。啟用此模式時，它會嘗試採用與 Oracle Pro\*C 相同的行為。

具體而言，此模式會在三個方面改變 `ecpg` 的行為：

* 字元陣列接收字串型別時，在尾端補上空白，直到指定長度。
* 以零位元組終止這些字元陣列，並在發生截斷時設定指示變數。
* 字元陣列接收空字串型別時，將空值指示變數設為 `-1`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-oracle-compat.html)（原文版本：18.6；核對日期：2026-09-07）
