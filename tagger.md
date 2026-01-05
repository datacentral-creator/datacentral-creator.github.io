**Navigation:**  
[Research](index.md) | [Datacentral](https://github.com/datacentral-creator/Datacentral) | [History](history.md)
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

# 8\. Speculative ontological framework

Additionally, a concept that emerged in text B was that users are pushed into echo chambers more so due to psychology than the direct effect of the youtube recommendation algorithm. Ultimately youtube is a collection of videos. Videos on youtube are made by people and every video ultimately expresses some kind of idea \- whether this is directly in terms of perhaps documentary videos or commentary videos or videos that are expressions of culture for example gaming videos are ultimately expressing the ideas embedded in the game. Therefore we can say that the collection of videos on youtube will likely form an egregore. Ultimately our notion of social interaction is typically conceived of people interacting with people however we could easily replace this with an egregore interacting with an egregore and the methodology would be the same (in the terms of an interaction as an exchange of memes). In this perspective we can classify watching youtube as a kind of social interaction. In our typical conception of a social interaction \- a conversation, the typical format people think of is one where we take turns speaking. There are two people, one person says something and the other person listens, then the person responds to the thing the first person said and vice versa. If we think of this in terms of memes when the first person is speaking and the second person is listening the first person is effectively inducing memes in the second person's head and then vice versa when the second person replies. Visually, we can conceive this as the meme “moving” from the head of one person to the other. In reality, a conversation isn’t typically perfectly balanced though. Typically one person tends to dominate the conversation \- that is one person will speak more than the other. Returning to our memetic visualisation we can say the person who is dominant in the conversation is doing the thinking and generating the ideas and the person who is listening is internalising these ideas in the sense described in Text A when talking about internalising patterns. We can think about interacting with youtube not just as a social interaction but a conversation. We “talk” to youtube by providing it with engagement patterns and it “replies” to us by recommending content. The problem with the conversation with youtube is that youtube is the dominant agent of this conversation kind of “pushing” it’s memes onto us and causing us to internalise what youtube is “saying” to us becoming **passive** recipients of memes as shown by decreasing social chaos in Text B.This is also embodied by phenomena such as parasocial relationships.This is the core idea that datacentral tries to overcome embodied by the tagger component \- it seeks to push the act of meme generation onto the user \- extracting form from information. 

This also links into a theory I’ve heard called “breeze theory”. Breeze theory is a theory that reality has an inescapable recursive nature. It actually echoes the themes of gnosticism whilst being \- as far as I know \- completely uninspired by it which I find fundamentally compelling. I will not regard breeze theory as an academic source as it has not been peer reviewed however I will consider it as a philosophical argument. Additionally, truth be told I haven’t extensively investigated breeze theory however I am aware of it on a superficial level. 

It echoes a notion I conceived personally. If we refer back to text A we can conceive ideas in terms of cortical columns however ultimately the evolutionary purpose of cortical columns is to model the reality around us \- in this biological sense we can conceive ideas as expressions of models of the world around us built off internalisations of these external qualities. If we think about ideas in terms of those qualities \- these qualities are ultimately expressions of physical systems \- if we conceive these physical systems as recursive as proposed in breeze theory, or at least simply hierarchical we can conceive a kind of “inverse idea”. If an idea is a construction of internalised patterns an “inverse idea” is simply the same thing except instead of being internalised it’s externalised. Ideas and inverse ideas fundamentally work in exactly the same way except inverse ideas don’t propagate through minds they propagate through physical systems. In the same way as we have memes we could then have “inverse memes” and even “inverse egregores” which are simply the systems themselves. We can think of “inverse egregores” as the patterns that multitudes of cultures across the world independently conceived of as deities or spirits. Returning to this hierarchical view we can conceive complex inverse egregores → qualities → Internalised qualities → Internalised egregores. 

There exists an idea that biological life exists as a catalyst of entropy \- perhaps this hierarchy I have conceived is an expression of systematic symmetry and throughout time the symmetry moves towards the mental side. The question becomes is there a way to accelerate this movement?

Case study: Tulpamancy 

# 9\. Future Vision: The Simulatrix

In the long term, the tagger will be extended with:

## 1\. Computational cortical columns

A model inspired by the Thousand Brains Theory, enabling the system to interpret egregores as literal neural‑like activations.

## 2\. Unified multimodal mapping

Text, images, and video mapped into the same structural space.

## 3\. Bidirectional interaction

* Input media → ask questions about it  
* Input text → generate media

## 4\. Research assistant capabilities

A system capable of analysing, synthesising, and generating structured knowledge.

## 5\. Computational physics

A speculative goal: using structural extraction to identify patterns in physical systems.

# Final Notes

This specification defines the theoretical foundation of the tagger component.  
 It is intentionally modular, allowing future improvements in:

* tokenisation  
* graph construction  
* perceptual modelling  
* tensor algebra  
* semantic grounding

The tagger is the first step toward a general system for extracting, comparing, and generating *form* across all media.

# 10\. Appendix

## My python implementation 

`import json`  
`import math`  
`import os`  
`import numpy as np`

`def get_uploads(files):`  
   `uploads = [json.load(open("uploads/"+file.split(".")[0]+".json")) for file in files]`  
   `return uploads`

`def create_unified_reference_index(files=os.listdir("uploads")):`  
   `indices = [sorted(index,key=index.get) for index in get_uploads(files)]`  
   `unified_index = []`  
   `for index in indices:`  
       `for el in index:`  
           `if el not in unified_index:`  
               `unified_index.append(el)`  
   `return dict(zip(unified_index,range(0,len(unified_index))))`

`def parse_tokens(tokens):`  
   `return [int(token) for token in tokens.split(",")]`  
`def Extract_thoughtforms_from_tokens(tokens):`  
   `tokens =parse_tokens(tokens)`  
   `indexes = set([(tokens.count(token) >= 2)*token for token in tokens])`  
   `indexes.discard(0)`  
   `return list(indexes)`

`def Calculate_strengths(tokens,file):`  
   `file_output = file.split(".")[0]+"_thoughtforms"+".json"`  
   `thoughtforms = Extract_thoughtforms_from_tokens(tokens)`  
   `if file_output not in os.listdir("uploads"):`  
       `thoughtforms_reference_index = dict(zip(range(0,len(thoughtforms)),thoughtforms))`  
       `open("uploads/"+file_output,"w").write(json.dumps(thoughtforms_reference_index))`  
   `return [tokens.count(str(thoughtform))/len(parse_tokens(tokens)) for thoughtform in thoughtforms]`

`def Extract_egregore_sets_from_tokens(tokens,file):`  
   `Strengths = Calculate_strengths(tokens,file)`  
   `Sequence = parse_tokens(tokens)`  
   `Distances = [len(Sequence)*strength for strength in Strengths]`  
   `Positions = json.load(open("uploads/"+file.split(".")[0]+"_thoughtforms"+".json","r"))`  
   `Ranges = [[math.floor(Positions[str(Distances.index(distance))]-distance),math.ceil(Positions[str(Distances.index(distance))]+distance)] for distance in Distances]`  
   `Egregore_sets = [[Sequence[el] for el in list(range(range_set[0],range_set[1]))] for range_set in Ranges]`  
   `return Egregore_sets`

`def remap_tensor_to_unified_index(tensor, old_index, unified_index):`  
   `"""`  
   *`Remap an egregore tensor from the old reference index into the unified reference index.`*

   *`tensor: list of strengths (length = len(old_index))`*  
   *`old_index: dict mapping token -> old_position`*  
   *`unified_index: dict mapping token -> unified_position`*

   *`returns: new tensor aligned to unified index`*  
   *`"""`*

   `# Create a new tensor full of zeros, sized to the unified index`  
   `new_tensor = [0] * len(unified_index)`

   `# Reverse old_index so we can map positions back to tokens`  
   `# old_index maps token -> pos, so we invert it to pos -> token`  
   `pos_to_token = {pos: token for token, pos in old_index.items()}`

   `# For each position in the old tensor`  
   `for old_pos, strength in enumerate(tensor):`

       `# Find which token this position corresponds to`  
       `token = pos_to_token.get(old_pos)`

       `# If the token exists in the unified index, remap it`  
       `if token in unified_index:`  
           `new_pos = unified_index[token]`  
           `new_tensor[new_pos] = strength`

   `return new_tensor`

`def Calculate_egregore_tensors(tokens,file):`  
   `Egregore_sets = Extract_egregore_sets_from_tokens(tokens,file)`  
   `Thoughtforms = [json.load(open("uploads/"+file.split(".")[0]+"_thoughtforms.json"))[str(el)] for el in list(range(0,len(Egregore_sets)))]`  
   `Sequence = parse_tokens(tokens)`  
   `for i, eg_set in enumerate(Egregore_sets):`  
       `tf = Thoughtforms[i]`  
       `if tf not in eg_set:`  
           `eg_set.insert(0, tf)`  
   `Strength_precursors = [[abs(set.index(Thoughtforms[Egregore_sets.index(set)])-set.index(el))*len(Sequence) for el in set] for set in Egregore_sets]`  
   `Strengths = []`  
   `for i, precursors in enumerate(Strength_precursors):`  
       `# Find the anchor position (where precursor == 0)`  
       `anchor_index = precursors.index(0)`

       `# Remove the zero so we don't divide by it`  
       `filtered = [p for p in precursors if p != 0]`

       `# Compute strengths for non-anchor tokens`  
       `strengths = [Sequence.count(Egregore_sets[i][precursors.index(p)]) / p for p in filtered]`

       `# Insert 0 back at the anchor position`  
       `strengths.insert(anchor_index, 0)`

       `Strengths.append(strengths)`  
   `return Strengths`

`def align_egregores_by_thoughtform(Egregores, Thoughtforms):`  
   `"""`  
   *`Convert list-based egregores into a dict mapping thoughtform -> tensor.`*  
   *`"""`*  
   `return {Thoughtforms[i]: Egregores[i] for i in range(len(Egregores))}`

`def Calculate_egregore_strength(tokens1, file1, tokens2, file2):`  
   `# Step 1: Compute egregore tensors for each text (using original indices)`  
   `E1 = Calculate_egregore_tensors(tokens1, file1)`  
   `E2 = Calculate_egregore_tensors(tokens2, file2)`

   `# Step 2: Load the original reference indices`  
   `idx1 = json.load(open("uploads/" + file1.split(".")[0] + ".json"))`  
   `idx2 = json.load(open("uploads/" + file2.split(".")[0] + ".json"))`

   `# Step 3: Load thoughtforms for each text`  
   `TF1 = json.load(open("uploads/" + file1.split(".")[0] + "_thoughtforms.json"))`  
   `TF2 = json.load(open("uploads/" + file2.split(".")[0] + "_thoughtforms.json"))`

   `# Convert thoughtform index->token into a list of tokens`  
   `TF1_list = [TF1[str(i)] for i in range(len(TF1))]`  
   `TF2_list = [TF2[str(i)] for i in range(len(TF2))]`

   `# Step 4: Align egregores by thoughtform`  
   `def align(E, TF_list):`  
       `return {TF_list[i]: E[i] for i in range(len(E))}`

   `E1_dict = align(E1, TF1_list)`  
   `E2_dict = align(E2, TF2_list)`

   `# Step 5: Find shared thoughtforms`  
   `shared = set(E1_dict.keys()) & set(E2_dict.keys())`  
   `if not shared:`  
       `return 0  # no shared thoughtforms → zero similarity`

   `# Step 6: Build unified reference index (runtime only)`  
   `unified_index = create_unified_reference_index([file1, file2])`

   `# Step 7: Remap tensors into unified index`  
   `def remap_tensor(tensor, old_index, unified_index):`  
       `new_tensor = [0] * len(unified_index)`  
       `pos_to_token = {pos: token for token, pos in old_index.items()}`  
       `for old_pos, strength in enumerate(tensor):`  
           `token = pos_to_token.get(old_pos)`  
           `if token in unified_index:`  
               `new_pos = unified_index[token]`  
               `new_tensor[new_pos] = strength`  
       `return new_tensor`

   `# Step 8: Compute dot products for each shared thoughtform`  
   `total = 0`  
   `for tf in shared:`  
       `t1 = remap_tensor(E1_dict[tf], idx1, unified_index)`  
       `t2 = remap_tensor(E2_dict[tf], idx2, unified_index)`  
       `total += np.dot(t1, t2)`

   `return total`

`def Extract_rference_index_from_text(text,file_name):`  
   `words = []`  
   `for word in text.split(" "):`  
       `if word not in words:`  
           `words.append(word)`  
   `open("uploads/"+file_name.split(".")[0]+".json","w").write(json.dumps(dict(zip(words,range(0,len(words))))))`

`def Extract_tokens_from_text(text,file_name):`  
   `if file_name.split(".")[0]+".json" not in os.listdir("uploads/"):`  
       `Extract_rference_index_from_text(text,file_name)`  
   `Reference_index = json.load(open("uploads/"+file_name.split(".")[0]+".json"))`  
   `Sequence = ",".join([str(Reference_index[word]) for word in text.split(" ")])`  
   `return Sequence`

`def Compare_texts(text,file_name,text_two,file_name_two):`  
   `return Calculate_egregore_strength(Extract_tokens_from_text(text,file_name),file_name,Extract_tokens_from_text(text_two,file_name_two),file_name_two)`

`text_one = open("text_one.txt",encoding="UTF8").read()`  
`text_two = open("text_two.txt",encoding="UTF8").read()`  
`print(Compare_texts(text_one, "text_one.txt", text_two, "text_two.txt"))`  
