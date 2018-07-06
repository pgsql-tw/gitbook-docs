# 65.1. Introduction

BRIN stands for Block Range Index. BRIN is designed for handling very large tables in which certain columns have some natural correlation with their physical location within the table. A _block range_ is a group of pages that are physically adjacent in the table; for each block range, some summary info is stored by the index. For example, a table storing a store's sale orders might have a date column on which each order was placed, and most of the time the entries for earlier orders will appear earlier in the table as well; a table storing a ZIP code column might have all codes for a city grouped together naturally.

BRIN indexes can satisfy queries via regular bitmap index scans, and will return all tuples in all pages within each range if the summary info stored by the index is _consistent_ with the query conditions. The query executor is in charge of rechecking these tuples and discarding those that do not match the query conditions — in other words, these indexes are lossy. Because a BRIN index is very small, scanning the index adds little overhead compared to a sequential scan, but may avoid scanning large parts of the table that are known not to contain matching tuples.

The specific data that a BRIN index will store, as well as the specific queries that the index will be able to satisfy, depend on the operator class selected for each column of the index. Data types having a linear sort order can have operator classes that store the minimum and maximum value within each block range, for instance; geometrical types might store the bounding box for all the objects in the block range.

The size of the block range is determined at index creation time by the `pages_per_range` storage parameter. The number of index entries will be equal to the size of the relation in pages divided by the selected value for `pages_per_range`. Therefore, the smaller the number, the larger the index becomes \(because of the need to store more index entries\), but at the same time the summary data stored can be more precise and more data blocks can be skipped during an index scan.

#### 65.1.1. Index Maintenance

At the time of creation, all existing heap pages are scanned and a summary index tuple is created for each range, including the possibly-incomplete range at the end. As new pages are filled with data, page ranges that are already summarized will cause the summary information to be updated with data from the new tuples. When a new page is created that does not fall within the last summarized range, that range does not automatically acquire a summary tuple; those tuples remain unsummarized until a summarization run is invoked later, creating initial summaries. This process can be invoked manually using the `brin_summarize_range(regclass, bigint)` or `brin_summarize_new_values(regclass)` functions; automatically when `VACUUM` processes the table; or by automatic summarization executed by autovacuum, as insertions occur. \(This last trigger is disabled by default and can be enabled with the `autosummarize` parameter.\) Conversely, a range can be de-summarized using the `brin_desummarize_range(regclass, bigint)` function, which is useful when the index tuple is no longer a very good representation because the existing values have changed.

When autosummarization is enabled, each time a page range is filled a request is sent to autovacuum for it to execute a targeted summarization for that range, to be fulfilled at the end of the next worker run on the same database. If the request queue is full, the request is not recorded and a message is sent to the server log:

```text
LOG:  request for BRIN range summarization for index "brin_wi_idx" page 128 was not recorded
```

When this happens, the range will be summarized normally during the next regular vacuum of the table.

