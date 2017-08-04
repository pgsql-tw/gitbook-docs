# 5.3. 限制條件[^1]

資料型別是一種限制資料如何被儲存在表格中的方式。然而，對許多應用來說，這樣的限制還是不夠細膩。舉個例子，一個欄位包含了產品價格，當然它必須只能是正整數，但並沒有標準的資料型別可以只限制在正整數。另一個需求是，你可能想要限制的條件是依據其他的資料而定。舉例來說，在表格中的產品資訊，每一個產品編號都不能重覆。

所以，SQL 允許你在表格和欄位上定義額外的限制條件，它幫助你對資料有更多的控制能力。當某個使用者輸入資料時，違反了限制條件，錯誤訊息就會產生。這些限制條件也會限制預設值的設定。

### 5.3.1. 檢查

使用 CHECK 是最普遍的限制條件製定方式，它可以允許你指定某個欄位必須符合某個布林條件式的判斷。舉個例子，要滿足產品價格是正數的話，你可以使用這樣的語法：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0)
);
```

如同你所看到的，限制條件會接在資料型別之後，就像是預設值的設定一樣。預設值和限制條件的設定，在語法撰寫上沒有先後次序。檢查限制條件使用關鍵字 CHECK，然後接著是一組以括號括起來的條件式。其條件式應該要包含被限制的欄位，不然就沒有任何意義。

你也可以讓該限制條件擁有另一個名稱，這樣的好處是，當錯誤訊息發生時，你可以明確得到是哪一個限制被違反了：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric 
CONSTRAINT positive_price CHECK (price > 0)
);
```

如上，給予這個限制條件一個名稱，使用關鍵字 CONSTRAINT，緊接著一個限制條件的定義。（如果你沒有自行命名，系統也會自動取一個名字）

一個限制條件可以參考多個欄位。例如你設定了標準價格和優惠價格，而你需要確保優惠價格一定是比標準價格要便宜的話：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

前兩個限制條件和前述很類似，而第三個是新的語法。它並不是只參考某個特定的欄位，而是以逗號分隔列出所有需要遵守的條件。欄位的定義和限制條件的定義，撰寫上沒有規定次序。

我們會說前兩個是欄位的限制，而第三個是表格的限制，因為它是獨立於其他的欄位定義的。欄位限制也可以寫成表格的限制方式，不過反過來通常就不行，因為一個欄位的限制，指的就是只參考到語法上它所接續的欄位而已。（PostgreSQL 並沒有強制這樣做，但如果你的語法與其他資料庫共用的話，最好還是依這樣的語法避免混用。）上面的例子也可以改寫成如此：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

或等同於：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0 AND price > discounted_price)
);
```

都可以照你所喜愛的語法撰寫。

命名表格的限制條件和欄位限制條件的命名是一樣的：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0),

    CONSTRAINT valid_discount CHECK (price > discounted_price)
);
```

應該要注意的是，檢查限制條件是否成立，端看條件表示式在運算後是真值（true）還是空值（null）。因為當有運算元是空值時，多數的運算結果都是空值，所以可能會有空值產生在想要限制條件的欄位之中。要確保欄位中不會出現空值的話，請參閱下一段的說明。

### 5.3.2. 限制無空值

限制無空值只要以下方的語法設定，就可以限制欄位不得存在空值的輸入：

```
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric
);
```

限制無空值的語法，只能使用在欄位限制上。而限制無空值等效於以 CHECK 建立一個限制條件式為（IS NOT NULL），但在 PostgreSQL 明確使用 NOT NULL 語法的話，處理會更快速。只是它的缺點是你無法給予這樣的限制一個自訂的名稱。

當然，一個欄位可以有一個以上的限制條件。只要一個接著一個即可：

```
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric NOT NULL CHECK (price > 0)
);
```

撰寫的次序沒有關係，也不需要去計較限制被檢查的次序。

NOT NULL 有一個相反的語法：NULL。這並非表示欄位裡只能是空值，如果這樣的話就完全沒用處了。其實這是一種簡化，將預設值設定為空值。NULL 語法並不是 SQL 標準的一部份，所以請不要用在可移植式的應用程式裡。（這僅是 PostgreSQL 為了相容其他資料庫而增加的功能）然而，有一些使用者喜歡使用它，因為在程序檔的撰寫上，很容易利用這個語法來切換限制條件。舉個例子，你可以先寫下：

