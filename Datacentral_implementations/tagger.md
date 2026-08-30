# Tagger Methodology  
*A unified framework for extracting form from information*

The tagger system is designed to answer a single question:

> **How can we extract *form* from information?**

It operationalises and improves upon the model developed in my [essay](../Research_and_philosophy/essay.md) where text is broken down into words which are replaced by numbers (and the map between the number and the word it represents is saved as a "Reference index"). We then turn this into a sequence of numbers and identify thoughtforms (recurring symbols) as cycles within the sequence. We then extract "Egregore sets" as a set of tokens around the thoughtforms and encode these egregore sets into tensors along with values that represent the strengths of the tokens in these sets (how related the token is to the set as a whole). This tensor then represents the form of the text as a whole. 

In the program Datacentral which the tagger component is a part of we can also decode the egregore sets back into text and highlight this text in the original media in order to create an automatic highlighting system saving these egregore sets as reusable objects within the program.

The methodology below describes the complete process.

---

# Methodology Overview

The tagger pipeline consists of six major stages:

1. **Tokenisation**  
2. **Motif (Thoughtform) Detection**  
3. **Strength Calculation**  
4. **Egregore Extraction**  
5. **Tensor Construction & Comparison**
6. **Reference index unification**
Each stage is described below.

---

# 1 Tokenisation

Tokenisation converts raw media into integer sequences.

## **Text (character‑level)**

The system uses **character‑level tokenisation**, not word‑level, because:

- it avoids fragmentation caused by punctuation,  
- it produces a small, universal reference index,  
- it allows motifs of arbitrary length to emerge naturally.
- it allows us to expand the procedure to images and videos in the future using pixel values as tokens

Procedure:

1. Build a reference index mapping each unique character → token ID.  
2. Convert the text into a sequence of token IDs.

This produces a reversible, language‑agnostic representation.

You can see a python implementation of this [here](./Encoding.py).

---

# 2 Motif (Thoughtform) Detection

A **thoughtform** is defined as a **repeated motif**: a substring that appears at least twice.

To detect motifs efficiently, the system uses the following procedure

1. Build a suffix automaton over the encoded data (represents the token sequence efficently)
2. Go through the encoded sequence token by token and find the shortest length between the token and itself. If this value is greater than or equal to 2 the token is a thoughtform.
3. Build a new reference index for thoughtforms

We then append this new reference index to a list of reference indexes and encode the data again using this reference index applying this step again to the newly encoded data repeatedly until no new thoughtforms can be found. This captures thoughtforms of any length. 

---

# 3 Strength Calculation

Each thoughtform receives a **strength score** based on:

- how often it appears (frequency),  
- how tightly clustered its occurrences are (average return distance),  
- and the length of the sequence.

The formula:

```
strength = frequency / (sequence_length × average_return_distance)
```

Interpretation:

- High strength → frequent, tightly clustered motifs  
- Low strength → rare or widely spaced motifs  

This ranking determines which motifs act as meaningful anchors.

---

# 4 Egregore Extraction

An **egregore** is the contextual neighbourhood around a thoughtform.

Procedure:

1. For each thoughtform, compute its strength.  
2. Convert strength into a **distance threshold**:

```
distance = sequence_length × strength
```

3. For each occurrence of the thoughtform:
   - extract all tokens within ±distance  
   - merge these windows into an egregore set

This yields a set of token sequences representing the motif’s structural neighbourhood.

---

# 5 Tensor Representation

Each egregore is embedded as a **tensor**:

- The tensor has one dimension per token in the **unified reference index**.  
- Each value encodes the correlation strength between the anchor thoughtform and that token.

This produces a high‑dimensional representation of the egregore’s structure.

---

# 6 Reference Index Unification

To compare egregores across files:

1. Convert each file’s reference index into an ordered list.  
2. Merge all lists into a **unified index**.  
3. Remap each tensor into this unified coordinate system.

This ensures tensors from different media are directly comparable.

---

# 7 Comparing Media

To compare two files:

1. Extract their egregore tensors.  
2. Normalise them to the unified reference index.  
3. Compute similarity using the **dot product**.  
4. Rank files by similarity.

This allows cross‑media comparison of structural patterns.

You can find the python code for the updates to this pipeline (the move to suffix automatons) [here](./Improved_model.py).
---

# 8 Lessons from Early Attempts

### **Word‑level tokenisation failed**  
Whitespace splitting introduced noise and fragmented cycles.

### **Character‑level tokenisation fixed this**  
But introduced accidental overlaps (e.g., “practice” vs “malpractice”).

### **Iterative suffix automaton thoughtform detection and encoding solves both of these problems**  
Tokens can represent whatever is meaningful within the data. It also allows you to make the data highly compressed which is efficient for transmitting the data between machines and allows you to transmit data in an encrypted format assuming both parties have access to the reference indexes.

---

# 8. Final Architecture

The final tagger pipeline is:

1. **Tokenise** (character → integer)  
2. **Build suffix array**  
3. **Extract motifs (thoughtforms)**  
4. **Compute strengths**  
5. **Extract egregores**  
6. **Construct tensors**  
7. **Unify reference indices**  
8. **Compare via dot product**

This system generalises across text, images, and video, enabling a unified theory of structural pattern extraction.


