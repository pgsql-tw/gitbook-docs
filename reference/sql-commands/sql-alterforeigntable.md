<a id="SQL-ALTERFOREIGNTABLE"></a><a id="id-1.9.3.13.1"></a>

## ALTER FOREIGN TABLE

ALTER FOREIGN TABLE — 變更外部資料表的定義

<a id="id-1.9.3.13.4"></a>

## 語法

```

ALTER FOREIGN TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    action [, ... ]
ALTER FOREIGN TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER FOREIGN TABLE [ IF EXISTS ] name
    RENAME TO new_name
ALTER FOREIGN TABLE [ IF EXISTS ] name
    SET SCHEMA new_schema

where action is one of:

    ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
    DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
    ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ]
    ALTER [ COLUMN ] column_name SET DEFAULT expression
    ALTER [ COLUMN ] column_name DROP DEFAULT
    ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
    ALTER [ COLUMN ] column_name SET STATISTICS integer
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }
    ALTER [ COLUMN ] column_name OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ])
    ADD table_constraint [ NOT VALID ]
    VALIDATE CONSTRAINT constraint_name
    DROP CONSTRAINT [ IF EXISTS ]  constraint_name [ RESTRICT | CASCADE ]
    DISABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE REPLICA TRIGGER trigger_name
    ENABLE ALWAYS TRIGGER trigger_name
    SET WITHOUT OIDS
    INHERIT parent_table
    NO INHERIT parent_table
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
    OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ])
```

<a id="id-1.9.3.13.5"></a>

## 說明

`ALTER FOREIGN TABLE` 會變更現有外部資料表的定義。它有以下幾種子形式：

`ADD [ COLUMN ] [ IF NOT EXISTS ]`
:   此形式會在外部資料表中新增欄位，使用與 [`CREATE FOREIGN TABLE`](sql-createforeigntable.md) 相同的語法。若指定了 `IF NOT EXISTS`，且已存在同名的欄位，則不會擲出錯誤。與在一般資料表中新增欄位不同，底層儲存不會有任何變化：此動作只是宣告現在可以透過該外部資料表存取某個新欄位。

`DROP [ COLUMN ] [ IF EXISTS ]`
:   此形式會從外部資料表中移除欄位。若資料表以外有任何東西相依於該欄位（例如檢視表），你需要指定 `CASCADE`。若指定了 `IF EXISTS` 而該欄位不存在，則不會擲出錯誤；此情況會改為發出 notice。

`SET DATA TYPE`
:   此形式會變更外部資料表中某個欄位的型別。同樣地，這對任何底層儲存都沒有影響：此動作只是變更 PostgreSQL 認定該欄位所具有的型別。

`SET`/`DROP DEFAULT`
:   這些形式會設定或移除欄位的預設值。預設值只會套用於後續的 `INSERT` 或 `UPDATE` 命令；它們不會使資料表中已有的資料列改變。

`SET`/`DROP NOT NULL`
:   將欄位標記為允許或不允許 null 值。

`SET STATISTICS`
:   此形式會為後續的 [`ANALYZE`](sql-analyze.md) 操作設定逐欄位的統計資訊收集目標。更多細節請參閱 [`ALTER TABLE`](sql-altertable.md) 中類似的形式。

`SET ( attribute_option = value [, ... ] )`<br>`RESET ( attribute_option [, ... ] )`
:   此形式會設定或重設逐屬性的選項。更多細節請參閱 [`ALTER TABLE`](sql-altertable.md) 中類似的形式。

`SET STORAGE`
:   此形式會設定欄位的儲存模式。更多細節請參閱 [`ALTER TABLE`](sql-altertable.md) 中類似的形式。請注意，除非該資料表的外部資料包裝器選擇理會儲存模式，否則儲存模式不會有任何作用。

`ADD table_constraint [ NOT VALID ]`

此形式會在外部資料表中新增限制條件，使用與 [`CREATE FOREIGN TABLE`](sql-createforeigntable.md) 相同的語法。目前只支援 `CHECK` 與 `NOT NULL` 限制條件。

與在一般資料表中新增限制條件不同，此動作不會做任何事來驗證限制條件是否正確；它只是宣告應假定某個新條件對外部資料表中的所有資料列都成立。（請參閱 [`CREATE FOREIGN TABLE`](sql-createforeigntable.md) 中的討論。）若限制條件被標記為 `NOT VALID`（只允許用於 `CHECK` 的情況），則不會假定它成立，只會將它記錄下來，以供未來可能的使用。

`VALIDATE CONSTRAINT`
:   此形式會將先前標記為 `NOT VALID` 的限制條件標記為有效。此動作不會驗證限制條件，但之後的查詢會假定它成立。

