---
description: 版本：11
---

# CREATE TYPE

CREATE TYPE — 定義新的資料型別

### 語法

```
CREATE TYPE name AS
    ( [ attribute_name data_type [ COLLATE collation ] [, ... ] ] )

CREATE TYPE name AS ENUM
    ( [ 'label' [, ... ] ] )

CREATE TYPE name AS RANGE (
    SUBTYPE = subtype
    [ , SUBTYPE_OPCLASS = subtype_operator_class ]
    [ , COLLATION = collation ]
    [ , CANONICAL = canonical_function ]
    [ , SUBTYPE_DIFF = subtype_diff_function ]
)

CREATE TYPE name (
    INPUT = input_function,
    OUTPUT = output_function
    [ , RECEIVE = receive_function ]
    [ , SEND = send_function ]
    [ , TYPMOD_IN = type_modifier_input_function ]
    [ , TYPMOD_OUT = type_modifier_output_function ]
    [ , ANALYZE = analyze_function ]
    [ , INTERNALLENGTH = { internallength | VARIABLE } ]
    [ , PASSEDBYVALUE ]
    [ , ALIGNMENT = alignment ]
    [ , STORAGE = storage ]
    [ , LIKE = like_type ]
    [ , CATEGORY = category ]
    [ , PREFERRED = preferred ]
    [ , DEFAULT = default ]
    [ , ELEMENT = element ]
    [ , DELIMITER = delimiter ]
    [ , COLLATABLE = collatable ]
)

CREATE TYPE name
```

### 說明

CREATE TYPE 註冊一個新的資料型別，以便在目前資料庫中使用。定義型別的使用者將成為其所有者。

如果加上了綱要名稱，則會在指定的綱要中建立型別。否則，它將在目前的綱要中建立。型別名稱必須與同一綱要中任何現有型別或 domain 的名稱不同。（因為資料表具有關連的資料型別，所以型別名稱也必須與同一綱要中任何現有資料表的名稱不同。）

CREATE TYPE 有五種形式，如上面的語法概要所示。分別可以建立複合型別、列舉型別、範圍型別、基本型別或 shell 型別。下面將依次討論前四個。 shell 型別只是一個佔位型別，用於稍後定義的型別；它透過發出 CREATE TYPE 建立的，除了型別名稱之外沒有參數。在建立範圍型別和基本型別時，需要使用 Shell 型別作為先行引用，詳細如下面小節中所述。

#### Composite Types (複合型別)

CREATE TYPE 的第一種形式是複合型別。複合型別以屬性名稱和資料型別列表組成。如果屬性可以指定 collation 的話，則也可以指定 collation。複合型別與資料表的資料列型別基本相同，但使用 CREATE TYPE 時，毌須建立實際的資料表，只需要定義型別即可。舉例來說，獨立複合型別可用於函數的參數或回傳型別。

要能夠建立複合型別，您必須具有所有屬性型別的 USAGE 權限。

#### Enumerated Types (列舉型別)

第二種形式的 CREATE TYPE 創建一個列舉（enum）型別，如[第 8.7 節](../../the-sql-language/data-types/enumerated-types.md)所述。列舉型別採用一個或多個帶引號的標籤列表，每個標籤的長度必須小於 NAMEDATALEN 個字元（標準 PostgreSQL 編譯中為 64 個字元）。（可以以空集合建立列舉型別，但是在使用 [ALTER TYPE](alter-type.md) 加入一個以上標籤之前，這樣的型別是不允許使用的。）

#### Range Types

第三種形式的 CREATE TYPE 建立一個新的範圍型別，如[第 8.17 節](../../the-sql-language/data-types/range-types.md)所述。

範圍型別的子型別可以是具有關連的 b-tree 運算子類的任何型別（用於確定範圍型別值的排序）。通常，子型別的預設 b-tree 運算子類用於決定排序；要使用非預設的運算子類，請使用 subtype\_opclass 指定其名稱。如果子型別是可指定 collation 的，並且您希望在範圍的排序中使用非預設的排序規則，請使用排序規則選項指定所需的排序規則。

