<a id="id-1.8.12.10.13.1"></a>

## SPI_freetuptable

SPI_freetuptable — 釋放由 `SPI_execute` 或類似函式建立的資料列集

## 語法

```

void SPI_freetuptable(SPITupleTable * tuptable)
```

<a id="id-1.8.12.10.13.5"></a>

## 說明

`SPI_freetuptable` 會釋放先前由 `SPI_execute` 等 SPI 命令執行函式建立的資料列集。因此，此函式常以全域變數 `SPI_tuptable` 作為引數呼叫。

若使用 SPI 的 C 函式需要執行多個命令，且不想保留先前命令的結果直到結束，此函式便很有用。任何未釋放的資料列集都會在 `SPI_finish` 時釋放。此外，若使用 SPI 的 C 函式執行期間啟動後又中止子交易，SPI 會自動釋放子交易執行時建立的資料列集。

自 PostgreSQL 9.3 起，`SPI_freetuptable` 包含保護邏輯，以防對相同資料列集重複要求刪除。較舊版本中，重複刪除會導致當機。

<a id="id-1.8.12.10.13.6"></a>

## 引數

`SPITupleTable * tuptable`
:   指向要釋放資料列集的指標；為 NULL 時不執行任何動作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-freetupletable.html)（原文版本：18.6；核對日期：2026-09-10）
