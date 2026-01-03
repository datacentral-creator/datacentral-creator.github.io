**Navigation:**  
[Research](index.md) | [Datacentral](https://github.com/datacentral-creator/Datacentral) | [History](history.md)

What is the tagger component?
The tagger component is the solution to a question. The question is “how can I create a system that allows you to extract form from information?”. I intend to answer this question by synthesising the work of my essay “Are ideas alive? How historical civilisations were governed by ideas”(text A) and my research paper “How do recommendation algorithms affect the formation of culture”(text B). 

The methodology 
As laid out in text A the first step is to convert the media into tokens with a way to translate between the raw data and tokenised data:
For text:
A reference index is created - a dictionary converting each word to the order it appears in chronologically
The text is converted into a sequence of words (but in the future I will extend this to be morphemes it’s just that the actual implementation of this uses spaces to separate words however for languages like chinese where morphemes aren’t separated by spaces this is a much more difficult task). 
Each word is mapped to it’s corresponding number using the dictionary
The text file now becomes a list of numbers 
For an image:
We could easily extend this tokenisation process to images except where the reference index maps numbers to the hexadecimal values of the pixels in the order they appear. 
For a video:
We could further extend the tokenisation process to a video using the same method as for an image but with each moment of the video
The second step is to create a graph from the tokens - this just means connecting them in a logical order.
For text we would get a 1 dimensional graph IE:
1 → 3 → 5 → 7
For images we would get a 2 dimensional graph IE:
1 → 3 → 5 → 7
|       |       |      |
\/     \/      \/      \/
3 → 6 → 4 → 8
Here we would just split this into multiple 1 dimensional graphs aligned along the 2 dimensions IE 
1 → 3 → 5 → 7
3 → 6 → 4 → 8
1 →3
3 →6
5 →4
7 →8
For videos we would get a 3 dimensional graph and the same principle applies.
The third step is to identify thoughtforms - that is elements of the graph that repeat.
We can then create a set of all the thoughtforms that occur for instance for our graph it would be (3)
To identify this in dimensions higher than the first dimension as well as analysing each graph you would have to analyse between graphs by going across each graph element by element and checking not only that graph but all other graphs for repeats. 
We then create a tensor space for each thoughtform where the position of the tensor space corresponds to the position of the thoughtform it is anchored on 
The fourth step is to calculate the strength of the thoughtforms using the formula:
Strength = frequency/(sequence length * average return distance)
Where frequency is how many times the thoughtform occurs, sequence length is the length of the sequence in which the thoughtform reoccurs (for instance for 3 this sequence would be 3 → 6 → 3) and the average return distance is the average amount of tokens in which the thoughtform returns 
For token 3 we would get strength = 2/(3*2) = ⅓ 
We can now create an egregore set which is a set of memes(tokens) such that the strength of each meme with the thoughtform is larger than the strength of the thoughtform itself
In this case we get the set of tokens where the strength with 3 is greater than ⅓ 
For all thoughtforms we can construct a sequence through which the thoughtform recurs - within this sequence the frequency of the thoughtform is constant and so is the sequence length so the only factor that changes is the average return distance where we can say average return distance = frequency/(sequence length * strength)
For memes that aren’t thoughtforms, frequency = 1 and average return distance will be the distance from the thoughtform so we can say distance from the thoughtform = 1/(sequence length * strength) 
We can then take all non-thoughtform memes within that distance from all occurrences of the thoughtform and say those are in our egregore set
For other thoughtforms in the sequence we can firstly check if they are still a thoughtform in this specific sequence (if not the rule above applies) and if they are a thoughtform we just divide their average distance from the thoughtform by their frequency and do the check above
For instance in our sequence we have 3 → 6 → 3.
We can say that the other token is a 6 and it doesn’t repeat so it’s not a thoughtform.
We get that distance from thoughtform = 1/(3*(⅓)) = 1 so all non-thoughtform memes within a distance of 1 from the thoughtform meet the criteria to be in our egregore giving us in this case an egregore set of {6} however because we have normalised the conditions for the tensor spaces we can represent this egregore set as (1/(3*1)) = (⅓) where ⅓ is the strength of token 6 with the thoughtform 3.
This method might seem convoluted however as the sequences get larger it becomes increasingly efficient
It also means however that when we have multiple egregores we must represent the tensor version of the egregore set consistently - for ever egregore tensor each element must represent the same token no matter the egregore however similar to the reference indexes we can simply do this using the convention of the first egregore. 
We can now compare files by extracting their egregore tensors then normalising their egregore tensors (in this context this means creating a set of all egregore tensors with the same anchor and convention and changing the anchors and convention of egregore tensors to make this set) and getting the dot product of all these tensors. 
We can then rank these files by how similar they are to recommend them 

The task of unification
Firstly - to record these conventions we can create a reference index mapping symbols to positions. Now normalisation becomes a task of unifying multiple reference indices. This is simple. For each reference index we will have a mapping of symbols to numbers, we can then sort the symbols in the order of those numbers. The numbers should be continuous considering they were assigned in chronological order meaning we can represent the reference index as an array of symbols where the index of the array (starting at 1 as opposed to 0) represents the number the symbol corresponds to. Now we can pick a reference index arbitrarily and add the other lists onto this list removing duplicated entries to create a unified reference index. We now go through the data of the other reference indexes and map them to the old reference index then to the new reference index to update them into a common format. 

The tagger future goal
In the future I wish to construct a computational implementation of cortical columns as described in text A and have these able to interpret egregore sets in a literal sense as neurological activations allowing the tagger to be able to conceive semantic meaning. I wish to then extend this to create a system I call the simulatrix where visual objects are also mapped onto the same mapping allowing you to input media into the system and speak to it through a textual interface or speak to the textual interface and generate media. I wish to use this in the future as a research assistant and hopefully a computational approach to physics. 
