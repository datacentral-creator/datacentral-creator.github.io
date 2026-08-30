
from __future__ import annotations  
from dataclasses import dataclass, field  
from functools import lru_cache  
from collections import Counter  
from typing import Dict, List, Tuple, Optional  
import math  
import os

# ------------------------------------------------------------  
# Suffix Automaton  
# ------------------------------------------------------------

@dataclass  
class SAMNode:  
   next: Dict[int, int] = field(default_factory=dict)  
   link: int = -1  
   length: int = 0  
   min_end_pos: int = 10**18

class SuffixAutomaton:  
   def __init__(self):  
       self.nodes: List[SAMNode] = [SAMNode()]  
       self.last: int = 0

   def extend(self, token: int, pos: int):  
       nodes = self.nodes  
       cur = len(nodes)  
       nodes.append(SAMNode(length=nodes[self.last].length + 1,  
                            min_end_pos=pos))

       p = self.last  
       while p != -1 and token not in nodes[p].next:  
           nodes[p].next[token] = cur  
           p = nodes[p].link

       if p == -1:  
           nodes[cur].link = 0  
       else:  
           q = nodes[p].next[token]  
           if nodes[p].length + 1 == nodes[q].length:  
               nodes[cur].link = q  
           else:  
               clone = len(nodes)  
               nodes.append(SAMNode(  
                   next=nodes[q].next.copy(),  
                   link=nodes[q].link,  
                   length=nodes[p].length + 1,  
                   min_end_pos=nodes[q].min_end_pos  
               ))

               while p != -1 and nodes[p].next.get(token) == q:  
                   nodes[p].next[token] = clone  
                   p = nodes[p].link

               nodes[q].link = nodes[cur].link = clone

       self.last = cur

   def build(self, tokens: List[int]):  
       for i, t in enumerate(tokens):  
           self.extend(t, i)  
       self._propagate_min_end_pos()

   def _propagate_min_end_pos(self):  
       order = sorted(range(len(self.nodes)),  
                      key=lambda i: self.nodes[i].length,  
                      reverse=True)  
       for v in order:  
           link = self.nodes[v].link  
           if link != -1:  
               self.nodes[link].min_end_pos = min(  
                   self.nodes[link].min_end_pos,  
                   self.nodes[v].min_end_pos  
               )

   def longest_previous_match(self, tokens: List[int], start: int) -> Tuple[int, Optional[int]]:  
       nodes = self.nodes  
       v = 0  
       length = 0  
       best_len = 0  
       n = len(tokens)

       for i in range(start, n):  
           t = tokens[i]  
           if t not in nodes[v].next:  
               break  
           v = nodes[v].next[t]  
           length += 1

           end_here = start + length - 1  
           if nodes[v].min_end_pos < end_here:  
               best_len = length  
           else:  
               break

       return best_len, (v if best_len > 0 else None)

# ------------------------------------------------------------  
# Compression  
# ------------------------------------------------------------

def compress_sam(encoded: List[int], highest_token: int):  
   sam = SuffixAutomaton()  
   sam.build(encoded)

   codex = {}  
   output = []  
   i = 0  
   n = len(encoded)

   while i < n:  
       best_len, _ = sam.longest_previous_match(encoded, i)

       if best_len >= 2:  
           seq = encoded[i:i + best_len]  
           highest_token += 1  
           tok = highest_token  
           codex[tok] = seq  
           output.append(tok)  
           i += best_len

           while i <= n - best_len and encoded[i:i + best_len] == seq:  
               output.append(tok)  
               i += best_len  
       else:  
           output.append(encoded[i])  
           i += 1

   return codex, output, highest_token

def encode_text(text: str):  
   seen = {}  
   for c in text:  
       if c not in seen:  
           seen[c] = len(seen)

   ref_codex = {i: c for c, i in seen.items()}  
   encoded = [seen[c] for c in text]

   codices = [ref_codex]  
   highest = len(ref_codex)

   codex, window, highest = compress_sam(encoded, highest)  
   if codex:  
       codices.append(codex)

   while True:  
       new_codex, window, highest = compress_sam(window, highest)  
       if not new_codex:  
           break  
       codices.append(new_codex)

   return codices, window

# ------------------------------------------------------------  
# Thoughtforms & Strengths  
# ------------------------------------------------------------

def extract_thoughtforms(codices):  
   return [key for codex in codices for key in codex.keys()]

