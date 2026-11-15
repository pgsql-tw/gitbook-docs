# 9.16.2. SQL/JSON 路徑語言

<a id="FUNCTIONS-SQLJSON-PATH"></a>

## 9.16.2. SQL/JSON 路徑語言 [#](#functions-sqljson-path) <a href="#functions-sqljson-path" id="functions-sqljson-path"></a>

<a id="id-1.5.8.22.9.2"></a>

SQL/JSON 路徑運算式指定要從 JSON 值中取出的項目，類似於用來存取 XML 內容的 XPath 運算式。在 PostgreSQL 中，路徑運算式實作為 `jsonpath` 資料型別，並且可以使用[第 8.14.7 節](../../datatype/datatype-json/datatype-jsonpath.md#datatype-jsonpath)所述的任何元素。

JSON 查詢函式與運算子會將所提供的路徑運算式傳遞給*路徑引擎*進行求值。如果運算式與所查詢的 JSON 資料相符，就會回傳對應的 JSON 項目或項目集合。如果沒有相符的結果，依函式的不同，結果會是 `NULL`、`false` 或錯誤。路徑運算式以 SQL/JSON 路徑語言撰寫，並且可以包含算術運算式與函式。

路徑運算式由 `jsonpath` 資料型別所允許的一連串元素組成。路徑運算式通常由左至右求值，但你可以使用括號來改變運算的順序。如果求值成功，就會產生一個 JSON 項目的序列，並將求值結果回傳給完成指定計算的 JSON 查詢函式。

若要參照正在查詢的 JSON 值（*內容項目*），請在路徑運算式中使用 `$` 變數。路徑的第一個元素一定是 `$`。其後可以接著一個或多個[存取子運算子](../../datatype/datatype-json/datatype-jsonpath.md#type-jsonpath-accessors)，它們會逐層向下深入 JSON 結構，以取出內容項目的子項目。每個存取子運算子都作用於前一個求值步驟的結果，並從每個輸入項目產生零個、一個或多個輸出項目。

例如，假設你有一些來自 GPS 追蹤器、想要剖析的 JSON 資料，例如：

```

SELECT '{
  "track": {
    "segments": [
      {
        "location":   [ 47.763, 13.4034 ],
        "start time": "2018-10-14 10:05:14",
        "HR": 73
      },
      {
        "location":   [ 47.706, 13.2635 ],
        "start time": "2018-10-14 10:39:21",
        "HR": 135
      }
    ]
  }
}' AS json \gset
```

（上面的範例可以複製並貼到 psql 中，為接下來的範例做好準備。接著 psql 會將 `:'json'` 展開為包含該 JSON 值、並已適當加上引號的字串常數。）

若要取出可用的軌跡區段（track segment），你需要使用 `.key` 存取子運算子來向下穿過外層的 JSON 物件，例如：

```

=> select jsonb_path_query(:'json', '$.track.segments');
                                                                         jsonb_path_query
-----------------------------------------------------------​-----------------------------------------------------------​---------------------------------------------
 [{"HR": 73, "location": [47.763, 13.4034], "start time": "2018-10-14 10:05:14"}, {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}]
```

若要取出陣列的內容，通常會使用 `[*]` 運算子。下面的範例會回傳所有可用軌跡區段的位置座標：

```

=> select jsonb_path_query(:'json', '$.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

這裡我們從整個 JSON 輸入值（`$`）開始，接著 `.track` 存取子選取了與物件鍵 `"track"` 相關聯的 JSON 物件，然後 `.segments` 存取子選取了該物件中與鍵 `"segments"` 相關聯的 JSON 陣列，接著 `[*]` 存取子選取了該陣列的每個元素（產生一連串的項目），然後 `.location` 存取子選取了這些物件中各自與鍵 `"location"` 相關聯的 JSON 陣列。在這個範例中，每個物件都有 `"location"` 鍵；但如果其中有任何物件沒有這個鍵，`.location` 存取子對於該輸入項目就只會不產生任何輸出。

若只要回傳第一個區段的座標，可以在 `[]` 存取子運算子中指定對應的下標。請記得 JSON 陣列的索引是從 0 開始的：

```

=> select jsonb_path_query(:'json', '$.track.segments[0].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
```

每個路徑求值步驟的結果，都可以由[第 9.16.2.3 節](#functions-sqljson-path-operators)所列的一個或多個 `jsonpath` 運算子與方法加以處理。每個方法名稱前面都必須加上一個句點。例如，你可以取得陣列的大小：

```

=> select jsonb_path_query(:'json', '$.track.segments.size()');
 jsonb_path_query
------------------
 2
```

在路徑運算式中使用 `jsonpath` 運算子與方法的更多範例，請見下方的[第 9.16.2.3 節](#functions-sqljson-path-operators)。

路徑中也可以包含*篩選運算式*，其作用類似於 SQL 中的 `WHERE` 子句。篩選運算式以問號開頭，並在括號中提供條件：

```

? (condition)
```

篩選運算式必須緊接在它所要套用的路徑求值步驟之後撰寫。該步驟的結果會經過篩選，只保留滿足所提供條件的項目。SQL/JSON 定義了三值邏輯，因此條件可以產生 `true`、`false` 或 `unknown`。`unknown` 值扮演與 SQL `NULL` 相同的角色，並且可以用 `is unknown` 述詞來測試。後續的路徑求值步驟只會使用篩選運算式回傳 `true` 的那些項目。

可以在篩選運算式中使用的函式與運算子列於[表 9.53](#functions-sqljson-filter-ex-table)。在篩選運算式中，`@` 變數代表正在考量的值（也就是前一個路徑步驟的其中一個結果）。你可以在 `@` 之後撰寫存取子運算子來取出其組成項目。

例如，假設你想要取出所有高於 130 的心率值。你可以這樣做：

```

=> select jsonb_path_query(:'json', '$.track.segments[*].HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

若要取得具有這類值之區段的開始時間，你必須在選取開始時間之前先篩選掉不相關的區段，因此篩選運算式要套用在前一個步驟上，而條件中使用的路徑也會有所不同：

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

如有需要，你可以依序使用多個篩選運算式。下面的範例會選取所有包含具有相關座標之位置以及高心率值之區段的開始時間：

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4) ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

也可以在不同的巢狀層級使用篩選運算式。下面的範例會先依位置篩選所有區段，然後回傳這些區段的高心率值（如果有的話）：

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4).HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

你也可以將篩選運算式彼此巢狀。這個範例會在軌跡包含任何具有高心率值的區段時回傳軌跡的大小，否則回傳空序列：

```

=> select jsonb_path_query(:'json', '$.track ? (exists(@.segments[*] ? (@.HR > 130))).segments.size()');
 jsonb_path_query
------------------
 2
```

<a id="FUNCTIONS-SQLJSON-DEVIATIONS"></a>

### 9.16.2.1. 與 SQL 標準的差異 [#](#functions-sqljson-deviations) <a href="#functions-sqljson-deviations" id="functions-sqljson-deviations"></a>

PostgreSQL 對 SQL/JSON 路徑語言的實作與 SQL/JSON 標準有下列差異。

<a id="FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS"></a>

### 9.16.2.1.1. 布林述詞檢查運算式 [#](#functions-sqljson-check-expressions) <a href="#functions-sqljson-check-expressions" id="functions-sqljson-check-expressions"></a>

作為 SQL 標準的延伸，PostgreSQL 的路徑運算式可以是布林述詞，而 SQL 標準只允許在篩選中使用述詞。SQL 標準的路徑運算式會回傳所查詢 JSON 值的相關元素，而述詞檢查運算式則會回傳述詞的單一三值 `jsonb` 結果：`true`、`false` 或 `null`。例如，我們可以撰寫這個符合 SQL 標準的篩選運算式：

```

=> select jsonb_path_query(:'json', '$.track.segments ?(@[*].HR > 130)');
                                jsonb_path_query
-----------------------------------------------------------​----------------------
 {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}
```

類似的述詞檢查運算式只會回傳 `true`，表示存在相符的項目：

```

=> select jsonb_path_query(:'json', '$.track.segments[*].HR > 130');
 jsonb_path_query
------------------
 true
```

### 注意 [#](#zhu-yi) <a href="#zhu-yi" id="zhu-yi"></a>

`@@` 運算子（以及 `jsonb_path_match` 函式）必須使用述詞檢查運算式，而 `@?` 運算子（或 `jsonb_path_exists` 函式）則不應使用述詞檢查運算式。

<a id="FUNCTIONS-SQLJSON-REGULAR-EXPRESSION-DEVIATION"></a>

### 9.16.2.1.2. 正規表示式的解讀 [#](#functions-sqljson-regular-expression-deviation) <a href="#functions-sqljson-regular-expression-deviation" id="functions-sqljson-regular-expression-deviation"></a>

在 `like_regex` 篩選中使用的正規表示式模式，其解讀方式有一些細微差異，如[第 9.16.2.4 節](#jsonpath-regular-expressions)所述。

<a id="FUNCTIONS-SQLJSON-STRICT-AND-LAX-MODES"></a>

### 9.16.2.2. 嚴格模式與寬鬆模式 [#](#functions-sqljson-strict-and-lax-modes) <a href="#functions-sqljson-strict-and-lax-modes" id="functions-sqljson-strict-and-lax-modes"></a>

查詢 JSON 資料時，路徑運算式可能與實際的 JSON 資料結構不相符。嘗試存取物件中不存在的成員或陣列中不存在的元素，被定義為結構錯誤。SQL/JSON 路徑運算式有兩種處理結構錯誤的模式：

* lax（寬鬆，預設）— 路徑引擎會隱含地讓所查詢的資料適應指定的路徑。任何無法依下述方式修正的結構錯誤都會被抑制，產生不相符的結果。
* strict（嚴格）— 如果發生結構錯誤，就會引發錯誤。

當 JSON 資料不符合預期的綱要時，寬鬆模式有助於讓 JSON 文件與路徑運算式相符。如果某個運算元不符合特定操作的要求，可以在執行該操作之前，自動將它包裝成 SQL/JSON 陣列，或是將其元素轉換為 SQL/JSON 序列來解除包裝。此外，比較運算子在寬鬆模式下會自動解除運算元的包裝，因此你可以直接比較 SQL/JSON 陣列。大小為 1 的陣列會被視為等於它唯一的元素。在下列情況下不會執行自動解除包裝：

* 路徑運算式包含 `type()` 或 `size()` 方法，這兩個方法分別回傳陣列的型別與元素個數。
* 所查詢的 JSON 資料包含巢狀陣列。在這種情況下，只有最外層的陣列會被解除包裝，所有內層陣列則保持不變。因此，在每個路徑求值步驟中，隱含的解除包裝只能向下深入一層。

例如，查詢上面列出的 GPS 資料時，在使用寬鬆模式下，你可以不必理會它儲存的是區段陣列這件事：

```

=> select jsonb_path_query(:'json', 'lax $.track.segments.location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

在嚴格模式下，指定的路徑必須完全符合所查詢 JSON 文件的結構，因此使用這個路徑運算式會導致錯誤：

```

=> select jsonb_path_query(:'json', 'strict $.track.segments.location');
ERROR:  jsonpath member accessor can only be applied to an object
```

若要得到與寬鬆模式相同的結果，你必須明確地解除 `segments` 陣列的包裝：

```

=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

寬鬆模式的解除包裝行為可能會導致出人意料的結果。例如，下面這個使用 `.**` 存取子的查詢，會將每個 `HR` 值都選取兩次：

```

=> select jsonb_path_query(:'json', 'lax $.**.HR');
 jsonb_path_query
------------------
 73
 135
 73
 135
```

會發生這種情況，是因為 `.**` 存取子同時選取了 `segments` 陣列及其每個元素，而 `.HR` 存取子在寬鬆模式下會自動解除陣列的包裝。為了避免出人意料的結果，我們建議只在嚴格模式下使用 `.**` 存取子。下面的查詢只會將每個 `HR` 值選取一次：

```

=> select jsonb_path_query(:'json', 'strict $.**.HR');
 jsonb_path_query
------------------
 73
 135
```

陣列的解除包裝也可能導致非預期的結果。請看這個選取所有 `location` 陣列的範例：

```

=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

如預期般，它會回傳完整的陣列。但套用篩選運算式會使陣列被解除包裝，以便對每個項目求值，結果只回傳符合運算式的項目：

```

=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
------------------
 47.763
 47.706
(2 rows)
```

儘管路徑運算式選取的是完整的陣列，結果仍是如此。請使用嚴格模式來恢復選取陣列：

```

=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

<a id="FUNCTIONS-SQLJSON-PATH-OPERATORS"></a>

### 9.16.2.3. SQL/JSON 路徑運算子與方法 [#](#functions-sqljson-path-operators) <a href="#functions-sqljson-path-operators" id="functions-sqljson-path-operators"></a>

[表 9.52](#functions-sqljson-op-table) 列出了 `jsonpath` 中可用的運算子與方法。請注意，一元運算子與方法可以套用在前一個路徑步驟所產生的多個值上，而二元運算子（加法等）只能套用在單一值上。在寬鬆模式下，套用在陣列上的方法會對陣列中的每個值執行。例外的是 `.type()` 與 `.size()`，它們會套用在陣列本身。

<a id="FUNCTIONS-SQLJSON-OP-TABLE"></a>

### 表 9.52. `jsonpath` 運算子與方法 [#](#functions-sqljson-op-table) <a href="#functions-sqljson-op-table" id="functions-sqljson-op-table"></a>

<table border="1" class="table" summary="jsonpath Operators and Methods"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator/Method
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">+</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        加法
       </p>
<p>
<code class="literal">jsonb_path_query('[2]', '$[0] + 3')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">+</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        一元正號（不做任何運算）；與加法不同，它可以對多個值逐一進行
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": [2,3,4]}', '+ $.x')</code>
        → <code class="returnvalue">[2, 3, 4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        減法
       </p>
<p>
<code class="literal">jsonb_path_query('[2]', '7 - $[0]')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        取負值；與減法不同，它可以對多個值逐一進行
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": [2,3,4]}', '- $.x')</code>
        → <code class="returnvalue">[-2, -3, -4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">*</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        乘法
       </p>
<p>
<code class="literal">jsonb_path_query('[4]', '2 * $[0]')</code>
        → <code class="returnvalue">8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">/</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        除法
       </p>
<p>
<code class="literal">jsonb_path_query('[8.5]', '$[0] / 2')</code>
        → <code class="returnvalue">4.2500000000000000</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">%</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        模數（餘數）
       </p>
<p>
<code class="literal">jsonb_path_query('[32]', '$[0] % 10')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">type()</code>
        → <code class="returnvalue"><em class="replaceable"><code>string</code></em></code>
</p>
<p>
        JSON 項目的型別（請參閱 <code class="function">json_typeof</code>）
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "2", {}]', '$[*].type()')</code>
        → <code class="returnvalue">["number", "string", "object"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">size()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        JSON 項目的大小（陣列元素的個數；如果不是陣列則為 1）
       </p>
<p>
<code class="literal">jsonb_path_query('{"m": [11, 15]}', '$.m.size()')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">boolean()</code>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        從 JSON 布林值、數值或字串轉換而來的布林值
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "yes", false]', '$[*].boolean()')</code>
        → <code class="returnvalue">[true, true, false]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">string()</code>
        → <code class="returnvalue"><em class="replaceable"><code>string</code></em></code>
</p>
<p>
        從 JSON 布林值、數值、字串或日期時間轉換而來的字串值
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1.23, "xyz", false]', '$[*].string()')</code>
        → <code class="returnvalue">["1.23", "xyz", "false"]</code>
</p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp().string()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">double()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的近似浮點數
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "1.9"}', '$.len.double() * 2')</code>
        → <code class="returnvalue">3.8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">ceiling()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        大於或等於給定數值的最接近整數
       </p>
<p>
<code class="literal">jsonb_path_query('{"h": 1.3}', '$.h.ceiling()')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">floor()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        小於或等於給定數值的最接近整數
       </p>
<p>
<code class="literal">jsonb_path_query('{"h": 1.7}', '$.h.floor()')</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">abs()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        給定數值的絕對值
       </p>
<p>
<code class="literal">jsonb_path_query('{"z": -0.3}', '$.z.abs()')</code>
        → <code class="returnvalue">0.3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">bigint()</code>
        → <code class="returnvalue"><em class="replaceable"><code>bigint</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的大整數值
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "9876543219"}', '$.len.bigint()')</code>
        → <code class="returnvalue">9876543219</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">decimal( [ <em class="replaceable"><code>precision</code></em> [ , <em class="replaceable"><code>scale</code></em> ] ] )</code>
        → <code class="returnvalue"><em class="replaceable"><code>decimal</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來、經過捨入的十進位值（<code class="literal">precision</code> 與 <code class="literal">scale</code> 必須是整數值）
       </p>
<p>
<code class="literal">jsonb_path_query('1234.5678', '$.decimal(6, 2)')</code>
        → <code class="returnvalue">1234.57</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">integer()</code>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的整數值
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "12345"}', '$.len.integer()')</code>
        → <code class="returnvalue">12345</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">number()</code>
        → <code class="returnvalue"><em class="replaceable"><code>numeric</code></em></code>
</p>
<p>
        從 JSON 數值或字串轉換而來的 numeric 值
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "123.45"}', '$.len.number()')</code>
        → <code class="returnvalue">123.45</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">datetime()</code> → <code class="returnvalue"><em class="replaceable"><code>datetime_type</code></em></code>（請參閱注意事項）
       </p>
