<a id="SQL-ALTERPUBLICATION"></a><a id="id-1.9.3.25.1"></a>

## ALTER PUBLICATION

ALTER PUBLICATION — 變更發佈的定義

<a id="id-1.9.3.25.4"></a>

## 語法

```

ALTER PUBLICATION name ADD publication_object [, ...]
ALTER PUBLICATION name SET publication_object [, ...]
ALTER PUBLICATION name DROP publication_drop_object [, ...]
ALTER PUBLICATION name SET ( publication_parameter [= value] [, ... ] )
ALTER PUBLICATION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER PUBLICATION name RENAME TO new_name

where publication_object is one of:

    TABLE table_and_columns [, ... ]
    TABLES IN SCHEMA { schema_name | CURRENT_SCHEMA } [, ... ]

and publication_drop_object is one of:

    TABLE [ ONLY ] table_name [ * ] [, ... ]
    TABLES IN SCHEMA { schema_name | CURRENT_SCHEMA } [, ... ]

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ... ] ) ] [ WHERE ( expression ) ]
```

<a id="id-1.9.3.25.5"></a>

## 說明

`ALTER PUBLICATION` 命令可以變更發佈的屬性。

前三種形式會變更哪些資料表／綱要屬於該發佈。`SET` 子句會以指定的清單取代發佈中的資料表／綱要清單；原本存在於發佈中的現有資料表／綱要將被移除。`ADD` 與 `DROP` 子句會在發佈中加入或移除一個或多個資料表／綱要。請注意，將資料表／綱要加入一個已被訂閱的發佈時，需要在訂閱端執行 [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION) 動作才會生效。另請注意，`DROP TABLES IN SCHEMA` 不會移除使用 [`FOR TABLE`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLE)／`ADD TABLE` 所指定的綱要資料表。

語法中列出的此命令第四種形式，可以變更 [CREATE PUBLICATION](sql-createpublication.md) 中指定的所有發佈屬性。命令中未提及的屬性會保留先前的設定。

其餘形式會變更發佈的擁有者與名稱。

你必須是該發佈的擁有者才能使用 `ALTER PUBLICATION`。將資料表加入發佈還需要擁有該資料表。對發佈執行 `ADD TABLES IN SCHEMA` 與 `SET TABLES IN SCHEMA` 需要執行命令的使用者是超級使用者。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有者角色，且該角色必須擁有該資料庫的 `CREATE` 權限。此外，[`FOR ALL TABLES`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) 或 [`FOR TABLES IN SCHEMA`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA) 發佈的新擁有者必須是超級使用者。不過，超級使用者可以不受這些限制地變更發佈的擁有權。

當發佈同時也發佈帶有欄位清單的資料表時，不支援加入／設定任何綱要，反之亦然。

<a id="id-1.9.3.25.6"></a>

## 參數

*`name`*
:   要變更其定義的現有發佈名稱。

*`table_name`*
:   現有資料表的名稱。若在資料表名稱前指定 `ONLY`，則只有該資料表會受到影響。若未指定 `ONLY`，則該資料表及其所有後代資料表（若有的話）都會受到影響。也可以選擇在資料表名稱後指定 `*`，以明確表示包含後代資料表。

    也可以選擇指定欄位清單。詳情請參閱 [CREATE PUBLICATION](sql-createpublication.md)。請注意，不支援一個訂閱擁有多個發佈、而同一個資料表在這些發佈中以不同欄位清單發佈的情況。關於變更欄位清單時可能發生的問題，請參閱 [警告：合併多個發佈的欄位清單](../../server-administration/logical-replication/logical-replication-col-lists.md#LOGICAL-REPLICATION-COL-LIST-COMBINING)。

    若指定了選擇性的 `WHERE` 子句，則 *`expression`* 求值結果為 false 或 null 的資料列將不會被發佈。請注意，運算式周圍必須加上括號。*`expression`* 會以複寫連線所使用的角色來求值。

*`schema_name`*
:   現有綱要的名稱。

`SET ( publication_parameter [= value] [, ... ] )`
:   此子句會變更原本由 [CREATE PUBLICATION](sql-createpublication.md) 設定的發佈參數。更多資訊請參閱該處。

    <a id="id-1.9.3.25.6.2.4.2.2"></a>

    ### 小心

    變更 `publish_via_partition_root` 參數可能會導致訂閱端的資料遺失或重複，因為它會改變已發佈資料表的識別與結構。請注意，這只會在將分割根資料表指定為複寫目標時發生。

    要避免這個問題，可以在執行 `ALTER PUBLICATION ... SET` 之後、執行 [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](sql-altersubscription.md) 之前，不修改分割區的葉資料表，並且只使用 `copy_data = off` 選項進行重新整理。

*`new_owner`*
:   發佈新擁有者的使用者名稱。

*`new_name`*
:   發佈的新名稱。

<a id="id-1.9.3.25.7"></a>

## 範例

變更發佈，使其只發佈刪除與更新：

```

ALTER PUBLICATION noinsert SET (publish = 'update, delete');
```

將一些資料表加入發佈：

```

ALTER PUBLICATION mypublication ADD TABLE users (user_id, firstname), departments;
```

變更某個資料表所發佈的欄位集合：

```

ALTER PUBLICATION mypublication SET TABLE users (user_id, firstname, lastname), TABLE departments;
```

將綱要 `marketing` 與 `sales` 加入發佈 `sales_publication`：

```

ALTER PUBLICATION sales_publication ADD TABLES IN SCHEMA marketing, sales;
```

將資料表 `users`、`departments` 與綱要 `production` 加入發佈 `production_publication`：

```

ALTER PUBLICATION production_publication ADD TABLE users, departments, TABLES IN SCHEMA production;
```

<a id="id-1.9.3.25.8"></a>

## 相容性

`ALTER PUBLICATION` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.25.9"></a>

## 另請參閱

[CREATE PUBLICATION](sql-createpublication.md), [DROP PUBLICATION](sql-droppublication.md), [CREATE SUBSCRIPTION](sql-createsubscription.md), [ALTER SUBSCRIPTION](sql-altersubscription.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterpublication.html)（原文版本：18.6；核對日期：2026-10-05）
