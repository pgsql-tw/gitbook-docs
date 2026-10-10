<a id="CUSTOM-RMGR"></a>

## 64.2. 自訂 WAL 資源管理器 [#](#CUSTOM-RMGR)

本節說明 PostgreSQL 核心系統與自訂 WAL 資源管理器之間的介面；自訂 WAL 資源管理器讓擴充功能能夠直接與 [WAL](../../server-administration/wal/README.md) 整合。

擴充功能，尤其是[資料表存取方法](../tableam/README.md)或[索引存取方法](../indexam/README.md)，可能需要使用 WAL 來進行復原、複寫及／或[邏輯解碼](../../server-programming/logicaldecoding/README.md)。

要建立新的自訂 WAL 資源管理器，首先定義一個 `RmgrData` 結構，其中包含資源管理器各方法的實作。請參閱 PostgreSQL 原始碼中的 `src/backend/access/transam/README` 與 `src/include/access/xlog_internal.h`。

```

/*
 * Method table for resource managers.
 *
 * This struct must be kept in sync with the PG_RMGR definition in
 * rmgr.c.
 *
 * rm_identify must return a name for the record based on xl_info (without
 * reference to the rmid). For example, XLOG_BTREE_VACUUM would be named
 * "VACUUM". rm_desc can then be called to obtain additional detail for the
 * record, if available (e.g. the last block).
 *
 * rm_mask takes as input a page modified by the resource manager and masks
 * out bits that shouldn't be flagged by wal_consistency_checking.
 *
 * RmgrTable[] is indexed by RmgrId values (see rmgrlist.h). If rm_name is
 * NULL, the corresponding RmgrTable entry is considered invalid.
 */
typedef struct RmgrData
{
    const char *rm_name;
    void        (*rm_redo) (XLogReaderState *record);
    void        (*rm_desc) (StringInfo buf, XLogReaderState *record);
    const char *(*rm_identify) (uint8 info);
    void        (*rm_startup) (void);
    void        (*rm_cleanup) (void);
    void        (*rm_mask) (char *pagedata, BlockNumber blkno);
    void        (*rm_decode) (struct LogicalDecodingContext *ctx,
                              struct XLogRecordBuffer *buf);
} RmgrData;
```

`src/test/modules/test_custom_rmgrs` 模組包含一個可運作的範例，示範自訂 WAL 資源管理器的用法。

接著，註冊你的新資源管理器。

```

/*
 * Register a new custom WAL resource manager.
 *
 * Resource manager IDs must be globally unique across all extensions. Refer
 * to https://wiki.postgresql.org/wiki/CustomWALResourceManagers to reserve a
 * unique RmgrId for your extension, to avoid conflicts with other extension
 * developers. During development, use RM_EXPERIMENTAL_ID to avoid needlessly
 * reserving a new ID.
 */
extern void RegisterCustomRmgr(RmgrId rmid, const RmgrData *rmgr);
```

`RegisterCustomRmgr` 必須從擴充功能模組的 [_PG_init](../../server-programming/extend/xfunc-c.md#XFUNC-C-DYNLOAD) 函式中呼叫。開發新的擴充功能期間，請使用 `RM_EXPERIMENTAL_ID` 作為 *`rmid`*。當你準備好將擴充功能發布給使用者時，請在 [Custom WAL Resource Manager](https://wiki.postgresql.org/wiki/CustomWALResourceManagers) 頁面上保留一個新的資源管理器 ID。

將實作自訂資源管理器的擴充功能模組放入 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)，使它在 PostgreSQL 啟動期間就提早載入。

<a id="CUSTOM-RMGR-NOTE"></a>

### 注意

只要系統中可能還存在任何自訂 WAL 記錄，擴充功能就必須保留在 `shared_preload_libraries` 中。否則 PostgreSQL 將無法套用或解碼這些自訂 WAL 記錄，這可能導致伺服器無法啟動。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/custom-rmgr.html)（原文版本：18.6；核對日期：2026-10-09）
