# 1\. Purpose

The tagger component is designed to answer a single question:

**How can we extract *form* from information?**

It synthesises the theoretical framework developed in:

* **Text A:** [*Are ideas alive? How historical civilisations were governed by ideas*](https://datacentral-creator.github.io/Research_and_philosophy/essay)
* **Text B:** [*How recommendation algorithms affect the formation of culture*]([https://github.com/datacentral-creator/datacentral-creator.github.io/blob/main//Research_and_philosophy/algorithms.md](https://datacentral-creator.github.io/Research_and_philosophy/algorithms))

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

# 7\. First attempt

I implemented this methodology in a react native app with the following code  
`// egregore.ts`  
`import { Platform } from "react-native";`  
`import * as FileSystem from "expo-file-system/legacy";`  
`import AsyncStorage from "@react-native-async-storage/async-storage";`

`// ------------------------------------------------------------`  
`// Platform Abstraction`  
`// ------------------------------------------------------------`

`const isWeb = Platform.OS === "web";`  
`const UPLOAD_DIR = (FileSystem.documentDirectory ?? "") + "uploads/";`  
`let uploadDirEnsured = false;`

`function normalizeKey(path: string): string {`  
 ``return `uploads:${path.toLowerCase().replace(/[^\w.-]/g, "_")}`;``  
`}`

`async function ensureUploadDir() {`  
 `if (isWeb || uploadDirEnsured) return;`  
 `const info = await FileSystem.getInfoAsync(UPLOAD_DIR);`  
 `if (!info.exists) {`  
   `await FileSystem.makeDirectoryAsync(UPLOAD_DIR, { intermediates: true });`  
 `}`  
 `uploadDirEnsured = true;`  
`}`

`async function fileExists(path: string): Promise<boolean> {`  
 `if (isWeb) {`  
   `return (await AsyncStorage.getItem(normalizeKey(path))) !== null;`  
 `}`  
 `await ensureUploadDir();`  
 `return (await FileSystem.getInfoAsync(UPLOAD_DIR + path)).exists;`  
`}`

`async function loadFile(path: string): Promise<string> {`  
 `if (isWeb) {`  
   `const value = await AsyncStorage.getItem(normalizeKey(path));`  
   ``if (value === null) throw new Error(`File not found: ${path}`);``  
   `return value;`  
 `}`  
 `await ensureUploadDir();`  
 `return FileSystem.readAsStringAsync(UPLOAD_DIR + path);`  
`}`

`async function writeFile(path: string, data: string) {`  
 `if (isWeb) {`  
   `await AsyncStorage.setItem(normalizeKey(path), data);`  
   `return;`  
 `}`  
 `await ensureUploadDir();`  
 `await FileSystem.writeAsStringAsync(UPLOAD_DIR + path, data);`  
`}`

`async function loadJson<T>(path: string): Promise<T> {`  
 `return JSON.parse(await loadFile(path));`  
`}`

`async function writeJson(path: string, data: any) {`  
 `await writeFile(path, JSON.stringify(data, null, 2));`  
`}`

`// ------------------------------------------------------------`  
`// Token utilities`  
`// ------------------------------------------------------------`

`const parseTokens = (tokens: string): number[] =>`  
 `tokens.split(",").map(Number);`

`function extractThoughtforms(tokens: string): number[] {`  
 `const seq = parseTokens(tokens);`  
 `const counts = new Map<number, number>();`

 `for (const t of seq) counts.set(t, (counts.get(t) ?? 0) + 1);`

 `return [...counts.entries()]`  
   `.filter(([_, c]) => c >= 2)`  
   `.sort((a, b) => seq.indexOf(a[0]) - seq.indexOf(b[0]))`  
   `.map(([tok]) => tok);`  
`}`

`// ------------------------------------------------------------`  
`// Strength calculations`  
`// ------------------------------------------------------------`

`async function calculateStrengths(tokens: string, file: string|any[]): Promise<number[]> {`  
 `const seq = parseTokens(tokens);`  
 `const total = seq.length;`

 `const counts = new Map<number, number>();`  
 `seq.forEach(t => counts.set(t, (counts.get(t) ?? 0) + 1));`

 `const thoughtforms = extractThoughtforms(tokens);`

 `if (typeof file == typeof ""){`  
   `//@ts-ignore`  
   `const base = file.split(".")[0].toLowerCase();`  
   ``const tfFile = `${base}_thoughtforms.json`;``

   `if (!(await fileExists(tfFile))) {`  
     `const tfIndex: Record<string, number[]> = {};`

     `thoughtforms.forEach((tf, i) => {`  
       `tfIndex[i] = seq`  
         `.map((tok, pos) => (tok === tf ? pos : -1))`  
         `.filter(pos => pos !== -1);`  
     `});`

     `await writeJson(tfFile, tfIndex);`  
   `}`  
 `}else{`  
    `const tfIndex: Record<string, number[]> = {};`  
     `thoughtforms.forEach((tf, i) => {`  
       `tfIndex[i] = seq`  
         `.map((tok, pos) => (tok === tf ? pos : -1))`  
         `.filter(pos => pos !== -1);`  
     `});`  
     `//@ts-ignore`  
     `file.push(tfIndex);`  
 `}`

 `return thoughtforms.map(tf => counts.get(tf)! / total);`  
`}`  
`// ------------------------------------------------------------`  
`// Egregore extraction`  
`// ------------------------------------------------------------`

`async function extractEgregoreSets(tokens: string, file: string|any[]): Promise<number[][]> {`  
 `const seq = parseTokens(tokens);`  
 `const n = seq.length;`

 `const strengths = await calculateStrengths(tokens,file);`  
 `const distances = strengths.map(s => n * s);`

 `if (typeof file == typeof ""){`  
   `//@ts-ignore`  
   `const base = file.split(".")[0];`  
   ``const positions = await loadJson<Record<string, number[]>>(`${base}_thoughtforms.json`);``  
   `const egSets: number[][] = [];`  
   `distances.forEach((dist, i) => {`  
     `const posList = positions[String(i)];`  
     `for (const pos of posList) {`  
       `const lo = Math.max(0, Math.floor(pos - dist));`  
       `const hi = Math.min(n, Math.ceil(pos + dist));`  
       `egSets.push(seq.slice(lo, hi));`  
     `}`  
   `});`  
   `return egSets;`  
 `}else{`  
   `const positions = file[0]`  
   `const egSets: number[][] = [];`  
   `distances.forEach((dist, i) => {`  
     `const posList = positions[String(i)];`  
     `for (const pos of posList) {`  
       `const lo = Math.max(0, Math.floor(pos - dist));`  
       `const hi = Math.min(n, Math.ceil(pos + dist));`  
       `egSets.push(seq.slice(lo, hi));`  
     `}`  
   `});`  
   `return egSets;`  
 `}`  
`}`

`// ------------------------------------------------------------`  
`// Text utilities`  
`// ------------------------------------------------------------`

`export async function extractReferenceIndex(`  
 `text: string,`  
 `fileName: string|null`  
`): Promise<Record<string, number>> {`  
 `const words = [...new Set(text.split(/\s+/))];`  
 `const mapping: Record<string, number> = {};`  
 `words.forEach((w, i) => (mapping[w] = i));`  
 `if (fileName){`  
   `const base = fileName.split(".")[0];`  
   ``const jsonPath = `${base}.json`;``

   `// Check for the JSON file, not TXT`  
   `if (await fileExists(jsonPath)) {`  
     `return loadJson(jsonPath);`  
   `}`  
   `await writeJson(jsonPath, mapping);`  
 `}`  
 `return mapping;`  
`}`

`export async function extractTokens(text: string, fileName: string|null): Promise<string> {`  
 `if (fileName){`  
   `const base = fileName.split(".")[0];`  
   ``const path = `${base}.json`;``

   `if (!(await fileExists(path))) {`  
     `await extractReferenceIndex(text, fileName);`  
   `}`

   `const ref = await loadJson<Record<string, number>>(path);`  
   `return text.split(/\s+/).map(w => ref[w]).join(",");`  
 `}else{`  
   `const ref = await extractReferenceIndex(text,null)`  
   `return text.split(/\s+/).map(w => ref[w]).join(",");`  
 `}`  
`}`

`export async function processWord(word: string, text: string, file: string): Promise<string> {`  
 `const tokens = await extractTokens(text, file);`  
 `const seq = parseTokens(tokens);`

 `const tf = extractThoughtforms(tokens);`  
 `const referenceIndex = await extractReferenceIndex(text, file);`

 `const symbol = referenceIndex[word];`  
 `if (!tf.includes(symbol)) return "";`

 `const base = file.split(".")[0];`  
 ``const positions = await loadJson<Record<string, number[]>>(`${base}_thoughtforms.json`);``

 `const tfIndexes = Object.entries(positions)`  
   `.filter(([_, posList]) => posList.some(p => seq[p] === symbol))`  
   `.map(([i]) => Number(i));`

 `if (tfIndexes.length === 0) return "";`

 `const reverseIndex = Object.fromEntries(`  
   `Object.entries(referenceIndex).map(([w, t]) => [t, w])`  
 `);`

 `const egSets = await extractEgregoreSets(tokens, file);`

 `const words: string[] = [];`

 `for (const idx of tfIndexes) {`  
   `words.push("...");`  
   `egSets[idx].forEach(t => words.push(reverseIndex[t]));`  
   `words.push("...");`  
 `}`

 `return words.join(" ");`  
`}`

`export async function ProcessWordNoFile(word:string,text:string){`  
 `const tokens = await extractTokens(text,null);`  
 `const seq = parseTokens(tokens);`

 `const tf = extractThoughtforms(tokens);`  
 `const referenceIndex = await extractReferenceIndex(text, null);`

 `const symbol = referenceIndex[word];`  
 `if (!tf.includes(symbol)) return "";`

 `const positions:any[] = []`  
 `const egSets = await extractEgregoreSets(tokens,positions);`

 `const tfIndexes = Object.entries(positions[0])`  
   `//@ts-ignore`  
   `.filter(([_, posList]) => posList.some(p => seq[p] === symbol))`  
   `.map(([i]) => Number(i));`

 `if (tfIndexes.length === 0) return "";`

 `const reverseIndex = Object.fromEntries(`  
   `Object.entries(referenceIndex).map(([w, t]) => [t, w])`  
 `);`

 `const words: string[] = [];`

 `for (const idx of tfIndexes) {`  
   `words.push("...");`  
   `egSets[idx].forEach(t => words.push(reverseIndex[t]));`  
   `words.push("...");`  
 `}`

 `return words.join(" ");`  
`}`

When I processed *The Black Cat* using my original methodology, the results were thoroughly disappointing. That failure forced me to examine the pipeline itself rather than the specific text. The first and most obvious weakness is the tokenisation step. Splitting text on whitespace is a naïve approach that introduces structural noise and amplifies errors at every subsequent stage of the tagger.

Whitespace tokenisation treats “apple” and “apple.” as different symbols, fragments cycles, inflates the reference index, and makes the system sensitive to punctuation rather than meaning. Because the tagger’s later stages depend on recurrence and adjacency, this early fragmentation propagates through the entire pipeline and degrades the quality of the extracted egregores.

A more robust approach is to tokenise at the character level. Characters form a universal symbolic basis across languages, and they eliminate the boundary problems inherent in word‑level splitting. Under this scheme, both “apple” and “apple.” contain the same recurring subsequence “apple”, allowing the system to detect meaningful patterns without being misled by punctuation. It also dramatically reduces the size of the reference index: for alphabetic languages, the index is bounded by the alphabet rather than by the vocabulary of the text.

However, this approach introduces its own challenges. Character‑level tokenisation collapses distinctions between words that share substrings. For example, “practice” and “malpractice” both contain the sequence “practice”, and without additional structure the system may treat them as related when they are not. Character‑level tokenisation therefore requires a more sophisticated method for identifying recurring sequences—n‑grams, variable‑length motifs, or cycle detection over character graphs—so that the tagger can distinguish meaningful patterns from accidental overlaps.

The problem now becomes that a morpheme can be of any length for example “supercalifragilousexpialidousous” is a perfectly valid morpheme in the context of may poppins however to scan for every possible n-gram for a text with an arbitrary number of characters you would need that number of scans. Additionally each scan requires processing c/n elements where c is the arbitrary number of characters. This gives c/1 \+ c/2 \+ c/3 \+ c/4 .. c/c elements to be processed. This is equivalent to c\*(1+ ½ \+ ⅓ \+ ¼ .. 1/c). This can be roughly estimated as c\*log(c) for large values of c giving us a computational complexity of O(nlog(n)).   
This is mathematically practical because as n increases log(n) barely increases for example log(100000000) \= 8\. This means the computation is approximately linear however this is still not ideal.

What we can do instead is ensure:  
1 character \= 1 token  
As we said above  
Then we can store this in an array.  
From there we can identify tokens that repeat.  
If a token repeats we then check if nearby tokens repeat.  
We keep extending this until we find a common boundary. 

We can make this O(n) if we implement it serially.  
We can iterate through each element of the array and construct a dictionary that maps each token to the number of occurrences and neighbouring tokens for example:  
\[0,1,2,3,2,3,2,1\]   
Becomes  
{0: {occurences: 1, neighbouring tokens: null},1:{occurences:2,neighbouring tokens:null},2:{occuences:3,neighbouring token:3},3:{occurences:2,neighbouring tokens:null}}

Here neighbouring tokens are destructive \- for example the subsequence \[3,2\] recurs but \[2,3\] doesn’t 2 should have 3 as a neighbouring token because 2 occurs after 3 but 3 shouldn’t have 2 as a neighbouring token because 3 does not occur after 2 as a part of the recurring sequence.

We can implement this by saving the last variable that occurred and using this as the neighbouring token in an array then if we get to the end and occurrences \> 2 we only include neighbouring tokens that appear more than twice.

I implemented this as   
`// egregore.ts`

`// ------------------------------------------------------------`  
`// Token utilities`  
`// ------------------------------------------------------------`

`const parseTokens = (tokens: string): number[] =>`  
 `tokens.split(",").map(Number);`

`function extractThoughtforms(tokens: string): number[][] {`  
 `const seq = parseTokens(tokens);`  
 `const occurrences:Record<number,number> = {}`  
 `const neighbours:Record<number,number> = {}`  
 `seq.forEach((token:number,index:number) => {`  
   `neighbours[token] = seq[index-1]`  
   `if (token in occurrences) {`  
     `occurrences[token] += 1`  
   `}else{`  
     `occurrences[token] = 1`  
   `}`  
 `})`  
 `//@ts-ignore`  
 `return Object.keys(occurrences).map((key:string)=>{`  
   `//@ts-ignore`  
   `if (occurrences[+key] > 1){`  
     `const tokens = [+key]`  
     `const added_tokens:number[] = []`  
     `let key_two = +key`  
     `let param = true`  
     `while (!(added_tokens.includes(key_two)) && param){`  
       `key_two = neighbours[key_two]`  
       `if ((key_two in occurrences)&&(occurrences[key_two] > 1)){`  
         `tokens.push(key_two);`  
         `added_tokens.push(key_two)`  
       `}else{`  
         `param = false`  
       `}`  
     `}`  
     `return tokens`  
   `}`  
 `}).filter((key:number[]|undefined)=>key)`  
`}`

`// ------------------------------------------------------------`  
`// Strength calculations`  
`// ------------------------------------------------------------`

`async function calculateStrengths(tokens: string, file: any[]): Promise<number[]> {`  
 `const seq = parseTokens(tokens);`  
 `const total = seq.length;`

 `const counts = new Map<number, number>();`  
 `seq.forEach(t => counts.set(t, (counts.get(t) ?? 0) + 1));`

 `const thoughtforms = extractThoughtforms(tokens);`  
 `const tfIndex: Record<string, number[]> = {};`  
 `thoughtforms.forEach((tf, i) => {`  
   `tfIndex[i] = seq`  
       `.map((tok, pos) => (tok === tf ? pos : -1))`  
       `.filter(pos => pos !== -1);`  
 `});`  
 `//@ts-ignore`  
 `file.push(tfIndex);`

 `return thoughtforms.map(tf => counts.get(tf)! / total);`  
`}`  
`// ------------------------------------------------------------`  
`// Egregore extraction`  
`// ------------------------------------------------------------`

`async function extractEgregoreSets(tokens: string, file: any[]): Promise<number[][]> {`  
 `const seq = parseTokens(tokens);`  
 `const n = seq.length;`

 `const strengths = await calculateStrengths(tokens,file);`  
 `const distances = strengths.map(s => n * s);`  
 `const positions = file[0]`  
 `const egSets: number[][] = [];`  
 `distances.forEach((dist, i) => {`  
   `const posList = positions[String(i)];`  
   `for (const pos of posList) {`  
     `const lo = Math.max(0, Math.floor(pos - dist));`  
     `const hi = Math.min(n, Math.ceil(pos + dist));`  
     `egSets.push(seq.slice(lo, hi));`  
   `}`  
 `});`  
 `return egSets;`  
 `}`

`// ------------------------------------------------------------`  
`// Text utilities`  
`// ------------------------------------------------------------`

`export async function extractReferenceIndex(text: string): Promise<Record<string, number>> {`  
 `const characters = [...new Set(text.split(""))]`  
 `const mapping: Record<string, number> = {};`  
 `characters.forEach((w, i) => (mapping[w] = i));`  
 `return mapping;`  
`}`

`export async function extractTokens(text: string):Promise<[string,Record<string,number>]>{`  
   `const ref = await extractReferenceIndex(text)`  
   `return [text.split("").map(w => ref[w]).join(","),ref]`  
`}`

`export async function ProcessWordNoFile(word:string,text:string){`  
 `const [tokens,referenceIndex] = await extractTokens(text);`  
 `const seq = parseTokens(tokens);`  
 `const tf = extractThoughtforms(tokens);`  
 `console.log(tf.map((tokens:number[])=>tokens.map((tf:number) => Object.keys(referenceIndex)[Object.values(referenceIndex).indexOf(tf)]).join("")))`

 `const symbol = referenceIndex[word];`  
 `if (!tf.includes(symbol)) return "";`

 `const positions:any[] = []`  
 `const egSets = await extractEgregoreSets(tokens,positions);`

 `const tfIndexes = Object.entries(positions[0])`  
   `//@ts-ignore`  
   `.filter(([_, posList]) => posList.some(p => seq[p] === symbol))`  
   `.map(([i]) => Number(i));`

 `if (tfIndexes.length === 0) return "";`

 `const reverseIndex = Object.fromEntries(`  
   `Object.entries(referenceIndex).map(([w, t]) => [t, w])`  
 `);`

 `const words: string[] = [];`

 `for (const idx of tfIndexes) {`  
   `words.push("...");`  
   `egSets[idx].forEach(t => words.push(reverseIndex[t]));`  
   `words.push("...");`  
 `}`

 `return words.join(" ");`  
`}`

`ProcessWordNoFile("Hello","Hello there in a hello world")`

And got   
\[ 'eh', 'lr', 'o', ' o', 'h ', 'ro' \]

Which was definitely not supposed to happen

# 8\. Second attempt

I realised the problem was that I was retrieving the data backwards which is why I got sequences like “eh”(This would have come from “he” like “he” in “hello”).

I decided to keep the idea of using motifs as thoughtforms as opposed to individual tokens and after researching the problem I had I decided to use a suffix array implementation creating the following code.

`// egregore.ts`  
`// ============================================================`  
`// TYPES`  
`// ============================================================`  
`//`  
`// MotifInfo represents a repeated substring (motif) discovered`  
`// by the suffix-array/LCP motif extractor.`  
`//`  
`// - motif:     the token sequence itself`  
`// - freq:      how many times it appears in the text`  
`// - positions: all starting indices where the motif occurs`  
`// - score:     information-content score (assigned later)`  
`//`  
`type MotifInfo = {`  
 `motif: number[];`  
 `freq: number;`  
 `positions: number[];`  
 `score?: number;`  
`};`

`// ============================================================`  
`// 1. TOKENISATION (character → integer token)`  
`// ============================================================`  
`//`  
`// Each unique character in the text is assigned a unique integer.`  
`// This makes the system fully generalisable: any media can be`  
`// converted into integer tokens and processed the same way.`  
`//`  
`// extractReferenceIndex:`  
`//   Builds a mapping from characters → token IDs.`  
`//`  
`// extractTokens:`  
`//   Converts the text into an array of token IDs using the mapping.`  
`//`  
`export function extractReferenceIndex(text: string): Record<string, number> {`  
 `const mapping: Record<string, number> = {};`  
 `let idx = 0;`

 `for (let i = 0; i < text.length; i++) {`  
   `const c = text[i];`  
   `if (mapping[c] === undefined) {`  
     `mapping[c] = idx++;`  
   `}`  
 `}`

 `return mapping;`  
`}`

`export function extractTokens(text: string): [number[], Record<string, number>] {`  
 `const ref = extractReferenceIndex(text);`  
 `const seq = new Array<number>(text.length);`

 `for (let i = 0; i < text.length; i++) {`  
   `seq[i] = ref[text[i]];`  
 `}`

 `return [seq, ref];`  
`}`

`// ============================================================`  
`// 2. SUFFIX ARRAY (prefix-doubling algorithm)`  
`// ============================================================`  
`//`  
`// A suffix array is a sorted list of all suffixes of the token`  
`// sequence. It allows us to detect repeated substrings efficiently.`  
`//`  
`// buildSuffixArray:`  
`//   Constructs the suffix array using the O(n log n) prefix-doubling`  
`//   algorithm. Works on integer tokens.`  
`//`  
`function buildSuffixArray(arr: number[]): number[] {`  
 `const n = arr.length;`  
 `const sa = Array.from({ length: n }, (_, i) => i);`  
 `const rank = [...arr];`  
 `const tmp = new Array<number>(n);`

 `for (let k = 1; k < n; k <<= 1) {`  
   `// Sort suffixes by (rank[i], rank[i+k])`  
   `sa.sort((a, b) => {`  
     `if (rank[a] !== rank[b]) return rank[a] - rank[b];`  
     `const ra = a + k < n ? rank[a + k] : -1;`  
     `const rb = b + k < n ? rank[b + k] : -1;`  
     `return ra - rb;`  
   `});`

   `// Recompute ranks`  
   `tmp[sa[0]] = 0;`  
   `for (let i = 1; i < n; i++) {`  
     `const prev = sa[i - 1];`  
     `const curr = sa[i];`  
     `const same =`  
       `rank[prev] === rank[curr] &&`  
       `(prev + k < n ? rank[prev + k] : -1) ===`  
         `(curr + k < n ? rank[curr + k] : -1);`

     `tmp[curr] = same ? tmp[prev] : tmp[prev] + 1;`  
   `}`

   `for (let i = 0; i < n; i++) rank[i] = tmp[i];`

   `// Early exit if all ranks are unique`  
   `if (rank[sa[n - 1]] === n - 1) break;`  
 `}`

 `return sa;`  
`}`

`// ============================================================`  
`// 3. LCP ARRAY (Longest Common Prefix)`  
`// ============================================================`  
`//`  
`// The LCP array stores the length of the longest common prefix`  
`// between adjacent suffixes in the suffix array.`  
`//`  
`// buildLCP:`  
`//   Computes the LCP array in O(n).`  
`//`  
`function buildLCP(arr: number[], sa: number[]): number[] {`  
 `const n = arr.length;`  
 `const rank = new Array<number>(n);`  
 `const lcp = new Array<number>(n - 1);`

 `for (let i = 0; i < n; i++) rank[sa[i]] = i;`

 `let h = 0;`  
 `for (let i = 0; i < n; i++) {`  
   `const r = rank[i];`  
   `if (r === 0) continue;`

   `const j = sa[r - 1];`

   `// Count matching prefix length`  
   `while (i + h < n && j + h < n && arr[i + h] === arr[j + h]) h++;`  
   `lcp[r - 1] = h;`

   `if (h > 0) h--;`  
 `}`

 `return lcp;`  
`}`

`// ============================================================`  
`// 4. MOTIF EXTRACTION (repeated substrings + positions)`  
`// ============================================================`  
`//`  
`// extractMotifsWithFreq:`  
`//   Uses the suffix array + LCP array to extract ALL repeated`  
`//   substrings (motifs) of length ≥ 2.`  
`//`  
`//   For each LCP entry of length L, we extract all prefixes of`  
`//   lengths 2..L. We also track all positions where each motif`  
`//   occurs.`  
`//`  
`//   This ensures motifs like "ello" are detected even if their`  
`//   suffixes are not adjacent in the suffix array.`  
`//`  
`function extractMotifsWithFreq(arr: number[]): MotifInfo[] {`  
 `const sa = buildSuffixArray(arr);`  
 `const lcp = buildLCP(arr, sa);`

 `const motifsMap = new Map<string, MotifInfo>();`

 `for (let i = 0; i < lcp.length; i++) {`  
   `const len = lcp[i];`  
   `if (len < 2) continue;`

   `const start1 = sa[i];`  
   `const start2 = sa[i + 1];`

   `// Extract all prefixes of the LCP region`  
   `for (let k = 2; k <= len; k++) {`  
     `const motif = arr.slice(start1, start1 + k);`  
     `const key = motif.join(",");`

     `if (!motifsMap.has(key)) {`  
       `motifsMap.set(key, {`  
         `motif,`  
         `freq: 2,`  
         `positions: [start1, start2]`  
       `});`  
     `} else {`  
       `const entry = motifsMap.get(key)!;`  
       `entry.freq++;`  
       `entry.positions.push(start2);`  
     `}`  
   `}`  
 `}`

 `return Array.from(motifsMap.values());`  
`}`

`// ============================================================`  
`// 5. THOUGHTFORM SELECTION (high-information motifs)`  
`// ============================================================`  
`//`  
`// informationContent:`  
`//   Computes IC = length × log(freq+1)`  
`//`  
`// extractThoughtformsFromTokens:`  
`//   Filters motifs by IC threshold and sorts them by score.`  
`//   These become the "thoughtforms" of the text.`  
`//`  
`function informationContent(motif: number[], freq: number): number {`  
 `return motif.length * Math.log(freq + 1);`  
`}`

`export function extractThoughtformsFromTokens(seq: number[]): MotifInfo[] {`  
 `const motifs = extractMotifsWithFreq(seq);`

 `const scored = motifs`  
   `.map(m => ({`  
     `...m,`  
     `score: informationContent(m.motif, m.freq)`  
   `}))`  
   `.filter(m => m.score! > 1.5) // tunable threshold`  
   `.sort((a, b) => b.score! - a.score!);`

 `return scored;`  
`}`

`// ============================================================`  
`// 6. EGREGORES (co-occurrence windows around motifs)`  
`// ============================================================`  
`//`  
`// extractEgregoreSets:`  
`//   For each motif, extract a window of ±20 tokens around each`  
`//   occurrence. These windows represent the "egregores" —`  
`//   contextual clusters of meaning.`  
`//`  
`export function extractEgregoreSets(seq: number[], motifs: MotifInfo[]): number[][] {`  
 `const egSets: number[][] = [];`  
 `const n = seq.length;`

 `for (const { motif, positions } of motifs) {`  
   `const m = motif.length;`  
   `const windows: number[] = [];`

   `for (const pos of positions) {`  
     `const lo = Math.max(0, pos - 20);`  
     `const hi = Math.min(n, pos + m + 20);`

     `for (let k = lo; k < hi; k++) {`  
       `windows.push(seq[k]);`  
     `}`  
   `}`

   `egSets.push(windows);`  
 `}`

 `return egSets;`  
`}`

`// ============================================================`  
`// 7. DEBUGGING / INSPECTION`  
`// ============================================================`  
`//`  
`// ProcessWordNoFile:`  
`//   Given a word and a text, this function:`  
`//`  
`//   1. Tokenises the text`  
`//   2. Extracts thoughtforms (motifs)`  
`//   3. Converts motifs back into readable strings`  
`//   4. Finds motifs that appear inside the given word`  
`//   5. Extracts egregores for those motifs`  
`//   6. Decodes egregores back into characters`  
`//`  
`//   This effectively retrieves "all information in the text`  
`//   associated with the given word".`  
`//`  
`export async function ProcessWordNoFile(word: string, text: string) {`  
 `const [seq, ref] = extractTokens(text);`

 `// Reverse lookup: token → character`  
 `const reverseIndex = Object.fromEntries(`  
   `Object.entries(ref).map(([k, v]) => [v, k])`  
 `);`

 `// Extract motifs (thoughtforms)`  
 `const motifs = extractThoughtformsFromTokens(seq);`

 `// Convert motifs to readable strings`  
 `const readableMotifs = motifs.map(m =>`  
   `m.motif.map(t => reverseIndex[t]).join("")`  
 `);`

 `const lowerWord = word.toLowerCase();`

 `// Find motifs that appear inside the given word`  
 `const matchingMotifs = motifs.filter((m, i) => {`  
   `const motifStr = readableMotifs[i];`  
   `return lowerWord.includes(motifStr.toLowerCase());`  
 `});`

 `if (matchingMotifs.length === 0) {`  
   ``return `No motifs from the text appear inside the word "${word}".`;``  
 `}`

 `// Extract egregores for matching motifs`  
 `const egSets = extractEgregoreSets(seq, matchingMotifs);`

 `// Decode egregores back into characters`  
 `const decoded = egSets.map(set =>`  
   `set.map(t => reverseIndex[t]).join("")`  
 `).join("...");`

 `return decoded;`  
`}`

Results after this attempt were far superior.
