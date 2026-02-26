**Navigation:**  
[Research](../index.md) | [Datacentral](https://github.com/datacentral-creator/Datacentral) | [History](../History/history.md)


# Preliminary research

This article is a part of a series of research and draws upon details from other articles. This section summarises those details.  
In my essay “Are ideas alive? How historical civilisations were governed by ideas” I discuss replicators \- patterns that form themselves in their environment. These were believed to be the precursors to biological life. Memes are ideological replicators and I argued that to that extent they can be considered alive. I also mentioned how interpretation is a directional process where the mind interprets the stimulus but the stimulus also updates the way the mind interacts with the environment. I also synthesised the idea of thoughtforms (self reinforcing ideas) and egregores (networks of thoughtforms) and introduced a methodology to tokenise text and extract thoughtforms and egregores from these tokens.

In “How do recommendation algorithms affect the formation of culture” I performed an experiment to analyse the effect of youtube’s recommendation algorithm on the parameter of social chaos (behavioural variance) and it created a stratified system as follows:

Individuals positioned above the top critical point exhibit extremely high levels of social chaos, where their exposure to diverse and rapidly changing digital content induces a state of cognitive overload. Drawing on Goffman’s (1959) concept of dramaturgy, these users perform multiple, often conflicting social roles simultaneously. This divergent role behavior results in high "role entropy" (as discussed by Prigogine, 1984), where predictable patterns break down and novel cultural expressions emerge. In this stratum, the individuals—I will term “cultural architects”—synthesize new memes by navigating and even exploiting the boundaries of algorithmically driven content recommendations. 

The majority of users occupy the middle strata, falling between the top and bottom critical points. Here, the influence of cultural architects is evident: individuals in this layer are able to access, maintain, and propagate the new cultural ideas generated in the upper strata. Their behavior is characterized by a moderate level of role entropy—less volatile than that of the cultural architects, yet sufficiently dynamic to facilitate a cascading diffusion of novel cultural forms. As these users share and reinforce emerging memes, they effectively transform radical ideas into mainstream trends, thereby shaping what is considered culturally acceptable.These individuals engage with the memes, sharing, remixing, and adapting them. They act as intermediaries, spreading the ideas beyond the original niche.

Individuals below the bottom critical point are primarily passive absorbers of culture. Their behavior is marked by a convergence around a stable, predictable set of social roles—NPCs as mentioned in our introduction. In our analysis, these users resist rapid cultural change, functioning as anchors that moderate the influx of new, rapidly evolving cultural content. Their role is crucial in filtering which emergent cultural movements persist over time, thereby ensuring long-term stability within the broader social system.The broader public, which internalizes these memes without necessarily contributing to their evolution.

It was found that there was a pull towards the lowest strata such that the further away from the lowest strata you are the stronger the pull is. 

In my “speculative ontological framework” document I emphasised how just as we conceive of ideas,memes and egregores these are all internalisations of parameters external to our mind \- these parameters can be thought of as “inverse ideas”,”inverse memes” and “inverse egregores”.

I interpreted my experiment within this ontology and found that the youtube recommendation algorithm itself acts as a “inverse egregore” and just like how we can have conversations between people which are effectively interactions between egregores we can have conversations with youtube which is an interaction between an egregore and a reverse egregore and the language of this exchange is engagement metrics. Just like how in a human-human conversation one person can tend to dominate the person and it is this person who is inducing memes in the other person, the power balance in the conversation between the users egregore and youtube’s reverse egregore is determined by their social chaos strata.

I also performed a case study of tulpamancy \- a practice where users can create “tulpas” \- symbols that become alive through sustained conscious interaction, even creating new consciousnesses or “alters” in the user's head. 

In my “historical reference point” document I found that symbolic language evolved in humans as a way to facilitate cooperation in evolutionary strategies however it evolved alongside a precursor to morality which is required to enforce these symbols

Humans are psychologically predisposed to assign agency and/or spiritual significance to external actors (inverse ideas and inverse egregores) \- this results in early practices like animism, shamanism and totemism

I therefore suggested that 

Animistic agents arose from assigning spiritual significance/agency to abstract symbols which come with an associated morality forming the foundation of religion. Alternatively we could say that religion arose as a way to enforce and interact with abstract symbols. Additionally totems (physical iterations of abstract symbols) amplify group cohesion and group identity. 

Where a “morality” is a behaviour enforced by a group. 

I also discussed how ritual is used to immerse us in this symbolic world. We can see it as a hierarchy with language and on this layer is memes then on the layer above is mythology with mythemes and symbols exist between these two layers like vessels. In ancient times symbols would have been used sparsely emerging when necessary as described however in the modern world we engage with symbols continuously \- in spoken communication for example, we often use metaphors and similes sometimes such that our metaphorical language can sometimes blend with our literal perception of reality. An example of this is people saying or brains our “like computers” \- eventually people started to say our brains our computers and now people can interpret this literally without thinking about it \- not in the sense that our brain has the same form as how we would imagine a computer, for example a laptop but in the sense that properties of a computer must necessarily apply to our brains. In this sense mythemes are fundamentally ingrained in our modern perception of reality.

I then observed a trend across cultures where increasingly self referential symbols cause a transition to philosophy and a shift in thought from mythos (experienced reality) to logos (Constructed reality). 

I also introduced a methodology to extract egregores from text.

Before describing the methodology, the following terms are essential:  
\- **Token**: A basic unit of information (word, pixel value, video frame value).  
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

# Introduction

This document is to act as a successor to my other documents in the series acting as a comprehensive analysis of the methodology of semantic processing in intelligent systems and simultaneously offering a computational implementation.

# Case Study 1: Tulpamancy further analysis

In our tulpamancy case study we found that focused social chaos can be used to create tulpas. This suggests that social chaos itself may be more than a constructed parameter for sociological analysis. Additionally we have the question: What class of “thing” is a tulpa? Here we are to exhibit high levels of discretion as to not assert unfounded metaphysical claims. We know that tulpas are things that are experienced by many people independently so we can classify them as a type of conscious experience. 

This anchors us in the realm of the psychological, prompting us to analyse social chaos in this way. We can consider that users who engage in tulpamancy have high levels of social chaos: as we know from our preceding research this suggests that they are fundamentally **creators** \- these are the people that **create** memes and new forms of culture.

Linking into my analysis of the way “conversations” are egregore/egregore or egregore/inverse egregore interactions we can argue that social chaos is a descriptor of a user's position in the hierarchy of this conversation \- the higher a user's social chaos, the more dominant they are in this interaction meaning that memes are consistently “coming out” of the users mind. 

Leveraging our pre-existing ideas we can recall that interpretation is the mechanism of ideological replication. This suggests that high social chaos users are the ones doing the interpretation of stimulus in this “conversation” and lower social chaos users are the ones using these interpretations. 

So tulpas are really attention directed at interpretation mechanisms. In my original essay “Are ideas alive? How historical civilisations were governed by ideas \- Essay” the interpretation mechanism is contextualised as something that controls the user and ultimately creates history by reorganising archetypes (and later mythemes) to create new social narratives (mythos experiences) however perhaps in tulpamancy social chaos and focus are used to reverse the direction of this process allowing users to construct mythemes intentionally using high levels of focus (these mythemes being tulpas) \- extracting form.

Thus we can consider our brain as an environment in which ideas are created where social chaos is the mutation rate and focus is the rate of replication.

We can consider interpretation as a kind of embedded computation. This is relevant because there have been experiments into embedded computation in the context of computational life. I selected the article “Computational Life: How Well-formed, Self-replicating Programs Emerge from Simple Interaction” to act as a bridge between the world of interpretation and computation using the idea of replicators in a computational context. The paper notes how in their experiment replicators form from implicit competition for computational resources in programs with self-modification. 

In these experiments, programs are randomly generated strings which execute themselves, changing their own contents. 

It reflects the relationship between replicators and embedded computation. A computation is defined as “any type of arithmetic or non-arithmetic calculation that is well-defined” where a statement is “well defined” if it can be translated into a Turing machine. Embedded computation is a computation that is a subcomputation of another computation. Autocatalytic processes are ultimately expressions of recurring embedded computation and replicators are ultimately competitive autocatalytic processes.

In terms of datacentral then, we will want to interact with our extracted egregores inside of embedded computation to create “form”, we will want the user to be doing the interpreting of form to maintain a healthy balance of social chaos and prevent the algorithm from dominating the conversation of social chaos as many traditional algorithms have done as previously discussed.

# Logos vs mythos in the current day

Mythos still play a large role in the current day. Even right now, we still participate in mythemes \- in today's world these are our collaborative social narratives and this is the layer of our perception that is felt. An example of this might be brands or the narrative of effectively “Go to school, get a job, buy a house, start a family, retire, enjoy retirement and die”. In this way we can also see how meaning is created on large social scales and people who fail to conform to this mytheme are labelled as “weird”/”weirdos”.   
In terms of actual argumentative for this we create a circular loop- these modern mythemes are social egregores. Mythos is the layer of our perception in which our ideas are “living” referring back to my first essay “Are ideas alive?How historical civilisations were governed by ideas” in a perfect loop. 

Logos also continues to exist in modern life. In modern life, logos presents itself as logical reasoning and often manifests itself through our internal monologue. We could argue that intelligent individuals experience a larger proportion of logos compared to mythos (as per the conventional understanding of intelligence). This is why studies show there seems to be a correlation between intelligence and depression \- as individuals experience a higher proportion of Logos they become detached from lived/felt reality and by extension detached from meaning. 

In terms of our computational framework, we can view mythos and logos as relating to two different types of logic. In Mythos, symbols are related by a loose type of logic I’ll call a “type A” logic (mythemes). This type of logic can be represented by non-terminating Turing machines \- it is narrative/descriptive and non computational. This would explain why people who only experience mythos experience a narrative based reality. We can also consider a second type of logic \- a “Type B” logic. We can say that this kind of logic is expressed by terminating turing machines and is computational. We can argue that logos is a kind of system where symbols are related by a Type B logic \- computation can be performed on them. We can argue that humans transitioned from mythos to logos as symbols became increasingly abstract \- perhaps when this happened the logic connecting these symbols \- the “mythological syntax” became computational. It would make sense for a logic that is computational to already exist in our brain because ultimately the initial purpose of ideas would have been to generate an action that would increase our chance of survival and this action generation would have been a form of computation so perhaps mythemes entered deeper levels of the human psyche bringing out this kind of logic. Ultimately the goal of datacentral then will be to extract egregores and construct these logics between the egregores allowing users to construct systems. We can do this by interacting with the logic or mapping the logic to different states. 

We can also say that type A logic is the “pure meaning” of a symbol. 

# Case study 2: Psychonetics

Psychonetics, similar to datacentral, is focused on extracting form from data. Psychonetics was also proposed as a technology, in the same way as datacentral meaning that it can be used to do a certain thing but not provide explanations for why things are that way. The main techniques of psychonetics are remarkably similar to tulpamancy. Coming directly from the book: “Psychonetics: A methodology to work with the mind and perception” the main sets of techniques in psychonetics are will meditation, working with perceptual uncertainties, working with attention and working with pure meanings. Will meditation is an exercise where the user meditates using the mantras “I am” and “I am will”. The user is supposed to focus entirely on these two mantras similar to the concept of “wonderland” in tulpamancy \- both spaces of extreme focus. The utility of these two mantras is for the user to associate their sense of self with “will” \- specifically the idea of will in abstract dissociated from any specific goal. This “will” is then used in other techniques where the user works with some concept such as attention to allow the user to demonstrate complete control over that aspect of their conscious experience. This ultimately allows users to operate in terms of pure meanings \- semantics themselves devoid of any kind of expression.

Additionally, we can see will meditation as the user seeding their mind with a thoughtform (in the form of a mantra) then using an attention to rapidly replicate that thoughtform and analyse it thoroughly. This insight will be useful to datacentral. 

# Pipelines

Both tulpamancy and psychonetics can be considered methodologies or technologies on the mind (psychotechnology \- where the term psychonetics comes from). Technologies can be thought of as fundamentally having a set of input parameters and a set of output parameters \- even something like a pen, for example the input parameter of a pen might be the pressure on the pen and the output might be the texture of the ink (IE more pressure \= darker ink). In both tulpamancy and psychonetics the fundamental input unit is a thoughtform. If we consider a thoughtform as a recurring token then in psychonetics the token is an entity in some field IE the visual, auditory or somatic field and in tulpamancy the tokens are morphemes and the goal is to create a tulpa, which in turn can be thought of as a technology where the input parameter is a morpheme thoughtform. In datacentral, a technology where the input parameter and output parameter are both thoughtforms is called a pipeline. Datacentral is fundamentally a combination of pipelines. The purpose of the analysis then is to determine fundamental properties of a pipeline for the construction of datacentral. In this case the properties so far would be that pipelines should empower the social chaos of the users not diminish it and the pipeline should ultimately construct the logic of the tokens (type A or type B type logic) and perform some operation on that logic as the output. 

# Patterns and antipatterns

The transformations we want to perform on a hypergraph fall into two categories:

* **Patterns**: The patterns in the data \- these are the constructed logic.  
* **Antipatterns**: These are effectively patterns that fit the data \- intuitively, we can think of this as being like an enzyme and a substrate in biology where the enzyme changes shape to fit the shape of the substrate exactly then transform the substrate into a new form. An antipattern could be something like a prompt (the substrate) that is transformed by the pattern to produce a meaningful output. 

# States and Objects

Data can be classified as either a state or an object. State data represents something quantifiable whereas object data represents discrete things with some kind of correlation.

Standard practice would be to use something called a neural network to learn patterns however this only works for state data. A neural network is a network of neurons as the names suggest.These neurons are computational neurons, models of biological neurons which use weights and biases (collectively called “parameters”). Neurons take the input state (which is between 0 and 1), multiply it by a weight and add a bias then put it in an activation function which maps this quantity to a number between 0 and 1 allowing it to be passed to another neuron. They also consist of an error feedback mechanism which updates the weights and biases to effectively “learn” mappings between inputs and outputs allowing for advanced pattern recognition and recreation. Large Language Models use vectors representing the semantics of words as states however this won’t work for datacentral as we operate on the level of mythemes/egregores not morphemes \- relationships between individual linguistic elements hold no significance on the forms of the text. Additionally, datacentral operates on tokens not raw text.

This forces us to think about patterns more generally, bringing us to the idea of change. Change is a universal theme in ancient cultures and in these cultures, elemental systems where elements act as symbols that allow the type B logic of the system to make actionable computations regarding change. The elemental system I am personally most familiar with is 五行(wu xing) which translates literally to the “five movements” however it is meant as in the “five phases” (or five elements) \- these elements are 木(wood),火(fire),土(earth),金(metal),水(water). These elements are very symbolic in chinese culture forming the foundation of traditional chinese medicine but what they actually represent is the movement of a force the chinese called 氣(qi) which they thought of as a kind of fundamental animating force similar to the “breath of God” in the bible (funnily enough in a literal sense the character 氣 does mean “breath” or “gas”) or what the Romans called “numen”(spirit associated with certain geographical regions and burial sites). Just as we did previously with the idea of “egregores” we can abstract these to simply represent states of change. If we use the “generative cycle” we can say the cycle of 氣 is 木 → 火 → 土 → 金 → 水 and this does in fact correspond to the seasons in traditional Chinese thought. If you think about them in terms of what they represent, 木 represents the initial conditions of a given state state. At 木 we could say the derivative of the state x(the rate of change of x represented by d/dx ) is 0 and the second derivative of x (the rate of change of d/dx represented by d^2/dx^2) is greater than 0\. We can say that the rate of change of x is 0 because this point is a minimum. We can then say that 火fundamentally represents a state where the rate of change is increasing very quickly \- fire is quite literally the element of change so we can say that d/dx \> 0\. This is the reason the second derivative was positive at 木 \- as you travel from d/dx \= 0 to d/dx \> 0 d/dx must be increasing therefore at 木 the rate of change of d/dx must be greater than 0 and we can say that d^2/dx^2 \> 0\. Now for 土 it makes sense that d/dx \> 0 because d^2/dx^2 \> 0 at 火 however at this point d^2/dx^2 \<0 because d/dx \= 0 at the next point in our cycle since we will be half way through the cycle meaning this point will be the maximum distance from 木 in our circle so it is by definition our local maximum. Now at 金 as I have just explained d/dx \= 0 but due to the start in the change in x d^2/dx^2 \<0 then at 水 we get that d/dx \< 0 and d^2/dx^2 is less than 0 to bring us back to our original state. This makes sense intuitively if you think of our state X as heat then this system is fundamentally describing the seasons. 

Ultimately though, the elements may not necessarily be balanced and when this happens the final state might not be equal to the original for instance if the 火 stage overacts the trajectory might overshoot or if 水 overacts the trajectory might undershoot (or alternatively if 土 or 金 underacts). If we imagine many of these cycles in sequence, if this happens consistently it will create chaos \- that is; a system that is sensitive to initial conditions.

In terms of computational modelling this system is replicated very well by the neuron. If we look at the computational model of a neuron you have a state x which is between 0 and 1 and each neuron multiplies that state by some number called a weight which can act as 火 amplifying the signal or 水 reducing the signal, we then add a bias which effectively counteracts the offshoot and put it in an activation function which acts as 金 or 土 stabilising the signal (it maps the number to a number between 0 and 1 allowing it to be used as the input of the next neuron).

The task is to create another implementation of this system in a way that can act on objects as well as states, effectively building a type A logic for these symbols of change.

The problem is that a token is fundamentally both a state and an object. A token is a number in the sense that it is represented by a digit however it can not be considered a number in the fact that there is no meaningful association between token 5 and token 6 \- it is just the order they appeared, so implicit syntax on quantities even such as counting can’t be considered meaningful. Because of this, we couldn’t train a neural network on these tokens since the concept of multiplying a token or adding to it doesn’t have meaning. A token can be considered an object, because ultimately in the way that tokens were just described they are discrete objects and they have relationships in the context of thoughtform strength. 

Ultimately our extracted egregores and egregore strengths act as a naive implementation of a type A logic ignoring syntax, languages native implementation of type A logic. This is because syntax is only explicitly defined for languages \- not for tokens in other fields such as optical or auditory fields. 

The task is ultimately then to construct a turing machine that operates on these tokens however as previously mentioned this turing machine would not terminate (so it’s not technically a turing machine as turing machines terminate by definition). We would then want to use this turing machine as a pattern in a pattern-antipattern schematic. 

This brings us back to the BFF experiment. We already have the alphabet of the turing machine (the reference index) and the states (the tokens). The main undefined variable is the transition function. As shown in the BFF experiment we can create computational replicators using embedded computation. It then stands to reason that we could create an approximation of this transition function using the same method if we implement an environmental pressure \- some kind of error function. The question would be what this would even represent.

# References

y Arcas, B.A. *et al.* (2024) ‘Computational Life: How Well-formed, Self-replicating Programs Emerge from Simple Interaction’, *arXiv \[cs.NE\]* \[Preprint\]. Available at: [http://arxiv.org/abs/2406.19108](http://arxiv.org/abs/2406.19108). 
