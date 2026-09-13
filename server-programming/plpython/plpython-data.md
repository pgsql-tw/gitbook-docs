<a id="PLPYTHON-DATA"></a>

## 44.2. 資料值 [#](#PLPYTHON-DATA)

[44.2.1. 資料型別對應](plpython-data.md#PLPYTHON-DATA-TYPE-MAPPING)

[44.2.2. Null、None](plpython-data.md#PLPYTHON-DATA-NULL)

[44.2.3. 陣列、list](plpython-data.md#PLPYTHON-ARRAYS)

[44.2.4. 複合型別](plpython-data.md#PLPYTHON-DATA-COMPOSITE-TYPES)

[44.2.5. 集合回傳函式](plpython-data.md#PLPYTHON-DATA-SET-RETURNING-FUNCS)

一般來說，PL/Python 的目標是在 PostgreSQL 與 Python 兩個世界之間提供一種「自然」的對應關係。下面所描述的資料對應規則正是依循這個原則。

<a id="PLPYTHON-DATA-TYPE-MAPPING"></a>

### 44.2.1. 資料型別對應 [#](#PLPYTHON-DATA-TYPE-MAPPING)

當 PL/Python 函式被呼叫時，它的引數會從 PostgreSQL 的資料型別轉換成對應的 Python 型別：

* PostgreSQL 的 `boolean` 轉換成 Python 的 `bool`。
* PostgreSQL 的 `smallint`、`int`、`bigint` 與 `oid` 轉換成 Python 的 `int`。
* PostgreSQL 的 `real` 與 `double` 轉換成 Python 的 `float`。
* PostgreSQL 的 `numeric` 轉換成 Python 的 `Decimal`。如果系統中有 `cdecimal` 套件，這個型別會從該套件匯入；否則就會使用標準函式庫中的 `decimal.Decimal`。`cdecimal` 比 `decimal` 快上許多。不過在 Python 3.3 以上的版本中，`cdecimal` 已經以 `decimal` 這個名稱整併進標準函式庫，因此兩者已無差別。
* PostgreSQL 的 `bytea` 轉換成 Python 的 `bytes`。
* 所有其他的資料型別，包括 PostgreSQL 的字元字串型別，都會轉換成 Python 的 `str`（與所有 Python 字串一樣使用 Unicode）。
* 非純量的資料型別請參閱下文。

當 PL/Python 函式回傳時，它的回傳值會依下列方式轉換成該函式所宣告的 PostgreSQL 回傳資料型別：

* 當 PostgreSQL 的回傳型別是 `boolean` 時，回傳值會依照 *Python* 的規則來判斷真假。也就是說，0 與空字串為假，但要特別注意 `'f'` 為真。
* 當 PostgreSQL 的回傳型別是 `bytea` 時，回傳值會用對應的 Python 內建函式轉換成 Python 的 `bytes`，其結果再轉換成 `bytea`。
* 對於所有其他的 PostgreSQL 回傳型別，回傳值會以 Python 內建的 `str` 轉換成字串，其結果再傳給該 PostgreSQL 資料型別的輸入函式。（如果 Python 值是 `float`，則會改用內建的 `repr` 而非 `str` 來轉換，以避免精度流失。）

  字串在傳給 PostgreSQL 時，會自動轉換成 PostgreSQL 的伺服器編碼。
* 非純量的資料型別請參閱下文。

請注意，所宣告的 PostgreSQL 回傳型別與實際回傳物件的 Python 資料型別在邏輯上不相符時，並不會被標示出來；該值無論如何都會被轉換。

<a id="PLPYTHON-DATA-NULL"></a>

### 44.2.2. Null、None [#](#PLPYTHON-DATA-NULL)

如果把 SQL 的 NULL 值<a id="id-1.8.11.10.4.2.1"></a>傳給函式，在 Python 中該引數值會呈現為 `None`。例如，[第 44.1 節](plpython-funcs.md)中所示的 `pymax` 函式定義，對於 NULL 輸入會回傳錯誤的答案。我們可以在函式定義中加上 `STRICT`，讓 PostgreSQL 做出比較合理的處理：如果傳入的是 NULL 值，該函式根本不會被呼叫，而會直接自動回傳 NULL 結果。或者，我們也可以在函式本體中檢查 NULL 輸入：

```

CREATE FUNCTION pymax (a integer, b integer)
  RETURNS integer
AS $$
  if (a is None) or (b is None):
    return None
  if a > b:
    return a
  return b
$$ LANGUAGE plpython3u;
```

如上所示，若要從 PL/Python 函式回傳 SQL 的 NULL 值，就回傳 `None` 這個值。無論該函式是否為 strict，都可以這樣做。

<a id="PLPYTHON-ARRAYS"></a>

### 44.2.3. 陣列、list [#](#PLPYTHON-ARRAYS)

SQL 的陣列值會以 Python list（串列）的形式傳入 PL/Python。若要從 PL/Python 函式回傳 SQL 陣列值，就回傳一個 Python list：

```

CREATE FUNCTION return_arr()
  RETURNS int[]
AS $$
return [1, 2, 3, 4, 5]
$$ LANGUAGE plpython3u;

SELECT return_arr();
 return_arr
-------------
 {1,2,3,4,5}
(1 row)
```

多維陣列會以巢狀的 Python list 形式傳入 PL/Python。舉例來說，二維陣列就是 list 的 list。從 PL/Python 函式回傳多維 SQL 陣列時，每一層的內層 list 大小都必須相同。例如：

```

CREATE FUNCTION test_type_conversion_array_int4(x int4[]) RETURNS int4[] AS $$
plpy.info(x, type(x))
return x
$$ LANGUAGE plpython3u;

SELECT * FROM test_type_conversion_array_int4(ARRAY[[1,2,3],[4,5,6]]);
INFO:  ([[1, 2, 3], [4, 5, 6]], <type 'list'>)
 test_type_conversion_array_int4
---------------------------------
 {{1,2,3},{4,5,6}}
(1 row)
```

其他的 Python 序列（例如 tuple）也同樣被接受，這是為了與 PostgreSQL 9.6 以下版本（當時尚未支援多維陣列）向後相容。不過它們永遠會被視為一維陣列，因為它們與複合型別之間有歧義。基於同樣的理由，當多維陣列中使用複合型別時，它必須以 tuple 而非 list 來表示。

請注意，在 Python 中字串也是序列，這可能造成 Python 程式設計師或許並不陌生的、不樂見的效果：

```

CREATE FUNCTION return_str_arr()
  RETURNS varchar[]
AS $$
return "hello"
$$ LANGUAGE plpython3u;

SELECT return_str_arr();
 return_str_arr
----------------
 {h,e,l,l,o}
(1 row)
```

<a id="PLPYTHON-DATA-COMPOSITE-TYPES"></a>

### 44.2.4. 複合型別 [#](#PLPYTHON-DATA-COMPOSITE-TYPES)

複合型別的引數會以 Python 映射（mapping）的形式傳給函式。映射的元素名稱就是該複合型別的屬性名稱。如果傳入之資料列中的某個屬性是 NULL 值，它在映射中的值就是 `None`。以下是一個例子：

```

CREATE TABLE employee (
  name text,
  salary integer,
  age integer
);

CREATE FUNCTION overpaid (e employee)
  RETURNS boolean
AS $$
  if e["salary"] > 200000:
    return True
  if (e["age"] < 30) and (e["salary"] > 100000):
    return True
  return False
$$ LANGUAGE plpython3u;
```

從 Python 函式回傳資料列或複合型別的方式有很多種。以下的例子都假設我們有：

```

CREATE TYPE named_value AS (
  name   text,
  value  integer
);
```

複合型別的結果可以用下列形式回傳：

序列型別（tuple 或 list，但不能是 set，因為它無法以索引存取）
:   回傳的序列物件所含的項目數量，必須與複合結果型別的欄位數量相同。索引 0 的項目會指派給複合型別的第一個欄位，1 指派給第二個，依此類推。例如：

    ```

    CREATE FUNCTION make_pair (name text, value integer)
      RETURNS named_value
    AS $$
      return ( name, value )
      # or alternatively, as list: return [ name, value ]
    $$ LANGUAGE plpython3u;
    ```

    若要讓某個欄位回傳 SQL 的 NULL，就在對應的位置放入 `None`。

    當要回傳複合型別的陣列時，不能以 list 的形式回傳，因為這樣會無法分辨該 Python list 代表的是複合型別還是另一個陣列維度。

映射（字典）
:   結果型別中每個欄位的值，會以欄位名稱為鍵從該映射中取得。例如：

    ```

    CREATE FUNCTION make_pair (name text, value integer)
      RETURNS named_value
    AS $$
      return { "name": name, "value": value }
    $$ LANGUAGE plpython3u;
    ```

    字典中任何多餘的鍵／值配對都會被忽略，而缺少的鍵則會被視為錯誤。若要讓某個欄位回傳 SQL 的 NULL 值，就以對應的欄位名稱為鍵放入 `None`。

物件（任何提供 `__getattr__` 方法的物件）
:   其運作方式與映射相同。例如：

    ```

    CREATE FUNCTION make_pair (name text, value integer)
      RETURNS named_value
    AS $$
      class named_value:
        def __init__ (self, n, v):
          self.name = n
          self.value = v
      return named_value(name, value)

      # or simply
      class nv: pass
      nv.name = name
      nv.value = value
      return nv
    $$ LANGUAGE plpython3u;
    ```

帶有 `OUT` 參數的函式同樣也受支援。例如：

```

CREATE FUNCTION multiout_simple(OUT i integer, OUT j integer) AS $$
return (1, 2)
$$ LANGUAGE plpython3u;

SELECT * FROM multiout_simple();
```

程序的輸出參數也是以同樣的方式傳回。例如：

```

CREATE PROCEDURE python_triple(INOUT a integer, INOUT b integer) AS $$
return (a * 3, b * 3)
$$ LANGUAGE plpython3u;

CALL python_triple(5, 10);
```

<a id="PLPYTHON-DATA-SET-RETURNING-FUNCS"></a>

### 44.2.5. 集合回傳函式 [#](#PLPYTHON-DATA-SET-RETURNING-FUNCS)

PL/Python 函式也可以回傳純量或複合型別的集合。達成這件事的方式有好幾種，因為回傳的物件在內部會被轉換成迭代器。以下的例子假設我們有這個複合型別：

```

CREATE TYPE greeting AS (
  how text,
  who text
);
```

集合結果可以從下列形式回傳：

序列型別（tuple、list、set）
:   ```

    CREATE FUNCTION greet (how text)
      RETURNS SETOF greeting
    AS $$
      # return tuple containing lists as composite types
      # all other combinations work also
      return ( [ how, "World" ], [ how, "PostgreSQL" ], [ how, "PL/Python" ] )
    $$ LANGUAGE plpython3u;
    ```

迭代器（任何提供 `__iter__` 與 `__next__` 方法的物件）
:   ```

    CREATE FUNCTION greet (how text)
      RETURNS SETOF greeting
    AS $$
      class producer:
        def __init__ (self, how, who):
          self.how = how
          self.who = who
          self.ndx = -1

        def __iter__ (self):
          return self

        def __next__(self):
          self.ndx += 1
          if self.ndx == len(self.who):
            raise StopIteration
          return ( self.how, self.who[self.ndx] )

      return producer(how, [ "World", "PostgreSQL", "PL/Python" ])
    $$ LANGUAGE plpython3u;
    ```

產生器（`yield`）
:   ```

    CREATE FUNCTION greet (how text)
      RETURNS SETOF greeting
    AS $$
      for who in [ "World", "PostgreSQL", "PL/Python" ]:
        yield ( how, who )
    $$ LANGUAGE plpython3u;
    ```

帶有 `OUT` 參數（使用 `RETURNS SETOF record`）的集合回傳函式同樣也受支援。例如：

```

CREATE FUNCTION multiout_simple_setof(n integer, OUT integer, OUT integer) RETURNS SETOF record AS $$
return [(1, 2)] * n
$$ LANGUAGE plpython3u;

SELECT * FROM multiout_simple_setof(3);
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-data.html)（原文版本：18.6；核對日期：2026-09-13）
