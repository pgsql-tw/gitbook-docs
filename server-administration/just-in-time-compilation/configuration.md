# 32.3. Configuration

The configuration variable [jit](../server-configuration/query-planning.md#GUC-JIT) determines whether JIT compilation is enabled or disabled. If it is enabled, the configuration variables [jit\_above\_cost](../server-configuration/query-planning.md#GUC-JIT-ABOVE-COST), [jit\_inline\_above\_cost](../server-configuration/query-planning.md#GUC-JIT-INLINE-ABOVE-COST), and [jit\_optimize\_above\_cost](../server-configuration/query-planning.md#GUC-JIT-OPTIMIZE-ABOVE-COST) determine whether JIT compilation is performed for a query, and how much effort is spent doing so.

[jit\_provider](../server-configuration/client-connection-defaults.md#GUC-JIT-PROVIDER) determines which JIT implementation is used. It is rarely required to be changed. See [Section 32.4.2](extensibility.md#JIT-PLUGGABLE).

For development and debugging purposes a few additional configuration parameters exist, as described in [Section 20.17](../server-configuration/developer-options.md).
