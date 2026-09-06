## 第 66 章 資料庫實體儲存

**目錄**

[66.1. 資料庫檔案配置](storage-file-layout.md)

[66.2. TOAST](storage-toast.md)
:   [66.2.1. 資料列外的磁碟 TOAST 儲存](storage-toast.md#STORAGE-TOAST-ONDISK)

    [66.2.2. 資料列外的記憶體 TOAST 儲存](storage-toast.md#STORAGE-TOAST-INMEMORY)

[66.3. 可用空間對照表](storage-fsm.md)

[66.4. 可見性對照表](storage-vm.md)

[66.5. 初始化分支檔案](storage-init.md)

[66.6. 資料庫頁面配置](storage-page-layout.md)
:   [66.6.1. 資料表資料列配置](storage-page-layout.md#STORAGE-TUPLE-LAYOUT)

[66.7. 僅存於堆積的資料列（HOT）](storage-hot.md)

本章概述 PostgreSQL 資料庫所使用的實體儲存格式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage.html)（原文版本：18.6；核對日期：2026-09-07）
