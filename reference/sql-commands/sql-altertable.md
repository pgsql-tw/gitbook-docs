<a id="SQL-ALTERTABLE"></a><a id="id-1.9.3.35.1"></a>

## ALTER TABLE

ALTER TABLE — 變更資料表的定義

<a id="id-1.9.3.35.4"></a>

## 語法

```

ALTER TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    action [, ... ]
ALTER TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    RENAME CONSTRAINT constraint_name TO new_constraint_name
ALTER TABLE [ IF EXISTS ] name
    RENAME TO new_name
ALTER TABLE [ IF EXISTS ] name
    SET SCHEMA new_schema
ALTER TABLE ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]
ALTER TABLE [ IF EXISTS ] name
    ATTACH PARTITION partition_name { FOR VALUES partition_bound_spec | DEFAULT }
ALTER TABLE [ IF EXISTS ] name
    DETACH PARTITION partition_name [ CONCURRENTLY | FINALIZE ]

where action is one of:

    ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
    DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
    ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ USING expression ]
    ALTER [ COLUMN ] column_name SET DEFAULT expression
    ALTER [ COLUMN ] column_name DROP DEFAULT
    ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
    ALTER [ COLUMN ] column_name SET EXPRESSION AS ( expression )
    ALTER [ COLUMN ] column_name DROP EXPRESSION [ IF EXISTS ]
    ALTER [ COLUMN ] column_name ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]
    ALTER [ COLUMN ] column_name { SET GENERATED { ALWAYS | BY DEFAULT } | SET sequence_option | RESTART [ [ WITH ] restart ] } [...]
    ALTER [ COLUMN ] column_name DROP IDENTITY [ IF EXISTS ]
    ALTER [ COLUMN ] column_name SET STATISTICS { integer | DEFAULT }
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }
    ALTER [ COLUMN ] column_name SET COMPRESSION compression_method
    ADD table_constraint [ NOT VALID ]
    ADD table_constraint_using_index
    ALTER CONSTRAINT constraint_name [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]
    ALTER CONSTRAINT constraint_name [ INHERIT | NO INHERIT ]
    VALIDATE CONSTRAINT constraint_name
    DROP CONSTRAINT [ IF EXISTS ]  constraint_name [ RESTRICT | CASCADE ]
    DISABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE REPLICA TRIGGER trigger_name
    ENABLE ALWAYS TRIGGER trigger_name
    DISABLE RULE rewrite_rule_name
    ENABLE RULE rewrite_rule_name
    ENABLE REPLICA RULE rewrite_rule_name
    ENABLE ALWAYS RULE rewrite_rule_name
    DISABLE ROW LEVEL SECURITY
    ENABLE ROW LEVEL SECURITY
    FORCE ROW LEVEL SECURITY
    NO FORCE ROW LEVEL SECURITY
    CLUSTER ON index_name
    SET WITHOUT CLUSTER
    SET WITHOUT OIDS
    SET ACCESS METHOD { new_access_method | DEFAULT }
    SET TABLESPACE new_tablespace
    SET { LOGGED | UNLOGGED }
    SET ( storage_parameter [= value] [, ... ] )
    RESET ( storage_parameter [, ... ] )
    INHERIT parent_table
    NO INHERIT parent_table
    OF type_name
    NOT OF
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
    REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )

and column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL [ NO INHERIT ] |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ] |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters |
  PRIMARY KEY index_parameters |
  REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{ CHECK ( expression ) [ NO INHERIT ] |
  NOT NULL column_name [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  PRIMARY KEY ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
  FOREIGN KEY ( column_name [, ... ] [, PERIOD column_name ] ) REFERENCES reftable [ ( refcolumn [, ... ]  [, PERIOD refcolumn ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and table_constraint_using_index is:

    [ CONSTRAINT constraint_name ]
    { UNIQUE | PRIMARY KEY } USING INDEX index_name
    [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( column_name [, ... ] ) ]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
[ USING INDEX TABLESPACE tablespace_name ]

exclude_element in an EXCLUDE constraint is:

{ column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

referential_action in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( column_name [, ... ] ) ] | SET DEFAULT [ ( column_name [, ... ] ) ] }
```

<a id="id-1.9.3.35.5"></a>

## 說明

`ALTER TABLE` 會變更現有資料表的定義。它有下列幾種子形式。請注意，每種子形式所需的鎖定層級可能不同。除非另有明確說明，否則會取得 `ACCESS EXCLUSIVE` 鎖定。若指定了多個子命令，所取得的鎖定會是所有子命令所需鎖定中最嚴格的那一個。

<a id="SQL-ALTERTABLE-DESC-ADD-COLUMN"></a>

