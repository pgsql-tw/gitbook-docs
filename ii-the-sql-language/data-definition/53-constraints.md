# 5.3. 限制條件[^1]

Data types are a way to limit the kind of data that can be stored in a table. For many applications, however, the constraint they provide is too coarse. For example, a column containing a product price should probably only accept positive values. But there is no standard data type that accepts only positive numbers. Another issue is that you might want to constrain column data with respect to other columns or rows. For example, in a table containing product information, there should be only one row for each product number.

To that end, SQL allows you to define constraints on columns and tables. Constraints give you as much control over the data in your tables as you wish. If a user attempts to store data in a column that would violate a constraint, an error is raised. This applies even if the value came from the default value definition.

### 5.3.1. Check Constraints





A check constraint is the most generic constraint type. It allows you to specify that the value in a certain column must satisfy a Boolean \(truth-value\) expression. For instance, to require positive product prices, you could use:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric 
CHECK (price 
>
 0)

);

```

As you see, the constraint definition comes after the data type, just like default value definitions. Default values and constraints can be listed in any order. A check constraint consists of the key word`CHECK`followed by an expression in parentheses. The check constraint expression should involve the column thus constrained, otherwise the constraint would not make too much sense.



You can also give the constraint a separate name. This clarifies error messages and allows you to refer to the constraint when you need to change it. The syntax is:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric 
CONSTRAINT positive_price
 CHECK (price 
>
 0)
);

```

So, to specify a named constraint, use the key word`CONSTRAINT`followed by an identifier followed by the constraint definition. \(If you don't specify a constraint name in this way, the system chooses a name for you.\)

A check constraint can also refer to several columns. Say you store a regular price and a discounted price, and you want to ensure that the discounted price is lower than the regular price:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price 
>
 0),
    discounted_price numeric CHECK (discounted_price 
>
 0),
    
CHECK (price 
>
 discounted_price)

);

```

The first two constraints should look familiar. The third one uses a new syntax. It is not attached to a particular column, instead it appears as a separate item in the comma-separated column list. Column definitions and these constraint definitions can be listed in mixed order.

We say that the first two constraints are column constraints, whereas the third one is a table constraint because it is written separately from any one column definition. Column constraints can also be written as table constraints, while the reverse is not necessarily possible, since a column constraint is supposed to refer to only the column it is attached to. \(PostgreSQLdoesn't enforce that rule, but you should follow it if you want your table definitions to work with other database systems.\) The above example could also be written as:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price 
>
 0),
    discounted_price numeric,
    CHECK (discounted_price 
>
 0),
    CHECK (price 
>
 discounted_price)
);

```

or even:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price 
>
 0),
    discounted_price numeric,
    CHECK (discounted_price 
>
 0 AND price 
>
 discounted_price)
);

```

It's a matter of taste.

Names can be assigned to table constraints in the same way as column constraints:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price 
>
 0),
    discounted_price numeric,
    CHECK (discounted_price 
>
 0),
    
CONSTRAINT valid_discount
 CHECK (price 
>
 discounted_price)
);

```



It should be noted that a check constraint is satisfied if the check expression evaluates to true or the null value. Since most expressions will evaluate to the null value if any operand is null, they will not prevent null values in the constrained columns. To ensure that a column does not contain null values, the not-null constraint described in the next section can be used.

### 5.3.2. Not-Null Constraints





A not-null constraint simply specifies that a column must not assume the null value. A syntax example:

```
CREATE TABLE products (
    product_no integer 
NOT NULL
,
    name text 
NOT NULL
,
    price numeric
);

```

A not-null constraint is always written as a column constraint. A not-null constraint is functionally equivalent to creating a check constraint`CHECK (`_`column_name`_IS NOT NULL\), but inPostgreSQLcreating an explicit not-null constraint is more efficient. The drawback is that you cannot give explicit names to not-null constraints created this way.

Of course, a column can have more than one constraint. Just write the constraints one after another:

```
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric NOT NULL CHECK (price 
>
 0)
);

```

The order doesn't matter. It does not necessarily determine in which order the constraints are checked.