```
CREATE TABLE products (
    product_no integer NULL,
    name text NULL,
    price numeric NULL
);
```

然後在需要的時候再適時加入 NOT 關鍵字即可。

### 小技巧

> 在多數資料庫設計原則上，主要欄位都應該被標示為 NOT NULL。

### 5.3.3. 限制唯一性

限制唯一性，確保在某個欄位或某一群欄位的資料，是在該表格中獨一無二的。語法如下：

```
CREATE TABLE products (
    product_no integer UNIQUE,
    name text,
    price numeric
);
```

這是欄位限制的語法。而：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
UNIQUE (product_no)
);
```

則是表格限制的寫法。

如果想要限制一群欄位的唯一性的話，請使用表格限制的語法，欄位名稱以逗號分隔：

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
UNIQUE (a, c)
);
```

這表示這些欄位所包含的內容組合，在整個表格中是具有唯一性的，但任何一個欄位本身並不一定具備唯一性。

你可以命名唯一性的限制條件，語法如下：

```
CREATE TABLE products (
    product_no integer CONSTRAINT must_be_different UNIQUE,
    name text,
    price numeric
);
```

加入唯一性的限制條件，將會自動建立一個具唯一性的 B-tree 索引，其包含的欄位就如限制條件中所條列的欄位。這樣唯一性限制的語法並不能只限制某部份列的唯一性，但如果使用「[部份索引 （partial index）](/ii-the-sql-language/indexes/118-partial-indexes.md) 」的話就可以做到。

一般來說，唯一性被違反的情況是，所限制的欄位在表格中，有超過一列的資料是相等的。不過，空值並不會被計算在內。這表示說，即使設定了唯一性的限制，在被限制的欄位中，還是有可能會有多個列的資料是空值。這個設計源自 SQL 標準，但聽說有其他的 SQL 資料庫並不是這樣的規則。所以，如果要移植這個語法到其他資料庫的話，要注意這項設計有無差異。

### 5.3.4. 主鍵（Primary Keys）

主鍵的意思是，某一個欄位或某一群欄位，在整個表格中，其每一列的組合都是唯一的，且有宣告唯一性的限制條件，並且也包含了非空值的條件（UNIQUE 及 NOT NULL）。所以，下面的兩種語法對資料的意義相同：

```
CREATE TABLE products (
    product_no integer UNIQUE NOT NULL,
    name text,
    price numeric
);
```

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

主鍵也可以包含多個欄位，語法和宣告唯一限制條件類似：

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,

PRIMARY KEY (a, c)
);
```

加入主鍵時，會自動建立一個具唯一性的 B-tree 索引，範圍為 PRIMARY KEY 語法所定義的欄位，並且會強制將這些欄位設定為非空值（NOT NULL）。

一個表格只能有一個主鍵。（你可以使用 UNIQUE 及 NOT NULL 設定多個同樣的限制條件，在功能上幾乎是相同的，但只能有一組條件是由 PRIMARY KEY 所定義。）關連式資料庫的理論指出，每一個表格都必須要有一個主鍵。這個規則在 PostgreSQL 中並不是強制的，但通常建議最好遵循這個理論。

主鍵在用戶端文件式的資料處理上是很有用的。舉個例子，一個圖型化介面讓使用者可以修改資料，那麼可能就需要主鍵來確認每一列的唯一性，而不致於產生混淆。也有一些用途是在資料庫系統的管理上，例如，主鍵會用於外部鍵（Foreign Keys）的處理，使其可以處理表格與表格間的資料對應問題。

### 5.3.5. 外部鍵（Foreign Keys）

外部鍵指的是某個欄位或某一群欄位的內容，必須在另一個表格相對欄位之中，存在相同內容的資料。我們會說這樣的行為是在維護兩個表格之間的關連性。

就使用我們已經使用多次的產品表格吧：

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

讓我們假設你有一個表格用來儲存這些產品的訂單，我們要確保這些訂單內的產品確實存在。所以我們定義一個外部鍵來關連訂單的表格和產品的表格：

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products (product_no),
    quantity integer
);
```

這樣的話，如果 product\_no 沒有出現在產品表格的話，就無法建立資料了。

我們會說像這樣的情況是，訂單表格是引用表格（referencing table），而產品表格是參考表格（referenced table）。相對地，欄位也稱為引用欄位（referencing columns）及參考欄位（referenced columns）。

