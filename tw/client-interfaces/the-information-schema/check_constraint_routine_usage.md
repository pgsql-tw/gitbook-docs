# 36.8. check\_constraint\_routine\_usage

The view `check_constraint_routine_usage` identifies routines \(functions and procedures\) that are used by a check constraint. Only those routines are shown that are owned by a currently enabled role.

**Table 36.6. `check_constraint_routine_usage` Columns**

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
        <p><code>constraint_catalog</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the database containing the constraint (always the current database)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>constraint_schema</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the schema containing the constraint</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>constraint_name</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the constraint</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>specific_catalog</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the database containing the function (always the current database)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>specific_schema</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the schema containing the function</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>specific_name</code>  <code>sql_identifier</code>
        </p>
        <p>The &#x201C;specific name&#x201D; of the function. See <a href="https://www.postgresql.org/docs/13/infoschema-routines.html">Section 36.41</a> for
          more information.</p>
      </td>
    </tr>
  </tbody>
</table>

