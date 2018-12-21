# ALTER TABLE

ALTER TABLE — 變更資料表的定義

### 語法

```text
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
    ATTACH PARTITION partition_name FOR VALUES partition_bound_spec
ALTER TABLE [ IF EXISTS ] name
    DETACH PARTITION partition_name

where action is one of:

    ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
    DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
    ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ USING expression ]
    ALTER [ COLUMN ] column_name SET DEFAULT expression
    ALTER [ COLUMN ] column_name DROP DEFAULT
    ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
    ALTER [ COLUMN ] column_name ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]
    ALTER [ COLUMN ] column_name { SET GENERATED { ALWAYS | BY DEFAULT } | SET sequence_option | RESTART [ [ WITH ] restart ] } [...]
    ALTER [ COLUMN ] column_name DROP IDENTITY [ IF EXISTS ]
    ALTER [ COLUMN ] column_name SET STATISTICS integer
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
    ADD table_constraint [ NOT VALID ]
    ADD table_constraint_using_index
    ALTER CONSTRAINT constraint_name [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]
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
    SET WITH OIDS
    SET WITHOUT OIDS
    SET TABLESPACE new_tablespace
    SET { LOGGED | UNLOGGED }
    SET ( storage_parameter = value [, ... ] )
    RESET ( storage_parameter [, ... ] )
    INHERIT parent_table
    NO INHERIT parent_table
    OF type_name
    NOT OF
    OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
    REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }

and table_constraint_using_index is:

    [ CONSTRAINT constraint_name ]
    { UNIQUE | PRIMARY KEY } USING INDEX index_name
    [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]
```

### 說明

`ALTER TABLE` 變更現有資料表的定義。有幾個子命令描述如下。請注意，每個子命令所需的鎖定等級可能不同。除非明確指出，否則都是 ACCESS EXCLUSIVE 鎖定。當列出多個子命令時，所有子命令所需的鎖以最嚴格的為準。

`ADD COLUMN [ IF NOT EXISTS ]`

該資料表使用與 [CREATE TABLE](create-table.md) 相同的語法在資料表中增加一個新的欄位。如果 IF NOT EXISTS 被指定，並且欄位已經存在這個名稱，則可以避免引發錯誤。

`DROP COLUMN [ IF EXISTS ]`

從該資料表中刪除一個欄位。涉及該欄位的索引和資料表限制條件也將自動刪除。如果刪除的欄位會導致統計信息僅包含單個欄位的資料的話，那麼引用刪除欄位的多變量統計數據也將被刪除。如果資料表外的任何內容取決於該欄位，例如外部鍵引用或 view，則需要使用 CASCADE。 如果指定 IF EXISTS 但該欄位卻不存在，則不會引發錯誤。通常在這種情況下，會發出提示訊息。

`SET DATA TYPE`

這種語法用於變更一個資料表中欄位的資料型別。涉及該欄位的索引和簡單的資料表限制條件將透過重新分析原始提供的表示式自動轉換為使用新的欄位型別。可選用的 COLLATE 子句指定新欄位的排序規則；如果省略的話，則排序規則是新欄位型別的預設值。可選用的 USING 子句指定如何從舊值計算為新的欄位值；如果省略，則預設轉換與從舊資料類型到新欄位轉換的賦值相同。 如果沒有隱含或賦值從舊型別轉換為新型別，則必須提供 USING 子句。

`SET`/`DROP DEFAULT`

這個語法設定或刪除欄位的預設值。預設值僅適用於其後續的 INSERT 或 UPDATE 指令；它不會變更資料表中已有的資料列。

`SET`/`DROP NOT NULL`

這個語法會變更欄位是否標記為允許空值或拒絕空值。當欄位不應該包含空值時，您就可以使用 SET NOT NULL。

如果此資料表是一個資料表分割區，而在父資料表中標記為 NOT NULL，則不能在欄位上執行 DROP NOT NULL。要從所有分割區中刪除 NOT NULL 約束，請在父資料表上執行 DROP NOT NULL。即使父級沒有 NOT NULL 限制條件，如果需要，這樣的限制條件仍然可以加到單獨的分割區中；也就是說，即使父資料表允許他們，子資料表們也可以不允許使用空值，但是反過來也是如此。

`ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY`  
`SET GENERATED { ALWAYS | BY DEFAULT }`  
`DROP IDENTITY [ IF EXISTS ]`

這個語法會變更欄位是否為標識欄位\(identity column\)或變更現有標識欄位的生成屬性。有關詳細訊息，請參閱 [CREATE TABLE](create-table.md)。

