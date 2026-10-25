<a id="FDW-FUNCTIONS"></a>

## 58.1. 外部資料包裝器函式 [#](#fdw-functions) <a href="#fdw-functions" id="fdw-functions"></a>

FDW 作者需要實作一個處理函式，並可選擇實作一個驗證函式。這兩個函式都必須以 C 之類的編譯式語言撰寫，並使用版本 1 介面。關於 C 語言呼叫慣例與動態載入的詳細資訊，請參閱[第 36.10 節](../../server-programming/extend/xfunc-c.md)。

處理函式只是回傳一個結構，其中包含指向各個回呼函式的函式指標；這些回呼函式會由規劃器、執行器以及各種維護命令呼叫。撰寫 FDW 的大部分工作都在於實作這些回呼函式。處理函式必須在 PostgreSQL 中註冊為不接受任何引數，並回傳特殊虛擬型別 `fdw_handler`。回呼函式是一般的 C 函式，在 SQL 層級既看不到，也無法呼叫。回呼函式的說明請參閱[第 58.2 節](fdw-callbacks.md)。

驗證函式負責驗證在 `CREATE` 與 `ALTER` 命令中，為其外部資料包裝器，以及使用該包裝器的外部伺服器、使用者對應和外部資料表所給定的選項。驗證函式必須註冊為接受兩個引數：一個包含待驗證選項的 text 陣列，以及一個代表這些選項所屬物件類型的 OID。後者對應於該物件所會儲存於其中的系統目錄的 OID，為下列之一：

* `AttributeRelationId`
* `ForeignDataWrapperRelationId`
* `ForeignServerRelationId`
* `ForeignTableRelationId`
* `UserMappingRelationId`

若未提供驗證函式，則在建立物件或修改物件時都不會檢查選項。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fdw-functions.html)（原文版本：18.6；核對日期：2026-10-17）
