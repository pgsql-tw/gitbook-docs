<a id="id-1.8.12.10.6.1"></a>

## SPI_palloc

SPI_palloc — 在上層執行器環境中配置記憶體

## 語法

```

void * SPI_palloc(Size size)
```

<a id="id-1.8.12.10.6.5"></a>

## 說明

`SPI_palloc` 會在上層執行器環境中配置記憶體。

此函式只能在連線至 SPI 時使用，否則會發生錯誤。

<a id="id-1.8.12.10.6.6"></a>

## 引數

`Size size`
:   要配置之儲存空間的大小（以位元組計）

<a id="id-1.8.12.10.6.7"></a>

## 回傳值

指向指定大小的新儲存空間的指標

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-palloc.html)（原文版本：18.6；核對日期：2026-09-10）