如果指定了 DROP IDENTITY IF EXISTS 而該欄位不是標識欄位，則不會引發錯誤。 在這種情況下，會發布通知。

`SET` _`sequence_option`_  
`RESTART`

這個語法變更現有標識欄下的序列設定。sequence\_option 是 [ALTER SEQUENCE](alter-sequence.md) 支援的選項，像是 INCREMENT BY。

`SET STATISTICS`

此語法為隨後的 [ANALYZE](analyze.md) 操作設定每個欄位的統計目標。目標可以設定在 0 到 10000 範圍內；或者，將其設定為 -1 以恢復為使用系統預設的統計訊息目標（[default\_statistics\_target](../../server-administration/server-configuration/query-planning.md#19-7-4-other-planner-options)）。有關 PostgreSQL 查詢規劃器使用統計訊息的更多資訊，請參閱[第 14.2 節](../../the-sql-language/performance-tips/statistics-used-by-the-planner.md)。

`SET STATISTICS` 會要求一個 `SHARE UPDATE EXCLUSIVE` 的鎖定。

`SET (` _`attribute_option`_ = _`value`_ \[, ... \] \)  
`RESET (` _`attribute_option`_ \[, ... \] \)

此語法設定或重置每個屬性選項。目前，只有定義的每個屬性選項是 n\_distinct 和 n\_distinct\_inherited，它們會覆蓋後續 [ANALYZE](analyze.md) 操作所做的不同值的估計數量。 n\_distinct 會影響資料表本身的統計訊息，而 n\_distinct\_inherited 會影響為該表及其繼承子資料表所收集的統計訊息。當設定為正值時，ANALYZE 將假定該欄位正好包含指定數量的相異非空值。當設定為負值（必須大於或等於 -1）時，ANALYZE 將假定欄位中相異非空值的數量與表的大小成線性關係；準確的計數是透過將估計的資料表大小乘以給定數字的絕對值來計算。例如，值 -1 意味著欄位中的所有值都是不同的，而值 -0.5 意味著每個值在平均值上會出現兩次。當資料表的大小隨時間變化時這很有用，因為在查詢計劃階段之前，不會執行資料表中行數的乘法運算。指定值 0 以恢復到一般性估計不同值的數量。有關 PostgreSQL 查詢規劃器使用統計資訊的更多訊息，請參閱[第 14.2 節](../../the-sql-language/performance-tips/statistics-used-by-the-planner.md)。

變更每個屬性選項會要求取得一個 SHARE UPDATE EXCLUSIVE 鎖定。

`SET STORAGE`

此語法設定欄位的儲存模式。 這將控制此欄位是以內建方式保存還是以輔助 TOAST 方式保存，以及是否應該壓縮資料。PLAIN 必須用於固定長度值（如整數），並且是內建的，未壓縮的。MAIN 用於內建可壓縮資料。EXTERNAL 用於外部未壓縮資料，EXTENDED 用於外部壓縮資料。EXTENDED 是非 PLAIN 儲存的大多數資料型別的預設值。 使用 EXTERNAL 將使得對非常大的字串和 bytea 值進行子字串處理的速度更快，從而增加儲存空間。請注意，SET STORAGE 本身並不會改變資料表中的任何內容，它只是設定在將來的資料表更新期間追求的策略。有關更多訊息，請參閱[第 66.2 節](../../internals/database-physical-storage/toast.md)。

`ADD` _`table_constraint`_ \[ NOT VALID \]

此語法用於與 [CREATE TABLE](create-table.md) 相同的語法為資料表加上一個新的限制條件，並可以加上選項 NOT VALID，該選項目前只允許用於外部鍵和 CHECK 限制條件。如果限制條件被標記為 NOT VALID，則跳過用於驗證資料表中的所有資料列滿足限制條件的冗長初始檢查。對於後續的插入或更新，這個檢查仍然會被執行（也就是說，除非在被引用的資料表中存在有匹配的資料，否則在外部鍵的情況下它們將會失敗；並且除非新的資料列匹配指定的檢查，否則它們將會失敗）。但是，資料庫不會假定該限制條件適用於資料表中的所有的資料，直到透過使用 VALIDATE CONSTRAINT 選項進行驗證。

`ADD` _`table_constraint_using_index`_

此語法根據現有的唯一索引向資料表中增加新的 PRIMARY KEY 或 UNIQUE 限制條件。索引中的所有欄位都將包含在限制條件裡。

