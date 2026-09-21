<a id="DATATYPE"></a>

## 第 8 章 資料型別

**目錄**

[8.1. 數值型別](datatype-numeric.md)
:   [8.1.1. 整數型別](datatype-numeric.md#DATATYPE-INT)

    [8.1.2. 任意精度數字](datatype-numeric.md#DATATYPE-NUMERIC-DECIMAL)

    [8.1.3. 浮點數型別](datatype-numeric.md#DATATYPE-FLOAT)

    [8.1.4. 序列型別](datatype-numeric.md#DATATYPE-SERIAL)

[8.2. 貨幣型別](datatype-money.md)

[8.3. 字元型別](datatype-character.md)

[8.4. 二進位資料型別](datatype-binary.md)
:   [8.4.1. `bytea` 十六進位格式](datatype-binary.md#DATATYPE-BINARY-BYTEA-HEX-FORMAT)

    [8.4.2. `bytea` 跳脫格式](datatype-binary.md#DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT)

[8.5. 日期／時間型別](datatype-datetime.md)
:   [8.5.1. 日期／時間輸入](datatype-datetime.md#DATATYPE-DATETIME-INPUT)

    [8.5.2. 日期／時間輸出](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT)

    [8.5.3. 時區](datatype-datetime.md#DATATYPE-TIMEZONES)

    [8.5.4. 時間間隔輸入](datatype-datetime.md#DATATYPE-INTERVAL-INPUT)

    [8.5.5. 時間間隔輸出](datatype-datetime.md#DATATYPE-INTERVAL-OUTPUT)

[8.6. 布林型別](datatype-boolean.md)

[8.7. 列舉型別](datatype-enum.md)
:   [8.7.1. 列舉型別的宣告](datatype-enum.md#DATATYPE-ENUM-DECLARATION)

    [8.7.2. 排序](datatype-enum.md#DATATYPE-ENUM-ORDERING)

    [8.7.3. 型別安全](datatype-enum.md#DATATYPE-ENUM-TYPE-SAFETY)

    [8.7.4. 實作細節](datatype-enum.md#DATATYPE-ENUM-IMPLEMENTATION-DETAILS)

[8.8. 幾何型別](datatype-geometric.md)
:   [8.8.1. 點](datatype-geometric.md#DATATYPE-GEOMETRIC-POINTS)

    [8.8.2. 直線](datatype-geometric.md#DATATYPE-LINE)

    [8.8.3. 線段](datatype-geometric.md#DATATYPE-LSEG)

    [8.8.4. 矩形](datatype-geometric.md#DATATYPE-GEOMETRIC-BOXES)

    [8.8.5. 路徑](datatype-geometric.md#DATATYPE-GEOMETRIC-PATHS)

    [8.8.6. 多邊形](datatype-geometric.md#DATATYPE-POLYGON)

    [8.8.7. 圓](datatype-geometric.md#DATATYPE-CIRCLE)

[8.9. 網路位址型別](datatype-net-types.md)
:   [8.9.1. `inet`](datatype-net-types.md#DATATYPE-INET)

    [8.9.2. `cidr`](datatype-net-types.md#DATATYPE-CIDR)

    [8.9.3. `inet` 與 `cidr` 的比較](datatype-net-types.md#DATATYPE-INET-VS-CIDR)

    [8.9.4. `macaddr`](datatype-net-types.md#DATATYPE-MACADDR)

    [8.9.5. `macaddr8`](datatype-net-types.md#DATATYPE-MACADDR8)

[8.10. 位元字串型別](datatype-bit.md)

[8.11. 全文檢索型別](datatype-textsearch.md)
:   [8.11.1. `tsvector`](datatype-textsearch.md#DATATYPE-TSVECTOR)

    [8.11.2. `tsquery`](datatype-textsearch.md#DATATYPE-TSQUERY)

[8.12. UUID 型別](datatype-uuid.md)

[8.13. XML 型別](datatype-xml.md)
:   [8.13.1. 建立 XML 值](datatype-xml.md#DATATYPE-XML-CREATING)

    [8.13.2. 編碼處理](datatype-xml.md#DATATYPE-XML-ENCODING-HANDLING)

    [8.13.3. 存取 XML 值](datatype-xml.md#DATATYPE-XML-ACCESSING-XML-VALUES)

[8.14. JSON 型別](datatype-json.md)
:   [8.14.1. JSON 的輸入與輸出語法](datatype-json.md#JSON-KEYS-ELEMENTS)

    [8.14.2. 設計 JSON 文件](datatype-json.md#JSON-DOC-DESIGN)

    [8.14.3. `jsonb` 的包含與存在](datatype-json.md#JSON-CONTAINMENT)

    [8.14.4. `jsonb` 索引](datatype-json.md#JSON-INDEXING)

    [8.14.5. `jsonb` 下標](datatype-json.md#JSONB-SUBSCRIPTING)

    [8.14.6. 轉換](datatype-json.md#DATATYPE-JSON-TRANSFORMS)

    [8.14.7. jsonpath 型別](datatype-json.md#DATATYPE-JSONPATH)

[8.15. 陣列](arrays.md)
:   [8.15.1. 陣列型別的宣告](arrays.md#ARRAYS-DECLARATION)

    [8.15.2. 陣列值的輸入](arrays.md#ARRAYS-INPUT)

    [8.15.3. 存取陣列](arrays.md#ARRAYS-ACCESSING)

    [8.15.4. 修改陣列](arrays.md#ARRAYS-MODIFYING)

    [8.15.5. 在陣列中搜尋](arrays.md#ARRAYS-SEARCHING)

    [8.15.6. 陣列的輸入與輸出語法](arrays.md#ARRAYS-IO)

[8.16. 複合型別](rowtypes.md)
:   [8.16.1. 複合型別的宣告](rowtypes.md#ROWTYPES-DECLARING)

    [8.16.2. 建構複合值](rowtypes.md#ROWTYPES-CONSTRUCTING)

    [8.16.3. 存取複合型別](rowtypes.md#ROWTYPES-ACCESSING)

    [8.16.4. 修改複合型別](rowtypes.md#ROWTYPES-MODIFYING)

    [8.16.5. 在查詢中使用複合型別](rowtypes.md#ROWTYPES-USAGE)

    [8.16.6. 複合型別的輸入與輸出語法](rowtypes.md#ROWTYPES-IO-SYNTAX)

[8.17. 範圍型別](rangetypes.md)
:   [8.17.1. 內建的範圍與多重範圍型別](rangetypes.md#RANGETYPES-BUILTIN)

    [8.17.2. 範例](rangetypes.md#RANGETYPES-EXAMPLES)

    [8.17.3. 含端點與不含端點的界限](rangetypes.md#RANGETYPES-INCLUSIVITY)

    [8.17.4. 無限（無界限）範圍](rangetypes.md#RANGETYPES-INFINITE)

    [8.17.5. 範圍的輸入／輸出](rangetypes.md#RANGETYPES-IO)

    [8.17.6. 建構範圍與多重範圍](rangetypes.md#RANGETYPES-CONSTRUCT)

    [8.17.7. 離散範圍型別](rangetypes.md#RANGETYPES-DISCRETE)

    [8.17.8. 定義新的範圍型別](rangetypes.md#RANGETYPES-DEFINING)

    [8.17.9. 索引](rangetypes.md#RANGETYPES-INDEXING)

    [8.17.10. 範圍上的限制條件](rangetypes.md#RANGETYPES-CONSTRAINT)

[8.18. 網域型別](domains.md)

[8.19. 物件識別碼型別](datatype-oid.md)

[8.20. `pg_lsn` 型別](datatype-pg-lsn.md)

[8.21. 虛擬型別](datatype-pseudo.md)

<a id="id-1.5.7.2"></a><a id="id-1.5.7.3"></a>

PostgreSQL 為使用者提供了一組豐富的原生資料型別。使用者也可以使用 [CREATE TYPE](../../reference/sql-commands/sql-createtype.md) 指令將新的型別加入 PostgreSQL。

[表 8.1](README.md#DATATYPE-TABLE) 列出所有內建的通用資料型別。「別名」欄位中所列的替代名稱，大多是 PostgreSQL 基於歷史因素在內部使用的名稱。此外，還有一些內部使用或已棄用的型別可以使用，但這裡並未列出。

<a id="DATATYPE-TABLE"></a>

**表 8.1. 資料型別**

<table border="1" class="table" summary="資料型別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>別名</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">bigint</code></td><td><code class="type">int8</code></td><td>有號八位元組整數</td></tr><tr><td><code class="type">bigserial</code></td><td><code class="type">serial8</code></td><td>自動遞增的八位元組整數</td></tr><tr><td><code class="type">bit [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td> </td><td>固定長度的位元字串</td></tr><tr><td><code class="type">bit varying [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td><code class="type">varbit [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td>可變長度的位元字串</td></tr><tr><td><code class="type">boolean</code></td><td><code class="type">bool</code></td><td>邏輯布林值（true/false）</td></tr><tr><td><code class="type">box</code></td><td> </td><td>平面上的矩形</td></tr><tr><td><code class="type">bytea</code></td><td> </td><td>二進位資料（<span class="quote">「<span class="quote">位元組陣列</span>」</span>）</td></tr><tr><td><code class="type">character [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td><code class="type">char [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td>固定長度的字元字串</td></tr><tr><td><code class="type">character varying [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td><code class="type">varchar [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td>可變長度的字元字串</td></tr><tr><td><code class="type">cidr</code></td><td> </td><td>IPv4 或 IPv6 網路位址</td></tr><tr><td><code class="type">circle</code></td><td> </td><td>平面上的圓</td></tr><tr><td><code class="type">date</code></td><td> </td><td>日曆日期（年、月、日）</td></tr><tr><td><code class="type">double precision</code></td><td><code class="type">float</code>, <code class="type">float8</code></td><td>倍精度浮點數（8 個位元組）</td></tr><tr><td><code class="type">inet</code></td><td> </td><td>IPv4 或 IPv6 主機位址</td></tr><tr><td><code class="type">integer</code></td><td><code class="type">int</code>, <code class="type">int4</code></td><td>有號四位元組整數</td></tr><tr><td><code class="type">interval [ <em class="replaceable"><code>fields</code></em> ] [ (<em class="replaceable"><code>p</code></em>) ]</code></td><td> </td><td>時間長度</td></tr><tr><td><code class="type">json</code></td><td> </td><td>文字形式的 JSON 資料</td></tr><tr><td><code class="type">jsonb</code></td><td> </td><td>二進位形式的 JSON 資料，已分解</td></tr><tr><td><code class="type">line</code></td><td> </td><td>平面上無限延伸的直線</td></tr><tr><td><code class="type">lseg</code></td><td> </td><td>平面上的線段</td></tr><tr><td><code class="type">macaddr</code></td><td> </td><td>MAC（Media Access Control）位址</td></tr><tr><td><code class="type">macaddr8</code></td><td> </td><td>MAC（Media Access Control）位址（EUI-64 格式）</td></tr><tr><td><code class="type">money</code></td><td> </td><td>貨幣金額</td></tr><tr><td><code class="type">numeric [ (<em class="replaceable"><code>p</code></em>,
         <em class="replaceable"><code>s</code></em>) ]</code></td><td><code class="type">decimal [ (<em class="replaceable"><code>p</code></em>,
         <em class="replaceable"><code>s</code></em>) ]</code></td><td>可指定精度的精確數值</td></tr><tr><td><code class="type">path</code></td><td> </td><td>平面上的幾何路徑</td></tr><tr><td><code class="type">pg_lsn</code></td><td> </td><td><span class="productname">PostgreSQL</span> 日誌序號（Log Sequence Number）</td></tr><tr><td><code class="type">pg_snapshot</code></td><td> </td><td>使用者層級的交易 ID 快照</td></tr><tr><td><code class="type">point</code></td><td> </td><td>平面上的幾何點</td></tr><tr><td><code class="type">polygon</code></td><td> </td><td>平面上的封閉幾何路徑</td></tr><tr><td><code class="type">real</code></td><td><code class="type">float4</code></td><td>單精度浮點數（4 個位元組）</td></tr><tr><td><code class="type">smallint</code></td><td><code class="type">int2</code></td><td>有號二位元組整數</td></tr><tr><td><code class="type">smallserial</code></td><td><code class="type">serial2</code></td><td>自動遞增的二位元組整數</td></tr><tr><td><code class="type">serial</code></td><td><code class="type">serial4</code></td><td>自動遞增的四位元組整數</td></tr><tr><td><code class="type">text</code></td><td> </td><td>可變長度的字元字串</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td> </td><td>一天中的時間（不含時區）</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td><code class="type">timetz</code></td><td>一天中的時間，包含時區</td></tr><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td> </td><td>日期與時間（不含時區）</td></tr><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td><code class="type">timestamptz</code></td><td>日期與時間，包含時區</td></tr><tr><td><code class="type">tsquery</code></td><td> </td><td>全文檢索查詢</td></tr><tr><td><code class="type">tsvector</code></td><td> </td><td>全文檢索文件</td></tr><tr><td><code class="type">txid_snapshot</code></td><td> </td><td>使用者層級的交易 ID 快照（已棄用；請參閱 <code class="type">pg_snapshot</code>）</td></tr><tr><td><code class="type">uuid</code></td><td> </td><td>通用唯一識別碼</td></tr><tr><td><code class="type">xml</code></td><td> </td><td>XML 資料</td></tr></tbody></table>

<br>

<a id="id-1.5.7.4"></a>

### 相容性

下列型別（或其寫法）是由 SQL 所規定的：`bigint`、`bit`、`bit varying`、`boolean`、`char`、`character varying`、`character`、`varchar`、`date`、`double precision`、`integer`、`interval`、`numeric`、`decimal`、`real`、`smallint`、`time`（含或不含時區）、`timestamp`（含或不含時區）、`xml`。

每種資料型別都有由其輸入與輸出函式所決定的外部表示法。許多內建型別具有顯而易見的外部格式。不過有幾種型別是 PostgreSQL 所特有的，例如幾何路徑；或者具有多種可能的格式，例如日期與時間型別。有些輸入與輸出函式並非可逆的，也就是說，輸出函式的結果與原本的輸入相比可能會損失精確度。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype.html)（原文版本：18.6；核對日期：2026-09-13）
