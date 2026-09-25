<a id="ROUTINE-REINDEX"></a>

## 24.2. 例行重新建立索引 [#](#ROUTINE-REINDEX)

<a id="id-1.6.11.11.2"></a>

在某些情況下，值得定期使用 [REINDEX](../../reference/sql-commands/sql-reindex.md) 指令，
或透過一連串個別的重建步驟，來重新建立索引。

已經完全變空的 B-tree 索引頁面會被回收以供重複使用。
不過，仍然有可能發生空間使用效率不佳的情況：如果某個頁面上
除了少數幾個索引鍵之外都已被刪除，這個頁面仍然會保持已配置狀態。因此，在某種使用
模式下，如果每個範圍內的索引鍵最終大多數（但不是全部）都會被刪除，
就會出現空間使用效率不佳的情形。對於這類使用模式，
建議定期重新建立索引。

非 B-tree 索引發生膨脹的可能性目前尚未有充分的研究。使用任何非
B-tree 索引型別時，最好定期監控索引的實體大小。

此外，對於 B-tree 索引來說，剛建立好的索引，其存取速度會比已經歷多次更新的索引
稍快，因為在新建立的索引中，邏輯上相鄰的頁面通常在實體上也是相鄰的。
（這項考量不適用於非 B-tree 索引。）單純為了提升存取速度而
定期重新建立索引，可能也是值得的。

[REINDEX](../../reference/sql-commands/sql-reindex.md) 在所有情況下都可以安全且輕易地使用。
這個指令預設會要求 `ACCESS EXCLUSIVE` 鎖定，因此通常較
適合搭配其 `CONCURRENTLY` 選項來執行，此選項只需要
`SHARE UPDATE EXCLUSIVE` 鎖定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/routine-reindex.html)（原文版本：18.6；核對日期：2026-09-25）
