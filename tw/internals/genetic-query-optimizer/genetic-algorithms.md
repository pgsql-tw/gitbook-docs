# 59.2. Genetic Algorithms

The genetic algorithm \(GA\) is a heuristic optimization method which operates through randomized search. The set of possible solutions for the optimization problem is considered as a _population_ of _individuals_. The degree of adaptation of an individual to its environment is specified by its _fitness_.

The coordinates of an individual in the search space are represented by _chromosomes_, in essence a set of character strings. A _gene_ is a subsection of a chromosome which encodes the value of a single parameter being optimized. Typical encodings for a gene could be _binary_ or _integer_.

Through simulation of the evolutionary operations _recombination_, _mutation_, and _selection_ new generations of search points are found that show a higher average fitness than their ancestors.

According to the comp.ai.genetic FAQ it cannot be stressed too strongly that a GA is not a pure random search for a solution to a problem. A GA uses stochastic processes, but the result is distinctly non-random \(better than random\).

**Figure 59.1. Structured Diagram of a Genetic Algorithm**

| P\(t\) | generation of ancestors at a time t |
| :--- | :--- |
| P''\(t\) | generation of descendants at a time t |

```text
+=========================================+
|>>>>>>>>>>>  Algorithm GA  <<<<<<<<<<<<<<|
+=========================================+
| INITIALIZE t := 0                       |
+=========================================+
| INITIALIZE P(t)                         |
+=========================================+
| evaluate FITNESS of P(t)                |
+=========================================+
| while not STOPPING CRITERION do         |
|   +-------------------------------------+
|   | P'(t)  := RECOMBINATION{P(t)}       |
|   +-------------------------------------+
|   | P''(t) := MUTATION{P'(t)}           |
|   +-------------------------------------+
|   | P(t+1) := SELECTION{P''(t) + P(t)}  |
|   +-------------------------------------+
|   | evaluate FITNESS of P''(t)          |
|   +-------------------------------------+
|   | t := t + 1                          |
+===+=====================================+
```

