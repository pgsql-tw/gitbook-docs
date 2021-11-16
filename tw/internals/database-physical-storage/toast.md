---
description: 版本：11
---

# 68.2. TOAST

本節概述了 TOAST（The Oversized-Attribute Storage Technique，超大型屬性儲存技術）。

PostgreSQL 使用固定的頁面大小（通常為 8 kB），並且不允許 tuple 跨越多個頁面。 因此，不可能直接儲存非常大的字串。為了克服這個限制，將大字串壓縮和分解成多個實體資料列。這對使用者而言是無感的，對大多數後端程式碼的影響很小。該技術被親切地稱為 TOAST（或「切片麵包以來最好的東西」）。TOAST 基礎結構還用於改進記憶體中大資料值的處理。

只有某些資料型別支援 TOAST - 不需要對無法産生大字串的資料型別增加成本。為了支援 TOAST，資料型別必須具有可變長度（varlena）表示，其中，通常，任何儲存值的第一個 4 bytes 包含以 byte 為單位的總長度（包括其自身）。TOAST不會限制資料型別表示的其餘部分。統稱為 TOASTed 的特殊值表示透過修改或重新解釋此初始長度字來起作用。因此，支援 TOAST-able 資料型別的 C 語言函數必須注意它們如何處理可能的 TOASTed 輸入值：輸入實際上可能不包含 4 bytes 長度的字和內容，直到它被解除 TOAST。（這通常透過在對輸入值執行任何操作之前呼叫 PG\_DETOAST\_DATUM 來完成，但在某些情況下可以採用更有效的方法。有關更多詳細訊息，請參閱[第 37.13.1 節](../../server-programming/extending-sql/user-defined-types.md#37-13-1-toast-considerations)。）

TOAST 使用 varlena 長度的兩位元（big-endian 機器上的高位元，little-endian 機器上的低位元），從而將 TOAST-able 資料型別的任何值的邏輯大小限制為 1 GB。當兩個位元都為零時，該值是資料型別的普通值非 TOAST，長度位元組的其餘位以位元組為單位記錄總資料大小（包括長度位元組）。當設定最高位或最低位時，該值只有一個單位元組標頭而不是普通的四位元組標頭，該位元組的其餘位元表示以位元組為單位的總資料大小（包括長度位元組） 。此額外的方案支援空間高效率儲存短於 127 位元組的值，同時仍允許資料型別在需要時增長到 1 GB。具有單位元組標頭的值不在任何特定邊界上對齊，而具有四位元組標頭的值在至少四位元組邊界上對齊；與短值相比，這種省略對齊填充提供了額外的空間節省。作為特殊情況，如果單位元組標頭的剩餘位全部為零（對於自包含長度而言這是不可能的），則該值是指向外部資料的指標，具有如所描述的幾種可能的替代方案，如下所示。這種 TOAST 指標的型別和大小由儲存在資料的第二個位元組中的代碼決定。最後，當最高位元或最低位元清除為零但相鄰位置時，資料的內容已被壓縮，必須在使用前解壓縮。在這種情況下，四位元組長度字的剩餘位表示壓縮資料的總大小，而不是原始資料。請注意，對於外部資料也可以進行壓縮，但 varlena 標頭不會告訴它是否已經發生 - 而 TOAST 指標的內容則說明這件事。

如上所述，有多種類型的 TOAST 指標基準。最舊和最常見的類型是指向儲存在 TOAST 資料表中的外部資料的指標，該資料表與包含 TOAST 指標資料本身的資料表分開但與之相關聯。當要儲存在磁碟上的 tuple 太大而無法按原樣儲存時，這些磁碟指標基準由 TOAST 管理代碼（在 access/heap/tuptoaster.c 中）建立。更多細節見[第 68.2.1 節](toast.md#66-2-1-out-of-line-on-disk-toast-storage)。或者，TOAST 指標資料可以包含指向出現在記憶體中其他位置外部資料的指標。這些資料必然是短暫的，並且永遠不會出現在磁碟上，但它們對於避免複製和冗餘處理大量資料值非常有用。更多細節見[第 68.2.2 節](toast.md#66-2-2-out-of-line-in-memory-toast-storage)。

用於壓縮資料的壓縮技術是 LZ 系列壓縮技術中相當簡單且非常快速的方法。有關詳細訊息，請參閱 src/common/pg\_lzcompress.c。

## 68.2.1. Out-of-line, on-disk TOAST storage

如果資料表的任何欄位都是可以 TOAST 的，則該資料表將擁有關連的 TOAST 資料表，其 OID 儲存在資料表的 pg\_class.reltoastrelid 項目中。磁盤上 TOAST 後的值保留在 TOAST 資料表中，下面將有更詳細的描述。

將 out-of-line 的內容（在壓縮後使用）分割為最多 TOAST\_MAX\_CHUNK\_SIZE 個字元的區塊（預設情況下，選擇此值使得四個區塊的資料列行剛好放進一個 page，大約為 2000 個字元）。每個區塊都屬於其所有資料表的 TOAST 資料表中單獨的資料列來儲存。每個 TOAST 資料表都有欄位的 chunk\_id（識別特定有 TOAST 值的 OID），chunk\_seq（其值中區塊的序列號）和 chunk\_data（區塊的實際資料）。chunk\_id 和 chunk\_seq 上的唯一索引提供了對內容的快速檢索。表示線上磁碟 TOAST 值的指標資料需要儲存要查看的 TOAST 資料表 OID 以及特定值的 OID（其chunk\_id）。為方便起見，指標 datum 還儲存邏輯上的 datum 大小（原始未壓縮字串長度）和實際上的儲存大小（如果套用了壓縮則會不同）。因此，允許 varlena 標頭字元，磁碟 TOAST 指標資料的總大小為 18 個位元組，不論其所表示字串大小。

僅當要儲存在資料表中的資料列內容大於 TOAST\_TUPLE\_THRESHOLD 字元（通常為2 kB）時，才會觸發 TOAST 機制。TOAST 程式將會壓縮或移動字串內容，直到資料列小於 TOAST\_TUPLE\_TARGET 個字元（通常也是 2 kB）或者不能再獲得更多的增益。在 UPDATE 操作期間，未變更字串的內容通常就保持原樣；因此，如果沒有任何 out-of-line 需要變更，則具有 out-of-line 的資料列更新就不會產生任何 TOAST 成本。

TOAST 機制識別用於在磁碟上儲存可 TOAST 欄位有四種不同策略：

* PLAIN 可防止壓縮或 out-of-line 儲存方式；此外，它禁止使用 varlena 類型的單字元標頭。對於非 TOAST-capable 資料型別欄位，這是唯一可行的策略。
* EXTENDED 允許壓縮和 out-of-line 儲存。這是大多數 TOAST-capable 資料型別的預設方式。首先嘗試壓縮，然後在資料列仍然太大的情況下進行 out-of-line 儲存。
* EXTERNAL 允許 out-of-line 儲存但不允許壓縮。使用 EXTERNAL 將使大量文字和 bytea 欄位上的子字串操作更快（以增加的儲存空間為代價），因為這些操作被最佳化為在未壓縮時僅獲取 out-of-line 內容所需的部分。
* MAIN 允許壓縮但不允許 out-of-line 儲存。（實際上，仍然會為這些欄位執行 out-of-line 儲存，但只有在沒有其他方法使資料列足夠小到適合頁面時才做的最後手段。）

每個 TOAST-able 資料型別會為該型別的欄位指定預設策略，但是可以使用 [ALTER TABLE ... SET STORAGE](../../reference/sql-commands/alter-table.md) 變更指定資料表欄位的策略。

可以使用 [`ALTER TABLE ... SET（toast_tuple_target = N）`](../../reference/sql-commands/alter-table.md)為每個資料表調整` TOAST_TUPLE_TARGET` 的值。

與更直覺的方法（例如允許資料列內容跨越頁面）相比，此方案具有許多優點。假設查詢通常透過與相對較小的鍵值進行比較來過濾，執行程序的大部分工作將使用主要欄位完成。 TOASTed 屬性的大量內容只會在結果集發送到用戶端時被取出（如果選中的話）。因此，與沒有任何外部儲存的情況相比，主要資料表更小並且其更多資料列置於共享緩衝區高速處理。排序集合也會縮小，而排序通常完全在記憶體中完成。一個小小的測試顯示，包含典型 HTML 頁面及其 URL 的資料儲存在大約一半的原始資料大小（包括 TOAST 資料表）中，並且主要資料表僅包含大約 10％ 的內容（URL 和一些小的 HTML）。與未轉換的相比，並沒有執行時間差異，其中所有 HTML 頁面都被削減到 7 kB 以適應頁面。

## 68.2.2. Out-of-line, in-memory TOAST storage

TOAST pointers can point to data that is not on disk, but is elsewhere in the memory of the current server process. Such pointers obviously cannot be long-lived, but they are nonetheless useful. There are currently two sub-cases: pointers to _indirect_ data and pointers to _expanded_ data.

Indirect TOAST pointers simply point at a non-indirect varlena value stored somewhere in memory. This case was originally created merely as a proof of concept, but it is currently used during logical decoding to avoid possibly having to create physical tuples exceeding 1 GB (as pulling all out-of-line field values into the tuple might do). The case is of limited use since the creator of the pointer datum is entirely responsible that the referenced data survives for as long as the pointer could exist, and there is no infrastructure to help with this.

Expanded TOAST pointers are useful for complex data types whose on-disk representation is not especially suited for computational purposes. As an example, the standard varlena representation of a PostgreSQL array includes dimensionality information, a nulls bitmap if there are any null elements, then the values of all the elements in order. When the element type itself is variable-length, the only way to find the _`N`_'th element is to scan through all the preceding elements. This representation is appropriate for on-disk storage because of its compactness, but for computations with the array it's much nicer to have an “expanded” or “deconstructed” representation in which all the element starting locations have been identified. The TOAST pointer mechanism supports this need by allowing a pass-by-reference Datum to point to either a standard varlena value (the on-disk representation) or a TOAST pointer that points to an expanded representation somewhere in memory. The details of this expanded representation are up to the data type, though it must have a standard header and meet the other API requirements given in `src/include/utils/expandeddatum.h`. C-level functions working with the data type can choose to handle either representation. Functions that do not know about the expanded representation, but simply apply `PG_DETOAST_DATUM`to their inputs, will automatically receive the traditional varlena representation; so support for an expanded representation can be introduced incrementally, one function at a time.

TOAST pointers to expanded values are further broken down into _read-write_ and _read-only_ pointers. The pointed-to representation is the same either way, but a function that receives a read-write pointer is allowed to modify the referenced value in-place, whereas one that receives a read-only pointer must not; it must first create a copy if it wants to make a modified version of the value. This distinction and some associated conventions make it possible to avoid unnecessary copying of expanded values during query execution.

For all types of in-memory TOAST pointer, the TOAST management code ensures that no such pointer datum can accidentally get stored on disk. In-memory TOAST pointers are automatically expanded to normal in-line varlena values before storage — and then possibly converted to on-disk TOAST pointers, if the containing tuple would otherwise be too big.
