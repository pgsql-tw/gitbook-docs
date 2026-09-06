<a id="id-1.8.12.8.32.1"></a><a id="id-1.8.12.8.32.2"></a>

## SPI_unregister_relation

SPI_unregister_relation — 從登錄表移除暫時具名關聯

## 語法

```

int SPI_unregister_relation(const char * name)
```

<a id="id-1.8.12.8.32.6"></a>

## 說明

`SPI_unregister_relation` 會從目前連線的登錄表移除暫時具名關聯。

<a id="id-1.8.12.8.32.7"></a>

## 引數

`const char * name`
:   關聯在登錄表中的項目名稱

<a id="id-1.8.12.8.32.8"></a>

## 回傳值

若命令執行成功，會回傳下列非負值：

`SPI_OK_REL_UNREGISTER`
:   已成功從登錄表移除 tuplestore

發生錯誤時，會回傳下列其中一個負值：

`SPI_ERROR_ARGUMENT`
:   *`name`* 為 `NULL`

`SPI_ERROR_UNCONNECTED`
:   從尚未連線的 C 函式呼叫

`SPI_ERROR_REL_NOT_FOUND`
:   在目前連線的登錄表中找不到 *`name`*

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-unregister-relation.html)（原文版本：18.6；核對日期：2026-09-07）
