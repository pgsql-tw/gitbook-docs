# 51.21. pg\_event\_trigger

The catalog `pg_event_trigger` stores event triggers. See [Chapter 39](https://www.postgresql.org/docs/13/event-triggers.html) for more information.

#### **Table 51.21. `pg_event_trigger` Columns**

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
        <p><code>evtname</code>  <code>name</code>
        </p>
        <p>Trigger name (must be unique)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>evtevent</code>  <code>name</code>
        </p>
        <p>Identifies the event for which this trigger fires</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>evtowner</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>oid</code>)</p>
        <p>Owner of the event trigger</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>evtfoid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-proc.html"><code>pg_proc</code></a>.<code>oid</code>)</p>
        <p>The function to be called</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>evtenabled</code>  <code>char</code>
        </p>
        <p>Controls in which <a href="https://www.postgresql.org/docs/13/runtime-config-client.html#GUC-SESSION-REPLICATION-ROLE">session_replication_role</a> modes
          the event trigger fires. <code>O</code> = trigger fires in &#x201C;origin&#x201D;
          and &#x201C;local&#x201D; modes, <code>D</code> = trigger is disabled, <code>R</code> =
          trigger fires in &#x201C;replica&#x201D; mode, <code>A</code> = trigger fires
          always.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>evttags</code>  <code>text[]</code>
        </p>
        <p>Command tags for which this trigger will fire. If NULL, the firing of
          this trigger is not restricted on the basis of the command tag.</p>
      </td>
    </tr>
  </tbody>
</table>

