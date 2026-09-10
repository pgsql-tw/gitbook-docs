<a id="id-1.8.12.8.31.1"></a><a id="id-1.8.12.8.31.2"></a>

## SPI_register_relation

SPI_register_relation — 讓 SPI 查詢可依名稱使用暫時具名關聯

## 語法

```

int SPI_register_relation(EphemeralNamedRelation enr)
```

<a id="id-1.8.12.8.31.6"></a>

## 說明

`SPI_register_relation` 會讓目前 SPI 連線規劃及執行的查詢，可使用暫時具名關聯及其相關資訊。

<a id="id-1.8.12.8.31.7"></a>

## 引數

`EphemeralNamedRelation enr`
:   暫時具名關聯登錄項目。

<a id="id-1.8.12.8.31.8"></a>

## 回傳值

命令成功執行時會傳回下列非負值：

`SPI_OK_REL_REGISTER`
:   關聯已依名稱成功登錄。

發生錯誤時會傳回下列其中一個負值：

`SPI_ERROR_ARGUMENT`
:   *`enr`* 或其 `name` 欄位為 `NULL`。

`SPI_ERROR_UNCONNECTED`
:   從未連線的 C 函式呼叫。

`SPI_ERROR_REL_DUPLICATE`
:   *`enr`* 的 `name` 欄位指定名稱已為此連線登錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-register-relation.html)（原文版本：18.6；核對日期：2026-09-10）
