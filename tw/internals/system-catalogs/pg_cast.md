# 51.10. pg\_cast

系統目錄 pg\_cast 儲存資料型別的轉換方式，包括了內建的和使用者定義的。

需要注意的是，pg\_cast 並不代表系統知道如何執行的每一種型別轉換；只有那些不能從某些通用規則中推導出來的。例如，domain 和它的基本型別之間的轉換在 pg\_cast 中就沒有明確表示。另一個重要的例外是「自動 I/O 強制轉換」，即使用資料型別自己的 I/O 函數執行的轉換為 text 或其他字串型別或從 text 及其他字串型別轉換的那些，在 pg\_cast 中沒有明確表示。

#### **Table 51.10. `pg_cast` Columns**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>oid</code>  <code>oid</code>
        </p>
        <p>Row identifier</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>castsource</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-type.html"><code>pg_type</code></a>.<code>oid</code>)</p>
        <p>OID of the source data type</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>casttarget</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-type.html"><code>pg_type</code></a>.<code>oid</code>)</p>
        <p>OID of the target data type</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>castfunc</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-proc.html"><code>pg_proc</code></a>.<code>oid</code>)</p>
        <p>The OID of the function to use to perform this cast. Zero is stored if
          the cast method doesn&apos;t require a function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>castcontext</code>  <code>char</code>
        </p>
        <p>Indicates what contexts the cast can be invoked in. <code>e</code> means
          only as an explicit cast (using <code>CAST</code> or <code>::</code> syntax). <code>a</code> means
          implicitly in assignment to a target column, as well as explicitly. <code>i</code> means
          implicitly in expressions, as well as the other cases.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>castmethod</code>  <code>char</code>
        </p>
        <p>Indicates how the cast is performed. <code>f</code> means that the function
          specified in the <code>castfunc</code> field is used. <code>i</code> means
          that the input/output functions are used. <code>b</code> means that the types
          are binary-coercible, thus no conversion is required.</p>
      </td>
    </tr>
  </tbody>
</table>

The cast functions listed in `pg_cast` must always take the cast source type as their first argument type, and return the cast destination type as their result type. A cast function can have up to three arguments. The second argument, if present, must be type `integer`; it receives the type modifier associated with the destination type, or -1 if there is none. The third argument, if present, must be type `boolean`; it receives `true` if the cast is an explicit cast, `false` otherwise.

It is legitimate to create a `pg_cast` entry in which the source and target types are the same, if the associated function takes more than one argument. Such entries represent “length coercion functions” that coerce values of the type to be legal for a particular type modifier value.

When a `pg_cast` entry has different source and target types and a function that takes more than one argument, it represents converting from one type to another and applying a length coercion in a single step. When no such entry is available, coercion to a type that uses a type modifier involves two steps, one to convert between data types and a second to apply the modifier.