The`NOT NULL`constraint has an inverse: the`NULL`constraint. This does not mean that the column must be null, which would surely be useless. Instead, this simply selects the default behavior that the column might be null. The`NULL`constraint is not present in the SQL standard and should not be used in portable applications. \(It was only added toPostgreSQLto be compatible with some other database systems.\) Some users, however, like it because it makes it easy to toggle the constraint in a script file. For example, you could start with:

```
CREATE TABLE products (
    product_no integer NULL,
    name text NULL,
    price numeric NULL
);

```

and then insert the`NOT`key word where desired.

### Tip

In most database designs the majority of columns should be marked not null.

### 5.3.3. Unique Constraints





Unique constraints ensure that the data contained in a column, or a group of columns, is unique among all the rows in the table. The syntax is:

```
CREATE TABLE products (
    product_no integer 
UNIQUE
,
    name text,
    price numeric
);

```

when written as a column constraint, and:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    
UNIQUE (product_no)

);

```

when written as a table constraint.

To define a unique constraint for a group of columns, write it as a table constraint with the column names separated by commas:

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    
UNIQUE (a, c)

);

```

This specifies that the combination of values in the indicated columns is unique across the whole table, though any one of the columns need not be \(and ordinarily isn't\) unique.

You can assign your own name for a unique constraint, in the usual way:

```
CREATE TABLE products (
    product_no integer 
CONSTRAINT must_be_different
 UNIQUE,
    name text,
    price numeric
);

```

Adding a unique constraint will automatically create a unique B-tree index on the column or group of columns listed in the constraint. A uniqueness restriction covering only some rows cannot be written as a unique constraint, but it is possible to enforce such a restriction by creating a unique[partial index](https://www.postgresql.org/docs/10/static/indexes-partial.html).



In general, a unique constraint is violated if there is more than one row in the table where the values of all of the columns included in the constraint are equal. However, two null values are never considered equal in this comparison. That means even in the presence of a unique constraint it is possible to store duplicate rows that contain a null value in at least one of the constrained columns. This behavior conforms to the SQL standard, but we have heard that other SQL databases might not follow this rule. So be careful when developing applications that are intended to be portable.

### 5.3.4. Primary Keys





A primary key constraint indicates that a column, or group of columns, can be used as a unique identifier for rows in the table. This requires that the values be both unique and not null. So, the following two table definitions accept the same data:

```
CREATE TABLE products (
    product_no integer UNIQUE NOT NULL,
    name text,
    price numeric
);

```

```
CREATE TABLE products (
    product_no integer 
PRIMARY KEY
,
    name text,
    price numeric
);

```

Primary keys can span more than one column; the syntax is similar to unique constraints:

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    
PRIMARY KEY (a, c)

);

```

Adding a primary key will automatically create a unique B-tree index on the column or group of columns listed in the primary key, and will force the column\(s\) to be marked`NOT NULL`.

A table can have at most one primary key. \(There can be any number of unique and not-null constraints, which are functionally almost the same thing, but only one can be identified as the primary key.\) Relational database theory dictates that every table must have a primary key. This rule is not enforced byPostgreSQL, but it is usually best to follow it.

Primary keys are useful both for documentation purposes and for client applications. For example, a GUI application that allows modifying row values probably needs to know the primary key of a table to be able to identify rows uniquely. There are also various ways in which the database system makes use of a primary key if one has been declared; for example, the primary key defines the default target column\(s\) for foreign keys referencing its table.

### 5.3.5. Foreign Keys







A foreign key constraint specifies that the values in a column \(or a group of columns\) must match the values appearing in some row of another table. We say this maintains the_referential integrity_between two related tables.

Say you have the product table that we have used several times already:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

```

Let's also assume you have a table storing orders of those products. We want to ensure that the orders table only contains orders of products that actually exist. So we define a foreign key constraint in the orders table that references the products table:

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer 
REFERENCES products (product_no)
,
    quantity integer
);

```

Now it is impossible to create orders with non-NULL`product_no`entries that do not appear in the products table.

We say that in this situation the orders table is the_referencing_table and the products table is the_referenced_table. Similarly, there are referencing and referenced columns.

You can also shorten the above command to:

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer 
REFERENCES products
,
    quantity integer
);

```

because in absence of a column list the primary key of the referenced table is used as the referenced column\(s\).

