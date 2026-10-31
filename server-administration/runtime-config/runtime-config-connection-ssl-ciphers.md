# SSL 密碼套件預設值

[返回連線與驗證設定](runtime-config-connection.md)

<a id="GUC-SSL-CIPHERS-HIGH"></a>

## `HIGH` [#](#guc-ssl-ciphers-high) <a href="#guc-ssl-ciphers-high" id="guc-ssl-ciphers-high"></a>

使用 `HIGH` 群組密碼（例如
AES、Camellia、3DES）的密碼套件

<a id="GUC-SSL-CIPHERS-MEDIUM"></a>

## `MEDIUM` [#](#guc-ssl-ciphers-medium) <a href="#guc-ssl-ciphers-medium" id="guc-ssl-ciphers-medium"></a>

使用 `MEDIUM` 群組密碼（例如 RC4、SEED）
的密碼套件

<a id="GUC-SSL-CIPHERS-PLUS-3DES"></a>

## `+3DES` [#](#guc-ssl-ciphers-plus-3des) <a href="#guc-ssl-ciphers-plus-3des" id="guc-ssl-ciphers-plus-3des"></a>

OpenSSL 對 `HIGH` 的預設排序
有問題，因為它將 3DES 排在
AES128 之前。這是錯誤的，因為 3DES 提供的
安全性低於 AES128，而且速度也慢得多。
`+3DES` 會將其重新排序到所有其他
`HIGH` 與 `MEDIUM` 密碼之後。

<a id="GUC-SSL-CIPHERS-NOT-ANULL"></a>

## `!aNULL` [#](#guc-ssl-ciphers-not-anull) <a href="#guc-ssl-ciphers-not-anull" id="guc-ssl-ciphers-not-anull"></a>

停用不進行驗證的匿名密碼套件。這類
密碼套件容易受到中間人（MITM）攻擊，
因此不應使用。

[返回連線與驗證設定](runtime-config-connection.md)

---

本頁內容由父頁分出，沿用其原文版本與核對日期。

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-connection.html)（原文版本：18.6；核對日期：2026-09-24）
