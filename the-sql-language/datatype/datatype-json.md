<a id="DATATYPE-JSON"></a>
## 8.14. JSON 型別 [#](#DATATYPE-JSON)

[8.14.1. JSON 輸入與輸出語法](datatype-json.md#JSON-KEYS-ELEMENTS)

[8.14.2. 設計 JSON 文件](datatype-json.md#JSON-DOC-DESIGN)

[8.14.3. `jsonb` 的包含與存在性](datatype-json.md#JSON-CONTAINMENT)

[8.14.4. `jsonb` 索引](datatype-json.md#JSON-INDEXING)

[8.14.5. `jsonb` 下標](datatype-json.md#JSONB-SUBSCRIPTING)

[8.14.6. 轉換（Transforms）](datatype-json.md#DATATYPE-JSON-TRANSFORMS)

[8.14.7. jsonpath 型別](datatype-json.md#DATATYPE-JSONPATH)

<a id="id-1.5.7.22.2"></a><a id="id-1.5.7.22.3"></a>

JSON 資料型別用於儲存 JSON（JavaScript Object
Notation）資料，其規範見於 [RFC
7159](https://datatracker.ietf.org/doc/html/rfc7159)。這類資料也可以儲存為
`text`，但 JSON 資料型別的優點在於可以強制檢查每個儲存值是否符合
JSON 規則而有效。此外，還有多種針對這些資料型別的 JSON 專用函式與運算子可供使用；請參閱[9.16 節](../functions/functions-json.md)。

PostgreSQL 提供了兩種儲存 JSON
資料的型別：`json` 與 `jsonb`。為了對這些資料型別實作高效率的查詢
機制，PostgreSQL
還提供了 `jsonpath` 資料型別，描述於
[8.14.7 節](datatype-json.md#DATATYPE-JSONPATH)。

`json` 與 `jsonb`
資料型別所接受的輸入值集合*幾乎*完全相同。兩者實際上的主要差異在於效率。
`json` 資料型別會儲存輸入文字的精確副本，
處理函式每次執行時都必須重新剖析；而
`jsonb` 資料則以分解過的二進位格式儲存，
這使得輸入時因為額外的轉換負擔而稍微較慢，但由於不需要重新剖析，
處理速度則明顯較快。`jsonb` 也支援索引，
這可能是一項重要的優勢。

由於 `json` 型別會儲存輸入文字的精確副本，它
會保留權杖（token）之間在語意上不重要的空白，
以及 JSON 物件中鍵的順序。此外，如果值中的某個 JSON 物件
內同一個鍵出現超過一次，所有的鍵/值配對都會被保留。（處理函式會將最後一個值視為
有效值。）相對地，`jsonb` 不會保留空白，
不會保留物件鍵的順序，也不會保留重複的物件鍵。若輸入中指定了重複的鍵，
只會保留最後一個值。

一般而言，大多數應用程式應該優先將 JSON 資料儲存為
`jsonb`，除非有相當特殊的需求，例如
對物件鍵順序有既有假設的舊系統。

RFC 7159 規定 JSON 字串應以 UTF8 編碼。
因此，除非資料庫編碼為 UTF8，
否則 JSON
型別不可能嚴格遵循 JSON 規範。若試圖直接包含
無法以資料庫編碼表示的字元將會失敗；反之，
能以資料庫編碼表示但無法以 UTF8 表示的字元則會被允許。

RFC 7159 允許 JSON 字串包含以
`\uXXXX` 表示的 Unicode 逸出序列。在
`json` 型別的輸入函式中，無論資料庫編碼為何，都允許使用 Unicode 逸出序列，
並且只會檢查其語法正確性（也就是 `\u` 後面
是否跟著四個十六進位數字）。然而，`jsonb` 的輸入函式較為嚴格：它不允許
使用資料庫編碼無法表示之字元的 Unicode 逸出序列。`jsonb` 型別
也會拒絕 `\u0000`（因為它無法以
PostgreSQL 的 `text` 型別表示），並且要求
任何用來表示 Unicode 基本多文種平面之外字元的 Unicode 代理對（surrogate
pair）都必須正確無誤。有效的 Unicode 逸出序列會被轉換為
對應的單一字元來儲存；這也包括將代理對摺疊為單一字元。

### 注意

[9.16 節](../functions/functions-json.md)中所述的許多 JSON 處理函式
會將 Unicode 逸出序列轉換為一般字元，因此即使其輸入的型別是
`json` 而非 `jsonb`，也一樣會拋出前面所述的同類型錯誤。
`json` 輸入函式不進行這些檢查的這項事實，
可以視為一種歷史遺留現象，不過它確實能夠讓
JSON Unicode 逸出序列在不支援所代表字元的資料庫編碼中，
以簡單的方式儲存（而不加以處理）。

在將文字形式的 JSON 輸入轉換為 `jsonb` 時，RFC
7159 所描述的基本型別會有效地對映到
原生的 PostgreSQL 型別，如
[表 8.23](datatype-json.md#JSON-TYPE-MAPPING-TABLE)所示。
因此，對於構成有效 `jsonb` 資料而言，
存在一些不適用於 `json` 型別、也不適用於抽象意義上 JSON 的
額外次要限制，這些限制對應於底層資料型別所能表示範圍的限制。
值得注意的是，`jsonb` 會拒絕超出
PostgreSQL `numeric` 資料型別範圍的數字，
而 `json` 則不會。RFC 7159 允許這類由實作定義的
限制。不過，實務上這類問題在其他
實作中更容易發生，因為將 JSON 的 `number`
基本型別以 IEEE 754 雙精度浮點數表示
是相當常見的做法（RFC 7159 也明確預期並允許這種做法）。
當使用 JSON 作為與這類系統交換資料的格式時，應考量
相較於原本由 PostgreSQL 所儲存的資料，
可能會遺失數值精度的風險。

反過來說，如表中所述，JSON 基本型別的輸入格式也存在一些
不適用於對應 PostgreSQL 型別的次要限制。

<a id="JSON-TYPE-MAPPING-TABLE"></a>

**表 8.23. JSON 基本型別與對應的 PostgreSQL 型別**

<table border="1" class="table" summary="JSON 基本型別與對應的 PostgreSQL 型別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>JSON 基本型別</th><th><span class="productname">PostgreSQL</span> 型別</th><th>備註</th></tr></thead><tbody><tr><td><code class="type">string</code></td><td><code class="type">text</code></td><td>不允許 <code class="literal">\u0000</code>，代表資料庫編碼中不存在
         之字元的 Unicode 逸出序列亦不允許</td></tr><tr><td><code class="type">number</code></td><td><code class="type">numeric</code></td><td>不允許 <code class="literal">NaN</code> 與 <code class="literal">infinity</code> 值</td></tr><tr><td><code class="type">boolean</code></td><td><code class="type">boolean</code></td><td>只接受小寫的 <code class="literal">true</code> 與 <code class="literal">false</code> 拼寫</td></tr><tr><td><code class="type">null</code></td><td>（無）</td><td>SQL 的 <code class="literal">NULL</code> 是不同的概念</td></tr></tbody></table>

<br><a id="JSON-KEYS-ELEMENTS"></a>

<a id="JSON-KEYS-ELEMENTS"></a>

### 8.14.1. JSON 輸入與輸出語法 [#](#JSON-KEYS-ELEMENTS)

JSON 資料型別的輸入／輸出語法如
RFC 7159 所規範。

以下都是有效的 `json`（或 `jsonb`）運算式：

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

如前所述，當一個 JSON 值被輸入後，在未經任何額外處理的情況下印出時，
`json` 會輸出與輸入完全相同的文字，
而 `jsonb` 則不會保留諸如空白等語意上不重要的
細節。舉例來說，請注意以下的差異：

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

有一項值得留意、語意上不重要的細節是，
在 `jsonb` 中，數字會依照底層
`numeric` 型別的行為來印出。實務上這表示
以 `E` 記法輸入的數字，在印出時將不會保留該記法，
例如：

```

SELECT '{"reading": 1.230e-5}'::json, '{"reading": 1.230e-5}'::jsonb;
         json          |          jsonb
-----------------------+-------------------------
 {"reading": 1.230e-5} | {"reading": 0.00001230}
(1 row)
```

不過，`jsonb` 會保留尾端的小數零，如此範例所示，
即使就相等性檢查等用途而言，這些尾端小數零在語意上並不重要。

關於用來建構與處理 JSON 值的內建函式與運算子清單，
請參閱[9.16 節](../functions/functions-json.md)。

<a id="JSON-DOC-DESIGN"></a>

### 8.14.2. 設計 JSON 文件 [#](#JSON-DOC-DESIGN)

以 JSON 表示資料，可以比傳統的關聯式資料模型
更具彈性，這在需求變動頻繁的環境中相當有吸引力。
這兩種做法完全可以在同一個應用程式中並存、
互補。然而，即使對於追求最大彈性的應用程式，
仍然建議 JSON 文件保有某種程度上固定的
結構。這種結構通常不會被強制要求（雖然仍可以宣告式地強制執行某些業務規則），
但擁有可預期的結構，能讓撰寫可有效彙總資料表中一組
「文件」（資料項）的查詢變得更容易。

JSON 資料在儲存於資料表中時，
同樣須考量與其他資料型別相同的並行控制考量。
雖然儲存大型文件是可行的，但請記住，
任何更新都會取得整列的列層級鎖定。
建議將 JSON 文件的大小控制在
可管理的範圍內，以減少更新交易之間的鎖定爭用。
理想情況下，每個 JSON 文件都應該
代表一個依業務規則判斷無法再合理拆分為
可獨立修改之較小資料項的原子資料項。

<a id="JSON-CONTAINMENT"></a>

### 8.14.3. `jsonb` 的包含與存在性 [#](#JSON-CONTAINMENT)

<a id="id-1.5.7.22.17.2"></a><a id="id-1.5.7.22.17.3"></a>

測試*包含*（containment）是 `jsonb`
的一項重要能力。`json` 型別並沒有相對應的一套
功能。包含性測試的是
某個 `jsonb` 文件內是否含有另一個文件。
以下範例除特別註明外，皆會傳回 true：

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

一般原則是，被包含的物件在結構與資料內容上必須
與包含它的物件相符，這裡容許先從
包含它的物件中捨棄部分不相符的陣列元素或物件鍵/值配對。
但請記住，在進行包含比對時，陣列元素的順序並不重要，
而重複的陣列元素在比對時實際上只會被視為出現一次。

作為結構必須相符這項一般原則的特殊例外，
陣列可以包含一個基本值：

```

-- This array contains the primitive string value:
SELECT '["foo", "bar"]'::jsonb @> '"bar"'::jsonb;

-- This exception is not reciprocal -- non-containment is reported here:
SELECT '"bar"'::jsonb @> '["bar"]'::jsonb;  -- yields false
```

`jsonb` 也有一個*存在性*（existence）運算子，這是
包含概念的一種變體：它測試某個字串
（以 `text` 值給定）是否出現在
`jsonb` 值頂層的物件鍵或陣列元素中。
以下範例除特別註明外，皆會傳回 true：

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

當涉及大量鍵或元素時，JSON 物件比陣列更適合
用來測試包含性或存在性，因為與陣列不同，
物件在內部已針對搜尋進行了最佳化，不需要
逐一線性搜尋。

### 提示

由於 JSON 的包含性是巢狀的，適當的查詢可以省略
子物件的明確選取。舉例來說，假設我們有
一個 `doc` 欄位，其頂層含有物件，其中
大多數物件都包含 `tags` 欄位，該欄位含有子物件所組成的陣列。
這個查詢會找出這樣的項目：其 tags 陣列中分別存在
含有 `"term":"paris"` 的子物件，以及含有 `"term":"food"` 的子物件（不要求同一個子物件同時符合兩者），
並忽略 `tags` 陣列以外出現的任何此類鍵：

```

SELECT doc->'site_name' FROM websites
  WHERE doc @> '{"tags":[{"term":"paris"}, {"term":"food"}]}';
```

也可以用類似下列的方式達到相同效果，

```

SELECT doc->'site_name' FROM websites
  WHERE doc->'tags' @> '[{"term":"paris"}, {"term":"food"}]';
```

不過這種做法彈性較差，效率通常也較低。

另一方面，JSON 存在性運算子並非巢狀的：它
只會在 JSON 值的頂層尋找指定的鍵或陣列元素。

各種包含性與存在性運算子，連同所有其他
JSON 運算子與函式，都記載
於[9.16 節](../functions/functions-json.md)。

<a id="JSON-INDEXING"></a>

### 8.14.4. `jsonb` 索引 [#](#JSON-INDEXING)

<a id="id-1.5.7.22.18.2"></a>

GIN 索引可以用來有效率地搜尋大量
`jsonb` 文件（資料項）中出現的
鍵或鍵/值配對。
系統提供了兩種 GIN「運算子類別」，
在效能與彈性之間提供不同的取捨。

`jsonb` 的預設 GIN 運算子類別支援使用
鍵存在運算子 `?`、`?|`
與 `?&`、包含運算子
`@>`，以及 `jsonpath` 比對
運算子 `@?` 與 `@@` 的查詢。
（關於這些運算子所實作語意的細節，
請參閱[表 9.48](../functions/functions-json.md#FUNCTIONS-JSONB-OP-TABLE)。）
以此運算子類別建立索引的範例如下：

```

CREATE INDEX idxgin ON api USING GIN (jdoc);
```

非預設的 GIN 運算子類別 `jsonb_path_ops`
不支援鍵存在運算子，但支援
`@>`、`@?` 與 `@@`。
以此運算子類別建立索引的範例如下：

```

CREATE INDEX idxginp ON api USING GIN (jdoc jsonb_path_ops);
```

考慮這樣一個範例：某個資料表儲存從第三方
Web 服務取得、具有已文件化綱要定義的 JSON 文件。
典型的文件如下：

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

我們將這些文件儲存於名為 `api` 的資料表中，
存放在名為 `jdoc` 的 `jsonb` 欄位裡。
若在此欄位上建立了 GIN 索引，
下列這類查詢便可以利用該索引：

```

-- Find documents in which the key "company" has value "Magnafone"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"company": "Magnafone"}';
```

然而，下列這類查詢無法利用該索引，因為
即使運算子 `?` 本身是可索引的，
它並沒有直接套用在有索引的欄位 `jdoc` 上：

```

-- Find documents in which the key "tags" contains key or array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc -> 'tags' ? 'qui';
```

儘管如此，只要適當使用運算式索引，
上述查詢仍然可以利用索引。若查詢
`"tags"` 鍵內特定項目是常見的需求，
建立像這樣的索引可能是值得的：

```

CREATE INDEX idxgintags ON api USING GIN ((jdoc -> 'tags'));
```

現在，`WHERE` 子句 `jdoc -> 'tags' ? 'qui'`
就會被辨識為對有索引的運算式
`jdoc -> 'tags'`
套用可索引運算子 `?`。
（關於運算式索引的更多資訊，請參閱[11.7 節](../indexes/indexes-expressional.md)。）

另一種查詢方式是利用包含性，例如：

```

-- Find documents in which the key "tags" contains array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"tags": ["qui"]}';
```

在 `jdoc` 欄位上建立的簡單 GIN 索引即可支援這個
查詢。但請注意，這樣的索引會儲存
`jdoc` 欄位中每個鍵與值的副本，
而前一個範例的運算式索引則只儲存
`tags` 鍵之下所找到的資料。雖然簡單索引的做法
彈性大得多（因為它支援對任何鍵的查詢），
但針對性的運算式索引通常會比簡單
索引更小、搜尋速度更快。

GIN 索引也支援 `@?`
與 `@@` 運算子，
用於執行 `jsonpath` 比對。範例如下：

```

SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @? '$.tags[*] ? (@ == "qui")';
```

```

SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @@ '$.tags[*] == "qui"';
```

對於這些運算子，GIN 索引會從
`jsonpath` 模式中擷取出形如
`accessors_chain
== constant` 的子句，
並依據這些子句中提到的鍵與值來執行索引搜尋。存取器
鏈可以包含 `.key`、
`[*]`，
以及 `[index]` 存取器。
`jsonb_ops` 運算子類別還
支援 `.*` 與 `.**` 存取器，
但 `jsonb_path_ops` 運算子類別則不支援。

雖然 `jsonb_path_ops` 運算子類別
只支援 `@>`、`@?`
與 `@@` 這幾個運算子，但相較於
預設的運算子類別 `jsonb_ops`，它具有明顯的
效能優勢。在相同資料上，`jsonb_path_ops`
索引通常比 `jsonb_ops`
索引小得多，搜尋的針對性也更好，
尤其是在查詢中含有資料裡頻繁出現的鍵時更是如此。因此，
搜尋操作的效能通常比使用預設運算子類別更好。

`jsonb_ops`
與 `jsonb_path_ops` GIN
索引之間的技術差異在於，前者
會為資料中的每個鍵與值各自建立獨立的索引項目，
而後者只會為資料中的
每個值建立索引項目。
[<a id="id-1.5.7.22.18.9.3"></a>[7]](#ftn.id-1.5.7.22.18.9.3)
基本上，每個 `jsonb_path_ops` 索引項目
都是該值以及通往該值之鍵的雜湊值；例如要為
`{"foo": {"bar": "baz"}}` 建立索引，就會建立單一索引項目，
將 `foo`、`bar`
與 `baz` 這三者全部納入雜湊值的計算。因此，
尋找此結構的包含性查詢會得到針對性極高的索引
搜尋；但完全無法得知 `foo`
是否曾以鍵的形式出現。另一方面，`jsonb_ops`
索引則會分別建立三個索引項目，代表
`foo`、`bar` 與 `baz`；
然後在進行包含性查詢時，會尋找同時含有這三個
項目的資料列。雖然 GIN 索引能夠相當有效率地執行這類
AND 搜尋，但它的針對性仍然會比
對應的 `jsonb_path_ops` 搜尋來得較差、
速度較慢，尤其是當有大量資料列
含有這三個索引項目中任何單一一個時，差異會更明顯。

`jsonb_path_ops` 做法的一項缺點在於，
對於不含任何值的 JSON 結構（例如
`{"a": {}}`），它不會產生任何索引項目。若請求
搜尋含有此類結構的文件，就需要進行
全索引掃描，這相當緩慢。因此
`jsonb_path_ops` 並不適合經常執行此類搜尋的應用程式。

`jsonb` 也支援 `btree` 與 `hash`
索引。這兩者通常只在需要檢查完整 JSON 文件是否相等時
才有用。
`jsonb` 資料項所用的 `btree`
排序方式很少受到太多關注，但為求完整起見，其排序規則如下：

```

Object > Array > Boolean > Number > String > null

Object with n pairs > object with n - 1 pairs

Array with n elements > array with n - 1 elements
```

但有一項例外情況（基於歷史因素）：頂層的空陣列排序小於*`null`*。
配對數量相同的物件，會依下列順序比較：

```

key-1, value-1, key-2 ...
```

請注意，物件的鍵是依其儲存順序來比較的；
特別是，由於較短的鍵會儲存在較長的鍵之前，
這可能導致一些不太直覺的結果，例如：

```

{ "aa": 1, "c": 1} > {"b": 1, "d": 1}
```

同樣地，元素數量相同的陣列，會依下列順序比較：

```

element-1, element-2 ...
```

基本的 JSON 值會使用與底層
PostgreSQL 資料型別相同的比較規則進行比較。字串則
使用預設的資料庫定序（collation）進行比較。

<a id="JSONB-SUBSCRIPTING"></a>

### 8.14.5. `jsonb` 下標 [#](#JSONB-SUBSCRIPTING)

`jsonb` 資料型別支援陣列風格的下標運算式，
用來擷取與修改元素。巢狀的值可以透過鏈接
下標運算式來表示，其規則與 `jsonb_set`
函式中的 `path` 引數相同。若某個 `jsonb`
值是陣列，數字下標從零開始，負整數則從陣列的
最後一個元素往回數。不支援切片運算式。
下標運算式的結果永遠是 jsonb 資料型別。

`UPDATE` 陳述式可以在
`SET` 子句中使用下標來修改 `jsonb` 值。下標
路徑必須就其存在的範圍而言，對所有受影響的值都是可追蹤的。舉
例來說，若每一個 `val`、
`val['a']` 以及 `val['a']['b']` 都是
物件，路徑 `val['a']['b']['c']` 就可以一路追蹤
到 `c`。若任何一個 `val['a']` 或
`val['a']['b']`
未曾定義，就會被建立為空物件，並依需要填入內容。
但是，若 `val` 本身或任何中間值
被定義為非物件的內容，例如字串、數字或
`jsonb` 的 `null`，就無法繼續追蹤，
因此會引發錯誤並中止交易。

下標語法的範例：

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

透過下標進行的 `jsonb` 賦值，在幾種邊緣情況下
的處理方式與 `jsonb_set` 有所不同。當來源
`jsonb` 值為 `NULL` 時，透過下標賦值的行為，
會如同它原本是由下標鍵所隱含的型別（物件或陣列）之空 JSON 值一般
進行處理：

```

-- Where jsonb_field was NULL, it is now {"a": 1}
UPDATE table_name SET jsonb_field['a'] = '1';

-- Where jsonb_field was NULL, it is now [1]
UPDATE table_name SET jsonb_field[0] = '1';
```

若對元素過少的陣列指定了某個索引，
系統會附加 `NULL` 元素，直到能夠到達該索引，
才設定該值。

```

-- Where jsonb_field was [], it is now [null, null, 2];
-- where jsonb_field was [0], it is now [0, null, 2]
UPDATE table_name SET jsonb_field[2] = '2';
```

只要最後所追蹤到的既有元素是物件或陣列（與
對應的下標相符），`jsonb` 值就會接受
對不存在下標路徑的賦值（路徑中最後一個下標所指的
元素則不會被追蹤，因此可以是任何內容）。系統會依照下標路徑
建立巢狀的陣列與物件結構，並在前者的情況下
以 `null` 填補，直到可以放入所賦的值為止。

```

-- Where jsonb_field was {}, it is now {"a": [{"b": 1}]}
UPDATE table_name SET jsonb_field['a'][0]['b'] = '1';

-- Where jsonb_field was [], it is now [null, {"a": 1}]
UPDATE table_name SET jsonb_field[1]['a'] = '1';
```

<a id="DATATYPE-JSON-TRANSFORMS"></a>

### 8.14.6. 轉換（Transforms） [#](#DATATYPE-JSON-TRANSFORMS)

系統提供了額外的擴充功能，可為不同的程序性語言
實作 `jsonb` 型別的轉換。

PL/Perl 適用的擴充功能名為 `jsonb_plperl` 與
`jsonb_plperlu`。若使用這些擴充功能，
`jsonb` 值會依情況對映為 Perl 的陣列、雜湊與純量。

PL/Python 適用的擴充功能名為 `jsonb_plpython3u`。
若使用此擴充功能，`jsonb` 值會依情況對映為
Python 的字典（dictionary）、串列（list）與純量。

在這些擴充功能中，`jsonb_plperl` 被
視為「受信任的」，也就是說，具有目前資料庫上
`CREATE` 權限的非超級使用者即可安裝它。其餘的則
需要超級使用者權限才能安裝。

<a id="DATATYPE-JSONPATH"></a>

### 8.14.7. jsonpath 型別 [#](#DATATYPE-JSONPATH)

<a id="id-1.5.7.22.21.2"></a>

`jsonpath` 型別在
PostgreSQL 中實作了對 SQL/JSON 路徑語言的支援，以有效率地查詢 JSON 資料。
它提供了已剖析之 SQL/JSON 路徑運算式的二進位表示，
指定路徑引擎要從 JSON 資料中擷取哪些項目，
供後續以 SQL/JSON 查詢函式進行處理。

SQL/JSON 路徑述詞與運算子的語意大致遵循 SQL 的做法。
同時，為了提供處理 JSON 資料的自然方式，
SQL/JSON 路徑語法採用了一些 JavaScript 的慣例：

* 點號（`.`）用於成員存取。
* 方括號（`[]`）用於陣列存取。
* SQL/JSON 陣列是以 0 為起始的，這與從 1 開始的一般 SQL
  陣列不同。

SQL/JSON 路徑運算式中的數值字面量遵循 JavaScript 規則，
這在某些小細節上與 SQL 及 JSON 都不同。舉
例來說，SQL/JSON 路徑允許使用 `.1` 與
`1.`，這在 JSON 中是無效的。系統支援非十進位整數
字面量與底線分隔符，例如
`1_000_000`、`0x1EEE_FFFF`、
`0o273`、`0b100101`。在 SQL/JSON 路徑
中（在 JavaScript 中也一樣，但並非 SQL 本身固有的語法），底線
分隔符不得緊接在基數前置詞之後。

SQL/JSON 路徑運算式通常會以 SQL 字元字串字面量的形式
寫在 SQL 查詢中，因此必須以單引號括住，
其中若需要單引號，則必須以雙倍表示
（請參閱[4.1.2.1 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)）。
某些形式的路徑運算式在其中需要字串字面量。
這些內嵌的字串字面量遵循 JavaScript／ECMAScript 慣例：
必須以雙引號括住，並可以在其中使用反斜線逸出序列
來表示原本難以輸入的字元。
特別是，若要在內嵌字串字面量中寫入雙引號，方式為
`\"`；若要寫入反斜線本身，
則必須寫成 `\\`。其他特殊的反斜線序列
還包括 JavaScript 字串中所辨識的：
`\b`、
`\f`、
`\n`、
`\r`、
`\t`、
`\v`，
用於表示各種 ASCII 控制字元，
`\xNN` 用於表示以兩位十六進位數字
書寫的字元碼，
`\uNNNN` 用於表示由 4 位十六進位碼位
所識別的 Unicode 字元，而
`\u{N...}` 則用於表示以 1 到 6 位
十六進位數字書寫的 Unicode 字元碼位。

路徑運算式由一連串路徑元素組成，
可以是下列任何一種：

* JSON 基本型別的路徑字面量：
  Unicode 文字、數字、true、false 或 null。
* [表 8.24](datatype-json.md#TYPE-JSONPATH-VARIABLES)中所列的路徑變數。
* [表 8.25](datatype-json.md#TYPE-JSONPATH-ACCESSORS)中所列的存取器運算子。
* [9.16.2.3 節](../functions/functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS)中所列的
  `jsonpath` 運算子與方法。
* 括號，可用於提供篩選運算式
  或定義路徑求值的順序。

關於在 SQL/JSON 查詢函式中使用 `jsonpath` 運算式的
詳情，請參閱[9.16.2 節](../functions/functions-json.md#FUNCTIONS-SQLJSON-PATH)。

<a id="TYPE-JSONPATH-VARIABLES"></a>

**表 8.24. `jsonpath` 變數**

<table border="1" class="table" summary="jsonpath 變數"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>變數</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">$</code></td><td>代表被查詢之 JSON 值的變數
      （即<em class="firstterm">上下文項目</em>）。
      </td></tr><tr><td><code class="literal">$varname</code></td><td>
        具名變數。其值可透過多個 JSON 處理函式的
        <em class="parameter"><code>vars</code></em> 參數設定；
        詳情請參閱<a class="xref" href="../functions/functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE">表 9.51</a>。
        
      </td></tr><tr><td><code class="literal">@</code></td><td>代表篩選運算式中路徑求值結果的
      變數。
      </td></tr></tbody></table>

<br><a id="TYPE-JSONPATH-ACCESSORS"></a>

**表 8.25. `jsonpath` 存取器**

<table border="1" class="table" summary="jsonpath 存取器"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>存取器運算子</th><th>說明</th></tr></thead><tbody><tr><td>
<p>
<code class="literal">.<em class="replaceable"><code>key</code></em></code>
</p>
<p>
<code class="literal">."$<em class="replaceable"><code>varname</code></em>"</code>
</p>
</td><td>
<p>
        成員存取器，傳回具有指定鍵的物件成員。若鍵名
        與某個以 <code class="literal">$</code> 開頭的具名變數相符，
        或不符合識別字的
        JavaScript 規則，則必須以雙引號括住，使其成為字串字面量。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">.*</code>
</p>
</td><td>
<p>
        萬用字元成員存取器，傳回位於目前物件頂層的所有
        成員之值。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">.**</code>
</p>
</td><td>
<p>
        遞迴萬用字元成員存取器，會處理目前物件之 JSON 階層的所有
        層級，並傳回所有的
        成員值，無論其巢狀層級為何。這是
        <span class="productname">PostgreSQL</span> 對
        SQL/JSON 標準的擴充。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">.**{<em class="replaceable"><code>level</code></em>}</code>
</p>
<p>
<code class="literal">.**{<em class="replaceable"><code>start_level</code></em> to
        <em class="replaceable"><code>end_level</code></em>}</code>
</p>
</td><td>
<p>
        與 <code class="literal">.**</code> 類似，但只選取指定的
        JSON 階層層級。巢狀層級以整數指定。
        第零層對應目前的物件。若要存取最低的
        巢狀層級，可以使用 <code class="literal">last</code> 關鍵字。
        這是 <span class="productname">PostgreSQL</span> 對
        SQL/JSON 標準的擴充。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">[<em class="replaceable"><code>subscript</code></em>, ...]</code>
</p>
</td><td>
<p>
        陣列元素存取器。
        <code class="literal"><em class="replaceable"><code>subscript</code></em></code> 可以
        以兩種形式給定：<code class="literal"><em class="replaceable"><code>index</code></em></code>
        或 <code class="literal"><em class="replaceable"><code>start_index</code></em> to <em class="replaceable"><code>end_index</code></em></code>。
        第一種形式依索引傳回單一陣列元素。第二種
        形式則依索引範圍傳回一段陣列切片，包含對應於所提供的
        <em class="replaceable"><code>start_index</code></em> 與 <em class="replaceable"><code>end_index</code></em> 的
        元素。
       </p>
<p>
        指定的 <em class="replaceable"><code>index</code></em> 可以是整數，
        也可以是傳回單一數值的運算式，該數值會自動
        轉型為整數。索引零對應陣列的第一個
        元素。您也可以使用 <code class="literal">last</code> 關鍵字
        來表示陣列的最後一個元素，這對於處理長度未知的
        陣列相當有用。
       </p>
</td></tr><tr><td>
<p>
<code class="literal">[*]</code>
</p>
</td><td>
<p>
        萬用字元陣列元素存取器，傳回所有陣列元素。
       </p>
</td></tr></tbody></table>

<br>

<br>

---

<a id="ftn.id-1.5.7.22.18.9.3"></a>

[[7]](#id-1.5.7.22.18.9.3) 
就此而言，「值」一詞也包括陣列元素，
儘管 JSON 術語有時會將陣列元素與物件中的值
視為不同的概念。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-json.html)（原文版本：18.6；核對日期：2026-09-25）
