<a id="PLTCL-FUNCTIONS"></a>

## 42.2. PL/Tcl 函式與引數 [#](#PLTCL-FUNCTIONS)

要以 PL/Tcl 語言建立函式，請使用標準的 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md) 語法：

```

CREATE FUNCTION funcname (argument-types) RETURNS return-type AS $$
    # PL/Tcl function body
$$ LANGUAGE pltcl;
```

PL/TclU 也一樣，只是語言必須指定為 `pltclu`。

函式的主體就只是一段 Tcl 指令稿。當函式被呼叫時，引數值會以名為 `1` ... `n` 的變數傳遞給 Tcl 指令稿。結果則以一般的方式，透過 `return` 陳述式從 Tcl 程式碼回傳。在程序（procedure）中，Tcl 程式碼的回傳值會被忽略。

例如，一個回傳兩個整數值中較大者的函式可以這樣定義：

```

CREATE FUNCTION tcl_max(integer, integer) RETURNS integer AS $$
    if {$1 > $2} {return $1}
    return $2
$$ LANGUAGE pltcl STRICT;
```

請注意 `STRICT` 子句，它讓我們不必去思考 NULL 輸入值的問題：如果傳入了 NULL 值，該函式根本不會被呼叫，而是會自動回傳 NULL 結果。

在非 strict 的函式中，如果某個引數的實際值是 NULL，對應的 `$n` 變數會被設為空字串。若要偵測某個特定引數是否為 NULL，請使用 `argisnull` 函式。例如，假設我們希望 `tcl_max` 在收到一個 NULL 與一個非 NULL 引數時，回傳那個非 NULL 的引數，而不是回傳 NULL：

```

CREATE FUNCTION tcl_max(integer, integer) RETURNS integer AS $$
    if {[argisnull 1]} {
        if {[argisnull 2]} { return_null }
        return $2
    }
    if {[argisnull 2]} { return $1 }
    if {$1 > $2} {return $1}
    return $2
$$ LANGUAGE pltcl;
```

如上所示，要從 PL/Tcl 函式回傳 NULL 值，請執行 `return_null`。不論該函式是否為 strict，都可以這麼做。

複合型別的引數會以 Tcl 陣列的形式傳遞給函式。陣列的元素名稱就是該複合型別的屬性名稱。如果傳入資料列中的某個屬性是 NULL 值，它就不會出現在陣列中。以下是一個例子：

```

CREATE TABLE employee (
    name text,
    salary integer,
    age integer
);

CREATE FUNCTION overpaid(employee) RETURNS boolean AS $$
    if {200000.0 < $1(salary)} {
        return "t"
    }
    if {$1(age) < 30 && 100000.0 < $1(salary)} {
        return "t"
    }
    return "f"
$$ LANGUAGE pltcl;
```

PL/Tcl 函式也可以回傳複合型別的結果。要做到這一點，Tcl 程式碼必須回傳一個由欄位名稱／值配對組成的 list（串列），並與預期的結果型別相符。清單中未列出的欄位會回傳 NULL；若出現非預期的欄位名稱，則會引發錯誤。以下是一個例子：

```

CREATE FUNCTION square_cube(in int, out squared int, out cubed int) AS $$
    return [list squared [expr {$1 * $1}] cubed [expr {$1 * $1 * $1}]]
$$ LANGUAGE pltcl;
```

程序的輸出引數也以同樣的方式回傳，例如：

```

CREATE PROCEDURE tcl_triple(INOUT a integer, INOUT b integer) AS $$
    return [list a [expr {$1 * 3}] b [expr {$2 * 3}]]
$$ LANGUAGE pltcl;

CALL tcl_triple(5, 10);
```

### 提示

結果 list 可以用 Tcl 的 `array get` 指令，從所需 tuple（值組）的陣列表示法產生出來。例如：

```

CREATE FUNCTION raise_pay(employee, delta int) RETURNS employee AS $$
    set 1(salary) [expr {$1(salary) + $2}]
    return [array get 1]
$$ LANGUAGE pltcl;
```

PL/Tcl 函式可以回傳集合。要做到這一點，Tcl 程式碼應該對每一筆要回傳的資料列呼叫一次 `return_next`，在回傳純量型別時傳入適當的值，或在回傳複合型別時傳入欄位名稱／值配對的 list。以下是一個回傳純量型別的例子：

```

CREATE FUNCTION sequence(int, int) RETURNS SETOF int AS $$
    for {set i $1} {$i < $2} {incr i} {
        return_next $i
    }
$$ LANGUAGE pltcl;
```

而這是一個回傳複合型別的例子：

```

CREATE FUNCTION table_of_squares(int, int) RETURNS TABLE (x int, x2 int) AS $$
    for {set i $1} {$i < $2} {incr i} {
        return_next [list x $i x2 [expr {$i * $i}]]
    }
$$ LANGUAGE pltcl;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-functions.html)（原文版本：18.6；核對日期：2026-09-12）
