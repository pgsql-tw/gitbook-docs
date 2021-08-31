# 36.9. check\_constraints

The view `check_constraints` contains all check constraints, either defined on a table or on a domain, that are owned by a currently enabled role. \(The owner of the table or domain is the owner of the constraint.\)

#### **Table 36.7. `check_constraints` Columns**

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
        <p><code>check_clause</code>  <code>character_data</code>
        </p>
        <p>The check expression of the check constraint</p>
      </td>
    </tr>
  </tbody>
</table>

