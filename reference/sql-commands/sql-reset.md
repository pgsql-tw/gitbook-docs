<a id="id-1.9.3.165.1"></a>

## RESET

RESET — 將某個執行期參數的值還原為預設值

## 語法

```

RESET configuration_parameter
RESET ALL
```

<a id="id-1.9.3.165.5"></a>

## 說明

`RESET` 會將執行期參數還原為其
預設值。`RESET` 是以下寫法的
另一種寫法：

```

SET configuration_parameter TO DEFAULT
```

詳情請參閱 [SET](sql-set.md)。

預設值的定義是：假如在目前工作階段中，從未對該參數執行過
`SET`，該參數原本應有的值。這個值的實際來源，可能是編譯內建的預設值、組態檔、命令列選項，或是各資料庫或各使用者的預設設定。這與定義為「工作階段開始時該參數的值」略有不同，因為如果該值來自組態檔，它會被還原為組態檔目前所指定的值。詳情請參閱
[第 19 章](../../server-administration/runtime-config/README.md)。

`RESET` 的交易行為與
`SET` 相同：其效果會因交易回復而被撤銷。

<a id="id-1.9.3.165.6"></a>

## 參數

*`configuration_parameter`*
:   可設定的執行期參數名稱。可用的參數記載於
    [第 19 章](../../server-administration/runtime-config/README.md) 以及
    [SET](sql-set.md) 參考頁面。

`ALL`
:   將所有可設定的執行期參數重設為預設值。

<a id="id-1.9.3.165.7"></a>

## 範例

將 `timezone` 組態變數設為其預設值：

```

RESET timezone;
```

<a id="id-1.9.3.165.8"></a>

## 相容性

`RESET` 是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.165.9"></a>

## 另請參閱

[SET](sql-set.md), [SHOW](sql-show.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-reset.html)（原文版本：18.6；核對日期：2026-09-28）
