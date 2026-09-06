<a id="ECPG-ORACLE-COMPAT"></a>

# 36.16. Oracle 相容模式

`ecpg` 可在所謂的<em class="firstterm">Oracle 相容模式</em>下執行。此模式啟用時，它會嘗試如同 Oracle Pro&#42;C 一般運作。

具體而言，此模式會從三方面改變 `ecpg`：

* 將接收字串型別的字元陣列以尾端空白填滿至指定長度
* 以零位元組結束這些字元陣列，並在發生截斷時設定指標變數
* 字元陣列接收空字串型別時，將空值指標設為 `-1`

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-oracle-compat.html)
