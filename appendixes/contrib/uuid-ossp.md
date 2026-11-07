<a id="UUID-OSSP"></a>

## F.49. uuid-ossp — UUID 產生器 [#](#uuid-ossp) <a href="#uuid-ossp" id="uuid-ossp"></a>

[F.49.1. `uuid-ossp` 函式](uuid-ossp/uuid-ossp-functions-sect.md#uuid-ossp-functions-sect)

[F.49.2. 建置 `uuid-ossp`](uuid-ossp.md#uuid-ossp-building)

[F.49.3. 作者](uuid-ossp.md#uuid-ossp-author)

<a id="id-1.11.7.59.2"></a>

`uuid-ossp` 模組提供多個函式，可使用數種標準演算法之一產生通用唯一識別碼（UUID）。此外也有函式可產生某些特殊的 UUID 常數。只有在需求超出 PostgreSQL 核心所提供的功能時，才需要此模組。產生 UUID 的內建方式請參閱[第 9.14 節](../../the-sql-language/functions/functions-uuid.md)。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

### F.49.1. `uuid-ossp` 函式 [#](#uuid-ossp-functions-sect) <a href="#uuid-ossp-functions-sect" id="uuid-ossp-functions-sect"></a>

完整內容請見 [F.49.1. uuid-ossp 函式](uuid-ossp/uuid-ossp-functions-sect.md#uuid-ossp-functions-sect)。

<a id="UUID-OSSP-BUILDING"></a>

### F.49.2. 建置 `uuid-ossp` [#](#uuid-ossp-building) <a href="#uuid-ossp-building" id="uuid-ossp-building"></a>

過去此模組依賴 OSSP UUID 函式庫，這也是此模組名稱的由來。雖然 OSSP UUID 函式庫仍可在 <http://www.ossp.org/pkg/lib/uuid/> 找到，但它的維護狀況不佳，而且越來越難以移植到較新的平台。現在 `uuid-ossp` 在某些平台上可以不依賴 OSSP 函式庫建置。在 FreeBSD 與其他一些 BSD 衍生平台上，核心的 `libc` 函式庫已包含合適的 UUID 建立函式。在 Linux、macOS 與其他一些平台上，合適的函式由 `libuuid` 函式庫提供，該函式庫最初來自 `e2fsprogs` 專案（不過在現代的 Linux 上，它被視為 `util-linux-ng` 的一部分）。呼叫 `configure` 時，指定 `--with-uuid=bsd` 以使用 BSD 函式，或指定 `--with-uuid=e2fs` 以使用 `e2fsprogs` 的 `libuuid`，或指定 `--with-uuid=ossp` 以使用 OSSP UUID 函式庫。一部特定機器上可能有超過一個這類函式庫可用，因此 `configure` 不會自動選擇其中一個。

<a id="UUID-OSSP-AUTHOR"></a>

### F.49.3. 作者 [#](#uuid-ossp-author) <a href="#uuid-ossp-author" id="uuid-ossp-author"></a>

Peter Eisentraut `<peter_e@gmx.net>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/uuid-ossp.html)（原文版本：18.6；核對日期：2026-10-22）
