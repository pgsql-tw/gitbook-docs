<a id="id-1.8.12.8.23.1"></a>

## SPI_cursor_find

SPI_cursor_find — 依名稱尋找既有游標

## 語法

```

Portal SPI_cursor_find(const char * name)
```

<a id="id-1.8.12.8.23.5"></a>

## 說明

`SPI_cursor_find` 會依名稱尋找既有的 portal。這主要用於解析其他函式以文字回傳的游標名稱。

<a id="id-1.8.12.8.23.6"></a>

## 引數

`const char * name`
:   portal 的名稱

<a id="id-1.8.12.8.23.7"></a>

## 回傳值

指向指定名稱之 portal 的指標；若找不到則回傳 `NULL`。

<a id="id-1.8.12.8.23.8"></a>

## 注意事項

請注意，此函式可能回傳不具游標特性的 `Portal` 物件，例如它可能不會回傳資料列。若只是將 `Portal` 指標傳給其他 SPI 函式，這些函式能自行處理此類情況；但直接檢查 `Portal` 時仍應謹慎。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-find.html)（原文版本：18.6；核對日期：2026-09-07）
