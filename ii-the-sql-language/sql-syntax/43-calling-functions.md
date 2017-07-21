# 4.3. 函數呼叫[^1]

PostgreSQL 允許函數呼叫的時候，使用編號或名稱記號。名稱記號特別好用在於有很多參數的時候，因為它能讓參數與實際的引數有更明確的關連，也更有信賴感。使用編號記號的話，函數呼叫就會依其宣告時的參數次序給予編號；而使用名稱記號的話，參數就會依宣告時的名稱配對，不需要次序對應。

不論哪一種記號方式，如果在宣告時有設定預設值的話，那就不一定要在呼叫時設定其值。不過這點對名稱記號特別好用，因為任何參數的組合都可以省略，而編號記號時就只有從最右邊的參數開始省略。

PostgreSQL 也支援混合式的記號方式，也就是同時使用編號，也使用名稱。在這個例子中，編號的參數會先使用，然後名稱的參數在其之後使用。

接下來的例子，將會描繪所有三種記號方式，都使用下列的函數定義：

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

函數 concat\_lower\_or\_upper 有兩個必要的參數，a 與 b。然後有一個參數是選擇性的，uppercase 的預設值是 false。參數 a 和 b 的文字會被連結起來，然後依 uppercase 的設定，強制轉換為大寫或小寫字母。這個函數定義的其他部份在這裡並不重要（詳情請參閱[第 37 章](/v-server-programming/extending-sql.md)）。

### 4.3.1. Using Positional Notation

Positional notation is the traditional mechanism for passing arguments to functions inPostgreSQL. An example is:

```
SELECT concat_lower_or_upper('Hello', 'World', true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

All arguments are specified in order. The result is upper case since`uppercase`is specified as`true`. Another example is:

```
SELECT concat_lower_or_upper('Hello', 'World');
 concat_lower_or_upper 
-----------------------
 hello world
(1 row)
```

Here, the`uppercase`parameter is omitted, so it receives its default value of`false`, resulting in lower case output. In positional notation, arguments can be omitted from right to left so long as they have defaults.

### 4.3.2. Using Named Notation

In named notation, each argument's name is specified using`=>`to separate it from the argument expression. For example:

```
SELECT concat_lower_or_upper(a =
>
 'Hello', b =
>
 'World');
 concat_lower_or_upper 
-----------------------
 hello world
(1 row)
```

Again, the argument`uppercase`was omitted so it is set to`false`implicitly. One advantage of using named notation is that the arguments may be specified in any order, for example:

```
SELECT concat_lower_or_upper(a =
>
 'Hello', b =
>
 'World', uppercase =
>
 true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)

SELECT concat_lower_or_upper(a =
>
 'Hello', uppercase =
>
 true, b =
>
 'World');
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

An older syntax based on ":=" is supported for backward compatibility:

```
SELECT concat_lower_or_upper(a := 'Hello', uppercase := true, b := 'World');
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

### 4.3.3. Using Mixed Notation

The mixed notation combines positional and named notation. However, as already mentioned, named arguments cannot precede positional arguments. For example:

```
SELECT concat_lower_or_upper('Hello', 'World', uppercase =
>
 true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

In the above query, the arguments`a`and`b`are specified positionally, while`uppercase`is specified by name. In this example, that adds little except documentation. With a more complex function having numerous parameters that have default values, named or mixed notation can save a great deal of writing and reduce chances for error.

### Note

Named and mixed call notations currently cannot be used when calling an aggregate function \(but they do work when an aggregate function is used as a window function\).

---

[^1]: [PostgreSQL: Documentation: 10: 4.3. Calling Functions](https://www.postgresql.org/docs/10/static/sql-syntax-calling-funcs.html)

