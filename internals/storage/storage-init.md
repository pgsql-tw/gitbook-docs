## 66.5. 初始化分支檔案 [#](#STORAGE-INIT)

<a id="id-1.10.18.7.2"></a>

每個不記錄 WAL 的資料表（unlogged table），以及其上的每個索引，都有一個初始化分支檔案（initialization fork）。初始化分支檔案是對應型別的空資料表或空索引。當不記錄 WAL 的資料表因系統當機而必須重設為空時，會將初始化分支檔案複製到主要分支檔案，並刪除其他分支檔案（需要時會自動重新建立）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-init.html)（原文版本：18.6；核對日期：2026-09-07）
