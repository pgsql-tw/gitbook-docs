# 36.4. administrable\_role\_authorizations

The view `administrable_role_authorizations` identifies all roles that the current user has the admin option for.

#### **Table 36.2. `administrable_role_authorizations` Columns**

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
        <p><code>grantee</code>  <code>sql_identifier</code>
        </p>
        <p>Name of the role to which this role membership was granted (can be the
          current user, or a different role in case of nested role memberships)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>role_name</code>  <code>sql_identifier</code>
        </p>
        <p>Name of a role</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>is_grantable</code>  <code>yes_or_no</code>
        </p>
        <p>Always <code>YES</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

