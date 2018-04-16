# 9.10. 列舉型別函式

For enum types \(described in[Section 8.7](https://www.postgresql.org/docs/10/static/datatype-enum.html)\), there are several functions that allow cleaner programming without hard-coding particular values of an enum type. These are listed in[Table 9.32](https://www.postgresql.org/docs/10/static/functions-enum.html#functions-enum-table). The examples assume an enum type created as:

```text
CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow', 'green', 'blue', 'purple');
```

**Table 9.32. Enum Support Functions**

| Function | Description | Example | Example Result |
| :--- | :--- | :--- | :--- |
| `enum_first(anyenum)` | Returns the first value of the input enum type | `enum_first(null::rainbow)` | `red` |
| `enum_last(anyenum)` | Returns the last value of the input enum type | `enum_last(null::rainbow)` | `purple` |
| `enum_range(anyenum)` | Returns all values of the input enum type in an ordered array | `enum_range(null::rainbow)` | `{red,orange,yellow,green,blue,purple}` |
| `enum_range(anyenum, anyenum)` | Returns the range between the two given enum values, as an ordered array. The values must be from the same enum type. If the first parameter is null, the result will start with the first value of the enum type. If the second parameter is null, the result will end with the last value of the enum type. | `enum_range('orange'::rainbow, 'green'::rainbow)` | `{orange,yellow,green}` |
|  |  | `enum_range(NULL, 'green'::rainbow)` | `{red,orange,yellow,green}` |
|  |  | `enum_range('orange'::rainbow, NULL)` | `{orange,yellow,green,blue,purple}` |

Notice that except for the two-argument form of`enum_range`, these functions disregard the specific value passed to them; they care only about its declared data type. Either null or a specific value of the type can be passed, with the same result. It is more common to apply these functions to a table column or function argument than to a hardwired type name as suggested by the examples.

