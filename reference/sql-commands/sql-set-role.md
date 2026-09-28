<a id="id-1.9.3.176.1"></a>

## SET ROLE

SET ROLE — 設定目前工作階段的目前使用者識別碼

## 語法

```

SET [ SESSION | LOCAL ] ROLE role_name
SET [ SESSION | LOCAL ] ROLE NONE
RESET ROLE
```

<a id="id-1.9.3.176.5"></a>

## 說明

此命令會將目前 SQL 工作階段的目前使用者識別碼設為
*`role_name`*。角色名稱可以寫成識別字，也可以寫成字串常值。
執行 `SET ROLE` 之後，SQL 命令的權限檢查會如同該指定角色是
最初登入的角色一般進行。請注意，`SET ROLE` 與
`SET SESSION AUTHORIZATION` 是例外；這兩者的權限檢查，
仍分別使用目前的工作階段使用者以及最初的工作階段使用者
（*已驗證使用者*）。

目前的工作階段使用者必須對指定的 *`role_name`*
具有 `SET` 選項，可以是直接具有，也可以是透過一連串
具有 `SET` 選項的成員關係間接取得。
（若工作階段使用者是超級使用者，則可以選擇任何角色。）

`SESSION` 與 `LOCAL` 修飾詞的作用方式，
與一般 [`SET`](sql-set.md) 命令相同。

`SET ROLE NONE` 會將目前使用者識別碼設為目前的工作階段使用者識別碼，
即 `session_user` 所回傳的值。`RESET ROLE` 會將
目前使用者識別碼設為連線時所指定的設定值——這個設定值可能來自
[命令列選項](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-OPTIONS)、
[`ALTER ROLE`](sql-alterrole.md)，或
[`ALTER DATABASE`](sql-alterdatabase.md)，
只要存在這類設定即可。否則，`RESET ROLE` 會將
目前使用者識別碼設為目前的工作階段使用者識別碼。任何使用者都可以執行這些形式。

<a id="id-1.9.3.176.6"></a>

## 注意事項

使用此命令，可以增加權限，也可以限縮自己的權限。若工作階段使用者角色
被授予的成員關係具有 `WITH INHERIT TRUE`，它會自動擁有
每一個這類角色的所有權限。在此情況下，`SET ROLE`
實際上會捨棄除了目標角色直接擁有或繼承而來以外的所有權限。
另一方面，若工作階段使用者角色被授予的成員關係具有
`WITH INHERIT FALSE`，預設無法存取所被授予角色的權限。
不過，若該角色的授予具有 `WITH SET TRUE`，
工作階段使用者就可以使用 `SET ROLE` 捨棄直接指派給
工作階段使用者的權限，改為取得該指定角色可用的權限。若角色的授予是
`WITH INHERIT
FALSE, SET FALSE`，那麼無論是否使用 `SET ROLE`，都無法行使該角色的權限。

`SET ROLE` 的效果與
[`SET SESSION AUTHORIZATION`](sql-set-session-authorization.md) 相當，
但涉及的權限檢查方式相當不同。此外，
`SET SESSION AUTHORIZATION` 會決定之後
`SET ROLE` 命令可使用哪些角色，而以
`SET ROLE` 變更角色，則不會改變之後
`SET ROLE` 可使用的角色集合。

`SET ROLE` 不會處理角色的
[`ALTER ROLE`](sql-alterrole.md) 設定所指定的工作階段變數；這些設定
只會在登入期間套用。

`SET ROLE` 無法在 `SECURITY DEFINER`
函式內使用。

<a id="id-1.9.3.176.7"></a>

## 範例

```

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | peter

SET ROLE 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | paul
```

<a id="id-1.9.3.176.8"></a>

## 相容性

PostgreSQL 允許使用識別字語法
（`"rolename"`），而 SQL 標準則要求角色名稱必須寫成
字串常值。SQL 標準不允許在交易中執行此命令；
PostgreSQL 並無此限制，因為沒有理由要這樣限制。
`SESSION` 與 `LOCAL` 修飾詞是
PostgreSQL 的擴充功能，`RESET`
語法亦同。

<a id="id-1.9.3.176.9"></a>

## 另請參閱

[SET SESSION AUTHORIZATION](sql-set-session-authorization.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-set-role.html)（原文版本：18.6；核對日期：2026-09-28）
