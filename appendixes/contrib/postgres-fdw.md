<a id="POSTGRES-FDW"></a>

## F.38. postgres_fdw — 存取儲存在外部 PostgreSQL 伺服器中的資料 [#](#postgres-fdw) <a href="#postgres-fdw" id="postgres-fdw"></a>

[F.38.1. postgres_fdw 的 FDW 選項](postgres-fdw.md#POSTGRES-FDW-OPTIONS)

[F.38.2. 函式](postgres-fdw.md#POSTGRES-FDW-FUNCTIONS)

[F.38.3. 連線管理](postgres-fdw.md#POSTGRES-FDW-CONNECTION-MANAGEMENT)

[F.38.4. 交易管理](postgres-fdw.md#POSTGRES-FDW-TRANSACTION-MANAGEMENT)

[F.38.5. 遠端查詢最佳化](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION)

[F.38.6. 遠端查詢執行環境](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT)

[F.38.7. 跨版本相容性](postgres-fdw.md#POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY)

[F.38.8. 等待事件](postgres-fdw.md#POSTGRES-FDW-WAIT-EVENTS)

[F.38.9. 設定參數](postgres-fdw.md#POSTGRES-FDW-CONFIGURATION-PARAMETERS)

[F.38.10. 範例](postgres-fdw.md#POSTGRES-FDW-EXAMPLES)

[F.38.11. 作者](postgres-fdw.md#POSTGRES-FDW-AUTHOR)

<a id="id-1.11.7.48.2"></a>

`postgres_fdw` 模組提供外部資料包裝器
`postgres_fdw`，可用來存取儲存在外部 PostgreSQL 伺服器中的資料。

此模組提供的功能與較舊的 [dblink](dblink.md) 模組的功能有大幅重疊。
但 `postgres_fdw` 提供更透明且更符合標準的語法來存取遠端資料表，而且在許多情況下能提供更好的效能。

要準備使用 `postgres_fdw` 進行遠端存取：

1. 使用 [CREATE EXTENSION](../../reference/sql-commands/sql-createextension.md) 安裝 `postgres_fdw` 擴充功能。
2. 使用 [CREATE SERVER](../../reference/sql-commands/sql-createserver.md) 建立外部伺服器物件，
   用來代表你要連線的每個遠端資料庫。
   將 `user` 與
   `password` 以外的連線資訊，指定為伺服器物件的選項。
3. 使用 [CREATE USER MAPPING](../../reference/sql-commands/sql-createusermapping.md)，為你要允許存取各外部伺服器的每個資料庫使用者建立使用者對應。
   將要使用的遠端使用者名稱與密碼，指定為使用者對應的
   `user` 與 `password` 選項。
4. 使用 [CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md)
   或 [IMPORT FOREIGN SCHEMA](../../reference/sql-commands/sql-importforeignschema.md)，
   為你要存取的每個遠端資料表建立外部資料表。外部資料表的欄位必須與所參照的遠端資料表相符。不過，若你將正確的遠端名稱指定為外部資料表物件的選項，就可以使用與遠端資料表不同的資料表名稱和（或）欄位名稱。

現在你只需要從外部資料表執行 `SELECT`，就能存取儲存在其底層遠端資料表中的資料。你也可以使用 `INSERT`、`UPDATE`、
`DELETE`、`COPY` 或
`TRUNCATE` 修改遠端資料表。
（當然，你在使用者對應中指定的遠端使用者必須具有執行這些操作的權限。）

請注意，在
`SELECT`、`UPDATE`、
`DELETE` 或 `TRUNCATE` 中指定的 `ONLY` 選項，
在存取或修改遠端資料表時沒有作用。

請注意，`postgres_fdw` 目前不支援帶有 `ON CONFLICT DO
UPDATE` 子句的 `INSERT` 陳述式。不過，只要省略唯一值索引推斷規格，就支援 `ON CONFLICT DO NOTHING`
子句。
另請注意，`postgres_fdw` 支援在分割資料表上執行的 `UPDATE` 陳述式所引發的資料列移動，但目前無法處理下列情況：被選為插入所移動資料列的遠端分割區，同時也是將在同一命令中其他地方被更新的 `UPDATE`
目標分割區。

一般建議外部資料表的欄位宣告為與遠端資料表中被參照欄位完全相同的資料型別，以及（若適用）相同的定序。雖然 `postgres_fdw`
目前對於在需要時執行資料型別轉換相當寬容，但當型別或定序不相符時，由於遠端伺服器解讀查詢條件的方式與本機伺服器不同，可能會出現令人意外的語意異常。

請注意，外部資料表可以宣告為比其底層遠端資料表更少的欄位，或使用不同的欄位順序。欄位與遠端資料表的對應是依名稱，而不是依位置。

<a id="POSTGRES-FDW-OPTIONS"></a>

### F.38.1. postgres_fdw 的 FDW 選項 [#](#POSTGRES-FDW-OPTIONS)

<a id="POSTGRES-FDW-OPTIONS-CONNECTION"></a>

#### F.38.1.1. 連線選項 [#](#POSTGRES-FDW-OPTIONS-CONNECTION)

使用 `postgres_fdw` 外部資料包裝器的外部伺服器，可以具有 libpq 在連線字串中接受的相同選項（如[第 32.1.2 節](../../client-interfaces/libpq/libpq-paramkeywords.md#libpq-paramkeywords)所述），
但下列選項不允許使用或有特殊處理：

* `user`、`password` 與 `sslpassword`（請改在使用者對應中指定，或使用服務檔）
* `client_encoding`（此選項會依本機伺服器編碼自動設定）
* `application_name`——此選項可以出現在連線設定與
  [postgres_fdw.application_name](postgres-fdw.md#GUC-PGFDW-APPLICATION-NAME) *其中之一或兩者*中。
  若兩者都存在，`postgres_fdw.application_name`
  會覆寫連線設定。
  與 libpq 不同，
  `postgres_fdw` 允許
  `application_name` 包含「逸出序列」。
  詳細資訊請參閱 [postgres_fdw.application_name](postgres-fdw.md#GUC-PGFDW-APPLICATION-NAME)。
* `fallback_application_name`（一律設為
  `postgres_fdw`）
* `sslkey` 與 `sslcert`——這些選項可以出現在連線設定與使用者對應*其中之一或兩者*中。若兩者都存在，使用者對應的設定會覆寫連線設定。

只有超級使用者可以建立或修改帶有
`sslcert` 或 `sslkey` 設定的使用者對應。

非超級使用者可以使用密碼驗證或 GSSAPI 委派憑證連線到外部伺服器，因此在需要密碼驗證的情況下，請為屬於非超級使用者的使用者對應指定
`password` 選項。

超級使用者可以針對個別使用者對應設定使用者對應選項 `password_required 'false'`，以覆寫此檢查，例如：

```

ALTER USER MAPPING FOR some_non_superuser SERVER loopback_nopw
OPTIONS (ADD password_required 'false');
```

為了防止無特權的使用者利用 postgres 伺服器執行身分之 unix 使用者的驗證權利，提升為超級使用者權利，只有超級使用者可以在使用者對應上設定此選項。

必須謹慎確保這不會讓被對應的使用者能夠以超級使用者身分連線到被對應的資料庫（參見
CVE-2007-3278 與 CVE-2007-6601）。不要在 `public` 角色上設定
`password_required=false`。請記住，被對應的使用者可能可以使用 postgres 伺服器執行身分之系統使用者 unix 家目錄中的任何用戶端憑證、
`.pgpass`、
`.pg_service.conf` 等。（關於如何找到家目錄的詳細資訊，請參閱[第 32.16 節](../../client-interfaces/libpq/libpq-pgpass.md)。）他們也可以使用由 `peer`
或 `ident` 驗證等驗證模式所授與的任何信任關係。

<a id="POSTGRES-FDW-OPTIONS-OBJECT-NAME"></a>

#### F.38.1.2. 物件名稱選項 [#](#POSTGRES-FDW-OPTIONS-OBJECT-NAME)

這些選項可用來控制送往遠端 PostgreSQL 伺服器之 SQL 陳述式中所使用的名稱。當建立外部資料表時使用的名稱與底層遠端資料表的名稱不同時，就需要這些選項。

`schema_name` (`string`)
:   此選項可為外部資料表指定，提供該外部資料表在遠端伺服器上要使用的綱要名稱。若省略此選項，則使用外部資料表所屬綱要的名稱。

`table_name` (`string`)
:   此選項可為外部資料表指定，提供該外部資料表在遠端伺服器上要使用的資料表名稱。若省略此選項，則使用外部資料表的名稱。

`column_name` (`string`)
:   此選項可為外部資料表的欄位指定，提供該欄位在遠端伺服器上要使用的欄位名稱。
    若省略此選項，則使用該欄位的名稱。

<a id="POSTGRES-FDW-OPTIONS-COST-ESTIMATION"></a>

#### F.38.1.3. 成本估算選項 [#](#POSTGRES-FDW-OPTIONS-COST-ESTIMATION)

`postgres_fdw` 是透過對遠端伺服器執行查詢來取得遠端資料，因此理想上，掃描外部資料表的估計成本應該等於在遠端伺服器上執行的成本，再加上一些通訊的額外負擔。取得這種估計值最可靠的方式是詢問遠端伺服器，再加上一些額外負擔——但對於簡單的查詢，為了取得成本估計而額外執行一次遠端查詢，可能並不划算。
因此 `postgres_fdw` 提供下列選項，用來控制如何進行成本估算：

`use_remote_estimate` (`boolean`)
:   此選項可為外部資料表或外部伺服器指定，控制 `postgres_fdw` 是否發出遠端
    `EXPLAIN` 命令以取得成本估計。
    外部資料表的設定會覆寫其伺服器的任何設定，但僅限於該資料表。
    預設為 `false`。

`fdw_startup_cost` (`floating point`)
:   此選項可為外部伺服器指定，是一個浮點數值，會加到該伺服器上任何外部資料表掃描的估計啟動成本中。這代表在遠端建立連線、剖析與規劃查詢等的額外負擔。
    預設值為 `100`。

`fdw_tuple_cost` (`floating point`)
:   此選項可為外部伺服器指定，是一個浮點數值，用來作為該伺服器上外部資料表掃描每個元組的額外成本。這代表伺服器之間資料傳輸的額外負擔。你可以調高或調低此數值，以反映到遠端伺服器較高或較低的網路延遲。
    預設值為 `0.2`。

當 `use_remote_estimate` 為 true 時，
`postgres_fdw` 會從遠端伺服器取得資料列數與成本估計，然後將 `fdw_startup_cost` 與
`fdw_tuple_cost` 加到成本估計中。當
`use_remote_estimate` 為 false 時，
`postgres_fdw` 會在本機進行資料列數與成本估算，然後將 `fdw_startup_cost` 與
`fdw_tuple_cost` 加到成本估計中。除非有遠端資料表統計資訊的本機副本，否則這種本機估算不太可能非常準確。對外部資料表執行
[ANALYZE](../../reference/sql-commands/sql-analyze.md) 是更新本機統計資訊的方式；這會掃描遠端資料表，然後就如同該資料表位於本機一樣計算並儲存統計資訊。
保留本機統計資訊是減少遠端資料表每次查詢之規劃負擔的有效方式——但若遠端資料表經常更新，本機統計資訊很快就會過時。

下列選項控制這類 `ANALYZE`
操作的行為：

`analyze_sampling` (`string`)
:   此選項可為外部資料表或外部伺服器指定，決定對外部資料表執行 `ANALYZE`
    時，是在遠端對資料進行取樣，還是讀取並傳輸所有資料後在本機進行取樣。支援的值為
    `off`、`random`、
    `system`、`bernoulli`
    與 `auto`。`off` 會停用遠端取樣，因此所有資料都會傳輸到本機並在本機取樣。
    `random` 使用
    `random()` 函式選擇要傳回的資料列來進行遠端取樣，
    而 `system` 與 `bernoulli` 則依賴同名的內建
    `TABLESAMPLE` 方法。`random` 適用於所有遠端伺服器版本，
    而 `TABLESAMPLE` 自 9.5 起才支援。
    `auto`（預設值）會自動選擇建議的取樣方法；目前它表示依遠端伺服器版本選擇
    `bernoulli` 或 `random`。

<a id="POSTGRES-FDW-OPTIONS-REMOTE-EXECUTION"></a>

#### F.38.1.4. 遠端執行選項 [#](#POSTGRES-FDW-OPTIONS-REMOTE-EXECUTION)

預設情況下，只有使用內建運算子與函式的 `WHERE` 子句，才會被考慮在遠端伺服器上執行。涉及非內建函式的子句，會在擷取資料列之後於本機檢查。若這類函式在遠端伺服器上可用，而且可以信賴它們產生與本機相同的結果，那麼將這類 `WHERE` 子句送往遠端執行就可以提升效能。此行為可以使用下列選項控制：

`extensions` (`string`)
:   此選項是以逗號分隔的 PostgreSQL 擴充功能名稱清單，這些擴充功能以相容的版本同時安裝在本機與遠端伺服器上。屬於所列擴充功能且為不可變（immutable）的函式與運算子，會被視為可送往遠端伺服器執行。
    此選項只能為外部伺服器指定，不能針對個別資料表指定。

    使用 `extensions` 選項時，確保所列的擴充功能在本機與遠端伺服器上都存在且行為完全相同，*是使用者的責任*。否則，遠端查詢可能會失敗或出現非預期的行為。

`fetch_size` (`integer`)
:   此選項指定 `postgres_fdw`
    在每次擷取操作中應取得的資料列數。它可以為外部資料表或外部伺服器指定。在資料表上指定的選項會覆寫為伺服器指定的選項。
    預設為 `100`。

`batch_size` (`integer`)
:   此選項指定 `postgres_fdw`
    在每次插入操作中應插入的資料列數。它可以為外部資料表或外部伺服器指定。在資料表上指定的選項會覆寫為伺服器指定的選項。
    預設為 `1`。

    請注意，`postgres_fdw` 一次實際插入的資料列數，取決於欄位數以及所提供的
    `batch_size` 值。批次會作為單一查詢執行，而 libpq 協定（`postgres_fdw`
    用來連線到遠端伺服器的協定）將單一查詢中的參數數量限制為 65535。當欄位數 \* `batch_size`
    超過此限制時，`batch_size` 會被調整以避免錯誤。

    此選項也適用於複製資料到外部資料表的情況。此時，`postgres_fdw` 一次實際複製的資料列數，是以類似插入的方式決定，但由於
    `COPY` 命令的實作限制，最多為 1000。

<a id="POSTGRES-FDW-OPTIONS-ASYNCHRONOUS-EXECUTION"></a>

#### F.38.1.5. 非同步執行選項 [#](#POSTGRES-FDW-OPTIONS-ASYNCHRONOUS-EXECUTION)

`postgres_fdw` 支援非同步執行，也就是並行而非依序執行 `Append` 節點的多個部分，以提升效能。
此執行方式可以使用下列選項控制：

`async_capable` (`boolean`)
:   此選項控制 `postgres_fdw` 是否允許為了非同步執行而並行掃描外部資料表。
    它可以為外部資料表或外部伺服器指定。
    資料表層級的選項會覆寫伺服器層級的選項。
    預設為 `false`。

    為了確保從外部伺服器傳回的資料一致，`postgres_fdw` 對給定的外部伺服器只會開啟一個連線，並且即使涉及多個外部資料表，也會依序對該伺服器執行所有查詢，除非這些資料表適用不同的使用者對應。
    在這種情況下，停用此選項以消除非同步執行查詢相關的額外負擔，效能可能會更好。

    即使 `Append` 節點同時包含同步執行的子計畫與非同步執行的子計畫，也會套用非同步執行。
    在這種情況下，若非同步子計畫是使用
    `postgres_fdw` 處理的，那麼要等到至少一個同步子計畫傳回所有元組之後，才會傳回非同步子計畫的元組，因為該同步子計畫是在非同步子計畫等待送往外部伺服器之非同步查詢結果的期間執行的。
    此行為在未來的版本中可能會改變。

<a id="POSTGRES-FDW-OPTIONS-TRANSACTION-MANAGEMENT"></a>

#### F.38.1.6. 交易管理選項 [#](#POSTGRES-FDW-OPTIONS-TRANSACTION-MANAGEMENT)

如交易管理一節所述，在
`postgres_fdw` 中，交易是透過建立對應的遠端交易來管理，子交易則是透過建立對應的遠端子交易來管理。當目前的本機交易涉及多個遠端交易時，預設情況下，
`postgres_fdw` 會在本機交易提交或中止時，依序提交或中止這些遠端交易。
當目前的本機子交易涉及多個遠端子交易時，預設情況下，`postgres_fdw` 會在本機子交易提交或中止時，依序提交或中止這些遠端子交易。
使用下列選項可以提升效能：

`parallel_commit` (`boolean`)
:   此選項控制在本機交易提交時，`postgres_fdw` 是否平行提交在該本機交易中於某個外部伺服器上開啟的遠端交易。此設定也適用於遠端與本機子交易。此選項只能為外部伺服器指定，不能針對個別資料表指定。預設為
    `false`。

`parallel_abort` (`boolean`)
:   此選項控制在本機交易中止時，`postgres_fdw` 是否平行中止在該本機交易中於某個外部伺服器上開啟的遠端交易。此設定也適用於遠端與本機子交易。此選項只能為外部伺服器指定，不能針對個別資料表指定。預設為
    `false`。

若本機交易涉及多個啟用了這些選項的外部伺服器，則在本機交易提交或中止時，這些外部伺服器上的多個遠端交易會跨這些外部伺服器平行提交或中止。

啟用這些選項時，具有許多遠端交易的外部伺服器，在本機交易提交或中止時，效能可能會受到負面影響。

<a id="POSTGRES-FDW-OPTIONS-UPDATABILITY"></a>

#### F.38.1.7. 可更新性選項 [#](#POSTGRES-FDW-OPTIONS-UPDATABILITY)

預設情況下，所有使用 `postgres_fdw` 的外部資料表都被假定為可更新。這可以使用下列選項覆寫：

`updatable` (`boolean`)
:   此選項控制 `postgres_fdw` 是否允許使用 `INSERT`、`UPDATE` 與
    `DELETE` 命令修改外部資料表。它可以為外部資料表或外部伺服器指定。資料表層級的選項會覆寫伺服器層級的選項。
    預設為 `true`。

    當然，若遠端資料表實際上無法更新，無論如何都會發生錯誤。使用此選項主要是讓錯誤可以在本機擲出，而不必查詢遠端伺服器。不過請注意，`information_schema` 檢視表會依此選項的設定，回報
    `postgres_fdw` 外部資料表是否可更新，而不會對遠端伺服器做任何檢查。

<a id="POSTGRES-FDW-OPTIONS-TRUNCATABILITY"></a>

#### F.38.1.8. 可截斷性選項 [#](#POSTGRES-FDW-OPTIONS-TRUNCATABILITY)

預設情況下，所有使用 `postgres_fdw` 的外部資料表都被假定為可截斷。這可以使用下列選項覆寫：

`truncatable` (`boolean`)
:   此選項控制 `postgres_fdw` 是否允許使用 `TRUNCATE`
    命令截斷外部資料表。它可以為外部資料表或外部伺服器指定。
    資料表層級的選項會覆寫伺服器層級的選項。
    預設為 `true`。

    當然，若遠端資料表實際上無法截斷，無論如何都會發生錯誤。使用此選項主要是讓錯誤可以在本機擲出，而不必查詢遠端伺服器。

<a id="POSTGRES-FDW-OPTIONS-IMPORTING"></a>

#### F.38.1.9. 匯入選項 [#](#POSTGRES-FDW-OPTIONS-IMPORTING)

`postgres_fdw` 能夠使用 [IMPORT FOREIGN SCHEMA](../../reference/sql-commands/sql-importforeignschema.md) 匯入外部資料表定義。此命令會在本機伺服器上建立與遠端伺服器上現有資料表或檢視表相符的外部資料表定義。若要匯入的遠端資料表具有使用者自訂資料型別的欄位，本機伺服器必須具有同名且相容的型別。

匯入行為可以使用下列選項（在 `IMPORT FOREIGN SCHEMA` 命令中提供）自訂：

`import_collate` (`boolean`)
:   此選項控制從外部伺服器匯入的外部資料表定義中，是否包含欄位的 `COLLATE` 選項。預設為 `true`。若遠端伺服器的定序名稱集合與本機伺服器不同（若遠端伺服器在不同的作業系統上執行，很可能就是這種情況），你可能需要關閉此選項。
    不過，若你這麼做，會有非常嚴重的風險：匯入的資料表欄位之定序可能與底層資料不符，導致查詢行為異常。

    即使此參數設為 `true`，匯入定序為遠端伺服器預設值的欄位也可能有風險。
    它們會以 `COLLATE "default"` 匯入，這會選用本機伺服器的預設定序，而該定序可能不同。

`import_default` (`boolean`)
:   此選項控制從外部伺服器匯入的外部資料表定義中，是否包含欄位的 `DEFAULT` 運算式。預設為 `false`。若你啟用此選項，請留意在本機伺服器上的計算結果可能與在遠端伺服器上不同的預設值；`nextval()` 是常見的問題來源。
    若匯入的預設值運算式使用了本機不存在的函式或運算子，整個 `IMPORT` 都會失敗。

`import_generated` (`boolean`)
:   此選項控制從外部伺服器匯入的外部資料表定義中，是否包含欄位的 `GENERATED` 運算式。預設為 `true`。
    若匯入的產生運算式使用了本機不存在的函式或運算子，整個 `IMPORT` 都會失敗。

`import_not_null` (`boolean`)
:   此選項控制從外部伺服器匯入的外部資料表定義中，是否包含欄位的 `NOT NULL`
    限制條件。預設為 `true`。

請注意，`NOT NULL` 以外的限制條件絕不會從遠端資料表匯入。雖然 PostgreSQL
確實支援外部資料表上的檢查限制條件，但由於限制條件運算式在本機與遠端伺服器上的求值結果可能不同，因此並未提供自動匯入它們的機制。檢查限制條件行為上的任何這類不一致，都可能在查詢最佳化中導致難以察覺的錯誤。
因此，若你想匯入檢查限制條件，必須手動進行，而且應該仔細驗證每一個限制條件的語意。
關於外部資料表上檢查限制條件之處理方式的更多細節，請參閱 [CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md)。

屬於其他資料表之分割區的資料表或外部資料表，只有在
`LIMIT TO` 子句中明確指定時才會被匯入。否則，它們會被自動排除在 [IMPORT FOREIGN SCHEMA](../../reference/sql-commands/sql-importforeignschema.md) 之外。
由於所有資料都可以透過作為分割階層根節點的分割資料表存取，因此只匯入分割資料表，應該就能存取所有資料，而不必建立額外的物件。

<a id="POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT"></a>

#### F.38.1.10. 連線管理選項 [#](#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT)

預設情況下，`postgres_fdw`
與外部伺服器建立的所有連線，都會在本機工作階段中保持開啟以供重複使用。

<a id="POSTGRES-FDW-OPTION-KEEP-CONNECTIONS"></a>

`keep_connections` (`boolean`) [#](#POSTGRES-FDW-OPTION-KEEP-CONNECTIONS)
:   此選項控制 `postgres_fdw` 是否讓與外部伺服器的連線保持開啟，以便後續查詢可以重複使用。它只能為外部伺服器指定。
    預設為 `on`。若設為 `off`，
    與此外部伺服器的所有連線都會在每個交易結束時被捨棄。
<a id="POSTGRES-FDW-OPTION-USE-SCRAM-PASSTHROUGH"></a>

`use_scram_passthrough` (`boolean`) [#](#POSTGRES-FDW-OPTION-USE-SCRAM-PASSTHROUGH)
:   此選項控制 `postgres_fdw` 是否使用 SCRAM 傳遞（pass-through）驗證連線到外部伺服器。它可以為外部伺服器或使用者對應指定。
    使用者對應的設定會覆寫外部伺服器的設定。
    使用 SCRAM 傳遞驗證時，
    `postgres_fdw` 會使用 SCRAM 雜湊後的祕密資料，而不是明文的使用者密碼，連線到遠端伺服器。這可以避免將明文的使用者密碼儲存在 PostgreSQL 系統目錄中。

    要使用 SCRAM 傳遞驗證：

    * 遠端伺服器必須要求 `scram-sha-256`
      驗證方法；否則連線會失敗。
    * 遠端伺服器可以是任何支援 SCRAM 的 PostgreSQL 版本。只有用戶端（FDW 端）需要支援 `use_scram_passthrough`。
    * 不會使用使用者對應的密碼。
    * 執行 `postgres_fdw` 的伺服器與遠端伺服器，對於在
      `postgres_fdw` 上用來向外部伺服器進行驗證的使用者，必須具有完全相同的 SCRAM 祕密資料（加密後的密碼）（相同的 salt 與迭代次數，而不僅僅是相同的密碼）。

      因此，若要建立連到多個主機的 FDW 連線（例如用於分割的外部資料表／分片），則所有主機對於所涉及的使用者都必須具有完全相同的 SCRAM 祕密資料。
    * 在發出對外 FDW 連線的 PostgreSQL 執行個體上，目前的工作階段對其傳入的用戶端連線也必須使用 SCRAM 驗證。（因此稱為「傳遞」：進出都必須使用 SCRAM。）
      這是 SCRAM 協定的技術要求。

<a id="POSTGRES-FDW-FUNCTIONS"></a>

### F.38.2. 函式 [#](#POSTGRES-FDW-FUNCTIONS)

`postgres_fdw_get_connections( IN check_conn boolean DEFAULT false, OUT server_name text, OUT user_name text, OUT valid boolean, OUT used_in_xact boolean, OUT closed boolean, OUT remote_backend_pid int4) returns setof record`
:   此函式傳回 postgres_fdw 從本機工作階段與外部伺服器建立的所有開啟中連線的資訊。若沒有開啟中的連線，則不傳回任何紀錄。

    若 `check_conn` 設為 `true`，
    此函式會檢查每個連線的狀態，並將結果顯示在 `closed` 欄位中。
    此功能目前只在支援
    `poll` 系統呼叫之非標準 `POLLRDHUP` 擴充的系統（包括 Linux）上可用。
    這對於檢查交易中使用的所有連線是否仍然開啟很有用。若有任何連線已關閉，交易就無法成功提交，
    因此最好在偵測到已關閉的連線時就立即回復，而不是繼續執行到最後。若此函式回報有連線的
    `used_in_xact` 與 `closed` 都是
    `true`，使用者可以立即回復交易。

    此函式的使用範例：

    ```

    postgres=# SELECT * FROM postgres_fdw_get_connections(true);
     server_name | user_name | valid | used_in_xact | closed | remote_backend_pid
    -------------+-----------+-------+--------------+-----------------------------
     loopback1   | postgres  | t     | t            | f      |            1353340
     loopback2   | public    | t     | t            | f      |            1353120
     loopback3   |           | f     | t            | f      |            1353156
    ```

    輸出欄位說明列於
    [表 F.28](postgres-fdw.md#POSTGRES-FDW-GET-CONNECTIONS-COLUMNS)。

    <a id="POSTGRES-FDW-GET-CONNECTIONS-COLUMNS"></a>

    **表 F.28. `postgres_fdw_get_connections` 輸出欄位**

    <table border="1" class="table" summary="postgres_fdw_get_connections 輸出欄位"><colgroup><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">server_name</code></td><td><code class="type">text</code></td><td>
             此連線的外部伺服器名稱。若伺服器已被刪除但連線仍保持開啟（亦即被標記為無效），此值將為 <code class="literal">NULL</code>。
            </td></tr><tr><td><code class="structfield">user_name</code></td><td><code class="type">text</code></td><td>
             對應到此連線之外部伺服器的本機使用者名稱；若使用的是 public 對應，則為 <code class="literal">public</code>。
             若使用者對應已被刪除但連線仍保持開啟（亦即被標記為無效），此值將為 <code class="literal">NULL</code>。
            </td></tr><tr><td><code class="structfield">valid</code></td><td><code class="type">boolean</code></td><td>
             若此連線無效則為 false；無效表示此連線在目前交易中被使用，但其外部伺服器或使用者對應已被變更或刪除。
             無效的連線會在交易結束時關閉。否則傳回 true。
            </td></tr><tr><td><code class="structfield">used_in_xact</code></td><td><code class="type">boolean</code></td><td>
             若此連線在目前交易中被使用則為 true。
            </td></tr><tr><td><code class="structfield">closed</code></td><td><code class="type">boolean</code></td><td>
             若此連線已關閉則為 true，否則為 false。
             <code class="literal">NULL</code> 會在 <code class="literal">check_conn</code>
             設為 <code class="literal">false</code>，或此平台上無法使用連線狀態檢查時傳回。
            </td></tr><tr><td><code class="structfield">remote_backend_pid</code></td><td><code class="type">int4</code></td><td>
             外部伺服器上處理此連線之遠端後端的程序 ID。若遠端後端已終止且連線已關閉（<code class="literal">closed</code> 設為
             <code class="literal">true</code>），此欄位仍會顯示已終止後端的程序 ID。
            </td></tr></tbody></table>

    <br>

`postgres_fdw_disconnect(server_name text) returns boolean`
:   此函式會捨棄
    `postgres_fdw` 從本機工作階段與指定名稱之外部伺服器建立的開啟中連線。請注意，使用不同的使用者對應，可能會有多個連到指定伺服器的連線。
    若這些連線在目前的本機交易中被使用，則不會中斷它們，並會回報警告訊息。
    若此函式中斷了至少一個連線，則傳回 `true`，否則傳回 `false`。
    若找不到指定名稱的外部伺服器，則會回報錯誤。
    此函式的使用範例：

    ```

    postgres=# SELECT postgres_fdw_disconnect('loopback1');
     postgres_fdw_disconnect
    -------------------------
     t
    ```

`postgres_fdw_disconnect_all() returns boolean`
:   此函式會捨棄
    `postgres_fdw` 從本機工作階段與外部伺服器建立的所有開啟中連線。若這些連線在目前的本機交易中被使用，則不會中斷它們，並會回報警告訊息。
    若此函式中斷了至少一個連線，則傳回 `true`，否則傳回 `false`。
    此函式的使用範例：

    ```

    postgres=# SELECT postgres_fdw_disconnect_all();
     postgres_fdw_disconnect_all
    -----------------------------
     t
    ```

<a id="POSTGRES-FDW-CONNECTION-MANAGEMENT"></a>

### F.38.3. 連線管理 [#](#POSTGRES-FDW-CONNECTION-MANAGEMENT)

`postgres_fdw` 會在第一個使用與某外部伺服器相關聯之外部資料表的查詢期間，建立與該外部伺服器的連線。預設情況下，此連線會被保留，並在同一工作階段的後續查詢中重複使用。
此行為可以使用外部伺服器的
`keep_connections` 選項控制。若使用多個使用者身分（使用者對應）存取外部伺服器，則會為每個使用者對應建立一個連線。

變更外部伺服器或使用者對應的定義，或將其移除時，相關聯的連線會被關閉。
但請注意，若有任何連線正在目前的本機交易中使用，它們會被保留到交易結束為止。
已關閉的連線會在之後使用外部資料表的查詢需要時重新建立。

與外部伺服器的連線一旦建立，預設會保留到本機或對應的遠端工作階段結束為止。要明確中斷連線，可以停用外部伺服器的
`keep_connections` 選項，或使用
`postgres_fdw_disconnect` 與
`postgres_fdw_disconnect_all` 函式。例如，這些方法可用來關閉不再需要的連線，從而釋放外部伺服器上的連線。

<a id="POSTGRES-FDW-TRANSACTION-MANAGEMENT"></a>

### F.38.4. 交易管理 [#](#POSTGRES-FDW-TRANSACTION-MANAGEMENT)

在參照外部伺服器上任何遠端資料表的查詢期間，若遠端伺服器上尚未開啟與目前本機交易對應的交易，
`postgres_fdw` 就會在遠端伺服器上開啟一個交易。遠端交易會在本機交易提交或中止時提交或中止。儲存點也以類似方式管理，也就是建立對應的遠端儲存點。

當本機交易的隔離等級為 `SERIALIZABLE` 時，遠端交易使用 `SERIALIZABLE`
隔離等級；否則使用 `REPEATABLE READ`
隔離等級。此選擇確保若一個查詢在遠端伺服器上執行多次資料表掃描，所有掃描都會得到快照一致的結果。其結果是，即使遠端伺服器上因其他活動而有並行的更新，單一交易內的連續查詢也會從遠端伺服器看到相同的資料。若本機交易使用 `SERIALIZABLE` 或 `REPEATABLE READ`
隔離等級，這種行為本來就在預期之中，但對於 `READ
COMMITTED` 的本機交易而言，可能會令人意外。未來的
PostgreSQL 版本可能會修改這些規則。

請注意，`postgres_fdw` 目前不支援為兩階段提交準備遠端交易。

<a id="POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION"></a>

### F.38.5. 遠端查詢最佳化 [#](#POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION)

`postgres_fdw` 會嘗試最佳化遠端查詢，以減少從外部伺服器傳輸的資料量。做法是將查詢的 `WHERE` 子句送往遠端伺服器執行，並且不擷取目前查詢不需要的資料表欄位。為了降低查詢被錯誤執行的風險，
`WHERE` 子句只有在其中使用的每個資料型別、運算子與函式都是內建的，或屬於外部伺服器 `extensions`
選項中所列的擴充功能時（各項可以分別是內建的或屬於所列擴充功能，兩者可混用），才會被送往遠端伺服器。這類子句中的運算子與函式也必須是
`IMMUTABLE`。
對於 `UPDATE` 或 `DELETE` 查詢，若查詢中沒有無法送往遠端伺服器的
`WHERE` 子句、查詢沒有本機連接、目標資料表上沒有資料列層級的本機 `BEFORE` 或
`AFTER` 觸發程序或儲存的產生欄位，而且沒有來自上層檢視表的 `CHECK OPTION` 限制條件，
`postgres_fdw` 就會嘗試將整個查詢送往遠端伺服器，以最佳化查詢的執行。在 `UPDATE` 中，
要指定給目標欄位的運算式只能使用內建資料型別、
`IMMUTABLE` 運算子或 `IMMUTABLE` 函式，
以降低查詢被錯誤執行的風險。

當 `postgres_fdw` 遇到同一外部伺服器上外部資料表之間的連接時，會將整個連接送往外部伺服器，除非它基於某種理由認為個別從每個資料表擷取資料列會更有效率，或者所涉及的資料表參照適用不同的使用者對應。送出 `JOIN`
子句時，它會採取與上述
`WHERE` 子句相同的預防措施。

實際送往遠端伺服器執行的查詢，可以使用 `EXPLAIN VERBOSE` 檢視。

<a id="POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT"></a>

### F.38.6. 遠端查詢執行環境 [#](#POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT)

在 `postgres_fdw` 開啟的遠端工作階段中，
[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 參數只設為
`pg_catalog`，因此不以綱要限定時，只有內建物件可見。這對 `postgres_fdw` 本身產生的查詢不成問題，因為它一律會提供這種限定。不過，對於透過遠端資料表上的觸發程序或規則在遠端伺服器上執行的函式，這可能會造成危險。例如，若遠端資料表實際上是一個檢視表，則該檢視表中使用的任何函式，都會以受限的搜尋路徑執行。建議在這類函式中以綱要限定所有名稱，或者為這類函式附加 `SET search_path` 選項
（請參閱 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md)），以建立其預期的搜尋路徑環境。

`postgres_fdw` 同樣會為多個參數建立遠端工作階段設定：

* [TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設為 `UTC`
* [DateStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 設為 `ISO`
* [IntervalStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-INTERVALSTYLE) 設為 `postgres`
* [extra_float_digits](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) 對 9.0 及更新版本的遠端伺服器設為 `3`，
  對較舊的版本設為 `2`

這些設定比 `search_path` 較不容易造成問題，但若有需要，可以使用函式的 `SET` 選項處理。

*不*建議你透過變更這些參數的工作階段層級設定來覆寫此行為；這很可能會導致 `postgres_fdw` 運作異常。

<a id="POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY"></a>

### F.38.7. 跨版本相容性 [#](#POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY)

`postgres_fdw` 可以搭配最早至 PostgreSQL 8.3 的遠端伺服器使用。唯讀功能則最早可支援到 8.1。

不過，有一項限制：若不可變（immutable）的內建函式與運算子出現在外部資料表的
`WHERE` 子句中，`postgres_fdw`
通常會假定可以安全地將它們送往遠端伺服器執行。因此，在遠端伺服器的版本發佈之後才新增的內建函式，可能會被送往該伺服器執行，導致「function does not exist」或類似的錯誤。這類失敗可以透過改寫查詢來因應，例如將外部資料表參照嵌入帶有 `OFFSET 0` 的子 `SELECT` 中作為最佳化屏障，並將有問題的函式或運算子放在子 `SELECT` 之外。

另一項限制是，在外部資料表上執行帶有 `ON CONFLICT DO NOTHING` 子句的 `INSERT`
陳述式時，遠端伺服器必須執行
PostgreSQL 9.5 或更新版本，因為較早的版本不支援此功能。

<a id="POSTGRES-FDW-WAIT-EVENTS"></a>

### F.38.8. 等待事件 [#](#POSTGRES-FDW-WAIT-EVENTS)

`postgres_fdw` 可以在等待事件類型 `Extension` 下回報下列等待事件：

`PostgresFdwCleanupResult`
:   等待遠端伺服器上的交易中止。

`PostgresFdwConnect`
:   等待與遠端伺服器建立連線。

`PostgresFdwGetResult`
:   等待從遠端伺服器接收查詢結果。

<a id="POSTGRES-FDW-CONFIGURATION-PARAMETERS"></a>

### F.38.9. 設定參數 [#](#POSTGRES-FDW-CONFIGURATION-PARAMETERS)

<a id="GUC-PGFDW-APPLICATION-NAME"></a>

`postgres_fdw.application_name` (`string`) <a id="id-1.11.7.48.19.2.1.1.3"></a> [#](#GUC-PGFDW-APPLICATION-NAME)
:   指定 `postgres_fdw`
    與外部伺服器建立連線時所使用的 [application_name](../../server-administration/runtime-config/runtime-config-logging.md#GUC-APPLICATION-NAME)
    設定參數值。這會覆寫伺服器物件的
    `application_name` 選項。
    請注意，變更此參數不會影響任何現有連線，直到這些連線重新建立為止。

    `postgres_fdw.application_name` 可以是任意長度的任何字串，甚至可以包含非 ASCII 字元。不過，當它被傳遞到外部伺服器並作為
    `application_name` 使用時，請注意它會被截斷為少於
    `NAMEDATALEN` 個字元。
    可列印 ASCII 字元以外的任何字元，都會被替換為 [C 語言風格的十六進位逸出序列](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE)。
    詳細資訊請參閱 [application_name](../../server-administration/runtime-config/runtime-config-logging.md#GUC-APPLICATION-NAME)。

    `%` 字元表示「逸出序列」的開始，這些序列會被替換為下文所述的狀態資訊。
    無法辨識的逸出序列會被忽略。其他字元會直接複製到應用程式名稱中。請注意，不允許在 `%`
    之後、選項之前指定正負號或數值常數，以進行對齊與填補。

    <table border="1" class="informaltable"><colgroup><col/><col/></colgroup><thead><tr><th>逸出序列</th><th>效果</th></tr></thead><tbody><tr><td><code class="literal">%a</code></td><td>本機伺服器上的應用程式名稱</td></tr><tr><td><code class="literal">%c</code></td><td>
              本機伺服器上的工作階段 ID
              （詳細資訊請參閱 <a class="xref" href="../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-LINE-PREFIX">log_line_prefix</a>）
             </td></tr><tr><td><code class="literal">%C</code></td><td>
              本機伺服器上的叢集名稱
              （詳細資訊請參閱 <a class="xref" href="../../server-administration/runtime-config/runtime-config-logging.md#GUC-CLUSTER-NAME">cluster_name</a>）
             </td></tr><tr><td><code class="literal">%u</code></td><td>本機伺服器上的使用者名稱</td></tr><tr><td><code class="literal">%d</code></td><td>本機伺服器上的資料庫名稱</td></tr><tr><td><code class="literal">%p</code></td><td>本機伺服器上後端的程序 ID</td></tr><tr><td><code class="literal">%%</code></td><td>字面的 %</td></tr></tbody></table>

    例如，假設使用者 `local_user` 從資料庫 `local_db` 以使用者 `foreign_user` 的身分建立連到
    `foreign_db` 的連線，
    則設定 `'db=%d, user=%u'` 會被替換為
    `'db=local_db, user=local_user'`。

<a id="POSTGRES-FDW-EXAMPLES"></a>

### F.38.10. 範例 [#](#POSTGRES-FDW-EXAMPLES)

以下是使用
`postgres_fdw` 建立外部資料表的範例。首先安裝擴充功能：

```

CREATE EXTENSION postgres_fdw;
```

接著使用 [CREATE SERVER](../../reference/sql-commands/sql-createserver.md) 建立外部伺服器。
在此範例中，我們希望連線到主機 `192.83.123.89` 上、在連接埠
`5432` 監聽的 PostgreSQL 伺服器。要連線的資料庫在遠端伺服器上名為 `foreign_db`：

```

CREATE SERVER foreign_server
        FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (host '192.83.123.89', port '5432', dbname 'foreign_db');
```

還需要一個以 [CREATE USER MAPPING](../../reference/sql-commands/sql-createusermapping.md) 定義的使用者對應，用來指定將在遠端伺服器上使用的角色：

```

CREATE USER MAPPING FOR local_user
        SERVER foreign_server
        OPTIONS (user 'foreign_user', password 'password');
```

現在就可以使用
[CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md) 建立外部資料表。在此範例中，我們希望存取遠端伺服器上名為 `some_schema.some_table`
的資料表。它在本機的名稱將是 `foreign_table`：

```

CREATE FOREIGN TABLE foreign_table (
        id integer NOT NULL,
        data text
)
        SERVER foreign_server
        OPTIONS (schema_name 'some_schema', table_name 'some_table');
```

在 `CREATE FOREIGN TABLE` 中宣告之欄位的資料型別與其他屬性，必須與實際的遠端資料表相符，這一點至關重要。
欄位名稱也必須相符，除非你為個別欄位附加 `column_name`
選項，指出它們在遠端資料表中的名稱。
在許多情況下，使用 [`IMPORT FOREIGN SCHEMA`](../../reference/sql-commands/sql-importforeignschema.md) 會比手動建構外部資料表定義更好。

<a id="POSTGRES-FDW-AUTHOR"></a>

### F.38.11. 作者 [#](#POSTGRES-FDW-AUTHOR)

Shigeru Hanada `<shigeru.hanada@gmail.com>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/postgres-fdw.html)（原文版本：18.6；核對日期：2026-10-22）