索引不能有表示式欄位，也不能是部分索引。此外，它必須是具有隱含排序順序的 b-tree 索引。這些限制可確保索引等同於由常態的 ADD PRIMARY KEY 或 ADD UNIQUE 指令建立的索引。

如果指定了 PRIMARY KEY，並且索引的欄位尚未標記為 NOT NULL，那麼此命令將嘗試對每個此類的欄位執行 ALTER COLUMN SET NOT NULL。這需要全資料表掃描來驗證列不包含空值。在所有其他情況下，這是一項快速的操作。

如果提供限制條件名稱，那麼索引將被重新命名以匹配限制條件名稱。否則，限制條件將被命名為與索引相同。

執行此命令後，索引由該限制條件「擁有」，就像索引由一般的 ADD PRIMARY KEY 或 ADD UNIQUE 命令建立的一樣。特別要注意是，刪除限制條件會使索引消失。

#### 注意

在需要增加新的限制條件情況下，使用現有索引加上約束可能會很有幫助。這種情況下需要加上新限制條件需要很長一段時間但不會阻斷資料表更新。為此，請使用 CREATE INDEX CONCURRENTLY 建立索引，然後使用此語法將其作為官方限制條件進行安裝。請參閱後續的例子。

`ALTER CONSTRAINT`

在資料表變更先前建立限制條件屬性。目前只有外部鍵限制條件可以變更。

`VALIDATE CONSTRAINT`

此語法透過掃描資料表來驗證先前設定為 NOT VALID 的外部鍵或檢查限制條件，以確保沒有不滿足限制條件的資料列。如果限制條件已被標記為有效，則不會產生任何行為。

驗證對於大型資料表可能是一個漫長的過程。將驗證與初始設定分離的價值在於，您可以將驗證延遲到不太繁忙的時間處理，或者可以用來給額外的時間來糾正原先存在的錯誤，同時防止出現新的錯誤。另請注意，驗證本身並不妨礙它在執行時對該資料表的正常寫入命令。

驗證僅獲取變更資料表上的 SHARE UPDATE EXCLUSIVE 鎖定。 如果限制條件是外部鍵，那麼在限制條件引用的資料表上也需要 ROW SHARE 鎖定。

`DROP CONSTRAINT [ IF EXISTS ]`

這個語法會在資料表上刪除指定的限制條件。如果指定了 IF EXISTS 並且該限制條件不存在，就不會引發錯誤。在這種情況下，會發布提示通知。

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] TRIGGER`

這個語法設定這個資料表的觸發器。被禁用的觸發器仍然是系統已知的，只是在發生觸發事件時不會執行而已。對於延遲觸發器，當事件發生時檢查啟用狀態，而不是在實際執行觸發器函數時檢查。可以禁用或啟用由名稱指定的單個觸發器或資料表中的所有觸發器，或者僅禁用使用者的觸發器（此選項不包括內部生成的限制條件觸發器，例如用於實作外部鍵約束或可延遲唯一性和排除限制條件的觸發器）。禁用或啟用內部生成的限制條件觸發器需要超級使用者權限；應該謹慎對待，因為如果不執行觸發器，限制條件的完整性將無法得到保證。觸發器的觸發機制也會受設定變數 [session\_replication\_role](../../server-administration/server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#session_replication_role-enum) 的影響。當複製角色是「origin」（預設）或「local」時，只需啟用觸發器就會觸發。配置為 ENABLE REPLICA 的觸發器只會在連線處於「replica」模式時觸發，而設定為 ENABLE ALWAYS 的觸發器將觸發，不論目前的複複模式為何。

此指令會取得一個 SHARE ROW EXCLUSIVE 鎖定。

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] RULE`

這個語法設定屬於資料表的覆寫規則的觸發。禁用的規則仍為系統所知的，但在查詢覆寫期間不適用。其語法義意和禁用/啟用觸發器一樣。對於 ON SELECT 規則，將忽略此設定，即使目前連線處於非預設的複製角色，也始終使用此設定以保持 view 能正常工作。

`DISABLE`/`ENABLE ROW LEVEL SECURITY`

這個語法為資料表控制屬於資料表的資料列級安全原則的適用。 如果啟用且該資料表不存在任何安全原則，則應用預設為拒絕原則。請注意，即使資料列級安全性被禁用，安全原則也可以存在於資料表中 - 在這種情況下，原則將不會被採用，它們將被忽略。 另請參閱 [CREATE POLICY](create-policy.md)。

