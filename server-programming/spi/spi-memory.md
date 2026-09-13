<a id="SPI-MEMORY"></a>

## 45.3. 記憶體管理 [#](#SPI-MEMORY)

[SPI_palloc](spi-spi-palloc.md) — 在上層執行器記憶體內容中配置記憶體

[SPI_repalloc](spi-realloc.md) — 在上層執行器記憶體內容中重新配置記憶體

[SPI_pfree](spi-spi-pfree.md) — 釋放上層執行器記憶體內容中的記憶體

[SPI_copytuple](spi-spi-copytuple.md) — 在上層執行器記憶體內容中複製一個資料列

[SPI_returntuple](spi-spi-returntuple.md) — 準備以 Datum 形式回傳一個 tuple（值組）

[SPI_modifytuple](spi-spi-modifytuple.md) — 以取代指定資料列中某些欄位的方式建立一個資料列

[SPI_freetuple](spi-spi-freetuple.md) — 釋放在上層執行器記憶體內容中配置的資料列

[SPI_freetuptable](spi-spi-freetupletable.md) — 釋放由 `SPI_execute` 或類似函式所建立的資料列集合

[SPI_freeplan](spi-spi-freeplan.md) — 釋放先前儲存的預備陳述式

<a id="id-1.8.12.10.2.1"></a>
PostgreSQL 會在*記憶體內容*（memory context）中配置記憶體，這提供了一種便利的方式，用來管理散布在許多不同地方、且存活時間各不相同的記憶體配置。銷毀一個記憶體內容就會釋放其中配置的所有記憶體。因此，為了避免記憶體洩漏，並不需要逐一追蹤個別物件；只要管理數量相對少的幾個記憶體內容即可。`palloc` 與相關的函式會從「目前的」記憶體內容中配置記憶體。

`SPI_connect` 會建立一個新的記憶體內容，並把它設為目前的記憶體內容。`SPI_finish` 則會還原先前的目前記憶體內容，並銷毀由 `SPI_connect` 所建立的那個記憶體內容。這些動作可確保在你的 C 函式內部所做的暫時性記憶體配置會在 C 函式結束時回收，避免記憶體洩漏。

然而，如果你的 C 函式需要回傳一個位於已配置記憶體中的物件（例如某個傳參照型別的值），你就不能用 `palloc` 來配置那塊記憶體——至少在你仍與 SPI 連線時不行。如果你這麼做，該物件會被 `SPI_finish` 釋放掉，你的 C 函式也就無法可靠運作。要解決這個問題，請改用 `SPI_palloc` 為你要回傳的物件配置記憶體。`SPI_palloc` 會在「上層執行器記憶體內容」中配置記憶體，也就是呼叫 `SPI_connect` 時的那個目前記憶體內容，而那正好就是適合用來存放 C 函式回傳值的記憶體內容。本節所介紹的其他幾個工具函式，同樣會回傳在上層執行器記憶體內容中建立的物件。

當 `SPI_connect` 被呼叫時，由 `SPI_connect` 所建立、屬於該 C 函式的私有記憶體內容會成為目前的記憶體內容。所有由 `palloc`、`repalloc` 或 SPI 工具函式所做的配置（本節所述的例外情況除外）都會落在這個記憶體內容中。當 C 函式（透過 `SPI_finish`）與 SPI 管理器中斷連線時，目前的記憶體內容會還原成上層執行器記憶體內容，而所有在該 C 函式記憶體內容中所做的配置都會被釋放，不能再使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-memory.html)（原文版本：18.6；核對日期：2026-09-12）
