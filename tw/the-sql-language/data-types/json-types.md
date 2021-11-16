# 8.14. JSON 型別

JSON 資料型別用於儲存 [RFC 7159](https://tools.ietf.org/html/rfc7159) 中所規範的 JSON（JavaScript Object Notation）資料。此類資料也可以儲存為 text，但是 JSON 資料型別的優點是可以根據 JSON 規則強制讓每個儲存的值必須是有效的值 。對於這些資料型別中儲存的資料，還提供了各種特定於 JSON 的函數和運算子。 另請參閱[第 9.15 節](../functions-and-operators/json-functions-and-operators.md)。

PostgreSQL 提供了兩種儲存 JSON 資料的型別：json 和 jsonb。為了對這些資料型別實作有效的查詢機制，PostgreSQL 還提供了 [8.14.6 節](json-types.md#8-14-6-jsonpath-type)中所描述的 jsonpath 資料型別。

json 和 jsonb 資料型別接受幾乎相同的內容集合作為輸入。實際主要的差別是效率。json 資料型別儲存與輸入字串完全相同的內容，處理函數必須在每次執行時重新解析；jsonb 資料型別則以分解後的二進位格式儲存，由於增加了轉換成本，因此資料輸入的速度稍慢，但由於後續不需要解析，因此處理速度明顯加快。jsonb 還支援索引處理，這是一個很大的優勢。

因為 json 型別儲存與輸入字串完全相同的內容，所以它將保留標記之間語義上無關的空白以及 JSON 物件中鍵的順序。另外，如果 JSON 內容物件包含相同的鍵不只一次，則所有鍵/值對都會保留。（處理函數會將最後一個值視為可用的值。）相比之下，jsonb 不會保留空白，不會保留物件中鍵的順序，也不會保留物件中重複的鍵。如果在輸入中指定了重複的鍵，則僅保留最後一個值。

通常，大多數應用程序應該將 JSON 資料儲存為 jsonb，除非有非常特殊的需求，例如關於物件中鍵的順序有一些傳統上的假設。

由於 PostgreSQL 每個資料庫只允許一種字元集的編碼。因此，除非資料庫編碼為 UTF8，否則 JSON 型別不可能嚴格符合 JSON 規範。嘗試直接使用資料庫編碼中無法表示的字元會失敗；相反，character 型別則允許使用可以在資料庫編碼中表示但不能以 UTF8 表示的字元。

RFC 7159 允許 JSON 字串包含 \uXXXX 所表示的 Unicode 轉譯序列。在 json 型別的輸入函數中，無論資料庫編碼如何，都允許 Unicode 轉譯，並且僅檢查語法正確性（即，四個十六進位數字跟在 \u 之後）。但是，jsonb 的輸入函數更嚴格：除非資料庫編碼為 UTF8，否則它不允許非 ASCII 字元（U+007F 以上的字元）使用 Unicode 轉譯。jsonb 型別也拒絕 \u0000（因為無法在 PostgreSQL 的 text 型別中表現），並且堅持認為使用 Unicode surrogate pair 對來指定 Unicode Basic Multilingual Plane 之外的字元都是正確的。有效的 Unicode 轉譯會轉換為等效的 ASCII 或 UTF8 字元進行儲存； 這包括將 surrogate pair 折疊為單個字元。

{% hint style="info" %}
第 9.15 節中描述的許多 JSON 處理函數會將 Unicode 轉譯為一般字元，因此，即使輸入型別為 json 而不是 jsonb，它們也會拋出與上述類型相同的錯誤。json 輸入函數不進行這些檢查的事實可能被認為是歷史共業，儘管它確實允許以非 UTF8 資料庫編碼的形式簡單儲存（毋須處理）JSON Unicode 轉譯。 通常，如果可以的話，最好避免將 JSON 中的 Unicode 轉譯與非 UTF8 資料庫編碼混在一起。
{% endhint %}

將字串 JSON 輸入轉換為 jsonb 時，RFC 7159 描述的原始型別將會有效地對應到內建的 PostgreSQL 型別，如 Table 8.23 所示。因此，對於構成有效 jsonb 資料的內容存在一些較小的附加約束條件，這些約束條件既不適用於 json 型別，也不適用於抽象上 JSON，這對應於基礎資料型別可以表示的內容限制。值得注意的是，jsonb 會拒絕 PostgreSQL 數字資料型別範圍之外的數字，而 json 不會。RFC 7159 允許此類實作定義限制。但是，實際上，在其他實作中更容易出現此類問題，因為通常將 JSON 的數字基本型別表示為 IEEE 754 雙精確度浮點數（RFC 7159 明確預期了這一點且允許）。當使用 JSON 作為此類系統的交換格式時，應考慮與 PostgreSQL 最初儲存的資料相比較，可能會有失去數字精確度的風險。

相反，如下表中所示，JSON 基本型別的輸入格式有一些微小的限制，但並不適用於其相應的 PostgreSQL 資料型別。

#### **Table 8.23. JSON Primitive Types and Corresponding PostgreSQL Types**

| JSON primitive type | PostgreSQL type | Notes                                               |
| ------------------- | --------------- | --------------------------------------------------- |
| `string`            | `text`          | 禁止使用 \u0000，如果資料庫編碼不是 UTF8，則不允許使用非 ASCII Unicode 轉譯 |
| `number`            | `numeric`       | 不允許使用 NaN 和 infinity                                |
| `boolean`           | `boolean`       | 僅接受小寫的 true 和 false                                 |
| `null`              | (none)          | 與 SQL NULL 是不同的概念                                   |

## 8.14.1. JSON 輸入與輸出語法

JSON 資料型別的輸入/輸出語法被規範在 RFC 7159 之中。

以下是所有有效的 json（或 jsonb）表示式：

```
-- Simple scalar/primitive value
-- Primitive values can be numbers, quoted strings, true, false, or null
SELECT '5'::json;

-- Array of zero or more elements (elements need not be of same type)
SELECT '[1, 2, "foo", null]'::json;

-- Object containing pairs of keys and values
-- Note that object keys must always be quoted strings
SELECT '{"bar": "baz", "balance": 7.77, "active": false}'::json;

-- Arrays and objects can be nested arbitrarily
SELECT '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json;
```

如前所述，當輸入 JSON 內容然後在不進行任何其他處理的情況下進行輸出時，json 輸出與輸入相同的內容，而 jsonb 則不會保留與語義無關的細節，像是空格。例如，請注意此處的差別：

```
SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::json;
                      json                       
-------------------------------------------------
 {"bar": "baz", "balance": 7.77, "active":false}
(1 row)

SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::jsonb;
                      jsonb                       
--------------------------------------------------
 {"bar": "baz", "active": false, "balance": 7.77}
(1 row)
```

值得注意的一個語義無關的細節是，在 jsonb 中，數字將根據基本數字型別的行為進行輸出。實際上，這意味著使用 E 記號輸入的數字將不會以原輸出形式輸出，例如：

```
SELECT '{"reading": 1.230e-5}'::json, '{"reading": 1.230e-5}'::jsonb;
         json          |          jsonb          
-----------------------+-------------------------
 {"reading": 1.230e-5} | {"reading": 0.00001230}
(1 row)
```

但是，jsonb 將保留小數尾巴的數字零，如在本範例中所示，即使它們在語義上無意義（例如，相等運算），也是如此。

有關可用於建構和處理 JSON 內容的內建函數和運算子的列表，請參閱[第 9.15 節](../functions-and-operators/json-functions-and-operators.md)。

## 8.14.2. 設計 JSON 文件結構

將資料表示為 JSON 可以比傳統的關連資料模型要靈活得多，而傳統的關連資料模型在需求多變的環境中非常引人注目。這兩種方法很可能在同一應用程序中共存和互補。但是，即使對於需要最大靈活性的應用程序，仍然建議 JSON 文件具有某種固定的結構。該結構通常是不具有強制性的（儘管可以宣告強制執行某些業務規則），但是具有可預測的結構可以使撰編查詢變得更加容易，該查詢可以有效地彙總資料表中的一組「文件」（datums）。

JSON 資料儲存在資料表中時，與其他任何資料型別一樣，要遵循相同的一致性控制事項。儘管儲存大型文件是可行的，但請記住，任何更新都會取得整筆資料的 row-level lock。考慮將 JSON 文件限制在可管理的大小以內，以減少更新交易事務之間的鎖定競爭。理想情況下，每個 JSON 文件都應代表一個完整交易單位資料(atomic datum)，業務規則規定不能將該完整交易單位資料進一步細分為可以獨立更新的較小單位資料。

## 8.14.3. `jsonb` Containment and Existence

測試包容性(containment)是 jsonb 的一項重要功能。json 型別沒有平行處理的工具集。包含性測試一個 jsonb 文件是否在其中包含另一個。除說明以外的部份，這些範例會回傳 true：

```
-- Simple scalar/primitive values contain only the identical value:
SELECT '"foo"'::jsonb @> '"foo"'::jsonb;

-- The array on the right side is contained within the one on the left:
SELECT '[1, 2, 3]'::jsonb @> '[1, 3]'::jsonb;

-- Order of array elements is not significant, so this is also true:
SELECT '[1, 2, 3]'::jsonb @> '[3, 1]'::jsonb;

-- Duplicate array elements don't matter either:
SELECT '[1, 2, 3]'::jsonb @> '[1, 2, 2]'::jsonb;

-- The object with a single pair on the right side is contained
-- within the object on the left side:
SELECT '{"product": "PostgreSQL", "version": 9.4, "jsonb": true}'::jsonb @> '{"version": 9.4}'::jsonb;

-- The array on the right side is not considered contained within the
-- array on the left, even though a similar array is nested within it:
SELECT '[1, 2, [1, 3]]'::jsonb @> '[1, 3]'::jsonb;  -- yields false

-- But with a layer of nesting, it is contained:
SELECT '[1, 2, [1, 3]]'::jsonb @> '[[1, 3]]'::jsonb;

-- Similarly, containment is not reported here:
SELECT '{"foo": {"bar": "baz"}}'::jsonb @> '{"bar": "baz"}'::jsonb;  -- yields false

-- A top-level key and an empty object is contained:
SELECT '{"foo": {"bar": "baz"}}'::jsonb @> '{"foo": {}}'::jsonb;
```

一般原則是，包含物件必須在結構和資料內容上與包含的物件相吻合，可能是在從包含的物件中丟棄了一些不吻合的陣列元素或物件鍵/值配對之後。但是請記住，進行包含性檢查時，陣列元素的順序並不重要，並且重複陣列元素僅有一個元素會被視為有效。

作為結構必須吻合的一般原則的特殊例外，陣列可以包含單一基本值：

```
-- This array contains the primitive string value:
SELECT '["foo", "bar"]'::jsonb @> '"bar"'::jsonb;

-- This exception is not reciprocal -- non-containment is reported here:
SELECT '"bar"'::jsonb @> '["bar"]'::jsonb;  -- yields false
```

jsonb 還具有一個 existence 運算子，它是包含性的變體：它測試字串（作為 text 值）是否作為物件鍵或陣列元素出現在 jsonb 值的頂層。這些範例回傳 true，除非另有說明：

```
-- String exists as array element:
SELECT '["foo", "bar", "baz"]'::jsonb ? 'bar';

-- String exists as object key:
SELECT '{"foo": "bar"}'::jsonb ? 'foo';

-- Object values are not considered:
SELECT '{"foo": "bar"}'::jsonb ? 'bar';  -- yields false

-- As with containment, existence must match at the top level:
SELECT '{"foo": {"bar": "baz"}}'::jsonb ? 'bar'; -- yields false

-- A string is considered to exist if it matches a primitive JSON string:
SELECT '"foo"'::jsonb ? 'foo';
```

當涉及許多鍵或元素時，JSON 物件比陣列更適合用於測試是否包含或存在，因為與陣列不同，JSON 物件在內部進行了最佳化以進行搜尋，因此不需要線性搜尋。

{% hint style="info" %}
由於 JSON 的包含性是巢狀的，因此適當的查詢可以跳過對子物件的明確選擇。舉例來說，假設我們有一個 doc 欄位，其中包含最上層物件，而大多數物件包含子物件陣列的標籤欄位。該查詢項目，在其中包含“ term”：“ paris”和“ term”：“ food”的子物件出現，而忽略標籤陣列以外的任何鍵：

```
SELECT doc->'site_name' FROM websites
  WHERE doc @> '{"tags":[{"term":"paris"}, {"term":"food"}]}';
```

例如，另一個方式可以完成同一件事

```
SELECT doc->'site_name' FROM websites
  WHERE doc->'tags' @> '[{"term":"paris"}, {"term":"food"}]';
```

但是這種方法靈活性較差，而且效率通常也較低。

另一方面，JSON 存在性運算子不是巢狀的：它只會在 JSON 內容的最上層查詢指定的鍵或陣列元素。
{% endhint %}

在第 9.15 節中記錄了各種包含性和存在性的運算子，以及所有其他 JSON 運算子和函數。

## 8.14.4. `jsonb` Indexing

GIN 索引可用於有效搜尋大量的 jsonb 文件（datums）中出現的鍵或鍵/值配對。有兩種 GIN “operator classes”，提供了不同的效能和靈活性權衡。

jsonb 的預設 GIN 運算子類支援使用最上層鍵存在的運算子 ?，?& 和 ?| 進行查詢。運算子和路徑/值存在性運算子 @>。（有關這些運算子實作的語義的詳細信息，請參見 [Table 9.45](../functions-and-operators/json-functions-and-operators.md#table-9-45-additional-jsonb-operators)。）使用此運算子類建立索引的範例是：

```
CREATE INDEX idxgin ON api USING GIN (jdoc);
```

非預設 GIN 運算子類 jsonb\_path\_ops 僅支援對 @> 運算子進行索引。使用此運算子類建立索引的範例是：

```
CREATE INDEX idxginp ON api USING GIN (jdoc jsonb_path_ops);
```

想像一個資料表的範例，該資料表儲存了從第三方 Web 服務檢索到的 JSON 文件以及已文件化的結構定義。典型的文件是：

```
{
    "guid": "9c36adc1-7fb5-4d5b-83b4-90356a46061a",
    "name": "Angela Barton",
    "is_active": true,
    "company": "Magnafone",
    "address": "178 Howard Place, Gulf, Washington, 702",
    "registered": "2009-11-07T08:53:22 +08:00",
    "latitude": 19.793713,
    "longitude": 86.513373,
    "tags": [
        "enim",
        "aliquip",
        "qui"
    ]
}
```

我們將這些文件儲存在名為 api 的資料表中，名為 jdoc 的 jsonb 欄位中。如果在此欄位上建立了 GIN 索引，則如下查詢可以使用到該索引：

```
-- Find documents in which the key "company" has value "Magnafone"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"company": "Magnafone"}';
```

但是，索引不能用於以下查詢，儘管運算子 ? 是可索引的，但它不會直接套用於索引欄位 jdoc：

```
-- Find documents in which the key "tags" contains key or array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc -> 'tags' ? 'qui';
```

儘管如此，透過適當使用表示式索引，上述查詢仍可以使用索引。如果在“tags”鍵中查詢特定項目很常見，則定義這樣的索引可能是值得的：

```
CREATE INDEX idxgintags ON api USING GIN ((jdoc -> 'tags'));
```

現在，WHERE 子句 jdoc->'tags' ? 'qui' 將被識別為可索引運算子的應用程序 ? 到索引表示式 jdoc->'tags'。（有關表示式索引的更多資訊，請參閱[第 11.7 節](../index/indexes-on-expressions.md)。）

另外，GIN 索引支援 ＠＠ 和 ＠？ 運算子，它們處理 jsonpath 的搜尋。

```
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @@ '$.tags[*] == "qui"';
```

```
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @@ '$.tags[*] ? (@ == "qui")';
```

GIN 索引從 jsonpath 中取出以下形式的語句：`accessors_chain = const`。Accessors chain 可能由 .key，\[\*] 和 \[index] 的 Accessor 所組成_。_jsonb\_ops 也支持_ .\*_ 和 .\*\* 的 Accessor。

查詢的另一種方法是利用 containment，例如：

```
-- Find documents in which the key "tags" contains array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"tags": ["qui"]}';
```

jdoc 欄位上的簡單 GIN 索引可以支援此查詢。但是請注意，這樣的索引將在 jdoc 欄位中儲存每個鍵和值的副本，而上一範例的表示式索引僅儲存在 tag 鍵下所找到的資料。儘管簡單索引方法更加靈活（因為它支援對任何鍵的查詢），但目標表示式索引可能比簡單索引更小且搜尋速度更快。

儘管 jsonb\_path\_ops 運算子類僅支援使用 @>，@@ 和 @? 運算子的查詢，它比預設的運算子類 jsonb\_ops 具有明顯的效能優勢。對於相同資料集，jsonb\_path\_ops 索引通常也比 jsonb\_ops 索引小得多，針對搜尋的專用性更好，尤其是當查詢包含頻繁出現在資料中的鍵時。因此，搜尋性質的操作通常比預設運算子類具有更好的效能。

The technical difference between a `jsonb_ops` and a `jsonb_path_ops` GIN index is that the former creates independent index items for each key and value in the data, while the latter creates index items only for each value in the data. [\[6\]](https://www.postgresql.org/docs/12/datatype-json.html#ftn.id-1.5.7.22.18.9.3) Basically, each `jsonb_path_ops` index item is a hash of the value and the key(s) leading to it; for example to index `{"foo": {"bar": "baz"}}`, a single index item would be created incorporating all three of `foo`, `bar`, and `baz` into the hash value. Thus a containment query looking for this structure would result in an extremely specific index search; but there is no way at all to find out whether `foo` appears as a key. On the other hand, a `jsonb_ops` index would create three index items representing `foo`, `bar`, and `baz` separately; then to do the containment query, it would look for rows containing all three of these items. While GIN indexes can perform such an AND search fairly efficiently, it will still be less specific and slower than the equivalent `jsonb_path_ops` search, especially if there are a very large number of rows containing any single one of the three index items.

A disadvantage of the `jsonb_path_ops` approach is that it produces no index entries for JSON structures not containing any values, such as `{"a": {}}`. If a search for documents containing such a structure is requested, it will require a full-index scan, which is quite slow. `jsonb_path_ops` is therefore ill-suited for applications that often perform such searches.

`jsonb` also supports `btree` and `hash` indexes. These are usually useful only if it's important to check equality of complete JSON documents. The `btree` ordering for `jsonb` datums is seldom of great interest, but for completeness it is:

```
Object > Array > Boolean > Number > String > Null

Object with n pairs > object with n - 1 pairs

Array with n elements > array with n - 1 elements
```

Objects with equal numbers of pairs are compared in the order:

```
key-1, value-1, key-2 ...
```

Note that object keys are compared in their storage order; in particular, since shorter keys are stored before longer keys, this can lead to results that might be unintuitive, such as:

```
{ "aa": 1, "c": 1} > {"b": 1, "d": 1}
```

Similarly, arrays with equal numbers of elements are compared in the order:

```
element-1, element-2 ...
```

Primitive JSON values are compared using the same comparison rules as for the underlying PostgreSQL data type. Strings are compared using the default database collation.

## 8.14.5. `jsonb` Subscripting

The `jsonb` data type supports array-style subscripting expressions to extract and modify elements. Nested values can be indicated by chaining subscripting expressions, following the same rules as the `path` argument in the `jsonb_set` function. If a `jsonb` value is an array, numeric subscripts start at zero, and negative integers count backwards from the last element of the array. Slice expressions are not supported. The result of a subscripting expression is always of the jsonb data type.

`UPDATE` statements may use subscripting in the `SET` clause to modify `jsonb` values. Subscript paths must be traversable for all affected values insofar as they exist. For instance, the path `val['a']['b']['c']` can be traversed all the way to `c` if every `val`, `val['a']`, and `val['a']['b']` is an object. If any `val['a']` or `val['a']['b']` is not defined, it will be created as an empty object and filled as necessary. However, if any `val` itself or one of the intermediary values is defined as a non-object such as a string, number, or `jsonb` `null`, traversal cannot proceed so an error is raised and the transaction aborted.

An example of subscripting syntax:

```

-- Extract object value by key
SELECT ('{"a": 1}'::jsonb)['a'];

-- Extract nested object value by key path
SELECT ('{"a": {"b": {"c": 1}}}'::jsonb)['a']['b']['c'];

-- Extract array element by index
SELECT ('[1, "2", null]'::jsonb)[1];

-- Update object value by key. Note the quotes around '1': the assigned
-- value must be of the jsonb type as well
UPDATE table_name SET jsonb_field['key'] = '1';

-- This will raise an error if any record's jsonb_field['a']['b'] is something
-- other than an object. For example, the value {"a": 1} has a numeric value
-- of the key 'a'.
UPDATE table_name SET jsonb_field['a']['b']['c'] = '1';

-- Filter records using a WHERE clause with subscripting. Since the result of
-- subscripting is jsonb, the value we compare it against must also be jsonb.
-- The double quotes make "value" also a valid jsonb string.
SELECT * FROM table_name WHERE jsonb_field['key'] = '"value"';
```

`jsonb` assignment via subscripting handles a few edge cases differently from `jsonb_set`. When a source `jsonb` value is `NULL`, assignment via subscripting will proceed as if it was an empty JSON value of the type (object or array) implied by the subscript key:

```
-- Where jsonb_field was NULL, it is now {"a": 1}
UPDATE table_name SET jsonb_field['a'] = '1';

-- Where jsonb_field was NULL, it is now [1]
UPDATE table_name SET jsonb_field[0] = '1';
```

If an index is specified for an array containing too few elements, `NULL` elements will be appended until the index is reachable and the value can be set.

```
-- Where jsonb_field was [], it is now [null, null, 2];
-- where jsonb_field was [0], it is now [0, null, 2]
UPDATE table_name SET jsonb_field[2] = '2';
```

A `jsonb` value will accept assignments to nonexistent subscript paths as long as the last existing element to be traversed is an object or array, as implied by the corresponding subscript (the element indicated by the last subscript in the path is not traversed and may be anything). Nested array and object structures will be created, and in the former case `null`-padded, as specified by the subscript path until the assigned value can be placed.

```
-- Where jsonb_field was {}, it is now {'a': [{'b': 1}]}
UPDATE table_name SET jsonb_field['a'][0]['b'] = '1';

-- Where jsonb_field was [], it is now [null, {'a': 1}]
UPDATE table_name SET jsonb_field[1]['a'] = '1';
```

## 8.14.6. 對應轉換

可以使用其他延伸功能來實作針對不同程序語言的 jsonb 型別轉換。

PL/Perl 的延伸功能名稱為 jsonb\_plperl 和 jsonb\_plperlu。如果使用它們，則 jsonb 的值將視情況對應轉換為到 Perl 的 array、hash 和 scalar。

PL/Python 的延伸功能名稱為 jsonb\_plpythonu，jsonb\_plpython2u 和 jsonb\_plpython3u（有關 PL/Python 的命名約定，請參閱第 45.1 節）。 如果使用它們，則 jsonb 值將適當地對應轉換到 Python 的 dictionary，list 和 scalar。

## 8.14.7. jsonpath Type

jsonpath 型別實現了 PostgreSQL 中對 SQL/JSON 路徑語法的支援，以有效地查詢 JSON 資料。它提供以二元運算的形式來使用已解析的 SQL/JSON 路徑表示式，此表示式讓路徑引擎從 JSON 資料檢索的項目取出內容，以供 SQL/JSON 查詢函數進一步處理。

SQL / JSON 路徑 predicate 和運算子的語義基本遵循 SQL 標準。同時，為了提供使用 JSON 資料的更自然的方式，SQL/JSON 路徑語法使用了一些 JavaScript 約定：

* 點（.）用於資料成員存取。
* 中括號（\[ ]）用於陣列存取。
* 與從 1 開始的一般 SQL 陣列不同，SQL/JSON 陣列是 從 0 開始。

SQL/JSON 路徑表示式通常以 SQL 字串文字形式寫在 SQL 查詢中，因此它必須用單引號引起來，並且值中所需的任何單引號都必須加倍（請參閱[第 4.1.2.1 節](../sql-syntax/lexical-structure.md#4-1-2-1-zi-chuan-chang-shu)）。某些形式的路徑表示式需要在其中包含字串文字。這些嵌入的字串文字遵循 JavaScript/ECMAScript 約定：它們必須用雙引號引起來，並且在其中可以使用反斜線轉譯符號來表示，否則很難輸入的字元。特別地，在嵌入式字串文字中寫雙引號的方式是 \\"，而寫反斜線本身則必須寫成 \。其他特殊的反斜線序列包括在 JSON 字串中識別的那些：\b，\f，\n，\r，\t，\v 用於各種 ASCII 控制字元，\uNNNN 用於其 4 進位數字代碼標識的 Unicode 字元。反斜線語法還包括 JSON 不允許的兩種情況：\xNN 僅用兩個十六進位數字編寫的字元代碼，而 \u {N ...} 用於用 1 至 6 個十六進位數字編寫的字元代碼。

A path expression consists of a sequence of path elements, which can be the following:

* Path literals of JSON primitive types: Unicode text, numeric, true, false, or null.
* Path variables listed in [Table 8.24](https://www.postgresql.org/docs/12/datatype-json.html#TYPE-JSONPATH-VARIABLES).
* Accessor operators listed in [Table 8.25](https://www.postgresql.org/docs/12/datatype-json.html#TYPE-JSONPATH-ACCESSORS).
* `jsonpath` operators and methods listed in [Section 9.15.2.3](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-PATH-OPERATORS)
* Parentheses, which can be used to provide filter expressions or define the order of path evaluation.

For details on using `jsonpath` expressions with SQL/JSON query functions, see [Section 9.15.2](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-PATH).

#### **Table 8.24. `jsonpath` Variables**

| Variable   | Description                                                                                                                                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `$`        | A variable representing the JSON text to be queried (the _context item_).                                                                                                                                                                  |
| `$varname` | A named variable. Its value can be set by the parameter _`vars`_ of several JSON processing functions. See [Table 9.47](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-JSON-PROCESSING-TABLE) and its notes for details. |
| `@`        | A variable representing the result of path evaluation in filter expressions.                                                                                                                                                               |

#### **Table 8.25. `jsonpath` Accessors**

| Accessor Operator                                                                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>.</code><em><code>key</code></em></p><p><code>."$</code><em><code>varname</code></em>"</p>                                               | Member accessor that returns an object member with the specified key. If the key name is a named variable starting with `$` or does not meet the JavaScript rules of an identifier, it must be enclosed in double quotes as a character string literal.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `.*`                                                                                                                                              | Wildcard member accessor that returns the values of all members located at the top level of the current object.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `.**`                                                                                                                                             | Recursive wildcard member accessor that processes all levels of the JSON hierarchy of the current object and returns all the member values, regardless of their nesting level. This is a PostgreSQL extension of the SQL/JSON standard.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| <p><code>.**{</code><em><code>level</code></em>}</p><p><code>.**{</code><em><code>start_level</code></em> to <em><code>end_level</code></em>}</p> | Same as `.**`, but with a filter over nesting levels of JSON hierarchy. Nesting levels are specified as integers. Zero level corresponds to the current object. To access the lowest nesting level, you can use the `last` keyword. This is a PostgreSQL extension of the SQL/JSON standard.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `[`_`subscript`_, ...]                                                                                                                            | <p>Array element accessor. <em><code>subscript</code></em> can be given in two forms: <em><code>index</code></em> or <em><code>start_index</code></em> to <em><code>end_index</code></em>. The first form returns a single array element by its index. The second form returns an array slice by the range of indexes, including the elements that correspond to the provided <em><code>start_index</code></em> and <em><code>end_index</code></em>.</p><p>The specified <em><code>index</code></em> can be an integer, as well as an expression returning a single numeric value, which is automatically cast to integer. Zero index corresponds to the first array element. You can also use the <code>last</code> keyword to denote the last array element, which is useful for handling arrays of unknown length.</p> |
| `[*]`                                                                                                                                             | Wildcard array element accessor that returns all array elements.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

[\[6\]](https://www.postgresql.org/docs/12/datatype-json.html#id-1.5.7.22.18.9.3) For this purpose, the term “value” includes array elements, though JSON terminology sometimes considers array elements distinct from values within objects.
