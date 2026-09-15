<a id="DDL-CONSTRAINTS"></a>

## 5.5. 限制條件 [#](#DDL-CONSTRAINTS)

[5.5.1. 檢查限制條件](ddl-constraints.md#DDL-CONSTRAINTS-CHECK-CONSTRAINTS)

[5.5.2. 非空值限制條件](ddl-constraints.md#DDL-CONSTRAINTS-NOT-NULL)

[5.5.3. 唯一限制條件](ddl-constraints.md#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS)

[5.5.4. 主鍵](ddl-constraints.md#DDL-CONSTRAINTS-PRIMARY-KEYS)

[5.5.5. 外鍵](ddl-constraints.md#DDL-CONSTRAINTS-FK)

[5.5.6. 排除限制條件](ddl-constraints.md#DDL-CONSTRAINTS-EXCLUSION)

<a id="id-1.5.4.7.2"></a>

資料型別是限制資料表中所能儲存之資料種類的一種方法。然而，對許多應用來說，資料型別所提供的限制太過粗略。例如，存放產品價格的欄位大概只應該接受正數值。但是並沒有一種標準的資料型別只接受正數。另一個問題是，你可能想要依據其他欄位或資料列來限制某個欄位的資料。例如，在存放產品資訊的資料表中，每一個產品編號應該只有一筆資料列。

為此，SQL 讓你可以在欄位與資料表上定義限制條件。限制條件讓你能夠依自己的需要，盡可能地掌控資料表中的資料。如果使用者試圖在欄位中儲存會違反限制條件的資料，就會引發錯誤。即使該值來自預設值的定義，也同樣適用。

<a id="DDL-CONSTRAINTS-CHECK-CONSTRAINTS"></a>

### 5.5.1. 檢查限制條件 [#](#DDL-CONSTRAINTS-CHECK-CONSTRAINTS)

<a id="id-1.5.4.7.5.2"></a><a id="id-1.5.4.7.5.3"></a>

檢查限制條件是最通用的限制條件型式。它讓你可以指定某個欄位中的值必須滿足一個布林（真假值）運算式。例如，若要求產品價格必須為正數，你可以使用：

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0)
);
```

如你所見，限制條件的定義寫在資料型別之後，就像預設值的定義一樣。預設值與限制條件可以用任意順序列出。檢查限制條件由關鍵字 `CHECK` 加上一個放在括號中的運算式所構成。檢查限制條件的運算式應該要牽涉到被限制的那個欄位，否則這個限制條件就沒什麼意義了。

<a id="id-1.5.4.7.5.6"></a>

你也可以為限制條件另外取一個名稱。這能讓錯誤訊息更清楚，也讓你在需要變更該限制條件時可以指名它。語法是：

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CONSTRAINT positive_price CHECK (price > 0)
);
```

因此，若要指定一個具名的限制條件，請使用關鍵字 `CONSTRAINT`，後面接一個識別符號，再接限制條件的定義。（如果你沒有用這種方式指定限制條件名稱，系統會為你選一個名稱。）

檢查限制條件也可以參照多個欄位。假設你存放了定價與折扣價，而你想確保折扣價低於定價：

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

前兩個限制條件看起來應該很眼熟。第三個則使用了新的語法。它並不附屬於某個特定欄位，而是以獨立項目的形式出現在以逗號分隔的欄位清單中。欄位定義與這類限制條件定義可以混合排列。

我們說前兩個限制條件是欄位限制條件，而第三個則是資料表限制條件，因為它是與任何單一欄位定義分開來寫的。欄位限制條件也可以寫成資料表限制條件，但反過來就不一定可行，因為欄位限制條件理應只參照它所附屬的那個欄位。（PostgreSQL 並不強制執行這項規則，但如果你希望自己的資料表定義能在其他資料庫系統上運作，就應該遵守它。）上面的例子也可以寫成：

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

甚至可以寫成：

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0 AND price > discounted_price)
);
```

這只是個人喜好的問題。

資料表限制條件也可以用與欄位限制條件相同的方式指定名稱：

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

<a id="id-1.5.4.7.5.12"></a>

應該要注意的是，當檢查運算式求值結果為 true 或空值時，檢查限制條件就算被滿足。由於大多數運算式只要有任一運算元為 NULL 就會求值為空值，因此它們並不會阻止被限制的欄位出現空值。若要確保某個欄位不含空值，可以使用下一節所說明的非空值限制條件。

### 注意

PostgreSQL 不支援參照被檢查之新資料列或更新後資料列以外之資料表資料的 `CHECK` 限制條件。違反這項規則的 `CHECK` 限制條件在簡單的測試中看似可以運作，但它無法保證資料庫不會進入該限制條件的條件為 false 的狀態（因為所牽涉的其他資料列後續可能被更動）。這會導致資料庫的傾印與還原失敗。即使整個資料庫狀態都與該限制條件一致，還原也可能因為資料列載入的順序無法滿足限制條件而失敗。可能的話，請使用 `UNIQUE`、`EXCLUDE` 或 `FOREIGN KEY` 限制條件來表達跨資料列與跨資料表的限制。

如果你想要的只是在資料列插入時對其他資料列做一次性的檢查，而不是持續維護的一致性保證，那麼可以使用自訂的[觸發程序](../../server-programming/triggers/README.md)來實作。（這種做法可以避免傾印／還原的問題，因為 pg_dump 要等到資料還原之後才會重新安裝觸發程序，所以在傾印／還原期間並不會強制執行這項檢查。）

### 注意

PostgreSQL 假設 `CHECK` 限制條件的條件是不變的，也就是說，對同一筆輸入資料列它們永遠會給出相同的結果。正是這個假設，才使得只在資料列被插入或更新時檢查 `CHECK` 限制條件、而不在其他時候檢查的做法得以成立。（上面關於不要參照其他資料表資料的警告，其實就是這項限制的一個特例。）

要打破這個假設，一個常見的方式是在 `CHECK` 運算式中參照使用者定義的函式，然後改變那個函式的行為。PostgreSQL 並不禁止這麼做，但是如果資料表中有現在會違反該 `CHECK` 限制條件的資料列，它並不會察覺。這會導致後續的資料庫傾印與還原失敗。處理這類變更的建議做法是移除該限制條件（使用 `ALTER TABLE`）、調整函式定義，然後再重新加入該限制條件，藉此針對資料表中所有資料列重新檢查一次。

<a id="DDL-CONSTRAINTS-NOT-NULL"></a>

### 5.5.2. 非空值限制條件 [#](#DDL-CONSTRAINTS-NOT-NULL)

<a id="id-1.5.4.7.6.2"></a><a id="id-1.5.4.7.6.3"></a>

非空值限制條件單純指定某個欄位不得取用空值。語法範例：

```

CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric
);
```

也可以指定明確的限制條件名稱，例如：

```

CREATE TABLE products (
    product_no integer NOT NULL,
    name text CONSTRAINT products_name_not_null NOT NULL,
    price numeric
);
```

非空值限制條件通常會寫成欄位限制條件。把它寫成資料表限制條件的語法是

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    NOT NULL product_no,
    NOT NULL name
);
```

但這個語法並不是標準的，主要是給 pg_dump 使用的。

非空值限制條件在功能上等同於建立一個檢查限制條件 `CHECK (column_name IS NOT NULL)`，但在 PostgreSQL 中，建立明確的非空值限制條件效率比較好。

當然，一個欄位可以有多個限制條件。只要把這些限制條件一個接一個寫出來就好：

```

CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric NOT NULL CHECK (price > 0)
);
```

順序並不重要。它也不一定決定限制條件被檢查的順序。

不過，一個欄位最多只能有一個明確的非空值限制條件。

`NOT NULL` 限制條件有一個相反的形式：`NULL` 限制條件。這並不表示該欄位必須為 NULL，那樣肯定毫無用處。相反地，它只是選擇了「該欄位可以為 NULL」這個預設行為。`NULL` 限制條件並不存在於 SQL 標準中，在講求可攜性的應用中不應該使用它。（它加進 PostgreSQL 只是為了與某些其他資料庫系統相容。）不過有些使用者喜歡它，因為它讓人可以在腳本檔中輕鬆地切換這個限制條件。例如，你可以先寫成：

```

CREATE TABLE products (
    product_no integer NULL,
    name text NULL,
    price numeric NULL
);
```

然後在需要的地方插入 `NOT` 關鍵字。

### 提示

在大多數的資料庫設計中，大部分的欄位都應該標示為非空值。

<a id="DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS"></a>

### 5.5.3. 唯一限制條件 [#](#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS)

<a id="id-1.5.4.7.7.2"></a><a id="id-1.5.4.7.7.3"></a>

唯一限制條件確保某個欄位或一組欄位中所含的資料，在資料表的所有資料列之間是唯一的。語法是：

```

CREATE TABLE products (
    product_no integer UNIQUE,
    name text,
    price numeric
);
```

這是寫成欄位限制條件時的形式，而：

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    UNIQUE (product_no)
);
```

則是寫成資料表限制條件時的形式。

若要為一組欄位定義唯一限制條件，請把它寫成資料表限制條件，並以逗號分隔各欄位名稱：

```

CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    UNIQUE (a, c)
);
```

這指定了所指出的那些欄位其值的組合在整個資料表中是唯一的，但其中任何單一欄位並不需要（通常也不會）是唯一的。

你可以用平常的方式，為唯一限制條件指定自己的名稱：

```

CREATE TABLE products (
    product_no integer CONSTRAINT must_be_different UNIQUE,
    name text,
    price numeric
);
```

加入唯一限制條件會自動在該限制條件所列出的欄位或欄位群組上建立一個唯一的 B-tree 索引。只涵蓋部分資料列的唯一性限制無法寫成唯一限制條件，但可以藉由建立唯一的[部分索引](../indexes/indexes-partial.md)來強制執行這類限制。

<a id="id-1.5.4.7.7.8"></a>

一般來說，如果資料表中有超過一筆資料列，其限制條件所包含的所有欄位之值都相等，就會違反唯一限制條件。在預設情況下，這項比較中兩個空值並不視為相等。這表示即使存在唯一限制條件，仍然可能儲存多筆重複的資料列，只要它們在被限制的欄位中至少有一個是空值。這個行為可以藉由加上 `NULLS NOT DISTINCT` 子句來改變，像這樣

```

CREATE TABLE products (
    product_no integer UNIQUE NULLS NOT DISTINCT,
    name text,
    price numeric
);
```

或

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    UNIQUE NULLS NOT DISTINCT (product_no)
);
```