A foreign key can also constrain and reference a group of columns. As usual, it then needs to be written in table constraint form. Here is a contrived syntax example:

```
CREATE TABLE t1 (
  a integer PRIMARY KEY,
  b integer,
  c integer,
  
FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)

);

```

Of course, the number and type of the constrained columns need to match the number and type of the referenced columns.

You can assign your own name for a foreign key constraint, in the usual way.

A table can have more than one foreign key constraint. This is used to implement many-to-many relationships between tables. Say you have tables about products and orders, but now you want to allow one order to contain possibly many products \(which the structure above did not allow\). You could use this table structure:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products,
    order_id integer REFERENCES orders,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);

```

Notice that the primary key overlaps with the foreign keys in the last table.





We know that the foreign keys disallow creation of orders that do not relate to any products. But what if a product is removed after an order is created that references it? SQL allows you to handle that as well. Intuitively, we have a few options:

* Disallow deleting a referenced product

* Delete the orders as well

* Something else?

To illustrate this, let's implement the following policy on the many-to-many relationship example above: when someone wants to remove a product that is still referenced by an order \(via`order_items`\), we disallow it. If someone removes an order, the order items are removed as well:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products 
ON DELETE RESTRICT
,
    order_id integer REFERENCES orders 
ON DELETE CASCADE
,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);

```

Restricting and cascading deletes are the two most common options.`RESTRICT`prevents deletion of a referenced row.`NO ACTION`means that if any referencing rows still exist when the constraint is checked, an error is raised; this is the default behavior if you do not specify anything. \(The essential difference between these two choices is that`NO ACTION`allows the check to be deferred until later in the transaction, whereas`RESTRICT`does not.\)`CASCADE`specifies that when a referenced row is deleted, row\(s\) referencing it should be automatically deleted as well. There are two other options:`SET NULL`and`SET DEFAULT`. These cause the referencing column\(s\) in the referencing row\(s\) to be set to nulls or their default values, respectively, when the referenced row is deleted. Note that these do not excuse you from observing any constraints. For example, if an action specifies`SET DEFAULT`but the default value would not satisfy the foreign key constraint, the operation will fail.

Analogous to`ON DELETE`there is also`ON UPDATE`which is invoked when a referenced column is changed \(updated\). The possible actions are the same. In this case,`CASCADE`means that the updated values of the referenced column\(s\) should be copied into the referencing row\(s\).

Normally, a referencing row need not satisfy the foreign key constraint if any of its referencing columns are null. If`MATCH FULL`is added to the foreign key declaration, a referencing row escapes satisfying the constraint only if all its referencing columns are null \(so a mix of null and non-null values is guaranteed to fail a`MATCH FULL`constraint\). If you don't want referencing rows to be able to avoid satisfying the foreign key constraint, declare the referencing column\(s\) as`NOT NULL`.

A foreign key must reference columns that either are a primary key or form a unique constraint. This means that the referenced columns always have an index \(the one underlying the primary key or unique constraint\); so checks on whether a referencing row has a match will be efficient. Since a`DELETE`of a row from the referenced table or an`UPDATE`of a referenced column will require a scan of the referencing table for rows matching the old value, it is often a good idea to index the referencing columns too. Because this is not always needed, and there are many choices available on how to index, declaration of a foreign key constraint does not automatically create an index on the referencing columns.

More information about updating and deleting data is in[Chapter 6](https://www.postgresql.org/docs/10/static/dml.html). Also see the description of foreign key constraint syntax in the reference documentation for[CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html).

### 5.3.6. Exclusion Constraints





Exclusion constraints ensure that if any two rows are compared on the specified columns or expressions using the specified operators, at least one of these operator comparisons will return false or null. The syntax is:

```
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);

```

See also[`CREATE TABLE ... CONSTRAINT ... EXCLUDE`](https://www.postgresql.org/docs/10/static/sql-createtable.html#sql-createtable-exclude)for details.

Adding an exclusion constraint will automatically create an index of the type specified in the constraint declaration.

---

[^1]: [PostgreSQL: Documentation: 10: 5.3. Constraints](https://www.postgresql.org/docs/10/static/ddl-constraints.html)