`NO FORCE`/`FORCE ROW LEVEL SECURITY`

當使用者為資料表的所有者時，這個語法控制屬於資料表的資料列安全原則的使用。如果啟用，則在使用者是資料表所有者時應用資料列級安全原則。 如果禁用（預設），那麼當使用者是資料表所有者時，資料列級安全性將不會被應用。另請參閱 [CREATE POLICY](create-policy.md)。

`CLUSTER ON`

此資料表為將來的 [CLUSTER](cluster.md) 操作選擇預設索引。但它實際上並不會重組資料表。

變更叢集選項將取得 SHARE UPDATE EXCLUSIVE 鎖定。

`SET WITHOUT CLUSTER`

此語法從資料表中刪除最近使用的 CLUSTER 索引設定。這會影響未指定索引的後續叢集操作。

 變更叢集選項將取得 SHARE UPDATE EXCLUSIVE 鎖定。

`SET WITH OIDS`

此語法在資料表中增加了一個 oid 系統欄位（參閱[第 5.4 節](../../the-sql-language/ddl/5.4.-xi-tong-lan-wei.md)）。 如果資料表已經有 OID，那就什麼都不做。

請注意，這不等同於 ADD COLUMN oid oid；那只會增加一個正常的欄位，而它碰巧被命名為 oid，而不是系統欄位。

`SET WITHOUT OIDS`

此語法從資料表中移除 oid 系統欄位。這完全等同於 DROP COLUMN oid RESTRICT，只是如果已經沒有 oid 欄位，它不會有動作產生。

`SET TABLESPACE`

此語法將資料表的資料表空間更改為指定的資料表空間，並將與資料表關聯的資料檔案移動到新的資料表空間。資料表中的索引（如果有的話）不會移動；但它們可以通過額外的 SET TABLESPACE 指令單獨移動。資料表空間中目前資料庫中的所有資料表都可以通過使用 ALL IN TABLESPACE 語法來移動，它將鎖定所有要移動的資料表，然後移動每個資料表。這種語法也支持 OWNED BY，它只會移動指定角色擁有的資料表。 如果指定了 NOWAIT 選項，那麼如果無法立即取得所有需要的鎖定，該指令將失敗。請注意，如果需要，系統目錄不會被此指令移動，而是使用 ALTER DATABASE 或 ALTER TABLE 呼叫。information\_schema 關連不被視為系統目錄的一部分，將會被移動。另請參閱 [CREATE TABLESPACE](create-tablespace.md)。

`SET { LOGGED | UNLOGGED }`

此子句會將資料表從無日誌資料表變更為有日誌資料表或反之亦然（請參閱 [UNLOGGED](create-table.md)）。它不能用於臨時資料表。

`SET (` _`storage_parameter`_ = _`value`_ \[, ... \] \)

此子句變更資料表的一個或多個儲存參數。有關可用參數的詳細訊息，請參閱[儲存參數選項](create-table.md#storage-parameters)。請注意，這個指令不會立即修改資料表內容；根據參數，您可能需要重填資料表以獲得所需的效果。這可以透過 [VACUUM FULL](vacuum.md)、[CLUSTER](cluster.md)或強制重填資料表的 ALTER TABLE 形式來完成。對於與規劃器相關的參數，更改將在下次資料表鎖定時生效，因此目前執行的查詢不會受到影響。

SHARE UPDATE EXCLUSIVE 會針對 fillfactor 和 autovacuum 儲存參數以及以下計劃程序的相關參數進行鎖定：effective\_io\_concurrency，parallel\_workers，seq\_page\_cost，random\_page\_cost，n\_distinct 和 n\_distinct\_inherited。

#### 注意

雖然 CREATE TABLE 允許在 WITH（storage\_parameter）語法中指定 OIDS，但 ALTER TABLE 不會將 OIDS 視為儲存參數。而是使用 SET WITH OIDS 和 SET WITHOUT OIDS 語法來變更 OID 狀態。

`RESET (` _`storage_parameter`_ \[, ... \] \)

此語法將一個或多個儲存參數重置為其預設值。 和 SET 一樣，可能需要重新寫入資料來完成更新其效果。

`INHERIT` _`parent_table`_

此子句將目標資料表加到指定的父資料表中成為新的子資料表。然後，針對父資料表的查詢將會包含目標資料表的資料。要作為子資料表加入前，目標資料表必須已經包含與父資料表的所有欄位（它也可以具有其他欄位）。這些欄位必須具有可匹配的資料型別，並且如果它們在父資料表中具有 NOT NULL 限制條件，那麼它們還必須在子資料表中也具有 NOT NULL 限制條件。

