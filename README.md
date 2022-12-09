
``` python
%load_ext autoreload
%autoreload 2
```

# BNCparse

> Parsing the BNC2014 Spoken with Python.

Quirin Würschinger, LMU Munich

<q.wuerschinger@lmu.de>

## Data overview

``` mermaid
classDiagram

class text {
    <<conversation>>
    text_id("Text ID")
}

class u {
    <<utterance>>
    n("Consecutive utterance number")
    who("Speaker ID")
    trans("Transition type")
    whoConfidence("Attribution confidence")
}

class w {
    <<token>>
    pos("part-of-speech tag [CLAWS]")
    lemma("lemmatised form")
    class("“simple” POS tag or major word-class")
    usas("semantic tag [USAS]")
}

class meta_speaker {
    <<meta_speaker>>
    id("Speaker ID")
    exactage("Exact age")
    age1994("Age (BNC1994 groups)")
    agerange("Age range")
    gender("Gender")
    nat("Nationality")
    birthplace("Place of birth")
    birthcountry("Country of birth")
    l1("First language")
    lingorig("Linguistic origin")
    dialect_rep("Accent/dialect as reported")
    hab_city("City/town living")
    hab_country("Country living")
    hab_dur("Duration living (years)")
    dialect_l1("Dialect at Level 1")
    dialect_l2("Dialect at Level 2")
    dialect_l3("Dialect at Level 3")
    dialect_l4("Dialect at Level 4")
    edqual("Highest qualification")
    occupation("Occupation: title")
    socgrade("Class: Social grade")
    nssec("Class: NS-SEC")
    l2("L2 (if bilingual)")
    fls("Foreign languages spoken")
    in_core("Part of core set of speakers")
}

class meta_text {
    <<meta_text>>
    text_id("Text ID")
    rec_length("Recording length")
    rec_date("Recording date")
    rec_year("Year of recording")
    rec_period("Recording period")
    n_speakers("Number of speakers")
    list_speakers("List of speaker IDs")
    rec_loc("Recording location")
    relationships("Inter-speaker relationship")
    topics("Topics covered")
    activity("Activity description")
    conv_type("Selected characterisations of conversation type")
    conventions("Transcription conventions used")
    in_sample("Sample release inclusion")
    transcriber("Transcriber")
}

text ..* u : contains
u ..* w : contains
text .. meta_text : text_id
u .. meta_speaker : who=id
```

# Load packages

Package requirements are stored in `requirements.yml`.

::: {.cell 0=‘e’ 1=‘x’ 2=‘p’ 3=‘o’ 4=‘r’ 5=‘t’}

``` python
from pathlib import Path
from collections import defaultdict

from lxml import etree
import pandas as pd
```

:::

# Variables

