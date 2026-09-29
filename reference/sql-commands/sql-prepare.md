<a id="id-1.9.3.159.1"></a><a id="id-1.9.3.159.2"></a>

## PREPARE

PREPARE — 準備一則陳述式以供執行

<a id="id-1.9.3.159.3"></a>

## 語法

```

PREPARE name [ ( data_type [, ...] ) ] AS statement
```

<a id="id-1.9.3.159.6"></a>

## 說明

`PREPARE` 會建立一個預備陳述式。預備陳述式是一種伺服器端物件，可用來最佳化效能。當執行 `PREPARE` 陳述式時，系統會剖析、分析並重寫指定的陳述式。之後發出 `EXECUTE` 指令時，就會對該預備陳述式進行規劃並執行。這種分工可避免重複的剖析分析工作，同時仍可讓執行計畫依所提供的特定參數值而定。

預備陳述式可以帶有參數：也就是在執行陳述式時會被代換進去的值。建立預備陳述式時，請使用 `$1`、`$2` 等依位置參照參數。你可以選擇性地指定對應的參數資料型別清單。當某個參數的資料型別未指定，或宣告為 `unknown` 時，系統會（在可能的情況下）從該參數第一次被參照的上下文推斷其型別。執行陳述式時，請在 `EXECUTE` 陳述式中指定這些參數的實際值。相關細節請參閱 [EXECUTE](sql-execute.md)。

預備陳述式僅在目前的資料庫工作階段期間有效。工作階段結束後，該預備陳述式就會被遺忘，因此下次使用前必須重新建立。這也表示單一預備陳述式無法同時被多個資料庫用戶端使用；不過，每個用戶端都可以自行建立要使用的預備陳述式。你可以使用 [`DEALLOCATE`](sql-deallocate.md) 指令手動清除預備陳述式。

當單一工作階段用來執行大量相似的陳述式時，預備陳述式帶來的效能優勢可能最為顯著。如果陳述式在規劃或重寫上較為複雜，例如查詢涉及多個資料表的連接運算，或需要套用多條規則，這種效能差異會特別明顯。如果陳述式的規劃與重寫相對簡單，但執行本身相對昂貴，那麼預備陳述式的效能優勢就會比較不明顯。

<a id="id-1.9.3.159.7"></a>

## 參數

*`name`*
:   賦予這個特定預備陳述式的任意名稱。它在單一工作階段內必須是唯一的，之後會用來執行或釋放先前建立的預備陳述式。

*`data_type`*
:   預備陳述式其中一個參數的資料型別。如果某個特定參數的資料型別未指定，或指定為 `unknown`，系統會從該參數第一次被參照的上下文推斷其型別。若要在預備陳述式本身中參照這些參數，請使用 `$1`、`$2` 等。

*`statement`*
:   任何 `SELECT`、`INSERT`、`UPDATE`、`DELETE`、`MERGE` 或 `VALUES` 陳述式。

<a id="SQL-PREPARE-NOTES"></a>

## 注意

預備陳述式可以用*通用計畫*（generic plan）或*客製計畫*（custom plan）來執行。通用計畫在所有執行中都相同，而客製計畫則是針對特定一次執行、依該次呼叫所提供的參數值產生的。使用通用計畫可以避免規劃的額外負擔，但在某些情況下，由於規劃器能夠利用參數值的相關知識，客製計畫的執行效率會高出許多。（當然，如果預備陳述式沒有任何參數，這一點就沒有意義，此時一律使用通用計畫。）

依預設（也就是當 [plan_cache_mode](../../server-administration/runtime-config/runtime-config-query.md#GUC-PLAN-CACHE-MODE) 設為 `auto` 時），伺服器會針對帶有參數的預備陳述式，自動選擇要使用通用計畫還是客製計畫。目前的規則是：前五次執行都採用客製計畫，並計算這些計畫的平均估計成本。接著會建立一個通用計畫，並將其估計成本與平均客製計畫成本相比較。之後的執行，只要通用計畫的成本沒有高出平均客製計畫成本太多、不至於讓重複重新規劃顯得比較划算，就會使用通用計畫。

可以透過將 `plan_cache_mode` 設為 `force_generic_plan` 或 `force_custom_plan`，覆寫此判斷方式，強制伺服器分別使用通用計畫或客製計畫。當通用計畫的成本估計因某些原因而嚴重失準時，這項設定特別有用，可讓系統即使在實際成本遠高於客製計畫的情況下，仍選用通用計畫。

若要檢查 PostgreSQL 為某個預備陳述式所使用的查詢計畫，請使用 [`EXPLAIN`](sql-explain.md)，例如

```

EXPLAIN EXECUTE name(parameter_values);
```

如果目前使用的是通用計畫，其中會包含參數符號 `$n`；如果是客製計畫，則會將所提供的參數值代入其中。

關於查詢規劃，以及 PostgreSQL 為此目的所收集的統計資料的更多資訊，請參閱 [ANALYZE](sql-analyze.md) 文件。

雖然預備陳述式的主要目的是避免重複剖析分析與規劃陳述式，但只要陳述式中所用到的資料庫物件，自預備陳述式上次使用以來曾發生定義（DDL）變更，或其規劃器統計資料曾被更新，PostgreSQL 就會在使用該陳述式之前強制重新剖析與重新規劃。此外，如果 [search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 的值在兩次使用之間發生變化，該陳述式就會依新的 `search_path` 重新剖析。（這後一種行為是從 PostgreSQL 9.3 開始新增的。）這些規則使得使用預備陳述式在語意上幾乎等同於一再重新送出相同的查詢文字，但只要沒有任何物件定義發生變更，尤其是在各次使用之間最佳計畫維持不變時，就能帶來效能上的好處。語意並非完全等價的一個例子是：如果陳述式以未限定名稱參照某個資料表，之後又在 `search_path` 中排序較前面的綱要中建立了同名的新資料表，由於陳述式中所用到的物件並未發生變更，就不會自動觸發重新剖析。不過，如果因其他變更而強制重新剖析，後續使用時就會參照到這個新的資料表。

你可以透過查詢 [`pg_prepared_statements`](../../internals/views/view-pg-prepared-statements.md) 系統檢視表，查看該工作階段中所有可用的預備陳述式。

<a id="SQL-PREPARE-EXAMPLES"></a>

## 範例

為 `INSERT` 陳述式建立一個預備陳述式，然後執行它：

```

PREPARE fooplan (int, text, bool, numeric) AS
    INSERT INTO foo VALUES($1, $2, $3, $4);
EXECUTE fooplan(1, 'Hunter Valley', 't', 200.00);
```

為 `SELECT` 陳述式建立一個預備陳述式，然後執行它：

```

PREPARE usrrptplan (int) AS
    SELECT * FROM users u, logs l WHERE u.usrid=$1 AND u.usrid=l.usrid
    AND l.date = $2;
EXECUTE usrrptplan(1, current_date);
```

在這個範例中，第二個參數的資料型別並未指定，因此會從 `$2` 被使用的上下文中推斷出來。

<a id="id-1.9.3.159.10"></a>

## 相容性

SQL 標準包含 `PREPARE` 陳述式，但僅供嵌入式 SQL 使用。這個版本的 `PREPARE` 陳述式也使用了略為不同的語法。

<a id="id-1.9.3.159.11"></a>

## 另請參閱

[DEALLOCATE](sql-deallocate.md), [EXECUTE](sql-execute.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-prepare.html)（原文版本：18.6；核對日期：2026-09-28）
