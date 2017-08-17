# 12.3. 細部控制[^1]

To implement full text searching there must be a function to create a`tsvector`from a document and a`tsquery`from a user query. Also, we need to return results in a useful order, so we need a function that compares documents with respect to their relevance to the query. It's also important to be able to display the results nicely.PostgreSQLprovides support for all of these functions.

### 12.3.1. Parsing Documents

PostgreSQLprovides the function`to_tsvector`for converting a document to the`tsvector`data type.



```
to_tsvector([
config
regconfig
, 
] 
document
text
) returns 
tsvector
```

`to_tsvector`parses a textual document into tokens, reduces the tokens to lexemes, and returns a`tsvector`which lists the lexemes together with their positions in the document. The document is processed according to the specified or default text search configuration. Here is a simple example:

```
SELECT to_tsvector('english', 'a fat  cat sat on a mat - it ate a fat rats');
                  to_tsvector
-----------------------------------------------------
 'ate':9 'cat':3 'fat':2,11 'mat':7 'rat':12 'sat':4

```

In the example above we see that the resulting`tsvector`does not contain the words`a`,`on`, or`it`, the word`rats`became`rat`, and the punctuation sign`-`was ignored.

The`to_tsvector`function internally calls a parser which breaks the document text into tokens and assigns a type to each token. For each token, a list of dictionaries \([Section 12.6](https://www.postgresql.org/docs/10/static/textsearch-dictionaries.html)\) is consulted, where the list can vary depending on the token type. The first dictionary that_recognizes_the token emits one or more normalized_lexemes_to represent the token. For example,`rats`became`rat`because one of the dictionaries recognized that the word`rats`is a plural form of`rat`. Some words are recognized as_stop words_\([Section 12.6.1](https://www.postgresql.org/docs/10/static/textsearch-dictionaries.html#textsearch-stopwords)\), which causes them to be ignored since they occur too frequently to be useful in searching. In our example these are`a`,`on`, and`it`. If no dictionary in the list recognizes the token then it is also ignored. In this example that happened to the punctuation sign`-`because there are in fact no dictionaries assigned for its token type \(`Space symbols`\), meaning space tokens will never be indexed. The choices of parser, dictionaries and which types of tokens to index are determined by the selected text search configuration \([Section 12.7](https://www.postgresql.org/docs/10/static/textsearch-configuration.html)\). It is possible to have many different configurations in the same database, and predefined configurations are available for various languages. In our example we used the default configuration`english`for the English language.

The function`setweight`can be used to label the entries of a`tsvector`with a given_weight_, where a weight is one of the letters`A`,`B`,`C`, or`D`. This is typically used to mark entries coming from different parts of a document, such as title versus body. Later, this information can be used for ranking of search results.

Because`to_tsvector`\(`NULL`\) will return`NULL`, it is recommended to use`coalesce`whenever a field might be null. Here is the recommended method for creating a`tsvector`from a structured document:

```
UPDATE tt SET ti =
    setweight(to_tsvector(coalesce(title,'')), 'A')    ||
    setweight(to_tsvector(coalesce(keyword,'')), 'B')  ||
    setweight(to_tsvector(coalesce(abstract,'')), 'C') ||
    setweight(to_tsvector(coalesce(body,'')), 'D');

```

Here we have used`setweight`to label the source of each lexeme in the finished`tsvector`, and then merged the labeled`tsvector`values using the`tsvector`concatenation operator`||`. \([Section 12.4.1](https://www.postgresql.org/docs/10/static/textsearch-features.html#textsearch-manipulate-tsvector)gives details about these operations.\)

### 12.3.2. Parsing Queries

PostgreSQLprovides the functions`to_tsquery`,`plainto_tsquery`, and`phraseto_tsquery`for converting a query to the`tsquery`data type.`to_tsquery`offers access to more features than either`plainto_tsquery`or`phraseto_tsquery`, but it is less forgiving about its input.



```
to_tsquery([
config
regconfig
, 
] 
querytext
text
) returns 
tsquery
```

`to_tsquery`creates a`tsquery`value from_`querytext`_, which must consist of single tokens separated by the`tsquery`operators`&`\(AND\),`|`\(OR\),`!`\(NOT\), and`<->`\(FOLLOWED BY\), possibly grouped using parentheses. In other words, the input to`to_tsquery`must already follow the general rules for`tsquery`input, as described in[Section 8.11.2](https://www.postgresql.org/docs/10/static/datatype-textsearch.html#datatype-tsquery). The difference is that while basic`tsquery`input takes the tokens at face value,`to_tsquery`normalizes each token into a lexeme using the specified or default configuration, and discards any tokens that are stop words according to the configuration. For example:

```
SELECT to_tsquery('english', 'The 
&
 Fat 
&
 Rats');
  to_tsquery   
---------------
 'fat' 
&
 'rat'

```

As in basic`tsquery`input, weight\(s\) can be attached to each lexeme to restrict it to match only`tsvector`lexemes of those weight\(s\). For example:

```
SELECT to_tsquery('english', 'Fat | Rats:AB');
    to_tsquery    
------------------
 'fat' | 'rat':AB

```

Also,`*`can be attached to a lexeme to specify prefix matching:

```
SELECT to_tsquery('supern:*A 
&
 star:A*B');
        to_tsquery        
--------------------------
 'supern':*A 
&
 'star':*AB

```

Such a lexeme will match any word in a`tsvector`that begins with the given string.

`to_tsquery`can also accept single-quoted phrases. This is primarily useful when the configuration includes a thesaurus dictionary that may trigger on such phrases. In the example below, a thesaurus contains the rule`supernovae stars : sn`:

```
SELECT to_tsquery('''supernovae stars'' 
&
 !crab');
  to_tsquery
---------------
 'sn' 
&
 !'crab'

```

Without quotes,`to_tsquery`will generate a syntax error for tokens that are not separated by an AND, OR, or FOLLOWED BY operator.



```
plainto_tsquery([
config
regconfig
, 
] 
querytext
text
) returns 
tsquery
```

`plainto_tsquery`transforms the unformatted text_`querytext`_to a`tsquery`value. The text is parsed and normalized much as for`to_tsvector`, then the`&`\(AND\)`tsquery`operator is inserted between surviving words.

Example:

```
SELECT plainto_tsquery('english', 'The Fat Rats');
 plainto_tsquery 
-----------------
 'fat' 
&
 'rat'

```

Note that`plainto_tsquery`will not recognize`tsquery`operators, weight labels, or prefix-match labels in its input:

```
SELECT plainto_tsquery('english', 'The Fat 
&
 Rats:C');
   plainto_tsquery   
---------------------
 'fat' 
&
 'rat' 
&
 'c'

```

Here, all the input punctuation was discarded as being space symbols.



```
phraseto_tsquery([
config
regconfig
, 
] 
querytext
text
) returns 
tsquery
```

`phraseto_tsquery`behaves much like`plainto_tsquery`, except that it inserts the`<->`\(FOLLOWED BY\) operator between surviving words instead of the`&`\(AND\) operator. Also, stop words are not simply discarded, but are accounted for by inserting`<`_`N`_&gt;operators rather than`<->`operators. This function is useful when searching for exact lexeme sequences, since the FOLLOWED BY operators check lexeme order not just the presence of all the lexemes.

Example:

```
SELECT phraseto_tsquery('english', 'The Fat Rats');
 phraseto_tsquery
------------------
 'fat' 
<
-
>
 'rat'

```

Like`plainto_tsquery`, the`phraseto_tsquery`function will not recognize`tsquery`operators, weight labels, or prefix-match labels in its input:

```
SELECT phraseto_tsquery('english', 'The Fat 
&
 Rats:C');
      phraseto_tsquery
-----------------------------
 'fat' 
<
-
>
 'rat' 
<
-
>
 'c'

```

### 12.3.3. Ranking Search Results

Ranking attempts to measure how relevant documents are to a particular query, so that when there are many matches the most relevant ones can be shown first.PostgreSQLprovides two predefined ranking functions, which take into account lexical, proximity, and structural information; that is, they consider how often the query terms appear in the document, how close together the terms are in the document, and how important is the part of the document where they occur. However, the concept of relevancy is vague and very application-specific. Different applications might require additional information for ranking, e.g., document modification time. The built-in ranking functions are only examples. You can write your own ranking functions and/or combine their results with additional factors to fit your specific needs.

The two ranking functions currently available are:



`ts_rank([`

_`weights`_

`float4[]`

,

\]

_`vector`_

`tsvector`

,

_`query`_

`tsquery`

\[

,

_`normalization`_

`integer`

\]\) returns

`float4`

Ranks vectors based on the frequency of their matching lexemes.



`ts_rank_cd([`

_`weights`_

`float4[]`

,

\]

_`vector`_

`tsvector`

,

_`query`_

`tsquery`

\[

,

_`normalization`_

`integer`

\]\) returns

`float4`

This function computes the_cover density_ranking for the given document vector and query, as described in Clarke, Cormack, and Tudhope's "Relevance Ranking for One to Three Term Queries" in the journal "Information Processing and Management", 1999. Cover density is similar to`ts_rank`ranking except that the proximity of matching lexemes to each other is taken into consideration.

This function requires lexeme positional information to perform its calculation. Therefore, it ignores any“stripped”lexemes in the`tsvector`. If there are no unstripped lexemes in the input, the result will be zero. \(See[Section 12.4.1](https://www.postgresql.org/docs/10/static/textsearch-features.html#textsearch-manipulate-tsvector)for more information about the`strip`function and positional information in`tsvector`s.\)

For both these functions, the optional_`weights`_argument offers the ability to weigh word instances more or less heavily depending on how they are labeled. The weight arrays specify how heavily to weigh each category of word, in the order:

```
{D-weight, C-weight, B-weight, A-weight}

```

If no_`weights`_are provided, then these defaults are used:

```
{0.1, 0.2, 0.4, 1.0}

```

Typically weights are used to mark words from special areas of the document, like the title or an initial abstract, so they can be treated with more or less importance than words in the document body.

Since a longer document has a greater chance of containing a query term it is reasonable to take into account document size, e.g., a hundred-word document with five instances of a search word is probably more relevant than a thousand-word document with five instances. Both ranking functions take an integer_`normalization`_option that specifies whether and how a document's length should impact its rank. The integer option controls several behaviors, so it is a bit mask: you can specify one or more behaviors using`|`\(for example,`2|4`\).

* 0 \(the default\) ignores the document length

* 1 divides the rank by 1 + the logarithm of the document length

* 2 divides the rank by the document length

* 4 divides the rank by the mean harmonic distance between extents \(this is implemented only by`ts_rank_cd`\)

* 8 divides the rank by the number of unique words in document

* 16 divides the rank by 1 + the logarithm of the number of unique words in document

* 32 divides the rank by itself + 1

If more than one flag bit is specified, the transformations are applied in the order listed.

It is important to note that the ranking functions do not use any global information, so it is impossible to produce a fair normalization to 1% or 100% as sometimes desired. Normalization option 32 \(`rank/(rank+1)`\) can be applied to scale all ranks into the range zero to one, but of course this is just a cosmetic change; it will not affect the ordering of the search results.

Here is an example that selects only the ten highest-ranked matches:

```
SELECT title, ts_rank_cd(textsearch, query) AS rank
FROM apod, to_tsquery('neutrino|(dark 
&
 matter)') query
WHERE query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |   rank
-----------------------------------------------+----------
 Neutrinos in the Sun                          |      3.1
 The Sudbury Neutrino Detector                 |      2.4
 A MACHO View of Galactic Dark Matter          |  2.01317
 Hot Gas and Dark Matter                       |  1.91171
 The Virgo Cluster: Hot Plasma and Dark Matter |  1.90953
 Rafting for Solar Neutrinos                   |      1.9
 NGC 4650A: Strange Galaxy and Dark Matter     |  1.85774
 Hot Gas and Dark Matter                       |   1.6123
 Ice Fishing for Cosmic Neutrinos              |      1.6
 Weak Lensing Distorts the Universe            | 0.818218

```

This is the same example using normalized ranking:

```
SELECT title, ts_rank_cd(textsearch, query, 32 /* rank/(rank+1) */ ) AS rank
FROM apod, to_tsquery('neutrino|(dark 
&
 matter)') query
WHERE  query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |        rank
-----------------------------------------------+-------------------
 Neutrinos in the Sun                          | 0.756097569485493
 The Sudbury Neutrino Detector                 | 0.705882361190954
 A MACHO View of Galactic Dark Matter          | 0.668123210574724
 Hot Gas and Dark Matter                       |  0.65655958650282
 The Virgo Cluster: Hot Plasma and Dark Matter | 0.656301290640973
 Rafting for Solar Neutrinos                   | 0.655172410958162
 NGC 4650A: Strange Galaxy and Dark Matter     | 0.650072921219637
 Hot Gas and Dark Matter                       | 0.617195790024749
 Ice Fishing for Cosmic Neutrinos              | 0.615384618911517
 Weak Lensing Distorts the Universe            | 0.450010798361481

```

Ranking can be expensive since it requires consulting the`tsvector`of each matching document, which can be I/O bound and therefore slow. Unfortunately, it is almost impossible to avoid since practical queries often result in large numbers of matches.

### 12.3.4. Highlighting Results

To present search results it is ideal to show a part of each document and how it is related to the query. Usually, search engines show fragments of the document with marked search terms.PostgreSQLprovides a function`ts_headline`that implements this functionality.



```
ts_headline([
config
regconfig
, 
] 
document
text
, 
query
tsquery
 [
, 
options
text
]) returns 
text
```

`ts_headline`accepts a document along with a query, and returns an excerpt from the document in which terms from the query are highlighted. The configuration to be used to parse the document can be specified by_`config`_; if_`config`_is omitted, the`default_text_search_config`configuration is used.

If an_`options`_string is specified it must consist of a comma-separated list of one or more_`option`_`=`_`value`_pairs. The available options are:

* `StartSel`,`StopSel`: the strings with which to delimit query words appearing in the document, to distinguish them from other excerpted words. You must double-quote these strings if they contain spaces or commas.

* `MaxWords`,`MinWords`: these numbers determine the longest and shortest headlines to output.

* `ShortWord`: words of this length or less will be dropped at the start and end of a headline. The default value of three eliminates common English articles.

* `HighlightAll`: Boolean flag; if`true`the whole document will be used as the headline, ignoring the preceding three parameters.

* `MaxFragments`: maximum number of text excerpts or fragments to display. The default value of zero selects a non-fragment-oriented headline generation method. A value greater than zero selects fragment-based headline generation. This method finds text fragments with as many query words as possible and stretches those fragments around the query words. As a result query words are close to the middle of each fragment and have words on each side. Each fragment will be of at most`MaxWords`and words of length`ShortWord`or less are dropped at the start and end of each fragment. If not all query words are found in the document, then a single fragment of the first`MinWords`in the document will be displayed.

* `FragmentDelimiter`: When more than one fragment is displayed, the fragments will be separated by this string.

Any unspecified options receive these defaults:

```
StartSel=
<
b
>
, StopSel=
<
/b
>
,
MaxWords=35, MinWords=15, ShortWord=3, HighlightAll=FALSE,
MaxFragments=0, FragmentDelimiter=" ... "

```

For example:

```
SELECT ts_headline('english',
  'The most common type of search
is to find all documents containing given query terms
and return them in order of their similarity to the
query.',
  to_tsquery('query 
&
 similarity'));
                        ts_headline                         
------------------------------------------------------------
 containing given 
<
b
>
query
<
/b
>
 terms
 and return them in order of their 
<
b
>
similarity
<
/b
>
 to the
 
<
b
>
query
<
/b
>
.

SELECT ts_headline('english',
  'The most common type of search
is to find all documents containing given query terms
and return them in order of their similarity to the
query.',
  to_tsquery('query 
&
 similarity'),
  'StartSel = 
<
, StopSel = 
>
');
                      ts_headline                      
-------------------------------------------------------
 containing given 
<
query
>
 terms
 and return them in order of their 
<
similarity
>
 to the
 
<
query
>
.

```

`ts_headline`uses the original document, not a`tsvector`summary, so it can be slow and should be used with care.

---



[^1]:  [PostgreSQL: Documentation: 10: 12.3. Controlling Text Search](https://www.postgresql.org/docs/10/static/textsearch-controls.html)

