# 31.1. What is JIT compilation?

Just-in-Time (JIT) compilation is the process of turning some form of interpreted program evaluation into a native program, and doing so at run time. For example, instead of using general-purpose code that can evaluate arbitrary SQL expressions to evaluate a particular SQL predicate like `WHERE a.col = 3`, it is possible to generate a function that is specific to that expression and can be natively executed by the CPU, yielding a speedup.

PostgreSQL has builtin support to perform JIT compilation using [LLVM](https://llvm.org) when PostgreSQL is built with [`--with-llvm`](https://www.postgresql.org/docs/13/install-procedure.html#CONFIGURE-WITH-LLVM).

See `src/backend/jit/README` for further details.

## 31.1.1. JIT Accelerated Operations

Currently PostgreSQL's JIT implementation has support for accelerating expression evaluation and tuple deforming. Several other operations could be accelerated in the future.

Expression evaluation is used to evaluate `WHERE` clauses, target lists, aggregates and projections. It can be accelerated by generating code specific to each case.

Tuple deforming is the process of transforming an on-disk tuple (see [Section 68.6.1](https://www.postgresql.org/docs/13/storage-page-layout.html#STORAGE-TUPLE-LAYOUT)) into its in-memory representation. It can be accelerated by creating a function specific to the table layout and the number of columns to be extracted.

## 31.1.2. Inlining

PostgreSQL is very extensible and allows new data types, functions, operators and other database objects to be defined; see [Chapter 37](https://www.postgresql.org/docs/13/extend.html). In fact the built-in objects are implemented using nearly the same mechanisms. This extensibility implies some overhead, for example due to function calls (see [Section 37.3](https://www.postgresql.org/docs/13/xfunc.html)). To reduce that overhead, JIT compilation can inline the bodies of small functions into the expressions using them. That allows a significant percentage of the overhead to be optimized away.

## 31.1.3. Optimization

LLVM has support for optimizing generated code. Some of the optimizations are cheap enough to be performed whenever JIT is used, while others are only beneficial for longer-running queries. See [https://llvm.org/docs/Passes.html#transform-passes](https://llvm.org/docs/Passes.html#transform-passes) for more details about optimizations.
