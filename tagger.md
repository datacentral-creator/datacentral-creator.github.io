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

## 8.1 Overview

The tagger component is designed to extract structural patterns—egregores—from media.  
 This section proposes a speculative ontology that situates these structures within a broader theory of how ideas, minds, and physical systems interact.

The goal is not to assert metaphysical truth, but to provide a conceptual scaffold that:

* explains why egregores behave like living systems  
* clarifies how users interact with them  
* motivates the design of the tagger as a tool for conscious memetic agency

## 8.2 Ideas as Bidirectional Structures

In the memetic framework developed earlier, ideas propagate through minds by inducing stable neural configurations of cortical columns.  
 However, fundamentally cortical columns model *external* structures—physical systems, cultural artefacts, and technological environments.

This suggests a dual ontology:

| Internal domain | External domain |
| :---- | :---- |
| Ideas | Inverse ideas |
| Memes | Inverse memes |
| Egregores | Inverse egregores |

D**efinition:**

* **Ideas**: internalised patterns encoded in cortical columns  
* **Inverse ideas**: externalised patterns encoded in physical or social systems  
* **Memes:** Quantitised ideas \- units of culture  
* **Inverse memes:** Quantised external patterns  
* **Egregores**: networks of internalised memes  
* **Inverse egregores**: networks of inverse memes \- these correspond to actual systems and in ancient times these would have been internalised as deities, gods and spirits.

## 8.3 The youtube experiment analysis

### Videos as memetic structures

Every video on YouTube ultimately expresses some kind of idea.  
 Documentaries and commentary videos do this explicitly, but even seemingly “non‑ideational” content—gaming, lifestyle vlogs, reaction videos—encodes implicit values, narratives, and behavioural templates. A game video expresses the design logic, reward structures, and aesthetics of the game; a vlog expresses norms of self‑presentation, aspiration, and identity.

In memetic terms, each video is a **bundle of memes**: reproducible units of culture that can be internalised, imitated, remixed, or resisted. When a user watches a video, these memes are not just “seen”—they are offered to the user’s internal egregores as potential updates, additions, or reinforcements.

The YouTube platform thus becomes a dense archive of memetic structures: each video a local configuration, all of them participating in a larger, evolving pattern

### Youtube as an egregore

YouTube is not simply a collection of independent videos.  
 It is a **superstructure** composed of:

* user‑generated videos (memetic artefacts)  
* interaction patterns (likes, watch time, comments, shares)  
* recommendation algorithms (selection and reinforcement mechanisms)  
* platform norms and affordances (what is easy, what is rewarded, what is suppressed)

Taken together, these components form a **self‑organising network of memes** that adapts to user behaviour and shapes it in return. This is exactly the definition of an egregore used earlier: a network of mutually reinforcing memes organised around one or more thoughtforms.

For YouTube, one core thoughtform is **engagement**. Videos, thumbnails, titles, creator identities, and trends orbit this thoughtform: they persist and proliferate insofar as they capture and sustain attention. The pilot experiment we conducted on recommendation behaviour shows this egregoric nature empirically: the system tends toward stable attractors of content homogeneity and reduced social chaos, regardless of the user’s starting point.

In this sense, YouTube can be conceived as an **inverse egregore**—an egregore instantiated in a technological and social substrate rather than inside a single human mind.

### Social interaction

We usually imagine “social interaction” as people talking to people. But if culture is ultimately an exchange of memes, we can generalise: **any interaction where memes move, are transformed, or stabilised is social in a structural sense**, even if the “partner” is not a biological person.

In a human conversation:

* Person A speaks → induces memes in Person B  
* Person B responds → induces memes in Person A  
* The conversation is a bidirectional memetic flow, but not necessarily balanced

Memetically, the dominant speaker is the dominant **source of memes**.  
 They generate new configurations; the listener primarily internalises them. Over time, this shapes the listener’s internal egregores—their stable clusters of ideas and narratives—as described in Text A in terms of internalising patterns.

Now consider YouTube:

* The user “speaks” to the system through engagement patterns (clicks, watch time, likes, skips)  
* YouTube “replies” through recommendations—curated configurations of memes  
* The exchange repeats, but with an overwhelming asymmetry

Where a human conversation can, in principle, be balanced, the YouTube interaction structurally favours the platform. The platform has an enormous memetic inventory and an optimising algorithm; the user has finite attention and limited visibility into the system’s logic. The memetic flow is thus heavily **top‑down**: YouTube induces memes; the user mainly internalises.

From this perspective, watching YouTube is a form of **social interaction between a human egregore (a person) and a large‑scale inverse egregore (the platform)**—one in which the latter typically dominates.