對於父資料表的所有 CHECK 限制條件，必須還有相對應的子資料表限制條件，除非父資料表中標記為不可繼承（即使用ALTER TABLE ... ADD CONSTRAINT ... NO INHERIT 所建立的，它們將會被忽略；所有匹配的子資料表限制條件不得標記為不可繼承。目前不用考慮 UNIQUE，PRIMARY KEY 和 FOREIGN KEY，但未來這些可能會改變。

`NO INHERIT` _`parent_table`_

此字句從指定的父資料表的子資料表中刪除目標資料表。針對父資料表的查詢將不再包含從目標資料表中所産生的記錄。

`OF` _`type_name`_

此子句將資料表連接到複合型別，就像 CREATE TABLE OF 已經産生它一樣。該資料表的欄位名稱和型別必須與組合型別的列表完全吻合；oid 系統欄位的存在會有所不同。該資料表不得從任何其他的資料表繼承。這些限制確保了 CREATE TABLE OF 將得到一個等效的資料表定義。

`NOT OF`

此子句將複合型別資料表從它的型別中分離出來。

`OWNER`

該子句將資料表、序列、檢視表、具體化檢視表或外部資料表的擁有者變更為指定的使用者。

`REPLICA IDENTITY`

此子句變更寫入 WAL 的訊息，以識別更新或刪除的資料列。如果正在使用邏輯複製的話，則此子句不起作用。DEFAULT（非系統資料表的預設值）記錄主鍵欄位的舊值（如果有的話）。USING INDEX 記錄指定索引覆蓋欄位的舊值，它必須是唯一的，不能是部分的，也不可是延遲的，並且只能包含標記為 NOT NULL 的欄位。FULL 記錄行中所有欄位的舊值。 沒有記錄關於舊資料列的訊息。（這是系統資料表的預設值。）在任何情況下，都不記錄舊值，除非至少有一個將記錄的欄位在新舊版本的資料列之間不同。

`RENAME`

給資料表一個新的名稱。RENAME 子句變更資料表的名稱（或索引、序列、檢視表、具體化檢視表或外部資料表）、資料表中各別的欄位名稱、及資料表的限制條件名稱。對於儲存的資料沒有任何影響。

`SET SCHEMA`

此子句將資料表移動到另一個綱要之中。資料表的關聯索引、約束和序列也將被移動。

`ATTACH PARTITION` _`partition_name`_ FOR VALUES _`partition_bound_spec`_

此子句使用與 [CREATE TABLE](create-table.md) 相同的 partition\_bound\_spec 語法，將現有資料表（可能本身已為分區割資料表）作為目標資料表的分割區。 分割區綁定規範必須對應於目標資料表的分割區限制條件和分割區主鍵。要附加的資料表必須與目標資料表具有相同的欄位，並且不得再更多；此外，欄位型別也必須匹配。而且，它必須具有目標資料表的所有 NOT NULL 和 CHECK 限制條件。目前暫不考慮UNIQUE，PRIMARY KEY 和 FOREIGN KEY 限制條件。如果附加資料表中的任何 CHECK 限制條件被標記為 NO INHERIT，則此指令將會失敗；這種限制條件必須在沒有 NO INHERIT 子句的情況下重新建立。

如果新的分割區是一般資料表，則執行全資料表掃描以檢查資料表中的現有資料列是否違反分割區的限制條件。透過在資料表中加入一個有效的 CHECK 限制條件來避免這種掃描，在執行此命令之前，只允許滿足所需分割區限制條件的資料列。資料庫將使用這樣的限制條件來確定，即不需要掃描資料表來驗證分割區的合法性。但是，如果任何分割區鍵是表示式並且分割區不接受 NULL 值，則這個語法不起作用。 如果附加一個不接受 NULL 值的列表分割區，除非它是一個表示式，否則請將 NOT NULL 限制條件加到到分割區鍵欄位。

如果新的分割區是外部資料表，則不會執行任何操作來驗證外部資料表中的所有資料都遵守分割區限制條件。（請參閱 [CREATE FOREIGN TABLE](create-foreign-table.md) 中有關外部資料表上限制條件的說明。）

`DETACH PARTITION` _`partition_name`_

此子句會分離目標資料表的指定分割區。 分離的分割區作為獨立資料表繼續存在，只是不再與原來的資料表相關聯。

