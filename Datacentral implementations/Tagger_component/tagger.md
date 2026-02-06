# 1\. Purpose

The tagger component is designed to answer a single question:

**How can we extract *form* from information?**

It synthesises the theoretical framework developed in:

* **Text A:** *Are ideas alive? How historical civilisations were governed by ideas*  
* **Text B:** *How recommendation algorithms affect the formation of culture*

The goal is to build a system capable of identifying structural patterns—*egregores*—within any medium (text, image, video), representing them mathematically, and using them to compare, classify, and recommend content.

# 2\. Key Concepts

Before describing the methodology, the following terms are essential:  
\- **Token**: A basic unit of information (word, pixel value, video frame value).  
\- **Thoughtform**: A token that participates in a cycle—a repeated pattern within a token graph.  
\- **Egregore**: A network of memes (tokens) organised around a thoughtform, defined by recurrence strength.  
\- **Anchor**: The thoughtform around which an egregore tensor is constructed.  
\- **Tensor**: A vector‑like representation encoding the strengths of relationships between a thoughtform and other tokens.  
\- **Reference Index**: A mapping between raw symbols and token numbers.

# 3\. Methodology

The tagger pipeline consists of five major stages

## 3.1 Tokenisation

The first step is to convert raw media into a sequence of tokens.

### Text

1. Construct a reference index:  
    A dictionary mapping each unique word to the order of its first appearance.  
2. Convert the text into a sequence of words.  
3. Map each word to its corresponding number.  
    The text becomes a list of integers.

*(Future extension: tokenisation by morphemes rather than words.)*

### Images

A naïve tokenisation approach maps each pixel’s hexadecimal value to a token number in scanline order.

*(Note: This is a placeholder. More sophisticated perceptual tokenisation—feature detectors or embeddings—can replace this in future versions.)*

### Video

Tokenise each frame using the image method, then treat the video as a sequence of 2D token grids over time.

## 3.2 Graph Construction

Tokens are arranged into graphs that reflect the structure of the medium.

### Text → 1D graph

1 → 3 → 5 → 7

### Image → 2D graph

1 → 3 → 5 → 7

↓      ↓      ↓    ↓ 

3 → 6 → 4 → 8

This is decomposed into orthogonal 1D sequences:

* Horizontal sequences  
* Vertical sequences

**Video → 3D graph**

Decomposed into:

* Horizontal sequences  
* Vertical sequences   
* Temporal sequences

This ensures all media ultimately reduce to sets of 1D token sequences.

# 3.3 Thoughtform Detection

A **thoughtform** is defined as:

* a token that participates in a **cycle**,  
* where a cycle is a **closed walk** in a token sequence,  
* and the **minimal cycle length** defines the return distance.

Example:

Sequence: `3 → 6 → 3`  
 Thoughtform: `3`  
 Return distance: `2`

Thoughtforms are detected by scanning each 1D sequence and identifying repeated tokens.  
 For higher‑dimensional media, cross‑sequence recurrence is also checked.

**3.4 Strength Calculation**

For each thoughtform, compute its **strength**:

Strength \= frequency/(sequence length \* average return distance)

Where:

* **frequency** \= number of occurrences  
* **sequence length** \= length of the cycle sequence  
* **average return distance** \= average number of tokens between recurrences

Example for token `3` in `3 → 6 → 3`:

Strength \= 2/(3\*2) \= ⅓ 

# 3.5 Egregore Extraction

An **egregore set** is the set of tokens whose correlation strength with the thoughtform exceeds the thoughtform’s own baseline strength.

We use an adapted version of the strength formula to find the strength between a token and a thoughtform where the frequency is the number of times the token occurs and the average return distance is the average number of tokens between the token and the thoughtform.

For memes (non-thoughtform tokens) this simplifies to:

Strength \= 1/(sequence length \* distance from thoughtform) 

Where frequency is 1 by definition. We can rearrange this to get:

Distance from thoughtform \= 1/(sequence length \* strength) where the strength is the baseline strength of the thoughtform 

Tokens within this distance from occurrences of the thoughtform are included in the egregore set.

**Example**

Sequence: `3 → 6 → 3`  
 Thoughtform: `3`  
 Strength: `1/3`  
 Distance threshold: `1/(3 × 1/3) = 1`

Token `6` lies within distance 1 → included in the egregore.

Thus:

E={6}

# 4\. Tensor Representation

Each egregore is represented as a **tensor** anchored on its thoughtform.

* Each tensor dimension corresponds to a token in the **unified reference index**.  
* Each value corresponds to the **strength** of that token’s correlation with the anchor.

This allows egregores from different media to be compared in a shared coordinate system.

# 5\. Reference Index Unification

To compare egregores across files, all tensors must use the same token ordering.