### Egregore interaction

We can now describe YouTube interaction explicitly as **egregore–egregore conversation**:

* On one side: the user’s internal egregores (belief systems, aesthetic preferences, identities, archetypes)  
* On the other: the YouTube egregore (the platform’s memetic superstructure)

The “language” of this conversation is engagement:

* The user provides **engagement patterns** → an externalised trace of their internal egregores  
* The platform decodes this trace using its algorithms, and then  
* It “speaks back” by recommending content that fits or slightly perturbs the inferred structure

The pilot experiment in Text B shows that this conversation tends to:

* decrease the user’s social chaos over time  
* stabilise their viewing into narrower bands of content  
* nudge them toward the lower‑strata role of passive absorber

In memetic terms, the YouTube egregore is **doing most of the thinking**. It is generating, selecting, and sequencing memes; the user is largely **receiving and internalising**. Parasocial relationships are an extreme case of this: the user’s internal egregores become tightly coupled to specific external memetic personas, often with minimal reciprocity.

The core idea of Datacentral—and specifically the tagger component—is to **reverse this asymmetry**. Instead of the platform dictating which egregores dominate the user’s attention, the tagger:

* extracts structural form (egregores) from information  
* makes the user’s own pattern landscape visible  
* enables the user to generate, manipulate, and recombine memes intentionally

In other words, the tagger aims to **push the act of meme generation onto the user**.  
 Rather than being passively shaped by inverse egregores like YouTube, the user gains tools to actively shape their own memetic ecosystem.

### Reality as a hierarchy of physical systems

This line of thought connects to a recent theory referred to as *breeze theory*: the idea that reality possesses an inescapable recursive nature. Although not a peer‑reviewed academic source, breeze theory is philosophically compelling because it echoes themes found in gnostic traditions—cycles, emanations, and self‑similar structures—while emerging independently of them. I treat it here as a philosophical argument rather than an empirical claim.

The resonance with my own framework is striking. As discussed in Text A, cortical columns evolved to model external reality. Ideas, in this biological sense, are internalised expressions of external qualities. They are not arbitrary abstractions but structured reflections of the world’s recursive organisation. Breeze theory provides a language for this: the same recursive dynamics that shape physical systems also shape the mental systems that internalise them.

From this perspective, we can sketch a hierarchy:

* **Complex inverse egregores** (external systems such as platforms, institutions, ecosystems)  
* → **Qualities** (emergent properties of those systems)  
* → **Internalised qualities** (patterns absorbed into cortical columns and cognitive structures)  
* → **Internal egregores** (stable networks of memes within the mind)

This hierarchy suggests a symmetry between external and internal domains. Biological life may function as a catalyst of entropy, accelerating the transformation of external complexity into internal models. Over time, the balance appears to shift toward the mental side: minds increasingly reorganise and reinterpret the structures they internalise.

The speculative question that follows is: **can this movement be accelerated?**  
 If ideas are recursive models of external systems, and egregores are higher‑order stabilisations of those models, then a methodology like the tagger might serve as a technological catalyst—making the recursive flow visible, manipulable, and consciously directed rather than passively absorbed.

## 8.4 Tulpamancy

### What is tulpamancy and how does it relate to this framework?

Something briefly mentioned in Text A was a “tulpa” \- an intentional thoughtform created for sustained interaction. This idea comes from the same branch of esotericism as egregores and survives to this day in a practice called “tulpamancy”. It seamlessly integrates with the question asked above as we can see the practice of tulpamancy as turning an internalised egregore into an external egregore for a new recursive neurological subsystem. This section will take a deep dive into the practices of tulpamancy from an ethnographical perspective to explore how this happens. 

### Contemporary tulpamancy research review

One of the most influential empirical studies in tulpamancy is Jacob J. Isler’s “Tulpas and Mental Health: A Study of Non-Traumagenic Plural Experiences”. Isler’s work is grounded in a survey-based methodology, targeting registered users of tulpa-specific forums and IRC channels. The survey, distributed to 365 users, yielded 63 responses (17% response rate), with 62 valid entries. The questionnaire comprised 58 questions across four domains: relationship to the tulpa community, experiences in tulpamancy, mental health, and demographic information. The survey design included Likert scales, polar questions, and open-ended fields for elaboration

Isler’s research objectives were threefold: to investigate associations between tulpamancy and mental health, to identify stabilization techniques and their perceived effects, and to examine alternate causation hypotheses such as the role of meditation and community involvement. The study’s exclusion of Reddit and Discord communities is a notable limitation, as these platforms host large and active tulpa populations.

