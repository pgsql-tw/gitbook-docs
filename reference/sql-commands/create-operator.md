<a id="SQL-CREATEOPERATOR"></a><a id="id-1.9.3.72.1"></a>

# CREATE OPERATOR

CREATE OPERATOR — define a new operator

## Synopsis

```

CREATE OPERATOR name (
    {FUNCTION|PROCEDURE} = function_name
    [, LEFTARG = left_type ] [, RIGHTARG = right_type ]
    [, COMMUTATOR = com_op ] [, NEGATOR = neg_op ]
    [, RESTRICT = res_proc ] [, JOIN = join_proc ]
    [, HASHES ] [, MERGES ]
)
```

<a id="id-1.9.3.72.5"></a>

## Description

`CREATE OPERATOR` defines a new operator, <em class="replaceable"><code>name</code></em>. The user who defines an operator becomes its owner. If a schema name is given then the operator is created in the specified schema. Otherwise it is created in the current schema.

The operator name is a sequence of up to `NAMEDATALEN`-1 (63 by default) characters from the following list:

<br>
+ - &#42; / < > = ~ ! @ # % ^ & | ` ?<br>

There are a few restrictions on your choice of name:

* `--` and `/*` cannot appear anywhere in an operator name, since they will be taken as the start of a comment.
* A multicharacter operator name cannot end in `+` or `-`, unless the name also contains at least one of these characters:

  <br>
  ~ ! @ # % ^ & | ` ?<br>

  For example, `@-` is an allowed operator name, but `*-` is not. This restriction allows PostgreSQL to parse SQL-compliant commands without requiring spaces between tokens.
* The symbol `=>` is reserved by the SQL grammar, so it cannot be used as an operator name.

The operator `!=` is mapped to `<>` on input, so these two names are always equivalent.

For binary operators, both `LEFTARG` and `RIGHTARG` must be defined. For prefix operators only `RIGHTARG` should be defined. The <em class="replaceable"><code>function&#95;name</code></em> function must have been previously defined using `CREATE FUNCTION` and must be defined to accept the correct number of arguments (either one or two) of the indicated types.

In the syntax of `CREATE OPERATOR`, the keywords `FUNCTION` and `PROCEDURE` are equivalent, but the referenced function must in any case be a function, not a procedure. The use of the keyword `PROCEDURE` here is historical and deprecated.

The other clauses specify optional operator optimization clauses. Their meaning is detailed in [Section 38.15](../../server-programming/extending-sql/operator-optimization-information.md).

To be able to create an operator, you must have `USAGE` privilege on the argument types and the return type, as well as `EXECUTE` privilege on the underlying function. If a commutator or negator operator is specified, you must own these operators.

<a id="id-1.9.3.72.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of the operator to be defined. See above for allowable characters. The name can be schema-qualified, for example `CREATE OPERATOR myschema.+ (...)`. If not, then the operator is created in the current schema. Two operators in the same schema can have the same name if they operate on different data types. This is called <em class="firstterm">overloading</em>.

<em class="replaceable"><code>function&#95;name</code></em>

The function used to implement this operator.

<em class="replaceable"><code>left&#95;type</code></em>

The data type of the operator's left operand, if any. This option would be omitted for a prefix operator.

<em class="replaceable"><code>right&#95;type</code></em>

The data type of the operator's right operand.

<em class="replaceable"><code>com&#95;op</code></em>

The commutator of this operator.

<em class="replaceable"><code>neg&#95;op</code></em>

The negator of this operator.

<em class="replaceable"><code>res&#95;proc</code></em>

The restriction selectivity estimator function for this operator.

<em class="replaceable"><code>join&#95;proc</code></em>

The join selectivity estimator function for this operator.

`HASHES`

Indicates this operator can support a hash join.

`MERGES`

Indicates this operator can support a merge join.

To give a schema-qualified operator name in <em class="replaceable"><code>com&#95;op</code></em> or the other optional arguments, use the `OPERATOR()` syntax, for example:

```

COMMUTATOR = OPERATOR(myschema.===) ,
```

<a id="id-1.9.3.72.7"></a>

## Notes

Refer to [Section 38.14](../../server-programming/extending-sql/user-defined-operators.md) for further information.

It is not possible to specify an operator's lexical precedence in `CREATE OPERATOR`, because the parser's precedence behavior is hard-wired. See [Section 4.1.6](https://www.postgresql.org/docs/15/sql-syntax-lexical.html#SQL-PRECEDENCE) for precedence details.

The obsolete options `SORT1`, `SORT2`, `LTCMP`, and `GTCMP` were formerly used to specify the names of sort operators associated with a merge-joinable operator. This is no longer necessary, since information about associated operators is found by looking at B-tree operator families instead. If one of these options is given, it is ignored except for implicitly setting `MERGES` true.

Use [`DROP OPERATOR`](drop-operator.md) to delete user-defined operators from a database. Use [`ALTER OPERATOR`](alter-operator.md) to modify operators in a database.

<a id="id-1.9.3.72.8"></a>

## Examples

The following command defines a new operator, area-equality, for the data type `box`:

```

CREATE OPERATOR === (
    LEFTARG = box,
    RIGHTARG = box,
    FUNCTION = area_equal_function,
    COMMUTATOR = ===,
    NEGATOR = !==,
    RESTRICT = area_restriction_function,
    JOIN = area_join_function,
    HASHES, MERGES
);
```

<a id="id-1.9.3.72.9"></a>

## Compatibility

`CREATE OPERATOR` is a PostgreSQL extension. There are no provisions for user-defined operators in the SQL standard.

<a id="id-1.9.3.72.10"></a>

## See Also

[ALTER OPERATOR](alter-operator.md), [CREATE OPERATOR CLASS](create-operator-class.md), [DROP OPERATOR](drop-operator.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-createoperator.html)（英文原文，待翻譯）
