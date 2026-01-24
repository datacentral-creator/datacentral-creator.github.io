**Navigation:**  
[Research](index.md) | [Datacentral](https://github.com/datacentral-creator/Datacentral) | [History](history.md)

# Precursor knowledge

* The “tagger component” is a program which implemented a methodology to extract egregores (clusters of memes (units of culture)) from text  
* My “speculative ontology” proposes that information follows the flow inverse egregores (systems that can be internalised as egregores) → Reverse ideas (qualities that emerge from systems \- can be internalised as ideas)/Reverse memes(similar to reverse ideas except these are specifically internalised as memes) → Ideas/Memes → Egregores  
* My “historical reference point” laid out the history of human meaning making where originally symbolic language arose in humans where symbols allowed humans to create complex cooperative strategies where symbols were associated with “moralities”(patterns of symbol enforcement). This became more complex over time creating a mode of early human being where we experienced the world through stories and external agents \- for example rocks were active participants in our world just like us however as symbols became more abstract eventually symbols began to describe other symbols creating the foundations of logic and philosophical thought. 

# Grounding the tagger component in historical context and our speculative ontology

## Introduction

Currently our tagger operates in the section of inverse ideas → memes. The idea of simulatrix is to expand the domain of our tagger to the full domain of our speculative ontology allowing it to act as a physics assistant.

In our historical reference point our tagger is operating on the level of symbolic language. 

Before describing the methodology, the following terms are essential:  
\- **Token**: A basic unit of information (word, pixel value, video frame value).  
\- **Thoughtform**: A token that participates in a cycle—a repeated pattern within a token graph.  
\- **Egregore**: A network of memes (tokens) organised around a thoughtform, defined by recurrence strength.  
\- **Anchor**: The thoughtform around which an egregore tensor is constructed.  
\- **Tensor**: A vector‑like representation encoding the strengths of relationships between a thoughtform and other tokens.  
\- **Reference Index**: A mapping between raw symbols and token numbers.

The tagger pipeline consists of five major stages

## Tokenisation

The first step is to convert raw media into a sequence of tokens.

1. Construct a reference index:  
    A dictionary mapping each unique word to the order of its first appearance.  
2. Convert the text into a sequence of words.  
3. Map each word to its corresponding number.  
    The text becomes a list of integers.

## Graph Construction

Tokens are arranged into graphs that reflect the structure of the medium.

IE for text:

1 → 3 → 5 → 7

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

## Strength Calculation

For each thoughtform, compute its **strength**:

Strength \= frequency/(sequence length \* average return distance)

Where:

* **frequency** \= number of occurrences  
* **sequence length** \= length of the cycle sequence  
* **average return distance** \= average number of tokens between recurrences

Example for token `3` in `3 → 6 → 3`:

Strength \= 2/(3\*2) \= ⅓ 

## Egregore sets and egregore tensors

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

Each egregore is represented as a **tensor** anchored on its thoughtform.

* Each tensor dimension corresponds to a token in the **unified reference index**.  
* Each value corresponds to the **strength** of that token’s correlation with the anchor.

To compare egregores across files, all tensors must use the same token ordering.

Procedure:

1. Convert each reference index into an ordered list of symbols.  
2. Merge all lists into a unified index, removing duplicates.  
3. Remap all tensors from their original indices into the unified index.

This ensures consistent tensor alignment.

## Comparing media

To compare two files:

1. Extract their egregore tensors.  
2. Normalise them to the unified reference index.  
3. Compute similarity using the **dot product** of corresponding tensors.  
4. Rank files by similarity.

## Reinterpreting the methodology

We can reinterpret our egregore sets.

* Anchoring thoughtform can be thought of as symbols  
* The egregore set can be thought of as patterns reinforcing the symbol(moralities)  
* Strengths are the values of the agency we assign the symbols 

# Expanding the tagger component 

## Mythemes

In my historical reference point, I concluded that mythemes (units of myths) manage memes. To add this to the methodology we can consider the “context” of an egregore set as the words around it. We can consider this to be a set of the tokens such that the strength of the token obeys the condition a \< s \< b where s is the strength and a is 1.5 times the interquartile range below the lower quartile of the egregore tensor (divided by the strength of the anchoring thoughtform with itself) and b is 1.5 times the interquartile range above the upper quartile of the egregore tensor (divided by the strength of the anchoring thoughtform by itself). The IQR method is used because anomalies are defined as values more than 1.5×IQR from the quartiles. This allows us to define the ‘normal’ context of an egregore as all non‑anomalous tokens.”

Mythemes now become patterns in the relationship between the context and the egregore.

Standard practice would be to use something called a neural network to learn patterns.  
A neural network is a network of neurons as the names suggest.   
Here I’m talking about computational neurons. These model biological neurons using just weights and biases which are collectively called “parameters”.  
Neurons take the input state (which is between 0 and 1), multiply it by a weight and add a bias then put it in an activation which maps it to a number between 0 and 1 allowing it to be passed to another neuron. They also consist of an error feedback which updates the weights and biases to learn patterns in data.

Large Language Models use vectors representing the semantics of words as states however this won’t work for our architecture as we’re not working on the level of morphemes but memes and mythemes. 

Additionally Large Language Models are large models meaning they are computationally heavy which isn't suitable for my architecture. 

Ultimately neuronal networks internalise change so it might make sense to look at change from first principles. 

Elemental systems arose all across the world to describe change however the one I am personally most familiar with is 五行(wu xing) which translates literally to the “five movements” however it is meant as in the “five phases” (or five elements) \- these elements are 木(wood),火(fire),土(earth),金(metal),水(water). These elements are very symbolic in chinese culture forming the foundation of traditional chinese medicine but what they actually represent is the movement of a force the chinese called 氣(qi) which they thought of as a kind of fundamental animating force similar to the “breath of God” in the bible (funnily enough in a literal sense the character 氣 does mean “breath” or “gas”) or what the romans called “numen”(spirit associated with certain geographical regions and burial sites). Just as we did previously with the idea of “egregores” we can abstract these to simply represent states of change. If we use the “generative cycle” we can say the cycle of 氣 is 木 → 火 → 土 → 金 → 水 and this does in fact correspond to the seasons in traditional Chinese thought. If you think about them in terms of what they represent if you have a state 木 represents the initial conditions of that state. At 木 we could say the derivative of the state x(the rate of change of x represented by d/dx ) is 0 and the second derivative of x (the rate of change of d/dx represented by d^2/dx^2) is greater than 0\. We can say that the rate of change of x is 0 because this point is a minimum. We can then say that 火fundamentally represents a state where the rate of change is increasing very quickly \- fire is quite literally the element of change so we can say that d/dx \> 0\. This is the reason the second derivative was positive at 木 \- as you travel from d/dx \= 0 to d/dx \> 0 d/dx must be increasing therefore at 木 the rate of change of d/dx must be greater than 0 and we can say that d^2/dx^2 \> 0\. Now for 土 it makes sense that d/dx \> 0 because d^2/dx^2 \> 0 at 火 however at this point d^2/dx^2 \<0 because d/dx \= 0 at the next point in our cycle since we will be half way through the cycle meaning this point will be the maximum distance from 木 in our circle so it is by definition our local maximum. Now at 金 as I have just explained d/dx \= 0 but due to the start in the change in x d^2/dx^2 \<0 then at 水 we get that d/dx \< 0 and d^2/dx^2 is less than 0 to bring us back to our original state. This makes sense intuitively if you think of our state X as heat then this system is fundamentally describing the seasons. 

Ultimately though, the elements may not necessarily be balanced and when this happens the final state might not be equal to the original for instance if the 火 stage overacts the trajectory might overshoot or if 水 overacts the trajectory might undershoot (or alternatively if 土 or 金 underacts). If we imagine many of these cycles in sequence, if this happens consistently it will create chaos \- that is; a system that is sensitive to initial conditions.

In terms of computational modelling this system is replicated very well by the neuron. If we look at the computational model of a neuron you have a state x which is between 0 and 1 and each neuron multiplies that state by some number called a weight which can act as 火 amplifying the signal or 水 reducing the signal, we then add a bias which effectively counteracts the offshoot and put it in an activation function which acts as 金 or 土 stabilising the signal (it maps the number to a number between 0 and 1 allowing it to be used as the input of the next neuron).

The question is \- is this the best way to do this?  
Firstly we need to determine how to change this to work with forms. Luckily there is a current solution using frontier technology.

As I brusquely mentioned something like 1 → 3 → 5 → 7 is a graph. This is because it contains nodes (numbers) and edges (arrows). Each edge connects two nodes to form a network. Just like there are graphs there are also hypergraphs. A hypergraph is similar to a graph except instead of having edges it has hyperedges. Any one hyperedge can connect any given number of vertices. Hypergraphs are used to encode higher order structures of meaning, for example the wolfram project uses hypergraphs to represent the universe where physical laws are represented by updates of the hypergraph. The wolfram project remains speculative but has begun to represent general relativity and quantum mechanics. 

It would definitely be possible to represent our data in a hypergraph.

Hypergraph based transformers are a frontier technology. Transformers are architectures that use neural networks and an attention mechanism that allow the neural network to use context as well as just the current state. Hypergraph based transformers use hypergraphs as the actual data they are using to learn. 

In hypergraph neural networks, hypergraphs are represented using an incidence matrix which is a matrix that looks like this:  
\[ …. \]  
\[ …. \]  
\[ ….\]  
….  
Where each column (section going down) is a hyperedge and the elements are vertices.  
Representing our data so far with a hypergraph is very useful as it allows us to isolate our data in terms of our reference indexes as well as connect multiple levels of abstraction (each egregore tensor is effectively one hyperedge connected to an anchoring thoughtform but we can also connect the original graph sequence).

They then apply a learnable weight matrix (which multiplies every element in the matrix by another element) and a learnable bias matrix (which adds biases to each element in the matrix) in order to transform the hypergraph.

In this case the nodes of the hypergraph are the actual states.

The transformations of the hypergraph we want are effectively **patterns** and **antipatterns** where **patterns** are effectively how the context changes an egregore tensor. An antipattern would be a new egregore tensor where we want the mythemes (pattern behaviours) to now act on these new egregore tensors. Ideally this would mean we could have say a text file and a prompt where we ask about the text file and it could “answer”. 

This will express the original layer of my historical reference point where the algorithm is “participating in a lived reality”. 

Here is my proposition that synthesises all of this information:

* Use waves to represent the form of the hypergraph  
* Use a fourier transform to decompose this wave into their components which we can save   
* We can combine these with antipatterns to transform the hypergraph of an antipattern achieving the desired result

Waves make sense because:

* Waves are composed of sine waves and cosine waves  
* The derivative of sine is cosine and the derivative of cosine is \-sine  
* This means the second derivative of sine is \-sine and the second derivative of cosine is \-cosine  
* This is a special property because it means that when df/dx \> 0, d^2f/dx^2 \< 0 and when df/dx \<0, d^2f/dx^2 \> 0 by definition satisfying our elemental phases system  
* Additionally, whereas neurons are dependent on the scale of the system (a larger scale system needs more neurons as there will be more inputs) waves are scale free plus much less calculations are needed (matrix multiplication etc is computationally expensive whereas a fourier transform is only one calculation).

Luckily there is already a hypergraph fourier transform which does this for us.

# Future Vision

* In the long term, the tagger will be extended with:  
  * Bidirectional interaction  
  * Input media → ask questions about it  
  * Input text → generate media  
* Research assistant capabilities  
  * A system capable of analysing, synthesising, and generating structured knowledge.  
  * Computational physics  
* A speculative goal: using structural extraction to identify patterns in physical systems.