Procedure:

1. Convert each reference index into an ordered list of symbols.  
2. Merge all lists into a unified index, removing duplicates.  
3. Remap all tensors from their original indices into the unified index.

This ensures consistent tensor alignment.

# 6\. Comparing Media

To compare two files:

1. Extract their egregore tensors.  
2. Normalise them to the unified reference index.  
3. Compute similarity using the **dot product** of corresponding tensors.  
4. Rank files by similarity.

# 7\. The experiment

I created a direct implementation of the method above in python including a function that allows you to input two pieces of text (and the file name of each piece of text) and it will create the references of the texts, tokenise the texts, extract the thoughtforms, create the thoughtform sets, create the thoughtform set reference indexes,extract the egregore tensors unify the reference indices and thoughtform set indices updating the egregore tensors into a common format and give the strength of the two text files as a decimal value. I can now directly test this method by uploading text files and seeing if these strength values actually reflect how similar the text files are. 

To perform this test I selected 3 sets of pairs text for each category: 

* High similarity  
* Medium similarity  
* Low similarity

## Findings

**High similarity**  
**Medium similarity**  
**Low similarity**

| Text pairing | Reason | Score |
| :---- | :---- | :---- |
| The Raven vs Annabel Lee  | Same Stoic concepts | 0.012450540585190168 |
| Meditations book 2 vs Enchridion | Same psychological motifs | 0.00024798518482772023 |
| The tell tale heart vs The black cat | Similar ethics, different metaphysics | 0.0007056744017995863 |
| Tao Te Cheng versus 1-10 vs Meditations Book 1 | Both books have similar themes however they approach them differently | 1.3893001838147057e-05 |
| The Yellow Wallpaper vs *The Tell‑Tale Heart* | Both books explore similar themes but from different perspectives | 0.00028391642516193273 |
| Aesops fables vs the book of proverbs | Both books are similar thematically but come from different contexts | 4.439103935979719e-05 |
| Ozymandias vs On the origin of species | These texts are conceptually unrelated | 7.380805499250904e-07 |
| Tao vs the black cat | These texts are both poetry but vastly different | 0.0001305644612593834 |
| The black cat vs ozymandias | These texts are both completely different | 2.7565450814343112e-05 |

This reflects that the system is very sensitive to thematic overlap and is working successfully.

Next I will integrate the youtube-transcript-api I can then perform a second experiment with youtube videos mirroring the experiment of text B. In terms of my project datacentral this means users will be able to upload their youtube histories using google activity then when they are working on a text file it will recommend them youtube videos they’ve previously watched that are similar. The only problem is I can’t remember the name of the API. 

# 8\. Appendix

## My python implementation 

`import json`  
`import math`  
`import os`  
`import numpy as np`  
`from functools import lru_cache`  
`from collections import Counter`

`# ------------------------------`  
`# Cached file loading`  
`# ------------------------------`  
`@lru_cache(maxsize=None)`  
`def load_json(path):`  
   `with open(path, "r") as f:`  
       `return json.load(f)`

`# ------------------------------`  
`# Token utilities`  
`# ------------------------------`  
`def parse_tokens(tokens):`  
   `return list(map(int, tokens.split(",")))`

`def extract_thoughtforms(tokens):`  
   `seq = parse_tokens(tokens)`  
   `counts = Counter(seq)`  
   `return [tok for tok, c in counts.items() if c >= 2]`

`# ------------------------------`  
`# Upload utilities`  
`# ------------------------------`  
`def get_uploads(files):`  
   `return [load_json(f"uploads/{file.split('.')[0]}.json") for file in files]`

`def create_unified_reference_index(files):`  
   `seen = set()`  
   `unified = []`

   `for index in get_uploads(files):`  
       `# index is dict token → pos`  
       `for token in sorted(index, key=index.get):`  
           `if token not in seen:`  
               `seen.add(token)`  
               `unified.append(token)`

   `return {tok: i for i, tok in enumerate(unified)}`

`# ------------------------------`  
`# Strength calculations`  
`# ------------------------------`  
`def calculate_strengths(tokens, file):`  
   `seq = parse_tokens(tokens)`  
   `counts = Counter(seq)`

   `thoughtforms = extract_thoughtforms(tokens)`  
   `file_output = f"uploads/{file.split('.')[0]}_thoughtforms.json"`

   `if not os.path.exists(file_output):`  
       `tf_index = {i: tf for i, tf in enumerate(thoughtforms)}`  
       `with open(file_output, "w") as f:`  
           `json.dump(tf_index, f)`

   `total = len(seq)`  
   `return [counts[tf] / total for tf in thoughtforms]`

