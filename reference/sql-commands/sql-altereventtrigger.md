<a id="SQL-ALTEREVENTTRIGGER"></a><a id="id-1.9.3.10.1"></a>

## ALTER EVENT TRIGGER

ALTER EVENT TRIGGER — 變更事件觸發程序的定義

<a id="id-1.9.3.10.4"></a>

## 語法

```

ALTER EVENT TRIGGER name DISABLE
ALTER EVENT TRIGGER name ENABLE [ REPLICA | ALWAYS ]
ALTER EVENT TRIGGER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER EVENT TRIGGER name RENAME TO new_name
```

<a id="id-1.9.3.10.5"></a>

## 說明

`ALTER EVENT TRIGGER` 會變更現有事件觸發程序的屬性。

你必須是超級使用者才能修改事件觸發程序。

<a id="id-1.9.3.10.6"></a>

## 參數

*`name`*
:   要修改的現有觸發程序名稱。

*`new_owner`*
:   事件觸發程序新擁有者的使用者名稱。

*`new_name`*
:   事件觸發程序的新名稱。

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ]`
:   這些形式用來設定事件觸發程序的觸發方式。已停用的觸發程序仍為系統所知，但在其觸發事件發生時不會執行。另請參閱 [session_replication_role](../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE)。

<a id="SQL-ALTERVENTTRIGGER-COMPATIBILITY"></a>

## 相容性

SQL 標準中沒有 `ALTER EVENT TRIGGER` 陳述式。

<a id="id-1.9.3.10.8"></a>

## 另請參閱

[CREATE EVENT TRIGGER](sql-createeventtrigger.md), [DROP EVENT TRIGGER](sql-dropeventtrigger.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altereventtrigger.html)（原文版本：18.6；核對日期：2026-10-05）
