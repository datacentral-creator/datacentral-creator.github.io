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

# 7\. Future Vision: The Simulatrix

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
