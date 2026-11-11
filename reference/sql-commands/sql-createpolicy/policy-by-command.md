# 各命令的政策

<a id="id-1.9.3.75.6.3"></a>

## 各命令的政策 [#](#ge-ming-ling-de-zheng-ce) <a href="#ge-ming-ling-de-zheng-ce" id="ge-ming-ling-de-zheng-ce"></a>

<a id="SQL-CREATEPOLICY-ALL"></a>

`ALL` [#](#SQL-CREATEPOLICY-ALL)

政策使用 `ALL` 表示它會套用於所有命令，不論命令的類型為何。若同時存在 `ALL` 政策與更具體的政策，則 `ALL` 政策與更具體的政策（一個或多個）都會被套用。此外，`ALL` 政策會同時套用於查詢的選取端與修改端；若只定義了 `USING` 運算式，則兩種情況都會使用該 `USING` 運算式。

舉例來說，若執行 `UPDATE`，則 `ALL` 政策既適用於 `UPDATE` 能夠選取作為待更新資料列的對象（套用 `USING` 運算式），也適用於更新後產生的資料列，以檢查它們是否允許被加入資料表（若有定義 `WITH CHECK` 運算式就套用它，否則套用 `USING` 運算式）。若 `INSERT` 或 `UPDATE` 命令嘗試加入資料表的資料列未通過 `ALL` 政策的 `WITH CHECK` 運算式（若該政策沒有 `WITH CHECK` 運算式，則為其 `USING` 運算式），整個命令將會中止。
<a id="SQL-CREATEPOLICY-SELECT"></a>

`SELECT` [#](#SQL-CREATEPOLICY-SELECT)

政策使用 `SELECT` 表示它會套用於 `SELECT` 查詢，以及每當需要對定義該政策的關聯具有 `SELECT` 權限的情況。其結果是，在 `SELECT` 查詢期間只會傳回該關聯中通過 `SELECT` 政策的紀錄；而需要 `SELECT` 權限的查詢，例如 `UPDATE`、`DELETE` 與 `MERGE`，同樣也只會看到 `SELECT` 政策所允許的紀錄。`SELECT` 政策不能有 `WITH
CHECK` 運算式，因為它只適用於從關聯中擷取紀錄的情況，下文所述的情況除外。

若資料修改查詢帶有 `RETURNING` 子句，則需要對該關聯具有 `SELECT` 權限，而且該關聯中任何新插入或更新的資料列，都必須滿足該關聯的 `SELECT` 政策，才能提供給 `RETURNING` 子句使用。若新插入或更新的資料列不滿足該關聯的 `SELECT` 政策，就會擲出錯誤（要傳回的已插入或已更新資料列*絕不會*被靜默地忽略）。

若 `INSERT` 帶有 `ON CONFLICT DO
UPDATE` 子句，或帶有指定了仲裁索引或限制條件的 `ON CONFLICT DO
NOTHING` 子句，則需要對該關聯具有 `SELECT` 權限，而且擬議插入的資料列會使用該關聯的 `SELECT` 政策進行檢查。若擬議插入的資料列不滿足該關聯的 `SELECT` 政策，就會擲出錯誤（`INSERT` *絕不會*被靜默地略過）。此外，若走的是 `UPDATE` 路徑，待更新的資料列與更新後的新資料列都會依據該關聯的 `SELECT` 政策進行檢查，若不滿足就會擲出錯誤（輔助的 `UPDATE` *絕不會*被靜默地略過）。

`MERGE` 命令需要對來源關聯與目標關聯都具有 `SELECT` 權限，因此每個關聯的 `SELECT` 政策都會在它們被連接之前套用，而 `MERGE` 動作只會看到這些政策所允許的紀錄。此外，若執行了 `UPDATE` 動作，目標關聯的 `SELECT` 政策會套用到更新後的資料列，與獨立的 `UPDATE` 相同，差別在於若不滿足這些政策就會擲出錯誤。
<a id="SQL-CREATEPOLICY-INSERT"></a>

`INSERT` [#](#SQL-CREATEPOLICY-INSERT)

政策使用 `INSERT` 表示它會套用於 `INSERT` 命令，以及包含 `INSERT` 動作的 `MERGE` 命令。被插入的資料列若未通過此政策，就會導致政策違規錯誤，且整個 `INSERT` 命令將會中止。`INSERT` 政策不能有 `USING` 運算式，因為它只適用於將紀錄加入關聯的情況。

請注意，帶有 `ON CONFLICT
DO NOTHING/UPDATE` 子句的 `INSERT`，會針對所有擬議插入的資料列檢查 `INSERT` 政策的 `WITH CHECK` 運算式，不論這些資料列最終是否被插入。
<a id="SQL-CREATEPOLICY-UPDATE"></a>

`UPDATE` [#](#SQL-CREATEPOLICY-UPDATE)

政策使用 `UPDATE` 表示它會套用於 `UPDATE`、`SELECT FOR UPDATE` 與 `SELECT FOR SHARE` 命令，以及 `INSERT` 命令的輔助 `ON CONFLICT DO UPDATE` 子句，還有包含 `UPDATE` 動作的 `MERGE` 命令。由於 `UPDATE` 命令涉及取出一筆現有紀錄，並以一筆經修改的新紀錄取代它，因此 `UPDATE` 政策同時接受 `USING` 運算式與 `WITH CHECK` 運算式。`USING` 運算式決定 `UPDATE` 命令會看到哪些紀錄來進行操作，而 `WITH CHECK` 運算式則定義哪些經修改的資料列允許被存回該關聯。

任何更新後的值未通過 `WITH CHECK` 運算式的資料列都會導致錯誤，且整個命令將會中止。若只指定了 `USING` 子句，則該子句會同時用於 `USING` 與 `WITH CHECK` 兩種情況。

`UPDATE` 命令通常也需要從被更新之關聯的欄位讀取資料（例如在 `WHERE` 子句或 `RETURNING` 子句中，或在 `SET` 子句右側的運算式中）。在這種情況下，也需要對被更新的關聯具有 `SELECT` 權限，而且除了 `UPDATE` 政策之外，還會套用適當的 `SELECT` 或 `ALL` 政策。因此，使用者除了必須透過 `UPDATE` 或 `ALL` 政策獲得更新資料列的許可之外，還必須能透過 `SELECT` 或 `ALL` 政策存取被更新的資料列。

當 `INSERT` 命令帶有輔助的 `ON CONFLICT DO UPDATE` 子句時，若走的是 `UPDATE` 路徑，待更新的資料列會先依據任何 `UPDATE` 政策的 `USING` 運算式進行檢查，接著更新後的新資料列再依據 `WITH CHECK` 運算式進行檢查。不過請注意，與獨立的 `UPDATE` 命令不同，若現有資料列未通過 `USING` 運算式，就會擲出錯誤（`UPDATE` 路徑*絕不會*被靜默地略過）。這同樣適用於 `MERGE` 命令的 `UPDATE` 動作。
<a id="SQL-CREATEPOLICY-DELETE"></a>

`DELETE` [#](#SQL-CREATEPOLICY-DELETE)

政策使用 `DELETE` 表示它會套用於 `DELETE` 命令，以及包含 `DELETE` 動作的 `MERGE` 命令。對於 `DELETE` 命令，只有通過此政策的資料列才會被 `DELETE` 命令看到。可能有些資料列透過 `SELECT` 政策可見，卻因為未通過 `DELETE` 政策的 `USING` 運算式而無法被刪除。不過請注意，`MERGE` 命令中的 `DELETE` 動作會看到透過 `SELECT` 政策可見的資料列，若這類資料列未通過 `DELETE` 政策，就會擲出錯誤。

在大多數情況下，`DELETE` 命令也需要從其正在刪除資料的關聯中讀取欄位資料（例如在 `WHERE` 子句或 `RETURNING` 子句中）。在這種情況下，也需要對該關聯具有 `SELECT` 權限，而且除了 `DELETE` 政策之外，還會套用適當的 `SELECT` 或 `ALL` 政策。因此，使用者除了必須透過 `DELETE` 或 `ALL` 政策獲得刪除資料列的許可之外，還必須能透過 `SELECT` 或 `ALL` 政策存取被刪除的資料列。

`DELETE` 政策不能有 `WITH
CHECK` 運算式，因為它只適用於從關聯中刪除紀錄的情況，因此沒有需要檢查的新資料列。

[表 300](#sql-createpolicy-summary) 彙整了不同類型的政策如何套用於特定命令。在表中，「檢查」表示會檢查政策運算式，若其傳回 false 或 null 就擲出錯誤；而「篩選」則表示若政策運算式傳回 false 或 null，該資料列會被靜默地忽略。

<a id="SQL-CREATEPOLICY-SUMMARY"></a>

### 表 300. 依命令類型套用的政策 [#](#sql-createpolicy-summary) <a href="#sql-createpolicy-summary" id="sql-createpolicy-summary"></a>

下表表頭中的 policy 指「政策」（例如 SELECT/ALL policy 指命令類型為 SELECT 的政策或命令類型為 ALL 的政策），USING expression 與 WITH CHECK expression 分別指「USING 運算式」與「WITH CHECK 運算式」。

<table border="1" class="table" summary="依命令類型套用的政策"><colgroup><col/><col/><col/><col class="update-using"/><col class="update-check"/><col/></colgroup><thead><tr><th rowspan="2">命令</th><th><code class="literal">SELECT/ALL policy</code></th><th><code class="literal">INSERT/ALL policy</code></th><th colspan="2"><code class="literal">UPDATE/ALL policy</code></th><th><code class="literal">DELETE/ALL policy</code></th></tr><tr><th><code class="literal">USING expression</code></th><th><code class="literal">WITH CHECK expression</code></th><th><code class="literal">USING expression</code></th><th><code class="literal">WITH CHECK expression</code></th><th><code class="literal">USING expression</code></th></tr></thead><tbody><tr><td><code class="command">SELECT</code> / <code class="command">COPY ... TO</code></td><td>篩選現有資料列</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td><code class="command">SELECT FOR UPDATE/SHARE</code></td><td>篩選現有資料列</td><td>—</td><td>篩選現有資料列</td><td>—</td><td>—</td></tr><tr><td><code class="command">INSERT</code></td><td>
        檢查新資料列 <a class="footnote" href="#ftn.RLS-SELECT-PRIV"><sup class="footnote" id="RLS-SELECT-PRIV">[a]</sup></a>
</td><td>檢查新資料列</td><td>—</td><td>—</td><td>—</td></tr><tr><td><code class="command">UPDATE</code></td><td>
        篩選現有資料列 <a class="footnoteref" href="#ftn.RLS-SELECT-PRIV"><sup class="footnoteref">[a]</sup></a> 並
        檢查新資料列 <a class="footnoteref" href="#ftn.RLS-SELECT-PRIV"><sup class="footnoteref">[a]</sup></a>
</td><td>—</td><td>篩選現有資料列</td><td>檢查新資料列</td><td>—</td></tr><tr><td><code class="command">DELETE</code></td><td>
        篩選現有資料列 <a class="footnoteref" href="#ftn.RLS-SELECT-PRIV"><sup class="footnoteref">[a]</sup></a>
</td><td>—</td><td>—</td><td>—</td><td>篩選現有資料列</td></tr><tr><td><code class="command">INSERT ... ON CONFLICT</code></td><td>
        檢查新資料列 <a class="footnote" href="#ftn.id-1.9.3.75.6.3.4.2.5.6.2.1"><sup class="footnote" id="id-1.9.3.75.6.3.4.2.5.6.2.1">[b]</sup></a><a class="footnote" href="#ftn.RLS-ON-CONFLICT-PRIV"><sup class="footnote" id="RLS-ON-CONFLICT-PRIV">[c]</sup></a>
</td><td>
        檢查新資料列 <a class="footnoteref" href="#ftn.RLS-ON-CONFLICT-PRIV"><sup class="footnoteref">[c]</sup></a>
</td><td>—</td><td>—</td><td>—</td></tr><tr><td><code class="command">ON CONFLICT DO UPDATE</code></td><td>
        檢查現有資料列與新資料列 <a class="footnote" href="#ftn.RLS-ON-CONFLICT-UPDATE-PRIV"><sup class="footnote" id="RLS-ON-CONFLICT-UPDATE-PRIV">[d]</sup></a>
</td><td>—</td><td>檢查現有資料列</td><td>
        檢查新資料列 <a class="footnoteref" href="#ftn.RLS-ON-CONFLICT-UPDATE-PRIV"><sup class="footnoteref">[d]</sup></a>
</td><td>—</td></tr><tr><td><code class="command">MERGE</code></td><td>篩選來源與目標資料列</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td><code class="command">MERGE ... THEN INSERT</code></td><td>
        檢查新資料列 <a class="footnoteref" href="#ftn.RLS-SELECT-PRIV"><sup class="footnoteref">[a]</sup></a>
</td><td>檢查新資料列</td><td>—</td><td>—</td><td>—</td></tr><tr><td><code class="command">MERGE ... THEN UPDATE</code></td><td>檢查新資料列</td><td>—</td><td>檢查現有資料列</td><td>檢查新資料列</td><td>—</td></tr><tr><td><code class="command">MERGE ... THEN DELETE</code></td><td>—</td><td>—</td><td>—</td><td>—</td><td>檢查現有資料列</td></tr></tbody><tbody class="footnotes"><tr><td colspan="6"><div class="footnote" id="ftn.RLS-SELECT-PRIV"><p><a class="para" href="#RLS-SELECT-PRIV"><sup class="para">[a] </sup></a>
          若需要讀取現有資料列或新資料列（例如，參照該關聯欄位的 <code class="literal">WHERE</code> 或 <code class="literal">RETURNING</code>
          子句）。
         </p></div><div class="footnote" id="ftn.id-1.9.3.75.6.3.4.2.5.6.2.1"><p><a class="para" href="#id-1.9.3.75.6.3.4.2.5.6.2.1"><sup class="para">[b] </sup></a>
          若指定了仲裁索引或限制條件。
         </p></div><div class="footnote" id="ftn.RLS-ON-CONFLICT-PRIV"><p><a class="para" href="#RLS-ON-CONFLICT-PRIV"><sup class="para">[c] </sup></a>
          無論是否發生衝突，擬議插入的資料列都會被檢查。
         </p></div><div class="footnote" id="ftn.RLS-ON-CONFLICT-UPDATE-PRIV"><p><a class="para" href="#RLS-ON-CONFLICT-UPDATE-PRIV"><sup class="para">[d] </sup></a>
          輔助 <code class="command">UPDATE</code> 命令的新資料列，可能與原始
          <code class="command">INSERT</code> 命令的新資料列不同。
         </p></div></td></tr></tbody></table>

<br>

[返回參數](../sql-createpolicy.md#can-shu)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createpolicy.html)（原文版本：18.6；核對日期：2026-10-05）
