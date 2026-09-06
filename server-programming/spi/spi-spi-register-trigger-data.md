<a id="id-1.8.12.8.33.1"></a><a id="id-1.8.12.8.33.2"></a><a id="id-1.8.12.8.33.3"></a>

## SPI_register_trigger_data

SPI_register_trigger_data — 讓 SPI 查詢可使用暫時性觸發程序資料

## 語法

```

int SPI_register_trigger_data(TriggerData *tdata)
```

<a id="id-1.8.12.8.33.7"></a>

## 說明

`SPI_register_trigger_data` 讓觸發程序擷取的任何暫時性關聯可供透過目前 SPI 連線規劃及執行的查詢使用。目前，這表示透過 `REFERENCING OLD/NEW TABLE AS` ... 子句所定義的 `AFTER` 觸發程序擷取的轉換資料表。PL 觸發程序處理函式應在連線後呼叫此函式。

<a id="id-1.8.12.8.33.8"></a>

## 引數

`TriggerData *tdata`
:   作為 `fcinfo->context` 傳遞至觸發程序處理函式的 `TriggerData` 物件

<a id="id-1.8.12.8.33.9"></a>

## 回傳值

命令成功執行時會回傳下列非負值：

`SPI_OK_TD_REGISTER`
:   已成功註冊擷取的觸發程序資料（若有）

發生錯誤時，會回傳下列其中一個負值：

`SPI_ERROR_ARGUMENT`
:   *`tdata`* 為 `NULL`

`SPI_ERROR_UNCONNECTED`
:   從未連線的 C 函式呼叫

`SPI_ERROR_REL_DUPLICATE`
:   任何觸發程序資料暫時性關聯的名稱已為此連線註冊

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-register-trigger-data.html)（原文版本：18.6；核對日期：2026-09-06）
