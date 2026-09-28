<a id="id-1.9.3.177.1"></a>

## SET SESSION AUTHORIZATION

SET SESSION AUTHORIZATION — 設定目前工作階段的工作階段使用者識別碼與目前使用者識別碼

## 語法

```

SET [ SESSION | LOCAL ] SESSION AUTHORIZATION user_name
SET [ SESSION | LOCAL ] SESSION AUTHORIZATION DEFAULT
RESET SESSION AUTHORIZATION
```

<a id="id-1.9.3.177.5"></a>

## 說明

此命令會將目前 SQL 工作階段的工作階段使用者識別碼與目前使用者識別碼設為
*`user_name`*。使用者名稱可以寫成識別字，也可以寫成字串常值。
使用此命令，舉例來說，可以暫時變成一個沒有權限的使用者，之後再切換回超級使用者。

工作階段使用者識別碼一開始會設為用戶端所提供的（可能經過驗證的）使用者名稱。
目前使用者識別碼通常等於工作階段使用者識別碼，但在
`SECURITY DEFINER` 函式及類似機制的情境下可能會暫時改變；
它也可以透過 [`SET ROLE`](sql-set-role.md) 來變更。
目前使用者識別碼與權限檢查有關。

只有在最初的工作階段使用者（*已驗證使用者*）具有超級使用者權限時，
才能變更工作階段使用者識別碼。否則，只有在此命令指定的正是已驗證使用者名稱時，
才會被接受。

`SESSION` 與 `LOCAL` 修飾詞的作用方式，
與一般 [`SET`](sql-set.md) 命令相同。

`DEFAULT` 與 `RESET` 形式會將工作階段使用者識別碼與目前使用者識別碼，
重設為最初通過驗證的使用者名稱。任何使用者都可以執行這些形式。

<a id="id-1.9.3.177.6"></a>

## 注意事項

`SET SESSION AUTHORIZATION` 無法在 `SECURITY DEFINER`
函式內使用。

<a id="id-1.9.3.177.7"></a>

## 範例

```

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | peter

SET SESSION AUTHORIZATION 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 paul         | paul
```

<a id="id-1.9.3.177.8"></a>

## 相容性

SQL 標準允許在字面值 *`user_name`* 的位置使用其他一些運算式，
但這些選項在實務上並不重要。PostgreSQL
允許使用識別字語法（`"username"`），而 SQL 標準並不允許。
SQL 標準不允許在交易中執行此命令；PostgreSQL
並無此限制，因為沒有理由要這樣限制。
`SESSION` 與 `LOCAL` 修飾詞是
PostgreSQL 的擴充功能，`RESET`
語法亦同。

執行此命令所需的權限，標準將其留給實作自行定義。

<a id="id-1.9.3.177.9"></a>

## 另請參閱

[SET ROLE](sql-set-role.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-set-session-authorization.html)（原文版本：18.6；核對日期：2026-09-28）
