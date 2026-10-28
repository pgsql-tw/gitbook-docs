<a id="SQL-ALTERDATABASE"></a><a id="id-1.9.3.7.1"></a>

## ALTER DATABASE

ALTER DATABASE — 變更資料庫

<a id="id-1.9.3.7.4"></a>

## 語法

```

ALTER DATABASE name [ [ WITH ] option [ ... ] ]

where option can be:

    ALLOW_CONNECTIONS allowconn
    CONNECTION LIMIT connlimit
    IS_TEMPLATE istemplate

ALTER DATABASE name RENAME TO new_name

ALTER DATABASE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER DATABASE name SET TABLESPACE new_tablespace

ALTER DATABASE name REFRESH COLLATION VERSION

ALTER DATABASE name SET configuration_parameter { TO | = } { value | DEFAULT }
ALTER DATABASE name SET configuration_parameter FROM CURRENT
ALTER DATABASE name RESET configuration_parameter
ALTER DATABASE name RESET ALL
```

<a id="id-1.9.3.7.5"></a>

## 說明

`ALTER DATABASE` 會變更資料庫的屬性。

第一種形式會變更某些個別資料庫的設定。（詳見下文。）只有資料庫擁有者或超級使用者可以變更這些設定。

第二種形式會變更資料庫的名稱。只有資料庫擁有者或超級使用者可以重新命名資料庫；非超級使用者的擁有者還必須具有 `CREATEDB` 權限。目前所在的資料庫無法重新命名。（若需要這麼做，請連線到另一個資料庫。）

第三種形式會變更資料庫的擁有者。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，而且你必須具有 `CREATEDB` 權限。（請注意，超級使用者會自動擁有所有這些權限。）

第四種形式會變更資料庫的預設資料表空間。只有資料庫擁有者或超級使用者可以這麼做；你還必須具有新資料表空間的 CREATE 權限。此命令會將資料庫舊預設資料表空間中的所有資料表或索引實體搬移到新的資料表空間。對此資料庫而言，新的預設資料表空間必須是空的，而且不能有任何人連線到該資料庫。位於非預設資料表空間中的資料表與索引不受影響。將檔案複製到新資料表空間所使用的方法，會受到 [file_copy_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-FILE-COPY-METHOD) 設定的影響。

其餘的形式會為某個 PostgreSQL 資料庫變更執行期組態變數的工作階段預設值。之後每當在該資料庫中啟動新的工作階段時，指定的值就會成為工作階段的預設值。資料庫專屬的預設值會覆寫 `postgresql.conf` 中的任何設定，或從 `postgres` 命令列接收到的設定。只有資料庫擁有者或超級使用者可以變更資料庫的工作階段預設值。某些變數無法以這種方式設定，或只能由超級使用者設定。

<a id="id-1.9.3.7.6"></a>

## 參數

*`name`*
:   要變更其屬性之資料庫的名稱。

*`allowconn`*
:   若為 false，則沒有人可以連線到此資料庫。

*`connlimit`*
:   此資料庫可以建立多少個並行連線。-1 表示沒有限制。

*`istemplate`*
:   若為 true，則任何具有 `CREATEDB` 權限的使用者都可以複製此資料庫；若為 false，則只有超級使用者或資料庫擁有者可以複製它。

*`new_name`*
:   資料庫的新名稱。

*`new_owner`*
:   資料庫的新擁有者。

*`new_tablespace`*

資料庫的新預設資料表空間。

此形式的命令不能在交易區塊內執行。

`REFRESH COLLATION VERSION`
:   更新資料庫的定序版本。背景說明請參閱[注意事項](sql-altercollation.md#SQL-ALTERCOLLATION-NOTES)。

*`configuration_parameter`*<br>*`value`*

將此資料庫中指定組態參數的工作階段預設值設為給定的值。若 *`value`* 為 `DEFAULT`，或等效地使用 `RESET`，則會移除資料庫專屬的設定，新的工作階段將繼承系統層級的預設設定。使用 `RESET
ALL` 可清除所有資料庫專屬的設定。`SET FROM CURRENT` 會將該參數在工作階段中目前的值儲存為資料庫專屬的值。

關於允許的參數名稱與值的更多資訊，請參閱 [SET](sql-set.md) 與[第 19 章](../../server-administration/runtime-config/README.md)。

<a id="id-1.9.3.7.7"></a>

## 注意事項

也可以將工作階段預設值綁定到特定角色而非資料庫；請參閱 [ALTER ROLE](sql-alterrole.md)。若有衝突，角色專屬的設定會覆寫資料庫專屬的設定。

<a id="id-1.9.3.7.8"></a>

## 範例

在資料庫 `test` 中預設停用索引掃描：

```

ALTER DATABASE test SET enable_indexscan TO off;
```

<a id="id-1.9.3.7.9"></a>

## 相容性

`ALTER DATABASE` 陳述式是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.7.10"></a>

## 另請參閱

[CREATE DATABASE](sql-createdatabase.md), [DROP DATABASE](sql-dropdatabase.md), [SET](sql-set.md), [CREATE TABLESPACE](sql-createtablespace.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterdatabase.html)（原文版本：18.6；核對日期：2026-10-05）
