<a id="SQL-CREATEINDEX"></a><a id="id-1.9.3.69.1"></a>

## CREATE INDEX

CREATE INDEX — 定義新的索引

<a id="id-1.9.3.69.4"></a>

## 語法

```

CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ] name ] ON [ ONLY ] table_name [ USING method ]
    ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
    [ INCLUDE ( column_name [, ...] ) ]
    [ NULLS [ NOT ] DISTINCT ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    [ WHERE predicate ]
```

<a id="id-1.9.3.69.5"></a>

## 說明

`CREATE INDEX` 會在指定關聯的指定欄位上建構索引，該關聯可以是資料表或具體化檢視表。索引主要用於提升資料庫效能（不過不當使用可能導致效能變慢）。

索引的鍵欄位以欄位名稱指定，或者也可以用括號括起來的運算式指定。若索引方法支援多欄位索引，就可以指定多個欄位。

索引欄位可以是由資料表資料列中一個或多個欄位的值計算而得的運算式。此功能可用於依據基本資料的某種轉換來快速存取資料。例如，以 `upper(col)` 計算的索引，可以讓子句 `WHERE upper(col) = 'JIM'` 使用索引。

PostgreSQL 提供 B-tree、hash、GiST、SP-GiST、GIN 與 BRIN 等索引方法。使用者也可以定義自己的索引方法，但那相當複雜。

當 `WHERE` 子句存在時，會建立*部分索引*。部分索引是只包含資料表中一部分資料之項目的索引，這部分通常比資料表的其餘部分更值得建立索引。例如，若你有一個資料表同時包含已開立帳單與未開立帳單的訂單，其中未開立帳單的訂單只占整個資料表的一小部分，卻是經常使用的區段，你就可以只在這部分上建立索引來提升效能。另一種可能的應用是將 `WHERE` 與 `UNIQUE` 搭配使用，以在資料表的子集合上強制唯一性。更多討論請參閱[第 11.8 節](../../the-sql-language/indexes/indexes-partial.md)。

`WHERE` 子句中使用的運算式只能參照底層資料表的欄位，但可以使用所有欄位，而不只是被索引的欄位。目前，`WHERE` 中也禁止使用子查詢與彙總運算式。同樣的限制也適用於屬於運算式的索引欄位。

索引定義中使用的所有函式與運算子都必須是「immutable」（不可變）的，也就是說，其結果必須只取決於其引數，而絕不取決於任何外部影響（例如另一個資料表的內容或目前時間）。此限制可確保索引的行為有明確定義。若要在索引運算式或 `WHERE` 子句中使用使用者定義的函式，請記得在建立該函式時將其標記為 immutable。

<a id="id-1.9.3.69.6"></a>

## 參數

`UNIQUE`
:   使系統在建立索引時（若已有資料）以及每次新增資料時，檢查資料表中是否有重複的值。嘗試插入或更新會導致重複項目的資料，將產生錯誤。

    將唯一值索引套用於分割資料表時，還有額外的限制；請參閱 [CREATE TABLE](sql-createtable.md)。

