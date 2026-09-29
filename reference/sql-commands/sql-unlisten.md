<a id="id-1.9.3.182.1"></a>

## UNLISTEN

UNLISTEN — 停止接聽某個通知頻道

<a id="id-1.9.3.182.2"></a>

## 語法

```

UNLISTEN { channel | * }
```

<a id="id-1.9.3.182.5"></a>

## 說明

`UNLISTEN` 用來移除既有的
`NOTIFY` 事件註冊。
`UNLISTEN` 會取消目前 PostgreSQL 工作階段
作為指定 *`channel`*
通知頻道的接聽者的既有註冊。特殊萬用字元
`*` 會取消目前工作階段的所有接聽註冊。

[NOTIFY](sql-notify.md)
針對 `LISTEN` 與
`NOTIFY` 的使用方式有更詳盡的討論。

<a id="id-1.9.3.182.6"></a>

## 參數

*`channel`*
:   通知頻道的名稱（任意識別字）。

`*`
:   清除此工作階段的所有目前接聽註冊。

<a id="id-1.9.3.182.7"></a>

## 注意事項

你可以對未曾接聽的頻道執行 unlisten，不會出現任何警告或錯誤。

每個工作階段結束時，都會自動執行 `UNLISTEN *`。

已執行過 `UNLISTEN` 的交易無法被準備用於
兩階段提交。

<a id="id-1.9.3.182.8"></a>

## 範例

建立一個註冊：

```

LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

一旦執行了 `UNLISTEN`，之後的 `NOTIFY`
訊息就會被忽略：

```

UNLISTEN virtual;
NOTIFY virtual;
-- no NOTIFY event is received
```

<a id="id-1.9.3.182.9"></a>

## 相容性

SQL 標準中沒有 `UNLISTEN` 指令。

<a id="id-1.9.3.182.10"></a>

## 參見

[LISTEN](sql-listen.md), [NOTIFY](sql-notify.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-unlisten.html)（原文版本：18.6；核對日期：2026-09-28）