`DROP CONSTRAINT [ IF EXISTS ]`
:   此形式會移除外部資料表上指定的限制條件。若指定了 `IF EXISTS` 而該限制條件不存在，則不會擲出錯誤；此情況會改為發出 notice。

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] TRIGGER`
:   這些形式會設定屬於該外部資料表之觸發程序的觸發方式。更多細節請參閱 [`ALTER TABLE`](sql-altertable.md) 中類似的形式。

`SET WITHOUT OIDS`
:   為了向後相容性而保留、用來移除 `oid` 系統欄位的語法。由於已無法再新增 `oid` 系統欄位，此語法永遠不會有任何作用。

`INHERIT parent_table`
:   此形式會將目標外部資料表加入為指定父資料表的新子資料表。更多細節請參閱 [`ALTER TABLE`](sql-altertable.md) 中類似的形式。

`NO INHERIT parent_table`
:   此形式會將目標外部資料表從指定父資料表的子資料表清單中移除。

`OWNER`
:   此形式會將外部資料表的擁有者變更為指定的使用者。

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`
:   變更外部資料表或其中某個欄位的選項。`ADD`、`SET` 與 `DROP` 指定要執行的動作。若未明確指定操作，則假定為 `ADD`。不允許重複的選項名稱（不過，資料表選項與欄位選項同名是可以的）。選項名稱與值也會經由外部資料包裝器函式庫驗證。

`RENAME`
:   `RENAME` 形式會變更外部資料表的名稱，或外部資料表中個別欄位的名稱。

`SET SCHEMA`
:   此形式會將外部資料表移到另一個綱要。

除了 `RENAME` 與 `SET SCHEMA` 之外，所有動作都可以組合成一個包含多項變更的清單，一併平行套用。例如，可以在單一命令中新增數個欄位和／或變更數個欄位的型別。

若命令寫成 `ALTER FOREIGN TABLE IF EXISTS ...`，而該外部資料表不存在，則不會擲出錯誤；此情況會發出 notice。

你必須擁有該資料表，才能使用 `ALTER FOREIGN TABLE`。若要變更外部資料表的綱要，你還必須擁有新綱要的 `CREATE` 權限。若要變更擁有者，你必須能對新的擁有者角色執行 `SET ROLE`，且該角色必須擁有該資料表所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立資料表而做到的事。不過，超級使用者無論如何都可以變更任何資料表的擁有權。）若要新增欄位或變更欄位型別，你還必須擁有該資料型別的 `USAGE` 權限。

<a id="id-1.9.3.13.6"></a>

## 參數

*`name`*
:   要變更的現有外部資料表名稱（可能以綱要限定）。若在資料表名稱前指定 `ONLY`，則只會變更該資料表。若未指定 `ONLY`，則會變更該資料表及其所有後代資料表（若有的話）。也可以選擇在資料表名稱後指定 `*`，明確表示包含後代資料表。

*`column_name`*
:   新欄位或現有欄位的名稱。

*`new_column_name`*
:   現有欄位的新名稱。

*`new_name`*
:   資料表的新名稱。

*`data_type`*
:   新欄位的資料型別，或現有欄位的新資料型別。

*`table_constraint`*
:   外部資料表的新資料表限制條件。

*`constraint_name`*
:   要移除的現有限制條件名稱。

`CASCADE`
:   自動移除相依於被移除之欄位或限制條件的物件（例如參照該欄位的檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何相依物件，則拒絕移除該欄位或限制條件。這是預設行為。

*`trigger_name`*
:   要停用或啟用的單一觸發程序名稱。

`ALL`
:   停用或啟用屬於該外部資料表的所有觸發程序。（若其中任何觸發程序是內部產生的觸發程序，則需要超級使用者權限。核心系統不會在外部資料表上加入這類觸發程序，但附加程式碼可能會這麼做。）

`USER`
:   停用或啟用屬於該外部資料表的所有觸發程序，但內部產生的觸發程序除外。

*`parent_table`*
:   要與此外部資料表建立或解除關聯的父資料表。

*`new_owner`*
:   資料表新擁有者的使用者名稱。

*`new_schema`*
:   資料表要移入的綱要名稱。

<a id="id-1.9.3.13.7"></a>

## 注意事項

關鍵字 `COLUMN` 是贅字，可以省略。

使用 `ADD COLUMN` 或 `DROP COLUMN` 新增或移除欄位、新增 `NOT NULL` 或 `CHECK` 限制條件，或使用 `SET DATA TYPE` 變更欄位型別時，都不會檢查與外部伺服器的一致性。確保資料表定義與遠端相符，是使用者的責任。

關於有效參數的進一步說明，請參閱 [`CREATE FOREIGN TABLE`](sql-createforeigntable.md)。

<a id="id-1.9.3.13.8"></a>

## 範例

將欄位標記為非 null：

```

ALTER FOREIGN TABLE distributors ALTER COLUMN street SET NOT NULL;
```

變更外部資料表的選項：

```

ALTER FOREIGN TABLE myschema.distributors OPTIONS (ADD opt1 'value', SET opt2 'value2', DROP opt3);
```

<a id="id-1.9.3.13.9"></a>

## 相容性

`ADD`、`DROP` 與 `SET DATA TYPE` 形式符合 SQL 標準。其他形式是 PostgreSQL 對 SQL 標準的擴充。此外，在單一 `ALTER FOREIGN TABLE` 命令中指定超過一項操作的能力，也是擴充語法。

`ALTER FOREIGN TABLE DROP COLUMN` 可以用來移除外部資料表唯一的欄位，留下沒有任何欄位的資料表。這是對 SQL 的擴充，SQL 不允許零欄位的外部資料表。

<a id="id-1.9.3.13.10"></a>

## 另請參閱

[CREATE FOREIGN TABLE](sql-createforeigntable.md), [DROP FOREIGN TABLE](sql-dropforeigntable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterforeigntable.html)（原文版本：18.6；核對日期：2026-10-05）