除了 RENAME，SET SCHEMA，ATTACH PARTITION 和 DETACH PARTITION 之外，所有在單個資料表上作用的 ALTER TABLE 子句可以組合成一個或多個變更的列表一起使用。例如，可以在單個命令中加入多個欄位（及/或）變更多個欄位的型別。這對於大型資料表尤其有用，因為只需要在資料表上進行一次操作。

您必須擁有該資料表才能使用 ALTER TABLE。要變更資料表的綱要或資料表空間，還必須對新的綱要或資料表空間具有 CREATE 權限。要將資料表加上為父資料表的新子資料表，您也必須擁有父資料表。另外，要將資料表附加為另一個資料表的新分割區，您必須擁有附加的資料表。要變更擁有者，您還必須是新擁有角色的直接或間接成員，並且該角色必須對資料表具有 CREATE 權限。（這些限制強制改變擁有者不會做任何刪除和重新建立資料表的操作，但超級用戶可以改變任何資料表的所有權。）要加入欄位或更改欄位型別或使用 OF 子句中，您還必須具有資料型別的 USAGE 權限。

### 參數

`IF EXISTS`

如果資料表不存在，請不要拋出錯誤。在這種情況下發布 NOTICE。

_`name`_

要變更的現有資料表名稱（可以加上綱要指定）。如果在資料表名稱之前指定了 ONLY，則只變更改該資料表。如果沒有指定 ONLY，則資料表及其所有繼承的資料表（如果有的話）都進行變更。或者，可以在資料表名稱之後指定 \* 以明確指示包含繼承資料表。

_`column_name`_

新的欄位或現有欄位的名稱。

_`new_column_name`_

現有欄位的新名稱。

_`new_name`_

資料表的新名稱。

_`data_type`_

新欄位的資料型別或現有欄位的新資料型別。

_`table_constraint`_

資料表新的限制條件。

_`constraint_name`_

新的或現有限制條件的名稱。

`CASCADE`

自動刪除相依於刪除欄位或限制條件的物件（例如，引用欄位的檢視表），並依次刪除相依於這些物件的所有物件（請參閱[第 5.13 節](../../the-sql-language/ddl/dependency-tracking.md)）。

`RESTRICT`

如果有任何相依物件，則拒絕刪除欄位或限制條件。這是預設的行為。

_`trigger_name`_

要停用或啟用事件觸發器的名稱。

`ALL`

停用或啟用屬於資料表的所有觸發器。（如果觸發器是內部生成的限制條件觸發器，例如那些用於實現外部鍵限制條件或可延遲的唯一性和排除性限制條件的觸發器，則調整它們需要超級使用者權限。）

`USER`

除內部産生的限制條件觸發器（例如那些用於實現外部鍵限制條件或可延遲唯一性和排除性限制條件的觸發器）之外，停用或啟用屬於資料表的所有觸發器。

_`index_name`_

現有索引的名稱。

_`storage_parameter`_

資料表儲存參數的名稱。

_`value`_

資料表儲存參數的新值。這可能是一個數字或一個字串，具體形式取決於參數為何。

_`parent_table`_

與此資料表關聯或取消關聯的父資料表。

_`new_owner`_

資料表的新擁有者名稱。

_`new_tablespace`_

資料表將被移動到的資料表空間名稱。

_`new_schema`_

資料表將被移動到的綱要名稱。

_`partition_name`_

要附加為新分割區或從此資料表中分離的分割區資料表名稱。

_`partition_bound_spec`_

新分割區的分割區綁定規範。關於語法的更多細節請參考 [CREATE TABLE](create-table.md)。

### 注意

關鍵詞 COLUMN 是可以省略的。

當使用 ADD COLUMN 增加欄時，資料表中的所有現有的資料列都將使用該欄位的預設值進行初始化（如果未指定 DEFAULT 子句，則為 NULL）。如果沒有 DEFAULT 子句的話，這只是一個結構的變更，而不需要立即更新資料表的資料，只是在讀出時加上 NULL 值。

使用 DEFAULT 子句增加欄位或變更現有欄位的型別會需要重寫整個資料表及其索引。變更現有欄位型別時的例外情況，如果 USING 子句不變更欄位內容，並且舊型別可以是新型別的二進制強製或新類型的不受限制的 domain，則不需要重寫資料表；但受影響欄位上的任何索引仍必須重建。增加或刪除系統 oid 欄位也需要重寫整個資料表。資料表和索引重建對於大型資料表來說，可能需要大量時間，並且暫時需要可能多達兩倍的磁碟空間。