<p>
        從字串轉換而來的日期／時間值
       </p>
<p>
<code class="literal">jsonb_path_query('["2015-8-1", "2015-08-12"]', '$[*] ? (@.datetime() &lt; "2015-08-2".datetime())')</code>
        → <code class="returnvalue">"2015-8-1"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">datetime(<em class="replaceable"><code>template</code></em>)</code> → <code class="returnvalue"><em class="replaceable"><code>datetime_type</code></em></code>（請參閱注意事項）
       </p>
<p>
        使用指定的 <code class="function">to_timestamp</code> 樣板，從字串轉換而來的日期／時間值
       </p>
<p>
<code class="literal">jsonb_path_query_array('["12:30", "18:40"]', '$[*].datetime("HH24:MI")')</code>
        → <code class="returnvalue">["12:30:00", "18:40:00"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">date()</code>
        → <code class="returnvalue"><em class="replaceable"><code>date</code></em></code>
</p>
<p>
        從字串轉換而來的日期值
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15"', '$.date()')</code>
        → <code class="returnvalue">"2023-08-15"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time()</code>
        → <code class="returnvalue"><em class="replaceable"><code>time without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間值
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56"', '$.time()')</code>
        → <code class="returnvalue">"12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>time without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56.789"', '$.time(2)')</code>
        → <code class="returnvalue">"12:34:56.79"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time_tz()</code>
        → <code class="returnvalue"><em class="replaceable"><code>time with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間值
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56 +05:30"', '$.time_tz()')</code>
        → <code class="returnvalue">"12:34:56+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time_tz(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>time with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56.789 +05:30"', '$.time_tz(2)')</code>
        → <code class="returnvalue">"12:34:56.79+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp()</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間戳記值
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp without time zone</code></em></code>
</p>
<p>
        從字串轉換而來的不帶時區的時間戳記值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56.789"', '$.timestamp(2)')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56.79"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp_tz()</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間戳記值
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56 +05:30"', '$.timestamp_tz()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp_tz(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp with time zone</code></em></code>
</p>
<p>
        從字串轉換而來的帶時區的時間戳記值，其小數秒會調整為給定的精確度
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56.789 +05:30"', '$.timestamp_tz(2)')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56.79+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>object</code></em> <code class="literal">.</code> <code class="literal">keyvalue()</code>
        → <code class="returnvalue"><em class="replaceable"><code>array</code></em></code>
</p>
<p>
        物件的鍵值對，表示為一個由物件組成的陣列，每個物件包含三個欄位：<code class="literal">"key"</code>、<code class="literal">"value"</code> 與 <code class="literal">"id"</code>；其中 <code class="literal">"id"</code> 是該鍵值對所屬之物件的唯一識別碼
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": "20", "y": 32}', '$.keyvalue()')</code>
        → <code class="returnvalue">[{"id": 0, "key": "x", "value": "20"}, {"id": 0, "key": "y", "value": 32}]</code>
</p></td></tr></tbody></table>

<br>

### 注意 [#](#zhu-yi-1) <a href="#zhu-yi-1" id="zhu-yi-1"></a>

`datetime()` 與 `datetime(template)` 方法的結果型別可以是 `date`、`timetz`、`time`、`timestamptz` 或 `timestamp`。這兩個方法都會動態地決定其結果型別。

`datetime()` 方法會依序嘗試將其輸入字串與 `date`、`timetz`、`time`、`timestamptz` 以及 `timestamp` 的 ISO 格式進行比對。它會在第一個相符的格式停止，並產生對應的資料型別。

`datetime(template)` 方法會依據所提供之樣板字串中使用的欄位來決定結果型別。

`datetime()` 與 `datetime(template)` 方法使用與 SQL 函式 `to_timestamp` 相同的剖析規則（請參閱[第 9.8 節](../functions-formatting.md)），但有三個例外。第一，這些方法不允許不相符的樣板模式。第二，樣板字串中只允許使用下列分隔符號：減號、句點、斜線（solidus）、逗號、撇號、分號、冒號與空白。第三，樣板字串中的分隔符號必須與輸入字串完全相符。

如果需要比較不同的日期／時間型別，會套用隱含的型別轉換。`date` 值可以轉換為 `timestamp` 或 `timestamptz`，`timestamp` 可以轉換為 `timestamptz`，而 `time` 可以轉換為 `timetz`。不過，除了第一種以外，這些轉換都取決於目前的 [TimeZone](../../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設定，因此只能在具時區感知能力的 `jsonpath` 函式中執行。同樣地，其他將字串轉換為日期／時間型別之日期／時間相關方法也會進行這種型別轉換，而這可能涉及目前的 [TimeZone](../../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) 設定。因此，這些轉換也只能在具時區感知能力的 `jsonpath` 函式中執行。

[表 9.53](#functions-sqljson-filter-ex-table) 列出了可用的篩選運算式元素。

<a id="FUNCTIONS-SQLJSON-FILTER-EX-TABLE"></a>

### 表 9.53. `jsonpath` 篩選運算式元素 [#](#functions-sqljson-filter-ex-table) <a href="#functions-sqljson-filter-ex-table" id="functions-sqljson-filter-ex-table"></a>

<table border="1" class="table" summary="jsonpath Filter Expression Elements"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Predicate/Value
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">==</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        相等比較（這個運算子以及其他比較運算子都適用於所有 JSON 純量值）
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == 1)')</code>
        → <code class="returnvalue">[1, 1]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == "a")')</code>
        → <code class="returnvalue">["a"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">!=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;&gt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        不相等比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 1, 3]', '$[*] ? (@ != 1)')</code>
        → <code class="returnvalue">[2, 3]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;&gt; "b")')</code>
        → <code class="returnvalue">["a", "c"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        小於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &lt; 2)')</code>
        → <code class="returnvalue">[1]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        小於或等於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;= "b")')</code>
        → <code class="returnvalue">["a", "b"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&gt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        大於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt; 2)')</code>
        → <code class="returnvalue">[3]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&gt;=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        大於或等於比較
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt;= 2)')</code>
        → <code class="returnvalue">[2, 3]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">true</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        JSON 常數 <code class="literal">true</code>