`CONCURRENTLY`
:   使用此選項時，PostgreSQL 建立索引時不會取得任何會阻止資料表上並行插入、更新或刪除的鎖定；而標準的索引建立則會鎖定資料表的寫入（但不鎖定讀取），直到完成為止。使用此選項時有幾項需要注意的事項——請參閱下方的[並行建立索引](sql-createindex.md#SQL-CREATEINDEX-CONCURRENTLY)。

    對於暫存資料表，`CREATE INDEX` 一律以非並行方式執行，因為其他工作階段都無法存取暫存資料表，而且非並行的索引建立成本較低。

`IF NOT EXISTS`
:   若已存在同名的關聯，不擲出錯誤；此情況會發出 notice。請注意，並不保證現有的索引與原本會建立的索引有任何相似之處。指定 `IF NOT EXISTS` 時，索引名稱為必要。

`INCLUDE`
:   選擇性的 `INCLUDE` 子句指定一份欄位清單，這些欄位會以*非鍵*欄位的形式包含在索引中。非鍵欄位不能用於索引掃描的搜尋條件，而且對於該索引所強制執行的任何唯一性或排除限制條件，都不會考慮非鍵欄位。不過，僅索引掃描（index-only scan）可以傳回非鍵欄位的內容，而無須造訪索引所屬的資料表，因為這些內容可直接從索引項目取得。因此，加入非鍵欄位可以讓原本無法使用僅索引掃描的查詢使用它。

    在索引中加入非鍵欄位時，最好保守一些，尤其是寬欄位。若索引 tuple 超過該索引類型允許的最大大小，資料插入將會失敗。無論如何，非鍵欄位都會複製索引所屬資料表中的資料並使索引變大，因而可能拖慢搜尋。此外，具有非鍵欄位的索引永遠不會使用 B-tree 去重複。

    列在 `INCLUDE` 子句中的欄位不需要適當的運算子類別；此子句可以包含其資料型別未針對給定存取方法定義運算子類別的欄位。

    不支援以運算式作為包含欄位，因為運算式無法用於僅索引掃描。

    目前，B-tree、GiST 與 SP-GiST 索引存取方法支援此功能。在這些索引中，列在 `INCLUDE` 子句中之欄位的值，會包含在對應於 heap tuple 的葉節點 tuple 中，但不會包含在用於樹狀導覽的上層索引項目中。

*`name`*
:   要建立之索引的名稱。此處不能包含綱要名稱；索引一律建立在與其父資料表相同的綱要中。索引的名稱必須與該綱要中任何其他關聯（資料表、序列、索引、檢視表、具體化檢視表或外部資料表）的名稱都不同。若省略名稱，PostgreSQL 會依據父資料表的名稱與被索引的欄位名稱，選擇一個合適的名稱。

`ONLY`
:   表示若資料表已分割，不要遞迴地在分割區上建立索引。預設為遞迴。

*`table_name`*
:   要建立索引之資料表的名稱（可選擇以綱要限定）。

*`method`*
:   要使用之索引方法的名稱。可選擇 `btree`、`hash`、`gist`、`spgist`、`gin`、`brin`，或使用者安裝的存取方法，例如 [bloom](../../appendixes/contrib/bloom.md)。預設方法為 `btree`。

*`column_name`*
:   資料表中某個欄位的名稱。

*`expression`*
:   以資料表中一個或多個欄位為基礎的運算式。如語法所示，運算式通常必須以括號括起來。不過，若運算式是函式呼叫的形式，則可以省略括號。

*`collation`*
:   索引要使用之定序的名稱。預設情況下，索引使用為被索引欄位宣告的定序，或被索引運算式的結果定序。使用非預設定序的索引，對於涉及使用非預設定序之運算式的查詢可能很有用。

*`opclass`*
:   運算子類別的名稱。詳情請參閱下文。

*`opclass_parameter`*
:   運算子類別參數的名稱。詳情請參閱下文。

`ASC`
:   指定遞增排序順序（此為預設值）。

`DESC`
:   指定遞減排序順序。

`NULLS FIRST`
:   指定 null 排在非 null 之前。指定 `DESC` 時，此為預設值。

`NULLS LAST`
:   指定 null 排在非 null 之後。未指定 `DESC` 時，此為預設值。

`NULLS DISTINCT`<br>`NULLS NOT DISTINCT`
:   指定對於唯一值索引，null 值是否應視為相異（不相等）。預設為相異，因此唯一值索引可以在一個欄位中包含多個 null 值。

*`storage_parameter`*
:   索引方法特有之儲存參數的名稱。詳情請參閱下方的[索引儲存參數](sql-createindex.md#SQL-CREATEINDEX-STORAGE-PARAMETERS)。

*`tablespace_name`*
:   要在其中建立索引的資料表空間。若未指定，會參考 [default_tablespace](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLESPACE)；若為暫存資料表上的索引，則參考 [temp_tablespaces](../../server-administration/runtime-config/runtime-config-client.md#GUC-TEMP-TABLESPACES)。

*`predicate`*
:   部分索引的限制條件運算式。

<a id="SQL-CREATEINDEX-STORAGE-PARAMETERS"></a>

### 索引儲存參數

選擇性的 `WITH` 子句為索引指定*儲存參數*。每種索引方法都有自己一組允許的儲存參數。

B-tree、hash、GiST 與 SP-GiST 索引方法都接受此參數：

<a id="INDEX-RELOPTION-FILLFACTOR"></a>

`fillfactor` (`integer`) <a id="id-1.9.3.69.6.3.4.1.1.3"></a> [#](#INDEX-RELOPTION-FILLFACTOR)
:   控制索引方法嘗試將索引頁面填滿的程度。對於 B-tree，在初始建立索引時，以及在索引右側延伸（加入新的最大鍵值）時，葉節點頁面會填到這個百分比。若頁面之後變得完全填滿，就會被分裂，導致磁碟上的索引結構產生碎片。B-tree 的預設 fillfactor 為 90，但可以選擇 10 到 100 之間的任何整數值。

    對於預期會有大量插入及／或更新的資料表，其上的 B-tree 索引可以受益於在 `CREATE INDEX` 時（於大量載入資料表之後）使用較低的 fillfactor 設定。50～90 範圍內的值，可以在 B-tree 索引生命週期的早期有效地「平滑」頁面分裂的*速率*（像這樣降低 fillfactor 甚至可能降低頁面分裂的絕對次數，不過此效果高度取決於工作負載）。[第 65.1.4.2 節](../../internals/indextypes/btree.md#BTREE-DELETION)所描述的 B-tree 由下而上索引刪除技術，仰賴頁面上有一些「額外」空間來儲存「額外」的 tuple 版本，因此可能受到 fillfactor 影響（不過其影響通常並不顯著）。

    在其他特定情況下，於 `CREATE INDEX` 時將 fillfactor 提高到 100，作為盡量提高空間使用率的方法，可能會有用。只有在你完全確定資料表是靜態的（亦即永遠不會受到插入或更新影響）時，才應該考慮這麼做。否則，fillfactor 設定為 100 有*損害*效能的風險：即使只有少量的更新或插入，也會引發突如其來的大量頁面分裂。

    其他索引方法以不同但大致類似的方式使用 fillfactor；預設 fillfactor 因方法而異。

B-tree 索引另外接受此參數：

<a id="INDEX-RELOPTION-DEDUPLICATE-ITEMS"></a>

`deduplicate_items` (`boolean`) <a id="id-1.9.3.69.6.3.6.1.1.3"></a> [#](#INDEX-RELOPTION-DEDUPLICATE-ITEMS)
:   控制是否使用[第 65.1.4.3 節](../../internals/indextypes/btree.md#BTREE-DEDUPLICATION)所描述的 B-tree 去重複技術。設為 `ON` 或 `OFF` 以啟用或停用此最佳化。（如[第 19.1 節](../../server-administration/runtime-config/config-setting.md)所述，`ON` 與 `OFF` 也允許使用其他寫法。）預設為 `ON`。

    <a id="id-1.9.3.69.6.3.6.1.2.2"></a>

    ### 注意

    透過 `ALTER INDEX` 關閉 `deduplicate_items`，可以防止未來的插入觸發去重複，但其本身並不會讓現有的 posting list tuple 改用標準的 tuple 表示法。

GiST 索引另外接受此參數：

<a id="INDEX-RELOPTION-BUFFERING"></a>

`buffering` (`enum`) <a id="id-1.9.3.69.6.3.8.1.1.3"></a> [#](#INDEX-RELOPTION-BUFFERING)
:   控制是否使用[第 65.2.4.1 節](../../internals/indextypes/gist.md#GIST-BUFFERING-BUILD)所描述的緩衝建立技術來建立索引。設為 `OFF` 時停用緩衝，設為 `ON` 時啟用，設為 `AUTO` 時一開始停用，但一旦索引大小達到 [effective_cache_size](../../server-administration/runtime-config/runtime-config-query.md#GUC-EFFECTIVE-CACHE-SIZE)，就會即時開啟。預設為 `AUTO`。請注意，若可以使用排序建立，除非指定了 `buffering=ON`，否則會改用排序建立，而不使用緩衝建立。

GIN 索引接受這些參數：

<a id="INDEX-RELOPTION-FASTUPDATE"></a>

`fastupdate` (`boolean`) <a id="id-1.9.3.69.6.3.10.1.1.3"></a> [#](#INDEX-RELOPTION-FASTUPDATE)
:   控制是否使用[第 65.4.4.1 節](../../internals/indextypes/gin.md#GIN-FAST-UPDATE)所描述的快速更新技術。`ON` 啟用快速更新，`OFF` 則停用。預設為 `ON`。

    <a id="id-1.9.3.69.6.3.10.1.2.2"></a>

    ### 注意

    透過 `ALTER INDEX` 關閉 `fastupdate`，可以防止未來的插入進入待處理索引項目清單，但其本身並不會清除現有的項目。之後你可能會想對該資料表執行 `VACUUM`，或呼叫 `gin_clean_pending_list` 函式，以確保待處理清單被清空。

<a id="INDEX-RELOPTION-GIN-PENDING-LIST-LIMIT"></a>

`gin_pending_list_limit` (`integer`) <a id="id-1.9.3.69.6.3.11.1.1.3"></a> [#](#INDEX-RELOPTION-GIN-PENDING-LIST-LIMIT)
:   為此索引覆寫 [gin_pending_list_limit](../../server-administration/runtime-config/runtime-config-client.md#GUC-GIN-PENDING-LIST-LIMIT) 的全域設定。此值以千位元組（kilobyte）為單位指定。

BRIN 索引接受這些參數：

<a id="INDEX-RELOPTION-PAGES-PER-RANGE"></a>

`pages_per_range` (`integer`) <a id="id-1.9.3.69.6.3.13.1.1.3"></a> [#](#INDEX-RELOPTION-PAGES-PER-RANGE)
:   定義構成 BRIN 索引每個項目之一個區塊範圍的資料表區塊數量（詳情請參閱[第 65.5.1 節](../../internals/indextypes/brin.md#BRIN-INTRO)）。預設為 `128`。
<a id="INDEX-RELOPTION-AUTOSUMMARIZE"></a>

`autosummarize` (`boolean`) <a id="id-1.9.3.69.6.3.13.2.1.3"></a> [#](#INDEX-RELOPTION-AUTOSUMMARIZE)
:   定義每當在下一個頁面範圍偵測到插入時，是否要為前一個頁面範圍排入一次摘要執行（詳情請參閱[第 65.5.1.1 節](../../internals/indextypes/brin.md#BRIN-OPERATION)）。預設為 `off`。

<a id="SQL-CREATEINDEX-CONCURRENTLY"></a>

### 並行建立索引

<a id="id-1.9.3.69.6.4.2"></a>

建立索引可能會干擾資料庫的正常運作。一般而言，PostgreSQL 會鎖定要建立索引的資料表以阻擋寫入，並以單次掃描資料表來完成整個索引建立。其他交易仍可讀取該資料表，但若它們嘗試在該資料表中插入、更新或刪除資料列，就會被阻擋，直到索引建立完成為止。若系統是正在運作的正式環境資料庫，這可能造成嚴重影響。非常大的資料表可能需要好幾個小時才能建立索引；即使是較小的資料表，索引建立也可能將寫入者鎖在外面，時間長到正式環境系統無法接受。

PostgreSQL 支援在不鎖定寫入的情況下建立索引。此方法透過指定 `CREATE INDEX` 的 `CONCURRENTLY` 選項來啟用。使用此選項時，PostgreSQL 必須對資料表執行兩次掃描，此外還必須等待所有可能修改或使用該索引的現有交易結束。因此，此方法所需的總工作量比標準索引建立更多，完成所需的時間也明顯更長。不過，由於它允許在建立索引期間繼續進行正常操作，此方法適合用於在正式環境中加入新的索引。當然，建立索引所帶來的額外 CPU 與 I/O 負載，可能會拖慢其他操作。

在並行索引建立中，索引實際上會先在一個交易中，以「無效」索引的形式登錄到系統目錄，接著在另外兩個交易中進行兩次資料表掃描。每次資料表掃描之前，索引建立都必須等待已修改該資料表的現有交易結束。第二次掃描之後，索引建立必須等待任何持有早於第二次掃描之快照（請參閱[第 13 章](../../the-sql-language/mvcc/README.md)）的交易結束；若所涉及的索引是部分索引，或具有不是單純欄位參照的欄位，這也包括其他資料表上任何階段的並行索引建立所使用的交易。最後，索引才能被標記為「有效」並可供使用，`CREATE INDEX` 命令也隨之結束。不過即使如此，該索引可能仍無法立即用於查詢：在最壞的情況下，只要還存在早於索引建立開始的交易，該索引就無法使用。

若在掃描資料表時發生問題，例如死結或唯一值索引中的唯一性違反，`CREATE INDEX` 命令會失敗，但會留下一個「無效」索引。由於這個索引可能不完整，查詢時會忽略它；然而它仍會帶來更新的額外負擔。psql 的 `\d` 命令會將這類索引回報為 `INVALID`：

```

postgres=# \d tab
       Table "public.tab"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 col    | integer |           |          |
Indexes:
    "idx" btree (col) INVALID
```

在這種情況下，建議的復原方法是移除該索引，然後再次嘗試執行 `CREATE INDEX CONCURRENTLY`。（另一種可能是以 `REINDEX INDEX CONCURRENTLY` 重建該索引。）

並行建立唯一值索引時的另一項注意事項是：從第二次資料表掃描開始時，唯一性限制條件就已經對其他交易強制執行。這表示在索引可供使用之前，甚至在索引建立最終失敗的情況下，其他查詢中都可能回報限制條件違反。此外，若第二次掃描確實發生失敗，該「無效」索引之後仍會繼續強制執行其唯一性限制條件。

支援並行建立運算式索引與部分索引。計算這些運算式時發生的錯誤，可能造成與上述唯一性限制條件違反類似的行為。

一般的索引建立允許同一資料表上的其他一般索引建立同時進行，但一個資料表一次只能進行一個並行索引建立。無論哪種情況，建立索引期間都不允許修改該資料表的結構定義。另一個差異是，一般的 `CREATE INDEX` 命令可以在交易區塊內執行，但 `CREATE INDEX CONCURRENTLY` 不行。

目前不支援在分割資料表上並行建立索引。不過，你可以先在每個分割區上個別並行建立索引，最後再以非並行方式建立分割索引，以縮短分割資料表的寫入被鎖定的時間。在這種情況下，建立分割索引只是一項僅涉及詮釋資料的操作。

<a id="id-1.9.3.69.7"></a>

## 注意事項

關於何時可以使用索引、何時不會使用索引，以及在哪些特定情況下索引會有用，請參閱[第 11 章](../../the-sql-language/indexes/README.md)。

目前只有 B-tree、GiST、GIN 與 BRIN 索引方法支援多鍵欄位索引。是否可以有多個鍵欄位，與是否可以在索引中加入 `INCLUDE` 欄位無關。索引最多可以有 32 個欄位，包含 `INCLUDE` 欄位在內。（此上限可以在建置 PostgreSQL 時變更。）目前只有 B-tree 支援唯一值索引。

可以為索引的每個欄位指定一個*運算子類別*，並可附帶選擇性的參數。運算子類別識別索引對該欄位要使用的運算子。例如，四位元組整數上的 B-tree 索引會使用 `int4_ops` 類別；此運算子類別包含四位元組整數的比較函式。實務上，欄位資料型別的預設運算子類別通常就已足夠。之所以要有運算子類別，主要是因為某些資料型別可能有超過一種有意義的排序方式。例如，我們可能想依絕對值或依實部來排序複數資料型別。我們可以為該資料型別定義兩個運算子類別，然後在建立索引時選擇適當的類別。關於運算子類別的更多資訊，請參閱[第 11.10 節](../../the-sql-language/indexes/indexes-opclass.md)與[第 36.16 節](../../server-programming/extend/xindex.md)。

在分割資料表上呼叫 `CREATE INDEX` 時，預設行為是遞迴到所有分割區，以確保它們都有相符的索引。系統會先檢查每個分割區是否已存在等效的索引；若存在，該索引會以分割區索引的身分附加到正在建立的索引上，而正在建立的索引則成為它的父索引。若不存在相符的索引，則會建立一個新索引並自動附加；每個分割區中新索引的名稱，會以彷彿命令中未指定索引名稱的方式決定。若指定了 `ONLY` 選項，則不會進行遞迴，且該索引會被標記為無效。（一旦所有分割區都取得相符的索引，`ALTER INDEX ... ATTACH PARTITION` 會將該索引標記為有效。）不過請注意，未來使用 `CREATE TABLE ... PARTITION OF` 建立的任何分割區，無論是否指定了 `ONLY`，都會自動擁有相符的索引。

對於支援有序掃描的索引方法（目前只有 B-tree），可以指定選擇性子句 `ASC`、`DESC`、`NULLS FIRST` 及／或 `NULLS LAST` 來修改索引的排序順序。由於有序索引可以向前或向後掃描，建立單一欄位的 `DESC` 索引通常沒有用處——該排序順序用一般索引就已經能取得。這些選項的價值在於，可以建立與混合排序查詢所要求之排序順序相符的多欄位索引，例如 `SELECT ... ORDER BY x ASC, y DESC`。若你需要在依賴索引來避免排序步驟的查詢中，支援「null 排在低處」的行為，而非預設的「null 排在高處」，`NULLS` 選項就很有用。

系統會定期收集資料表所有欄位的統計資訊。新建立的非運算式索引可以立即使用這些統計資訊來判斷索引的效用。對於新的運算式索引，必須執行 [`ANALYZE`](sql-analyze.md) 或等待 [autovacuum 常駐程式](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)分析該資料表，才能為這些索引產生統計資訊。

`CREATE INDEX` 執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog, pg_temp`。

對於大多數索引方法，建立索引的速度取決於 [maintenance_work_mem](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) 的設定。較大的值會縮短建立索引所需的時間，只要你沒有將它設得比實際可用的記憶體還大；否則會迫使機器進行置換（swapping）。

PostgreSQL 可以在建立索引時利用多個 CPU，以更快處理資料表的資料列。此功能稱為*平行索引建立*。對於支援平行建立索引的索引方法（目前為 B-tree、GIN 與 BRIN），`maintenance_work_mem` 指定的是每個索引建立操作整體可使用的最大記憶體量，不論啟動了多少個工作程序。一般而言，會由成本模型自動決定應該請求多少個工作程序（若需要的話）。

增加 `maintenance_work_mem` 可能使平行索引建立受益，而等效的循序索引建立卻幾乎或完全不會受益。請注意，`maintenance_work_mem` 可能會影響所請求的工作程序數量，因為平行工作程序必須在 `maintenance_work_mem` 總預算中至少分得 `32MB` 的份額。此外還必須為領導程序保留剩餘的 `32MB` 份額。增加 [max_parallel_maintenance_workers](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS) 可能允許使用更多工作程序，進而縮短建立索引所需的時間，前提是索引建立尚未受限於 I/O。當然，也應該有足夠的、原本會閒置的 CPU 容量。

透過 [`ALTER TABLE`](sql-altertable.md) 為 `parallel_workers` 設定值，可以直接控制針對該資料表的 `CREATE INDEX` 會請求多少個平行工作程序。這會完全略過成本模型，並使 `maintenance_work_mem` 不會影響所請求的平行工作程序數量。透過 `ALTER TABLE` 將 `parallel_workers` 設為 0，則在所有情況下都會停用該資料表上的平行索引建立。

<a id="id-1.9.3.69.7.13"></a>

### 提示

在為了調校索引建立而設定 `parallel_workers` 之後，你可能會想將它重設。這可以避免意外改變查詢計畫，因為 `parallel_workers` 會影響*所有*平行資料表掃描。

雖然帶有 `CONCURRENTLY` 選項的 `CREATE INDEX` 支援平行建立且沒有特別限制，但實際上只有第一次資料表掃描會以平行方式執行。

使用 [`DROP INDEX`](sql-dropindex.md) 來移除索引。

如同任何長時間執行的交易，在資料表上執行 `CREATE INDEX`，可能會影響並行的 `VACUUM` 在其他任何資料表上能移除哪些 tuple。

PostgreSQL 先前的版本也有 R-tree 索引方法。此方法已被移除，因為它相較於 GiST 方法沒有顯著的優勢。若指定了 `USING rtree`，`CREATE INDEX` 會將它解讀為 `USING gist`，以簡化舊資料庫轉換到 GiST 的過程。

每個執行 `CREATE INDEX` 的後端都會在 `pg_stat_progress_create_index` 檢視表中回報其進度。詳情請參閱[第 27.4.4 節](../../server-administration/monitoring/progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)。

<a id="id-1.9.3.69.8"></a>

## 範例

在資料表 `films` 的欄位 `title` 上建立唯一值 B-tree 索引：

```

CREATE UNIQUE INDEX title_idx ON films (title);
```

在資料表 `films` 的欄位 `title` 上建立唯一值 B-tree 索引，並包含欄位 `director` 與 `rating`：

```

CREATE UNIQUE INDEX title_idx ON films (title) INCLUDE (director, rating);
```

建立停用去重複的 B-Tree 索引：

```

CREATE INDEX title_idx ON films (title) WITH (deduplicate_items = off);
```

在運算式 `lower(title)` 上建立索引，以便有效率地進行不分大小寫的搜尋：

```

CREATE INDEX ON films ((lower(title)));
```

（在此範例中，我們選擇省略索引名稱，因此系統會選擇一個名稱，通常是 `films_lower_idx`。）

建立使用非預設定序的索引：

```

CREATE INDEX title_idx_german ON films (title COLLATE "de_DE");
```

建立使用非預設 null 排序順序的索引：

```

CREATE INDEX title_idx_nulls_low ON films (title NULLS FIRST);
```

建立使用非預設填充因子（fill factor）的索引：

```

CREATE UNIQUE INDEX title_idx ON films (title) WITH (fillfactor = 70);
```

建立停用快速更新的 GIN 索引：

```

CREATE INDEX gin_idx ON documents_table USING GIN (locations) WITH (fastupdate = off);
```

在資料表 `films` 的欄位 `code` 上建立索引，並讓該索引位於資料表空間 `indexspace` 中：

```

CREATE INDEX code_idx ON films (code) TABLESPACE indexspace;
```

在 point 屬性上建立 GiST 索引，以便能對轉換函式的結果有效率地使用 box 運算子：

```

CREATE INDEX pointloc
    ON points USING gist (box(location,location));
SELECT * FROM points
    WHERE box(location,location) && '(0,0),(1,1)'::box;
```

建立索引而不鎖定資料表的寫入：

```

CREATE INDEX CONCURRENTLY sales_quantity_index ON sales_table (quantity);
```

<a id="id-1.9.3.69.9"></a>

## 相容性

`CREATE INDEX` 是 PostgreSQL 的語言擴充。SQL 標準中沒有任何關於索引的規定。

<a id="id-1.9.3.69.10"></a>

## 另請參閱

[ALTER INDEX](sql-alterindex.md), [DROP INDEX](sql-dropindex.md), [REINDEX](sql-reindex.md), [第 27.4.4 節](../../server-administration/monitoring/progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createindex.html)（原文版本：18.6；核對日期：2026-10-04）
