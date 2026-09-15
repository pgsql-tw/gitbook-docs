<a id="DDL-DEPEND"></a>

## 5.15. 相依性追蹤 [#](#DDL-DEPEND)

<a id="id-1.5.4.17.2"></a><a id="id-1.5.4.17.3"></a>

當你建立複雜的資料庫結構，其中包含許多帶有外鍵限制條件的資料表、檢視表、觸發程序、函式等等時，你就隱含地在這些物件之間建立了一張相依性的網。例如，帶有外鍵限制條件的資料表會相依於它所參照的資料表。

為了確保整個資料庫結構的完整性，PostgreSQL 會確保你無法移除其他物件仍相依於它的物件。例如，如果 orders 資料表相依於我們在[第 5.5.5 節](ddl-constraints.md#DDL-CONSTRAINTS-FK)所討論的 products 資料表，那麼嘗試移除 products 資料表就會產生像這樣的錯誤訊息：

```

DROP TABLE products;

ERROR:  cannot drop table products because other objects depend on it
DETAIL:  constraint orders_product_no_fkey on table orders depends on table products
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

這個錯誤訊息包含了一個有用的提示：如果你不想費工夫一個一個刪除所有相依的物件，可以執行：

```

DROP TABLE products CASCADE;
```

如此一來，所有相依的物件都會被移除，相依於這些物件的物件也會被遞迴地移除。在這個例子中，它並不會移除 orders 資料表，而只會移除外鍵限制條件。它到此就停止了，因為沒有任何東西相依於這個外鍵限制條件。（如果你想檢查 `DROP ... CASCADE` 會做些什麼，可以先執行不加 `CASCADE` 的 `DROP`，然後閱讀 `DETAIL` 的輸出。）

PostgreSQL 中幾乎所有的 `DROP` 指令都支援指定 `CASCADE`。當然，可能存在的相依性其性質會隨物件型別而異。你也可以寫 `RESTRICT` 而不是 `CASCADE`，以取得預設的行為，也就是禁止移除任何其他物件所相依的物件。

### 注意

依照 SQL 標準，在 `DROP` 指令中必須指定 `RESTRICT` 或 `CASCADE` 其中之一。實際上沒有任何資料庫系統強制執行這項規則，但預設行為究竟是 `RESTRICT` 還是 `CASCADE`，則各系統不盡相同。

如果一個 `DROP` 指令列出了多個物件，只有在所指定的那組物件之外還存在相依性時，才需要 `CASCADE`。例如，當執行 `DROP TABLE tab1, tab2` 時，即使 `tab2` 中有一個參照 `tab1` 的外鍵存在，也不表示需要 `CASCADE` 才能成功。

對於本體是以字串常數定義的使用者定義函式或程序，PostgreSQL 會追蹤與該函式外部可見屬性相關的相依性，例如它的引數型別與結果型別，但*不會*追蹤那些唯有檢視函式本體才能得知的相依性。舉例來說，考慮以下這個情況：

```

CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow',
                             'green', 'blue', 'purple');

CREATE TABLE my_colors (color rainbow, note text);

CREATE FUNCTION get_color_note (rainbow) RETURNS text AS
  'SELECT note FROM my_colors WHERE color = $1'
  LANGUAGE SQL;
```

（SQL 語言函式的說明請參閱[第 36.5 節](../../server-programming/extend/xfunc-sql.md)。）PostgreSQL 會知道 `get_color_note` 函式相依於 `rainbow` 型別：移除這個型別就會強制移除這個函式，因為它的引數型別將不再有定義。但是 PostgreSQL 不會認為 `get_color_note` 相依於 `my_colors` 資料表，因此當該資料表被移除時，並不會移除這個函式。這種做法雖然有缺點，但也有好處。即使資料表不存在了，這個函式在某種意義上仍然是有效的，儘管執行它會產生錯誤；建立一個同名的新資料表就能讓這個函式再次運作。

另一方面，對於本體以 SQL 標準風格撰寫的 SQL 語言函式或程序，其本體會在函式定義時被剖析，而且剖析器所辨識出的所有相依性都會被儲存起來。因此，如果我們把上面的函式寫成

```

CREATE FUNCTION get_color_note (rainbow) RETURNS text
BEGIN ATOMIC
  SELECT note FROM my_colors WHERE color = $1;
END;
```

那麼這個函式對 `my_colors` 資料表的相依性就會被知悉，並由 `DROP` 強制執行。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-depend.html)（原文版本：18.6；核對日期：2026-09-13）
