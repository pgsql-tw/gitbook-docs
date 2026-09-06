<a id="id-1.8.12.8.5.1"></a>

## SPI_exec

SPI_exec — 執行讀取／寫入命令

## 語法

```

int SPI_exec(const char * command, long count)
```

<a id="id-1.8.12.8.5.5"></a>

## 說明

`SPI_exec` 與 `SPI_execute` 相同，但後者的 *`read_only`* 參數一律採用 `false`。

<a id="id-1.8.12.8.5.6"></a>

## 引數

`const char * command`
:   包含要執行命令的字串

`long count`
:   要回傳的最大資料列數；`0` 表示不限

<a id="id-1.8.12.8.5.7"></a>

## 回傳值

請參閱 `SPI_execute`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-exec.html)（原文版本：18.6；核對日期：2026-09-06）
