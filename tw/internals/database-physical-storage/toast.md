---
description: 版本：11
---

# 68.2. TOAST

本節概述了 TOAST（The Oversized-Attribute Storage Technique，超大型屬性儲存技術）。

PostgreSQL 使用固定的頁面大小（通常為 8 kB），並且不允許 tuple 跨越多個頁面。 因此，不可能直接儲存非常大的字串。為了克服這個限制，將大字串壓縮和分解成多個實體資料列。這對使用者而言是無感的，對大多數後端程式碼的影響很小。該技術被親切地稱為 TOAST（或「切片麵包以來最好的東西」）。TOAST 基礎結構還用於改進記憶體中大資料值的處理。

只有某些資料型別支援 TOAST - 不需要對無法産生大字串的資料型別增加成本。為了支援 TOAST，資料型別必須具有可變長度（varlena）表示，其中，通常，任何儲存值的第一個 4 bytes 包含以 byte 為單位的總長度（包括其自身）。TOAST不會限制資料型別表示的其餘部分。統稱為 TOASTed 的特殊值表示透過修改或重新解釋此初始長度字來起作用。因此，支援 TOAST-able 資料型別的 C 語言函數必須注意它們如何處理可能的 TOASTed 輸入值：輸入實際上可能不包含 4 bytes 長度的字和內容，直到它被解除 TOAST。（這通常透過在對輸入值執行任何操作之前呼叫 PG\_DETOAST\_DATUM 來完成，但在某些情況下可以採用更有效的方法。有關更多詳細訊息，請參閱[第 37.11.1 節](../../server-programming/extending-sql/user-defined-types.md#37-11-1-toast-considerations)。）

TOAST 使用 varlena 長度的兩位元（big-endian 機器上的高位元，little-endian 機器上的低位元），從而將 TOAST-able 資料型別的任何值的邏輯大小限制為 1 GB。當兩個位元都為零時，該值是資料型別的普通值非 TOAST，長度位元組的其餘位以位元組為單位記錄總資料大小（包括長度位元組）。當設定最高位或最低位時，該值只有一個單位元組標頭而不是普通的四位元組標頭，該位元組的其餘位元表示以位元組為單位的總資料大小（包括長度位元組） 。此額外的方案支援空間高效率儲存短於 127 位元組的值，同時仍允許資料型別在需要時增長到 1 GB。具有單位元組標頭的值不在任何特定邊界上對齊，而具有四位元組標頭的值在至少四位元組邊界上對齊；與短值相比，這種省略對齊填充提供了額外的空間節省。作為特殊情況，如果單位元組標頭的剩餘位全部為零（對於自包含長度而言這是不可能的），則該值是指向外部資料的指標，具有如所描述的幾種可能的替代方案，如下所示。這種 TOAST 指標的型別和大小由儲存在資料的第二個位元組中的代碼決定。最後，當最高位元或最低位元清除為零但相鄰位置時，資料的內容已被壓縮，必須在使用前解壓縮。在這種情況下，四位元組長度字的剩餘位表示壓縮資料的總大小，而不是原始資料。請注意，對於外部資料也可以進行壓縮，但 varlena 標頭不會告訴它是否已經發生 - 而 TOAST 指標的內容則說明這件事。

如上所述，有多種類型的 TOAST 指標基準。最舊和最常見的類型是指向儲存在 TOAST 資料表中的外部資料的指標，該資料表與包含 TOAST 指標資料本身的資料表分開但與之相關聯。當要儲存在磁碟上的 tuple 太大而無法按原樣儲存時，這些磁碟指標基準由 TOAST 管理代碼（在 access/heap/tuptoaster.c 中）建立。更多細節見[第 66.2.1 節](toast.md#66-2-1-out-of-line-on-disk-toast-storage)。或者，TOAST 指標資料可以包含指向出現在記憶體中其他位置外部資料的指標。這些資料必然是短暫的，並且永遠不會出現在磁碟上，但它們對於避免複製和冗餘處理大量資料值非常有用。更多細節見[第 66.2.2 節](toast.md#66-2-2-out-of-line-in-memory-toast-storage)。

用於壓縮資料的壓縮技術是 LZ 系列壓縮技術中相當簡單且非常快速的方法。有關詳細訊息，請參閱 src/common/pg\_lzcompress.c。

## 66.2.1. Out-of-line, on-disk TOAST storage

如果資料表的任何欄位都是可以 TOAST 的，則該資料表將擁有關連的 TOAST 資料表，其 OID 儲存在資料表的 pg\_class.reltoastrelid 項目中。磁盤上 TOAST 後的值保留在 TOAST 資料表中，下面將有更詳細的描述。

Out-of-line values are divided \(after compression if used\) into chunks of at most `TOAST_MAX_CHUNK_SIZE` bytes \(by default this value is chosen so that four chunk rows will fit on a page, making it about 2000 bytes\). Each chunk is stored as a separate row in the TOAST table belonging to the owning table. Every TOAST table has the columns `chunk_id` \(an OID identifying the particular TOASTed value\), `chunk_seq` \(a sequence number for the chunk within its value\), and `chunk_data` \(the actual data of the chunk\). A unique index on `chunk_id` and `chunk_seq` provides fast retrieval of the values. A pointer datum representing an out-of-line on-disk TOASTed value therefore needs to store the OID of the TOAST table in which to look and the OID of the specific value \(its `chunk_id`\). For convenience, pointer datums also store the logical datum size \(original uncompressed data length\) and physical stored size \(different if compression was applied\). Allowing for the varlena header bytes, the total size of an on-disk TOAST pointer datum is therefore 18 bytes regardless of the actual size of the represented value.

The TOAST management code is triggered only when a row value to be stored in a table is wider than `TOAST_TUPLE_THRESHOLD` bytes \(normally 2 kB\). The TOAST code will compress and/or move field values out-of-line until the row value is shorter than `TOAST_TUPLE_TARGET`bytes \(also normally 2 kB\) or no more gains can be had. During an UPDATE operation, values of unchanged fields are normally preserved as-is; so an UPDATE of a row with out-of-line values incurs no TOAST costs if none of the out-of-line values change.

The TOAST management code recognizes four different strategies for storing TOAST-able columns on disk:

* `PLAIN` prevents either compression or out-of-line storage; furthermore it disables use of single-byte headers for varlena types. This is the only possible strategy for columns of non-TOAST-able data types.
* `EXTENDED` allows both compression and out-of-line storage. This is the default for most TOAST-able data types. Compression will be attempted first, then out-of-line storage if the row is still too big.
* `EXTERNAL` allows out-of-line storage but not compression. Use of `EXTERNAL` will make substring operations on wide `text` and `bytea` columns faster \(at the penalty of increased storage space\) because these operations are optimized to fetch only the required parts of the out-of-line value when it is not compressed.
* `MAIN` allows compression but not out-of-line storage. \(Actually, out-of-line storage will still be performed for such columns, but only as a last resort when there is no other way to make the row small enough to fit on a page.\)

Each TOAST-able data type specifies a default strategy for columns of that data type, but the strategy for a given table column can be altered with [`ALTER TABLE ... SET STORAGE`](https://www.postgresql.org/docs/10/static/sql-altertable.html).

This scheme has a number of advantages compared to a more straightforward approach such as allowing row values to span pages. Assuming that queries are usually qualified by comparisons against relatively small key values, most of the work of the executor will be done using the main row entry. The big values of TOASTed attributes will only be pulled out \(if selected at all\) at the time the result set is sent to the client. Thus, the main table is much smaller and more of its rows fit in the shared buffer cache than would be the case without any out-of-line storage. Sort sets shrink also, and sorts will more often be done entirely in memory. A little test showed that a table containing typical HTML pages and their URLs was stored in about half of the raw data size including the TOAST table, and that the main table contained only about 10% of the entire data \(the URLs and some small HTML pages\). There was no run time difference compared to an un-TOASTed comparison table, in which all the HTML pages were cut down to 7 kB to fit.

## 66.2.2. Out-of-line, in-memory TOAST storage

TOAST pointers can point to data that is not on disk, but is elsewhere in the memory of the current server process. Such pointers obviously cannot be long-lived, but they are nonetheless useful. There are currently two sub-cases: pointers to _indirect_ data and pointers to _expanded_ data.

Indirect TOAST pointers simply point at a non-indirect varlena value stored somewhere in memory. This case was originally created merely as a proof of concept, but it is currently used during logical decoding to avoid possibly having to create physical tuples exceeding 1 GB \(as pulling all out-of-line field values into the tuple might do\). The case is of limited use since the creator of the pointer datum is entirely responsible that the referenced data survives for as long as the pointer could exist, and there is no infrastructure to help with this.

Expanded TOAST pointers are useful for complex data types whose on-disk representation is not especially suited for computational purposes. As an example, the standard varlena representation of a PostgreSQL array includes dimensionality information, a nulls bitmap if there are any null elements, then the values of all the elements in order. When the element type itself is variable-length, the only way to find the _`N`_'th element is to scan through all the preceding elements. This representation is appropriate for on-disk storage because of its compactness, but for computations with the array it's much nicer to have an “expanded” or “deconstructed” representation in which all the element starting locations have been identified. The TOAST pointer mechanism supports this need by allowing a pass-by-reference Datum to point to either a standard varlena value \(the on-disk representation\) or a TOAST pointer that points to an expanded representation somewhere in memory. The details of this expanded representation are up to the data type, though it must have a standard header and meet the other API requirements given in `src/include/utils/expandeddatum.h`. C-level functions working with the data type can choose to handle either representation. Functions that do not know about the expanded representation, but simply apply `PG_DETOAST_DATUM`to their inputs, will automatically receive the traditional varlena representation; so support for an expanded representation can be introduced incrementally, one function at a time.

TOAST pointers to expanded values are further broken down into _read-write_ and _read-only_ pointers. The pointed-to representation is the same either way, but a function that receives a read-write pointer is allowed to modify the referenced value in-place, whereas one that receives a read-only pointer must not; it must first create a copy if it wants to make a modified version of the value. This distinction and some associated conventions make it possible to avoid unnecessary copying of expanded values during query execution.

For all types of in-memory TOAST pointer, the TOAST management code ensures that no such pointer datum can accidentally get stored on disk. In-memory TOAST pointers are automatically expanded to normal in-line varlena values before storage — and then possibly converted to on-disk TOAST pointers, if the containing tuple would otherwise be too big.

