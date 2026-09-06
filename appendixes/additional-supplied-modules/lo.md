<a id="LO"></a>

# F.22. lo

[F.22.1. 原理](#id-1.11.7.31.5)

[F.22.2. 使用方式](#id-1.11.7.31.6)

[F.22.3. 限制](#id-1.11.7.31.7)

[F.22.4. 作者](#id-1.11.7.31.8)

<a id="id-1.11.7.31.2"></a>

`lo` 模組提供管理大型物件（Large Objects，也稱為 LO 或 BLOB）的支援，其中包含 `lo` 資料型別與 `lo_manage` 觸發器。

此模組屬於「可信任」模組；只要對目前資料庫具有 `CREATE` 權限，非超級使用者也能安裝它。

<a id="id-1.11.7.31.5"></a>

## F.22.1. 原理

JDBC 驅動程式的一項問題（ODBC 驅動程式也受到影響）是，其規格假設 BLOB（Binary Large Objects）參照會儲存在資料表內，且該資料列變更時，關聯的 BLOB 會從資料庫刪除。

PostgreSQL 的行為不是如此。大型物件被視為獨立物件；資料表中的資料列可以透過 OID 參照大型物件，但多個資料列可能參照相同的大型物件 OID。因此，系統不會只因為變更或移除其中一個資料列，就刪除該大型物件。

這對 PostgreSQL 專用的應用程式沒有問題，但使用 JDBC 或 ODBC 的標準程式碼不會刪除這些物件，因而形成孤立物件：它們沒有被任何資料參照，卻仍佔用磁碟空間。

`lo` 模組可藉由在含有 LO 參照欄位的資料表上附加觸發器來解決此問題。每當刪除或修改參照大型物件的值，觸發器基本上會執行 `lo_unlink`。使用此觸發器時，必須假定由觸發器控制的欄位中，每個被參照的大型物件只有一個資料庫參照！

此模組也提供 `lo` 資料型別；它實際上是 `oid` 型別上的 [domain](../glossary.md#GLOSSARY-DOMAIN)。這有助於區分保存大型物件參照的資料庫欄位，以及保存其他物件 OID 的欄位。使用觸發器不一定要使用 `lo` 型別，但它有助於識別資料庫中由此觸發器管理的大型物件欄位。據說 ODBC 驅動程式在 BLOB 欄位未使用 `lo` 型別時也可能發生問題。

<a id="id-1.11.7.31.6"></a>

## F.22.2. 使用方式

以下是簡單的使用範例：

```

CREATE TABLE image (title text, raster lo);

CREATE TRIGGER t_raster BEFORE UPDATE OR DELETE ON image
    FOR EACH ROW EXECUTE FUNCTION lo_manage(raster);
```

對每個將保存大型物件唯一參照的欄位，建立 `BEFORE UPDATE OR DELETE` 觸發器，並將欄位名稱作為唯一的觸發器引數。你也可以使用 `BEFORE UPDATE OF` <em class="replaceable"><code>column&#95;name</code></em>，限制觸發器只在更新該欄位時執行。同一資料表若需要多個 `lo` 欄位，請為每一個欄位建立獨立觸發器，並為同一資料表上的每個觸發器使用不同名稱。

<a id="id-1.11.7.31.7"></a>

## F.22.3. 限制

* 刪除資料表時不會執行觸發器，該資料表中的物件仍會成為孤立物件。你可以在 `DROP TABLE` 前先執行 <code class="command">DELETE FROM <em class="replaceable"><code>table</code></em></code> 來避免此情況。

  `TRUNCATE` 也有相同風險。

  若已有或懷疑有孤立的大型物件，請參閱 [vacuumlo](../additional-supplied-programs/client-applications/vacuumlo.md) 模組以協助清理。定期執行 vacuumlo，作為 `lo_manage` 觸發器的補強措施，是個好做法。
* 某些前端程式可能自行建立資料表，卻不會建立關聯觸發器。此外，使用者也可能忘記（或不知道）要建立觸發器。

<a id="id-1.11.7.31.8"></a>

## F.22.4. 作者

Peter Mount <code class="email">&lt;<a class="email" href="mailto:peter@retep.org.uk">peter@retep.org.uk</a>&gt;</code>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/lo.html)
