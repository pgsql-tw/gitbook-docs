# 8.12. UUID 型別

資料型別 uuid 儲存由 RFC 4122、ISO/IEC 9834-8:2005 和相關標準定義的通用唯一識別字 (Universally Unique IDentifiers, UUID)。（有些系統將此資料型別稱為 Globally Unique IDentifier 或 GUID。）此識別字是一個 128 位元的數字，由所選擇演算法產生，以確保其他任何人在已知的情況下使用相同的演算法都不太可能產生相同的識別字。因此，對於分散式系統，這些識別字提供了比序列產生器更好的唯一性保證，序列產生器僅在單一資料庫中確保唯一性。

一個 UUID 寫成一系列小寫的十六進位數字，由連接字元分隔為幾組，特別是一組 8 位數字後跟三組 4 位數字後跟一組 12 位數字，總共 32 位數字代表 128 位元。此標準形式的 UUID 範例是：

```
a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
```

PostgreSQL 還接受以下替代形式的輸入方式：使用大寫數字、用大括號括起來的標準格式、省略部分或全部連接字元、在任何一組四位數字後加上連接字元。一些例子如下：

```
A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11
{a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11}
a0eebc999c0b4ef8bb6d6bb9bd380a11
a0ee-bc99-9c0b-4ef8-bb6d-6bb9-bd38-0a11
{a0eebc99-9c0b4ef8-bb6d6bb9-bd380a11}
```

Output is always in the standard form.

有關如何在 PostgreSQL 中產生 UUID，請參閱[第 9.14 節](../functions-and-operators/uuid-functions.md)。
