<a id="ECPG-VARIABLES-TYPE-MAPPING"></a>

## 34.4.4. 型別對應 [#](#ecpg-variables-type-mapping) <a href="#ecpg-variables-type-mapping" id="ecpg-variables-type-mapping"></a>

當 ECPG 應用程式在 PostgreSQL 伺服器與 C 應用程式之間交換值時，例如從伺服器取得查詢結果，或執行帶有輸入參數的 SQL 陳述式時，這些值需要在 PostgreSQL 資料型別與主機語言變數型別（具體而言就是 C 語言資料型別）之間轉換。ECPG 的重點之一，就是在大多數情況下會自動處理這件事。

就這方面而言，資料型別分為兩類：一些簡單的 PostgreSQL 資料型別，例如 `integer` 與 `text`，應用程式可以直接讀寫。其他 PostgreSQL 資料型別，例如 `timestamp` 與 `numeric`，則只能透過特殊的函式庫函式存取；請參閱[第 34.4.4.2 節](ecpg-variables-special-types.md#ecpg-special-types)。

[表 34.1](ecpg-variables-type-mapping.md#ECPG-DATATYPE-HOSTVARS-TABLE) 列出哪些 PostgreSQL 資料型別對應到哪些 C 資料型別。當你想要傳送或接收某個 PostgreSQL 資料型別的值時，應該在宣告區段中宣告對應 C 資料型別的 C 變數。

<a id="ECPG-DATATYPE-HOSTVARS-TABLE"></a>

**表 34.1. PostgreSQL 資料型別與 C 變數型別之間的對應**

<table border="1" class="table" summary="PostgreSQL 資料型別與 C 變數型別之間的對應"><colgroup><col/><col/></colgroup><thead><tr><th>PostgreSQL 資料型別</th><th>主機變數型別</th></tr></thead><tbody><tr><td><code class="type">smallint</code></td><td><code class="type">short</code></td></tr><tr><td><code class="type">integer</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">bigint</code></td><td><code class="type">long long int</code></td></tr><tr><td><code class="type">decimal</code></td><td><code class="type">decimal</code><a class="footnote" href="#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnote" id="ECPG-DATATYPE-TABLE-FN">[a]</sup></a></td></tr><tr><td><code class="type">numeric</code></td><td><code class="type">numeric</code><a class="footnoteref" href="ecpg-variables-type-mapping.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">real</code></td><td><code class="type">float</code></td></tr><tr><td><code class="type">double precision</code></td><td><code class="type">double</code></td></tr><tr><td><code class="type">smallserial</code></td><td><code class="type">short</code></td></tr><tr><td><code class="type">serial</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">bigserial</code></td><td><code class="type">long long int</code></td></tr><tr><td><code class="type">oid</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">character(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">varchar(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">text</code></td><td><code class="type">char[<em class="replaceable"><code>n</code></em>+1]</code>, <code class="type">VARCHAR[<em class="replaceable"><code>n</code></em>+1]</code></td></tr><tr><td><code class="type">name</code></td><td><code class="type">char[NAMEDATALEN]</code></td></tr><tr><td><code class="type">timestamp</code></td><td><code class="type">timestamp</code><a class="footnoteref" href="ecpg-variables-type-mapping.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">interval</code></td><td><code class="type">interval</code><a class="footnoteref" href="ecpg-variables-type-mapping.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">date</code></td><td><code class="type">date</code><a class="footnoteref" href="ecpg-variables-type-mapping.md#ftn.ECPG-DATATYPE-TABLE-FN"><sup class="footnoteref">[a]</sup></a></td></tr><tr><td><code class="type">boolean</code></td><td><code class="type">bool</code><a class="footnote" href="#ftn.id-1.7.5.10.7.5.2.2.17.2.2"><sup class="footnote" id="id-1.7.5.10.7.5.2.2.17.2.2">[b]</sup></a></td></tr><tr><td><code class="type">bytea</code></td><td><code class="type">char *</code>, <code class="type">bytea[<em class="replaceable"><code>n</code></em>]</code></td></tr></tbody><tbody class="footnotes"><tr><td colspan="2"><div class="footnote" id="ftn.ECPG-DATATYPE-TABLE-FN"><p><a class="para" href="#ECPG-DATATYPE-TABLE-FN"><sup class="para">[a] </sup></a>此型別只能透過特殊的函式庫函式存取；請參閱<a class="xref" href="ecpg-variables-special-types.md#ecpg-special-types">第 34.4.4.2 節</a>。</p></div><div class="footnote" id="ftn.id-1.7.5.10.7.5.2.2.17.2.2"><p><a class="para" href="#id-1.7.5.10.7.5.2.2.17.2.2"><sup class="para">[b] </sup></a>若非原生型別，則宣告於 <code class="filename">ecpglib.h</code></p></div></td></tr></tbody></table>

<br>

<a id="ECPG-CHAR"></a>

### 34.4.4.1. 處理字元字串 [#](#ecpg-char) <a href="#ecpg-char" id="ecpg-char"></a>

若要處理 SQL 字元字串資料型別，例如 `varchar` 與 `text`，宣告主機變數有兩種可行的方式。

一種是使用 `char[]`，也就是 `char` 的陣列，這是 C 語言中處理字元資料最常見的方式。

```

EXEC SQL BEGIN DECLARE SECTION;
    char str[50];
EXEC SQL END DECLARE SECTION;
```

請注意，你必須自行處理長度。如果你把這個主機變數用作某個查詢的目標變數，而該查詢傳回超過 49 個字元的字串，就會發生緩衝區溢位。

另一種方式是使用 `VARCHAR` 型別，這是 ECPG 提供的特殊型別。`VARCHAR` 型別陣列的定義，會針對每個變數轉換成一個具名的 `struct`。像這樣的宣告：

```

VARCHAR var[180];
```

會被轉換成：

```

struct varchar_var { int len; char arr[180]; } var;
```

成員 `arr` 存放字串，包含結尾的零位元組。因此，若要在 `VARCHAR` 主機變數中存放字串，宣告該主機變數時，長度必須把零位元組結尾符號也算進去。成員 `len` 存放 `arr` 中所儲存字串的長度，不含結尾的零位元組。當主機變數用作查詢的輸入時，若 `strlen(arr)` 與 `len` 不同，會使用較短的那一個。

`VARCHAR` 可以全部大寫或全部小寫，但不能大小寫混用。

`char` 與 `VARCHAR` 主機變數也可以存放其他 SQL 型別的值，這些值會以字串形式儲存。

<a id="ECPG-SPECIAL-TYPES"></a>

### 34.4.4.2. 存取特殊資料型別 [#](#ecpg-special-types) <a href="#ecpg-special-types" id="ecpg-special-types"></a>

本節內容請參閱[34.4.4.2. 存取特殊資料型別](ecpg-variables-special-types.md#ecpg-special-types)。

<a id="ECPG-VARIABLES-NONPRIMITIVE-C"></a>

### 34.4.4.3. 非基本型別的主機變數 [#](#ecpg-variables-nonprimitive-c) <a href="#ecpg-variables-nonprimitive-c" id="ecpg-variables-nonprimitive-c"></a>

本節內容請參閱[34.4.4.3. 非基本型別的主機變數](ecpg-variables-nonprimitive-c.md#ecpg-variables-nonprimitive-c)。

[返回 34.4. 使用主機變數](ecpg-variables.md#ecpg-variables)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-variables.html)（原文版本：18.6；核對日期：2026-10-18）