</p>
<p>
<code class="literal">jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == true)')</code>
        → <code class="returnvalue">{"name": "Chris", "parent": true}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">false</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        JSON 常數 <code class="literal">false</code>
</p>
<p>
<code class="literal">jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == false)')</code>
        → <code class="returnvalue">{"name": "John", "parent": false}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">null</code>
        → <code class="returnvalue"><em class="replaceable"><code>value</code></em></code>
</p>
<p>
        JSON 常數 <code class="literal">null</code>（請注意，與 SQL 不同，與 <code class="literal">null</code> 的比較會正常運作）
       </p>
<p>
<code class="literal">jsonb_path_query('[{"name": "Mary", "job": null}, {"name": "Michael", "job": "driver"}]', '$[*] ? (@.job == null) .name')</code>
        → <code class="returnvalue">"Mary"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">&amp;&amp;</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        布林 AND
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &gt; 1 &amp;&amp; @ &lt; 5)')</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">||</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        布林 OR
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &lt; 1 || @ &gt; 5)')</code>
        → <code class="returnvalue">7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">!</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        布林 NOT
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (!(@ &lt; 5))')</code>
        → <code class="returnvalue">7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">is unknown</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試布林條件是否為 <code class="literal">unknown</code>。
       </p>
<p>
<code class="literal">jsonb_path_query('[-1, 2, 7, "foo"]', '$[*] ? ((@ &gt; 0) is unknown)')</code>
        → <code class="returnvalue">"foo"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">like_regex</code> <em class="replaceable"><code>string</code></em> [<span class="optional"> <code class="literal">flag</code> <em class="replaceable"><code>string</code></em> </span>]
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試第一個運算元是否符合第二個運算元所給的正規表示式，並可選擇性地套用由 <code class="literal">flag</code> 字元字串所描述的修改（請參閱<a class="xref" href="#jsonpath-regular-expressions">第 9.16.2.4 節</a>）。
       </p>