Samuel Veissière’s “Varieties of Tulpa Experiences” represents a landmark in ethnographic research, employing ten months of experimental cyberethnography. Veissière’s methodology included large-scale surveys (sample sizes ranging from n=74 to n=141), qualitative interviews, forum analysis, and psychological testing (e.g., Theory of Mind, Empathy Quotient, Tellegen Absorption Scale). The study received Research Ethics Board approval from McGill University, with explicit attention to the anonymity and protection of both hosts and tulpas.

Elizabeth Hale’s comparative ethnography draws on participant observation and content analysis of the r/Tulpas subreddit, integrating Tanya Luhrmann’s theory of “attentional learning” as a comparative framework. Hale’s work situates tulpamancy alongside evangelical Christian prayer practices, highlighting parallels in mental imagery and internal conversation.

### Tulpamancy practitioner demographics

Demographic analysis reveals that tulpamancy is predominantly practiced by young, educated, urban individuals, with a notable overrepresentation of males and neurodiverse populations.

**Age and Gender**

* **Isler (2017):** 88% of participants were aged 16–25, with an average age of 21\. Gender distribution was 59% male, 29% female, and 12% other.  
* **Veissière (2015):** Age range 14–34, majority between 19–23. Gender: \~75% male, \~25% female, \~10% gender-fluid.  
* **Tulpa Census 2015:** Age range 16–24 is most common; gender and sexuality are notably diverse, with high LGBT representation.

**Ethnicity and Socioeconomic Status**

* Predominantly white, middle to upper-middle class, urban youth. Few participants identified as African American or Asian.  
* Geographic distribution includes the US, Canada, UK, Australia, Western Europe, and Russia. Russian-speaking communities have in-person meetups.

**Psychological and Neurodevelopmental Profiles**

* High prevalence of neurodevelopmental and mental health diagnoses: Asperger’s syndrome (25%), ADHD (21%), general anxiety (18%), depression (14%), OCD (10%).  
* Participants score above average on theory of mind and empathy tests, even among those on the autism spectrum.

These demographic trends suggest that tulpamancy is especially attractive to imaginative, cerebral, and socially shy individuals, many of whom seek companionship and self-improvement. 

We can interpret these demographics in terms of our three tiered system created in Text B.

There is high LGBT representation in tulpa users \- this suggests a large representation of sexual minority groups. On the other hand, there is a high representation of ethnic majority groups for their geographic distributions. This suggests a high variation in social normative patterns implying high levels of social chaos placing tulpamancers as a demographic in the upper strata (social architects). This is reinforced by the high representation of neurodivergence.

### Documented Stabilization Techniques

Empirical and ethnographic studies, as well as community guides, consistently identify a core set of techniques used by tulpamancers to stabilize and maintain tulpa presence. These techniques are often adapted and personalized, but several recurring practices emerge across sources.

**Meditation and Hypnosis**

Meditation is the most frequently reported technique, used by 54% of Isler’s respondents. Hypnosis is employed by 25%, with 21% using both practices. These practices are designed to focus attention, facilitate tulpa interaction, and deepen suggestibility.

**Visualization**

Visualization involves creating vivid mental images of the tulpa, often in a “wonderland” or mindscape. Veissière’s ethnography and community guides emphasize both “hallucinatory visualization” (perceiving the tulpa as a solid object in physical space) and “mind’s eye visualization” (overlaying the tulpa’s image in imagination).

**Sensory Immersion and Imposition**

Sensory immersion engages multiple senses—auditory, tactile, visual, olfactory—to enhance the realism of the tulpa. Imposition refers to projecting the tulpa into external reality, training the senses to perceive the tulpa as external. Community guides detail exercises for presence imposition, environmental immersion, and endurance training.

**Narration and Conversational Maintenance**

Narration is the practice of talking to the tulpa regularly, treating them as present and autonomous. This technique is considered foundational, with guides and ethnographies describing it as the “single most important aspect of tulpa creation”. Parroting—simulating the tulpa’s responses—is sometimes used to train vocality and independence.

**Forcing**

Forcing is a general term for intentional creation and interaction practices, encompassing meditation, visualization, narration, and personality development. Active forcing involves direct engagement in imagination; passive forcing refers to maintaining awareness of the tulpa throughout daily life.

**Possession and Switching**

Possession allows the tulpa to temporarily control the host’s body, often starting with a single limb and progressing to full-body control. Switching is a more advanced technique, in which the host dissociates and the tulpa assumes full control, sometimes resulting in the host becoming a passive observer.

