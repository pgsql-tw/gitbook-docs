<a id="id-1.8.12.9.12.1"></a>

## SPI_result_code_string

SPI_result_code_string — 將錯誤碼作為字串傳回

## 語法

```

const char * SPI_result_code_string(int code);
```

<a id="id-1.8.12.9.12.5"></a>

## 說明

`SPI_result_code_string` 傳回各種 SPI 函式所傳回或儲存於 `SPI_result` 的結果碼字串表示法。

<a id="id-1.8.12.9.12.6"></a>

## 引數

`int code`
:   結果碼

<a id="id-1.8.12.9.12.7"></a>

## 回傳值

結果碼的字串表示法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-result-code-string.html)（原文版本：18.6；核對日期：2026-09-06）