你可以將這個語法簡化為：

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products,
    quantity integer
);
```

因為在參考表格中，不在主鍵欄位組合中的欄位，就是參考欄位。

外部鍵也可以參考一組欄位。一般來說，這樣要寫成表格限制條件形式，如下：

```
CREATE TABLE t1 (
  a integer PRIMARY KEY,
  b integer,
  c integer,

FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)
);
```

當然，組合外部鍵的欄位數量，彼此之間必須要相等。

你可以給外部鍵一個名稱，使用語法與限制條件相同。

一個表格可以有許多個外部鍵，這用於表格之間多對多的關係。例如你有一些表格記錄了很多產品和訂單，但現在你要讓每一筆訂單也可以訂購多項產品（這在先前的語法並不允許）。你也許可以試試這個表格宣告：

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products,
    order_id integer REFERENCES orders,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

注意到這裡的主鍵和外部鍵是重覆的。

我們知道外部鍵不允許沒有關連到產品的訂單，但如果企圖移除一個有訂單的產品會如何呢？SQL 有幾個選項讓你直覺進行這項操作：

* 不允許移除被參考到的產品
* 同時也刪去訂單
* 其他？

要描繪這些情況，讓我們建立如上需求的多對多關連的結構：當某人要移除一個有訂單的產品（以 order\_items 關連）時，我們不允許執行。而如果某人移除了一筆訂單，訂單內的項目也會同步被移除：

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products ON DELETE RESTRICT,
    order_id integer REFERENCES orders ON DELETE CASCADE,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

引用和同步刪除有兩個常見的作法。用「RESTRICT」防止參考的資料被刪除；「NO ACTION」表示當限制條件被違反時，引用欄位的資料仍會留存，然後回傳錯誤訊息，如果未指定處理方式的話，這會是預設的行為（這兩個語法根本上的不同是「NO ACTION」允許延遲檢查到交易事務的最後，而「RESTRICT」則不會。）；「CASCADE」指的是當參考的資料列被刪除時，引用的資料列也會同步被刪除。刪除時還有兩個其他的選項：SET NULL 和 SET DEFAULT，表示引用的資料會被更新為空值或其預設值。注意到，這並不是說你就可以違反限制條件。舉個例來說，如果使用了 SET DEFAULT，但預設值卻違反了外部鍵的限制，這個操作將會失敗。

類似的於 ON DELETE 的情況是 ON UPDATE，也就是在參考欄位的資料內容被更新時的情況。可以設定的動作關鍵字是相同的。在這個情況的 CASCADE 指的就是更新參考欄位的資料內容時，引用欄位的內容也會同步被更新為相同的內容。

一般來說，引用的資料列不需要滿足外部鍵的定義，如果其任一欄位內容為空值的話。而如果「MATCH FULL」加到宣告的語法之中的話，引用的資料列就必須要全部都是空值才不受外部鍵的限制（也就是部份空值的資料列就不受限制）。如果要避免空值使得外部鍵失效的話，就應該宣告相關欄位為 NOT NULL。

外部鍵所參考的欄位必須要是主鍵或是宣告其唯一性限制，這表示參考欄位會有索引存在，這使得檢查關連的過程會是很有效率的。因為在刪除或更新參考資料表時，需要檢查引用資料表的情況，所以在引用表格的欄位建立索引，也是常見的作法。因為這並不是一定需要，而還有許多的選擇在於如何索引，所以宣告外部鍵時並不會自行以引用欄位組合建立索引。

關於更新資料與刪除資料的細節在[第 6 章](/ii-the-sql-language/data-manipulation.md)。也可以在 [CREATE TABLE](/vi-reference/i-sql-commands/create-table.md) 語法說明中，找到更多外部鍵的說明。

### 5.3.6. Exclusion Constraints

Exclusion constraints ensure that if any two rows are compared on the specified columns or expressions using the specified operators, at least one of these operator comparisons will return false or null. The syntax is:

```
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

See also[`CREATE TABLE ... CONSTRAINT ... EXCLUDE`](https://www.postgresql.org/docs/10/static/sql-createtable.html#sql-createtable-exclude)for details.

Adding an exclusion constraint will automatically create an index of the type specified in the constraint declaration.

---

[^1]: [PostgreSQL: Documentation: 10: 5.3. Constraints](https://www.postgresql.org/docs/10/static/ddl-constraints.html)

