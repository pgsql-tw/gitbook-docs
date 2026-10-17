<a id="STORAGE-VM"></a>

## 66.4. 可見性對應表 [#](#STORAGE-VM)

<a id="id-1.10.18.6.2"></a><a id="id-1.10.18.6.3"></a>

每個堆積關聯都有一個可見性對應表（Visibility Map，VM），用來追蹤哪些頁面只包含已知對所有作用中交易皆可見的元組；它也會追蹤哪些頁面只包含已凍結的元組。它與主要關聯資料一同儲存在獨立的關聯 fork 中，名稱為關聯的 filenode 編號加上 `_vm` 後綴。例如，若關聯的 filenode 為 12345，VM 就儲存在與主要關聯檔案相同目錄中、名為 `12345_vm` 的檔案。請注意，索引沒有 VM。

可見性對應表為每個堆積頁面儲存兩個位元。第一個位元若已設定，表示該頁面為全部可見（all-visible），換句話說，該頁面不包含任何需要清理（vacuum）的元組。[*僅索引掃描*](../../the-sql-language/indexes/indexes-index-only-scans.md)也可以利用這項資訊，只使用索引元組來回答查詢。第二個位元若已設定，表示該頁面上的所有元組都已凍結。這代表即使是防回捲（anti-wraparound）的清理，也不需要再次造訪該頁面。

這個對應表是保守的：我們確保每當某個位元被設定時，都已知該條件成立；但若某個位元未設定，該條件可能成立，也可能不成立。可見性對應表的位元只會由清理作業設定，但頁面上任何修改資料的操作都會清除這些位元。

[pg_visibility](../../appendixes/contrib/pgvisibility.md) 模組可以用來檢查可見性對應表中所儲存的資訊。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-vm.html)（原文版本：18.6；核對日期：2026-10-12）