增加 CHECK 或 NOT NULL 限制條件需要掃描資料表以驗證現有的資料列是否滿足限制條件，但不需要重寫資料表。

同樣，在附加新分割區時，可能會掃描它們以驗證現有資料是否符合分割區的限制條件。

提供在單個 ALTER TABLE 中指定多個變更選項的主要原因是多個資料表掃描或重寫可以因此在資料表中組合成單次作業。

DROP COLUMN 資料表不會在實體上刪除欄位，而只是使其對 SQL 操作設為不可見。資料表中的後續插入和更新操作將該欄位儲存為空值。因此，刪除欄位很快，但不會立即減少資料表的磁碟大小，因為所刪除的欄位所佔用的空間並不會被回收。隨著現有資料的更新，空間將隨著時間的推移而被回收。（這些語句在刪除系統 oid 欄位時不適用，這是透過立即重寫完成的。）

要強制立即回收被刪除的欄位所佔用的空間，可以執行 ALTER TABLE 的一種語法來執行整個資料表的重寫。這會導致重建每個資料列，並將刪除的欄位替換為空值。

ALTER TABLE 的重寫語法並不是 MVCC 安全的。在資料表重寫後，如果使用在重寫發生之前的快照，該資料表對於平行事務將會顯示為空。更多細節參閱 [13.5 節](../../the-sql-language/concurrency-control/13.5.-te-bie-zhu-yi.md)。

SET DATA TYPE 的 USING 選項實際上可以指定涉及資料列舊值的任何表示式；也就是說，它可以引用其他欄位以及正在轉換的欄位。這允許使用 SET DATA TYPE 語法完成非常普遍的轉換。由於這種靈活性，USING 表示式並不適用於欄位的預設值（如果有的話）； 結果可能不是預設所需的常數表示式。這意味著，如果沒有隱含或賦值從舊型別轉換為新型別，即使提供了 USING 子句，SET DATA TYPE 也可能無法轉換預設值。在這種情況下，請使用 DROP DEFAULT 刪除預設值，執行 ALTER TYPE，然後使用 SET DEFAULT 加上合適的新預設值。類似的考量適用於涉及該欄位的索引和限制條件。

如果資料表有任何後代資料表，則不允許在父資料表中增加、重新命名或變更欄位的型別，卻不對後代資料進行相同操作。這確保了後代資料總是有與父代資料匹配的欄位。同樣，如果不在所有後代資料表中重新命名限制條件，則不能在父級資料表中重新命名該限制條件，以便限制條件在父代資料及其後代資料表之間也匹配。此外，因為從父代資料中查詢也會從其後代資料中進行查詢，所以對父代資料表的限制條件不能被標記為有效，除非它對於那些後代資料表也被標記為有效。在所有這些情況下，ALTER TABLE ONLY 將會被拒絕。

遞迴的 DROP COLUMN 操作只有在後代資料表不從其他父代繼承該欄位並且從未擁有該欄位的獨立定義的情況下才會刪除後代資料表欄位。非遞迴 DROP COLUMN（即，ALTER TABLE ONLY ... DROP COLUMN）永遠不會刪除任何後代欄位，而是將它們標記為獨立定義而非繼承。對於分割區資料表，非遞迴 DROP COLUMN 命令將會失敗，因為資料表的所有分割區必須與分割區源頭具有相同的欄位。

識別欄位（ADD GENERATED，SET 等，DROP IDENTITY）的行為以及TRIGGER，CLUSTER，OWNER 和 TABLESPACE 行為絕不會遞迴到後代資料表；也就是說，他們總是像只有被指定的那樣行事。增加限制條件僅針對未標記為 NO INHERIT 的 CHECK constraints 遞迴。

變更系統目錄資料表的任何部分都不會允許。

有關有效參數的更多描述，請參閱 [CREATE TABLE](create-table.md)。[第 5 章](../../the-sql-language/ddl/)則有關於繼承的更多訊息。

### 範例

要將一個 varchar 型別的欄位加到資料表中，請執行以下操作指令：

```text
ALTER TABLE distributors ADD COLUMN address varchar(30);
```

從資料表中刪除一個欄位：

```text
ALTER TABLE distributors DROP COLUMN address RESTRICT;
```

在一個操作指令中變更兩個現有欄位的型別：

```text
ALTER TABLE distributors
    ALTER COLUMN address TYPE varchar(80),
    ALTER COLUMN name TYPE varchar(100);
```

透過 USING 子句將包含 Unix 時間戳記的整數欄位變更為帶有時區的時間戳記：

