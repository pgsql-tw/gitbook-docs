## 66.3. 可用空間對應表 [#](#STORAGE-FSM)

<a id="id-1.10.18.5.2"></a><a id="id-1.10.18.5.3"></a>

除雜湊索引外，每個堆積與索引關聯都有可用空間對應表（FSM），用來追蹤關聯中的可用空間。它會與主要關聯資料一同儲存在獨立關聯 fork 中，名稱為關聯的 filenode 編號加上 `_fsm` 後綴。例如，關聯 filenode 為 12345 時，FSM 儲存在與主要關聯檔案相同目錄的 `12345_fsm` 檔案。

可用空間對應表組織為 FSM 頁面的樹。最底層 FSM 頁面會儲存每個堆積（或索引）頁面可用的空間，每個頁面以一個位元組表示；上層則彙總下層資訊。

每個 FSM 頁面內有一個二元樹，以陣列儲存且每個節點一個位元組。每個葉節點代表堆積頁面或下層 FSM 頁面；非葉節點儲存其子節點較高的值，因此根節點會儲存葉節點中的最大值。

FSM 的結構、更新與搜尋細節請參閱 `src/backend/storage/freespace/README`。可使用 [pg_freespacemap](../../appendixes/contrib/pgfreespacemap.md) 模組檢查可用空間對應表中的資訊。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-fsm.html)（原文版本：18.6；核對日期：2026-09-11）