BNC2014 needs to be downloaded for this script to work. It can be
obtained from the official [BNC
website](http://corpora.lancs.ac.uk/bnc2014/).

The following variables need to be updated to the corpus’ local path. In
the current setting the BNC2014 data were stored in the project folder
in the folder `data/bnc-2014-spoken`.

For development, I use a small subset of the corpus contained in
`data/test` that only contains the first 10 texts.

``` python
testing = True

if testing:
    path_bnc = Path('../data/test/bnc-2014-spoken')
    texts_n = 10
    tokens_n = 94_659
else:
    path_bnc = Path('../data/bnc-2014-spoken')
    texts_n = 1251
    tokens_n = 11_422_615
```

``` python
path_corpus = Path(path_bnc / 'spoken' / 'tagged')
path_metadata = Path(path_bnc / 'spoken' / 'metadata')
```

``` python
assert path_bnc.exists()
assert path_corpus.exists()
assert path_metadata.exists()
```

# Load and parse XML

``` python
path_texts = list(path_corpus.glob('*.xml'))
```

``` python
assert len(path_texts) == texts_n
```

::: {.cell 0=‘e’ 1=‘x’ 2=‘p’ 3=‘o’ 4=‘r’ 5=‘t’}

``` python
def get_xml(f_path):
    with open(f_path, 'r') as f:
        f = f.read()
    xml = etree.fromstring(f)
    return xml
```

:::

``` python
texts = [get_xml(path) for path in path_texts]
```

# Corpus statistics

## Texts

Calculate the total number of texts in the corpus.

``` python
text_ids = [xml.get('id') for xml in texts]

print(f"number of documents in the corpus: {len(text_ids)}")
```

    number of documents in the corpus: 1251

``` python
assert len(text_ids) == texts_n
```

## Speakers

1.  Determine all speakers in the corpus.
2.  Calculate the total number of words each speaker has contributed to
    the corpus.

``` python
speakers_words = defaultdict(int)
for text in texts:
    for u in text.iter('u'):
        speaker = u.get('who')
        n_words = len([w for w in u.iter('w')])
        speakers_words[speaker] += n_words
```

### Number of speakers

``` python
print(f"number of speakers: {len(speakers_words)}")
```

    number of speakers: 671

### Words per speaker

``` python
df_speakers_tokens = pd.DataFrame(
    list(speakers_words.items()), columns=['speaker', 'tokens'])
df_speakers_tokens = df_speakers_tokens.sort_values('tokens', ascending=False)
df_speakers_tokens
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>speaker</th>
      <th>tokens</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>179</th>
      <td>S0192</td>
      <td>362107</td>
    </tr>
    <tr>
      <th>6</th>
      <td>S0012</td>
      <td>277953</td>
    </tr>
    <tr>
      <th>17</th>
      <td>S0084</td>
      <td>276558</td>
    </tr>
    <tr>
      <th>18</th>
      <td>S0041</td>
      <td>208025</td>
    </tr>
    <tr>
      <th>59</th>
      <td>S0439</td>
      <td>205049</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>537</th>
      <td>S0121</td>
      <td>61</td>
    </tr>
    <tr>
      <th>654</th>
      <td>S0414</td>
      <td>43</td>
    </tr>
    <tr>
      <th>388</th>
      <td>S0413</td>
      <td>36</td>
    </tr>
    <tr>
      <th>670</th>
      <td>S0066</td>
      <td>28</td>
    </tr>
    <tr>
      <th>415</th>
      <td>S0676</td>
      <td>19</td>
    </tr>
  </tbody>
</table>
<p>671 rows × 2 columns</p>
</div>

The table containing all speakers and their total token counts can be
found in `speakers_tokens.csv`.

``` python
if not testing:
    df_speakers_tokens.to_csv('../out/speakers_tokens.csv', index=False)
```

## Vocabulary

``` python
tokens = []
for text in texts:
    for w in text.iter('w'):
        tokens.append(w.text)
```

``` python
pd.DataFrame([
    ['tokens', f'{len(tokens):,}'],
    ['types', f'{len(set(tokens)):,}'],
]
)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>tokens</td>
      <td>11,422,615</td>
    </tr>
    <tr>
      <th>1</th>
      <td>types</td>
      <td>69,190</td>
    </tr>
  </tbody>
</table>
</div>

# Export corpus data in tabular format

In addition to the metadata present in the corpus, I’ve added three
columns providing positional information about the tokens:

- `u_toks`: total number of tokens in the given utterance
- `w_idx`: token position (‘index’) in the given utterance, starting at
  1
- `w_idx_rel`: relative token position in the given utterance:
  `w_idx / u_toks`

``` python
%%time

tokens = []

for text in texts:
    for u in text.findall('u'):
        for i, w in enumerate(u.iter('w')):
            tok_d = {}

            tok_d['text_id'] = text.get('id')

            tok_d['u_n'] = u.get('n')
            tok_d['u_who'] = u.get('who')
            tok_d['u_trans'] = u.get('trans')
            tok_d['u_whoConfidence'] = u.get('whoConfidence')
            tok_d['u_toks'] = len(list(u.iter('w')))

            tok_d['w_pos'] = w.get('pos')
            tok_d['w_lemma'] = w.get('lemma')
            tok_d['w_class'] = w.get('class')
            tok_d['w_usas'] = w.get('usas')
            tok_d['w_text'] = w.text
            tok_d['w_idx'] = i + 1
            tok_d['w_idx_rel'] = round(tok_d['w_idx'] / tok_d['u_toks'], 2)

            tokens.append(tok_d)
```

    CPU times: user 1min 43s, sys: 1min 42s, total: 3min 26s
    Wall time: 4min 19s

``` python
%%time
tokens = pd.DataFrame(tokens)
```

    CPU times: user 54.8 s, sys: 3min 36s, total: 4min 31s
    Wall time: 6min 1s

``` python
tokens.head(50)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>text_id</th>
      <th>u_n</th>
      <th>u_who</th>
      <th>u_trans</th>
      <th>u_whoConfidence</th>
      <th>u_toks</th>
      <th>w_pos</th>
      <th>w_lemma</th>
      <th>w_class</th>
      <th>w_usas</th>
      <th>w_text</th>
      <th>w_idx</th>
      <th>w_idx_rel</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>PPIS1</td>
      <td>i</td>
      <td>PRON</td>
      <td>Z8</td>
      <td>I</td>
      <td>1</td>
      <td>0.06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>VBM</td>
      <td>be</td>
      <td>VERB</td>
      <td>A3</td>
      <td>'m</td>
      <td>2</td>
      <td>0.11</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>JJ</td>
      <td>glad</td>
      <td>ADJ</td>
      <td>E4:2</td>
      <td>glad</td>
      <td>3</td>
      <td>0.17</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>EX</td>
      <td>there</td>
      <td>PRON</td>
      <td>Z5</td>
      <td>there</td>
      <td>4</td>
      <td>0.22</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>VBZ</td>
      <td>be</td>
      <td>VERB</td>
      <td>A3</td>
      <td>'s</td>
      <td>5</td>
      <td>0.28</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>AT</td>
      <td>the</td>
      <td>ART</td>
      <td>Z5</td>
      <td>the</td>
      <td>6</td>
      <td>0.33</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>MC</td>
      <td>two</td>
      <td>ADJ</td>
      <td>N1</td>
      <td>two</td>
      <td>7</td>
      <td>0.39</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>PNQS</td>
      <td>who</td>
      <td>PRON</td>
      <td>Z8</td>
      <td>who</td>
      <td>8</td>
      <td>0.44</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>PPIS1</td>
      <td>i</td>
      <td>PRON</td>
      <td>Z8</td>
      <td>I</td>
      <td>9</td>
      <td>0.50</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>RR</td>
      <td>almost</td>
      <td>ADV</td>
      <td>A13:4</td>
      <td>almost</td>
      <td>10</td>
      <td>0.56</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>VVD</td>
      <td>come</td>
      <td>VERB</td>
      <td>A1:1:1</td>
      <td>came</td>
      <td>11</td>
      <td>0.61</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>TO</td>
      <td>to</td>
      <td>PREP</td>
      <td>Z5</td>
      <td>to</td>
      <td>12</td>
      <td>0.67</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>RR</td>
      <td>well</td>
      <td>ADV</td>
      <td>A5:1</td>
      <td>well</td>
      <td>13</td>
      <td>0.72</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>XX</td>
      <td>not</td>
      <td>ADV</td>
      <td>Z6</td>
      <td>not</td>
      <td>14</td>
      <td>0.78</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>VVD</td>
      <td>come</td>
      <td>VERB</td>
      <td>A4:1</td>
      <td>came</td>
      <td>15</td>
      <td>0.83</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>II</td>
      <td>to</td>
      <td>PREP</td>
      <td>A4:1</td>
      <td>to</td>
      <td>16</td>
      <td>0.89</td>
    </tr>
    <tr>
      <th>16</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>NN2</td>
      <td>blow</td>
      <td>SUBST</td>
      <td>S8</td>
      <td>blows</td>
      <td>17</td>
      <td>0.94</td>
    </tr>
    <tr>
      <th>17</th>
      <td>SN64</td>
      <td>1</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>18</td>
      <td>CCB</td>
      <td>but</td>
      <td>CONJ</td>
      <td>Z5</td>
      <td>but</td>
      <td>18</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>18</th>
      <td>SN64</td>
      <td>3</td>
      <td>S0590</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>1</td>
      <td>UH</td>
      <td>erm</td>
      <td>INTERJ</td>
      <td>Z4</td>
      <td>erm</td>
      <td>1</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>19</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>VDD</td>
      <td>do</td>
      <td>VERB</td>
      <td>Z5</td>
      <td>did</td>
      <td>1</td>
      <td>0.11</td>
    </tr>
    <tr>
      <th>20</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>PPY</td>
      <td>you</td>
      <td>PRON</td>
      <td>Z8</td>
      <td>you</td>
      <td>2</td>
      <td>0.22</td>
    </tr>
    <tr>
      <th>21</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>VVI</td>
      <td>put</td>
      <td>VERB</td>
      <td>X9:2</td>
      <td>put</td>
      <td>3</td>
      <td>0.33</td>
    </tr>
    <tr>
      <th>22</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>APPGE</td>
      <td>your</td>
      <td>PRON</td>
      <td>Z8</td>
      <td>your</td>
      <td>4</td>
      <td>0.44</td>
    </tr>
    <tr>
      <th>23</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>NN1</td>
      <td>foot</td>
      <td>SUBST</td>
      <td>X9:2</td>
      <td>foot</td>
      <td>5</td>
      <td>0.56</td>
    </tr>
    <tr>
      <th>24</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>II</td>
      <td>in</td>
      <td>PREP</td>
      <td>X9:2</td>
      <td>in</td>
      <td>6</td>
      <td>0.67</td>
    </tr>
    <tr>
      <th>25</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>PPH1</td>
      <td>it</td>
      <td>PRON</td>
      <td>X9:2</td>
      <td>it</td>
      <td>7</td>
      <td>0.78</td>
    </tr>
    <tr>
      <th>26</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>RL</td>
      <td>somewhere</td>
      <td>ADV</td>
      <td>M6</td>
      <td>somewhere</td>
      <td>8</td>
      <td>0.89</td>
    </tr>
    <tr>
      <th>27</th>
      <td>SN64</td>
      <td>4</td>
      <td>S0588</td>
      <td>nonoverlap</td>
      <td>high</td>
      <td>9</td>
      <td>YQUE</td>
      <td>PUNC</td>
      <td>STOP</td>
      <td></td>
      <td>?</td>
      <td>9</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>28</th>
      <td>SN64</td>
      <td>5</td>
      <td>S0589</td>
      <td>overlap</td>
      <td>high</td>
      <td>7</td>
      <td>AT</td>
      <td>no</td>
      <td>ART</td>
      <td>Z6</td>
      <td>no</td>
      <td>1</td>
      <td>0.14</td>
    </tr>
    <tr>
      <th>29</th>
      <td>SN64</td>
      <td>5</td>
      <td>S0589</td>
      <td>overlap</td>
      <td>high</td>
      <td>7</td>
      <td>NN1</td>
      <td>idea</td>
      <td>SUBST</td>
      <td>X4:1</td>
      <td>idea</td>
      <td>2</td>
      <td>0.29</td>
    </tr>
    <tr>
      <th>30</th>
      <td>SN64</td>
      <td>5</td>
      <td>S0589</td>
      <td>overlap</td>
      <td>high</td>
      <td>7</td>
      <td>RRQ</td>
      <td>where</td>
      <td>ADV</td>
      <td>M6</td>
      <td>where</td>
      <td>3</td>
      <td>0.43</td>
    </tr>
    <tr>
      <th>31</th>
      <td>SN64</td>
      <td>5</td>
      <td>S0589</td>
      <td>overlap</td>
      <td>high</td>
      <td>7</td>
      <td>PPHS2</td>
      <td>they</td>
      <td>PRON</td>
      <td>Z8</td>
      <td>they</td>
      <td>4</td>
      <td>0.57</td>
    </tr>
    <tr>
      <th>32</th>
      <td>SN64</td>
      <td>5</td>
      <td>S0589</td>
      <td>overlap</td>
      <td>high</td>
      <td>7</td>
      <td>VH0</td>
      <td>have</td>
      <td>VERB</td>
      <td>Z5</td>
      <td>'ve</td>
      <td>5</td>
      <td>0.71</td>
    </tr>
    <tr>
      <th>33</th>
      <td>SN64</td>
      <td>5</td>
      <td>S0589</td>
      <td>overlap</td>
      <td>high</td>
      <td>7</td>
      <td>VBN</td>
      <td>be</td>
      <td>VERB</td>
      <td>Z5</td>
      <td>been</td>
      <td>6</td>
      <td>0.86</td>
    </tr>
    <tr>
      <th>34</th>
      <td>SN64</td>
      <td>5</td>
      <td>S0589</td>
      <td>overlap</td>
      <td>high</td>
      <td>7</td>
      <td>VVN</td>
      <td>put</td>
      <td>VERB</td>
      <td>M2</td>
      <td>put</td>
      <td>7</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>35</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>UH</td>
      <td>no</td>
      <td>INTERJ</td>
      <td>Z4</td>
      <td>no</td>
      <td>1</td>
      <td>0.06</td>
    </tr>
    <tr>
      <th>36</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>UH</td>
      <td>no</td>
      <td>INTERJ</td>
      <td>Z4</td>
      <td>no</td>
      <td>2</td>
      <td>0.11</td>
    </tr>
    <tr>
      <th>37</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>UH</td>
      <td>no</td>
      <td>INTERJ</td>
      <td>Z4</td>
      <td>no</td>
      <td>3</td>
      <td>0.17</td>
    </tr>
    <tr>
      <th>38</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>AT1</td>
      <td>a</td>
      <td>ART</td>
      <td>Z5</td>
      <td>a</td>
      <td>4</td>
      <td>0.22</td>
    </tr>
    <tr>
      <th>39</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>NN1</td>
      <td>man</td>
      <td>SUBST</td>
      <td>S2:2</td>
      <td>man</td>
      <td>5</td>
      <td>0.28</td>
    </tr>
    <tr>
      <th>40</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>AT1</td>
      <td>a</td>
      <td>ART</td>
      <td>Z5</td>
      <td>a</td>
      <td>6</td>
      <td>0.33</td>
    </tr>
    <tr>
      <th>41</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>NN</td>
      <td>pair</td>
      <td>SUBST</td>
      <td>N5</td>
      <td>pair</td>
      <td>7</td>
      <td>0.39</td>
    </tr>
    <tr>
      <th>42</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>IO</td>
      <td>of</td>
      <td>PREP</td>
      <td>Z5</td>
      <td>of</td>
      <td>8</td>
      <td>0.44</td>
    </tr>
    <tr>
      <th>43</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>NN2</td>
      <td>man</td>
      <td>SUBST</td>
      <td>S2:2</td>
      <td>men</td>
      <td>9</td>
      <td>0.50</td>
    </tr>
    <tr>
      <th>44</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>CCB</td>
      <td>but</td>
      <td>CONJ</td>
      <td>Z5</td>
      <td>but</td>
      <td>10</td>
      <td>0.56</td>
    </tr>
    <tr>
      <th>45</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>MC1</td>
      <td>one</td>
      <td>ADJ</td>
      <td>N1</td>
      <td>one</td>
      <td>11</td>
      <td>0.61</td>
    </tr>
    <tr>
      <th>46</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>MC1</td>
      <td>one</td>
      <td>ADJ</td>
      <td>N1</td>
      <td>one</td>
      <td>12</td>
      <td>0.67</td>
    </tr>
    <tr>
      <th>47</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>IO</td>
      <td>of</td>
      <td>PREP</td>
      <td>Z5</td>
      <td>of</td>
      <td>13</td>
      <td>0.72</td>
    </tr>
    <tr>
      <th>48</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>PPHO2</td>
      <td>they</td>
      <td>PRON</td>
      <td>Z8</td>
      <td>them</td>
      <td>14</td>
      <td>0.78</td>
    </tr>
    <tr>
      <th>49</th>
      <td>SN64</td>
      <td>6</td>
      <td>S0590</td>
      <td>overlap</td>
      <td>high</td>
      <td>18</td>
      <td>XX</td>
      <td>not</td>
      <td>ADV</td>
      <td>Z6</td>
      <td>not</td>
      <td>15</td>
      <td>0.83</td>
    </tr>
  </tbody>
</table>
</div>

``` python
assert len(tokens) == tokens_n
```

I export the full token table to `tokens.csv`.

``` python
if not testing:
    tokens.to_csv('../out/tokens.csv', index=False)
```

I also export a smaller version for use in spreadsheet software. This
version contains the first 50,000 tokens in the corpus and is stored in
`tokens_50k.csv`.

``` python
if not testing:
    (tokens
     .head(50_000)
     .to_csv('../out/tokens_50k.csv', index=False))
```

::: {.cell 0=‘h’ 1=‘i’ 2=‘d’ 3=‘e’}

``` python
import nbdev
nbdev.nbdev_export()
```

:::
