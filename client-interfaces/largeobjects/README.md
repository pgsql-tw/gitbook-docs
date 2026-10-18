<a id="LARGEOBJECTS"></a>

## 第 33 章 大型物件

**目錄**

[33.1. 簡介](lo-intro.md)

[33.2. 實作特性](lo-implementation.md)

[33.3. 用戶端介面](lo-interfaces.md)
:   [33.3.1. 建立大型物件](lo-interfaces.md#LO-CREATE)

    [33.3.2. 匯入大型物件](lo-interfaces.md#LO-IMPORT)

    [33.3.3. 匯出大型物件](lo-interfaces.md#LO-EXPORT)

    [33.3.4. 開啟既有的大型物件](lo-interfaces.md#LO-OPEN)

    [33.3.5. 將資料寫入大型物件](lo-interfaces.md#LO-WRITE)

    [33.3.6. 從大型物件讀取資料](lo-interfaces.md#LO-READ)

    [33.3.7. 在大型物件中移動位置](lo-interfaces.md#LO-SEEK)

    [33.3.8. 取得大型物件的目前位置](lo-interfaces.md#LO-TELL)

    [33.3.9. 截斷大型物件](lo-interfaces.md#LO-TRUNCATE)

    [33.3.10. 關閉大型物件描述子](lo-interfaces.md#LO-CLOSE)

    [33.3.11. 移除大型物件](lo-interfaces.md#LO-UNLINK)

[33.4. 伺服器端函式](lo-funcs.md)

[33.5. 範例程式](lo-examplesect.md)

<a id="id-1.7.4.2"></a><a id="id-1.7.4.3"></a>

PostgreSQL 具有*大型物件*
功能，可對儲存在特殊大型物件結構中的使用者資料，
提供串流式的存取。當處理的資料值太大、
不便以整體方式操作時，串流存取就很有用。

本章說明 PostgreSQL 大型物件資料的實作，
以及其程式設計與查詢語言介面。本章的範例使用
libpq C 函式庫，但大多數
PostgreSQL 原生的程式設計介面都支援
同等的功能。其他介面可能會在內部使用大型
物件介面，以提供對大型值的通用支援。
這部分不在此說明。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/largeobjects.html)（原文版本：18.6；核對日期：2026-10-18）
