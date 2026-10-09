<a id="SQL-ALTERCOLLATION"></a><a id="id-1.9.3.5.1"></a>

## ALTER COLLATION

ALTER COLLATION — 變更定序的定義

<a id="id-1.9.3.5.4"></a>

## 語法

```

ALTER COLLATION name REFRESH VERSION

ALTER COLLATION name RENAME TO new_name
ALTER COLLATION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER COLLATION name SET SCHEMA new_schema
```

<a id="id-1.9.3.5.5"></a>

## 說明

`ALTER COLLATION` 會變更定序的定義。

你必須是定序的擁有者才能使用 `ALTER COLLATION`。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，且該角色必須具有該定序所在綱要的 `CREATE` 權限。（這些限制是為了確保變更擁有者不會做到你無法透過移除並重新建立定序而做到的事。不過，超級使用者無論如何都可以變更任何定序的擁有權。）

<a id="id-1.9.3.5.6"></a>

## 參數

*`name`*
:   現有定序的名稱（可選擇以綱要限定）。

*`new_name`*
:   定序的新名稱。

*`new_owner`*
:   定序的新擁有者。

*`new_schema`*
:   定序的新綱要。

`REFRESH VERSION`
:   更新定序的版本。請參閱下方的[注意事項](sql-altercollation.md#SQL-ALTERCOLLATION-NOTES)。

<a id="SQL-ALTERCOLLATION-NOTES"></a>

## 注意事項

建立定序物件時，定序的提供者特定版本會記錄在系統目錄中。使用該定序時，會將目前版本與記錄的版本相比對，若不一致就會發出警告，例如：

```

WARNING:  collation "xx-x-icu" has version mismatch
DETAIL:  The collation in the database was created using version 1.2.3.4, but the operating system provides version 2.3.4.5.
HINT:  Rebuild all objects affected by this collation and run ALTER COLLATION pg_catalog."xx-x-icu" REFRESH VERSION, or build PostgreSQL with the right library version.
```

定序定義的變更可能導致索引損毀及其他問題，因為資料庫系統依賴已儲存的物件具有特定的排序順序。一般而言應該避免這種情況，但它也可能在正當的情況下發生，例如將作業系統升級到新的主要版本時，或使用 `pg_upgrade` 升級到與較新版本 ICU 連結的伺服器執行檔時。發生這種情況時，所有相依於該定序的物件都應該重建，例如使用 `REINDEX`。完成之後，就可以使用命令 `ALTER COLLATION ... REFRESH
VERSION` 更新定序版本。這會更新系統目錄以記錄目前的定序版本，並使警告消失。請注意，此命令並不會實際檢查所有受影響的物件是否都已正確重建。

使用 `libc` 提供的定序時，在使用 GNU C 函式庫的系統（大多數 Linux 系統）、FreeBSD 與 Windows 上會記錄版本資訊。使用 ICU 提供的定序時，版本資訊由 ICU 函式庫提供，且在所有平台上皆可使用。

<a id="SQL-ALTERCOLLATION-NOTES-NOTE"></a>

### 注意

使用 GNU C 函式庫提供定序時，會以 C 函式庫的版本作為定序版本的替代指標。許多 Linux 發行版只在升級 C 函式庫時才變更定序定義，但這種做法並不完美，因為維護者可以自由地將較新的定序定義反向移植到較舊的 C 函式庫版本。

使用 Windows 提供定序時，只有以 BCP 47 語言標籤（例如 `en-US`）定義的定序才有版本資訊可用。

對於資料庫的預設定序，有一個類似的命令 `ALTER DATABASE ... REFRESH COLLATION VERSION`。

下列查詢可用來找出目前資料庫中所有需要更新的定序，以及相依於它們的物件：

```

SELECT pg_describe_object(refclassid, refobjid, refobjsubid) AS "Collation",
       pg_describe_object(classid, objid, objsubid) AS "Object"
  FROM pg_depend d JOIN pg_collation c
       ON refclassid = 'pg_collation'::regclass AND refobjid = c.oid
  WHERE c.collversion <> pg_collation_actual_version(c.oid)
  ORDER BY 1, 2;
```

<a id="id-1.9.3.5.8"></a>

## 範例

將定序 `de_DE` 重新命名為 `german`：

```

ALTER COLLATION "de_DE" RENAME TO german;
```

將定序 `en_US` 的擁有者變更為 `joe`：

```

ALTER COLLATION "en_US" OWNER TO joe;
```

<a id="id-1.9.3.5.9"></a>

## 相容性

SQL 標準中沒有 `ALTER COLLATION` 陳述式。

<a id="id-1.9.3.5.10"></a>

## 另請參閱

[CREATE COLLATION](sql-createcollation.md), [DROP COLLATION](sql-dropcollation.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altercollation.html)（原文版本：18.6；核對日期：2026-10-05）