`# ------------------------------`  
`# Egregore extraction`  
`# ------------------------------`  
`def extract_egregore_sets(tokens, file):`  
   `strengths = calculate_strengths(tokens, file)`  
   `seq = parse_tokens(tokens)`  
   `n = len(seq)`

   `distances = [n * s for s in strengths]`

   `positions = load_json(f"uploads/{file.split('.')[0]}_thoughtforms.json")`

   `eg_sets = []`  
   `for i, dist in enumerate(distances):`  
       `pos = positions[str(i)]  # correct mapping: thoughtform index → position`  
       `lo = max(0, math.floor(pos - dist))`  
       `hi = min(n, math.ceil(pos + dist))`  
       `eg_sets.append(seq[lo:hi])`

   `return eg_sets`

`# ------------------------------`  
`# Tensor remapping`  
`# ------------------------------`  
`def remap_tensor(tensor, old_index, unified_index):`  
   `new = [0] * len(unified_index)`

   `# Reverse lookup once`  
   `pos_to_token = {pos: tok for tok, pos in old_index.items()}`

   `for old_pos, strength in enumerate(tensor):`  
       `tok = pos_to_token.get(old_pos)`  
       `if tok in unified_index:`  
           `new[unified_index[tok]] = strength`

   `return new`

`# ------------------------------`  
`# Egregore tensor calculation`  
`# ------------------------------`  
`def calculate_egregore_tensors(tokens, file):`  
   `eg_sets = extract_egregore_sets(tokens, file)`  
   `seq = parse_tokens(tokens)`

   `tf_path = f"uploads/{file.split('.')[0]}_thoughtforms.json"`  
   `thoughtforms = load_json(tf_path)`  
   `tf_list = [thoughtforms[str(i)] for i in range(len(eg_sets))]`

   `# Ensure anchor is included`  
   `for i, eg in enumerate(eg_sets):`  
       `if tf_list[i] not in eg:`  
           `eg.insert(0, tf_list[i])`

   `strengths = []`  
   `for i, eg in enumerate(eg_sets):`  
       `anchor = tf_list[i]`  
       `anchor_pos = eg.index(anchor)`

       `precursors = [abs(anchor_pos - j) * len(seq) for j in range(len(eg))]`

       `# Compute strengths`  
       `s = []`  
       `for j, p in enumerate(precursors):`  
           `if p == 0:`  
               `s.append(0)`  
           `else:`  
               `s.append(seq.count(eg[j]) / p)`

       `strengths.append(s)`

   `return strengths`

`# ------------------------------`  
`# Main similarity function`  
`# ------------------------------`  
`def calculate_egregore_strength(tokens1, file1, tokens2, file2):`  
   `E1 = calculate_egregore_tensors(tokens1, file1)`  
   `E2 = calculate_egregore_tensors(tokens2, file2)`

   `idx1 = load_json(f"uploads/{file1.split('.')[0]}.json")`  
   `idx2 = load_json(f"uploads/{file2.split('.')[0]}.json")`

   `TF1 = load_json(f"uploads/{file1.split('.')[0]}_thoughtforms.json")`  
   `TF2 = load_json(f"uploads/{file2.split('.')[0]}_thoughtforms.json")`

   `TF1_list = [TF1[str(i)] for i in range(len(TF1))]`  
   `TF2_list = [TF2[str(i)] for i in range(len(TF2))]`

   `E1_dict = dict(zip(TF1_list, E1))`  
   `E2_dict = dict(zip(TF2_list, E2))`

   `shared = set(E1_dict) & set(E2_dict)`  
   `if not shared:`  
       `return 0`

   `unified = create_unified_reference_index([file1, file2])`

   `total = 0`  
   `for tf in shared:`  
       `t1 = remap_tensor(E1_dict[tf], idx1, unified)`  
       `t2 = remap_tensor(E2_dict[tf], idx2, unified)`  
       `total += np.dot(t1, t2)`

   `return total`

`# ------------------------------`  
`# Text utilities`  
`# ------------------------------`  
`def extract_reference_index(text, file_name):`  
   `words = list(dict.fromkeys(text.split()))`  
   `mapping = {w: i for i, w in enumerate(words)}`

   `with open(f"uploads/{file_name.split('.')[0]}.json", "w") as f:`  
       `json.dump(mapping, f)`

`def extract_tokens(text, file_name):`  
   `path = f"uploads/{file_name.split('.')[0]}.json"`  
   `if not os.path.exists(path):`  
       `extract_reference_index(text, file_name)`

   `ref = load_json(path)`  
   `return ",".join(str(ref[w]) for w in text.split())`

`def compare_texts(text1, file1, text2, file2):`  
   `return calculate_egregore_strength(`  
       `extract_tokens(text1, file1),`  
       `file1,`  
       `extract_tokens(text2, file2),`  
       `file2,`  
   `)`
