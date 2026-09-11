<a id="SQL-SYNTAX-CALLING-FUNCS"></a>

## 4.3. 呼叫函式 [#](#SQL-SYNTAX-CALLING-FUNCS)

[4.3.1. 使用位置表示法](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-POSITIONAL)

[4.3.2. 使用具名表示法](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-NAMED)

[4.3.3. 使用混合表示法](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-MIXED)

<a id="id-1.5.3.7.2"></a>

PostgreSQL 允許使用*位置*（positional）表示法或*具名*（named）表示法來呼叫具有具名參數的函式。具名表示法對於參數很多的函式特別有用，因為它能讓參數與實際引數之間的對應關係更明確、更可靠。使用位置表示法時，函式呼叫中的引數值要依照函式宣告中定義的順序撰寫。使用具名表示法時，引數會依名稱與函式參數對應，因此可以用任何順序撰寫。無論使用哪一種表示法，也請考量函式引數型別的影響，相關說明請參閱[第 10.3 節](../typeconv/typeconv-func.md)。

無論使用哪一種表示法，在函式宣告中具有預設值的參數，在呼叫時都可以完全不寫。不過這在具名表示法中特別有用，因為可以省略任何參數組合；而在位置表示法中，參數只能從右到左省略。

PostgreSQL 也支援*混合*（mixed）表示法，結合了位置表示法與具名表示法。在這種情況下，要先寫位置參數，具名參數則出現在其後。

以下範例會使用下列函式定義，說明這三種表示法的用法：

```

CREATE FUNCTION concat_lower_or_upper(a text, b text, uppercase boolean DEFAULT false)
RETURNS text
AS
$$
 SELECT CASE
        WHEN $3 THEN UPPER($1 || ' ' || $2)
        ELSE LOWER($1 || ' ' || $2)
        END;
$$
LANGUAGE SQL IMMUTABLE STRICT;
```

函式 `concat_lower_or_upper` 有兩個必要參數 `a` 與 `b`。另外還有一個選用參數 `uppercase`，其預設值為 `false`。輸入的 `a` 與 `b` 會被串接起來，並依 `uppercase` 參數強制轉為大寫或小寫。這個函式定義的其餘細節在此並不重要（更多資訊請參閱[第 36 章](../../server-programming/extend/README.md)）。

<a id="SQL-SYNTAX-CALLING-FUNCS-POSITIONAL"></a>

### 4.3.1. 使用位置表示法 [#](#SQL-SYNTAX-CALLING-FUNCS-POSITIONAL)

<a id="id-1.5.3.7.7.2"></a>

位置表示法是 PostgreSQL 中傳遞引數給函式的傳統機制。範例如下：

```

SELECT concat_lower_or_upper('Hello', 'World', true);
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

所有引數都依序指定。由於 `uppercase` 被指定為 `true`，結果會是大寫。另一個範例如下：

```

SELECT concat_lower_or_upper('Hello', 'World');
 concat_lower_or_upper
-----------------------
 hello world
(1 row)
```

這裡省略了 `uppercase` 參數，因此它會使用預設值 `false`，輸出結果為小寫。在位置表示法中，只要引數有預設值，就可以從右到左省略。

<a id="SQL-SYNTAX-CALLING-FUNCS-NAMED"></a>

### 4.3.2. 使用具名表示法 [#](#SQL-SYNTAX-CALLING-FUNCS-NAMED)

<a id="id-1.5.3.7.8.2"></a>

在具名表示法中，每個引數的名稱都要指定，並使用 `=>` 將名稱與引數運算式分隔開來。例如：

```

SELECT concat_lower_or_upper(a => 'Hello', b => 'World');
 concat_lower_or_upper
-----------------------
 hello world
(1 row)
```

同樣地，這裡省略了引數 `uppercase`，因此它會被隱含地設為 `false`。使用具名表示法的一個優點是，引數可以用任何順序指定，例如：

```

SELECT concat_lower_or_upper(a => 'Hello', b => 'World', uppercase => true);
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)

SELECT concat_lower_or_upper(a => 'Hello', uppercase => true, b => 'World');
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

為了向後相容，也支援以「:=」為基礎的舊語法：

```

SELECT concat_lower_or_upper(a := 'Hello', uppercase := true, b := 'World');
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

<a id="SQL-SYNTAX-CALLING-FUNCS-MIXED"></a>

### 4.3.3. 使用混合表示法 [#](#SQL-SYNTAX-CALLING-FUNCS-MIXED)

<a id="id-1.5.3.7.9.2"></a>

混合表示法結合了位置表示法與具名表示法。不過，如前所述，具名引數不能出現在位置引數之前。例如：

```

SELECT concat_lower_or_upper('Hello', 'World', uppercase => true);
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

在上面的查詢中，引數 `a` 與 `b` 是以位置方式指定的，而 `uppercase` 則是以名稱指定的。在這個例子中，這樣做除了具有說明作用之外沒有太大好處。但對於有許多具預設值參數的複雜函式，具名或混合表示法可以省下大量的撰寫工作，並減少出錯的機會。

### 注意

目前在呼叫彙總函式時，無法使用具名與混合的呼叫表示法（但當彙總函式作為 window 函式使用時則可以）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-syntax-calling-funcs.html)（原文版本：18.6；核對日期：2026-09-11）