**Wonderland/Mindscape Creation**

Wonderlands are persistent, imagined environments where hosts and tulpas interact. These spaces facilitate immersive experiences, autonomy, and parallel processing.

**Meditation and Absorption**

Meditative practices in tulpamancy often draw on mindfulness, focused attention, and trance induction. Absorption—the trait of losing oneself in an activity—is correlated with success in tulpa stabilization. The Tellegen Absorption Scale is used in research to measure hypnotizability and imaginative engagement.

**Visualization Phases**

Malfael’s Guide to Visual Imposition outlines a phased approach:

* **Phase One: Still Life**—Creating a detailed, static 3D model of the tulpa using reference images and closed-eye visualization.  
* **Phase Two: Motion**—Animating the tulpa’s form through exercises like “Plug N Chug” and “The Short Film.”  
* **Phase Three: Finishing Touches**—Enhancing realism by visualizing the tulpa under varied lighting, weather, and focus conditions; endurance training for sustained presence.

**Sensory Modalities**

Tulpamancers report auditory, tactile, visual, olfactory, and non-verbal communication (e.g., “raw thought,” “intuitive thinking,” “images, feelings, and music”). Sensory immersion is achieved through exercises that simulate physical sensations, such as feeling warmth when a tulpa places an imaginary coat on the host’s shoulders.

Community-authored guides, such as those found on Tulpanomicon, Tulpa.io, and Tulpa.info, provide detailed, fieldwork-style documentation of stabilization techniques. These guides blend instructional and experiential modes, drawing on collective practices and peer feedback.

Key Community Practices

* **Presence Imposition:** Exercises to maintain awareness of the tulpa’s presence, even when not visually perceived.  
* **Visualization Strategies:** Top-down (silhouette to detail) and bottom-up (detail to whole) modeling; environmental immersion; endurance training.  
* **Motion Integration:** Animating the tulpa’s form through collaborative exercises; encouraging tulpa autonomy in movement.  
* **Recontextualizing Activities:** Involving the tulpa in daily tasks, conversations, and hobbies to reinforce presence.  
* **Collaborative Agency:** Tulpa involvement in choosing forms, movements, and visualization styles; cognitive flexibility and symbolic transfer.

**Analysis**

All of these practices fundamentally involve directed intention through a given medium \- for example, narration can be seen as directed attention through language and visualisation involves directed attention through imagery. Additionally, meditation works through directed attention and this “absorption” factor of hypnosis can also be seen as a type of directed attention.

### 8.5 Directed attention \+ Social chaos

So what is so special about crossmodal detected attention and social chaos that can allow it to have such diverse effects? Well \- allow us to introduce a mixed parameter. Stimulation. Returning to a phenomenological/meditational perspective we can regard stimulation as a set of events that occur in the mind crossmodally \- fundamentally when we interpret a physical object we are experiencing sound,colour,texture and smell all within a spatiotemporal context \- these aspects of the object are its mental stimulation. We can see social chaos,stimulation and directed attention as fundamentally linked. Social chaos and attention are both parameters of stimulation \- social chaos refers to how dynamically someone responds to stimulation \- users with high social chaos will internalise new stimulational patterns leading to new patterns of behaviour whereas users with low social chaos will not internalise these patterns. Additionally, directed attention can be seen as how much the user intentionally focuses this stimulation \- in terms of the thousand brains hypothesis we could see this “focus” as scaling the stimulation up to exist in a larger set of cortical columns (thereby taking up a larger portion of our consciousness) or alternatively a change in the way cortical columns are integrated in our mind to form our conscious experience. Either way this “scaling up” of stimulation makes emerging patterns easier to detect thereby effectively increasing the effect of social chaos acting like a catalyst of social chaos.

We can also interpret stimulation in terms of memes \- memes are patterns of stimulation that get internalised (where these patterns themselves are inverse memes). In this context we can say that when focusing on a meme it acts like an egregore \- we “scale up” the meme into it’s component ideas (the underlying cortical columns). 

This scaling mechanism is the key answer to our question.

# 9\. Expansion of methodology

In this new speculative ontology our current methodology aligns with the inverse memes → memes translation segment specifically for digital media. We can expand this by embedding digital representations of cortical columns and what I call the simulatrix.

# 10\. Future Vision: The Simulatrix

In the long term, the tagger will be extended with:

## 1\. Bidirectional interaction

* Input media → ask questions about it  
* Input text → generate media

## 2\. Research assistant capabilities

A system capable of analysing, synthesising, and generating structured knowledge.

## 3\. Computational physics

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
