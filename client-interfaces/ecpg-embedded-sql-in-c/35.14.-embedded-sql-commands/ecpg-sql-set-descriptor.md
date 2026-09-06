<a id="ECPG-SQL-SET-DESCRIPTOR"></a>

# SET DESCRIPTOR

SET DESCRIPTOR — set information in an SQL descriptor area

## Synopsis

```

SET DESCRIPTOR descriptor_name descriptor_header_item = value
SET DESCRIPTOR descriptor_name VALUE number descriptor_item = value [, ...]
```

<a id="id-1.7.5.20.16.3"></a>

## Description

`SET DESCRIPTOR` populates an SQL descriptor area with values. The descriptor area is then typically used to bind parameters in a prepared query execution.

This command has two forms: The first form applies to the descriptor “header”, which is independent of a particular datum. The second form assigns values to particular datums, identified by number.

<a id="id-1.7.5.20.16.4"></a>

## Parameters

<em class="replaceable"><code>descriptor&#95;name</code></em>

A descriptor name.

<em class="replaceable"><code>descriptor&#95;header&#95;item</code></em>

A token identifying which header information item to set. Only `COUNT`, to set the number of descriptor items, is currently supported.

<em class="replaceable"><code>number</code></em>

The number of the descriptor item to set. The count starts at 1.

<em class="replaceable"><code>descriptor&#95;item</code></em>

A token identifying which item of information to set in the descriptor. See [Section 36.7.1](../35.7.-using-descriptor-areas.md#ECPG-NAMED-DESCRIPTORS) for a list of supported items.

<em class="replaceable"><code>value</code></em>

A value to store into the descriptor item. This can be an SQL constant or a host variable.

<a id="id-1.7.5.20.16.5"></a>

## Examples

```

EXEC SQL SET DESCRIPTOR indesc COUNT = 1;
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = 2;
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = :val1;
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val1, DATA = 'some string';
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val2null, DATA = :val2;
```

<a id="id-1.7.5.20.16.6"></a>

## Compatibility

`SET DESCRIPTOR` is specified in the SQL standard.

<a id="id-1.7.5.20.16.7"></a>

## See Also

[ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-set-descriptor.html)（英文原文，待翻譯）