預設行為則可以用 `NULLS DISTINCT` 明確指定。依照 SQL 標準，唯一限制條件中對 NULL 的預設處理方式是由實作自行定義的，其他實作可能有不同的行為。因此在開發需要可攜性的應用時請多加留意。

<a id="DDL-CONSTRAINTS-PRIMARY-KEYS"></a>

### 5.5.4. 主鍵 [#](#DDL-CONSTRAINTS-PRIMARY-KEYS)

<a id="id-1.5.4.7.8.2"></a><a id="id-1.5.4.7.8.3"></a>

主鍵限制條件表示某個欄位或一組欄位可以用來當作資料表中資料列的唯一識別碼。這要求這些值既是唯一的、也不能是 NULL。因此，下面這兩個資料表定義所接受的資料是相同的：

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

主鍵可以橫跨多個欄位；其語法與唯一限制條件類似：

```

CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    PRIMARY KEY (a, c)
);
```

加入主鍵會自動在主鍵所列出的欄位或欄位群組上建立一個唯一的 B-tree 索引，並且會強制把這些欄位標示為 `NOT NULL`。

一個資料表最多只能有一個主鍵。（唯一限制條件的數量則沒有限制，而唯一限制條件與非空值限制條件合起來在功能上幾乎是同一回事，但只有一個可以被認定為主鍵。）關聯式資料庫理論規定每個資料表都必須有主鍵。PostgreSQL 並不強制執行這項規則，但通常最好還是遵守它。

主鍵無論是對文件說明的用途，還是對用戶端應用程式來說，都很有用。例如，一個允許修改資料列值的 GUI 應用程式，大概需要知道資料表的主鍵才能唯一地識別資料列。資料庫系統本身也會以各種方式運用已宣告的主鍵；例如，主鍵定義了參照該資料表之外鍵所預設的目標欄位。

<a id="DDL-CONSTRAINTS-FK"></a>

### 5.5.5. 外鍵 [#](#DDL-CONSTRAINTS-FK)

<a id="id-1.5.4.7.9.2"></a><a id="id-1.5.4.7.9.3"></a><a id="id-1.5.4.7.9.4"></a>

外鍵限制條件指定某個欄位（或一組欄位）中的值必須與另一個資料表中某筆資料列所出現的值相符。我們說這維持了兩個相關資料表之間的*參照完整性*。

假設你有我們已經用過好幾次的產品資料表：

