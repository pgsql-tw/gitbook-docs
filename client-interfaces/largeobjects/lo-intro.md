## 33.1. 簡介 [#](#LO-INTRO)

<a id="id-1.7.4.6.2"></a>

所有大型物件都儲存在名為 [`pg_largeobject`](../../internals/catalogs/catalog-pg-largeobject.md) 的單一系統資料表中。每個大型物件在系統資料表 [`pg_largeobject_metadata`](../../internals/catalogs/catalog-pg-largeobject-metadata.md) 中也有一筆項目。你可以透過類似標準檔案操作的讀寫 API，建立、修改及刪除大型物件。

PostgreSQL 也支援稱為 [「TOAST」](../../internals/storage/storage-toast.md) 的儲存系統，會自動將大於單一資料庫頁面的值，存入各資料表的次要儲存區。這使大型物件功能的部分用途已被取代。大型物件仍有一項優勢：它允許最大 4 TB 的值，而使用 TOAST 的欄位最多只能有 1 GB。此外，大型物件的局部讀取與更新可以有效率地執行，而 TOAST 欄位的大多數操作會將整個值視為一個單位來讀寫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/lo-intro.html)（原文版本：18.6；核對日期：2026-09-07）