```text
ALTER TABLE foo
    ALTER COLUMN foo_timestamp SET DATA TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second';
```

同樣，當有一個欄位沒有自動轉換為新資料型別的預設表示式時：

```text
ALTER TABLE foo
    ALTER COLUMN foo_timestamp DROP DEFAULT,
    ALTER COLUMN foo_timestamp TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second',
    ALTER COLUMN foo_timestamp SET DEFAULT now();
```

重新命名現有的欄位：

```text
ALTER TABLE distributors RENAME COLUMN address TO city;
```

重新命名現有的資料表：

```text
ALTER TABLE distributors RENAME TO suppliers;
```

重新命名現有的限制條件：

```text
ALTER TABLE distributors RENAME CONSTRAINT zipchk TO zip_check;
```

要將欄位加上 not null 的限制條件：

```text
ALTER TABLE distributors ALTER COLUMN street SET NOT NULL;
```

從欄位中刪除 not null 的限制條件：

```text
ALTER TABLE distributors ALTER COLUMN street DROP NOT NULL;
```

為資料表及其所有子資料表加上檢查的限制條件：

```text
ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5);
```

要僅將要檢查的限制條件加到資料表而不加到其子資料表：

```text
ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5) NO INHERIT;
```

（檢查用的限制條件並不會被未來的子資料表繼承。）

從資料表及其所有子資料表中移除限制條件：

```text
ALTER TABLE distributors DROP CONSTRAINT zipchk;
```

僅從一個資料表中刪除限制條件：

```text
ALTER TABLE ONLY distributors DROP CONSTRAINT zipchk;
```

（限制條件會保留在所有的子資料表中。）

將外部鍵的限制條件加到到資料表中：

```text
ALTER TABLE distributors ADD CONSTRAINT distfk FOREIGN KEY (address) REFERENCES addresses (address);
```

將外部鍵限制條件以其他工作影響最小的方式加到資料表中：

```text
ALTER TABLE distributors ADD CONSTRAINT distfk FOREIGN KEY (address) REFERENCES addresses (address) NOT VALID;
ALTER TABLE distributors VALIDATE CONSTRAINT distfk;
```

在資料表中加上（多個欄位）唯一性的限制條件：

```text
ALTER TABLE distributors ADD CONSTRAINT dist_id_zipcode_key UNIQUE (dist_id, zipcode);
```

要在資料表中加上一個自動命名的主鍵限制條件，注意的是，一個資料表只能有一個主鍵：

```text
ALTER TABLE distributors ADD PRIMARY KEY (dist_id);
```

將資料表移動到不同的資料表空間：

```text
ALTER TABLE distributors SET TABLESPACE fasttablespace;
```

將資料表移動到不同的 schema：

```text
ALTER TABLE myschema.distributors SET SCHEMA yourschema;
```

在重建索引時重新建立主鍵的限制條件，而不阻擋資料更新：

```text
CREATE UNIQUE INDEX CONCURRENTLY dist_id_temp_idx ON distributors (dist_id);
ALTER TABLE distributors DROP CONSTRAINT distributors_pkey,
    ADD CONSTRAINT distributors_pkey PRIMARY KEY USING INDEX dist_id_temp_idx;
```

將資料表分割區附加到範圍型的分割資料表中：

```text
ALTER TABLE measurement
    ATTACH PARTITION measurement_y2016m07 FOR VALUES FROM ('2016-07-01') TO ('2016-08-01');
```

將資料表分割區附加到列表型的分割資料表中：

```text
ALTER TABLE cities
    ATTACH PARTITION cities_ab FOR VALUES IN ('a', 'b');
```

從分割資料表中分離資料表分割區：

```text
ALTER TABLE measurement
    DETACH PARTITION measurement_y2015m12;
```

### 相容性

ADD（沒有 USING INDEX）、DROP \[COLUMN\]、DROP IDENTITY、RESTART、SET DEFAULT、SET DATA TYPE（沒有 USING）、SET GENERATED 和 SET sequence\_option 的語法是符合 SQL 標準的。其他語法則是 SQL 標準的 PostgreSQL 延伸語法。此外，在單個 ALTER TABLE 指令中進行多個操作的功能也是延伸語法。

ALTER TABLE DROP COLUMN 可用於刪除資料表的單一欄位，而留下一個沒有欄位的資料表。這是 SQL 的延伸，SQL 標準禁止使用無欄位的資料表。

### 參閱

[CREATE TABLE](create-table.md)

