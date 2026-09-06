## 66.6. Database Page Layout [#](#STORAGE-PAGE-LAYOUT)

[66.6.1. Table Row Layout](storage-page-layout.md#STORAGE-TUPLE-LAYOUT)

This section provides an overview of the page format used within
PostgreSQL tables and indexes.[<a id="id-1.10.18.8.2.2"></a>[19]](#ftn.id-1.10.18.8.2.2)
Sequences and TOAST tables are formatted just like a regular table.

In the following explanation, a
*byte*
is assumed to contain 8 bits. In addition, the term
*item*
refers to an individual data value that is stored on a page. In a table,
an item is a row; in an index, an item is an index entry.

Every table and index is stored as an array of *pages* of a
fixed size (usually 8 kB, although a different page size can be selected
when compiling the server). In a table, all the pages are logically
equivalent, so a particular item (row) can be stored in any page. In
indexes, the first page is generally reserved as a *metapage*
holding control information, and there can be different types of pages
within the index, depending on the index access method.

[Table 66.2](storage-page-layout.md#PAGE-TABLE) shows the overall layout of a page.
There are five parts to each page.

<a id="PAGE-TABLE"></a>

**Table 66.2. Overall Page Layout**

<table border="1" class="table" summary="Overall Page Layout"><colgroup><col/><col/></colgroup><thead><tr><th>
Item
</th><th>Description</th></tr></thead><tbody><tr><td>PageHeaderData</td><td>24 bytes long. Contains general information about the page, including
free space pointers.</td></tr><tr><td>ItemIdData</td><td>Array of item identifiers pointing to the actual items. Each
entry is an (offset,length) pair. 4 bytes per item.</td></tr><tr><td>Free space</td><td>The unallocated space. New item identifiers are allocated from
the start of this area, new items from the end.</td></tr><tr><td>Items</td><td>The actual items themselves.</td></tr><tr><td>Special space</td><td>Index access method specific data. Different methods store different
data. Empty in ordinary tables.</td></tr></tbody></table>

<br>

The first 24 bytes of each page consists of a page header
(`PageHeaderData`). Its format is detailed in [Table 66.3](storage-page-layout.md#PAGEHEADERDATA-TABLE). The first field tracks the most
recent WAL entry related to this page. The second field contains
the page checksum if [data checksums](../../server-administration/wal/checksums.md) are
enabled. Next is a 2-byte field containing flag bits. This is followed
by three 2-byte integer fields (`pd_lower`,
`pd_upper`, and
`pd_special`). These contain byte offsets
from the page start to the start of unallocated space, to the end of
unallocated space, and to the start of the special space. The next 2
bytes of the page header, `pd_pagesize_version`,
store both the page size and a version indicator. Beginning with
PostgreSQL 8.3 the version number is 4;
PostgreSQL 8.1 and 8.2 used version number 3;
PostgreSQL 8.0 used version number 2;
PostgreSQL 7.3 and 7.4 used version number 1;
prior releases used version number 0.
(The basic page layout and header format has not changed in most of these
versions, but the layout of heap row headers has.) The page size
is basically only present as a cross-check; there is no support for having
more than one page size in an installation.
The last field is a hint that shows whether pruning the page is likely
to be profitable: it tracks the oldest un-pruned XMAX on the page.

<a id="PAGEHEADERDATA-TABLE"></a>

**Table 66.3. PageHeaderData Layout**

<table border="1" class="table" summary="PageHeaderData Layout"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>Field</th><th>Type</th><th>Length</th><th>Description</th></tr></thead><tbody><tr><td>pd_lsn</td><td>PageXLogRecPtr</td><td>8 bytes</td><td>LSN: next byte after last byte of WAL record for last change
   to this page</td></tr><tr><td>pd_checksum</td><td>uint16</td><td>2 bytes</td><td>Page checksum</td></tr><tr><td>pd_flags</td><td>uint16</td><td>2 bytes</td><td>Flag bits</td></tr><tr><td>pd_lower</td><td>LocationIndex</td><td>2 bytes</td><td>Offset to start of free space</td></tr><tr><td>pd_upper</td><td>LocationIndex</td><td>2 bytes</td><td>Offset to end of free space</td></tr><tr><td>pd_special</td><td>LocationIndex</td><td>2 bytes</td><td>Offset to start of special space</td></tr><tr><td>pd_pagesize_version</td><td>uint16</td><td>2 bytes</td><td>Page size and layout version number information</td></tr><tr><td>pd_prune_xid</td><td>TransactionId</td><td>4 bytes</td><td>Oldest unpruned XMAX on page, or zero if none</td></tr></tbody></table>

<br>

All the details can be found in
`src/include/storage/bufpage.h`.

Following the page header are item identifiers
(`ItemIdData`), each requiring four bytes.
An item identifier contains a byte-offset to
the start of an item, its length in bytes, and a few attribute bits
which affect its interpretation.
New item identifiers are allocated
as needed from the beginning of the unallocated space.
The number of item identifiers present can be determined by looking at
`pd_lower`, which is increased to allocate a new identifier.
Because an item
identifier is never moved until it is freed, its index can be used on a
long-term basis to reference an item, even when the item itself is moved
around on the page to compact free space. In fact, every pointer to an
item (`ItemPointer`, also known as
`CTID`) created by
PostgreSQL consists of a page number and the
index of an item identifier.

The items themselves are stored in space allocated backwards from the end
of unallocated space. The exact structure varies depending on what the
table is to contain. Tables and sequences both use a structure named
`HeapTupleHeaderData`, described below.

The final section is the “special section” which can
contain anything the access method wishes to store. For example,
b-tree indexes store links to the page's left and right siblings,
as well as some other data relevant to the index structure.
Ordinary tables do not use a special section at all (indicated by setting
`pd_special` to equal the page size).

[Figure 66.1](storage-page-layout.md#STORAGE-PAGE-LAYOUT-FIGURE) illustrates how these parts are
laid out in a page.

<a id="STORAGE-PAGE-LAYOUT-FIGURE"></a>

**Figure 66.1. Page Layout**

<br><a id="STORAGE-TUPLE-LAYOUT"></a>

### 66.6.1. Table Row Layout [#](#STORAGE-TUPLE-LAYOUT)

All table rows are structured in the same way. There is a fixed-size
header (occupying 23 bytes on most machines), followed by an optional null
bitmap, an optional object ID field, and the user data. The header is
detailed
in [Table 66.4](storage-page-layout.md#HEAPTUPLEHEADERDATA-TABLE). The actual user data
(columns of the row) begins at the offset indicated by
`t_hoff`, which must always be a multiple of the MAXALIGN
distance for the platform.
The null bitmap is
only present if the *HEAP_HASNULL* bit is set in
`t_infomask`. If it is present it begins just after
the fixed header and occupies enough bytes to have one bit per data column
(that is, the number of bits that equals the attribute count in
`t_infomask2`). In this list of bits, a
1 bit indicates not-null, a 0 bit is a null. When the bitmap is not
present, all columns are assumed not-null.
The object ID is only present if the *HEAP_HASOID_OLD* bit
is set in `t_infomask`. If present, it appears just
before the `t_hoff` boundary. Any padding needed to make
`t_hoff` a MAXALIGN multiple will appear between the null
bitmap and the object ID. (This in turn ensures that the object ID is
suitably aligned.)

<a id="HEAPTUPLEHEADERDATA-TABLE"></a>

**Table 66.4. HeapTupleHeaderData Layout**

<table border="1" class="table" summary="HeapTupleHeaderData Layout"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>Field</th><th>Type</th><th>Length</th><th>Description</th></tr></thead><tbody><tr><td>t_xmin</td><td>TransactionId</td><td>4 bytes</td><td>insert XID stamp</td></tr><tr><td>t_xmax</td><td>TransactionId</td><td>4 bytes</td><td>delete XID stamp</td></tr><tr><td>t_cid</td><td>CommandId</td><td>4 bytes</td><td>insert and/or delete CID stamp (overlays with t_xvac)</td></tr><tr><td>t_xvac</td><td>TransactionId</td><td>4 bytes</td><td>XID for VACUUM operation moving a row version</td></tr><tr><td>t_ctid</td><td>ItemPointerData</td><td>6 bytes</td><td>current TID of this or newer row version</td></tr><tr><td>t_infomask2</td><td>uint16</td><td>2 bytes</td><td>number of attributes, plus various flag bits</td></tr><tr><td>t_infomask</td><td>uint16</td><td>2 bytes</td><td>various flag bits</td></tr><tr><td>t_hoff</td><td>uint8</td><td>1 byte</td><td>offset to user data</td></tr></tbody></table>

<br>

All the details can be found in
`src/include/access/htup_details.h`.

Interpreting the actual data can only be done with information obtained
from other tables, mostly `pg_attribute`. The
key values needed to identify field locations are
`attlen` and `attalign`.
There is no way to directly get a
particular attribute, except when there are only fixed width fields and no
null values. All this trickery is wrapped up in the functions
*heap_getattr*, *fastgetattr*
and *heap_getsysattr*.

To read the data you need to examine each attribute in turn. First check
whether the field is NULL according to the null bitmap. If it is, go to
the next. Then make sure you have the right alignment. If the field is a
fixed width field, then all the bytes are simply placed. If it's a
variable length field (attlen = -1) then it's a bit more complicated.
All variable-length data types share the common header structure
`struct varlena`, which includes the total length of the stored
value and some flag bits. Depending on the flags, the data can be either
inline or in a TOAST table;
it might be compressed, too (see [Section 66.2](storage-toast.md)).

<br>

---

<a id="ftn.id-1.10.18.8.2.2"></a>

[[19]](#id-1.10.18.8.2.2) 
Actually, use of this page format is not required for either table or
index access methods. The `heap` table access method
always uses this format. All the existing index methods also use the
basic format, but the data kept on index metapages usually doesn't follow
the item layout rules.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-page-layout.html)（英文原文，待翻譯）