```

CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

我們再假設你有一個存放這些產品訂單的資料表。我們想確保訂單資料表只包含實際存在之產品的訂單。因此我們在訂單資料表中定義一個參照產品資料表的外鍵限制條件：

```

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products (product_no),
    quantity integer
);
```

如此一來，就不可能建立 `product_no` 項目非 NULL、卻沒有出現在產品資料表中的訂單了。

我們說在這種情況下，訂單資料表是*參照*資料表，而產品資料表是*被參照*資料表。同樣地，也有參照欄位與被參照欄位之分。

你也可以把上面的指令簡寫成：

```

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products,
    quantity integer
);
```

因為在沒有欄位清單的情況下，會以被參照資料表的主鍵作為被參照的欄位。

你可以用平常的方式，為外鍵限制條件指定自己的名稱。

外鍵也可以限制並參照一組欄位。如同慣例，這時它需要寫成資料表限制條件的形式。以下是一個刻意編造的語法範例：

```

CREATE TABLE t1 (
  a integer PRIMARY KEY,
  b integer,
  c integer,
  FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)
);
```

當然，被限制之欄位的數量與型別必須與被參照欄位的數量與型別相符。

<a id="id-1.5.4.7.9.11"></a>

有時候，讓外鍵限制條件的「另一個資料表」就是同一個資料表會很有用；這稱為*自我參照*外鍵。例如，如果你希望用資料表的資料列來表示樹狀結構的節點，你可以寫成

```

CREATE TABLE tree (
    node_id integer PRIMARY KEY,
    parent_id integer REFERENCES tree,
    name text,
    ...
);
```

最上層的節點其 `parent_id` 會是 NULL，而非 NULL 的 `parent_id` 項目則會被限制為必須參照資料表中有效的資料列。

一個資料表可以有多個外鍵限制條件。這被用來實作資料表之間的多對多關係。假設你有關於產品與訂單的資料表，但現在你想允許一張訂單包含多項產品（這是上面的結構所不允許的）。你可以使用這樣的資料表結構：

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

請注意，在最後一個資料表中，主鍵與外鍵是重疊的。

<a id="id-1.5.4.7.9.14"></a><a id="id-1.5.4.7.9.15"></a>

我們知道外鍵禁止建立與任何產品都無關的訂單。但如果在一張訂單建立並參照某項產品之後，該產品被移除了呢？SQL 也讓你能夠處理這種情況。直覺上，我們有幾個選擇：

* 禁止刪除被參照的產品
* 連訂單也一併刪除
* 其他做法？

為了說明這一點，讓我們在上面的多對多關係範例上實作以下的原則：當有人想移除仍被某張訂單（透過 `order_items`）參照的產品時，我們禁止這麼做。如果有人移除了一張訂單，訂單項目也會一併被移除：

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

預設的 `ON DELETE` 動作是 `ON DELETE NO ACTION`；這不需要特別指定。這表示允許被參照資料表中的刪除作業繼續進行。但外鍵限制條件仍然必須被滿足，所以這項操作通常會導致錯誤。不過，外鍵限制條件的檢查也可以延遲到交易稍後才進行（本章不涵蓋這部分）。在那種情況下，`NO ACTION` 設定就能讓其他指令在限制條件被檢查之前先「修正」這個情況，例如在被參照資料表中插入另一筆適當的資料列，或是從參照資料表中刪除那些如今已懸空的資料列。

`RESTRICT` 是比 `NO ACTION` 更嚴格的設定。它會阻止刪除被參照的資料列。`RESTRICT` 不允許把檢查延遲到交易稍後才進行。

`CASCADE` 則指定當被參照的資料列被刪除時，參照它的資料列也應該自動被刪除。

另外還有兩個選項：`SET NULL` 與 `SET DEFAULT`。當被參照的資料列被刪除時，它們會讓參照資料列中的參照欄位分別被設為 NULL 或其預設值。請注意，這些做法並不能免除你遵守其他限制條件的責任。例如，如果某個動作指定了 `SET DEFAULT`，但預設值並不滿足外鍵限制條件，那麼這項操作就會失敗。

`ON DELETE` 動作要如何選擇才恰當，取決於相關資料表所代表的物件種類。當參照資料表所代表的東西是被參照資料表所代表之物的組成部分、且無法獨立存在時，`CASCADE` 可能就是恰當的選擇。如果這兩個資料表代表的是各自獨立的物件，那麼 `RESTRICT` 或 `NO ACTION` 會比較恰當；若應用程式確實想要刪除這兩個物件，就必須明確地表達，並執行兩道刪除指令。在上面的例子中，訂單項目是訂單的一部分，所以當訂單被刪除時讓它們自動被刪除是很方便的。但產品與訂單是不同的東西，因此讓刪除產品自動導致某些訂單項目被刪除，可能會被認為是有問題的。如果外鍵關係代表的是選擇性的資訊，那麼 `SET NULL` 或 `SET DEFAULT` 動作可能就很恰當。例如，如果產品資料表中含有對產品經理的參照，而該產品經理的項目被刪除了，那麼把該產品的產品經理設為 NULL 或預設值可能會很有用。

`SET NULL` 與 `SET DEFAULT` 動作可以帶一個欄位清單，用來指定要設定哪些欄位。通常外鍵限制條件的所有欄位都會被設定；只設定其中一部分在某些特殊情況下很有用。考慮以下這個例子：

```

