<a id="id-1.8.12.10.7.1"></a>

## SPI_repalloc

SPI_repalloc — 重新配置上層執行器記憶體環境中的記憶體

## 語法

```

void * SPI_repalloc(void * pointer, Size size)
```

<a id="id-1.8.12.10.7.5"></a>

## 說明

`SPI_repalloc` 會變更先前使用 `SPI_palloc` 配置之記憶體區段的大小。

此函式現在與一般的 `repalloc` 沒有差異，僅為了維持既有程式碼的向後相容性而保留。

<a id="id-1.8.12.10.7.6"></a>

## 引數

`void * pointer`
:   指向要變更之既有儲存空間的指標

`Size size`
:   要配置的儲存空間大小，單位為位元組

<a id="id-1.8.12.10.7.7"></a>

## 回傳值

指向指定大小之新儲存空間的指標，其內容已從原有區域複製而來。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-realloc.html)（原文版本：18.6；核對日期：2026-09-07）
