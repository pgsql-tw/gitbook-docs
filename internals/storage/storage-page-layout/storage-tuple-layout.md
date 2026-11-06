# 66.6.1. 資料表資料列配置

<a id="STORAGE-TUPLE-LAYOUT"></a>

## 66.6.1. 資料表資料列配置 [#](#storage-tuple-layout) <a href="#storage-tuple-layout" id="storage-tuple-layout"></a>

所有資料表資料列的結構都相同。有一個固定大小的標頭（在大多數機器上佔 23 個位元組），接著是選用的 null 點陣圖、選用的物件 ID 欄位，以及使用者資料。標頭詳見[表 66.4](storage-tuple-layout.md#heaptupleheaderdata-table)。實際的使用者資料（資料列的欄位）從 `t_hoff` 所指示的位移開始，這個位移必須永遠是該平台 MAXALIGN 距離的倍數。只有在 `t_infomask` 中設定了 *HEAP_HASNULL* 位元時，才會有 null 點陣圖。若存在，它會緊接在固定標頭之後開始，並佔用足夠的位元組，讓每個資料欄位各有一個位元（也就是位元數等於 `t_infomask2` 中的屬性數量）。在這個位元清單中，1 位元表示非 null，0 位元表示 null。當點陣圖不存在時，所有欄位都會被視為非 null。只有在 `t_infomask` 中設定了 *HEAP_HASOID_OLD* 位元時，才會有物件 ID。若存在，它會出現在緊接 `t_hoff` 邊界之前的位置。為了讓 `t_hoff` 成為 MAXALIGN 的倍數所需的任何填補，都會出現在 null 點陣圖與物件 ID 之間。（這也進而確保物件 ID 有適當的對齊。）

<a id="HEAPTUPLEHEADERDATA-TABLE"></a>

### 表 66.4. HeapTupleHeaderData 配置 [#](#heaptupleheaderdata-table) <a href="#heaptupleheaderdata-table" id="heaptupleheaderdata-table"></a>

<table border="1" class="table" summary="HeapTupleHeaderData 配置"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>長度</th><th>說明</th></tr></thead><tbody><tr><td>t_xmin</td><td>TransactionId</td><td>4 位元組</td><td>插入時的 XID 戳記</td></tr><tr><td>t_xmax</td><td>TransactionId</td><td>4 位元組</td><td>刪除時的 XID 戳記</td></tr><tr><td>t_cid</td><td>CommandId</td><td>4 位元組</td><td>插入以及／或刪除時的 CID 戳記（與 t_xvac 共用同一空間）</td></tr><tr><td>t_xvac</td><td>TransactionId</td><td>4 位元組</td><td>VACUUM 操作搬移資料列版本時的 XID</td></tr><tr><td>t_ctid</td><td>ItemPointerData</td><td>6 位元組</td><td>此資料列版本或較新資料列版本目前的 TID</td></tr><tr><td>t_infomask2</td><td>uint16</td><td>2 位元組</td><td>屬性數量，加上各種旗標位元</td></tr><tr><td>t_infomask</td><td>uint16</td><td>2 位元組</td><td>各種旗標位元</td></tr><tr><td>t_hoff</td><td>uint8</td><td>1 位元組</td><td>到使用者資料的位移</td></tr></tbody></table>

<br>

所有細節都可以在 `src/include/access/htup_details.h` 中找到。

只有使用從其他資料表（主要是 `pg_attribute`）取得的資訊，才能解讀實際的資料。識別欄位位置所需的關鍵值是 `attlen` 與 `attalign`。除非只有固定寬度的欄位而且沒有 null 值，否則無法直接取得特定的屬性。這些技巧全都包裝在函式 *heap_getattr*、*fastgetattr* 與 *heap_getsysattr* 中。

要讀取資料，你需要依序檢查每個屬性。首先根據 null 點陣圖檢查該欄位是否為 NULL。如果是，就前往下一個。接著確認對齊是否正確。若該欄位是固定寬度欄位，那麼所有位元組都是直接放置的。若它是可變長度欄位（attlen = -1），就會稍微複雜一些。所有可變長度資料型別都共用通用的標頭結構 `struct varlena`，其中包含所儲存之值的總長度與一些旗標位元。視旗標而定，資料可能是內嵌（inline）的，也可能位於 TOAST 資料表中；它也可能經過壓縮（請參閱[第 66.2 節](../storage-toast.md)）。

[返回 66.6. 資料庫頁面配置](../storage-page-layout.md#storage-page-layout)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-page-layout.html)（原文版本：18.6；核對日期：2026-10-17）
