<a id="ROLE-ATTRIBUTES"></a>

## 21.2. 角色屬性 [#](#ROLE-ATTRIBUTES)

資料庫角色可以具有多項屬性，這些屬性定義了該角色的權限，
並與用戶端驗證系統互動。

login 權限<a id="id-1.6.8.6.2.1.1.1.1"></a>
:   只有具有 `LOGIN` 屬性的角色，才能用作資料庫連線的
    初始角色名稱。具有 `LOGIN` 屬性的角色，
    可以視為等同於「資料庫使用者」。若要建立具有登入權限的角色，
    可使用以下任一方式：

    ```

    CREATE ROLE name LOGIN;
    CREATE USER name;
    ```

    （`CREATE USER` 等同於 `CREATE ROLE`，
    差別在於 `CREATE USER` 預設包含 `LOGIN`，
    而 `CREATE ROLE` 則不會。）

超級使用者狀態<a id="id-1.6.8.6.2.1.2.1.1"></a>
:   資料庫超級使用者，會略過除了登入權限以外的所有權限檢查。
    這是一項危險的權限，不應輕率使用；最好大部分工作，
    都以非超級使用者的角色來進行。若要建立新的資料庫超級使用者，
    請使用 `CREATE ROLE name SUPERUSER`。
    您必須以本身已是超級使用者的角色，來執行此操作。

建立資料庫<a id="id-1.6.8.6.2.1.3.1.1"></a>
:   角色必須被明確授予建立資料庫的權限
    （超級使用者除外，因為超級使用者會略過所有權限檢查）。
    若要建立這樣的角色，請使用
    `CREATE ROLE name CREATEDB`。

<a id="ROLE-CREATION"></a>建立角色<a id="id-1.6.8.6.2.1.4.1.1"></a>
:   角色必須被明確授予建立其他角色的權限
    （超級使用者除外，因為超級使用者會略過所有權限檢查）。
    若要建立這樣的角色，請使用
    `CREATE ROLE name CREATEROLE`。
    具有 `CREATEROLE` 權限的角色，可以變更與刪除
    那些已以 `ADMIN` 選項授予該 `CREATEROLE`
    使用者的角色。當非超級使用者的 `CREATEROLE`
    使用者建立新角色時，就會自動發生這樣的授予，因此
    依預設，`CREATEROLE` 使用者可以變更與刪除
    自己所建立的角色。變更角色，涵蓋了大多數可透過
    `ALTER ROLE` 進行的變更，例如變更密碼。
    這也包括可透過 `COMMENT` 與
    `SECURITY LABEL` 指令，對角色所做的修改。

    不過，`CREATEROLE` 並不賦予建立
    `SUPERUSER` 角色的能力，對於既有的
    `SUPERUSER` 角色，也不賦予任何權力。
    此外，`CREATEROLE` 也不賦予建立
    `REPLICATION` 使用者的能力，也不能授予或撤銷
    `REPLICATION` 權限，更不能修改這類使用者的
    角色屬性。不過，它確實允許在 `REPLICATION`
    角色上使用 `ALTER ROLE ... SET` 與
    `ALTER ROLE ... RENAME`，也允許使用
    `COMMENT ON ROLE`、
    `SECURITY LABEL ON ROLE`
    以及 `DROP ROLE`。最後，
    `CREATEROLE` 也不賦予授予或撤銷
    `BYPASSRLS` 權限的能力。

發起複寫<a id="id-1.6.8.6.2.1.5.1.1"></a>
:   角色必須被明確授予發起串流複寫的權限
    （超級使用者除外，因為超級使用者會略過所有權限檢查）。
    用於串流複寫的角色，也必須具有 `LOGIN` 權限。
    若要建立這樣的角色，請使用
    `CREATE ROLE name REPLICATION LOGIN`。

密碼<a id="id-1.6.8.6.2.1.6.1.1"></a>
:   只有當用戶端驗證方式要求使用者在連線資料庫時
    提供密碼，密碼才有意義。`password` 與
    `md5` 驗證方式，都會用到密碼。
    資料庫密碼與作業系統密碼是分開的。
    可在建立角色時，透過
    `CREATE ROLE name PASSWORD 'string'`
    指定密碼。