def calculate_strengths(tokens, codices): 
   """  
   *Strength of a thoughtform token is:*  
       *count(token) / (len(tokens) * avg_distance_between_occurrences)*  
   *"""*  
   strengths = {}

   # All thoughtform tokens (keys of codices)  
   thoughtforms = set()  
   for codex in codices:  
       thoughtforms.update(codex.keys())

   # Positions of each thoughtform in the compressed token stream  
   positions = {tf: [] for tf in thoughtforms}  
   for i, t in enumerate(tokens):  
       if t in positions:  
           positions[t].append(i)

   # Compute strengths  
   for tf, pos_list in positions.items():  
       if len(pos_list) < 2:  
           continue  # cannot compute distances

       diffs = [pos_list[i] - pos_list[i - 1] for i in range(1, len(pos_list))]  
       avg_dist = sum(diffs) / len(diffs)

       strength = len(pos_list) / (len(tokens) * avg_dist)  
       strengths[tf] = strength

   return strengths

# ------------------------------------------------------------  
# Egregore sets  
# ------------------------------------------------------------

def extract_egregore_sets(tokens: List[int], codices: List[Dict[int, List[int]]]):  
   strengths = calculate_strengths(tokens, codices)  
   thoughtforms = extract_thoughtforms(codices)

   tf_positions = {tf: [] for tf in thoughtforms}  
   for i, t in enumerate(tokens):  
       if t in tf_positions:  
           tf_positions[t].append(i)

   eg_sets = []  
   n = len(tokens)

   for tf in thoughtforms:  
       dist = strengths.get(tf, 1)  
       for pos in tf_positions[tf]:  
           lo = max(0, math.floor(pos - dist))  
           hi = min(n, math.ceil(pos + dist))  
           eg_sets.append((tokens[lo:hi], tf))

   return eg_sets

# ------------------------------------------------------------  
# Decompression  
# ------------------------------------------------------------

def translate_tokens(tokens: List[int], codices: List[Dict[int, List[int]]]):  
   lookup = {}  
   for codex in codices:  
       lookup.update(codex)

   cache = {}

   def expand(t):  
       if t in cache:  
           return cache[t]

       v = lookup.get(t)  
       if v is None:  
           cache[t] = [t]  
           return [t]

       if not isinstance(v, list):  
           cache[t] = [v]  
           return [v]

       result = []  
       for x in v:  
           result.extend(expand(x))

       cache[t] = result  
       return result

   out = []  
   for t in tokens:  
       out.extend(expand(t))  
   return out

# ------------------------------------------------------------  
# Load + Encode File  
# ------------------------------------------------------------

def get_file_encoding(path: str):  
   with open(path, "r", encoding="utf-8") as f:  
       text = f.read()

   codices, tokens = encode_text(text)  
   return codices, tokens

# ------------------------------------------------------------  
# Thoughtform Evaluation  
# ------------------------------------------------------------

def get_evaluated_thoughtforms(path: str):  
   codices, tokens = get_file_encoding(path)

   strengths = calculate_strengths(tokens, codices)  
   thoughtforms = extract_thoughtforms(codices)

   evaluated = [[tf, strengths.get(tf, 0)] for tf in thoughtforms]  
   evaluated.sort(key=lambda x: x[1], reverse=True)

   return evaluated

# ------------------------------------------------------------  
# Egregore Set Evaluation  
# ------------------------------------------------------------

def get_evaluated_egregore_sets(path: str):  
   codices, tokens = get_file_encoding(path)

   strengths = calculate_strengths(tokens, codices)  
   eg_sets = extract_egregore_sets(tokens, codices)

   evaluated = []  
   for seq, anchor in eg_sets:  
       strength = strengths.get(anchor, 0)  
       evaluated.append([seq, strength])

   evaluated.sort(key=lambda x: x[1], reverse=True)  
   return evaluated

def translate_evaluated_egregore_sets(evaluated_eg_sets, codices):  
   """  
   *Takes evaluated egregore sets in token form:*  
       *[ [token_seq], strength ]*  
   *and returns:*  
       *[ "expanded_text", strength ]*  
   *"""*  
   translated = []

   for token_seq, strength in evaluated_eg_sets:  
       expanded = translate_tokens(token_seq, codices)  
       text = "".join(str(x) for x in expanded)  
       translated.append([text, strength])

   return translated

def translate_evaluated_thoughtforms(evaluated_tfs, codices):  
   """  
   *Takes evaluated thoughtforms:*  
       *[tf_token, strength]*  
   *and returns:*  
       *["expanded_text", strength]*  
   *"""*  
   translated = []

   for tf, strength in evaluated_tfs:  
       expanded = translate_tokens([tf], codices)  
       text = "".join(str(x) for x in expanded)  
       translated.append([text, strength])

   return translated
