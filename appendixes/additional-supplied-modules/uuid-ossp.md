# F.44. uuid-ossp

uuid-ossp 模組提供了使用幾種標準演算法來產生 Universally Unique IDentifiers (UUIDs) 的功能。還有一些函數可以產生某些特殊的 UUID 常數。此模組僅在 PostgreSQL 中特殊需求時才需要。有關產生 UUID 的內建函數，請參閱[第 9.14 節](../../the-sql-language/functions-and-operators/uuid-functions.md)。

該模組被認為是「可信任的」，也就是說，它可以由對目前資料庫具有 CREATE 權限的非超級使用者安裝。

## F.44.1. `uuid-ossp` Functions

[Table F.32](uuid-ossp.md#table-f-32-functions-for-uuid-generation) 列出了可用於產生 UUID 的函數。相關標準為 ITU-T Rec. X.667、ISO/IEC 9834-8:2005 和 RFC 4122 所指定的四種用於產生 UUID 的演算法，由標示為版本號 1、3、4 和 5 。（沒有版本 2 。）這些演算法可能適用於不同的應用情境。

#### **Table F.32. Functions for UUID Generation**

| <p>Function</p><p>Description</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p><code>uuid_generate_v1</code> () → <code>uuid</code></p><p>版本 1 UUID。 這涉及主機的 MAC 位址和時間戳記。請注意，此類 UUID 會顯示建立識別符的主機身份及其建立時間，這可能使其不適用於某些對安全敏感的應用情境。</p>                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| <p><code>uuid_generate_v1mc</code> () → <code>uuid</code></p><p>產生版本 1 UUID，但使用隨機的 multicast MAC 位址而不是主機的真實 MAC 位址。</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| <p><code>uuid_generate_v3</code> ( <em><code>namespace</code></em> <code>uuid</code>, <em><code>name</code></em> <code>text</code> ) → <code>uuid</code></p><p>使用指定的輸入名稱在給予的命名空間 namespace 中產生成版本 3 的 UUID。命名空間應該是 <a href="uuid-ossp.md#table-f-33-functions-returning-uuid-constants">Table F.33</a> 中列出的的 uuid<em>ns</em>*() 函數產生的特殊常數之一。（理論上可以是任何的 UUID。）名稱是所選命名空間中的識別字。</p><p>例如：<br>SELECT uuid_generate_v3(uuid_ns_url(), '<a href="http://www.postgresql.org">http://www.postgresql.org</a>');</p><p>參數 name 將為 MD5 雜湊值，因此無法從產生的 UUID 反推原來的內容。透過這種方法產生的 UUID 並沒有隨機或與環境相關的元素，因此是可重現的。</p> |
| <p><code>uuid_generate_v4</code> () → <code>uuid</code></p><p>產生版本 4 UUID，它完全來自亂數。</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| <p><code>uuid_generate_v5</code> ( <em><code>namespace</code></em> <code>uuid</code>, <em><code>name</code></em> <code>text</code> ) → <code>uuid</code></p><p>產生版本 5 的 UUID，此版本與版本 3 UUID 類似，不同之處在於以 SHA-1 作為雜湊演算法。版本 5 應該比版本 3 更好，因為 SHA-1 被認為比 MD5 更加安全。</p>                                                                                                                                                                                                                                                                                                                                  |

#### **Table F.33. Functions Returning UUID Constants**

| <p>Function</p><p>Description</p>                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>uuid_nil</code> () → <code>uuid</code></p><p>回傳一個「nil」UUID 常數，它不會產生為真正的 UUID。</p>                                                         |
| <p><code>uuid_ns_dns</code> () → <code>uuid</code></p><p>回傳一個常數，為 UUID 指定為 DNS 的命名空間。</p>                                                          |
| <p><code>uuid_ns_url</code> () → <code>uuid</code></p><p>回傳一個常數，指定 UUID 為 URL 的命名空間。</p>                                                           |
| <p><code>uuid_ns_oid</code> () → <code>uuid</code></p><p>回傳一個常數，為 UUID 指定 ISO 物件識別符號 (OID) 的命名空間。 （這與 ASN.1 OID 相關，它與 PostgreSQL 中使用的 OID 無關。）</p> |
| <p><code>uuid_ns_x500</code> () → <code>uuid</code></p><p>回傳指定 UUID 為 X.500 專有名稱 (DN) 命名空間的常數。</p>                                                 |

## F.44.2. Building `uuid-ossp`

從歷史上看，這個模組相依於 OSSP UUID 函式庫，它也是模組名稱的由來。雖然 OSSP UUID 庫仍然可以在 [http://www.ossp.org/pkg/lib/uuid/](http://www.ossp.org/pkg/lib/uuid/) 找到，但它沒有得到很好的維護，並且越來越難以移植到更新的平台。uuid-ossp 現在可以在某些平台上在沒有 OSSP 函式庫的情況下編譯。在 FreeBSD、NetBSD 和其他一些 BSD 衍生平台上，核心 libc 函式庫中包含合適的 UUID 建立函數。在 Linux、macOS 和其他一些平台上，libuuid 函式庫中提供了合適的函數，該函式庫最初來自 e2fsprogs 專案（儘管在近代 Linux 上它被認為是 util-linux-ng 的一部分）。呼叫 configure 時，指定 --with-uuid=bsd 使用 BSD 函數，或 --with-uuid=e2fs 使用 e2fsprogs 的 libuuid，或 --with-uuid=ossp 使用 OSSP UUID 函式庫。在某些主機上可能有多種函式庫可用，因此 configure 並不會自動選擇。

## F.44.3. Author

Peter Eisentraut `<`[`peter_e@gmx.net`](mailto:peter\_e@gmx.net)`>`
