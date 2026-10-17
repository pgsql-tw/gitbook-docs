<a id="TABLEAM"></a>

## 第 62 章 資料表存取方法介面定義

<a id="id-1.10.14.2"></a><a id="id-1.10.14.3"></a>

本章說明 PostgreSQL 核心系統與*資料表存取方法*之間的介面，資料表存取方法負責管理資料表的儲存。除了此處所規範的內容之外，核心系統對這些存取方法所知甚少，因此可以藉由撰寫附加程式碼來開發全新的存取方法類型。

每個資料表存取方法都由 [`pg_am`](../catalogs/catalog-pg-am.md) 系統目錄中的一筆資料列描述。`pg_am` 項目指定了資料表存取方法的名稱與*處理函式*。這些項目可以使用 [CREATE ACCESS METHOD](../../reference/sql-commands/sql-create-access-method.md) 與 [DROP ACCESS METHOD](../../reference/sql-commands/sql-drop-access-method.md) SQL 命令建立與移除。

資料表存取方法的處理函式必須宣告為接受單一個型別為 `internal` 的引數，並傳回虛擬型別
`table_am_handler`。該引數是一個虛設值，作用只是防止處理函式直接從 SQL 命令中被呼叫。

以下是擴充功能的 SQL 指令碼檔案建立資料表存取方法處理函式的可能寫法：

```

CREATE OR REPLACE FUNCTION my_tableam_handler(internal)
  RETURNS table_am_handler AS 'my_extension', 'my_tableam_handler'
  LANGUAGE C STRICT;

CREATE ACCESS METHOD myam TYPE TABLE HANDLER my_tableam_handler;
```

此函式的結果必須是指向型別為
`TableAmRoutine` 之結構的指標，該結構包含核心程式碼使用此資料表存取方法所需知道的一切。傳回值的生命週期必須與伺服器相同，通常的做法是在全域範圍中將它定義為 `static const` 變數。

以下是包含資料表存取方法處理函式之原始碼檔案的可能樣貌：

```

#include "postgres.h"

#include "access/tableam.h"
#include "fmgr.h"

PG_MODULE_MAGIC;

static const TableAmRoutine my_tableam_methods = {
    .type = T_TableAmRoutine,

    /* Methods of TableAmRoutine omitted from example, add them here. */
};

PG_FUNCTION_INFO_V1(my_tableam_handler);

Datum
my_tableam_handler(PG_FUNCTION_ARGS)
{
    PG_RETURN_POINTER(&my_tableam_methods);
}
```

`TableAmRoutine` 結構也稱為存取方法的 *API 結構*，它以回呼函式定義存取方法的行為。這些回呼函式是指向一般 C 函式的指標，在 SQL 層級既不可見，也無法呼叫。所有回呼函式及其行為都定義在
`TableAmRoutine` 結構中（結構內的註解定義了對回呼函式的要求）。大多數回呼函式都有包裝函式，這些包裝函式是從資料表存取方法的使用者（而非實作者）的角度撰寫文件。詳細資訊請參閱 [`src/include/access/tableam.h`](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/access/tableam.h;hb=HEAD) 檔案。

要實作存取方法，實作者通常需要實作一種 AM 專屬的 tuple table slot 類型（請參閱
[`src/include/executor/tuptable.h`](https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/include/executor/tuptable.h;hb=HEAD)），讓存取方法以外的程式碼可以持有對該 AM 之 tuple 的參照，並存取 tuple 的欄位。

目前，AM 實際儲存資料的方式相當不受限制。例如，可以使用（但並非必須使用）postgres 的共享緩衝區快取。若有使用它，那麼使用
[第 66.6 節](../storage/storage-page-layout.md)所述的 PostgreSQL 標準頁面配置，可能會比較合理。

資料表存取方法 API 有一項相當大的限制：目前，如果 AM 想要支援修改及／或索引，每個 tuple 都必須具有由區塊編號與項目編號組成的 tuple 識別碼（TID）（另請參閱[第 66.6 節](../storage/storage-page-layout.md)）。TID 的各組成部分並不嚴格要求具有與（例如）`heap` 中相同的意義，但如果希望支援點陣圖掃描（這是選用的），區塊編號就必須能提供區域性。

為了確保當機安全，AM 可以使用 postgres 的 [WAL](../../server-administration/wal/README.md)，或使用自訂的實作。
若選擇 WAL，可以使用[通用 WAL 記錄](../wal-for-extensions/generic-wal.md)，
也可以實作[自訂 WAL 資源管理器](../wal-for-extensions/custom-rmgr.md)。

若要以允許在單一交易中存取不同資料表存取方法的方式實作交易支援，很可能必須與
`src/backend/access/transam/xlog.c` 中的機制緊密整合。

任何新 `table access method` 的開發者，都可以參考
`src/backend/access/heap/heapam_handler.c` 中現有的 `heap` 實作，了解其實作細節。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tableam.html)（原文版本：18.6；核對日期：2026-10-12）