`ADD [ COLUMN ] [ IF NOT EXISTS ]` [#](#SQL-ALTERTABLE-DESC-ADD-COLUMN)
:   此形式會在資料表中新增欄位，使用與 [`CREATE TABLE`](sql-createtable.md) 相同的語法。若指定了 `IF NOT EXISTS`，且已存在同名的欄位，則不會擲出錯誤。
<a id="SQL-ALTERTABLE-DESC-DROP-COLUMN"></a>

`DROP [ COLUMN ] [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-DROP-COLUMN)
:   此形式會從資料表中移除欄位。涉及該欄位的索引與資料表限制條件也會自動移除。若移除該欄位會導致參照它的多變量統計資訊只包含單一欄位的資料，則該多變量統計資訊也會一併移除。若資料表之外有任何東西相依於該欄位，例如外鍵參照或檢視表，你就需要指定 `CASCADE`。若指定了 `IF EXISTS` 而該欄位不存在，則不會擲出錯誤，而是發出 notice。
<a id="SQL-ALTERTABLE-DESC-SET-DATA-TYPE"></a>

`SET DATA TYPE` [#](#SQL-ALTERTABLE-DESC-SET-DATA-TYPE)

此形式會變更資料表中某個欄位的型別。涉及該欄位的索引與簡單資料表限制條件，會透過重新剖析原先提供的運算式，自動轉換為使用新的欄位型別。選擇性的 `COLLATE` 子句為新欄位指定定序；若省略，則定序為新欄位型別的預設定序。選擇性的 `USING` 子句指定如何從舊值計算新的欄位值；若省略，預設的轉換方式與從舊資料型別到新資料型別的指派轉換相同。若舊型別到新型別之間沒有隱含轉換或指派轉換，就必須提供 `USING` 子句。

使用此形式時，該欄位的統計資訊會被移除，因此建議之後對該資料表執行 [`ANALYZE`](sql-analyze.md)。對於虛擬產生欄位，不需要執行 `ANALYZE`，因為這類欄位永遠不會有統計資訊。
<a id="SQL-ALTERTABLE-DESC-SET-DROP-DEFAULT"></a>

`SET`/`DROP DEFAULT` [#](#SQL-ALTERTABLE-DESC-SET-DROP-DEFAULT)
:   這些形式會設定或移除欄位的預設值（移除等同於將預設值設為 NULL）。新的預設值只會套用於後續的 `INSERT` 或 `UPDATE` 命令；它不會使資料表中已有的資料列發生變更。
<a id="SQL-ALTERTABLE-DESC-SET-DROP-NOT-NULL"></a>

`SET`/`DROP NOT NULL` [#](#SQL-ALTERTABLE-DESC-SET-DROP-NOT-NULL)

這些形式會變更欄位被標記為允許空值或拒絕空值。

只有在資料表中沒有任何紀錄的該欄位含有 `NULL` 值時，才可以對該欄位套用 `SET NOT NULL`。通常這會在 `ALTER TABLE` 期間透過掃描整個資料表來檢查，除非指定了 `NOT VALID`；不過，若存在一個有效的 `CHECK` 限制條件（且未在同一個命令中被移除），能證明不可能存在 `NULL`，則會略過資料表掃描。若欄位具有無效的非空值限制條件，`SET NOT NULL` 會驗證它。

若此資料表是分割區，且某個欄位在父資料表中被標記為 `NOT NULL`，就不能對該欄位執行 `DROP NOT NULL`。若要從所有分割區移除 `NOT NULL` 限制條件，請對父資料表執行 `DROP NOT NULL`。即使父資料表上沒有 `NOT NULL` 限制條件，若有需要，仍然可以將這種限制條件加到個別分割區上；也就是說，即使父資料表允許空值，子資料表也可以不允許空值，但反過來則不行。也可以僅從父資料表（`ONLY`）移除 `NOT NULL` 限制條件，這樣不會從子資料表中移除它。
<a id="SQL-ALTERTABLE-DESC-SET-EXPRESSION"></a>

`SET EXPRESSION AS` [#](#SQL-ALTERTABLE-DESC-SET-EXPRESSION)

此形式會取代產生欄位的運算式。儲存式產生欄位中的既有資料會被重寫，而之後的所有變更都會套用新的產生運算式。

對儲存式產生欄位使用此形式時，其統計資訊會被移除，因此建議之後對該資料表執行 [`ANALYZE`](sql-analyze.md)。對於虛擬產生欄位，不需要執行 `ANALYZE`，因為這類欄位永遠不會有統計資訊。
<a id="SQL-ALTERTABLE-DESC-DROP-EXPRESSION"></a>

`DROP EXPRESSION [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-DROP-EXPRESSION)

此形式會將儲存式產生欄位轉換為一般的基本欄位。欄位中的既有資料會被保留，但之後的變更將不再套用產生運算式。

此形式目前只支援儲存式產生欄位（不支援虛擬產生欄位）。

若指定了 `DROP EXPRESSION IF EXISTS` 而該欄位不是產生欄位，則不會擲出錯誤，而是發出 notice。
<a id="SQL-ALTERTABLE-DESC-GENERATED-IDENTITY"></a>

`ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY`<br>`SET GENERATED { ALWAYS | BY DEFAULT }`<br>`DROP IDENTITY [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-GENERATED-IDENTITY)

這些形式會變更欄位是否為識別欄位，或變更既有識別欄位的產生屬性。詳細資訊請參閱 [`CREATE TABLE`](sql-createtable.md)。與 `SET DEFAULT` 一樣，這些形式只會影響後續 `INSERT` 與 `UPDATE` 命令的行為；它們不會使資料表中已有的資料列發生變更。

若指定了 `DROP IDENTITY IF EXISTS` 而該欄位不是識別欄位，則不會擲出錯誤，而是發出 notice。
<a id="SQL-ALTERTABLE-DESC-SET-SEQUENCE-OPTION"></a>

`SET sequence_option`<br>`RESTART` [#](#SQL-ALTERTABLE-DESC-SET-SEQUENCE-OPTION)
:   這些形式會變更既有識別欄位底層的序列。*`sequence_option`* 是 [`ALTER SEQUENCE`](sql-altersequence.md) 所支援的選項，例如 `INCREMENT BY`。
<a id="SQL-ALTERTABLE-DESC-SET-STATISTICS"></a>

`SET STATISTICS` [#](#SQL-ALTERTABLE-DESC-SET-STATISTICS)
:   此形式會為後續的 [`ANALYZE`](sql-analyze.md) 操作設定各欄位的統計資訊收集目標。目標可設定的範圍為 0 到 10000。將它設為 `DEFAULT` 可恢復使用系統預設的統計目標（[default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)）。（將值設為 -1 是達成相同結果的過時寫法。）關於 PostgreSQL 查詢規劃器如何使用統計資訊的詳細資訊，請參閱[第 14.2 節](../../the-sql-language/performance-tips/planner-stats.md)。

    `SET STATISTICS` 會取得 `SHARE UPDATE EXCLUSIVE` 鎖定。
<a id="SQL-ALTERTABLE-DESC-SET-ATTRIBUTE-OPTION"></a>

`SET ( attribute_option = value [, ... ] )`<br>`RESET ( attribute_option [, ... ] )` [#](#SQL-ALTERTABLE-DESC-SET-ATTRIBUTE-OPTION)

此形式會設定或重設各屬性的選項。目前唯一定義的各屬性選項是 `n_distinct` 與 `n_distinct_inherited`，它們會覆寫後續 [`ANALYZE`](sql-analyze.md) 操作所做的相異值數量估計。`n_distinct` 影響資料表本身的統計資訊，而 `n_distinct_inherited` 影響針對資料表及其繼承子資料表所收集的統計資訊，以及針對分割資料表所收集的統計資訊。當指定的值為正值時，查詢規劃器會假定該欄位恰好包含所指定數量的相異非空值。也可以使用小於 0 且大於或等於 -1 的值，來指定分數形式的值。這會指示查詢規劃器將指定數字的絕對值乘以資料表的估計資料列數，以估計相異值的數量。例如，值為 -1 表示欄位中的所有值都是相異的，而值為 -0.5 表示每個值平均出現兩次。當資料表的大小隨時間變化時，這可能很有用。關於 PostgreSQL 查詢規劃器如何使用統計資訊的詳細資訊，請參閱[第 14.2 節](../../the-sql-language/performance-tips/planner-stats.md)。

變更各屬性的選項會取得 `SHARE UPDATE EXCLUSIVE` 鎖定。
<a id="SQL-ALTERTABLE-DESC-SET-STORAGE"></a>

`SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }` <a id="id-1.9.3.35.5.2.3.12.1.2"></a> [#](#SQL-ALTERTABLE-DESC-SET-STORAGE)
:   此形式會設定欄位的儲存模式。這控制該欄位是以內嵌方式保存，還是保存在次要的 TOAST 資料表中，以及資料是否應該壓縮。`PLAIN` 必須用於像 `integer` 這類固定長度的值，採用內嵌、不壓縮的方式。`MAIN` 用於內嵌、可壓縮的資料。`EXTERNAL` 用於外部、不壓縮的資料，而 `EXTENDED` 用於外部、壓縮的資料。寫 `DEFAULT` 會將儲存模式設為該欄位資料型別的預設模式。對於大多數支援非 `PLAIN` 儲存的資料型別而言，`EXTENDED` 是預設模式。使用 `EXTERNAL` 會讓對非常大的 `text` 與 `bytea` 值所做的子字串操作執行得更快，代價是儲存空間增加。請注意，`ALTER TABLE ... SET STORAGE` 本身不會變更資料表中的任何內容；它只是設定在未來資料表更新時所要採行的策略。詳細資訊請參閱[第 66.2 節](../../internals/storage/storage-toast.md)。
<a id="SQL-ALTERTABLE-DESC-SET-COMPRESSION"></a>

`SET COMPRESSION compression_method` [#](#SQL-ALTERTABLE-DESC-SET-COMPRESSION)
:   此形式會設定欄位的壓縮方法，決定未來插入的值將如何壓縮（前提是儲存模式本來就允許壓縮）。這不會導致資料表被重寫，因此既有資料可能仍以其他壓縮方法壓縮。若以 pg_restore 還原資料表，則所有值都會以所設定的壓縮方法重寫。不過，從另一個關聯插入資料時（例如透過 `INSERT ... SELECT`），來源資料表中的值不一定會被解除 TOAST（detoast），因此任何先前已壓縮的資料可能保留其既有的壓縮方法，而不會以目標欄位的壓縮方法重新壓縮。支援的壓縮方法為 `pglz` 與 `lz4`。（只有在建置 PostgreSQL 時使用了 `--with-lz4`，才能使用 `lz4`。）此外，*`compression_method`* 也可以是 `default`，它會選擇預設行為，也就是在插入資料時參考 [default_toast_compression](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION) 設定來決定要使用的方法。
<a id="SQL-ALTERTABLE-DESC-ADD-TABLE-CONSTRAINT"></a>

`ADD table_constraint [ NOT VALID ]` [#](#SQL-ALTERTABLE-DESC-ADD-TABLE-CONSTRAINT)

此形式會在資料表中新增限制條件，使用與 [`CREATE TABLE`](sql-createtable.md) 相同的限制條件語法，外加 `NOT VALID` 選項；此選項目前只允許用於外鍵、`CHECK` 與非空值限制條件。

通常，此形式會掃描資料表，以驗證資料表中所有既有資料列都滿足新的限制條件。但若使用了 `NOT VALID` 選項，就會略過這個可能很耗時的掃描。該限制條件仍會套用於後續的插入或更新（也就是說，就外鍵而言，除非被參照的資料表中有相符的資料列，否則這些操作會失敗；或者，除非新資料列符合所指定的檢查條件，否則這些操作會失敗）。但在使用 `VALIDATE CONSTRAINT` 選項驗證之前，資料庫不會假定該限制條件對資料表中的所有資料列都成立。關於使用 `NOT VALID` 選項的詳細資訊，請參閱下方的[注意事項](sql-altertable.md#SQL-ALTERTABLE-NOTES)。

雖然大多數形式的 `ADD table_constraint` 都需要 `ACCESS EXCLUSIVE` 鎖定，但 `ADD FOREIGN KEY` 只需要 `SHARE ROW EXCLUSIVE` 鎖定。請注意，除了在宣告該限制條件的資料表上取得的鎖定之外，`ADD FOREIGN KEY` 也會在被參照的資料表上取得 `SHARE ROW EXCLUSIVE` 鎖定。

在分割資料表上新增唯一或主鍵限制條件時，還有額外的限制；請參閱 [`CREATE TABLE`](sql-createtable.md)。
<a id="SQL-ALTERTABLE-DESC-ADD-TABLE-CONSTRAINT-USING-INDEX"></a>

`ADD table_constraint_using_index` [#](#SQL-ALTERTABLE-DESC-ADD-TABLE-CONSTRAINT-USING-INDEX)

此形式會根據現有的唯一值索引，在資料表中新增 `PRIMARY KEY` 或 `UNIQUE` 限制條件。該索引的所有欄位都會納入限制條件中。

該索引不能有運算式欄位，也不能是部分索引。此外，它必須是採用預設排序順序的 B-tree 索引。這些限制確保該索引等同於由一般的 `ADD PRIMARY KEY` 或 `ADD UNIQUE` 命令所建立的索引。

若指定了 `PRIMARY KEY`，且索引的欄位尚未標記為 `NOT NULL`，則此命令會嘗試對每個這樣的欄位執行 `ALTER COLUMN SET NOT NULL`。這需要完整掃描資料表，以驗證這些欄位不含空值。在其他所有情況下，這都是快速的操作。

若有提供限制條件名稱，則索引會被重新命名以符合限制條件名稱。否則，限制條件的名稱會與索引相同。

執行此命令後，該索引就由限制條件「擁有」，就如同該索引是由一般的 `ADD PRIMARY KEY` 或 `ADD UNIQUE` 命令所建立的一樣。特別是，移除限制條件也會使索引一併消失。

此形式目前不支援分割資料表。

<a id="id-1.9.3.35.5.2.3.15.2.7"></a>

### 注意 [#](#sql-altertable-restored-note-1) <a href="#sql-altertable-restored-note-1" id="sql-altertable-restored-note-1"></a>

在需要新增限制條件、又不想長時間阻擋資料表更新的情況下，使用現有索引來新增限制條件可能會很有幫助。做法是使用 `CREATE UNIQUE INDEX CONCURRENTLY` 建立索引，然後使用此語法將它轉換為限制條件。請參閱下方的範例。
<a id="SQL-ALTERTABLE-DESC-ALTER-CONSTRAINT"></a>

`ALTER CONSTRAINT` [#](#SQL-ALTERTABLE-DESC-ALTER-CONSTRAINT)
:   此形式會變更先前所建立之限制條件的屬性。目前只有外鍵限制條件可以用這種方式變更，但請參閱下文。
<a id="SQL-ALTERTABLE-DESC-ALTER-CONSTRAINT-INHERIT"></a>

`ALTER CONSTRAINT ... INHERIT`<br>`ALTER CONSTRAINT ... NO INHERIT` [#](#SQL-ALTERTABLE-DESC-ALTER-CONSTRAINT-INHERIT)
:   這些形式會將可繼承的限制條件修改為不可繼承，或反之。目前只有非空值限制條件可以用這種方式變更。除了變更限制條件的可繼承狀態之外，若是將不可繼承的限制條件標記為可繼承，且該資料表有子資料表，則會在子資料表上新增等效的限制條件。若是在有子資料表的資料表上將可繼承的限制條件標記為不可繼承，則子資料表上對應的限制條件會被標記為不再是繼承而來，但不會被移除。
<a id="SQL-ALTERTABLE-DESC-VALIDATE-CONSTRAINT"></a>

`VALIDATE CONSTRAINT` [#](#SQL-ALTERTABLE-DESC-VALIDATE-CONSTRAINT)

此形式會驗證先前以 `NOT VALID` 建立的外鍵、檢查或非空值限制條件，做法是掃描資料表，確保沒有任何不滿足該限制條件的資料列。若該限制條件被設為 `NOT ENFORCED`，則會擲出錯誤。若限制條件已標記為有效，則不會發生任何事。（關於此命令的用處，請參閱下方[注意事項](sql-altertable.md#SQL-ALTERTABLE-NOTES)中的說明。）

此命令會取得 `SHARE UPDATE EXCLUSIVE` 鎖定。
<a id="SQL-ALTERTABLE-DESC-DROP-CONSTRAINT"></a>

`DROP CONSTRAINT [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-DROP-CONSTRAINT)
:   此形式會移除資料表上指定的限制條件，以及該限制條件底層的任何索引。若指定了 `IF EXISTS` 而該限制條件不存在，則不會擲出錯誤，而是發出 notice。
<a id="SQL-ALTERTABLE-DESC-DISABLE-ENABLE-TRIGGER"></a>

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] TRIGGER` [#](#SQL-ALTERTABLE-DESC-DISABLE-ENABLE-TRIGGER)

這些形式設定屬於該資料表之觸發程序的觸發方式。已停用的觸發程序仍為系統所知，但在其觸發事件發生時不會執行。（對於延遲觸發程序，啟用狀態是在事件發生時檢查，而不是在觸發程序函式實際執行時檢查。）你可以停用或啟用依名稱指定的單一觸發程序、資料表上的所有觸發程序，或只停用或啟用使用者觸發程序（此選項會排除內部產生的限制條件觸發程序，例如用來實作外鍵限制條件，或可延遲的唯一性限制條件與排除限制條件的觸發程序）。停用或啟用內部產生的限制條件觸發程序需要超級使用者權限；這應該謹慎進行，因為若不執行這些觸發程序，當然就無法保證限制條件的完整性。

觸發程序的觸發機制也會受到設定變數 [session_replication_role](../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE) 的影響。單純啟用的觸發程序（預設）會在複寫角色為「origin」（預設）或「local」時觸發。設定為 `ENABLE REPLICA` 的觸發程序只會在工作階段處於「replica」模式時觸發，而設定為 `ENABLE ALWAYS` 的觸發程序則不論目前的複寫角色為何都會觸發。

此機制的效果是，在預設設定下，觸發程序不會在複本上觸發。這很有用，因為若在來源端使用觸發程序在資料表之間傳遞資料，複寫系統也會複寫這些被傳遞的資料；因此觸發程序不應該在複本上再觸發一次，否則會導致資料重複。不過，若觸發程序用於其他目的，例如建立外部警示，則可能適合將它設為 `ENABLE ALWAYS`，使它在複本上也會觸發。

當此命令套用於分割資料表時，分割區中對應的複製（clone）觸發程序的狀態也會一併更新，除非指定了 `ONLY`。

此命令會取得 `SHARE ROW EXCLUSIVE` 鎖定。
<a id="SQL-ALTERTABLE-DESC-DISABLE-ENABLE-RULE"></a>

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] RULE` [#](#SQL-ALTERTABLE-DESC-DISABLE-ENABLE-RULE)

這些形式設定屬於該資料表之重寫規則的觸發方式。已停用的規則仍為系統所知，但在查詢重寫期間不會被套用。其語意與停用／啟用觸發程序相同。對於 `ON SELECT` 規則，此設定會被忽略；這類規則一律會被套用，以便即使目前工作階段處於非預設的複寫角色，檢視表仍能正常運作。

規則的觸發機制也會受到設定變數 [session_replication_role](../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE) 的影響，與上述的觸發程序類似。
<a id="SQL-ALTERTABLE-DESC-DISABLE-ENABLE-ROW-LEVEL-SECURITY"></a>

`DISABLE`/`ENABLE ROW LEVEL SECURITY` [#](#SQL-ALTERTABLE-DESC-DISABLE-ENABLE-ROW-LEVEL-SECURITY)
:   這些形式控制屬於該資料表之資料列安全性原則的套用。若已啟用而該資料表沒有任何原則，則會套用預設拒絕的原則。請注意，即使資料列層級安全性已停用，資料表仍可以有原則存在。在這種情況下，這些原則*不會*被套用，並且會被忽略。另請參閱 [`CREATE POLICY`](sql-createpolicy.md)。
<a id="SQL-ALTERTABLE-DESC-FORCE-ROW-LEVEL-SECURITY"></a>

`NO FORCE`/`FORCE ROW LEVEL SECURITY` [#](#SQL-ALTERTABLE-DESC-FORCE-ROW-LEVEL-SECURITY)
:   這些形式控制當使用者是資料表擁有者時，屬於該資料表之資料列安全性原則的套用。若啟用，則當使用者是資料表擁有者時，會套用資料列層級安全性原則。若停用（預設），則當使用者是資料表擁有者時，不會套用資料列層級安全性。另請參閱 [`CREATE POLICY`](sql-createpolicy.md)。
<a id="SQL-ALTERTABLE-DESC-CLUSTER-ON"></a>

`CLUSTER ON` [#](#SQL-ALTERTABLE-DESC-CLUSTER-ON)

此形式會為未來的 [`CLUSTER`](sql-cluster.md) 操作選擇預設索引。它並不會實際重新叢集資料表。

變更叢集選項會取得 `SHARE UPDATE EXCLUSIVE` 鎖定。
<a id="SQL-ALTERTABLE-DESC-SET-WITHOUT-CLUSTER"></a>

`SET WITHOUT CLUSTER` [#](#SQL-ALTERTABLE-DESC-SET-WITHOUT-CLUSTER)

此形式會從資料表中移除最近使用的 [`CLUSTER`](sql-cluster.md) 索引設定。這會影響未來未指定索引的叢集操作。

變更叢集選項會取得 `SHARE UPDATE EXCLUSIVE` 鎖定。
<a id="SQL-ALTERTABLE-DESC-SET-WITHOUT-OIDS"></a>

`SET WITHOUT OIDS` [#](#SQL-ALTERTABLE-DESC-SET-WITHOUT-OIDS)
:   為了向後相容性而保留的語法，用於移除 `oid` 系統欄位。由於已無法再新增 `oid` 系統欄位，此形式永遠不會有任何效果。
<a id="SQL-ALTERTABLE-DESC-SET-ACCESS-METHOD"></a>

`SET ACCESS METHOD` [#](#SQL-ALTERTABLE-DESC-SET-ACCESS-METHOD)

此形式會使用指定的存取方法重寫資料表，藉此變更資料表的存取方法；指定 `DEFAULT` 會選擇 [default_table_access_method](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD) 設定參數所設定的存取方法。詳細資訊請參閱[第 62 章](../../internals/tableam/README.md)。

套用於分割資料表時，沒有資料需要重寫，但之後建立的分割區預設會使用所指定的存取方法，除非以 `USING` 子句覆寫。指定 `DEFAULT` 會移除先前的值，使未來的分割區預設使用 `default_table_access_method`。
<a id="SQL-ALTERTABLE-DESC-SET-TABLESPACE"></a>

`SET TABLESPACE` [#](#SQL-ALTERTABLE-DESC-SET-TABLESPACE)

此形式會將資料表的資料表空間變更為指定的資料表空間，並將與該資料表相關聯的資料檔案移到新的資料表空間。資料表上的索引（若有的話）不會被移動；但可以用額外的 `SET TABLESPACE` 命令分別移動它們。套用於分割資料表時，不會移動任何東西，但之後以 `CREATE TABLE PARTITION OF` 建立的任何分割區都會使用該資料表空間，除非以 `TABLESPACE` 子句覆寫。

使用 `ALL IN TABLESPACE` 形式，可以移動目前資料庫中位於某個資料表空間內的所有資料表；此形式會先鎖定所有要移動的資料表，然後再逐一移動。此形式也支援 `OWNED BY`，只會移動由指定角色所擁有的資料表。若指定了 `NOWAIT` 選項，則當無法立即取得所有需要的鎖定時，命令就會失敗。請注意，此命令不會移動系統目錄；如有需要，請改用 `ALTER DATABASE` 或明確的 `ALTER TABLE` 呼叫。`information_schema` 中的關聯不被視為系統目錄的一部分，因此會被移動。另請參閱 [`CREATE TABLESPACE`](sql-createtablespace.md)。
<a id="SQL-ALTERTABLE-DESC-SET-LOGGED-UNLOGGED"></a>

`SET { LOGGED | UNLOGGED }` [#](#SQL-ALTERTABLE-DESC-SET-LOGGED-UNLOGGED)

此形式會將資料表從無日誌（unlogged）變更為有日誌（logged），或反之（請參閱 [`UNLOGGED`](sql-createtable.md#SQL-CREATETABLE-UNLOGGED)）。它不能套用於暫存資料表。

這也會變更與該資料表連結之任何序列（用於識別欄位或 serial 欄位）的持久性。不過，也可以另外單獨變更這類序列的持久性。

此形式不支援分割資料表。
<a id="SQL-ALTERTABLE-DESC-SET-STORAGE-PARAMETER"></a>

`SET ( storage_parameter [= value] [, ... ] )` [#](#SQL-ALTERTABLE-DESC-SET-STORAGE-PARAMETER)

此形式會變更資料表的一個或多個儲存參數。可用參數的詳細資訊，請參閱 [`CREATE TABLE`](sql-createtable.md) 文件中的[儲存參數](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS)。請注意，此命令不會立即修改資料表內容；視參數而定，你可能需要重寫資料表才能得到想要的效果。這可以透過 [`VACUUM FULL`](sql-vacuum.md)、[`CLUSTER`](sql-cluster.md)，或某一種會強制重寫資料表的 `ALTER TABLE` 形式來完成。對於與規劃器相關的參數，變更會從下一次鎖定該資料表時開始生效，因此目前正在執行的查詢不會受到影響。

對於 fillfactor、TOAST 與 autovacuum 儲存參數，以及規劃器參數 `parallel_workers`，會取得 `SHARE UPDATE EXCLUSIVE` 鎖定。
<a id="SQL-ALTERTABLE-DESC-RESET-STORAGE-PARAMETER"></a>

`RESET ( storage_parameter [, ... ] )` [#](#SQL-ALTERTABLE-DESC-RESET-STORAGE-PARAMETER)
:   此形式會將一個或多個儲存參數重設為其預設值。與 `SET` 一樣，可能需要重寫資料表才能完整更新資料表。
<a id="SQL-ALTERTABLE-DESC-INHERIT"></a>

`INHERIT parent_table` [#](#SQL-ALTERTABLE-DESC-INHERIT)

此形式會將目標資料表加入為指定父資料表的新子資料表。之後，對父資料表的查詢將包含目標資料表的紀錄。要加入為子資料表，目標資料表必須已經包含與父資料表相同的所有欄位（它也可以有額外的欄位）。這些欄位的資料型別必須相符。

此外，父資料表上的所有 `CHECK` 與 `NOT NULL` 限制條件也必須存在於子資料表上，但標記為不可繼承者（也就是以 `ALTER TABLE ... ADD CONSTRAINT ... NO INHERIT` 建立者）除外，這些會被忽略。所有相符的子資料表限制條件都不得標記為不可繼承。目前不會考慮 `UNIQUE`、`PRIMARY KEY` 與 `FOREIGN KEY` 限制條件，但這在未來可能會改變。
<a id="SQL-ALTERTABLE-DESC-NO-INHERIT"></a>

`NO INHERIT parent_table` [#](#SQL-ALTERTABLE-DESC-NO-INHERIT)
:   此形式會將目標資料表從指定父資料表的子資料表清單中移除。對父資料表的查詢將不再包含取自目標資料表的紀錄。
<a id="SQL-ALTERTABLE-DESC-OF"></a>

`OF type_name` [#](#SQL-ALTERTABLE-DESC-OF)
:   此形式會將資料表連結到複合型別，如同該資料表是由 `CREATE TABLE OF` 所建立的一樣。資料表的欄位名稱與型別清單必須與該複合型別的完全相符。該資料表不得繼承自任何其他資料表。這些限制確保 `CREATE TABLE OF` 會允許等效的資料表定義。
<a id="SQL-ALTERTABLE-DESC-NOT-OF"></a>

`NOT OF` [#](#SQL-ALTERTABLE-DESC-NOT-OF)
:   此形式會解除具型別資料表與其型別之間的關聯。
<a id="SQL-ALTERTABLE-DESC-OWNER-TO"></a>

`OWNER TO` [#](#SQL-ALTERTABLE-DESC-OWNER-TO)
:   此形式會將資料表、序列、檢視表、具體化檢視表或外部資料表的擁有者變更為指定的使用者。
<a id="SQL-ALTERTABLE-REPLICA-IDENTITY"></a>

`REPLICA IDENTITY` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY)
:   此形式會變更寫入預寫日誌（write-ahead log）、用來識別被更新或刪除之資料列的資訊。在大多數情況下，只有當每個欄位的舊值與新值不同時才會記錄舊值；不過，若舊值是以外部方式儲存，則不論是否變更都一律會記錄。除非使用邏輯複寫，否則此選項沒有任何效果。

    <a id="SQL-ALTERTABLE-REPLICA-IDENTITY-DEFAULT"></a>

    `DEFAULT` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-DEFAULT)
    :   記錄主鍵欄位的舊值。這是非系統資料表的預設值。沒有主鍵時，行為與 `NOTHING` 相同。
    <a id="SQL-ALTERTABLE-REPLICA-IDENTITY-USING-INDEX"></a>

    `USING INDEX index_name` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-USING-INDEX)
    :   記錄所指名索引所涵蓋之欄位的舊值；該索引必須是唯一的、非部分的、不可延遲的，並且只包含標記為 `NOT NULL` 的欄位。若此索引被移除，行為與 `NOTHING` 相同。
    <a id="SQL-ALTERTABLE-REPLICA-IDENTITY-FULL"></a>

    `FULL` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-FULL)
    :   記錄資料列中所有欄位的舊值。
    <a id="SQL-ALTERTABLE-REPLICA-IDENTITY-NOTHING"></a>

    `NOTHING` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-NOTHING)
    :   不記錄任何關於舊資料列的資訊。這是系統資料表的預設值。
<a id="SQL-ALTERTABLE-DESC-RENAME"></a>

`RENAME` [#](#SQL-ALTERTABLE-DESC-RENAME)
:   `RENAME` 形式會變更資料表（或索引、序列、檢視表、具體化檢視表或外部資料表）的名稱、資料表中個別欄位的名稱，或資料表之限制條件的名稱。重新命名具有底層索引的限制條件時，該索引也會一併重新命名。這對已儲存的資料沒有任何影響。
<a id="SQL-ALTERTABLE-DESC-SET-SCHEMA"></a>

`SET SCHEMA` [#](#SQL-ALTERTABLE-DESC-SET-SCHEMA)
:   此形式會將資料表移到另一個綱要。相關聯的索引、限制條件，以及由資料表欄位所擁有的序列也會一併移動。
<a id="SQL-ALTERTABLE-ATTACH-PARTITION"></a>

`ATTACH PARTITION partition_name { FOR VALUES partition_bound_spec | DEFAULT }` [#](#SQL-ALTERTABLE-ATTACH-PARTITION)

此形式會將現有的資料表（它本身可能也是分割資料表）附加為目標資料表的分割區。可以使用 `FOR VALUES` 將該資料表附加為特定值的分割區，或使用 `DEFAULT` 將它附加為預設分割區。對於目標資料表中的每個索引，若分割區中已存在有效的等效索引，該索引會被附加到目標資料表的索引，如同執行了 ALTER INDEX ATTACH PARTITION 一樣；否則，會建立新的對應索引。分割區上的無效索引會被略過。請注意，若現有的資料表是外部資料表，且目標資料表上有 `UNIQUE` 索引，則目前不允許將該資料表附加為目標資料表的分割區。（另請參閱 [CREATE FOREIGN TABLE](sql-createforeigntable.md)。）對於目標資料表中存在的每個使用者定義的資料列層級觸發程序，都會在被附加的資料表中建立對應的觸發程序。

使用 `FOR VALUES` 的分割區，其 *`partition_bound_spec`* 使用與 [`CREATE TABLE`](sql-createtable.md) 相同的語法。分割區邊界規格必須符合目標資料表的分割策略與分割鍵。要附加的資料表必須擁有與目標資料表相同的所有欄位，且不能有更多欄位；此外，欄位型別也必須相符。並且，它必須具有目標資料表所有未標記為 `NO INHERIT` 的 `NOT NULL` 與 `CHECK` 限制條件。目前不會考慮 `FOREIGN KEY` 限制條件。若分割區中尚不存在父資料表的 `UNIQUE` 與 `PRIMARY KEY` 限制條件，則會在分割區中建立它們。

若新分割區是一般資料表，會執行完整的資料表掃描，以檢查資料表中的既有資料列沒有違反分割區限制條件。在執行此命令之前，可以先在該資料表上新增一個有效的 `CHECK` 限制條件，只允許滿足所需分割區限制條件的資料列，藉此避免這次掃描。系統會使用該 `CHECK` 限制條件來判定不需要掃描資料表就能驗證分割區限制條件。不過，若任何分割鍵是運算式，且該分割區不接受 `NULL` 值，這種做法就無效。若要附加一個不接受 `NULL` 值的清單分割區，除非分割鍵欄位是運算式，否則也請在該分割鍵欄位上新增 `NOT NULL` 限制條件。

若新分割區是外部資料表，則不會進行任何驗證來確認外部資料表中的所有資料列都遵守分割區限制條件。（請參閱 [CREATE FOREIGN TABLE](sql-createforeigntable.md) 中關於外部資料表上限制條件的討論。）

當資料表有預設分割區時，定義新的分割區會改變預設分割區的分割區限制條件。預設分割區不能包含任何需要移到新分割區的資料列，系統會掃描預設分割區以驗證沒有這樣的資料列存在。這次掃描與新分割區的掃描一樣，若存在適當的 `CHECK` 限制條件就可以避免。同樣與新分割區的掃描一樣，當預設分割區是外部資料表時，一律會略過這次掃描。

附加分割區時，除了在被附加的資料表與預設分割區（若有的話）上取得 `ACCESS EXCLUSIVE` 鎖定之外，還會在父資料表上取得 `SHARE UPDATE EXCLUSIVE` 鎖定。

若被附加的資料表本身是分割資料表，則還必須在其所有子分割區上持有更多鎖定。若預設分割區本身是分割資料表，情況也一樣。如[第 5.12.2.2 節](../../the-sql-language/ddl/ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE-MAINTENANCE)所述，可以透過新增 `CHECK` 限制條件來避免鎖定子分割區。
<a id="SQL-ALTERTABLE-DETACH-PARTITION"></a>

`DETACH PARTITION partition_name [ CONCURRENTLY | FINALIZE ]` [#](#SQL-ALTERTABLE-DETACH-PARTITION)

此形式會卸離目標資料表的指定分割區。被卸離的分割區會繼續以獨立資料表的形式存在，但與它被卸離前所屬的資料表不再有任何關聯。任何已附加到目標資料表之索引的索引都會被卸離。任何作為目標資料表中觸發程序之複製品而建立的觸發程序都會被移除。在外鍵限制條件中參照此分割資料表的任何資料表上，都會取得 `SHARE` 鎖定。

若指定了 `CONCURRENTLY`，它會以較低的鎖定層級執行，以避免阻擋可能正在存取該分割資料表的其他工作階段。在此模式下，內部會使用兩個交易。在第一個交易期間，會在父資料表與分割區上都取得 `SHARE UPDATE EXCLUSIVE` 鎖定，並將分割區標記為正在卸離；此時，該交易會被提交，並等待所有其他正在使用該分割資料表的交易。一旦這些交易全部完成，第二個交易會在分割資料表上取得 `SHARE UPDATE EXCLUSIVE`，並在分割區上取得 `ACCESS EXCLUSIVE`，然後完成卸離作業。系統會在分割區上新增一個與分割區限制條件重複的 `CHECK` 限制條件。`CONCURRENTLY` 不能在交易區塊中執行，且若分割資料表包含預設分割區，則不允許使用。

若指定了 `FINALIZE`，則會完成先前被取消或中斷的 `DETACH CONCURRENTLY` 呼叫。一個分割資料表中，同一時間最多只能有一個分割區處於等待卸離的狀態。

除了 `RENAME`、`SET SCHEMA`、`ATTACH PARTITION` 與 `DETACH PARTITION` 之外，所有作用於單一資料表的 `ALTER TABLE` 形式都可以組合成一份由多項變更構成的清單，一起套用。例如，可以在單一命令中新增數個欄位和／或變更數個欄位的型別。這對大型資料表特別有用，因為只需要對資料表進行一次處理。

你必須擁有該資料表才能使用 `ALTER TABLE`。若要變更資料表的綱要或資料表空間，你還必須擁有新綱要或新資料表空間的 `CREATE` 權限。若要將該資料表加入為某個父資料表的新子資料表，你也必須擁有該父資料表。此外，若要將某個資料表附加為此資料表的新分割區，你必須擁有被附加的資料表。若要變更擁有者，你必須能夠 `SET ROLE` 為新的擁有角色，而且該角色必須擁有該資料表所屬綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立資料表而做到的事。不過，超級使用者無論如何都可以變更任何資料表的擁有權。）若要新增欄位、變更欄位型別或使用 `OF` 子句，你還必須擁有該資料型別的 `USAGE` 權限。

<a id="id-1.9.3.35.6"></a>

## 參數

<a id="SQL-ALTERTABLE-PARMS-IF-EXISTS"></a>

`IF EXISTS` [#](#SQL-ALTERTABLE-PARMS-IF-EXISTS)
:   資料表不存在時不擲出錯誤；此情況會發出 notice。
<a id="SQL-ALTERTABLE-PARMS-NAME"></a>

*`name`* [#](#SQL-ALTERTABLE-PARMS-NAME)
:   要變更之現有資料表的名稱（可選擇以綱要限定）。若在資料表名稱前指定 `ONLY`，則只會變更該資料表。若未指定 `ONLY`，則會變更該資料表及其所有後代資料表（若有的話）。也可以選擇在資料表名稱後指定 `*`，以明確表示包含後代資料表。
<a id="SQL-ALTERTABLE-PARMS-COLUMN-NAME"></a>

*`column_name`* [#](#SQL-ALTERTABLE-PARMS-COLUMN-NAME)
:   新欄位或現有欄位的名稱。
<a id="SQL-ALTERTABLE-PARMS-NEW-COLUMN-NAME"></a>

*`new_column_name`* [#](#SQL-ALTERTABLE-PARMS-NEW-COLUMN-NAME)
:   現有欄位的新名稱。
<a id="SQL-ALTERTABLE-PARMS-NEW-NAME"></a>

*`new_name`* [#](#SQL-ALTERTABLE-PARMS-NEW-NAME)
:   資料表的新名稱。
<a id="SQL-ALTERTABLE-PARMS-DATA-TYPE"></a>

*`data_type`* [#](#SQL-ALTERTABLE-PARMS-DATA-TYPE)
:   新欄位的資料型別，或現有欄位的新資料型別。
<a id="SQL-ALTERTABLE-PARMS-TABLE-CONSTRAINT"></a>

*`table_constraint`* [#](#SQL-ALTERTABLE-PARMS-TABLE-CONSTRAINT)
:   資料表的新資料表限制條件。
<a id="SQL-ALTERTABLE-PARMS-CONSTRAINT-NAME"></a>

*`constraint_name`* [#](#SQL-ALTERTABLE-PARMS-CONSTRAINT-NAME)
:   新限制條件或現有限制條件的名稱。
<a id="SQL-ALTERTABLE-PARMS-CASCADE"></a>

`CASCADE` [#](#SQL-ALTERTABLE-PARMS-CASCADE)
:   自動移除相依於被移除之欄位或限制條件的物件（例如參照該欄位的檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。
<a id="SQL-ALTERTABLE-PARMS-RESTRICT"></a>

`RESTRICT` [#](#SQL-ALTERTABLE-PARMS-RESTRICT)
:   若有任何相依物件，則拒絕移除該欄位或限制條件。這是預設行為。
<a id="SQL-ALTERTABLE-PARMS-TRIGGER-NAME"></a>

*`trigger_name`* [#](#SQL-ALTERTABLE-PARMS-TRIGGER-NAME)
:   要停用或啟用的單一觸發程序名稱。
<a id="SQL-ALTERTABLE-PARMS-ALL"></a>

`ALL` [#](#SQL-ALTERTABLE-PARMS-ALL)
:   停用或啟用屬於該資料表的所有觸發程序。（若其中任何觸發程序是內部產生的限制條件觸發程序，例如用來實作外鍵限制條件，或可延遲的唯一性限制條件與排除限制條件的觸發程序，則需要超級使用者權限。）
<a id="SQL-ALTERTABLE-PARMS-USER"></a>

`USER` [#](#SQL-ALTERTABLE-PARMS-USER)
:   停用或啟用屬於該資料表的所有觸發程序，但內部產生的限制條件觸發程序除外，例如用來實作外鍵限制條件，或可延遲的唯一性限制條件與排除限制條件的觸發程序。
<a id="SQL-ALTERTABLE-PARMS-INDEX-NAME"></a>

*`index_name`* [#](#SQL-ALTERTABLE-PARMS-INDEX-NAME)
:   現有索引的名稱。
<a id="SQL-ALTERTABLE-PARMS-STORAGE-PARAMETER"></a>

*`storage_parameter`* [#](#SQL-ALTERTABLE-PARMS-STORAGE-PARAMETER)
:   資料表儲存參數的名稱。
<a id="SQL-ALTERTABLE-PARMS-VALUE"></a>

*`value`* [#](#SQL-ALTERTABLE-PARMS-VALUE)
:   資料表儲存參數的新值。視參數而定，它可能是數字或單字。
<a id="SQL-ALTERTABLE-PARMS-PARENT-TABLE"></a>

*`parent_table`* [#](#SQL-ALTERTABLE-PARMS-PARENT-TABLE)
:   要與此資料表建立關聯或解除關聯的父資料表。
<a id="SQL-ALTERTABLE-PARMS-NEW-OWNER"></a>

*`new_owner`* [#](#SQL-ALTERTABLE-PARMS-NEW-OWNER)
:   資料表新擁有者的使用者名稱。
<a id="SQL-ALTERTABLE-PARMS-NEW-ACCESS-METHOD"></a>

*`new_access_method`* [#](#SQL-ALTERTABLE-PARMS-NEW-ACCESS-METHOD)
:   資料表將要轉換成的存取方法名稱。
<a id="SQL-ALTERTABLE-PARMS-NEW-TABLESPACE"></a>

*`new_tablespace`* [#](#SQL-ALTERTABLE-PARMS-NEW-TABLESPACE)
:   資料表將要移入的資料表空間名稱。
<a id="SQL-ALTERTABLE-PARMS-NEW-SCHEMA"></a>

*`new_schema`* [#](#SQL-ALTERTABLE-PARMS-NEW-SCHEMA)
:   資料表將要移入的綱要名稱。
<a id="SQL-ALTERTABLE-PARMS-PARTITION-NAME"></a>

*`partition_name`* [#](#SQL-ALTERTABLE-PARMS-PARTITION-NAME)
:   要附加為新分割區，或要從此資料表卸離的資料表名稱。
<a id="SQL-ALTERTABLE-PARMS-PARTITION-BOUND-SPEC"></a>

*`partition_bound_spec`* [#](#SQL-ALTERTABLE-PARMS-PARTITION-BOUND-SPEC)
:   新分割區的分割區邊界規格。關於其語法的詳細資訊，請參閱 [CREATE TABLE](sql-createtable.md)。

<a id="SQL-ALTERTABLE-NOTES"></a>

## 注意事項

關鍵字 `COLUMN` 是贅字，可以省略。

使用 `ADD COLUMN` 新增欄位並指定了非易變（non-volatile）的 `DEFAULT` 時，預設值會在陳述式執行時計算，結果會儲存在資料表的中繼資料中；存取任何既有資料列時，都會傳回這個值。該值只會在資料表被重寫時才實際套用，這使得 `ALTER TABLE` 即使在大型資料表上也非常快速。若未指定任何欄位限制條件，則會使用 NULL 作為 `DEFAULT`。這兩種情況都不需要重寫資料表。

新增具有易變（volatile）`DEFAULT`（例如 `clock_timestamp()`）的欄位、儲存式產生欄位、識別欄位，或資料型別為具有限制條件之網域的欄位，都會導致整個資料表及其索引被重寫。新增虛擬產生欄位則永遠不需要重寫。

變更現有欄位的型別通常會導致整個資料表及其索引被重寫。例外情況是：變更現有欄位的型別時，若 `USING` 子句不會改變欄位內容，且舊型別可以二進位相容地轉換為新型別，或舊型別是建立在新型別之上、不帶限制條件的網域，則不需要重寫資料表。不過，除非系統能驗證新索引在邏輯上與既有索引等效，否則索引仍會被重建。例如，若欄位的定序已變更，就需要重建索引，因為新的排序順序可能不同。不過，在定序沒有變更的情況下，欄位可以從 `text` 變更為 `varchar`（或反之）而不必重建索引，因為這些資料型別的排序方式相同。

對大型資料表而言，重建資料表和／或索引可能需要相當長的時間，而且暫時會需要多達兩倍的磁碟空間。

新增 `CHECK` 或 `NOT NULL` 限制條件需要掃描資料表，以驗證既有資料列符合限制條件，但不需要重寫資料表。若 `CHECK` 限制條件是以 `NOT ENFORCED` 新增，則不會進行任何驗證。

同樣地，附加新分割區時，可能會掃描該分割區，以驗證既有資料列符合分割區限制條件。

之所以提供在單一 `ALTER TABLE` 中指定多項變更的選項，主要原因是這樣就可以將多次資料表掃描或重寫合併為對資料表的單次處理。

掃描大型資料表以驗證新的外鍵、檢查或非空值限制條件可能需要很長的時間，而且在 `ALTER TABLE ADD CONSTRAINT` 命令提交之前，對該資料表的其他更新都會被阻擋。`NOT VALID` 限制條件選項的主要目的，是減少新增限制條件對並行更新的影響。使用 `NOT VALID` 時，`ADD CONSTRAINT` 命令不會掃描資料表，並且可以立即提交。之後，可以發出 `VALIDATE CONSTRAINT` 命令來驗證既有資料列是否滿足限制條件。驗證步驟不需要阻擋並行更新，因為它知道其他交易會對它們插入或更新的資料列強制執行該限制條件；只有原先已存在的資料列需要檢查。因此，驗證只會在被變更的資料表上取得 `SHARE UPDATE EXCLUSIVE` 鎖定。（若限制條件是外鍵，則還需要在該限制條件所參照的資料表上取得 `ROW SHARE` 鎖定。）除了改善並行性之外，在已知資料表含有既存違規資料的情況下，使用 `NOT VALID` 與 `VALIDATE CONSTRAINT` 也可能很有用。一旦限制條件就位，就無法再插入新的違規資料，而既有的問題可以從容修正，直到 `VALIDATE CONSTRAINT` 最終成功為止。

`DROP COLUMN` 形式並不會實際移除欄位，而只是讓它對 SQL 操作不可見。之後在該資料表中的插入與更新操作，會為該欄位儲存空值。因此，移除欄位很快，但不會立即縮小資料表在磁碟上的大小，因為被移除欄位所佔用的空間並不會被回收。隨著既有資料列被更新，這些空間會逐漸被回收。

若要強制立即回收被移除欄位所佔用的空間，你可以執行某一種會重寫整個資料表的 `ALTER TABLE` 形式。這會重建每一筆資料列，並將被移除的欄位以空值取代。

會重寫資料表的 `ALTER TABLE` 形式不是 MVCC 安全的。資料表重寫之後，若並行交易使用的是在重寫發生之前取得的快照，則對這些交易而言，該資料表會顯得是空的。詳細資訊請參閱[第 13.6 節](../../the-sql-language/mvcc/mvcc-caveats.md)。

`SET DATA TYPE` 的 `USING` 選項實際上可以指定任何涉及該資料列舊值的運算式；也就是說，它除了可以參照正在轉換的欄位之外，也可以參照其他欄位。這使得 `SET DATA TYPE` 語法可以進行非常廣泛的轉換。由於這種彈性，`USING` 運算式不會套用到欄位的預設值（若有的話）；其結果可能不是預設值所要求的常數運算式。這表示當舊型別到新型別之間沒有隱含轉換或指派轉換時，即使提供了 `USING` 子句，`SET DATA TYPE` 仍可能無法轉換預設值。在這種情況下，請先使用 `DROP DEFAULT` 移除預設值，執行 `ALTER TYPE`，然後再使用 `SET DEFAULT` 加上適當的新預設值。類似的考量也適用於涉及該欄位的索引與限制條件。

若資料表有任何後代資料表，則不允許在父資料表中新增欄位、重新命名欄位或變更欄位型別，而不對後代資料表做同樣的變更。這確保後代資料表的欄位一定與父資料表相符。同樣地，`CHECK` 限制條件不能只在父資料表中重新命名，而不同時在所有後代資料表中重新命名，如此 `CHECK` 限制條件在父資料表與其後代資料表之間也會保持相符。（不過，該限制不適用於以索引為基礎的限制條件。）此外，由於從父資料表查詢時也會從其後代資料表查詢，因此除非父資料表上的限制條件在那些後代資料表上也被標記為有效，否則它不能被標記為有效。在上述所有情況下，`ALTER TABLE ONLY` 都會被拒絕。

遞迴的 `DROP COLUMN` 操作，只有在後代資料表沒有從任何其他父資料表繼承該欄位，且從未獨立定義過該欄位時，才會移除後代資料表的該欄位。非遞迴的 `DROP COLUMN`（即 `ALTER TABLE ONLY ... DROP COLUMN`）永遠不會移除任何後代資料表的欄位，而是將它們標記為獨立定義，而非繼承而來。對分割資料表執行非遞迴的 `DROP COLUMN` 命令會失敗，因為資料表的所有分割區都必須具有與分割根資料表相同的欄位。

識別欄位的動作（`ADD GENERATED`、`SET` 等、`DROP IDENTITY`），以及 `CLUSTER`、`OWNER` 與 `TABLESPACE` 動作，永遠不會遞迴到後代資料表；也就是說，它們的行為一律如同指定了 `ONLY`。影響觸發程序狀態的動作會遞迴到分割資料表的分割區（除非指定了 `ONLY`），但永遠不會遞迴到傳統繼承的後代資料表。新增限制條件時，只有對未標記為 `NO INHERIT` 的 `CHECK` 限制條件才會遞迴。

不允許變更系統目錄資料表的任何部分。

有效參數的進一步說明，請參閱 [CREATE TABLE](sql-createtable.md)。[第 5 章](../../the-sql-language/ddl/README.md)有更多關於繼承的資訊。

<a id="id-1.9.3.35.8"></a>

## 範例

將 `varchar` 型別的欄位新增到資料表：

```

ALTER TABLE distributors ADD COLUMN address varchar(30);
```

這會讓資料表中所有既有資料列的新欄位都填入空值。

新增具有非空值預設值的欄位：

```

ALTER TABLE measurements
  ADD COLUMN mtime timestamp with time zone DEFAULT now();
```

既有資料列的新欄位會填入目前時間作為其值，之後新的資料列則會取得各自插入時的時間。

新增欄位，並以不同於之後要使用之預設值的值來填入它：

```

ALTER TABLE transactions
  ADD COLUMN status varchar(30) DEFAULT 'old',
  ALTER COLUMN status SET default 'current';
```

既有資料列會填入 `old`，但之後命令的預設值會是 `current`。效果與在兩個獨立的 `ALTER TABLE` 命令中分別下達這兩個子命令相同。

從資料表中移除欄位：

```

ALTER TABLE distributors DROP COLUMN address RESTRICT;
```

在一次操作中變更兩個現有欄位的型別：

```

ALTER TABLE distributors
    ALTER COLUMN address TYPE varchar(80),
    ALTER COLUMN name TYPE varchar(100);
```

透過 `USING` 子句，將包含 Unix 時間戳記的整數欄位變更為 `timestamp with time zone`：

```

ALTER TABLE foo
    ALTER COLUMN foo_timestamp SET DATA TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second';
```

同樣的操作，但該欄位具有無法自動轉換為新資料型別的預設值運算式：

```

ALTER TABLE foo
    ALTER COLUMN foo_timestamp DROP DEFAULT,
    ALTER COLUMN foo_timestamp TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second',
    ALTER COLUMN foo_timestamp SET DEFAULT now();
```

重新命名現有欄位：

```

ALTER TABLE distributors RENAME COLUMN address TO city;
```

重新命名現有資料表：

```

ALTER TABLE distributors RENAME TO suppliers;
```

重新命名現有限制條件：

```

ALTER TABLE distributors RENAME CONSTRAINT zipchk TO zip_check;
```

為欄位新增非空值限制條件：

```

ALTER TABLE distributors ALTER COLUMN street SET NOT NULL;
```

從欄位移除非空值限制條件：

```

ALTER TABLE distributors ALTER COLUMN street DROP NOT NULL;
```

為資料表及其所有子資料表新增檢查限制條件：

```

ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5);
```

只為資料表新增檢查限制條件，而不加到其子資料表：

```

ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5) NO INHERIT;
```

（未來的子資料表也不會繼承此檢查限制條件。）

從資料表及其所有子資料表移除檢查限制條件：

```

ALTER TABLE distributors DROP CONSTRAINT zipchk;
```

只從單一資料表移除檢查限制條件：

```

ALTER TABLE ONLY distributors DROP CONSTRAINT zipchk;
```

（所有子資料表上的該檢查限制條件仍會保留。）

為資料表新增外鍵限制條件：

```

ALTER TABLE distributors ADD CONSTRAINT distfk FOREIGN KEY (address) REFERENCES addresses (address);
```

以對其他工作影響最小的方式，為資料表新增外鍵限制條件：

```

ALTER TABLE distributors ADD CONSTRAINT distfk FOREIGN KEY (address) REFERENCES addresses (address) NOT VALID;
ALTER TABLE distributors VALIDATE CONSTRAINT distfk;
```

為資料表新增（多欄位）唯一性限制條件：

```

ALTER TABLE distributors ADD CONSTRAINT dist_id_zipcode_key UNIQUE (dist_id, zipcode);
```

為資料表新增自動命名的主鍵限制條件；請注意，一個資料表永遠只能有一個主鍵：

```

ALTER TABLE distributors ADD PRIMARY KEY (dist_id);
```

將資料表移到不同的資料表空間：

```

ALTER TABLE distributors SET TABLESPACE fasttablespace;
```

將資料表移到不同的綱要：

```

ALTER TABLE myschema.distributors SET SCHEMA yourschema;
```

重建主鍵限制條件，且在重建索引期間不阻擋更新：

```

CREATE UNIQUE INDEX CONCURRENTLY dist_id_temp_idx ON distributors (dist_id);
ALTER TABLE distributors DROP CONSTRAINT distributors_pkey,
    ADD CONSTRAINT distributors_pkey PRIMARY KEY USING INDEX dist_id_temp_idx;
```

將分割區附加到範圍分割資料表：

```

ALTER TABLE measurement
    ATTACH PARTITION measurement_y2016m07 FOR VALUES FROM ('2016-07-01') TO ('2016-08-01');
```

將分割區附加到清單分割資料表：

```

ALTER TABLE cities
    ATTACH PARTITION cities_ab FOR VALUES IN ('a', 'b');
```

將分割區附加到雜湊分割資料表：

```

ALTER TABLE orders
    ATTACH PARTITION orders_p4 FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

將預設分割區附加到分割資料表：

```

ALTER TABLE cities
    ATTACH PARTITION cities_partdef DEFAULT;
```

從分割資料表卸離分割區：

```

ALTER TABLE measurement
    DETACH PARTITION measurement_y2015m12;
```

<a id="id-1.9.3.35.9"></a>

## 相容性

`ADD [COLUMN]`、`DROP [COLUMN]`、`DROP IDENTITY`、`RESTART`、`SET DEFAULT`、`SET DATA TYPE`（不含 `USING`）、`SET GENERATED` 與 `SET sequence_option` 這些形式符合 SQL 標準。當省略 `USING INDEX` 與 `NOT VALID` 子句，且限制條件類型為 `CHECK`、`UNIQUE`、`PRIMARY KEY` 或 `REFERENCES` 之一時，`ADD table_constraint` 形式符合 SQL 標準。其他形式是 PostgreSQL 對 SQL 標準的擴充。此外，在單一 `ALTER TABLE` 命令中指定超過一項操作的能力，也是一項擴充。

`ALTER TABLE DROP COLUMN` 可以用來移除資料表唯一的欄位，留下沒有任何欄位的資料表。這是對 SQL 的擴充，SQL 不允許零欄位的資料表。

<a id="id-1.9.3.35.10"></a>

## 另請參閱

[CREATE TABLE](sql-createtable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertable.html)（原文版本：18.6；核對日期：2026-10-04）
