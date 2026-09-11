## F.21. lo — 管理大型物件 [#](#LO)

[F.21.1. 原理](lo.md#LO-RATIONALE)

[F.21.2. 使用方式](lo.md#LO-HOW-TO-USE)

[F.21.3. 限制](lo.md#LO-LIMITATIONS)

[F.21.4. 作者](lo.md#LO-AUTHOR)

<a id="id-1.11.7.31.2"></a>

`lo` 模組支援管理大型物件（Large Objects，也稱為 LO 或 BLOB）。它包含資料型別 `lo` 與觸發程序 `lo_manage`。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="LO-RATIONALE"></a>

### F.21.1. 原理 [#](#LO-RATIONALE)

JDBC 驅動程式的一項問題（也會影響 ODBC 驅動程式）是，規範假定 BLOB（Binary Large OBject，大型二進位物件）的參照儲存在資料表中，且若該項目變更，關聯的 BLOB 會從資料庫刪除。

在 PostgreSQL 中，這不會發生。大型物件會被視為獨立物件；一個資料表項目可透過 OID 參照大型物件，但可能有多個資料表項目參照相同大型物件 OID，因此系統不會僅因變更或移除其中一個項目就刪除大型物件。

這對 PostgreSQL 專用應用程式沒有問題，但使用 JDBC 或 ODBC 的標準程式碼不會刪除這些物件，因而產生孤立物件——未被任何項目參照、只占用磁碟空間的物件。

`lo` 模組可透過將觸發程序附加到含有 LO 參照欄位的資料表來解決此問題。每當刪除或修改參照大型物件的值時，觸發程序實質上只會執行 `lo_unlink`。使用此觸發程序時，您假定觸發程序控制欄位所參照的每個大型物件僅有一個資料庫參照！

此模組也提供資料型別 `lo`，它實際上只是 `oid` 型別上的[網域](../glossary/README.md#GLOSSARY-DOMAIN)。這有助於區分持有大型物件參照的資料庫欄位與持有其他物件 OID 的欄位。使用觸發程序不必使用 `lo` 型別，但用它來追蹤資料庫中哪些欄位表示由觸發程序管理的大型物件可能較方便。據說若未對 BLOB 欄位使用 `lo`，ODBC 驅動程式也會發生混淆。

<a id="LO-HOW-TO-USE"></a>

### F.21.2. 使用方式 [#](#LO-HOW-TO-USE)

以下是簡單的使用範例：

```

CREATE TABLE image (title text, raster lo);

CREATE TRIGGER t_raster BEFORE UPDATE OR DELETE ON image
    FOR EACH ROW EXECUTE FUNCTION lo_manage(raster);
```

對每個將包含大型物件唯一參照的欄位，建立一個 `BEFORE UPDATE OR DELETE` 觸發程序，並將欄位名稱作為唯一的觸發程序引數。也可使用 `BEFORE UPDATE OF` *`column_name`*，限制觸發程序僅在更新該欄位時執行。若同一資料表需要多個 `lo` 欄位，請為每個欄位建立個別觸發程序，並記得為同一資料表上的每個觸發程序指定不同名稱。

<a id="LO-LIMITATIONS"></a>

### F.21.3. 限制 [#](#LO-LIMITATIONS)

* 捨棄資料表時，由於不會執行觸發程序，其中包含的物件仍會成為孤立物件。可在 `DROP TABLE` 前執行 `DELETE FROM table` 避免此情況。

  `TRUNCATE` 也有相同的風險。

  若已有或懷疑有孤立大型物件，請參閱 [vacuumlo](../contrib-prog/vacuumlo.md) 模組以協助清理。偶爾執行 vacuumlo 作為 `lo_manage` 觸發程序的後備措施是個好主意。
* 某些前端可能會建立自己的資料表，卻不會建立關聯的觸發程序。此外，使用者可能不記得（或不知道）要建立觸發程序。

<a id="LO-AUTHOR"></a>

### F.21.4. 作者 [#](#LO-AUTHOR)

Peter Mount `<peter@retep.org.uk>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/lo.html)
