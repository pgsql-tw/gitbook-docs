<a id="FUNCTIONS-XML"></a>

## 9.15. XML 函式 [#](#FUNCTIONS-XML)

[9.15.1. 產生 XML 內容](functions-xml.md#FUNCTIONS-PRODUCING-XML)

[9.15.2. XML 述詞](functions-xml.md#FUNCTIONS-XML-PREDICATES)

[9.15.3. 處理 XML](functions-xml.md#FUNCTIONS-XML-PROCESSING)

[9.15.4. 將資料表對應到 XML](functions-xml.md#FUNCTIONS-XML-MAPPING)

<a id="id-1.5.8.21.2"></a>

本節所說明的函式與類函式運算式，都作用在 `xml` 型別的值上。關於 `xml` 型別的資訊，請參閱[第 8.13 節](../datatype/datatype-xml.md)。用於與 `xml` 型別互相轉換的類函式運算式 `xmlparse` 與 `xmlserialize`，記載於該節，而不在本節中。

大多數這些函式都需要 PostgreSQL 在建置時使用了 `configure --with-libxml`。

<a id="FUNCTIONS-PRODUCING-XML"></a>

### 9.15.1. 產生 XML 內容 [#](#FUNCTIONS-PRODUCING-XML)

有一組函式與類函式運算式，可用於從 SQL 資料產生 XML 內容。因此，它們特別適合用來將查詢結果格式化為 XML 文件，以便在用戶端應用程式中處理。

<a id="FUNCTIONS-PRODUCING-XML-XMLTEXT"></a>

#### 9.15.1.1. `xmltext` [#](#FUNCTIONS-PRODUCING-XML-XMLTEXT)

<a id="id-1.5.8.21.5.3.2"></a>

```

xmltext ( text ) → xml
```

函式 `xmltext` 會回傳一個 XML 值，其中包含一個以輸入引數為內容的單一文字節點。預先定義的實體，例如 & 符號（`&`）、左右角括號（`< >`）以及引號（`""`），都會被跳脫。

範例：

```

SELECT xmltext('< foo & bar >');
         xmltext
-------------------------
 &lt; foo &amp; bar &gt;
```

<a id="FUNCTIONS-PRODUCING-XML-XMLCOMMENT"></a>

#### 9.15.1.2. `xmlcomment` [#](#FUNCTIONS-PRODUCING-XML-XMLCOMMENT)

<a id="id-1.5.8.21.5.4.2"></a>

```

xmlcomment ( text ) → xml
```

函式 `xmlcomment` 會建立一個 XML 值，其中包含一個以指定文字為內容的 XML 註解。該文字不能包含「`--`」，也不能以「`-`」結尾，否則產生的結構就不會是有效的 XML 註解。如果引數為 null，結果就是 null。

範例：

```

SELECT xmlcomment('hello');

  xmlcomment
--------------
 <!--hello-->
```

<a id="FUNCTIONS-PRODUCING-XML-XMLCONCAT"></a>

#### 9.15.1.3. `xmlconcat` [#](#FUNCTIONS-PRODUCING-XML-XMLCONCAT)

<a id="id-1.5.8.21.5.5.2"></a>

```

xmlconcat ( xml [, ...] ) → xml
```

函式 `xmlconcat` 會串接一串個別的 XML 值，建立一個包含 XML 內容片段的單一值。null 值會被省略；只有在沒有任何非 null 引數時，結果才會是 null。

範例：

```

SELECT xmlconcat('<abc/>', '<bar>foo</bar>');

      xmlconcat
----------------------
 <abc/><bar>foo</bar>
```

XML 宣告（如果有的話）會依下列方式合併。如果所有引數值都有相同的 XML 版本宣告，結果就會使用該版本，否則不使用任何版本。如果所有引數值的 standalone 宣告值都是「yes」，結果就會使用該值。如果所有引數值都有 standalone 宣告值，而且至少有一個是「no」，結果就會使用「no」。否則結果不會有 standalone 宣告。如果判定結果需要 standalone 宣告但沒有版本宣告，就會使用版本 1.0 的版本宣告，因為 XML 要求 XML 宣告必須包含版本宣告。在所有情況下，編碼宣告都會被忽略並移除。

範例：

```

SELECT xmlconcat('<?xml version="1.1"?><foo/>', '<?xml version="1.1" standalone="no"?><bar/>');

             xmlconcat
-----------------------------------
 <?xml version="1.1"?><foo/><bar/>
```

<a id="FUNCTIONS-PRODUCING-XML-XMLELEMENT"></a>

#### 9.15.1.4. `xmlelement` [#](#FUNCTIONS-PRODUCING-XML-XMLELEMENT)

<a id="id-1.5.8.21.5.6.2"></a>

```

xmlelement ( NAME name [, XMLATTRIBUTES ( attvalue [ AS attname ] [, ...] ) ] [, content [, ...]] ) → xml
```

`xmlelement` 運算式會產生一個具有給定名稱、屬性與內容的 XML 元素。語法中所示的 *`name`* 與 *`attname`* 項目是簡單的識別符號，而不是值。*`attvalue`* 與 *`content`* 項目則是運算式，可以產生任何 PostgreSQL 資料型別。`XMLATTRIBUTES` 中的引數會產生 XML 元素的屬性；*`content`* 值會被串接起來，形成元素的內容。

範例：

```

SELECT xmlelement(name foo);

 xmlelement
------------
 <foo/>

SELECT xmlelement(name foo, xmlattributes('xyz' as bar));

    xmlelement
------------------
 <foo bar="xyz"/>

SELECT xmlelement(name foo, xmlattributes(current_date as bar), 'cont', 'ent');

             xmlelement
-------------------------------------
 <foo bar="2007-01-26">content</foo>
```

不是有效 XML 名稱的元素與屬性名稱，會以序列 `_xHHHH_` 取代有問題的字元來加以跳脫，其中 *`HHHH`* 是該字元以十六進位表示的 Unicode 碼位。例如：

```

SELECT xmlelement(name "foo$bar", xmlattributes('xyz' as "a&b"));

            xmlelement
----------------------------------
 <foo_x0024_bar a_x0026_b="xyz"/>
```

如果屬性值是欄位參照，就不需要指定明確的屬性名稱，在這種情況下，預設會使用欄位的名稱作為屬性名稱。在其他情況下，必須為屬性指定明確的名稱。因此，這個範例是有效的：

```

CREATE TABLE test (a xml, b xml);
SELECT xmlelement(name test, xmlattributes(a, b)) FROM test;
```

但下面這些則無效：

```

SELECT xmlelement(name test, xmlattributes('constant'), a, b) FROM test;
SELECT xmlelement(name test, xmlattributes(func(a, b))) FROM test;
```

元素內容（如果有指定的話）會依照其資料型別進行格式化。如果內容本身是 `xml` 型別，就可以建構複雜的 XML 文件。例如：

```

SELECT xmlelement(name foo, xmlattributes('xyz' as bar),
                            xmlelement(name abc),
                            xmlcomment('test'),
                            xmlelement(name xyz));

                  xmlelement
----------------------------------------------
 <foo bar="xyz"><abc/><!--test--><xyz/></foo>
```

其他型別的內容會被格式化為有效的 XML 字元資料。這特別表示字元 <、> 與 & 會被轉換為實體。二進位資料（資料型別 `bytea`）會以 base64 或十六進位編碼表示，取決於組態參數 [xmlbinary](../../server-administration/runtime-config/runtime-config-client.md#GUC-XMLBINARY) 的設定。個別資料型別的特定行為預期會逐步演進，以使 PostgreSQL 的對應方式與 SQL:2006 及之後版本所規定的一致，如[第 D.3.1.3 節](../../appendixes/features/xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-CASTS)所述。

<a id="FUNCTIONS-PRODUCING-XML-XMLFOREST"></a>

#### 9.15.1.5. `xmlforest` [#](#FUNCTIONS-PRODUCING-XML-XMLFOREST)

<a id="id-1.5.8.21.5.7.2"></a>

```

xmlforest ( content [ AS name ] [, ...] ) → xml
```

`xmlforest` 運算式會使用給定的名稱與內容，產生一個由元素組成的 XML 森林（序列）。與 `xmlelement` 一樣，每個 *`name`* 都必須是簡單的識別符號，而 *`content`* 運算式可以是任何資料型別。

範例：

```

SELECT xmlforest('abc' AS foo, 123 AS bar);

          xmlforest
------------------------------
 <foo>abc</foo><bar>123</bar>


SELECT xmlforest(table_name, column_name)
FROM information_schema.columns
WHERE table_schema = 'pg_catalog';

                                xmlforest
------------------------------------​-----------------------------------
 <table_name>pg_authid</table_name>​<column_name>rolname</column_name>
 <table_name>pg_authid</table_name>​<column_name>rolsuper</column_name>
 ...
```

如第二個範例所示，如果內容值是欄位參照，就可以省略元素名稱，在這種情況下預設會使用欄位名稱。否則必須指定名稱。

不是有效 XML 名稱的元素名稱，會如上面 `xmlelement` 所示的方式跳脫。同樣地，內容資料會被跳脫以成為有效的 XML 內容，除非它已經是 `xml` 型別。

請注意，如果 XML 森林由不只一個元素組成，它就不是有效的 XML 文件，因此將 `xmlforest` 運算式包在 `xmlelement` 中可能會很有用。

<a id="FUNCTIONS-PRODUCING-XML-XMLPI"></a>

#### 9.15.1.6. `xmlpi` [#](#FUNCTIONS-PRODUCING-XML-XMLPI)

<a id="id-1.5.8.21.5.8.2"></a>

```

xmlpi ( NAME name [, content ] ) → xml
```

`xmlpi` 運算式會建立一個 XML 處理指令。與 `xmlelement` 一樣，*`name`* 必須是簡單的識別符號，而 *`content`* 運算式可以是任何資料型別。*`content`*（如果有的話）不得包含字元序列 `?>`。

範例：

```

SELECT xmlpi(name php, 'echo "hello world";');

            xmlpi
-----------------------------
 <?php echo "hello world";?>
```

<a id="FUNCTIONS-PRODUCING-XML-XMLROOT"></a>

#### 9.15.1.7. `xmlroot` [#](#FUNCTIONS-PRODUCING-XML-XMLROOT)

<a id="id-1.5.8.21.5.9.2"></a>

```

xmlroot ( xml, VERSION {text|NO VALUE} [, STANDALONE {YES|NO|NO VALUE} ] ) → xml
```

`xmlroot` 運算式會改變 XML 值之根節點的屬性。如果指定了版本，它會取代根節點版本宣告中的值；如果指定了 standalone 設定，它會取代根節點 standalone 宣告中的值。

```

SELECT xmlroot(xmlparse(document '<?xml version="1.1"?><content>abc</content>'),
               version '1.0', standalone yes);

                xmlroot
----------------------------------------
 <?xml version="1.0" standalone="yes"?>
 <content>abc</content>
```

<a id="FUNCTIONS-XML-XMLAGG"></a>

#### 9.15.1.8. `xmlagg` [#](#FUNCTIONS-XML-XMLAGG)

<a id="id-1.5.8.21.5.10.2"></a>

```

xmlagg ( xml ) → xml
```

與這裡所說明的其他函式不同，函式 `xmlagg` 是一個彙總函式。它會串接彙總函式呼叫的輸入值，很像 `xmlconcat` 所做的，只是串接是跨資料列進行，而不是跨單一資料列中的運算式進行。關於彙總函式的更多資訊，請參閱[第 9.21 節](functions-aggregate.md)。

範例：

```

CREATE TABLE test (y int, x xml);
INSERT INTO test VALUES (1, '<foo>abc</foo>');
INSERT INTO test VALUES (2, '<bar/>');
SELECT xmlagg(x) FROM test;
        xmlagg
----------------------
 <foo>abc</foo><bar/>
```

要決定串接的順序，可以如[第 4.2.7 節](../sql-syntax/sql-expressions.md#SYNTAX-AGGREGATES)所述，在彙總呼叫中加上 `ORDER BY` 子句。例如：

```

SELECT xmlagg(x ORDER BY y DESC) FROM test;
        xmlagg
----------------------
 <bar/><foo>abc</foo>
```

下面這種非標準的做法在先前的版本中曾被推薦，在特定情況下可能仍然有用：

```

SELECT xmlagg(x) FROM (SELECT * FROM test ORDER BY y DESC) AS tab;
        xmlagg
----------------------
 <bar/><foo>abc</foo>
```

<a id="FUNCTIONS-XML-PREDICATES"></a>

### 9.15.2. XML 述詞 [#](#FUNCTIONS-XML-PREDICATES)

本節所說明的運算式會檢查 `xml` 值的特性。

<a id="FUNCTIONS-PRODUCING-XML-IS-DOCUMENT"></a>

#### 9.15.2.1. `IS DOCUMENT` [#](#FUNCTIONS-PRODUCING-XML-IS-DOCUMENT)

<a id="id-1.5.8.21.6.3.2"></a>

```

xml IS DOCUMENT → boolean
```

如果引數的 XML 值是正確的 XML 文件，運算式 `IS DOCUMENT` 就回傳 true；如果不是（也就是它是內容片段），則回傳 false；如果引數為 null，則回傳 null。關於文件與內容片段之間的差異，請參閱[第 8.13 節](../datatype/datatype-xml.md)。

<a id="FUNCTIONS-PRODUCING-XML-IS-NOT-DOCUMENT"></a>

#### 9.15.2.2. `IS NOT DOCUMENT` [#](#FUNCTIONS-PRODUCING-XML-IS-NOT-DOCUMENT)

<a id="id-1.5.8.21.6.4.2"></a>

```

xml IS NOT DOCUMENT → boolean
```

如果引數的 XML 值是正確的 XML 文件，運算式 `IS NOT DOCUMENT` 就回傳 false；如果不是（也就是它是內容片段），則回傳 true；如果引數為 null，則回傳 null。

<a id="XML-EXISTS"></a>

#### 9.15.2.3. `XMLEXISTS` [#](#XML-EXISTS)

<a id="id-1.5.8.21.6.5.2"></a>

```

XMLEXISTS ( text PASSING [BY {REF|VALUE}] xml [BY {REF|VALUE}] ) → boolean
```

函式 `xmlexists` 會以傳入的 XML 值作為其情境項目，評估一個 XPath 1.0 運算式（第一個引數）。如果評估的結果是空的節點集合，函式就回傳 false；如果產生任何其他值，則回傳 true。如果有任何引數為 null，函式就回傳 null。作為情境項目傳入的非 null 值必須是 XML 文件，而不能是內容片段或任何非 XML 的值。

範例：

```

SELECT xmlexists('//town[text() = ''Toronto'']' PASSING BY VALUE '<towns><town>Toronto</town><town>Ottawa</town></towns>');

 xmlexists
------------
 t
(1 row)
```

PostgreSQL 接受 `BY REF` 與 `BY VALUE` 子句，但會忽略它們，如[第 D.3.2 節](../../appendixes/features/xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL)所述。

在 SQL 標準中，`xmlexists` 函式評估的是 XML Query 語言的運算式，但 PostgreSQL 只允許 XPath 1.0 運算式，如[第 D.3.1 節](../../appendixes/features/xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-XPATH1)所述。

<a id="XML-IS-WELL-FORMED"></a>

#### 9.15.2.4. `xml_is_well_formed` [#](#XML-IS-WELL-FORMED)

<a id="id-1.5.8.21.6.6.2"></a><a id="id-1.5.8.21.6.6.3"></a><a id="id-1.5.8.21.6.6.4"></a>

```

xml_is_well_formed ( text ) → boolean
xml_is_well_formed_document ( text ) → boolean
xml_is_well_formed_content ( text ) → boolean
```

這些函式會檢查 `text` 字串是否代表格式正確的 XML，並回傳布林結果。`xml_is_well_formed_document` 檢查格式正確的文件，而 `xml_is_well_formed_content` 檢查格式正確的內容。如果 [xmloption](../../server-administration/runtime-config/runtime-config-client.md#GUC-XMLOPTION) 組態參數設為 `DOCUMENT`，`xml_is_well_formed` 會進行前者的檢查；如果設為 `CONTENT`，則進行後者的檢查。這表示 `xml_is_well_formed` 可以用來查看簡單地轉換為 `xml` 型別是否會成功，而另外兩個函式則可以用來查看 `XMLPARSE` 的對應變化形式是否會成功。

範例：

```

SET xmloption TO DOCUMENT;
SELECT xml_is_well_formed('<>');
 xml_is_well_formed
--------------------
 f
(1 row)

SELECT xml_is_well_formed('<abc/>');
 xml_is_well_formed
--------------------
 t
(1 row)

SET xmloption TO CONTENT;
SELECT xml_is_well_formed('abc');
 xml_is_well_formed
--------------------
 t
(1 row)

SELECT xml_is_well_formed_document('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</pg:foo>');
 xml_is_well_formed_document
-----------------------------
 t
(1 row)

SELECT xml_is_well_formed_document('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</my:foo>');
 xml_is_well_formed_document
-----------------------------
 f
(1 row)
```

最後一個範例顯示，這些檢查也包括命名空間是否正確對應。

<a id="FUNCTIONS-XML-PROCESSING"></a>

### 9.15.3. 處理 XML [#](#FUNCTIONS-XML-PROCESSING)

為了處理 `xml` 資料型別的值，PostgreSQL 提供了評估 XPath 1.0 運算式的函式 `xpath` 與 `xpath_exists`，以及 `XMLTABLE` 資料表函式。

<a id="FUNCTIONS-XML-PROCESSING-XPATH"></a>

#### 9.15.3.1. `xpath` [#](#FUNCTIONS-XML-PROCESSING-XPATH)

<a id="id-1.5.8.21.7.3.2"></a>

```

xpath ( xpath text, xml xml [, nsarray text[] ] ) → xml[]
```

函式 `xpath` 會針對 XML 值 *`xml`* 評估 XPath 1.0 運算式 *`xpath`*（以文字形式提供）。它會回傳一個 XML 值陣列，對應於該 XPath 運算式所產生的節點集合。如果 XPath 運算式回傳的是純量值而不是節點集合，就會回傳一個單一元素的陣列。

第二個引數必須是格式正確的 XML 文件。特別是，它必須有單一的根節點元素。

函式選用的第三個引數是一個命名空間對應陣列。這個陣列應該是一個二維的 `text` 陣列，其第二個軸的長度等於 2（也就是說，它應該是一個由陣列組成的陣列，每個陣列正好由 2 個元素組成）。每個陣列項目的第一個元素是命名空間名稱（別名），第二個元素是命名空間 URI。這個陣列中所提供的別名，不必與 XML 文件本身所使用的別名相同（換句話說，無論在 XML 文件中還是在 `xpath` 函式的情境中，別名都是*區域性的*）。

範例：

```

SELECT xpath('/my:a/text()', '<my:a xmlns:my="http://example.com">test</my:a>',
             ARRAY[ARRAY['my', 'http://example.com']]);

 xpath
--------
 {test}
(1 row)
```

要處理預設（匿名）命名空間，可以這樣做：

```

SELECT xpath('//mydefns:b/text()', '<a xmlns="http://example.com"><b>test</b></a>',
             ARRAY[ARRAY['mydefns', 'http://example.com']]);

 xpath
--------
 {test}
(1 row)
```

<a id="FUNCTIONS-XML-PROCESSING-XPATH-EXISTS"></a>

#### 9.15.3.2. `xpath_exists` [#](#FUNCTIONS-XML-PROCESSING-XPATH-EXISTS)

<a id="id-1.5.8.21.7.4.2"></a>

```

xpath_exists ( xpath text, xml xml [, nsarray text[] ] ) → boolean
```

函式 `xpath_exists` 是 `xpath` 函式的一種特殊形式。這個函式不會回傳滿足 XPath 1.0 運算式的個別 XML 值，而是回傳一個布林值，指出查詢是否被滿足（具體來說，就是它是否產生了空節點集合以外的任何值）。這個函式等同於 `XMLEXISTS` 述詞，只是它還支援命名空間對應引數。

範例：

```

SELECT xpath_exists('/my:a/text()', '<my:a xmlns:my="http://example.com">test</my:a>',
                     ARRAY[ARRAY['my', 'http://example.com']]);

 xpath_exists
--------------
 t
(1 row)
```

<a id="FUNCTIONS-XML-PROCESSING-XMLTABLE"></a>

#### 9.15.3.3. `xmltable` [#](#FUNCTIONS-XML-PROCESSING-XMLTABLE)

<a id="id-1.5.8.21.7.5.2"></a><a id="id-1.5.8.21.7.5.3"></a>

```

XMLTABLE (
    [ XMLNAMESPACES ( namespace_uri AS namespace_name [, ...] ), ]
    row_expression PASSING [BY {REF|VALUE}] document_expression [BY {REF|VALUE}]
    COLUMNS name { type [PATH column_expression] [DEFAULT default_expression] [NOT NULL | NULL]
                  | FOR ORDINALITY }
            [, ...]
) → setof record
```

`xmltable` 運算式會根據一個 XML 值、一個用來擷取資料列的 XPath 過濾器，以及一組欄位定義，產生一個資料表。雖然它在語法上類似函式，但它只能以資料表的形式出現在查詢的 `FROM` 子句中。

選用的 `XMLNAMESPACES` 子句提供一份以逗號分隔的命名空間定義清單，其中每個 *`namespace_uri`* 都是一個 `text` 運算式，而每個 *`namespace_name`* 都是一個簡單的識別符號。它指定文件中所使用的 XML 命名空間及其別名。目前不支援預設命名空間規格。

必要的 *`row_expression`* 引數是一個 XPath 1.0 運算式（以 `text` 提供），評估時會將 XML 值 *`document_expression`* 作為其情境項目傳入，以取得一組 XML 節點。`xmltable` 會將這些節點轉換為輸出資料列。如果 *`document_expression`* 為 null，或者 *`row_expression`* 產生空的節點集合或節點集合以外的任何值，就不會產生任何資料列。

*`document_expression`* 為 *`row_expression`* 提供情境項目。它必須是格式正確的 XML 文件；不接受片段／森林。`BY REF` 與 `BY VALUE` 子句會被接受但忽略，如[第 D.3.2 節](../../appendixes/features/xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL)所述。

在 SQL 標準中，`xmltable` 函式評估的是 XML Query 語言的運算式，但 PostgreSQL 只允許 XPath 1.0 運算式，如[第 D.3.1 節](../../appendixes/features/xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-XPATH1)所述。

必要的 `COLUMNS` 子句指定將在輸出資料表中產生的欄位。格式請見上面的語法摘要。每個欄位都需要一個名稱，也需要一個資料型別（除非指定了 `FOR ORDINALITY`，在這種情況下隱含為 `integer` 型別）。路徑、預設值與可否為 null 的子句則是選用的。

標記為 `FOR ORDINALITY` 的欄位，會依照從 *`row_expression`* 的結果節點集合取得節點的順序，填入從 1 開始的資料列編號。最多只能有一個欄位標記為 `FOR ORDINALITY`。

### 注意

XPath 1.0 並未規定節點集合中節點的順序，因此依賴結果之特定順序的程式碼將取決於實作。詳情請參閱[第 D.3.1.2 節](../../appendixes/features/xml-limits-conformance.md#XML-XPATH-1-SPECIFICS)。

欄位的 *`column_expression`* 是一個 XPath 1.0 運算式，會針對每一筆資料列評估，並以 *`row_expression`* 結果中的目前節點作為其情境項目，以求得該欄位的值。如果沒有給定 *`column_expression`*，就會使用欄位名稱作為隱含的路徑。

如果欄位的 XPath 運算式回傳非 XML 的值（在 XPath 1.0 中僅限於字串、布林值或 double），而該欄位的 PostgreSQL 型別不是 `xml`，該欄位的設定方式，就如同將該值的字串表示指派給該 PostgreSQL 型別一樣。（如果值是布林值，當輸出欄位的型別類別為數值時，其字串表示會被視為 `1` 或 `0`，否則視為 `true` 或 `false`。）

如果欄位的 XPath 運算式回傳非空的 XML 節點集合，而該欄位的 PostgreSQL 型別是 `xml`，只要運算式的結果是文件或內容形式，就會被原封不動地指派給該欄位。[<a id="id-1.5.8.21.7.5.15.2"></a>[8]](#ftn.id-1.5.8.21.7.5.15.2)

指派給 `xml` 輸出欄位的非 XML 結果會產生內容，也就是一個具有該結果字串值的單一文字節點。指派給任何其他型別欄位的 XML 結果不得有超過一個節點，否則會引發錯誤。如果正好有一個節點，該欄位的設定方式，就如同將該節點的字串值（依照 XPath 1.0 `string` 函式的定義）指派給該 PostgreSQL 型別一樣。

XML 元素的字串值，是依文件順序串接該元素及其後代中所包含之所有文字節點的結果。沒有後代文字節點之元素的字串值是空字串（而不是 `NULL`）。任何 `xsi:nil` 屬性都會被忽略。請注意，兩個非文字元素之間只包含空白的 `text()` 節點會被保留，而且 `text()` 節點上的前導空白不會被壓平。關於定義其他 XML 節點類型與非 XML 值之字串值的規則，可以參考 XPath 1.0 的 `string` 函式。

這裡所介紹的轉換規則並不完全是 SQL 標準的規則，如[第 D.3.1.3 節](../../appendixes/features/xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-CASTS)所述。

如果路徑運算式對某筆資料列回傳空的節點集合（通常是在它不相符時），該欄位就會被設為 `NULL`，除非指定了 *`default_expression`*；在那種情況下，會使用評估該運算式所得的值。

*`default_expression`* 並不是在呼叫 `xmltable` 時立即評估，而是在每次需要該欄位的預設值時才評估。如果該運算式符合 stable 或 immutable 的條件，就可能略過重複的評估。這表示你可以在 *`default_expression`* 中有效地使用像 `nextval` 這樣的 volatile 函式。

欄位可以標記為 `NOT NULL`。如果 `NOT NULL` 欄位的 *`column_expression`* 沒有比對到任何東西，而且沒有 `DEFAULT`，或者 *`default_expression`* 的評估結果也是 null，就會回報錯誤。

範例：

```

CREATE TABLE xmldata AS SELECT
xml $$
<ROWS>
  <ROW id="1">
    <COUNTRY_ID>AU</COUNTRY_ID>
    <COUNTRY_NAME>Australia</COUNTRY_NAME>
  </ROW>
  <ROW id="5">
    <COUNTRY_ID>JP</COUNTRY_ID>
    <COUNTRY_NAME>Japan</COUNTRY_NAME>
    <PREMIER_NAME>Shinzo Abe</PREMIER_NAME>
    <SIZE unit="sq_mi">145935</SIZE>
  </ROW>
  <ROW id="6">
    <COUNTRY_ID>SG</COUNTRY_ID>
    <COUNTRY_NAME>Singapore</COUNTRY_NAME>
    <SIZE unit="sq_km">697</SIZE>
  </ROW>
</ROWS>
$$ AS data;

SELECT xmltable.*
  FROM xmldata,
       XMLTABLE('//ROWS/ROW'
                PASSING data
                COLUMNS id int PATH '@id',
                        ordinality FOR ORDINALITY,
                        "COUNTRY_NAME" text,
                        country_id text PATH 'COUNTRY_ID',
                        size_sq_km float PATH 'SIZE[@unit = "sq_km"]',
                        size_other text PATH
                             'concat(SIZE[@unit!="sq_km"], " ", SIZE[@unit!="sq_km"]/@unit)',
                        premier_name text PATH 'PREMIER_NAME' DEFAULT 'not specified');

 id | ordinality | COUNTRY_NAME | country_id | size_sq_km |  size_other  | premier_name
----+------------+--------------+------------+------------+--------------+---------------
  1 |          1 | Australia    | AU         |            |              | not specified
  5 |          2 | Japan        | JP         |            | 145935 sq_mi | Shinzo Abe
  6 |          3 | Singapore    | SG         |        697 |              | not specified
```

下面的範例展示了多個 text() 節點的串接、使用欄位名稱作為 XPath 過濾器，以及對空白、XML 註解與處理指令的處理方式：

```

CREATE TABLE xmlelements AS SELECT
xml $$
  <root>
   <element>  Hello<!-- xyxxz -->2a2<?aaaaa?> <!--x-->  bbb<x>xxx</x>CC  </element>
  </root>
$$ AS data;

SELECT xmltable.*
  FROM xmlelements, XMLTABLE('/root' PASSING data COLUMNS element text);
         element
-------------------------
   Hello2a2   bbbxxxCC
```

下面的範例說明如何使用 `XMLNAMESPACES` 子句，指定在 XML 文件以及 XPath 運算式中所使用的命名空間清單：

```

WITH xmldata(data) AS (VALUES ('
<example xmlns="http://example.com/myns" xmlns:B="http://example.com/b">
 <item foo="1" B:bar="2"/>
 <item foo="3" B:bar="4"/>
 <item foo="4" B:bar="5"/>
</example>'::xml)
)
SELECT xmltable.*
  FROM XMLTABLE(XMLNAMESPACES('http://example.com/myns' AS x,
                              'http://example.com/b' AS "B"),
             '/x:example/x:item'
                PASSING (SELECT data FROM xmldata)
                COLUMNS foo int PATH '@foo',
                  bar int PATH '@B:bar');
 foo | bar
-----+-----
   1 |   2
   3 |   4
   4 |   5
(3 rows)
```

<a id="FUNCTIONS-XML-MAPPING"></a>

### 9.15.4. 將資料表對應到 XML [#](#FUNCTIONS-XML-MAPPING)

<a id="id-1.5.8.21.8.2"></a>

下列函式會將關聯式資料表的內容對應到 XML 值。可以將它們想成是 XML 匯出功能：

```

table_to_xml ( table regclass, nulls boolean,
               tableforest boolean, targetns text ) → xml
query_to_xml ( query text, nulls boolean,
               tableforest boolean, targetns text ) → xml
cursor_to_xml ( cursor refcursor, count integer, nulls boolean,
                tableforest boolean, targetns text ) → xml
```

`table_to_xml` 會對應以參數 *`table`* 傳入之具名資料表的內容。`regclass` 型別接受以一般表示法識別資料表的字串，包括選用的綱要限定與雙引號（詳情請參閱[第 8.19 節](../datatype/datatype-oid.md)）。`query_to_xml` 會執行以參數 *`query`* 傳入其文字的查詢，並對應其結果集合。`cursor_to_xml` 會從參數 *`cursor`* 所指定的游標擷取指定數量的資料列。如果必須對應大型資料表，建議使用這個變化形式，因為每個函式都會在記憶體中建立結果值。

如果 *`tableforest`* 為 false，產生的 XML 文件會像這樣：

```

<tablename>
  <row>
    <columnname1>data</columnname1>
    <columnname2>data</columnname2>
  </row>

  <row>
    ...
  </row>

  ...
</tablename>
```

如果 *`tableforest`* 為 true，結果會是一個像這樣的 XML 內容片段：

```

<tablename>
  <columnname1>data</columnname1>
  <columnname2>data</columnname2>
</tablename>

<tablename>
  ...
</tablename>

...
```

如果沒有可用的資料表名稱，也就是在對應查詢或游標時，第一種格式會使用字串 `table`，第二種格式則使用 `row`。

要選擇哪一種格式由使用者決定。第一種格式是正確的 XML 文件，這在許多應用程式中都很重要。如果結果值之後要重新組合成一份文件，第二種格式在 `cursor_to_xml` 函式中往往會比較有用。上面所討論的產生 XML 內容的函式，特別是 `xmlelement`，可以用來依喜好修改結果。

資料值的對應方式，與上面函式 `xmlelement` 所說明的相同。

參數 *`nulls`* 決定輸出中是否應該包含 null 值。如果為 true，欄位中的 null 值會表示為：

```

<columnname xsi:nil="true"/>
```

其中 `xsi` 是 XML Schema Instance 的 XML 命名空間前綴。適當的命名空間宣告會被加入到結果值中。如果為 false，包含 null 值的欄位就會直接從輸出中省略。

參數 *`targetns`* 指定所需之結果的 XML 命名空間。如果不需要特定的命名空間，應該傳入空字串。

下列函式會回傳 XML Schema 文件，描述上面對應函式所執行的對應：

```

table_to_xmlschema ( table regclass, nulls boolean,
                     tableforest boolean, targetns text ) → xml
query_to_xmlschema ( query text, nulls boolean,
                     tableforest boolean, targetns text ) → xml
cursor_to_xmlschema ( cursor refcursor, nulls boolean,
                      tableforest boolean, targetns text ) → xml
```

為了得到相符的 XML 資料對應與 XML Schema 文件，傳入相同的參數是必要的。

下列函式會在一份文件（或森林）中，產生彼此連結的 XML 資料對應與對應的 XML Schema。當需要自成一體且能自我描述的結果時，它們可能會很有用：

```

table_to_xml_and_xmlschema ( table regclass, nulls boolean,
                             tableforest boolean, targetns text ) → xml
query_to_xml_and_xmlschema ( query text, nulls boolean,
                             tableforest boolean, targetns text ) → xml
```

此外，還有下列函式可用於產生整個綱要或整個目前資料庫的類似對應：

```

schema_to_xml ( schema name, nulls boolean,
                tableforest boolean, targetns text ) → xml
schema_to_xmlschema ( schema name, nulls boolean,
                      tableforest boolean, targetns text ) → xml
schema_to_xml_and_xmlschema ( schema name, nulls boolean,
                              tableforest boolean, targetns text ) → xml

database_to_xml ( nulls boolean,
                  tableforest boolean, targetns text ) → xml
database_to_xmlschema ( nulls boolean,
                        tableforest boolean, targetns text ) → xml
database_to_xml_and_xmlschema ( nulls boolean,
                                tableforest boolean, targetns text ) → xml
```

這些函式會忽略目前使用者無法讀取的資料表。整個資料庫範圍的函式還會另外忽略目前使用者沒有 `USAGE`（查找）權限的綱要。

請注意，這些函式可能會產生大量的資料，而這些資料需要在記憶體中建立。在要求大型綱要或資料庫的內容對應時，或許值得考慮改為個別對應資料表，甚至可能透過游標來進行。

綱要內容對應的結果如下所示：

```

<schemaname>

table1-mapping

table2-mapping

...

</schemaname>
```

其中資料表對應的格式，取決於上面所說明的 *`tableforest`* 參數。

資料庫內容對應的結果如下所示：

```

<dbname>

<schema1name>
  ...
</schema1name>

<schema2name>
  ...
</schema2name>

...

</dbname>
```

其中綱要對應如上所述。

作為使用這些函式所產生之輸出的範例，[範例 9.1](functions-xml.md#XSLT-XML-HTML) 展示了一份 XSLT 樣式表，它會將 `table_to_xml_and_xmlschema` 的輸出轉換為一份以表格呈現資料表資料的 HTML 文件。以類似的方式，這些函式的結果也可以轉換為其他以 XML 為基礎的格式。

<a id="XSLT-XML-HTML"></a>

**範例 9.1. 將 SQL/XML 輸出轉換為 HTML 的 XSLT 樣式表**

```

<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.w3.org/1999/xhtml"
>

  <xsl:output method="xml"
      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
      doctype-public="-//W3C/DTD XHTML 1.0 Strict//EN"
      indent="yes"/>

  <xsl:template match="/*">
    <xsl:variable name="schema" select="//xsd:schema"/>
    <xsl:variable name="tabletypename"
                  select="$schema/xsd:element[@name=name(current())]/@type"/>
    <xsl:variable name="rowtypename"
                  select="$schema/xsd:complexType[@name=$tabletypename]/xsd:sequence/xsd:element[@name='row']/@type"/>

    <html>
      <head>
        <title><xsl:value-of select="name(current())"/></title>
      </head>
      <body>
        <table>
          <tr>
            <xsl:for-each select="$schema/xsd:complexType[@name=$rowtypename]/xsd:sequence/xsd:element/@name">
              <th><xsl:value-of select="."/></th>
            </xsl:for-each>
          </tr>

          <xsl:for-each select="row">
            <tr>
              <xsl:for-each select="*">
                <td><xsl:value-of select="."/></td>
              </xsl:for-each>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
```

<br>

<br>

---

<a id="ftn.id-1.5.8.21.7.5.15.2"></a>

[[8]](#id-1.5.8.21.7.5.15.2) 
在最上層包含不只一個元素節點，或在元素之外有非空白文字的結果，就是內容形式的例子。XPath 結果也可能既不是文件形式也不是內容形式，例如當它回傳從包含它的元素中選出的屬性節點時。這樣的結果會被轉為內容形式，其中每個不被允許的節點都會被替換為其字串值（依照 XPath 1.0 `string` 函式的定義）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-xml.html)（原文版本：18.6；核對日期：2026-09-11）
