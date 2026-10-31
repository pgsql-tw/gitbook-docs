<a id="SQL-ALTERSUBSCRIPTION"></a><a id="id-1.9.3.33.1"></a>

## ALTER SUBSCRIPTION

ALTER SUBSCRIPTION — 變更訂閱的定義

<a id="id-1.9.3.33.4"></a>

## 語法

```

ALTER SUBSCRIPTION name CONNECTION 'conninfo'
ALTER SUBSCRIPTION name SET PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ADD PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name DROP PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name REFRESH PUBLICATION [ WITH ( refresh_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ENABLE
ALTER SUBSCRIPTION name DISABLE
ALTER SUBSCRIPTION name SET ( subscription_parameter [= value] [, ... ] )
ALTER SUBSCRIPTION name SKIP ( skip_option = value )
ALTER SUBSCRIPTION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SUBSCRIPTION name RENAME TO new_name
```

<a id="id-1.9.3.33.5"></a>

## 說明

`ALTER SUBSCRIPTION` 可以變更大部分可在
[CREATE SUBSCRIPTION](sql-createsubscription.md) 中指定的訂閱屬性。

你必須擁有該訂閱，才能使用 `ALTER SUBSCRIPTION`。
要重新命名訂閱或變更擁有者，你必須具備該資料庫的
`CREATE` 權限。此外，要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色。若該訂閱設定了
`password_required=false`，則只有超級使用者可以修改它。

重新整理發佈時，我們會移除不再屬於該發佈的關聯，若有資料表同步插槽，也會將其移除。必須移除這些插槽，才能釋放在遠端主機上為該訂閱配置的資源。若因網路中斷或其他錯誤，使 PostgreSQL
無法移除這些插槽，就會回報錯誤。要在這種情況下繼續進行，使用者需要重試該操作，或者將插槽與訂閱解除關聯，並依
[DROP SUBSCRIPTION](sql-dropsubscription.md) 中的說明移除該訂閱。

`ALTER SUBSCRIPTION ... REFRESH PUBLICATION` 命令、
`refresh` 選項為 `true` 的
`ALTER SUBSCRIPTION ... {SET|ADD|DROP} PUBLICATION ...` 命令、
`ALTER SUBSCRIPTION ... SET (failover = true|false)` 命令，以及
`ALTER SUBSCRIPTION ... SET (two_phase = false)` 命令，
都不能在交易區塊內執行。

當訂閱啟用了
[`two_phase`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-two-phase)
提交時，`ALTER SUBSCRIPTION ... REFRESH PUBLICATION` 命令以及
`refresh` 選項為 `true` 的
`ALTER SUBSCRIPTION ... {SET|ADD|DROP} PUBLICATION ...` 命令也同樣不能執行，除非
[`copy_data`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-copy-data)
為 `false`。請參閱
[`pg_subscription`](../../internals/catalogs/catalog-pg-subscription.md) 的 `subtwophasestate` 欄位，
以得知實際的兩階段狀態。

<a id="id-1.9.3.33.6"></a>

## 參數

<a id="SQL-ALTERSUBSCRIPTION-PARAMS-NAME"></a>

*`name`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NAME)
:   要變更其屬性之訂閱的名稱。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION"></a>

`CONNECTION 'conninfo'` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION)
:   此子句會取代原先由
    [CREATE SUBSCRIPTION](sql-createsubscription.md) 設定的連線字串。更多資訊請參閱該處。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-SETADDDROP-PUBLICATION"></a>

`SET PUBLICATION publication_name`<br>`ADD PUBLICATION publication_name`<br>`DROP PUBLICATION publication_name` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SETADDDROP-PUBLICATION)

這些形式會變更所訂閱之發佈的清單。
`SET`
會以新的清單取代整份發佈清單，
`ADD` 會將額外的發佈加入發佈清單，而 `DROP` 會從發佈清單中移除這些發佈。我們允許在 `ADD` 與 `SET` 形式中指定不存在的發佈，讓使用者可以之後再加入它們。更多資訊請參閱 [CREATE SUBSCRIPTION](sql-createsubscription.md)。預設情況下，此命令也會發揮與
`REFRESH PUBLICATION` 相同的作用。

*`publication_option`* 指定此操作的額外選項。支援的選項有：

- `refresh` (`boolean`)

  設為 false 時，此命令不會嘗試重新整理資料表資訊。
  之後應該另外執行 `REFRESH PUBLICATION`。
  預設值為 `true`。

此外，也可以指定
`REFRESH PUBLICATION` 底下所述的選項，以控制隱含的重新整理操作。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION"></a>

`REFRESH PUBLICATION` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)

從發佈者擷取缺少的資料表資訊。這會開始複寫自 [`CREATE SUBSCRIPTION`](sql-createsubscription.md) 或上一次呼叫
`REFRESH PUBLICATION` 以來，新加入所訂閱之發佈的資料表。

*`refresh_option`* 指定重新整理操作的額外選項。支援的選項有：

- `copy_data` (`boolean`)

  指定複寫開始時，是否要複製所訂閱之發佈中既有的資料。
  預設值為 `true`。

  先前已訂閱的資料表不會被複製，即使某個資料表的資料列篩選器
  `WHERE` 子句在那之後已被修改。

  關於 `copy_data = true` 如何與
  [`origin`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-origin)
  參數互動的細節，請參閱[注意事項](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES)。

  關於以二進位格式複製既有資料的細節，請參閱
  `CREATE SUBSCRIPTION` 的
  [`binary`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-binary)
  參數。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE"></a>

