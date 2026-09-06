<a id="ECPG-SQL-TYPE"></a>

# TYPE

TYPE — 定義新的資料型別

## 語法

```

TYPE type_name IS ctype
```

<a id="id-1.7.5.20.17.3"></a>

## 說明

`TYPE` 命令定義新的 C 型別。它等同於在宣告區段中放入 `typedef`。

只有以 `-c` 選項執行 `ecpg` 時，才會識別此命令。

<a id="id-1.7.5.20.17.4"></a>

## 參數

<em class="replaceable"><code>type&#95;name</code></em>

新型別的名稱，必須是有效的 C 型別名稱。

<em class="replaceable"><code>ctype</code></em>

C 型別規格。

<a id="id-1.7.5.20.17.5"></a>

## 範例

```

EXEC SQL TYPE customer IS
    struct
    {
        varchar name[50];
        int     phone;
    };

EXEC SQL TYPE cust_ind IS
    struct ind
    {
        short   name_ind;
        short   phone_ind;
    };

EXEC SQL TYPE c IS char reference;
EXEC SQL TYPE ind IS union { int integer; short smallint; };
EXEC SQL TYPE intarray IS int[AMOUNT];
EXEC SQL TYPE str IS varchar[BUFFERSIZ];
EXEC SQL TYPE string IS char[11];
```

以下是使用 `EXEC SQL TYPE` 的範例程式：

```

EXEC SQL WHENEVER SQLERROR SQLPRINT;

EXEC SQL TYPE tt IS
    struct
    {
        varchar v[256];
        int     i;
    };

EXEC SQL TYPE tt_ind IS
    struct ind {
        short   v_ind;
        short   i_ind;
    };

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    tt t;
    tt_ind t_ind;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL SELECT current_database(), 256 INTO :t:t_ind LIMIT 1;

    printf("t.v = %s\n", t.v.arr);
    printf("t.i = %d\n", t.i);

    printf("t_ind.v_ind = %d\n", t_ind.v_ind);
    printf("t_ind.i_ind = %d\n", t_ind.i_ind);

    EXEC SQL DISCONNECT con1;

    return 0;
}
```

此程式的輸出如下：

```

t.v = testdb
t.i = 256
t_ind.v_ind = 0
t_ind.i_ind = 0
```

<a id="id-1.7.5.20.17.6"></a>

## 相容性

`TYPE` 命令是 PostgreSQL 擴充功能。

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-type.html)
