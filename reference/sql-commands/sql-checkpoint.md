<a id="SQL-CHECKPOINT"></a><a id="id-1.9.3.49.1"></a>

## CHECKPOINT

CHECKPOINT — 強制執行預寫式日誌檢查點

<a id="id-1.9.3.49.4"></a>

## 語法

```

CHECKPOINT
```

<a id="id-1.9.3.49.5"></a>

## 說明

檢查點是預寫式日誌序列中的一個時間點，在該點上，所有資料檔都已更新以反映日誌中的資訊。所有資料檔都會被寫入（flush）到磁碟。關於檢查點期間會發生哪些事的更多細節，請參閱[第 28.5 節](../../server-administration/wal/wal-configuration.md)。

`CHECKPOINT` 命令會在下達命令時強制立即執行檢查點，而不等待系統排定的定期檢查點（由[第 19.5.2 節](../../server-administration/runtime-config/runtime-config-wal.md#runtime-config-wal-checkpoints)中的設定控制）。`CHECKPOINT` 並非設計給正常運作期間使用。

若在復原期間執行，`CHECKPOINT` 命令會強制執行重新啟動點（請參閱[第 28.5 節](../../server-administration/wal/wal-configuration.md)），而不是寫入新的檢查點。

只有超級使用者或擁有 [pg_checkpoint](../../server-administration/user-manag/predefined-roles.md#PREDEFINED-ROLE-PG-CHECKPOINT) 角色權限的使用者，才能呼叫 `CHECKPOINT`。

<a id="id-1.9.3.49.6"></a>

## 相容性

`CHECKPOINT` 命令是 PostgreSQL 的語言擴充。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-checkpoint.html)（原文版本：18.6；核對日期：2026-10-04）
