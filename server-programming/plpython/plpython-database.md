<a id="PLPYTHON-DATABASE"></a>

## 44.6. 資料庫存取 [#](#PLPYTHON-DATABASE)

[44.6.1. 資料庫存取函式](plpython-database.md#PLPYTHON-DATABASE-ACCESS-FUNCS)

[44.6.2. 攔截錯誤](plpython-database.md#PLPYTHON-TRAPPING)

PL/Python 語言模組會自動匯入一個名為 `plpy` 的 Python 模組。這個模組中的函式與常數可以在你的 Python 程式碼中以 `plpy.foo` 的形式使用。

<a id="PLPYTHON-DATABASE-ACCESS-FUNCS"></a>

### 44.6.1. 資料庫存取函式 [#](#PLPYTHON-DATABASE-ACCESS-FUNCS)

`plpy` 模組提供了數個用來執行資料庫指令的函式：

`plpy.execute(query [, limit])`
:   以一個查詢字串與一個選擇性的資料列數量上限引數呼叫 `plpy.execute`，會使該查詢被執行，並將結果以結果物件的形式回傳。

    如果有指定 *`limit`* 且其值大於零，則 `plpy.execute` 最多只會取出 *`limit`* 筆資料列，就好像該查詢帶有 `LIMIT` 子句一樣。省略 *`limit`* 或把它指定為零，則不會限制資料列數量。

    結果物件模擬了 list 或字典物件的行為。結果物件可以用資料列編號與欄位名稱來存取。例如：

    ```

    rv = plpy.execute("SELECT * FROM my_table", 5)
    ```

    這會從 `my_table` 回傳最多 5 筆資料列。如果 `my_table` 有一個名為 `my_column` 的欄位，就可以這樣存取它：

    ```

    foo = rv[i]["my_column"]
    ```

    回傳的資料列數量可以用內建的 `len` 函式取得。

    結果物件還有下列這些額外的方法：

    `nrows()`
    :   回傳該指令所處理的資料列數量。請注意，這不一定與回傳的資料列數量相同。例如，`UPDATE` 指令會設定這個值，但不會回傳任何資料列（除非有使用 `RETURNING`）。

    `status()`
    :   `SPI_execute()` 的回傳值。

    `colnames()`<br>`coltypes()`<br>`coltypmods()`
    :   分別回傳欄位名稱的 list、欄位型別 OID 的 list，以及各欄位之型別專屬型別修飾詞的 list。

        如果對「沒有產生結果集的指令」所得到的結果物件呼叫這些方法（例如沒有 `RETURNING` 的 `UPDATE`，或 `DROP TABLE`），就會拋出例外。不過，對包含零筆資料列的結果集使用這些方法是可以的。

    `__str__()`
    :   標準的 `__str__` 方法有被定義，因此例如可以使用 `plpy.debug(rv)` 來對查詢執行結果進行除錯。

    結果物件是可以被修改的。

    請注意，呼叫 `plpy.execute` 會使整個結果集被讀入記憶體。只有在你確定結果集相對較小時才使用這個函式。如果你不想在取得大量結果時冒著耗用過多記憶體的風險，請改用 `plpy.cursor` 而非 `plpy.execute`。

`plpy.prepare(query [, argtypes])`<br>`plpy.execute(plan [, arguments [, limit]])`
:   <a id="id-1.8.11.14.3.3.2.3.1.1"></a>
    `plpy.prepare` 會為查詢準備執行計畫。呼叫它時要給定一個查詢字串，以及（若查詢中有參數參照）一個參數型別的 list。例如：

    ```

    plan = plpy.prepare("SELECT last_name FROM my_users WHERE first_name = $1", ["text"])
    ```

    `text` 是你將要為 `$1` 傳入之變數的型別。如果你不打算傳任何參數給該查詢，第二個引數是選擇性的。

    在準備好陳述式之後，你會使用 `plpy.execute` 函式的一種變體來執行它：

    ```

    rv = plpy.execute(plan, ["name"], 5)
    ```

    把執行計畫當成第一個引數傳入（取代查詢字串），並把要代入查詢的值的 list 當成第二個引數。如果該查詢不需要任何參數，第二個引數是選擇性的。第三個引數則和先前一樣，是選擇性的資料列數量上限。

    或者，你也可以對該執行計畫物件呼叫 `execute` 方法：

    ```

    rv = plan.execute(["name"], 5)
    ```

    查詢參數與結果資料列欄位會依[第 44.2 節](plpython-data.md)所述的方式在 PostgreSQL 與 Python 資料型別之間轉換。

    當你使用 PL/Python 模組準備執行計畫時，它會自動被儲存起來。這代表什麼意思，請閱讀 SPI 的文件（[第 45 章](../spi/README.md)）。為了在多次函式呼叫之間有效運用這一點，必須使用持續性儲存字典 `SD` 或 `GD` 其中之一（請參閱[第 44.3 節](plpython-sharing.md)）。例如：

    ```

    CREATE FUNCTION usesavedplan() RETURNS trigger AS $$
        if "plan" in SD:
            plan = SD["plan"]
        else:
            plan = plpy.prepare("SELECT 1")
            SD["plan"] = plan
        # rest of function
    $$ LANGUAGE plpython3u;
    ```

`plpy.cursor(query)`<br>`plpy.cursor(plan [, arguments])`
:   `plpy.cursor` 函式接受與 `plpy.execute` 相同的引數（除了資料列數量上限之外），並回傳一個游標物件，讓你可以分成較小的批次來處理大型結果集。與 `plpy.execute` 一樣，你可以使用查詢字串，也可以使用執行計畫物件搭配引數的 list，或者把 `cursor` 函式當成執行計畫物件的方法來呼叫。

    游標物件提供了一個 `fetch` 方法，它接受一個整數參數並回傳一個結果物件。每次你呼叫 `fetch`，回傳的物件都會包含下一批資料列，數量絕不會超過該參數值。一旦所有資料列都取完，`fetch` 就會開始回傳空的結果物件。游標物件同時也提供了[迭代器介面](https://docs.python.org/library/stdtypes.html#iterator-types)，每次產出一筆資料列，直到所有資料列都取完為止。以這種方式取得的資料並不是以結果物件回傳，而是以字典回傳，每個字典對應一筆結果資料列。

    以下是處理大型資料表資料的兩種方式的例子：

    ```

    CREATE FUNCTION count_odd_iterator() RETURNS integer AS $$
    odd = 0
    for row in plpy.cursor("select num from largetable"):
        if row['num'] % 2:
             odd += 1
    return odd
    $$ LANGUAGE plpython3u;

    CREATE FUNCTION count_odd_fetch(batch_size integer) RETURNS integer AS $$
    odd = 0
    cursor = plpy.cursor("select num from largetable")
    while True:
        rows = cursor.fetch(batch_size)
        if not rows:
            break
        for row in rows:
            if row['num'] % 2:
                odd += 1
    return odd
    $$ LANGUAGE plpython3u;

    CREATE FUNCTION count_odd_prepared() RETURNS integer AS $$
    odd = 0
    plan = plpy.prepare("select num from largetable where num % $1 <> 0", ["integer"])
    rows = list(plpy.cursor(plan, [2]))  # or: = list(plan.cursor([2]))

    return len(rows)
    $$ LANGUAGE plpython3u;
    ```

    游標會自動被釋放。但如果你想明確釋放某個游標所持有的所有資源，請使用 `close` 方法。一旦關閉，就不能再從該游標取出資料。

    ### 提示

    請不要把 `plpy.cursor` 所建立的物件與 [Python 資料庫 API 規格](https://www.python.org/dev/peps/pep-0249/)所定義的 DB-API 游標混為一談。除了名稱之外，它們毫無共通之處。

<a id="PLPYTHON-TRAPPING"></a>

### 44.6.2. 攔截錯誤 [#](#PLPYTHON-TRAPPING)

存取資料庫的函式可能會遇到錯誤，而這些錯誤會使它們中止並拋出例外。`plpy.execute` 與 `plpy.prepare` 兩者都可能拋出 `plpy.SPIError` 之子類別的實例，這在預設情況下會終止該函式。這個錯誤可以像處理其他任何 Python 例外一樣，用 `try/except` 結構來處理。例如：

```

CREATE FUNCTION try_adding_joe() RETURNS text AS $$
    try:
        plpy.execute("INSERT INTO users(username) VALUES ('joe')")
    except plpy.SPIError:
        return "something went wrong"
    else:
        return "Joe added"
$$ LANGUAGE plpython3u;
```

實際被拋出之例外的類別，對應到造成該錯誤的特定條件。可能的條件清單請參閱[表 A.1](../../appendixes/errcodes-appendix/README.md#ERRCODES-TABLE)。模組 `plpy.spiexceptions` 為每一個 PostgreSQL 條件定義了一個例外類別，其名稱衍生自條件名稱。例如，`division_by_zero` 會變成 `DivisionByZero`、`unique_violation` 變成 `UniqueViolation`、`fdw_error` 變成 `FdwError`，依此類推。這些例外類別每一個都繼承自 `SPIError`。這樣的區分使得處理特定錯誤更為容易，例如：

```

CREATE FUNCTION insert_fraction(numerator int, denominator int) RETURNS text AS $$
from plpy import spiexceptions
try:
    plan = plpy.prepare("INSERT INTO fractions (frac) VALUES ($1 / $2)", ["int", "int"])
    plpy.execute(plan, [numerator, denominator])
except spiexceptions.DivisionByZero:
    return "denominator cannot equal zero"
except spiexceptions.UniqueViolation:
    return "already have that fraction"
except plpy.SPIError as e:
    return "other error, SQLSTATE %s" % e.sqlstate
else:
    return "fraction inserted"
$$ LANGUAGE plpython3u;
```

請注意，由於 `plpy.spiexceptions` 模組中的所有例外都繼承自 `SPIError`，用來處理它的 `except` 子句會攔截任何資料庫存取錯誤。

處理不同錯誤條件的另一種替代做法，是攔截 `SPIError` 例外，並在 `except` 區塊內檢視該例外物件的 `sqlstate` 屬性，以判定特定的錯誤條件。這個屬性是一個字串值，內含「SQLSTATE」錯誤碼。這種做法所提供的功能大致相同

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-database.html)（原文版本：18.6；核對日期：2026-09-13）
