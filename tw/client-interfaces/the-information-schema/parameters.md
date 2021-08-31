# 36.33. parameters

The view `parameters` contains information about the parameters \(arguments\) of all functions in the current database. Only those functions are shown that the current user has access to \(by way of being the owner or having some privilege\).

#### **Table 36.31. `parameters` Columns**

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
    <tr>
      <td style="text-align:left">
        <p><code>ordinal_position</code>  <code>cardinal_number</code>
        </p>
        <p>Ordinal position of the parameter in the argument list of the function
          (count starts at 1)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>parameter_mode</code>  <code>character_data</code>
        </p>
        <p><code>IN</code> for input parameter, <code>OUT</code> for output parameter,
          and <code>INOUT</code> for input/output parameter.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>is_result</code>  <code>yes_or_no</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>as_locator</code>  <code>yes_or_no</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>parameter_name</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the parameter, or null if the parameter has no name</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>data_type</code>  <code>character_data</code>
        </p>
        <p>Data type of the parameter, if it is a built-in type, or <code>ARRAY</code> if
          it is some array (in that case, see the view <code>element_types</code>),
          else <code>USER-DEFINED</code> (in that case, the type is identified in <code>udt_name</code> and
          associated columns).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>character_maximum_length</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>character_octet_length</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>character_set_catalog</code>  <code>sql_identifier</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>character_set_schema</code>  <code>sql_identifier</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>character_set_name</code>  <code>sql_identifier</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>collation_catalog</code>  <code>sql_identifier</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>collation_schema</code>  <code>sql_identifier</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>collation_name</code>  <code>sql_identifier</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>numeric_precision</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>numeric_precision_radix</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>numeric_scale</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>datetime_precision</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>interval_type</code>  <code>character_data</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>interval_precision</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, since this information is not applied to parameter data types
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>udt_catalog</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the database that the data type of the parameter is defined in
          (always the current database)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>udt_schema</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the schema that the data type of the parameter is defined in</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>udt_name</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the data type of the parameter</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>scope_catalog</code>  <code>sql_identifier</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>scope_schema</code>  <code>sql_identifier</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>scope_name</code>  <code>sql_identifier</code>
        </p>
        <p>Applies to a feature not available in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>maximum_cardinality</code>  <code>cardinal_number</code>
        </p>
        <p>Always null, because arrays always have unlimited maximum cardinality
          in PostgreSQL</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>dtd_identifier</code>  <code>sql_identifier</code>
        </p>
        <p>An identifier of the data type descriptor of the parameter, unique among
          the data type descriptors pertaining to the function. This is mainly useful
          for joining with other instances of such identifiers. (The specific format
          of the identifier is not defined and not guaranteed to remain the same
          in future versions.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>parameter_default</code>  <code>character_data</code>
        </p>
        <p>The default expression of the parameter, or null if none or if the function
          is not owned by a currently enabled role.</p>
      </td>
    </tr>
  </tbody>
</table>