權限繼承<a id="id-1.6.8.6.2.1.7.1.1"></a>
:   依預設，角色會繼承其所屬角色的權限。
    不過，若要建立一個預設不繼承權限的角色，
    請使用 `CREATE ROLE name NOINHERIT`。
    此外，也可以針對個別的授予，使用
    `WITH INHERIT TRUE` 或
    `WITH INHERIT FALSE`，來覆寫繼承設定。

略過資料列層級安全性<a id="id-1.6.8.6.2.1.8.1.1"></a>
:   角色必須被明確授予略過每一項資料列層級安全性（RLS）政策的權限
    （超級使用者除外，因為超級使用者會略過所有權限檢查）。
    若要建立這樣的角色，請以超級使用者身分使用
    `CREATE ROLE name BYPASSRLS`。

連線數上限<a id="id-1.6.8.6.2.1.9.1.1"></a>
:   連線數上限，可以指定某個角色最多能同時建立多少連線。
    -1（預設值）代表沒有上限。可在建立角色時，
    透過 `CREATE ROLE name CONNECTION LIMIT 'integer'`
    指定連線數上限。

角色的屬性，可以在建立之後，透過
`ALTER ROLE` 修改。<a id="id-1.6.8.6.2.3"></a>
詳情請參閱 [CREATE ROLE](../../reference/sql-commands/sql-createrole.md)
與 [ALTER ROLE](../../reference/sql-commands/sql-alterrole.md) 指令的參考頁面。

角色也可以針對[第 19 章](../runtime-config/README.md)中所述的許多執行期組態設定，
擁有角色專屬的預設值。舉例來說，若基於某些原因，
您希望每次連線時都停用索引掃描（提示：這不是個好主意），
可以使用：

```

ALTER ROLE myname SET enable_indexscan TO off;
```

這會儲存該項設定（但不會立即套用）。在該角色
之後的連線中，就會如同在工作階段開始前，
剛執行過 `SET enable_indexscan TO off` 一般。
您仍然可以在工作階段期間變更此設定；
它只是作為預設值。若要移除角色專屬的預設設定，
請使用 `ALTER ROLE rolename RESET varname`。
請注意，附加在不具 `LOGIN` 權限之角色上的
角色專屬預設值，相當沒有用處，因為它們永遠不會被啟用。

當非超級使用者利用 `CREATEROLE` 權限
建立角色時，該新建立的角色，會自動被反向授予給
建立者，就如同啟動用超級使用者（bootstrap superuser）
執行了以下指令一般：
`GRANT created_user TO creating_user WITH ADMIN TRUE, SET FALSE, INHERIT FALSE`。
由於 `CREATEROLE` 使用者，只有在對某個既有角色
具有 `ADMIN OPTION` 時，才能對其行使特殊權限，
因此這項授予，正好足以讓 `CREATEROLE` 使用者，
管理自己所建立的角色。不過，由於這項授予是以
`INHERIT FALSE, SET FALSE` 建立的，
`CREATEROLE` 使用者並不會繼承所建立角色的權限，
也無法透過 `SET ROLE` 存取該角色的權限。
不過，由於任何對某個角色具有 `ADMIN OPTION`
的使用者，都能將該角色的成員資格，授予任何其他使用者，
因此 `CREATEROLE` 使用者，只需將所建立的角色，
以 `INHERIT` 及／或 `SET` 選項
反向授予給自己，即可取得對該角色的存取權。
因此，「權限預設不會被繼承」以及「預設不會授予
`SET ROLE`」這項事實，其實是一種避免意外的保護措施，
而非安全性功能。另請注意，由於這項自動授予，
是由啟動用超級使用者所授予的，因此
`CREATEROLE` 使用者無法將其移除或變更；
不過，任何超級使用者，都可以撤銷它、修改它，
及／或對其他 `CREATEROLE` 使用者，
再發出額外的此類授予。無論在任何時間點，
只要 `CREATEROLE` 使用者對某個角色具有
`ADMIN OPTION`，就都能管理該角色。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/role-attributes.html)（原文版本：18.6；核對日期：2026-09-22）