`ENABLE` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE)
:   啟用先前已停用的訂閱，並在交易結束時啟動邏輯複寫工作程序。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE"></a>

`DISABLE` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)
:   停用執行中的訂閱，並在交易結束時停止邏輯複寫工作程序。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-SET"></a>

`SET ( subscription_parameter [= value] [, ... ] )` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SET)

此子句會變更原先由
[CREATE SUBSCRIPTION](sql-createsubscription.md) 設定的參數。更多資訊請參閱該處。可以變更的參數有
[`slot_name`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-slot-name)、
[`synchronous_commit`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-synchronous-commit)、
[`binary`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-binary)、
[`streaming`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-streaming)、
[`disable_on_error`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-disable-on-error)、
[`password_required`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-password-required)、
[`run_as_owner`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-run-as-owner)、
[`origin`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-origin)、
[`failover`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-failover) 與
[`two_phase`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-two-phase)。
只有超級使用者可以設定 `password_required = false`。

變更
[`slot_name`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-slot-name)
時，所指定插槽的 `failover` 與 `two_phase` 屬性值，可能與訂閱中所指定之對應的
[`failover`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-failover)
與 [`two_phase`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-two-phase)
參數不同。建立插槽時，請確保插槽屬性 `failover` 與 `two_phase`
符合訂閱中對應的參數。
否則，發佈者上的插槽的行為可能與這些訂閱選項所述的不同：例如，即使訂閱的
[`failover`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-failover)
選項已停用，發佈者上的插槽仍可能被同步到待命伺服器；或者即使訂閱的
[`failover`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-failover)
選項已啟用，該插槽仍可能被停用同步。

[`failover`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-failover)
與 [`two_phase`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-two-phase)
參數只能在訂閱停用時變更。

將 [`two_phase`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-two-phase)
從 `true` 變更為 `false` 時，若發現任何由邏輯複寫工作程序完成的預備交易（來自 `two_phase`
參數仍為 `true` 的期間），後端程序會回報錯誤。你可以在發佈者節點上解決這些預備交易，或在訂閱者手動將它們回滾，然後再試一次。對應於特定訂閱的邏輯複寫工作程序所預備的交易，具有下列模式：「`pg_gid_%u_%u`」
（參數：訂閱 *`oid`*、遠端交易 ID *`xid`*）。
要手動解決這類交易，你需要回滾名稱中含有對應訂閱 ID 的所有預備交易。應用程式可以查看
[`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md)
來找出所需的預備交易。將 `two_phase`
選項從 `true` 變更為 `false` 之後，
發佈者會在這些交易提交時再次複寫它們。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-SKIP"></a>

`SKIP ( skip_option = value )` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SKIP)

略過套用遠端交易的所有變更。若傳入的資料違反任何限制條件，邏輯複寫會停止，直到問題解決為止。使用 `ALTER SUBSCRIPTION ... SKIP` 命令，
邏輯複寫工作程序會略過該交易中所有的資料修改變更。對於已在訂閱者啟用
[`two_phase`](sql-createsubscription-parameters.md#sql-createsubscription-params-with-two-phase)
而已預備的交易，此選項沒有作用。
在邏輯複寫工作程序成功略過該交易或完成某個交易之後，LSN（儲存於
`pg_subscription`.`subskiplsn`）
會被清除。關於邏輯複寫衝突的細節，請參閱[第 29.7 節](../../server-administration/logical-replication/logical-replication-conflicts.md)。

*`skip_option`* 指定此操作的選項。
支援的選項有：

- `lsn` (`pg_lsn`)

  指定其變更要被邏輯複寫工作程序略過之遠端交易的完成 LSN。完成 LSN
  是該交易被提交或被預備時的 LSN。
  不支援略過個別的子交易。設定
  `NONE` 會重設 LSN。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-NEW-OWNER"></a>

*`new_owner`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NEW-OWNER)
:   訂閱之新擁有者的使用者名稱。
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-NEW-NAME"></a>

*`new_name`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NEW-NAME)
:   訂閱的新名稱。

指定 `boolean` 型別的參數時，可以省略
`=` *`value`*
部分，這等同於指定 `TRUE`。

<a id="id-1.9.3.33.7"></a>

## 範例

將訂閱所訂閱的發佈變更為
`insert_only`：

```

ALTER SUBSCRIPTION mysub SET PUBLICATION insert_only;
```

停用（停止）訂閱：

```

ALTER SUBSCRIPTION mysub DISABLE;
```

<a id="id-1.9.3.33.8"></a>

## 相容性

`ALTER SUBSCRIPTION` 是 PostgreSQL
的擴充語法。

<a id="id-1.9.3.33.9"></a>

## 另請參閱

[CREATE SUBSCRIPTION](sql-createsubscription.md), [DROP SUBSCRIPTION](sql-dropsubscription.md), [CREATE PUBLICATION](sql-createpublication.md), [ALTER PUBLICATION](sql-alterpublication.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altersubscription.html)（原文版本：18.6；核對日期：2026-10-04）
