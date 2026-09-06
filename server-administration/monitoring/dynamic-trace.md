## 27.5. Dynamic Tracing [#](#DYNAMIC-TRACE)

[27.5.1. Compiling for Dynamic Tracing](dynamic-trace.md#COMPILING-FOR-TRACE)

[27.5.2. Built-in Probes](dynamic-trace.md#TRACE-POINTS)

[27.5.3. Using Probes](dynamic-trace.md#USING-TRACE-POINTS)

[27.5.4. Defining New Probes](dynamic-trace.md#DEFINING-TRACE-POINTS)

<a id="id-1.6.14.10.2"></a>

PostgreSQL provides facilities to support
dynamic tracing of the database server. This allows an external
utility to be called at specific points in the code and thereby trace
execution.

A number of probes or trace points are already inserted into the source
code. These probes are intended to be used by database developers and
administrators. By default the probes are not compiled into
PostgreSQL; the user needs to explicitly tell
the configure script to make the probes available.

Currently, the
[DTrace](https://en.wikipedia.org/wiki/DTrace)
utility is supported, which, at the time of this writing, is available
on Solaris, macOS, FreeBSD, NetBSD, and Oracle Linux. The
[SystemTap](https://sourceware.org/systemtap/) project
for Linux provides a DTrace equivalent and can also be used. Supporting other dynamic
tracing utilities is theoretically possible by changing the definitions for
the macros in `src/include/utils/probes.h`.

<a id="COMPILING-FOR-TRACE"></a>

### 27.5.1. Compiling for Dynamic Tracing [#](#COMPILING-FOR-TRACE)

By default, probes are not available, so you will need to
explicitly tell the configure script to make the probes available
in PostgreSQL. To include DTrace support
specify `--enable-dtrace` to configure. See [Section 17.3.3.6](../installation/install-make.md#CONFIGURE-OPTIONS-DEVEL) for further information.

<a id="TRACE-POINTS"></a>

### 27.5.2. Built-in Probes [#](#TRACE-POINTS)

A number of standard probes are provided in the source code,
as shown in [Table 27.49](dynamic-trace.md#DTRACE-PROBE-POINT-TABLE);
[Table 27.50](dynamic-trace.md#TYPEDEFS-TABLE)
shows the types used in the probes. More probes can certainly be
added to enhance PostgreSQL's observability.

<a id="DTRACE-PROBE-POINT-TABLE"></a>

**Table 27.49. Built-in DTrace Probes**

<table border="1" class="table" summary="Built-in DTrace Probes"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>Name</th><th>Parameters</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">transaction-start</code></td><td><code class="literal">(LocalTransactionId)</code></td><td>Probe that fires at the start of a new transaction.
      arg0 is the transaction ID.</td></tr><tr><td><code class="literal">transaction-commit</code></td><td><code class="literal">(LocalTransactionId)</code></td><td>Probe that fires when a transaction completes successfully.
      arg0 is the transaction ID.</td></tr><tr><td><code class="literal">transaction-abort</code></td><td><code class="literal">(LocalTransactionId)</code></td><td>Probe that fires when a transaction completes unsuccessfully.
      arg0 is the transaction ID.</td></tr><tr><td><code class="literal">query-start</code></td><td><code class="literal">(const char *)</code></td><td>Probe that fires when the processing of a query is started.
      arg0 is the query string.</td></tr><tr><td><code class="literal">query-done</code></td><td><code class="literal">(const char *)</code></td><td>Probe that fires when the processing of a query is complete.
      arg0 is the query string.</td></tr><tr><td><code class="literal">query-parse-start</code></td><td><code class="literal">(const char *)</code></td><td>Probe that fires when the parsing of a query is started.
      arg0 is the query string.</td></tr><tr><td><code class="literal">query-parse-done</code></td><td><code class="literal">(const char *)</code></td><td>Probe that fires when the parsing of a query is complete.
      arg0 is the query string.</td></tr><tr><td><code class="literal">query-rewrite-start</code></td><td><code class="literal">(const char *)</code></td><td>Probe that fires when the rewriting of a query is started.
      arg0 is the query string.</td></tr><tr><td><code class="literal">query-rewrite-done</code></td><td><code class="literal">(const char *)</code></td><td>Probe that fires when the rewriting of a query is complete.
      arg0 is the query string.</td></tr><tr><td><code class="literal">query-plan-start</code></td><td><code class="literal">()</code></td><td>Probe that fires when the planning of a query is started.</td></tr><tr><td><code class="literal">query-plan-done</code></td><td><code class="literal">()</code></td><td>Probe that fires when the planning of a query is complete.</td></tr><tr><td><code class="literal">query-execute-start</code></td><td><code class="literal">()</code></td><td>Probe that fires when the execution of a query is started.</td></tr><tr><td><code class="literal">query-execute-done</code></td><td><code class="literal">()</code></td><td>Probe that fires when the execution of a query is complete.</td></tr><tr><td><code class="literal">statement-status</code></td><td><code class="literal">(const char *)</code></td><td>Probe that fires anytime the server process updates its
      <code class="structname">pg_stat_activity</code>.<code class="structfield">status</code>.
      arg0 is the new status string.</td></tr><tr><td><code class="literal">checkpoint-start</code></td><td><code class="literal">(int)</code></td><td>Probe that fires when a checkpoint is started.
      arg0 holds the bitwise flags used to distinguish different checkpoint
      types, such as shutdown, immediate or force.</td></tr><tr><td><code class="literal">checkpoint-done</code></td><td><code class="literal">(int, int, int, int, int)</code></td><td>Probe that fires when a checkpoint is complete.
      (The probes listed next fire in sequence during checkpoint processing.)
      arg0 is the number of buffers written. arg1 is the total number of
      buffers. arg2, arg3 and arg4 contain the number of WAL files added,
      removed and recycled respectively.</td></tr><tr><td><code class="literal">clog-checkpoint-start</code></td><td><code class="literal">(bool)</code></td><td>Probe that fires when the CLOG portion of a checkpoint is started.
      arg0 is true for normal checkpoint, false for shutdown
      checkpoint.</td></tr><tr><td><code class="literal">clog-checkpoint-done</code></td><td><code class="literal">(bool)</code></td><td>Probe that fires when the CLOG portion of a checkpoint is
      complete. arg0 has the same meaning as for <code class="literal">clog-checkpoint-start</code>.</td></tr><tr><td><code class="literal">subtrans-checkpoint-start</code></td><td><code class="literal">(bool)</code></td><td>Probe that fires when the SUBTRANS portion of a checkpoint is
      started.
      arg0 is true for normal checkpoint, false for shutdown
      checkpoint.</td></tr><tr><td><code class="literal">subtrans-checkpoint-done</code></td><td><code class="literal">(bool)</code></td><td>Probe that fires when the SUBTRANS portion of a checkpoint is
      complete. arg0 has the same meaning as for
      <code class="literal">subtrans-checkpoint-start</code>.</td></tr><tr><td><code class="literal">multixact-checkpoint-start</code></td><td><code class="literal">(bool)</code></td><td>Probe that fires when the MultiXact portion of a checkpoint is
      started.
      arg0 is true for normal checkpoint, false for shutdown
      checkpoint.</td></tr><tr><td><code class="literal">multixact-checkpoint-done</code></td><td><code class="literal">(bool)</code></td><td>Probe that fires when the MultiXact portion of a checkpoint is
      complete. arg0 has the same meaning as for
      <code class="literal">multixact-checkpoint-start</code>.</td></tr><tr><td><code class="literal">buffer-checkpoint-start</code></td><td><code class="literal">(int)</code></td><td>Probe that fires when the buffer-writing portion of a checkpoint
      is started.
      arg0 holds the bitwise flags used to distinguish different checkpoint
      types, such as shutdown, immediate or force.</td></tr><tr><td><code class="literal">buffer-sync-start</code></td><td><code class="literal">(int, int)</code></td><td>Probe that fires when we begin to write dirty buffers during
      checkpoint (after identifying which buffers must be written).
      arg0 is the total number of buffers.
      arg1 is the number that are currently dirty and need to be written.</td></tr><tr><td><code class="literal">buffer-sync-written</code></td><td><code class="literal">(int)</code></td><td>Probe that fires after each buffer is written during checkpoint.
      arg0 is the ID number of the buffer.</td></tr><tr><td><code class="literal">buffer-sync-done</code></td><td><code class="literal">(int, int, int)</code></td><td>Probe that fires when all dirty buffers have been written.
      arg0 is the total number of buffers.
      arg1 is the number of buffers actually written by the checkpoint process.
      arg2 is the number that were expected to be written (arg1 of
      <code class="literal">buffer-sync-start</code>); any difference reflects other processes flushing
      buffers during the checkpoint.</td></tr><tr><td><code class="literal">buffer-checkpoint-sync-start</code></td><td><code class="literal">()</code></td><td>Probe that fires after dirty buffers have been written to the
      kernel, and before starting to issue fsync requests.</td></tr><tr><td><code class="literal">buffer-checkpoint-done</code></td><td><code class="literal">()</code></td><td>Probe that fires when syncing of buffers to disk is
      complete.</td></tr><tr><td><code class="literal">twophase-checkpoint-start</code></td><td><code class="literal">()</code></td><td>Probe that fires when the two-phase portion of a checkpoint is
      started.</td></tr><tr><td><code class="literal">twophase-checkpoint-done</code></td><td><code class="literal">()</code></td><td>Probe that fires when the two-phase portion of a checkpoint is
      complete.</td></tr><tr><td><code class="literal">buffer-extend-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, unsigned int)</code></td><td>Probe that fires when a relation extension starts.
       arg0 contains the fork to be extended. arg1, arg2, and arg3 contain the
       tablespace, database, and relation OIDs identifying the relation.  arg4
       is the ID of the backend which created the temporary relation for a
       local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared
       buffer. arg5 is the number of blocks the caller would like to extend
       by.</td></tr><tr><td><code class="literal">buffer-extend-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, unsigned int, BlockNumber)</code></td><td>Probe that fires when a relation extension is complete.
       arg0 contains the fork to be extended. arg1, arg2, and arg3 contain the
       tablespace, database, and relation OIDs identifying the relation.  arg4
       is the ID of the backend which created the temporary relation for a
       local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared
       buffer. arg5 is the number of blocks the relation was extended by, this
       can be less than the number in the
       <code class="literal">buffer-extend-start</code> due to resource
       constraints. arg6 contains the BlockNumber of the first new
       block.</td></tr><tr><td><code class="literal">buffer-read-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int)</code></td><td>Probe that fires when a buffer read is started.
      arg0 and arg1 contain the fork and block numbers of the page.
      arg2, arg3, and arg4 contain the tablespace, database, and relation OIDs
      identifying the relation.
      arg5 is the ID of the backend which created the temporary relation for a
      local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared buffer.
      </td></tr><tr><td><code class="literal">buffer-read-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, bool)</code></td><td>Probe that fires when a buffer read is complete.
      arg0 and arg1 contain the fork and block numbers of the page.
      arg2, arg3, and arg4 contain the tablespace, database, and relation OIDs
      identifying the relation.
      arg5 is the ID of the backend which created the temporary relation for a
      local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared buffer.
      arg6 is true if the buffer was found in the pool, false if not.</td></tr><tr><td><code class="literal">buffer-flush-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid)</code></td><td>Probe that fires before issuing any write request for a shared
      buffer.
      arg0 and arg1 contain the fork and block numbers of the page.
      arg2, arg3, and arg4 contain the tablespace, database, and relation OIDs
      identifying the relation.</td></tr><tr><td><code class="literal">buffer-flush-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid)</code></td><td>Probe that fires when a write request is complete.  (Note
      that this just reflects the time to pass the data to the kernel;
      it's typically not actually been written to disk yet.)
      The arguments are the same as for <code class="literal">buffer-flush-start</code>.</td></tr><tr><td><code class="literal">wal-buffer-write-dirty-start</code></td><td><code class="literal">()</code></td><td>Probe that fires when a server process begins to write a
      dirty WAL buffer because no more WAL buffer space is available.
      (If this happens often, it implies that
      <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-WAL-BUFFERS">wal_buffers</a> is too small.)</td></tr><tr><td><code class="literal">wal-buffer-write-dirty-done</code></td><td><code class="literal">()</code></td><td>Probe that fires when a dirty WAL buffer write is complete.</td></tr><tr><td><code class="literal">wal-insert</code></td><td><code class="literal">(unsigned char, unsigned char)</code></td><td>Probe that fires when a WAL record is inserted.
      arg0 is the resource manager (rmid) for the record.
      arg1 contains the info flags.</td></tr><tr><td><code class="literal">wal-switch</code></td><td><code class="literal">()</code></td><td>Probe that fires when a WAL segment switch is requested.</td></tr><tr><td><code class="literal">smgr-md-read-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int)</code></td><td>Probe that fires when beginning to read a block from a relation.
      arg0 and arg1 contain the fork and block numbers of the page.
      arg2, arg3, and arg4 contain the tablespace, database, and relation OIDs
      identifying the relation.
      arg5 is the ID of the backend which created the temporary relation for a
      local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared buffer.</td></tr><tr><td><code class="literal">smgr-md-read-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, int, int)</code></td><td>Probe that fires when a block read is complete.
      arg0 and arg1 contain the fork and block numbers of the page.
      arg2, arg3, and arg4 contain the tablespace, database, and relation OIDs
      identifying the relation.
      arg5 is the ID of the backend which created the temporary relation for a
      local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared buffer.
      arg6 is the number of bytes actually read, while arg7 is the number
      requested (if these are different it indicates a short read).</td></tr><tr><td><code class="literal">smgr-md-write-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int)</code></td><td>Probe that fires when beginning to write a block to a relation.
      arg0 and arg1 contain the fork and block numbers of the page.
      arg2, arg3, and arg4 contain the tablespace, database, and relation OIDs
      identifying the relation.
      arg5 is the ID of the backend which created the temporary relation for a
      local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared buffer.</td></tr><tr><td><code class="literal">smgr-md-write-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, int, int)</code></td><td>Probe that fires when a block write is complete.
      arg0 and arg1 contain the fork and block numbers of the page.
      arg2, arg3, and arg4 contain the tablespace, database, and relation OIDs
      identifying the relation.
      arg5 is the ID of the backend which created the temporary relation for a
      local buffer, or <code class="symbol">INVALID_PROC_NUMBER</code> (-1) for a shared buffer.
      arg6 is the number of bytes actually written, while arg7 is the number
      requested (if these are different it indicates a short write).</td></tr><tr><td><code class="literal">sort-start</code></td><td><code class="literal">(int, bool, int, int, bool, int)</code></td><td>Probe that fires when a sort operation is started.
      arg0 indicates heap, index or datum sort.
      arg1 is true for unique-value enforcement.
      arg2 is the number of key columns.
      arg3 is the number of kilobytes of work memory allowed.
      arg4 is true if random access to the sort result is required.
      arg5 indicates serial when <code class="literal">0</code>, parallel worker when
      <code class="literal">1</code>, or parallel leader when <code class="literal">2</code>.</td></tr><tr><td><code class="literal">sort-done</code></td><td><code class="literal">(bool, long)</code></td><td>Probe that fires when a sort is complete.
      arg0 is true for external sort, false for internal sort.
      arg1 is the number of disk blocks used for an external sort,
      or kilobytes of memory used for an internal sort.</td></tr><tr><td><code class="literal">lwlock-acquire</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>Probe that fires when an LWLock has been acquired.
      arg0 is the LWLock's tranche.
      arg1 is the requested lock mode, either exclusive or shared.</td></tr><tr><td><code class="literal">lwlock-release</code></td><td><code class="literal">(char *)</code></td><td>Probe that fires when an LWLock has been released (but note
      that any released waiters have not yet been awakened).
      arg0 is the LWLock's tranche.</td></tr><tr><td><code class="literal">lwlock-wait-start</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>Probe that fires when an LWLock was not immediately available and
      a server process has begun to wait for the lock to become available.
      arg0 is the LWLock's tranche.
      arg1 is the requested lock mode, either exclusive or shared.</td></tr><tr><td><code class="literal">lwlock-wait-done</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>Probe that fires when a server process has been released from its
      wait for an LWLock (it does not actually have the lock yet).
      arg0 is the LWLock's tranche.
      arg1 is the requested lock mode, either exclusive or shared.</td></tr><tr><td><code class="literal">lwlock-condacquire</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>Probe that fires when an LWLock was successfully acquired when the
      caller specified no waiting.
      arg0 is the LWLock's tranche.
      arg1 is the requested lock mode, either exclusive or shared.</td></tr><tr><td><code class="literal">lwlock-condacquire-fail</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>Probe that fires when an LWLock was not successfully acquired when
      the caller specified no waiting.
      arg0 is the LWLock's tranche.
      arg1 is the requested lock mode, either exclusive or shared.</td></tr><tr><td><code class="literal">lock-wait-start</code></td><td><code class="literal">(unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, LOCKMODE)</code></td><td>Probe that fires when a request for a heavyweight lock (lmgr lock)
      has begun to wait because the lock is not available.
      arg0 through arg3 are the tag fields identifying the object being
      locked.  arg4 indicates the type of object being locked.
      arg5 indicates the lock type being requested.</td></tr><tr><td><code class="literal">lock-wait-done</code></td><td><code class="literal">(unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, LOCKMODE)</code></td><td>Probe that fires when a request for a heavyweight lock (lmgr lock)
      has finished waiting (i.e., has acquired the lock).
      The arguments are the same as for <code class="literal">lock-wait-start</code>.</td></tr><tr><td><code class="literal">deadlock-found</code></td><td><code class="literal">()</code></td><td>Probe that fires when a deadlock is found by the deadlock
      detector.</td></tr></tbody></table>

<br><a id="TYPEDEFS-TABLE"></a>

**Table 27.50. Defined Types Used in Probe Parameters**

<table border="1" class="table" summary="Defined Types Used in Probe Parameters"><colgroup><col/><col/></colgroup><thead><tr><th>Type</th><th>Definition</th></tr></thead><tbody><tr><td><code class="type">LocalTransactionId</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">LWLockMode</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">LOCKMODE</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">BlockNumber</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">Oid</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">ForkNumber</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">bool</code></td><td><code class="type">unsigned char</code></td></tr></tbody></table>

<br>

<a id="USING-TRACE-POINTS"></a>

### 27.5.3. Using Probes [#](#USING-TRACE-POINTS)

The example below shows a DTrace script for analyzing transaction
counts in the system, as an alternative to snapshotting
`pg_stat_database` before and after a performance test:

```

#!/usr/sbin/dtrace -qs

postgresql$1:::transaction-start
{
      @start["Start"] = count();
      self->ts  = timestamp;
}

postgresql$1:::transaction-abort
{
      @abort["Abort"] = count();
}

postgresql$1:::transaction-commit
/self->ts/
{
      @commit["Commit"] = count();
      @time["Total time (ns)"] = sum(timestamp - self->ts);
      self->ts=0;
}
```

When executed, the example D script gives output such as:

```

# ./txn_count.d `pgrep -n postgres` or ./txn_count.d <PID>
^C

Start                                          71
Commit                                         70
Total time (ns)                        2312105013
```

### Note

SystemTap uses a different notation for trace scripts than DTrace does,
even though the underlying trace points are compatible. One point worth
noting is that at this writing, SystemTap scripts must reference probe
names using double underscores in place of hyphens. This is expected to
be fixed in future SystemTap releases.

You should remember that DTrace scripts need to be carefully written and
debugged, otherwise the trace information collected might
be meaningless. In most cases where problems are found it is the
instrumentation that is at fault, not the underlying system. When
discussing information found using dynamic tracing, be sure to enclose
the script used to allow that too to be checked and discussed.

<a id="DEFINING-TRACE-POINTS"></a>

### 27.5.4. Defining New Probes [#](#DEFINING-TRACE-POINTS)

New probes can be defined within the code wherever the developer
desires, though this will require a recompilation. Below are the steps
for inserting new probes:

1. Decide on probe names and data to be made available through the probes
2. Add the probe definitions to `src/backend/utils/probes.d`
3. Include `pg_trace.h` if it is not already present in the
   module(s) containing the probe points, and insert
   `TRACE_POSTGRESQL` probe macros at the desired locations
   in the source code
4. Recompile and verify that the new probes are available

**Example:**
Here is an example of how you would add a probe to trace all new
transactions by transaction ID.

1. Decide that the probe will be named `transaction-start` and
   requires a parameter of type `LocalTransactionId`
2. Add the probe definition to `src/backend/utils/probes.d`:

   ```

   probe transaction__start(LocalTransactionId);
   ```

   Note the use of the double underline in the probe name. In a DTrace
   script using the probe, the double underline needs to be replaced with a
   hyphen, so `transaction-start` is the name to document for
   users.
3. At compile time, `transaction__start` is converted to a macro
   called `TRACE_POSTGRESQL_TRANSACTION_START` (notice the
   underscores are single here), which is available by including
   `pg_trace.h`. Add the macro call to the appropriate location
   in the source code. In this case, it looks like the following:

   ```

   TRACE_POSTGRESQL_TRANSACTION_START(vxid.localTransactionId);
   ```
4. After recompiling and running the new binary, check that your newly added
   probe is available by executing the following DTrace command. You
   should see similar output:

   ```

   # dtrace -ln transaction-start
      ID    PROVIDER          MODULE           FUNCTION NAME
   18705 postgresql49878     postgres     StartTransactionCommand transaction-start
   18755 postgresql49877     postgres     StartTransactionCommand transaction-start
   18805 postgresql49876     postgres     StartTransactionCommand transaction-start
   18855 postgresql49875     postgres     StartTransactionCommand transaction-start
   18986 postgresql49873     postgres     StartTransactionCommand transaction-start
   ```

There are a few things to be careful about when adding trace macros
to the C code:

* You should take care that the data types specified for a probe's
  parameters match the data types of the variables used in the macro.
  Otherwise, you will get compilation errors.
* On most platforms, if PostgreSQL is
  built with `--enable-dtrace`, the arguments to a trace
  macro will be evaluated whenever control passes through the
  macro, *even if no tracing is being done*. This is
  usually not worth worrying about if you are just reporting the
  values of a few local variables. But beware of putting expensive
  function calls into the arguments. If you need to do that,
  consider protecting the macro with a check to see if the trace
  is actually enabled:

  ```

  if (TRACE_POSTGRESQL_TRANSACTION_START_ENABLED())
      TRACE_POSTGRESQL_TRANSACTION_START(some_function(...));
  ```

  Each trace macro has a corresponding `ENABLED` macro.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dynamic-trace.html)（英文原文，待翻譯）
