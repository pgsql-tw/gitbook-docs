# 51.26 pg\_index

目錄 pg\_index 包含有關索引的部分信息。其餘的大多數是在 pg\_class 中。

**Table 51.26. `pg_index` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `indexrelid` | `oid` | \`\`[`pg_class`](pg_class.md).oid | 此索引在 pg\_class 中的 OID |
| `indrelid` | `oid` | \`\`[`pg_class`](pg_class.md).oid | 此索引對應資料表在 pg\_class 中的 OID |
| `indnatts` | `int2` |  | 索引中的欄位數（複製自 pg\_class.relnatts） |
| `indisunique` | `bool` |  | 如果為 true，則這是唯一性索引 |
| `indisprimary` | `bool` |  | 如果為 true，則此索引表示資料表的主鍵（如果為 true，則 indisunique 應始終為true） |
| `indisexclusion` | `bool` |  | 如果為 true，則此索引支援排除限制條件 |
| `indimmediate` | `bool` |  | 如果為 true，則在插入時立即強制執行唯一性檢查（如果 indisunique 不成立則無關緊要） |
| `indisclustered` | `bool` |  | If true, the table was last clustered on this index |
| `indisvalid` | `bool` |  | 如果為 true，則索引目前對查詢有效。False 意味著索引可能不完整：它仍然必須通過 INSERT / UPDATE 操作進行修改，但它不能安全地用於查詢。 如果它是唯一的，則唯一性屬性也不保證是真的。 |
| `indcheckxmin` | `bool` |  | 如果為 true，則查詢必須不使用索引，直到此 pg\_index 資料列的 xmin 低於其 TransactionXmin 事務範圍，因為可以看到該資料表可能包含具有不相容資料列的損壞 HOT 鏈 |
| `indisready` | `bool` |  | 如果為 true，則索引目前已準備好進行插入。False 表示 INSERT / UPDATE 操作必須忽略索引。 |
| `indislive` | `bool` |  | 如果為 false，則索引正在被移除，並且應該被忽略用於所有目的（包括 HOT-safety 決策） |
| `indisreplident` | `bool` |  | If true this index 已使用 ALTER TABLE ... REPLICA IDENTITY 選擇“replica identity”... |
| `indkey` | `int2vector` | \`\`[`pg_attribute`](pg_attribute.md).attnum | 這是一個 indnatts 陣列，意指此索引所索引的資料表欄位。例如，值為 1 3 意味著第一個和第三個資料表欄位構成索引鍵。此陣列中的零表示相應的索引屬性是資料表欄位上的表示式，而不是簡單的欄位引用。 |
| `indcollation` | `oidvector` | \`\`[`pg_collation`](pg_collation.md).oid | 對於索引鍵中的每一個欄位，它包含用於索引的排序規則的 OID，如果該欄位不是可合併的資料型別，則為零。 |
| `indclass` | `oidvector` | \`\`[`pg_opclass`](pg_opclass.md).oid | 對於索引鍵中的每一欄位，它包含要使用的運算子類的 OID。有關詳細訊息，請參閱 [pg\_opclass](pg_opclass.md)。 |
| `indoption` | `int2vector` |  | 這是一個 indnatts 陣列，用於儲存每個欄位的旗標位元。位元的意義由索引的存取方法定義。 |
| `indexprs` | `pg_node_tree` |  | 表示式樹（以 nodeToString\(\) 表示），用於不是簡單欄位引用的索引屬性。這是一個列表，其中包含 indkey 中每個零項目的一個元素。如果所有索引屬性都是簡單引用，則為空。 |
| `indpred` | `pg_node_tree` |  | 部分索引條件的表示式樹（以 nodeToString\(\) 表示）。如果不是部分索引，則為空。 |

