## 34.15. Informix Compatibility Mode [#](#ECPG-INFORMIX-COMPAT)

[34.15.1. Additional Types](ecpg-informix-compat.md#ECPG-INFORMIX-TYPES)

[34.15.2. Additional/Missing Embedded SQL Statements](ecpg-informix-compat.md#ECPG-INFORMIX-STATEMENTS)

[34.15.3. Informix-compatible SQLDA Descriptor Areas](ecpg-informix-compat.md#ECPG-INFORMIX-SQLDA)

[34.15.4. Additional Functions](ecpg-informix-compat.md#ECPG-INFORMIX-FUNCTIONS)

[34.15.5. Additional Constants](ecpg-informix-compat.md#ECPG-INFORMIX-CONSTANTS)

`ecpg` can be run in a so-called *Informix compatibility mode*. If
this mode is active, it tries to behave as if it were the Informix
precompiler for Informix E/SQL. Generally spoken this will allow you to use
the dollar sign instead of the `EXEC SQL` primitive to introduce
embedded SQL commands:

```

$int j = 3;
$CONNECT TO :dbname;
$CREATE TABLE test(i INT PRIMARY KEY, j INT);
$INSERT INTO test(i, j) VALUES (7, :j);
$COMMIT;
```

### Note

There must not be any white space between the `$`
and a following preprocessor directive, that is,
`include`, `define`, `ifdef`,
etc. Otherwise, the preprocessor will parse the token as a host
variable.

There are two compatibility modes: `INFORMIX`, `INFORMIX_SE`

When linking programs that use this compatibility mode, remember to link
against `libcompat` that is shipped with ECPG.

Besides the previously explained syntactic sugar, the Informix compatibility
mode ports some functions for input, output and transformation of data as
well as embedded SQL statements known from E/SQL to ECPG.

Informix compatibility mode is closely connected to the pgtypeslib library
of ECPG. pgtypeslib maps SQL data types to data types within the C host
program and most of the additional functions of the Informix compatibility
mode allow you to operate on those C host program types. Note however that
the extent of the compatibility is limited. It does not try to copy Informix
behavior; it allows you to do more or less the same operations and gives
you functions that have the same name and the same basic behavior but it is
no drop-in replacement if you are using Informix at the moment. Moreover,
some of the data types are different. For example,
PostgreSQL's datetime and interval types do not
know about ranges like for example `YEAR TO MINUTE` so you won't
find support in ECPG for that either.

<a id="ECPG-INFORMIX-TYPES"></a>

### 34.15.1. Additional Types [#](#ECPG-INFORMIX-TYPES)

The Informix-special "string" pseudo-type for storing right-trimmed character string data is now
supported in Informix-mode without using `typedef`. In fact, in Informix-mode,
ECPG refuses to process source files that contain `typedef sometype string;`

```

EXEC SQL BEGIN DECLARE SECTION;
string userid; /* this variable will contain trimmed data */
EXEC SQL END DECLARE SECTION;

EXEC SQL FETCH MYCUR INTO :userid;
```

<a id="ECPG-INFORMIX-STATEMENTS"></a>

### 34.15.2. Additional/Missing Embedded SQL Statements [#](#ECPG-INFORMIX-STATEMENTS)

<a id="ECPG-INFORMIX-STATEMENTS-CLOSE-DATABASE"></a>

`CLOSE DATABASE` [#](#ECPG-INFORMIX-STATEMENTS-CLOSE-DATABASE)
:   This statement closes the current connection. In fact, this is a
    synonym for ECPG's `DISCONNECT CURRENT`:

    ```

    $CLOSE DATABASE;                /* close the current connection */
    EXEC SQL CLOSE DATABASE;
    ```
<a id="ECPG-INFORMIX-STATEMENTS-FREE-CURSOR-NAME"></a>

`FREE cursor_name` [#](#ECPG-INFORMIX-STATEMENTS-FREE-CURSOR-NAME)
:   Due to differences in how ECPG works compared to Informix's ESQL/C (namely, which steps
    are purely grammar transformations and which steps rely on the underlying run-time library)
    there is no `FREE cursor_name` statement in ECPG. This is because in ECPG,
    `DECLARE CURSOR` doesn't translate to a function call into
    the run-time library that uses to the cursor name. This means that there's no run-time
    bookkeeping of SQL cursors in the ECPG run-time library, only in the PostgreSQL server.
<a id="ECPG-INFORMIX-STATEMENTS-FREE-STATEMENT-NAME"></a>

`FREE statement_name` [#](#ECPG-INFORMIX-STATEMENTS-FREE-STATEMENT-NAME)
:   `FREE statement_name` is a synonym for `DEALLOCATE PREPARE statement_name`.

<a id="ECPG-INFORMIX-SQLDA"></a>

### 34.15.3. Informix-compatible SQLDA Descriptor Areas [#](#ECPG-INFORMIX-SQLDA)

Informix-compatible mode supports a different structure than the one described in
[Section 34.7.2](ecpg-descriptors.md#ECPG-SQLDA-DESCRIPTORS). See below:

```

struct sqlvar_compat
{
    short   sqltype;
    int     sqllen;
    char   *sqldata;
    short  *sqlind;
    char   *sqlname;
    char   *sqlformat;
    short   sqlitype;
    short   sqlilen;
    char   *sqlidata;
    int     sqlxid;
    char   *sqltypename;
    short   sqltypelen;
    short   sqlownerlen;
    short   sqlsourcetype;
    char   *sqlownername;
    int     sqlsourceid;
    char   *sqlilongdata;
    int     sqlflags;
    void   *sqlreserved;
};

struct sqlda_compat
{
    short  sqld;
    struct sqlvar_compat *sqlvar;
    char   desc_name[19];
    short  desc_occ;
    struct sqlda_compat *desc_next;
    void  *reserved;
};

typedef struct sqlvar_compat    sqlvar_t;
typedef struct sqlda_compat     sqlda_t;
```

The global properties are:

<a id="ECPG-INFORMIX-SQLDA-SQLD"></a>

`sqld` [#](#ECPG-INFORMIX-SQLDA-SQLD)
:   The number of fields in the `SQLDA` descriptor.
<a id="ECPG-INFORMIX-SQLDA-SQLVAR"></a>

`sqlvar` [#](#ECPG-INFORMIX-SQLDA-SQLVAR)
:   Pointer to the per-field properties.
<a id="ECPG-INFORMIX-SQLDA-DESC-NAME"></a>

`desc_name` [#](#ECPG-INFORMIX-SQLDA-DESC-NAME)
:   Unused, filled with zero-bytes.
<a id="ECPG-INFORMIX-SQLDA-DESC-OCC"></a>

`desc_occ` [#](#ECPG-INFORMIX-SQLDA-DESC-OCC)
:   Size of the allocated structure.
<a id="ECPG-INFORMIX-SQLDA-DESC-NEXT"></a>

`desc_next` [#](#ECPG-INFORMIX-SQLDA-DESC-NEXT)
:   Pointer to the next SQLDA structure if the result set contains more than one record.
<a id="ECPG-INFORMIX-SQLDA-RESERVED"></a>

`reserved` [#](#ECPG-INFORMIX-SQLDA-RESERVED)
:   Unused pointer, contains NULL. Kept for Informix-compatibility.

The per-field properties are below, they are stored in the `sqlvar` array:

<a id="ECPG-INFORMIX-SQLDA-SQLTYPE"></a>

`sqltype` [#](#ECPG-INFORMIX-SQLDA-SQLTYPE)
:   Type of the field. Constants are in `sqltypes.h`
<a id="ECPG-INFORMIX-SQLDA-SQLLEN"></a>

`sqllen` [#](#ECPG-INFORMIX-SQLDA-SQLLEN)
:   Length of the field data.
<a id="ECPG-INFORMIX-SQLDA-SQLDATA"></a>

`sqldata` [#](#ECPG-INFORMIX-SQLDA-SQLDATA)
:   Pointer to the field data. The pointer is of `char *` type,
    the data pointed by it is in a binary format. Example:

    ```

    int intval;

    switch (sqldata->sqlvar[i].sqltype)
    {
        case SQLINTEGER:
            intval = *(int *)sqldata->sqlvar[i].sqldata;
            break;
      ...
    }
    ```
<a id="ECPG-INFORMIX-SQLDA-SQLIND"></a>

`sqlind` [#](#ECPG-INFORMIX-SQLDA-SQLIND)
:   Pointer to the NULL indicator. If returned by DESCRIBE or FETCH then it's always a valid pointer.
    If used as input for `EXECUTE ... USING sqlda;` then NULL-pointer value means
    that the value for this field is non-NULL. Otherwise a valid pointer and `sqlitype`
    has to be properly set. Example:

    ```

    if (*(int2 *)sqldata->sqlvar[i].sqlind != 0)
        printf("value is NULL\n");
    ```
<a id="ECPG-INFORMIX-SQLDA-SQLNAME"></a>

`sqlname` [#](#ECPG-INFORMIX-SQLDA-SQLNAME)
:   Name of the field. 0-terminated string.
<a id="ECPG-INFORMIX-SQLDA-SQLFORMAT"></a>

`sqlformat` [#](#ECPG-INFORMIX-SQLDA-SQLFORMAT)
:   Reserved in Informix, value of [`PQfformat`](../libpq/libpq-exec.md#LIBPQ-PQFFORMAT) for the field.
<a id="ECPG-INFORMIX-SQLDA-SQLITYPE"></a>

`sqlitype` [#](#ECPG-INFORMIX-SQLDA-SQLITYPE)
:   Type of the NULL indicator data. It's always SQLSMINT when returning data from the server.
    When the `SQLDA` is used for a parameterized query, the data is treated
    according to the set type.
<a id="ECPG-INFORMIX-SQLDA-SQLILEN"></a>

`sqlilen` [#](#ECPG-INFORMIX-SQLDA-SQLILEN)
:   Length of the NULL indicator data.
<a id="ECPG-INFORMIX-SQLDA-SQLXID"></a>

`sqlxid` [#](#ECPG-INFORMIX-SQLDA-SQLXID)
:   Extended type of the field, result of [`PQftype`](../libpq/libpq-exec.md#LIBPQ-PQFTYPE).
<a id="ECPG-INFORMIX-SQLDA-SQLTYPENAME"></a>

`sqltypename`<br>`sqltypelen`<br>`sqlownerlen`<br>`sqlsourcetype`<br>`sqlownername`<br>`sqlsourceid`<br>`sqlflags`<br>`sqlreserved` [#](#ECPG-INFORMIX-SQLDA-SQLTYPENAME)
:   Unused.
<a id="ECPG-INFORMIX-SQLDA-SQLILONGDATA"></a>

`sqlilongdata` [#](#ECPG-INFORMIX-SQLDA-SQLILONGDATA)
:   It equals to `sqldata` if `sqllen` is larger than 32kB.

Example:

```

EXEC SQL INCLUDE sqlda.h;

    sqlda_t        *sqlda; /* This doesn't need to be under embedded DECLARE SECTION */

    EXEC SQL BEGIN DECLARE SECTION;
    char *prep_stmt = "select * from table1";
    int i;
    EXEC SQL END DECLARE SECTION;

    ...

    EXEC SQL PREPARE mystmt FROM :prep_stmt;

    EXEC SQL DESCRIBE mystmt INTO sqlda;

    printf("# of fields: %d\n", sqlda->sqld);
    for (i = 0; i < sqlda->sqld; i++)
      printf("field %d: \"%s\"\n", sqlda->sqlvar[i]->sqlname);

    EXEC SQL DECLARE mycursor CURSOR FOR mystmt;
    EXEC SQL OPEN mycursor;
    EXEC SQL WHENEVER NOT FOUND GOTO out;

    while (1)
    {
      EXEC SQL FETCH mycursor USING sqlda;
    }

    EXEC SQL CLOSE mycursor;

    free(sqlda); /* The main structure is all to be free(),
                  * sqlda and sqlda->sqlvar is in one allocated area */
```

For more information, see the `sqlda.h` header and the
`src/interfaces/ecpg/test/compat_informix/sqlda.pgc` regression test.

<a id="ECPG-INFORMIX-FUNCTIONS"></a>

### 34.15.4. Additional Functions [#](#ECPG-INFORMIX-FUNCTIONS)

<a id="ECPG-INFORMIX-FUNCTIONS-DECADD"></a>

`decadd` [#](#ECPG-INFORMIX-FUNCTIONS-DECADD)
:   Add two decimal type values.

    ```

    int decadd(decimal *arg1, decimal *arg2, decimal *sum);
    ```

    The function receives a pointer to the first operand of type decimal
    (`arg1`), a pointer to the second operand of type decimal
    (`arg2`) and a pointer to a value of type decimal that will
    contain the sum (`sum`). On success, the function returns 0.
    `ECPG_INFORMIX_NUM_OVERFLOW` is returned in case of overflow and
    `ECPG_INFORMIX_NUM_UNDERFLOW` in case of underflow. -1 is returned for
    other failures and `errno` is set to the respective `errno` number of the
    pgtypeslib.
<a id="ECPG-INFORMIX-FUNCTIONS-DECCMP"></a>

`deccmp` [#](#ECPG-INFORMIX-FUNCTIONS-DECCMP)
:   Compare two variables of type decimal.

    ```

    int deccmp(decimal *arg1, decimal *arg2);
    ```

    The function receives a pointer to the first decimal value
    (`arg1`), a pointer to the second decimal value
    (`arg2`) and returns an integer value that indicates which is
    the bigger value.

    * 1, if the value that `arg1` points to is bigger than the
      value that `var2` points to
    * -1, if the value that `arg1` points to is smaller than the
      value that `arg2` points to
    * 0, if the value that `arg1` points to and the value that
      `arg2` points to are equal
<a id="ECPG-INFORMIX-FUNCTIONS-DECCOPY"></a>

`deccopy` [#](#ECPG-INFORMIX-FUNCTIONS-DECCOPY)
:   Copy a decimal value.

    ```

    void deccopy(decimal *src, decimal *target);
    ```

    The function receives a pointer to the decimal value that should be
    copied as the first argument (`src`) and a pointer to the
    target structure of type decimal (`target`) as the second
    argument.
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVASC"></a>

`deccvasc` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVASC)
:   Convert a value from its ASCII representation into a decimal type.

    ```

    int deccvasc(char *cp, int len, decimal *np);
    ```

    The function receives a pointer to string that contains the string
    representation of the number to be converted (`cp`) as well
    as its length `len`. `np` is a pointer to the
    decimal value that saves the result of the operation.

    Valid formats are for example:
    `-2`,
    `.794`,
    `+3.44`,
    `592.49E07` or
    `-32.84e-4`.

    The function returns 0 on success. If overflow or underflow occurred,
    `ECPG_INFORMIX_NUM_OVERFLOW` or
    `ECPG_INFORMIX_NUM_UNDERFLOW` is returned. If the ASCII
    representation could not be parsed,
    `ECPG_INFORMIX_BAD_NUMERIC` is returned or
    `ECPG_INFORMIX_BAD_EXPONENT` if this problem occurred while
    parsing the exponent.
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVDBL"></a>

`deccvdbl` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVDBL)
:   Convert a value of type double to a value of type decimal.

    ```

    int deccvdbl(double dbl, decimal *np);
    ```

    The function receives the variable of type double that should be
    converted as its first argument (`dbl`). As the second
    argument (`np`), the function receives a pointer to the
    decimal variable that should hold the result of the operation.

    The function returns 0 on success and a negative value if the
    conversion failed.
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVINT"></a>

`deccvint` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVINT)
:   Convert a value of type int to a value of type decimal.

    ```

    int deccvint(int in, decimal *np);
    ```

    The function receives the variable of type int that should be
    converted as its first argument (`in`). As the second
    argument (`np`), the function receives a pointer to the
    decimal variable that should hold the result of the operation.

    The function returns 0 on success and a negative value if the
    conversion failed.
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVLONG"></a>

`deccvlong` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVLONG)
:   Convert a value of type long to a value of type decimal.

    ```

    int deccvlong(long lng, decimal *np);
    ```

    The function receives the variable of type long that should be
    converted as its first argument (`lng`). As the second
    argument (`np`), the function receives a pointer to the
    decimal variable that should hold the result of the operation.

    The function returns 0 on success and a negative value if the
    conversion failed.
<a id="ECPG-INFORMIX-FUNCTIONS-DECDIV"></a>

`decdiv` [#](#ECPG-INFORMIX-FUNCTIONS-DECDIV)
:   Divide two variables of type decimal.

    ```

    int decdiv(decimal *n1, decimal *n2, decimal *result);
    ```

    The function receives pointers to the variables that are the first
    (`n1`) and the second (`n2`) operands and
    calculates `n1`/`n2`. `result` is a
    pointer to the variable that should hold the result of the operation.

    On success, 0 is returned and a negative value if the division fails.
    If overflow or underflow occurred, the function returns
    `ECPG_INFORMIX_NUM_OVERFLOW` or
    `ECPG_INFORMIX_NUM_UNDERFLOW` respectively. If an attempt to
    divide by zero is observed, the function returns
    `ECPG_INFORMIX_DIVIDE_ZERO`.
<a id="ECPG-INFORMIX-FUNCTIONS-DECMUL"></a>

`decmul` [#](#ECPG-INFORMIX-FUNCTIONS-DECMUL)
:   Multiply two decimal values.

    ```

    int decmul(decimal *n1, decimal *n2, decimal *result);
    ```

    The function receives pointers to the variables that are the first
    (`n1`) and the second (`n2`) operands and
    calculates `n1`\*`n2`. `result` is a
    pointer to the variable that should hold the result of the operation.

    On success, 0 is returned and a negative value if the multiplication
    fails. If overflow or underflow occurred, the function returns
    `ECPG_INFORMIX_NUM_OVERFLOW` or
    `ECPG_INFORMIX_NUM_UNDERFLOW` respectively.
<a id="ECPG-INFORMIX-FUNCTIONS-DECSUB"></a>

`decsub` [#](#ECPG-INFORMIX-FUNCTIONS-DECSUB)
:   Subtract one decimal value from another.

    ```

    int decsub(decimal *n1, decimal *n2, decimal *result);
    ```

    The function receives pointers to the variables that are the first
    (`n1`) and the second (`n2`) operands and
    calculates `n1`-`n2`. `result` is a
    pointer to the variable that should hold the result of the operation.

    On success, 0 is returned and a negative value if the subtraction
    fails. If overflow or underflow occurred, the function returns
    `ECPG_INFORMIX_NUM_OVERFLOW` or
    `ECPG_INFORMIX_NUM_UNDERFLOW` respectively.
<a id="ECPG-INFORMIX-FUNCTIONS-DECTOASC"></a>

`dectoasc` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOASC)
:   Convert a variable of type decimal to its ASCII representation in a C
    char\* string.

    ```

    int dectoasc(decimal *np, char *cp, int len, int right)
    ```

    The function receives a pointer to a variable of type decimal
    (`np`) that it converts to its textual representation.
    `cp` is the buffer that should hold the result of the
    operation. The parameter `right` specifies, how many digits
    right of the decimal point should be included in the output. The result
    will be rounded to this number of decimal digits. Setting
    `right` to -1 indicates that all available decimal digits
    should be included in the output. If the length of the output buffer,
    which is indicated by `len` is not sufficient to hold the
    textual representation including the trailing zero byte, only a
    single `*` character is stored in the result and -1 is
    returned.

    The function returns either -1 if the buffer `cp` was too
    small or `ECPG_INFORMIX_OUT_OF_MEMORY` if memory was
    exhausted.
<a id="ECPG-INFORMIX-FUNCTIONS-DECTODBL"></a>

`dectodbl` [#](#ECPG-INFORMIX-FUNCTIONS-DECTODBL)
:   Convert a variable of type decimal to a double.

    ```

    int dectodbl(decimal *np, double *dblp);
    ```

    The function receives a pointer to the decimal value to convert
    (`np`) and a pointer to the double variable that
    should hold the result of the operation (`dblp`).

    On success, 0 is returned and a negative value if the conversion
    failed.
<a id="ECPG-INFORMIX-FUNCTIONS-DECTOINT"></a>

`dectoint` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOINT)
:   Convert a variable of type decimal to an integer.

    ```

    int dectoint(decimal *np, int *ip);
    ```

    The function receives a pointer to the decimal value to convert
    (`np`) and a pointer to the integer variable that
    should hold the result of the operation (`ip`).

    On success, 0 is returned and a negative value if the conversion
    failed. If an overflow occurred, `ECPG_INFORMIX_NUM_OVERFLOW`
    is returned.

    Note that the ECPG implementation differs from the Informix
    implementation. Informix limits an integer to the range from -32767 to
    32767, while the limits in the ECPG implementation depend on the
    architecture (`INT_MIN .. INT_MAX`).
<a id="ECPG-INFORMIX-FUNCTIONS-DECTOLONG"></a>

`dectolong` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOLONG)
:   Convert a variable of type decimal to a long integer.

    ```

    int dectolong(decimal *np, long *lngp);
    ```

    The function receives a pointer to the decimal value to convert
    (`np`) and a pointer to the long variable that
    should hold the result of the operation (`lngp`).

    On success, 0 is returned and a negative value if the conversion
    failed. If an overflow occurred, `ECPG_INFORMIX_NUM_OVERFLOW`
    is returned.

    Note that the ECPG implementation differs from the Informix
    implementation. Informix limits a long integer to the range from
    -2,147,483,647 to 2,147,483,647, while the limits in the ECPG
    implementation depend on the architecture (`-LONG_MAX ..
    LONG_MAX`).
<a id="ECPG-INFORMIX-FUNCTIONS-RDATESTR"></a>

`rdatestr` [#](#ECPG-INFORMIX-FUNCTIONS-RDATESTR)
:   Converts a date to a C char\* string.

    ```

    int rdatestr(date d, char *str);
    ```

    The function receives two arguments, the first one is the date to
    convert (`d`) and the second one is a pointer to the target
    string. The output format is always `yyyy-mm-dd`, so you need
    to allocate at least 11 bytes (including the zero-byte terminator) for the
    string.

    The function returns 0 on success and a negative value in case of
    error.

    Note that ECPG's implementation differs from the Informix
    implementation. In Informix the format can be influenced by setting
    environment variables. In ECPG however, you cannot change the output
    format.
<a id="ECPG-INFORMIX-FUNCTIONS-RSTRDATE"></a>

`rstrdate` [#](#ECPG-INFORMIX-FUNCTIONS-RSTRDATE)
:   Parse the textual representation of a date.

    ```

    int rstrdate(char *str, date *d);
    ```

    The function receives the textual representation of the date to convert
    (`str`) and a pointer to a variable of type date
    (`d`). This function does not allow you to specify a format
    mask. It uses the default format mask of Informix which is
    `mm/dd/yyyy`. Internally, this function is implemented by
    means of `rdefmtdate`. Therefore, `rstrdate` is
    not faster and if you have the choice you should opt for
    `rdefmtdate` which allows you to specify the format mask
    explicitly.

    The function returns the same values as `rdefmtdate`.
<a id="ECPG-INFORMIX-FUNCTIONS-RTODAY"></a>

`rtoday` [#](#ECPG-INFORMIX-FUNCTIONS-RTODAY)
:   Get the current date.

    ```

    void rtoday(date *d);
    ```

    The function receives a pointer to a date variable (`d`)
    that it sets to the current date.

    Internally this function uses the [`PGTYPESdate_today`](ecpg-pgtypes.md#PGTYPESDATETODAY)
    function.
<a id="ECPG-INFORMIX-FUNCTIONS-RJULMDY"></a>

`rjulmdy` [#](#ECPG-INFORMIX-FUNCTIONS-RJULMDY)
:   Extract the values for the day, the month and the year from a variable
    of type date.

    ```

    int rjulmdy(date d, short mdy[3]);
    ```

    The function receives the date `d` and a pointer to an array
    of 3 short integer values `mdy`. The variable name indicates
    the sequential order: `mdy[0]` will be set to contain the
    number of the month, `mdy[1]` will be set to the value of the
    day and `mdy[2]` will contain the year.

    The function always returns 0 at the moment.

    Internally the function uses the [`PGTYPESdate_julmdy`](ecpg-pgtypes.md#PGTYPESDATEJULMDY)
    function.
<a id="ECPG-INFORMIX-FUNCTIONS-RDEFMTDATE"></a>

`rdefmtdate` [#](#ECPG-INFORMIX-FUNCTIONS-RDEFMTDATE)
:   Use a format mask to convert a character string to a value of type
    date.

    ```

    int rdefmtdate(date *d, char *fmt, char *str);
    ```

    The function receives a pointer to the date value that should hold the
    result of the operation (`d`), the format mask to use for
    parsing the date (`fmt`) and the C char\* string containing
    the textual representation of the date (`str`). The textual
    representation is expected to match the format mask. However you do not
    need to have a 1:1 mapping of the string to the format mask. The
    function only analyzes the sequential order and looks for the literals
    `yy` or `yyyy` that indicate the
    position of the year, `mm` to indicate the position of
    the month and `dd` to indicate the position of the
    day.

    The function returns the following values:

    * 0 - The function terminated successfully.
    * `ECPG_INFORMIX_ENOSHORTDATE` - The date does not contain
      delimiters between day, month and year. In this case the input
      string must be exactly 6 or 8 bytes long but isn't.
    * `ECPG_INFORMIX_ENOTDMY` - The format string did not
      correctly indicate the sequential order of year, month and day.
    * `ECPG_INFORMIX_BAD_DAY` - The input string does not
      contain a valid day.
    * `ECPG_INFORMIX_BAD_MONTH` - The input string does not
      contain a valid month.
    * `ECPG_INFORMIX_BAD_YEAR` - The input string does not
      contain a valid year.

    Internally this function is implemented to use the [`PGTYPESdate_defmt_asc`](ecpg-pgtypes.md#PGTYPESDATEDEFMTASC) function. See the reference there for a
    table of example input.
<a id="ECPG-INFORMIX-FUNCTIONS-RFMTDATE"></a>

`rfmtdate` [#](#ECPG-INFORMIX-FUNCTIONS-RFMTDATE)
:   Convert a variable of type date to its textual representation using a
    format mask.

    ```

    int rfmtdate(date d, char *fmt, char *str);
    ```

    The function receives the date to convert (`d`), the format
    mask (`fmt`) and the string that will hold the textual
    representation of the date (`str`).

    On success, 0 is returned and a negative value if an error occurred.

    Internally this function uses the [`PGTYPESdate_fmt_asc`](ecpg-pgtypes.md#PGTYPESDATEFMTASC)
    function, see the reference there for examples.
<a id="ECPG-INFORMIX-FUNCTIONS-RMDYJUL"></a>

`rmdyjul` [#](#ECPG-INFORMIX-FUNCTIONS-RMDYJUL)
:   Create a date value from an array of 3 short integers that specify the
    day, the month and the year of the date.

    ```

    int rmdyjul(short mdy[3], date *d);
    ```

    The function receives the array of the 3 short integers
    (`mdy`) and a pointer to a variable of type date that should
    hold the result of the operation.

    Currently the function returns always 0.

    Internally the function is implemented to use the function [`PGTYPESdate_mdyjul`](ecpg-pgtypes.md#PGTYPESDATEMDYJUL).
<a id="ECPG-INFORMIX-FUNCTIONS-RDAYOFWEEK"></a>

`rdayofweek` [#](#ECPG-INFORMIX-FUNCTIONS-RDAYOFWEEK)
:   Return a number representing the day of the week for a date value.

    ```

    int rdayofweek(date d);
    ```

    The function receives the date variable `d` as its only
    argument and returns an integer that indicates the day of the week for
    this date.

    * 0 - Sunday
    * 1 - Monday
    * 2 - Tuesday
    * 3 - Wednesday
    * 4 - Thursday
    * 5 - Friday
    * 6 - Saturday

    Internally the function is implemented to use the function [`PGTYPESdate_dayofweek`](ecpg-pgtypes.md#PGTYPESDATEDAYOFWEEK).
<a id="ECPG-INFORMIX-FUNCTIONS-DTCURRENT"></a>

`dtcurrent` [#](#ECPG-INFORMIX-FUNCTIONS-DTCURRENT)
:   Retrieve the current timestamp.

    ```

    void dtcurrent(timestamp *ts);
    ```

    The function retrieves the current timestamp and saves it into the
    timestamp variable that `ts` points to.
<a id="ECPG-INFORMIX-FUNCTIONS-DTCVASC"></a>

`dtcvasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTCVASC)
:   Parses a timestamp from its textual representation
    into a timestamp variable.

    ```

    int dtcvasc(char *str, timestamp *ts);
    ```

    The function receives the string to parse (`str`) and a
    pointer to the timestamp variable that should hold the result of the
    operation (`ts`).

    The function returns 0 on success and a negative value in case of
    error.

    Internally this function uses the [`PGTYPEStimestamp_from_asc`](ecpg-pgtypes.md#PGTYPESTIMESTAMPFROMASC) function. See the reference there
    for a table with example inputs.
<a id="ECPG-INFORMIX-FUNCTIONS-DTCVFMTASC"></a>

`dtcvfmtasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTCVFMTASC)
:   Parses a timestamp from its textual representation
    using a format mask into a timestamp variable.

    ```

    dtcvfmtasc(char *inbuf, char *fmtstr, timestamp *dtvalue)
    ```

    The function receives the string to parse (`inbuf`), the
    format mask to use (`fmtstr`) and a pointer to the timestamp
    variable that should hold the result of the operation
    (`dtvalue`).

    This function is implemented by means of the [`PGTYPEStimestamp_defmt_asc`](ecpg-pgtypes.md#PGTYPESTIMESTAMPDEFMTASC) function. See the documentation
    there for a list of format specifiers that can be used.

    The function returns 0 on success and a negative value in case of
    error.
<a id="ECPG-INFORMIX-FUNCTIONS-DTSUB"></a>

`dtsub` [#](#ECPG-INFORMIX-FUNCTIONS-DTSUB)
:   Subtract one timestamp from another and return a variable of type
    interval.

    ```

    int dtsub(timestamp *ts1, timestamp *ts2, interval *iv);
    ```

    The function will subtract the timestamp variable that `ts2`
    points to from the timestamp variable that `ts1` points to
    and will store the result in the interval variable that `iv`
    points to.

    Upon success, the function returns 0 and a negative value if an
    error occurred.
<a id="ECPG-INFORMIX-FUNCTIONS-DTTOASC"></a>

`dttoasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTTOASC)
:   Convert a timestamp variable to a C char\* string.

    ```

    int dttoasc(timestamp *ts, char *output);
    ```

    The function receives a pointer to the timestamp variable to convert
    (`ts`) and the string that should hold the result of the
    operation (`output`). It converts `ts` to its
    textual representation according to the SQL standard, which is
    be `YYYY-MM-DD HH:MM:SS`.

    Upon success, the function returns 0 and a negative value if an
    error occurred.
<a id="ECPG-INFORMIX-FUNCTIONS-DTTOFMTASC"></a>

`dttofmtasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTTOFMTASC)
:   Convert a timestamp variable to a C char\* using a format mask.

    ```

    int dttofmtasc(timestamp *ts, char *output, int str_len, char *fmtstr);
    ```

    The function receives a pointer to the timestamp to convert as its
    first argument (`ts`), a pointer to the output buffer
    (`output`), the maximal length that has been allocated for
    the output buffer (`str_len`) and the format mask to
    use for the conversion (`fmtstr`).

    Upon success, the function returns 0 and a negative value if an
    error occurred.

    Internally, this function uses the [`PGTYPEStimestamp_fmt_asc`](ecpg-pgtypes.md#PGTYPESTIMESTAMPFMTASC) function. See the reference there for
    information on what format mask specifiers can be used.
<a id="ECPG-INFORMIX-FUNCTIONS-INTOASC"></a>

`intoasc` [#](#ECPG-INFORMIX-FUNCTIONS-INTOASC)
:   Convert an interval variable to a C char\* string.

    ```

    int intoasc(interval *i, char *str);
    ```

    The function receives a pointer to the interval variable to convert
    (`i`) and the string that should hold the result of the
    operation (`str`). It converts `i` to its
    textual representation according to the SQL standard, which is
    be `YYYY-MM-DD HH:MM:SS`.

    Upon success, the function returns 0 and a negative value if an
    error occurred.
<a id="ECPG-INFORMIX-FUNCTIONS-RFMTLONG"></a>

`rfmtlong` [#](#ECPG-INFORMIX-FUNCTIONS-RFMTLONG)
:   Convert a long integer value to its textual representation using a
    format mask.

    ```

    int rfmtlong(long lng_val, char *fmt, char *outbuf);
    ```

    The function receives the long value `lng_val`, the format
    mask `fmt` and a pointer to the output buffer
    `outbuf`. It converts the long value according to the format
    mask to its textual representation.

    The format mask can be composed of the following format specifying
    characters:

    * `*` (asterisk) - if this position would be blank
      otherwise, fill it with an asterisk.
    * `&` (ampersand) - if this position would be
      blank otherwise, fill it with a zero.
    * `#` - turn leading zeroes into blanks.
    * `<` - left-justify the number in the string.
    * `,` (comma) - group numbers of four or more digits
      into groups of three digits separated by a comma.
    * `.` (period) - this character separates the
      whole-number part of the number from the fractional part.
    * `-` (minus) - the minus sign appears if the number
      is a negative value.
    * `+` (plus) - the plus sign appears if the number is
      a positive value.
    * `(` - this replaces the minus sign in front of the
      negative number. The minus sign will not appear.
    * `)` - this character replaces the minus and is
      printed behind the negative value.
    * `$` - the currency symbol.
<a id="ECPG-INFORMIX-FUNCTIONS-RUPSHIFT"></a>

`rupshift` [#](#ECPG-INFORMIX-FUNCTIONS-RUPSHIFT)
:   Convert a string to upper case.

    ```

    void rupshift(char *str);
    ```

    The function receives a pointer to the string and transforms every
    lower case character to upper case.
<a id="ECPG-INFORMIX-FUNCTIONS-BYLENG"></a>

`byleng` [#](#ECPG-INFORMIX-FUNCTIONS-BYLENG)
:   Return the number of characters in a string without counting trailing
    blanks.

    ```

    int byleng(char *str, int len);
    ```

    The function expects a fixed-length string as its first argument
    (`str`) and its length as its second argument
    (`len`). It returns the number of significant characters,
    that is the length of the string without trailing blanks.
<a id="ECPG-INFORMIX-FUNCTIONS-LDCHAR"></a>

`ldchar` [#](#ECPG-INFORMIX-FUNCTIONS-LDCHAR)
:   Copy a fixed-length string into a null-terminated string.

    ```

    void ldchar(char *src, int len, char *dest);
    ```

    The function receives the fixed-length string to copy
    (`src`), its length (`len`) and a pointer to the
    destination memory (`dest`). Note that you need to reserve at
    least `len+1` bytes for the string that `dest`
    points to. The function copies at most `len` bytes to the new
    location (less if the source string has trailing blanks) and adds the
    null-terminator.
<a id="ECPG-INFORMIX-FUNCTIONS-RGETMSG"></a>

`rgetmsg` [#](#ECPG-INFORMIX-FUNCTIONS-RGETMSG)
:   ```

    int rgetmsg(int msgnum, char *s, int maxsize);
    ```

    This function exists but is not implemented at the moment!
<a id="ECPG-INFORMIX-FUNCTIONS-RTYPALIGN"></a>

`rtypalign` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPALIGN)
:   ```

    int rtypalign(int offset, int type);
    ```

    This function exists but is not implemented at the moment!
<a id="ECPG-INFORMIX-FUNCTIONS-RTYPMSIZE"></a>

`rtypmsize` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPMSIZE)
:   ```

    int rtypmsize(int type, int len);
    ```

    This function exists but is not implemented at the moment!
<a id="ECPG-INFORMIX-FUNCTIONS-RTYPWIDTH"></a>

`rtypwidth` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPWIDTH)
:   ```

    int rtypwidth(int sqltype, int sqllen);
    ```

    This function exists but is not implemented at the moment!
<a id="RSETNULL"></a>

`rsetnull` [#](#RSETNULL)
:   Set a variable to NULL.

    ```

    int rsetnull(int t, char *ptr);
    ```

    The function receives an integer that indicates the type of the
    variable and a pointer to the variable itself that is cast to a C
    char\* pointer.

    The following types exist:

    * `CCHARTYPE` - For a variable of type `char` or `char*`
    * `CSHORTTYPE` - For a variable of type `short int`
    * `CINTTYPE` - For a variable of type `int`
    * `CBOOLTYPE` - For a variable of type `boolean`
    * `CFLOATTYPE` - For a variable of type `float`
    * `CLONGTYPE` - For a variable of type `long`
    * `CDOUBLETYPE` - For a variable of type `double`
    * `CDECIMALTYPE` - For a variable of type `decimal`
    * `CDATETYPE` - For a variable of type `date`
    * `CDTIMETYPE` - For a variable of type `timestamp`

    Here is an example of a call to this function:

    ```

    $char c[] = "abc       ";
    $short s = 17;
    $int i = -74874;

    rsetnull(CCHARTYPE, (char *) c);
    rsetnull(CSHORTTYPE, (char *) &s);
    rsetnull(CINTTYPE, (char *) &i);
    ```
<a id="ECPG-INFORMIX-FUNCTIONS-RISNULL"></a>

`risnull` [#](#ECPG-INFORMIX-FUNCTIONS-RISNULL)
:   Test if a variable is NULL.

    ```

    int risnull(int t, char *ptr);
    ```

    The function receives the type of the variable to test (`t`)
    as well a pointer to this variable (`ptr`). Note that the
    latter needs to be cast to a char\*. See the function [`rsetnull`](ecpg-informix-compat.md#RSETNULL) for a list of possible variable types.

    Here is an example of how to use this function:

    ```

    $char c[] = "abc       ";
    $short s = 17;
    $int i = -74874;

    risnull(CCHARTYPE, (char *) c);
    risnull(CSHORTTYPE, (char *) &s);
    risnull(CINTTYPE, (char *) &i);
    ```

<a id="ECPG-INFORMIX-CONSTANTS"></a>

### 34.15.5. Additional Constants [#](#ECPG-INFORMIX-CONSTANTS)

Note that all constants here describe errors and all of them are defined
to represent negative values. In the descriptions of the different
constants you can also find the value that the constants represent in the
current implementation. However you should not rely on this number. You can
however rely on the fact all of them are defined to represent negative
values.

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-OVERFLOW"></a>

`ECPG_INFORMIX_NUM_OVERFLOW` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-OVERFLOW)
:   Functions return this value if an overflow occurred in a
    calculation. Internally it is defined as -1200 (the Informix
    definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-UNDERFLOW"></a>

`ECPG_INFORMIX_NUM_UNDERFLOW` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-UNDERFLOW)
:   Functions return this value if an underflow occurred in a calculation.
    Internally it is defined as -1201 (the Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DIVIDE-ZERO"></a>

`ECPG_INFORMIX_DIVIDE_ZERO` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DIVIDE-ZERO)
:   Functions return this value if an attempt to divide by zero is
    observed. Internally it is defined as -1202 (the Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-YEAR"></a>

`ECPG_INFORMIX_BAD_YEAR` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-YEAR)
:   Functions return this value if a bad value for a year was found while
    parsing a date. Internally it is defined as -1204 (the Informix
    definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-MONTH"></a>

`ECPG_INFORMIX_BAD_MONTH` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-MONTH)
:   Functions return this value if a bad value for a month was found while
    parsing a date. Internally it is defined as -1205 (the Informix
    definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DAY"></a>

`ECPG_INFORMIX_BAD_DAY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DAY)
:   Functions return this value if a bad value for a day was found while
    parsing a date. Internally it is defined as -1206 (the Informix
    definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOSHORTDATE"></a>

`ECPG_INFORMIX_ENOSHORTDATE` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOSHORTDATE)
:   Functions return this value if a parsing routine needs a short date
    representation but did not get the date string in the right length.
    Internally it is defined as -1209 (the Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DATE-CONVERT"></a>

`ECPG_INFORMIX_DATE_CONVERT` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DATE-CONVERT)
:   Functions return this value if an error occurred during date
    formatting. Internally it is defined as -1210 (the
    Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-OUT-OF-MEMORY"></a>

`ECPG_INFORMIX_OUT_OF_MEMORY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-OUT-OF-MEMORY)
:   Functions return this value if memory was exhausted during
    their operation. Internally it is defined as -1211 (the
    Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOTDMY"></a>

`ECPG_INFORMIX_ENOTDMY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOTDMY)
:   Functions return this value if a parsing routine was supposed to get a
    format mask (like `mmddyy`) but not all fields were listed
    correctly. Internally it is defined as -1212 (the Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-NUMERIC"></a>

`ECPG_INFORMIX_BAD_NUMERIC` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-NUMERIC)
:   Functions return this value either if a parsing routine cannot parse
    the textual representation for a numeric value because it contains
    errors or if a routine cannot complete a calculation involving numeric
    variables because at least one of the numeric variables is invalid.
    Internally it is defined as -1213 (the Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-EXPONENT"></a>

`ECPG_INFORMIX_BAD_EXPONENT` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-EXPONENT)
:   Functions return this value if a parsing routine cannot parse
    an exponent. Internally it is defined as -1216 (the
    Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DATE"></a>

`ECPG_INFORMIX_BAD_DATE` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DATE)
:   Functions return this value if a parsing routine cannot parse
    a date. Internally it is defined as -1218 (the
    Informix definition).
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-EXTRA-CHARS"></a>

`ECPG_INFORMIX_EXTRA_CHARS` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-EXTRA-CHARS)
:   Functions return this value if a parsing routine is passed extra
    characters it cannot parse. Internally it is defined as -1264 (the
    Informix definition).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-informix-compat.html)（英文原文，待翻譯）