選擇性的規範函數必須能接受所定義範圍型別的一個參數，並回傳相同型別的值。在套用時，這會用於將範圍值轉換為所規範形式。有關更多訊息，請參閱[第 8.17.8 節](https://docs.postgresql.tw/the-sql-language/data-types/range-types#8-17-8-defining-new-range-types)。建立規範函數有點棘手，因為必須在宣告範圍型別之前定義它。而要執行此操作，必須先建立一個 shell 型別，這是一種佔位型別，除了名稱和所有者之外沒有其他屬性。這是透過發出命令 CREATE TYPE name 來完成的，沒有其他參數。然後可以使用 shell 型別作為參數和結果宣告函數，最後可以使用相同的名稱宣告範圍型別。這會自動使用有效的範圍型別替換 shell 型別參數。

選擇性的 subtype\_diff 函數必須將子型別的兩個值作為參數，並回傳表示兩個給定值之間差異的雙精確度值。雖然這是選擇性的，但是有提供它的話，可以在範圍型別的欄位上實現更高的 GiST 索引效率。有關更多訊息，請參閱[第 8.17.8 節](https://docs.postgresql.tw/the-sql-language/data-types/range-types#8-17-8-defining-new-range-types)。

#### Base Types (基本型別)

The fourth form of `CREATE TYPE` creates a new base type (scalar type). To create a new base type, you must be a superuser. (This restriction is made because an erroneous type definition could confuse or even crash the server.)

The parameters can appear in any order, not only that illustrated above, and most are optional. You must register two or more functions (using `CREATE FUNCTION`) before defining the type. The support functions _`input_function`_ and _`output_function`_ are required, while the functions _`receive_function`_, _`send_function`_, _`type_modifier_input_function`_, _`type_modifier_output_function`_ and _`analyze_function`_ are optional. Generally these functions have to be coded in C or another low-level language.

The _`input_function`_ converts the type's external textual representation to the internal representation used by the operators and functions defined for the type. _`output_function`_ performs the reverse transformation. The input function can be declared as taking one argument of type `cstring`, or as taking three arguments of types `cstring`, `oid`, `integer`. The first argument is the input text as a C string, the second argument is the type's own OID (except for array types, which instead receive their element type's OID), and the third is the `typmod` of the destination column, if known (-1 will be passed if not). The input function must return a value of the data type itself. Usually, an input function should be declared STRICT; if it is not, it will be called with a NULL first parameter when reading a NULL input value. The function must still return NULL in this case, unless it raises an error. (This case is mainly meant to support domain input functions, which might need to reject NULL inputs.) The output function must be declared as taking one argument of the new data type. The output function must return type `cstring`. Output functions are not invoked for NULL values.

The optional _`receive_function`_ converts the type's external binary representation to the internal representation. If this function is not supplied, the type cannot participate in binary input. The binary representation should be chosen to be cheap to convert to internal form, while being reasonably portable. (For example, the standard integer data types use network byte order as the external binary representation, while the internal representation is in the machine's native byte order.) The receive function should perform adequate checking to ensure that the value is valid. The receive function can be declared as taking one argument of type `internal`, or as taking three arguments of types `internal`, `oid`, `integer`. The first argument is a pointer to a `StringInfo` buffer holding the received byte string; the optional arguments are the same as for the text input function. The receive function must return a value of the data type itself. Usually, a receive function should be declared STRICT; if it is not, it will be called with a NULL first parameter when reading a NULL input value. The function must still return NULL in this case, unless it raises an error. (This case is mainly meant to support domain receive functions, which might need to reject NULL inputs.) Similarly, the optional _`send_function`_ converts from the internal representation to the external binary representation. If this function is not supplied, the type cannot participate in binary output. The send function must be declared as taking one argument of the new data type. The send function must return type `bytea`. Send functions are not invoked for NULL values.

You should at this point be wondering how the input and output functions can be declared to have results or arguments of the new type, when they have to be created before the new type can be created. The answer is that the type should first be defined as a _shell type_, which is a placeholder type that has no properties except a name and an owner. This is done by issuing the command `CREATE TYPE `_`name`_, with no additional parameters. Then the C I/O functions can be defined referencing the shell type. Finally, `CREATE TYPE` with a full definition replaces the shell entry with a complete, valid type definition, after which the new type can be used normally.

The optional _`type_modifier_input_function`_ and _`type_modifier_output_function`_ are needed if the type supports modifiers, that is optional constraints attached to a type declaration, such as `char(5)` or `numeric(30,2)`. PostgreSQL allows user-defined types to take one or more simple constants or identifiers as modifiers. However, this information must be capable of being packed into a single non-negative integer value for storage in the system catalogs. The _`type_modifier_input_function`_ is passed the declared modifier(s) in the form of a `cstring` array. It must check the values for validity (throwing an error if they are wrong), and if they are correct, return a single non-negative `integer` value that will be stored as the column “typmod”. Type modifiers will be rejected if the type does not have a _`type_modifier_input_function`_. The _`type_modifier_output_function`_ converts the internal integer typmod value back to the correct form for user display. It must return a `cstring` value that is the exact string to append to the type name; for example `numeric`'s function might return `(30,2)`. It is allowed to omit the _`type_modifier_output_function`_, in which case the default display format is just the stored typmod integer value enclosed in parentheses.

The optional _`analyze_function`_ performs type-specific statistics collection for columns of the data type. By default, `ANALYZE` will attempt to gather statistics using the type's “equals” and “less-than” operators, if there is a default b-tree operator class for the type. For non-scalar types this behavior is likely to be unsuitable, so it can be overridden by specifying a custom analysis function. The analysis function must be declared to take a single argument of type `internal`, and return a `boolean` result. The detailed API for analysis functions appears in `src/include/commands/vacuum.h`.

While the details of the new type's internal representation are only known to the I/O functions and other functions you create to work with the type, there are several properties of the internal representation that must be declared to PostgreSQL. Foremost of these is _`internallength`_. Base data types can be fixed-length, in which case _`internallength`_ is a positive integer, or variable-length, indicated by setting _`internallength`_ to `VARIABLE`. (Internally, this is represented by setting `typlen` to -1.) The internal representation of all variable-length types must start with a 4-byte integer giving the total length of this value of the type. (Note that the length field is often encoded, as described in [Section 68.2](https://www.postgresql.org/docs/12/storage-toast.html); it's unwise to access it directly.)

The optional flag `PASSEDBYVALUE` indicates that values of this data type are passed by value, rather than by reference. Types passed by value must be fixed-length, and their internal representation cannot be larger than the size of the `Datum` type (4 bytes on some machines, 8 bytes on others).

The _`alignment`_ parameter specifies the storage alignment required for the data type. The allowed values equate to alignment on 1, 2, 4, or 8 byte boundaries. Note that variable-length types must have an alignment of at least 4, since they necessarily contain an `int4` as their first component.

The _`storage`_ parameter allows selection of storage strategies for variable-length data types. (Only `plain` is allowed for fixed-length types.) `plain` specifies that data of the type will always be stored in-line and not compressed. `extended` specifies that the system will first try to compress a long data value, and will move the value out of the main table row if it's still too long. `external` allows the value to be moved out of the main table, but the system will not try to compress it. `main` allows compression, but discourages moving the value out of the main table. (Data items with this storage strategy might still be moved out of the main table if there is no other way to make a row fit, but they will be kept in the main table preferentially over `extended` and `external` items.)

All _`storage`_ values other than `plain` imply that the functions of the data type can handle values that have been _toasted_, as described in [Section 68.2](https://www.postgresql.org/docs/12/storage-toast.html) and [Section 37.13.1](https://www.postgresql.org/docs/12/xtypes.html#XTYPES-TOAST). The specific other value given merely determines the default TOAST storage strategy for columns of a toastable data type; users can pick other strategies for individual columns using `ALTER TABLE SET STORAGE`.

The _`like_type`_ parameter provides an alternative method for specifying the basic representation properties of a data type: copy them from some existing type. The values of _`internallength`_, _`passedbyvalue`_, _`alignment`_, and _`storage`_ are copied from the named type. (It is possible, though usually undesirable, to override some of these values by specifying them along with the `LIKE` clause.) Specifying representation this way is especially useful when the low-level implementation of the new type “piggybacks” on an existing type in some fashion.

The _`category`_ and _`preferred`_ parameters can be used to help control which implicit cast will be applied in ambiguous situations. Each data type belongs to a category named by a single ASCII character, and each type is either “preferred” or not within its category. The parser will prefer casting to preferred types (but only from other types within the same category) when this rule is helpful in resolving overloaded functions or operators. For more details see [Chapter 10](https://www.postgresql.org/docs/12/typeconv.html). For types that have no implicit casts to or from any other types, it is sufficient to leave these settings at the defaults. However, for a group of related types that have implicit casts, it is often helpful to mark them all as belonging to a category and select one or two of the “most general” types as being preferred within the category. The _`category`_ parameter is especially useful when adding a user-defined type to an existing built-in category, such as the numeric or string types. However, it is also possible to create new entirely-user-defined type categories. Select any ASCII character other than an upper-case letter to name such a category.

A default value can be specified, in case a user wants columns of the data type to default to something other than the null value. Specify the default with the `DEFAULT` key word. (Such a default can be overridden by an explicit `DEFAULT` clause attached to a particular column.)

To indicate that a type is an array, specify the type of the array elements using the `ELEMENT` key word. For example, to define an array of 4-byte integers (`int4`), specify `ELEMENT = int4`. More details about array types appear below.

To indicate the delimiter to be used between values in the external representation of arrays of this type, _`delimiter`_ can be set to a specific character. The default delimiter is the comma (`,`). Note that the delimiter is associated with the array element type, not the array type itself.

If the optional Boolean parameter _`collatable`_ is true, column definitions and expressions of the type may carry collation information through use of the `COLLATE` clause. It is up to the implementations of the functions operating on the type to actually make use of the collation information; this does not happen automatically merely by marking the type collatable.

#### Array Types (陣列型別)

每當建立使用者定義的型別時，PostgreSQL 都會自動建立一個相關聯的陣列型別，其名稱由元素型別的名稱組成，該名稱前面帶有底線，並在必要時將其截斷以使其長度小於 NAMEDATALEN 個字元。（如果這樣產生的名稱與現有型別名稱衝突，則重複此程序，直到找到一個非衝突名稱為止。）這個在幕後建立的陣列型別為可變長度，並使用內建的輸入和輸出函數 array\_in 和 array\_out。陣列型別會追隨其元素型別的所有者或網要中的所有變更，如果元素型別被刪除，也會將其刪除。

直覺地您可能會問，如果系統自動產生正確的陣列型別，為什麼會有 ELEMENT 選項。使用 ELEMENT 唯一有用的情況是，當您建立一個固定長度的型別時，該型別在內部恰好是由許多相同的東西組成的陣列，並且除了希望直接透過索引來存取這些元素。您打算為整個型別提供的任何支援操作。例如，型別 point 僅表示為兩個浮點數，可以使用 point\[0] 和 point\[1] 對其進行存取的行為。請注意，此功能僅適用於內部格式完全相同的固定長度欄位序列的固定長度型別。可索引的可變長度型別必須具有由 array\_in 和 array\_out 使用的通用內部表示形式。出於歷史原因（也就是說，這顯然是錯誤的，但要更改它為時已晚），固定長度陣列型別的索引是從零開始的，而非如同可變長度陣列從一開始。

### Parameters

_`name`_

The name (optionally schema-qualified) of a type to be created.

_`attribute_name`_

The name of an attribute (column) for the composite type.

_`data_type`_

The name of an existing data type to become a column of the composite type.

_`collation`_

The name of an existing collation to be associated with a column of a composite type, or with a range type.

_`label`_

A string literal representing the textual label associated with one value of an enum type.

_`subtype`_

The name of the element type that the range type will represent ranges of.

_`subtype_operator_class`_

The name of a b-tree operator class for the subtype.

_`canonical_function`_

The name of the canonicalization function for the range type.

_`subtype_diff_function`_

The name of a difference function for the subtype.

_`input_function`_

The name of a function that converts data from the type's external textual form to its internal form.

_`output_function`_

The name of a function that converts data from the type's internal form to its external textual form.

_`receive_function`_

The name of a function that converts data from the type's external binary form to its internal form.

_`send_function`_

The name of a function that converts data from the type's internal form to its external binary form.

_`type_modifier_input_function`_

The name of a function that converts an array of modifier(s) for the type into internal form.

_`type_modifier_output_function`_

The name of a function that converts the internal form of the type's modifier(s) to external textual form.

_`analyze_function`_

The name of a function that performs statistical analysis for the data type.

_`internallength`_

A numeric constant that specifies the length in bytes of the new type's internal representation. The default assumption is that it is variable-length.

_`alignment`_

The storage alignment requirement of the data type. If specified, it must be `char`, `int2`, `int4`, or `double`; the default is `int4`.

_`storage`_

The storage strategy for the data type. If specified, must be `plain`, `external`, `extended`, or `main`; the default is `plain`.

_`like_type`_

The name of an existing data type that the new type will have the same representation as. The values of _`internallength`_, _`passedbyvalue`_, _`alignment`_, and _`storage`_ are copied from that type, unless overridden by explicit specification elsewhere in this `CREATE TYPE` command.

_`category`_

The category code (a single ASCII character) for this type. The default is `'U'` for “user-defined type”. Other standard category codes can be found in [Table 51.64](https://www.postgresql.org/docs/12/catalog-pg-type.html#CATALOG-TYPCATEGORY-TABLE). You may also choose other ASCII characters in order to create custom categories.

_`preferred`_

True if this type is a preferred type within its type category, else false. The default is false. Be very careful about creating a new preferred type within an existing type category, as this could cause surprising changes in behavior.

_`default`_

The default value for the data type. If this is omitted, the default is null.

_`element`_

The type being created is an array; this specifies the type of the array elements.

_`delimiter`_

The delimiter character to be used between values in arrays made of this type.

_`collatable`_

True if this type's operations can use collation information. The default is false.

### Notes

Because there are no restrictions on use of a data type once it's been created, creating a base type or range type is tantamount to granting public execute permission on the functions mentioned in the type definition. This is usually not an issue for the sorts of functions that are useful in a type definition. But you might want to think twice before designing a type in a way that would require “secret” information to be used while converting it to or from external form.

Before PostgreSQL version 8.3, the name of a generated array type was always exactly the element type's name with one underscore character (`_`) prepended. (Type names were therefore restricted in length to one less character than other names.) While this is still usually the case, the array type name may vary from this in case of maximum-length names or collisions with user type names that begin with underscore. Writing code that depends on this convention is therefore deprecated. Instead, use `pg_type`.`typarray` to locate the array type associated with a given type.

It may be advisable to avoid using type and table names that begin with underscore. While the server will change generated array type names to avoid collisions with user-given names, there is still risk of confusion, particularly with old client software that may assume that type names beginning with underscores always represent arrays.

Before PostgreSQL version 8.2, the shell-type creation syntax `CREATE TYPE `_`name`_ did not exist. The way to create a new base type was to create its input function first. In this approach, PostgreSQL will first see the name of the new data type as the return type of the input function. The shell type is implicitly created in this situation, and then it can be referenced in the definitions of the remaining I/O functions. This approach still works, but is deprecated and might be disallowed in some future release. Also, to avoid accidentally cluttering the catalogs with shell types as a result of simple typos in function definitions, a shell type will only be made this way when the input function is written in C.

In PostgreSQL versions before 7.3, it was customary to avoid creating a shell type at all, by replacing the functions' forward references to the type name with the placeholder pseudo-type `opaque`. The `cstring` arguments and results also had to be declared as `opaque` before 7.3. To support loading of old dump files, `CREATE TYPE` will accept I/O functions declared using `opaque`, but it will issue a notice and change the function declarations to use the correct types.

### 範例

此範例建立一個複合型別並在函數定義中使用它：

```
CREATE TYPE compfoo AS (f1 int, f2 text);

CREATE FUNCTION getfoo() RETURNS SETOF compfoo AS $$
    SELECT fooid, fooname FROM foo
$$ LANGUAGE SQL;
```

此範例建立列舉型別並在資料表定義中使用它：

```
CREATE TYPE bug_status AS ENUM ('new', 'open', 'closed');

CREATE TABLE bug (
    id serial,
    description text,
    status bug_status
);
```

此範例建立範圍型別：

```
CREATE TYPE float8_range AS RANGE (subtype = float8, subtype_diff = float8mi);
```

此範例建立基本資料型別 box，然後在資料表定義中使用該型別：

```
CREATE TYPE box;

CREATE FUNCTION my_box_in_function(cstring) RETURNS box AS ... ;
CREATE FUNCTION my_box_out_function(box) RETURNS cstring AS ... ;

CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function
);

CREATE TABLE myboxes (
    id integer,
    description box
);
```

如果 box 的內部結構是一個包含四個 float4 元素的陣列，我們可能會使用：

```
CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function,
    ELEMENT = float4
);
```

這將允許透過索引存取 box 值的組件編號。其他型別的行為與先前相同。

此範例建立一個 large object 型別並在資料表定義中使用它：

```
CREATE TYPE bigobj (
    INPUT = lo_filein, OUTPUT = lo_fileout,
    INTERNALLENGTH = VARIABLE
);
CREATE TABLE big_objs (
    id integer,
    obj bigobj
);
```

更多範例，包括適當的輸入和輸出功能，請參閱[第 37.13 節](../../server-programming/extending-sql/user-defined-types.md)。

### 相容性

建立複合型別 CREATE TYPE 指令的第一種形式符合 SQL 標準。其他形式則是 PostgreSQL 延伸語法。SQL 標準中的 CREATE TYPE 語句還定義了 PostgreSQL 中未實作的其他形式。

建立具有零屬性的複合型別是 PostgreSQL 專有的（類似於 CREATE TABLE 的情況）。

### 參閱

[ALTER TYPE](alter-type.md), [CREATE DOMAIN](create-domain.md),[ CREATE FUNCTION](create-function.md), [DROP TYPE](drop-type.md)
