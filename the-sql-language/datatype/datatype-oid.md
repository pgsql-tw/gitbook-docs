<a id="DATATYPE-OID"></a>

## 8.19. 物件識別碼型別 [#](#DATATYPE-OID)

<a id="id-1.5.7.27.2"></a><a id="id-1.5.7.27.3"></a><a id="id-1.5.7.27.4"></a><a id="id-1.5.7.27.5"></a><a id="id-1.5.7.27.6"></a><a id="id-1.5.7.27.7"></a><a id="id-1.5.7.27.8"></a><a id="id-1.5.7.27.9"></a><a id="id-1.5.7.27.10"></a><a id="id-1.5.7.27.11"></a><a id="id-1.5.7.27.12"></a><a id="id-1.5.7.27.13"></a><a id="id-1.5.7.27.14"></a><a id="id-1.5.7.27.15"></a><a id="id-1.5.7.27.16"></a><a id="id-1.5.7.27.17"></a><a id="id-1.5.7.27.18"></a>

物件識別碼（OID）是 PostgreSQL 內部用來作為各種系統資料表主鍵的識別碼。型別 `oid` 代表一個物件識別碼。`oid` 還有數種別名型別，每一種都命名為 `regsomething` 的形式。[表 8.26](datatype-oid.md#DATATYPE-OID-TABLE) 列出了它們的概觀。

`oid` 型別目前是以無號的四位元組整數實作。因此，它不足以在大型資料庫中、甚至在單一的大型資料表中，提供整個資料庫範圍的唯一性。

`oid` 型別本身除了比較之外幾乎沒有其他運算。不過它可以型別轉換成 integer，然後使用標準的整數運算子加以操作。（如果你這麼做，請小心可能發生的有號與無號混淆問題。）

OID 別名型別除了專用的輸入與輸出常式之外，沒有自己的運算。這些常式能夠接受並顯示系統物件的符號名稱，而不是 `oid` 型別所使用的原始數值。這些別名型別讓查詢物件的 OID 值變得更簡單。例如，若要檢視與資料表 `mytable` 相關的 `pg_attribute` 資料列，可以這樣寫：

```

SELECT * FROM pg_attribute WHERE attrelid = 'mytable'::regclass;
```

而不必寫成：

```

SELECT * FROM pg_attribute
  WHERE attrelid = (SELECT oid FROM pg_class WHERE relname = 'mytable');
```

雖然這樣看起來似乎還不算太糟，但它其實還是過度簡化了。如果在不同綱要中有多個名為 `mytable` 的資料表，就需要一個複雜得多的子查詢才能選出正確的 OID。`regclass` 的輸入轉換器會依照綱要路徑設定來處理資料表查詢，因此它會自動做出「正確的事」。同樣地，把資料表的 OID 型別轉換成 `regclass`，也很方便用來以符號形式顯示數值 OID。

<a id="DATATYPE-OID-TABLE"></a>

**表 8.26. 物件識別碼型別**

<table border="1" class="table" summary="物件識別碼型別"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>參照</th><th>說明</th><th>值範例</th></tr></thead><tbody><tr><td><code class="type">oid</code></td><td>任意</td><td>數值物件識別碼</td><td><code class="literal">564182</code></td></tr><tr><td><code class="type">regclass</code></td><td><code class="structname">pg_class</code></td><td>關聯名稱</td><td><code class="literal">pg_type</code></td></tr><tr><td><code class="type">regcollation</code></td><td><code class="structname">pg_collation</code></td><td>定序名稱</td><td><code class="literal">"POSIX"</code></td></tr><tr><td><code class="type">regconfig</code></td><td><code class="structname">pg_ts_config</code></td><td>全文檢索設定</td><td><code class="literal">english</code></td></tr><tr><td><code class="type">regdictionary</code></td><td><code class="structname">pg_ts_dict</code></td><td>全文檢索字典</td><td><code class="literal">simple</code></td></tr><tr><td><code class="type">regnamespace</code></td><td><code class="structname">pg_namespace</code></td><td>命名空間名稱</td><td><code class="literal">pg_catalog</code></td></tr><tr><td><code class="type">regoper</code></td><td><code class="structname">pg_operator</code></td><td>運算子名稱</td><td><code class="literal">+</code></td></tr><tr><td><code class="type">regoperator</code></td><td><code class="structname">pg_operator</code></td><td>含引數型別的運算子</td><td><code class="literal">*(integer,​integer)</code>
         或 <code class="literal">-(NONE,​integer)</code></td></tr><tr><td><code class="type">regproc</code></td><td><code class="structname">pg_proc</code></td><td>函式名稱</td><td><code class="literal">sum</code></td></tr><tr><td><code class="type">regprocedure</code></td><td><code class="structname">pg_proc</code></td><td>含引數型別的函式</td><td><code class="literal">sum(int4)</code></td></tr><tr><td><code class="type">regrole</code></td><td><code class="structname">pg_authid</code></td><td>角色名稱</td><td><code class="literal">smithee</code></td></tr><tr><td><code class="type">regtype</code></td><td><code class="structname">pg_type</code></td><td>資料型別名稱</td><td><code class="literal">integer</code></td></tr></tbody></table>

<br>

所有依命名空間分組之物件的 OID 別名型別，都接受加上綱要限定的名稱；而且如果不加限定就無法在目前的搜尋路徑中找到該物件，它們在輸出時也會顯示加上綱要限定的名稱。例如，`myschema.mytable` 是 `regclass` 可接受的輸入（前提是確實有這樣的資料表）。該值輸出時可能顯示為 `myschema.mytable`，也可能只顯示為 `mytable`，取決於目前的搜尋路徑。`regproc` 與 `regoper` 別名型別只接受唯一（未多載）的輸入名稱，因此用途有限；在大多數情況下，`regprocedure` 或 `regoperator` 更為合適。對於 `regoperator`，一元運算子是以在未使用的運算元位置寫上 `NONE` 來識別的。

這些型別的輸入函式允許語彙單元之間有空白字元，並且會把大寫字母摺疊成小寫，但雙引號內的部分除外；這麼做是為了讓語法規則與 SQL 中撰寫物件名稱的方式相似。反過來說，輸出函式在必要時會使用雙引號，以使輸出成為有效的 SQL 識別符號。例如，一個名為 `Foo`（`F` 為大寫）且接受兩個整數引數的函式，其 OID 可以輸入為 `' "Foo" ( int, integer ) '::regprocedure`。輸出則會像 `"Foo"(integer,integer)` 這樣。函式名稱與引數型別名稱也都可以加上綱要限定。

許多 PostgreSQL 內建函式都接受資料表或其他種類資料庫物件的 OID，為了方便起見，它們被宣告為接受 `regclass`（或適當的 OID 別名型別）。這表示你不必手動查出物件的 OID，只要以字串常數的形式輸入它的名稱即可。例如，`nextval(regclass)` 函式接受序列關聯的 OID，因此你可以像這樣呼叫它：

```

nextval('foo')              operates on sequence foo
nextval('FOO')              same as above
nextval('"Foo"')            operates on sequence Foo
nextval('myschema.foo')     operates on myschema.foo
nextval('"myschema".foo')   same as above
nextval('foo')              searches search path for foo
```

### 注意

當你把這種函式的引數寫成沒有額外修飾的字面值字串時，它會成為 `regclass` 型別（或適當型別）的常數。由於這實際上就只是一個 OID，即使之後物件被更名、重新指派綱要等等，它仍然會追蹤原本所識別的物件。這種「早期繫結」行為，對於欄位預設值與檢視表中的物件參照通常是我們想要的。但有時候你可能會希望採用「延遲繫結」，也就是在執行期才解析物件參照。若要取得延遲繫結的行為，請強制讓該常數以 `text` 常數而非 `regclass` 的形式儲存：

```

nextval('foo'::text)      foo is looked up at runtime
```

`to_regclass()` 函式及其同類函式也可以用來執行執行期的查詢。請參閱[表 9.76](../functions/functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE)。

另一個使用 `regclass` 的實用例子，是查出列在 `information_schema` 檢視表中之資料表的 OID，因為這些檢視表並不會直接提供這類 OID。例如，你可能想呼叫需要資料表 OID 的 `pg_relation_size()` 函式。把上述規則納入考量後，正確的做法是

```

SELECT table_schema, table_name,
       pg_relation_size((quote_ident(table_schema) || '.' ||
                         quote_ident(table_name))::regclass)
FROM information_schema.tables
WHERE ...
```

`quote_ident()` 函式會在需要時負責為識別符號加上雙引號。看似比較簡單的寫法

```

SELECT pg_relation_size(table_name)
FROM information_schema.tables
WHERE ...
```

則是*不建議使用的*，因為對於不在你搜尋路徑中的資料表，或是名稱需要加引號的資料表，它會失敗。

大多數 OID 別名型別還有一項額外的特性，就是會建立相依性。如果這些型別之一的常數出現在已儲存的運算式中（例如欄位的預設值運算式或檢視表），它就會建立對所參照物件的相依性。例如，如果某個欄位的預設值運算式是 `nextval('my_seq'::regclass)`，PostgreSQL 會知道這個預設值運算式相依於序列 `my_seq`，因此系統不會允許在尚未移除該預設值運算式之前就刪除該序列。改用 `nextval('my_seq'::text)` 則不會建立相依性。（`regrole` 是這項特性的例外。這種型別的常數不允許出現在已儲存的運算式中。）

系統使用的另一種識別碼型別是 `xid`，也就是交易（縮寫為 xact）識別碼。這是系統欄位 `xmin` 與 `xmax` 的資料型別。交易識別碼是 32 位元的量值。在某些情境下會使用 64 位元的變體 `xid8`。與 `xid` 值不同，`xid8` 值是嚴格單調遞增的，而且在資料庫叢集的生命週期內不會被重複使用。更多細節請參閱[第 67.1 節](../../internals/transactions/transaction-id.md)。

系統使用的第三種識別碼型別是 `cid`，也就是指令識別碼。這是系統欄位 `cmin` 與 `cmax` 的資料型別。指令識別碼同樣是 32 位元的量值。

系統使用的最後一種識別碼型別是 `tid`，也就是 tuple 識別碼（資料列識別碼）。這是系統欄位 `ctid` 的資料型別。tuple ID 是一組（區塊編號、區塊內的 tuple 索引）配對，用來識別資料列在其資料表中的實體位置。

（這些系統欄位在[第 5.6 節](../ddl/ddl-system-columns.md)中有進一步的說明。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-oid.html)（原文版本：18.6；核對日期：2026-09-13）
