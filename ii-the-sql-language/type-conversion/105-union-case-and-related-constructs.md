# 10.5. UNION、CASE等相關操作[^1]

SQL`UNION`constructs must match up possibly dissimilar types to become a single result set. The resolution algorithm is applied separately to each output column of a union query. The`INTERSECT`and`EXCEPT`constructs resolve dissimilar types in the same way as`UNION`. The`CASE`,`ARRAY`,`VALUES`,`GREATEST`and`LEAST`constructs use the identical algorithm to match up their component expressions and select a result data type.

**Type Resolution for`UNION`,`CASE`, and Related Constructs**

1. If all inputs are of the same type, and it is not`unknown`, resolve as that type.

2. If any input is of a domain type, treat it as being of the domain's base type for all subsequent steps.[\[9\]](https://www.postgresql.org/docs/10/static/typeconv-union-case.html#ftn.idm46249849266800)

3. If all inputs are of type`unknown`, resolve as type`text`\(the preferred type of the string category\). Otherwise,`unknown`inputs are ignored for the purposes of the remaining rules.

4. If the non-unknown inputs are not all of the same type category, fail.

5. Choose the first non-unknown input type which is a preferred type in that category, if there is one.

6. Otherwise, choose the last non-unknown input type that allows all the preceding non-unknown inputs to be implicitly converted to it. \(There always is such a type, since at least the first type in the list must satisfy this condition.\)

7. Convert all inputs to the selected type. Fail if there is not a conversion from a given input to the selected type.

Some examples follow.

**Example 10.9. Type Resolution with Underspecified Types in a Union**

```
SELECT text 'a' AS "text" UNION SELECT 'b';

 text
------
 a
 b
(2 rows)

```

Here, the unknown-type literal`'b'`will be resolved to type`text`.

  


**Example 10.10. Type Resolution in a Simple Union**

```
SELECT 1.2 AS "numeric" UNION SELECT 1;

 numeric
---------
       1
     1.2
(2 rows)

```

The literal`1.2`is of type`numeric`, and the`integer`value`1`can be cast implicitly to`numeric`, so that type is used.

  


**Example 10.11. Type Resolution in a Transposed Union**

```
SELECT 1 AS "real" UNION SELECT CAST('2.2' AS REAL);

 real
------
    1
  2.2
(2 rows)

```

Here, since type`real`cannot be implicitly cast to`integer`, but`integer`can be implicitly cast to`real`, the union result type is resolved as`real`.

  


  


---

[\[9\]](https://www.postgresql.org/docs/10/static/typeconv-union-case.html#idm46249849266800)Somewhat like the treatment of domain inputs for operators and functions, this behavior allows a domain type to be preserved through a`UNION`or similar construct, so long as the user is careful to ensure that all inputs are implicitly or explicitly of that exact type. Otherwise the domain's base type will be preferred.

  


---



[^1]:  [PostgreSQL: Documentation: 10: 10.5. UNION, CASE, and Related Constructs](https://www.postgresql.org/docs/10/static/typeconv-union-case.html)

