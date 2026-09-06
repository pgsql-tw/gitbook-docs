## F.35. pg_trgm — support for similarity of text using trigram matching [#](#PGTRGM)

[F.35.1. Trigram (or Trigraph) Concepts](pgtrgm.md#PGTRGM-CONCEPTS)

[F.35.2. Functions and Operators](pgtrgm.md#PGTRGM-FUNCS-OPS)

[F.35.3. GUC Parameters](pgtrgm.md#PGTRGM-GUC)

[F.35.4. Index Support](pgtrgm.md#PGTRGM-INDEX)

[F.35.5. Text Search Integration](pgtrgm.md#PGTRGM-TEXT-SEARCH)

[F.35.6. References](pgtrgm.md#PGTRGM-REFERENCES)

[F.35.7. Authors](pgtrgm.md#PGTRGM-AUTHORS)

<a id="id-1.11.7.45.2"></a>

The `pg_trgm` module provides functions and operators
for determining the similarity of
alphanumeric text based on trigram matching, as
well as index operator classes that support fast searching for similar
strings.

This module is considered “trusted”, that is, it can be
installed by non-superusers who have `CREATE` privilege
on the current database.

<a id="PGTRGM-CONCEPTS"></a>

### F.35.1. Trigram (or Trigraph) Concepts [#](#PGTRGM-CONCEPTS)

A trigram is a group of three consecutive characters taken
from a string. We can measure the similarity of two strings by
counting the number of trigrams they share. This simple idea
turns out to be very effective for measuring the similarity of
words in many natural languages.

### Note

`pg_trgm` ignores non-word characters
(non-alphanumerics) when extracting trigrams from a string.
Each word is considered to have two spaces
prefixed and one space suffixed when determining the set
of trigrams contained in the string.
For example, the set of trigrams in the string
“`cat`” is
“ `c`”,
“ `ca`”,
“`cat`”, and
“`at` ”.
The set of trigrams in the string
“`foo|bar`” is
“ `f`”,
“ `fo`”,
“`foo`”,
“`oo` ”,
“ `b`”,
“ `ba`”,
“`bar`”, and
“`ar` ”.

<a id="PGTRGM-FUNCS-OPS"></a>

### F.35.2. Functions and Operators [#](#PGTRGM-FUNCS-OPS)

The functions provided by the `pg_trgm` module
are shown in [Table F.26](pgtrgm.md#PGTRGM-FUNC-TABLE), the operators
in [Table F.27](pgtrgm.md#PGTRGM-OP-TABLE).

<a id="PGTRGM-FUNC-TABLE"></a>

**Table F.26. `pg_trgm` Functions**

<table border="1" class="table" summary="pg_trgm Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.1.1.1.1"></a>
<code class="function">similarity</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        Returns a number that indicates how similar the two arguments are.
        The range of the result is zero (indicating that the two strings are
        completely dissimilar) to one (indicating that the two strings are
        identical).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.2.1.1.1"></a>
<code class="function">show_trgm</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        Returns an array of all the trigrams in the given string.
        (In practice this is seldom useful except for debugging.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.3.1.1.1"></a>
<code class="function">word_similarity</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        Returns a number that indicates the greatest similarity between
        the set of trigrams in the first string and any continuous extent
        of an ordered set of trigrams in the second string.  For details, see
        the explanation below.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.4.1.1.1"></a>
<code class="function">strict_word_similarity</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        Same as <code class="function">word_similarity</code>, but forces
        extent boundaries to match word boundaries.  Since we don't have
        cross-word trigrams, this function actually returns greatest similarity
        between first string and any continuous extent of words of the second
        string.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.5.1.1.1"></a>
<code class="function">show_limit</code> ()
        → <code class="returnvalue">real</code>
</p>
<p>
        Returns the current similarity threshold used by the <code class="literal">%</code>
        operator.  This sets the minimum similarity between
        two words for them to be considered similar enough to
        be misspellings of each other, for example.
        (<span class="emphasis"><em>Deprecated</em></span>; instead use <code class="command">SHOW</code>
<code class="varname">pg_trgm.similarity_threshold</code>.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.6.1.1.1"></a>
<code class="function">set_limit</code> ( <code class="type">real</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        Sets the current similarity threshold that is used by the <code class="literal">%</code>
        operator.  The threshold must be between 0 and 1 (default is 0.3).
        Returns the same value passed in.
        (<span class="emphasis"><em>Deprecated</em></span>; instead use <code class="command">SET</code>
<code class="varname">pg_trgm.similarity_threshold</code>.)
       </p></td></tr></tbody></table>

<br>

Consider the following example:

```

# SELECT word_similarity('word', 'two words');
 word_similarity
-----------------
             0.8
(1 row)
```

In the first string, the set of trigrams is
`{" w"," wo","wor","ord","rd "}`.
In the second string, the ordered set of trigrams is
`{" t"," tw","two","wo "," w"," wo","wor","ord","rds","ds "}`.
The most similar extent of an ordered set of trigrams in the second string
is `{" w"," wo","wor","ord"}`, and the similarity is
`0.8`.

This function returns a value that can be approximately understood as the
greatest similarity between the first string and any substring of the second
string. However, this function does not add padding to the boundaries of
the extent. Thus, the number of additional characters present in the
second string is not considered, except for the mismatched word boundaries.

At the same time, `strict_word_similarity`
selects an extent of words in the second string. In the example above,
`strict_word_similarity` would select the
extent of a single word `'words'`, whose set of trigrams is
`{" w"," wo","wor","ord","rds","ds "}`.

```

# SELECT strict_word_similarity('word', 'two words'), similarity('word', 'words');
 strict_word_similarity | similarity
------------------------+------------
               0.571429 |   0.571429
(1 row)
```

Thus, the `strict_word_similarity` function
is useful for finding the similarity to whole words, while
`word_similarity` is more suitable for
finding the similarity for parts of words.

<a id="PGTRGM-OP-TABLE"></a>

**Table F.27. `pg_trgm` Operators**

<table border="1" class="table" summary="pg_trgm Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">%</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns <code class="literal">true</code> if its arguments have a similarity
        that is greater than the current similarity threshold set by
        <code class="varname">pg_trgm.similarity_threshold</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;%</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns <code class="literal">true</code> if the similarity between the trigram
        set in the first argument and a continuous extent of an ordered trigram
        set in the second argument is greater than the current word similarity
        threshold set by <code class="varname">pg_trgm.word_similarity_threshold</code>
        parameter.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">%&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Commutator of the <code class="literal">&lt;%</code> operator.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;&lt;%</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns <code class="literal">true</code> if its second argument has a continuous
        extent of an ordered trigram set that matches word boundaries,
        and its similarity to the trigram set of the first argument is greater
        than the current strict word similarity threshold set by the
        <code class="varname">pg_trgm.strict_word_similarity_threshold</code> parameter.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">%&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Commutator of the <code class="literal">&lt;&lt;%</code> operator.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        Returns the <span class="quote">“<span class="quote">distance</span>”</span> between the arguments, that is
        one minus the <code class="function">similarity()</code> value.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;&lt;-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        Returns the <span class="quote">“<span class="quote">distance</span>”</span> between the arguments, that is
        one minus the <code class="function">word_similarity()</code> value.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;-&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        Commutator of the <code class="literal">&lt;&lt;-&gt;</code> operator.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;&lt;&lt;-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        Returns the <span class="quote">“<span class="quote">distance</span>”</span> between the arguments, that is
        one minus the <code class="function">strict_word_similarity()</code> value.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;-&gt;&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        Commutator of the <code class="literal">&lt;&lt;&lt;-&gt;</code> operator.
       </p></td></tr></tbody></table>

<br>

<a id="PGTRGM-GUC"></a>

### F.35.3. GUC Parameters [#](#PGTRGM-GUC)

<a id="GUC-PGTRGM-SIMILARITY-THRESHOLD"></a>

`pg_trgm.similarity_threshold` (`real`) <a id="id-1.11.7.45.7.2.1.1.3"></a> [#](#GUC-PGTRGM-SIMILARITY-THRESHOLD)
:   Sets the current similarity threshold that is used by the `%`
    operator. The threshold must be between 0 and 1 (default is 0.3).
<a id="GUC-PGTRGM-WORD-SIMILARITY-THRESHOLD"></a>

`pg_trgm.word_similarity_threshold` (`real`) <a id="id-1.11.7.45.7.2.2.1.3"></a> [#](#GUC-PGTRGM-WORD-SIMILARITY-THRESHOLD)
:   Sets the current word similarity threshold that is used by the
    `<%` and `%>` operators. The threshold
    must be between 0 and 1 (default is 0.6).
<a id="GUC-PGTRGM-STRICT-WORD-SIMILARITY-THRESHOLD"></a>

`pg_trgm.strict_word_similarity_threshold` (`real`) <a id="id-1.11.7.45.7.2.3.1.3"></a> [#](#GUC-PGTRGM-STRICT-WORD-SIMILARITY-THRESHOLD)
:   Sets the current strict word similarity threshold that is used by the
    `<<%` and `%>>` operators. The threshold
    must be between 0 and 1 (default is 0.5).

<a id="PGTRGM-INDEX"></a>

### F.35.4. Index Support [#](#PGTRGM-INDEX)

The `pg_trgm` module provides GiST and GIN index
operator classes that allow you to create an index over a text column for
the purpose of very fast similarity searches. These index types support
the above-described similarity operators, and additionally support
trigram-based index searches for `LIKE`, `ILIKE`,
`~`, `~*` and `=` queries.
The similarity comparisons are case-insensitive in a default build of
`pg_trgm`.
Inequality operators are not supported.
Note that those indexes may not be as efficient as regular B-tree indexes
for equality operator.

Example:

```

CREATE TABLE test_trgm (t text);
CREATE INDEX trgm_idx ON test_trgm USING GIST (t gist_trgm_ops);
```

or

```

CREATE INDEX trgm_idx ON test_trgm USING GIN (t gin_trgm_ops);
```

`gist_trgm_ops` GiST opclass approximates a set of
trigrams as a bitmap signature. Its optional integer parameter
`siglen` determines the
signature length in bytes. The default length is 12 bytes.
Valid values of signature length are between 1 and 2024 bytes. Longer
signatures lead to a more precise search (scanning a smaller fraction of the index and
fewer heap pages), at the cost of a larger index.

Example of creating such an index with a signature length of 32 bytes:

```

CREATE INDEX trgm_idx ON test_trgm USING GIST (t gist_trgm_ops(siglen=32));
```

At this point, you will have an index on the `t` column that
you can use for similarity searching. A typical query is

```

SELECT t, similarity(t, 'word') AS sml
  FROM test_trgm
  WHERE t % 'word'
  ORDER BY sml DESC, t;
```

This will return all values in the text column that are sufficiently
similar to *`word`*, sorted from best match to worst. The
index will be used to make this a fast operation even over very large data
sets.

A variant of the above query is

```

SELECT t, t <-> 'word' AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

This can be implemented quite efficiently by GiST indexes, but not
by GIN indexes. It will usually beat the first formulation when only
a small number of the closest matches is wanted.

Also you can use an index on the `t` column for word
similarity or strict word similarity. Typical queries are:

```

SELECT t, word_similarity('word', t) AS sml
  FROM test_trgm
  WHERE 'word' <% t
  ORDER BY sml DESC, t;
```

and

```

SELECT t, strict_word_similarity('word', t) AS sml
  FROM test_trgm
  WHERE 'word' <<% t
  ORDER BY sml DESC, t;
```

This will return all values in the text column for which there is a
continuous extent in the corresponding ordered trigram set that is
sufficiently similar to the trigram set of *`word`*,
sorted from best match to worst. The index will be used to make this
a fast operation even over very large data sets.

Possible variants of the above queries are:

```

SELECT t, 'word' <<-> t AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

and

```

SELECT t, 'word' <<<-> t AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

This can be implemented quite efficiently by GiST indexes, but not
by GIN indexes.

Beginning in PostgreSQL 9.1, these index types also support
index searches for `LIKE` and `ILIKE`, for example

```

SELECT * FROM test_trgm WHERE t LIKE '%foo%bar';
```

The index search works by extracting trigrams from the search string
and then looking these up in the index. The more trigrams in the search
string, the more effective the index search is. Unlike B-tree based
searches, the search string need not be left-anchored.

Beginning in PostgreSQL 9.3, these index types also support
index searches for regular-expression matches
(`~` and `~*` operators), for example

```

SELECT * FROM test_trgm WHERE t ~ '(foo|bar)';
```

The index search works by extracting trigrams from the regular expression
and then looking these up in the index. The more trigrams that can be
extracted from the regular expression, the more effective the index search
is. Unlike B-tree based searches, the search string need not be
left-anchored.

For both `LIKE` and regular-expression searches, keep in mind
that a pattern with no extractable trigrams will degenerate to a full-index
scan.

The choice between GiST and GIN indexing depends on the relative
performance characteristics of GiST and GIN, which are discussed elsewhere.

<a id="PGTRGM-TEXT-SEARCH"></a>

### F.35.5. Text Search Integration [#](#PGTRGM-TEXT-SEARCH)

Trigram matching is a very useful tool when used in conjunction
with a full text index. In particular it can help to recognize
misspelled input words that will not be matched directly by the
full text search mechanism.

The first step is to generate an auxiliary table containing all
the unique words in the documents:

```

CREATE TABLE words AS SELECT word FROM
        ts_stat('SELECT to_tsvector(''simple'', bodytext) FROM documents');
```

where `documents` is a table that has a text field
`bodytext` that we wish to search. The reason for using
the `simple` configuration with the `to_tsvector`
function, instead of using a language-specific configuration,
is that we want a list of the original (unstemmed) words.

Next, create a trigram index on the word column:

```

CREATE INDEX words_idx ON words USING GIN (word gin_trgm_ops);
```

Now, a `SELECT` query similar to the previous example can
be used to suggest spellings for misspelled words in user search terms.
A useful extra test is to require that the selected words are also of
similar length to the misspelled word.

### Note

Since the `words` table has been generated as a separate,
static table, it will need to be periodically regenerated so that
it remains reasonably up-to-date with the document collection.
Keeping it exactly current is usually unnecessary.

<a id="PGTRGM-REFERENCES"></a>

### F.35.6. References [#](#PGTRGM-REFERENCES)

GiST Development Site
<http://www.sai.msu.su/~megera/postgres/gist/>

Tsearch2 Development Site
<http://www.sai.msu.su/~megera/postgres/gist/tsearch/V2/>

<a id="PGTRGM-AUTHORS"></a>

### F.35.7. Authors [#](#PGTRGM-AUTHORS)

Oleg Bartunov `<oleg@sai.msu.su>`, Moscow, Moscow University, Russia

Teodor Sigaev `<teodor@sigaev.ru>`, Moscow, Delta-Soft Ltd.,Russia

Alexander Korotkov `<a.korotkov@postgrespro.ru>`, Moscow, Postgres Professional, Russia

Documentation: Christopher Kings-Lynne

This module is sponsored by Delta-Soft Ltd., Moscow, Russia.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgtrgm.html)（英文原文，待翻譯）