<p>
<code class="literal">jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c")')</code>
        → <code class="returnvalue">["abc", "abdacb"]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c" flag "i")')</code>
        → <code class="returnvalue">["abc", "aBdC", "abdacb"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">starts with</code> <em class="replaceable"><code>string</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試第二個運算元是否為第一個運算元的開頭子字串。
       </p>
<p>
<code class="literal">jsonb_path_query('["John Smith", "Mary Stone", "Bob Johnson"]', '$[*] ? (@ starts with "John")')</code>
        → <code class="returnvalue">"John Smith"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">exists</code> <code class="literal">(</code> <em class="replaceable"><code>path_expression</code></em> <code class="literal">)</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試路徑運算式是否至少符合一個 SQL/JSON 項目。如果路徑運算式會導致錯誤，就回傳 <code class="literal">unknown</code>；第二個範例利用這一點，避免在嚴格模式下發生鍵不存在的錯誤。
       </p>
<p>
<code class="literal">jsonb_path_query('{"x": [1, 2], "y": [2, 4]}', 'strict $.* ? (exists (@ ? (@[*] &gt; 2)))')</code>
        → <code class="returnvalue">[2, 4]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('{"value": 41}', 'strict $ ? (exists (@.name)) .name')</code>
        → <code class="returnvalue">[]</code>
</p></td></tr></tbody></table>

<br>

<a id="JSONPATH-REGULAR-EXPRESSIONS"></a>

### 9.16.2.4. SQL/JSON 正規表示式 [#](#jsonpath-regular-expressions) <a href="#jsonpath-regular-expressions" id="jsonpath-regular-expressions"></a>

<a id="id-1.5.8.22.9.23.2"></a>

SQL/JSON 路徑運算式可以使用 `like_regex` 篩選，將文字與正規表示式進行比對。例如，下面的 SQL/JSON 路徑查詢會以不區分大小寫的方式，比對陣列中所有以英文母音開頭的字串：

```

$[*] ? (@ like_regex "^[aeiou]" flag "i")
```

選用的 `flag` 字串可以包含下列一個或多個字元：`i` 表示不區分大小寫的比對，`m` 允許 `^` 與 `$` 在換行處比對，`s` 允許 `.` 比對換行字元，而 `q` 則將整個模式加上引號（使行為簡化為單純的子字串比對）。

SQL/JSON 標準的正規表示式定義借用自 `LIKE_REGEX` 運算子，而該運算子又使用 XQuery 標準。PostgreSQL 目前並不支援 `LIKE_REGEX` 運算子。因此，`like_regex` 篩選是使用[第 9.7.3 節](../functions-matching/functions-posix-regexp.md#functions-posix-regexp)所述的 POSIX 正規表示式引擎實作的。這導致了與標準 SQL/JSON 行為之間的各種細微差異，這些差異整理於[第 9.7.3.8 節](../functions-matching/functions-posix-regexp.md#posix-vs-xquery)。不過請注意，該處所述的旗標字母不相容問題並不適用於 SQL/JSON，因為它會將 XQuery 的旗標字母轉換為 POSIX 引擎所預期的形式。

請記住，`like_regex` 的模式引數是一個 JSON 路徑字串字面值，依照[第 8.14.7 節](../../datatype/datatype-json/datatype-jsonpath.md#datatype-jsonpath)所述的規則撰寫。這特別意味著，你想在正規表示式中使用的任何反斜線都必須重複兩次。例如，要比對根文件中只包含數字的字串值：

```

$.* ? (@ like_regex "^\\d+$")
```

[返回 9.16. JSON 函式與運算子](../functions-json.md#functions-json)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-json.html)（原文版本：18.6；核對日期：2026-09-11）