CREATE TABLE tenants (
    tenant_id integer PRIMARY KEY
);

CREATE TABLE users (
    tenant_id integer REFERENCES tenants ON DELETE CASCADE,
    user_id integer NOT NULL,
    PRIMARY KEY (tenant_id, user_id)
);

CREATE TABLE posts (
    tenant_id integer REFERENCES tenants ON DELETE CASCADE,
    post_id integer NOT NULL,
    author_id integer,
    PRIMARY KEY (tenant_id, post_id),
    FOREIGN KEY (tenant_id, author_id) REFERENCES users ON DELETE SET NULL (author_id)
);
```

如果沒有指定該欄位，這個外鍵也會把 `tenant_id` 欄位設為 NULL，但那個欄位身為主鍵的一部分仍然是必要的。

與 `ON DELETE` 類似，還有 `ON UPDATE`，它會在被參照欄位被變更（更新）時被觸發。可用的動作是相同的，只不過 `SET NULL` 與 `SET DEFAULT` 不能指定欄位清單。在這種情況下，`CASCADE` 表示被參照欄位更新後的值應該被複製到參照的資料列中。此外，`ON UPDATE NO ACTION`（預設值）與 `ON UPDATE RESTRICT` 之間有一個明顯的差異。前者會允許更新繼續進行，並且針對更新後的狀態檢查外鍵限制條件。後者則會阻止更新執行，即使更新後的狀態仍然會滿足該限制條件也一樣。這可以防止把被參照的資料列更新成一個雖然不同、但比較起來卻相等的值（例如在使用不區分大小寫定序的字元字串型別時，大小寫寫法不同的字元字串）。

通常，如果參照資料列的任何一個參照欄位為 NULL，該資料列就不需要滿足外鍵限制條件。如果在外鍵宣告中加上 `MATCH FULL`，那麼參照資料列只有在它所有的參照欄位都為 NULL 時，才能免於滿足該限制條件（因此 NULL 與非 NULL 值混雜的情況必定無法通過 `MATCH FULL` 限制條件）。如果你不希望參照資料列有辦法避開外鍵限制條件，請把參照欄位宣告為 `NOT NULL`。

外鍵所參照的欄位必須是主鍵、構成唯一限制條件，或者是來自非部分唯一值索引的欄位。這表示被參照的欄位一定會有索引，以便能有效率地查詢某筆參照資料列是否有相符的對象。由於從被參照資料表 `DELETE` 一筆資料列，或是 `UPDATE` 一個被參照欄位，都會需要掃描參照資料表以找出符合舊值的資料列，因此為參照欄位也建立索引通常是個好主意。由於這並非總是必要，而且建立索引的方式有許多選擇，因此宣告外鍵限制條件並不會自動在參照欄位上建立索引。

關於更新與刪除資料的更多資訊，請參閱[第 6 章](../dml/README.md)。也請參閱 [CREATE TABLE](../../reference/sql-commands/sql-createtable.md) 參考文件中關於外鍵限制條件語法的說明。

<a id="DDL-CONSTRAINTS-EXCLUSION"></a>

### 5.5.6. 排除限制條件 [#](#DDL-CONSTRAINTS-EXCLUSION)

<a id="id-1.5.4.7.10.2"></a><a id="id-1.5.4.7.10.3"></a>

排除限制條件確保：如果對任兩筆資料列以指定的運算子比較指定的欄位或運算式，這些運算子比較中至少會有一項回傳 false 或 NULL。語法是：

```

CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

細節也請參閱 [`CREATE TABLE ... CONSTRAINT ... EXCLUDE`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-EXCLUDE)。

加入排除限制條件會自動建立一個型別為該限制條件宣告中所指定之類型的索引。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-constraints.html)（原文版本：18.6；核對日期：2026-09-13）
