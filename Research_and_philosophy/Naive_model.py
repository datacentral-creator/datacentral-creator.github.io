import json  
import math  
import os  
import numpy as np  
from functools import lru_cache  
from collections import Counter

# ------------------------------  
# Cached file loading  
# ------------------------------  
@lru_cache(maxsize=None)  
def load_json(path):  
   with open(path, "r") as f:  
       return json.load(f)

# ------------------------------  
# Token utilities  
# ------------------------------  
def parse_tokens(tokens):  
   return list(map(int, tokens.split(",")))

def extract_thoughtforms(tokens):  
   seq = parse_tokens(tokens)  
   counts = Counter(seq)  
   return [tok for tok, c in counts.items() if c >= 2]

# ------------------------------  
# Upload utilities  
# ------------------------------  
def get_uploads(files):  
   return [load_json(f"uploads/{file.split('.')[0]}.json") for file in files]

def create_unified_reference_index(files):  
   seen = set()  
   unified = []

   for index in get_uploads(files):  
       # index is dict token → pos  
       for token in sorted(index, key=index.get):  
           if token not in seen:  
               seen.add(token)  
               unified.append(token)

   return {tok: i for i, tok in enumerate(unified)}

# ------------------------------  
# Strength calculations  
# ------------------------------  
def calculate_strengths(tokens, file):  
   seq = parse_tokens(tokens)  
   counts = Counter(seq)

   thoughtforms = extract_thoughtforms(tokens)  
   file_output = f"uploads/{file.split('.')[0]}_thoughtforms.json"

   if not os.path.exists(file_output):  
       tf_index = {i: tf for i, tf in enumerate(thoughtforms)}  
       with open(file_output, "w") as f:  
           json.dump(tf_index, f)

   total = len(seq)  
   return [counts[tf] / total for tf in thoughtforms]

# ------------------------------  
# Egregore extraction  
# ------------------------------  
def extract_egregore_sets(tokens, file):  
   strengths = calculate_strengths(tokens, file)  
   seq = parse_tokens(tokens)  
   n = len(seq)

   distances = [n * s for s in strengths]

   positions = load_json(f"uploads/{file.split('.')[0]}_thoughtforms.json")

   eg_sets = []  
   for i, dist in enumerate(distances):  
       pos = positions[str(i)]  # correct mapping: thoughtform index → position  
       lo = max(0, math.floor(pos - dist))  
       hi = min(n, math.ceil(pos + dist))  
       eg_sets.append(seq[lo:hi])

   return eg_sets

# ------------------------------  
# Tensor remapping  
# ------------------------------  
def remap_tensor(tensor, old_index, unified_index):  
   new = [0] * len(unified_index)

   # Reverse lookup once  
   pos_to_token = {pos: tok for tok, pos in old_index.items()}

   for old_pos, strength in enumerate(tensor):  
       tok = pos_to_token.get(old_pos)  
       if tok in unified_index:  
           new[unified_index[tok]] = strength

   return new

# ------------------------------  
# Egregore tensor calculation  
# ------------------------------  
def calculate_egregore_tensors(tokens, file):  
   eg_sets = extract_egregore_sets(tokens, file)  
   seq = parse_tokens(tokens)

   tf_path = f"uploads/{file.split('.')[0]}_thoughtforms.json"  
   thoughtforms = load_json(tf_path)  
   tf_list = [thoughtforms[str(i)] for i in range(len(eg_sets))]

   # Ensure anchor is included  
   for i, eg in enumerate(eg_sets):  
       if tf_list[i] not in eg:  
           eg.insert(0, tf_list[i])

   strengths = []  
   for i, eg in enumerate(eg_sets):  
       anchor = tf_list[i]  
       anchor_pos = eg.index(anchor)

       precursors = [abs(anchor_pos - j) * len(seq) for j in range(len(eg))]

       # Compute strengths  
       s = []  
       for j, p in enumerate(precursors):  
           if p == 0:  
               s.append(0)  
           else:  
               s.append(seq.count(eg[j]) / p)

       strengths.append(s)

   return strengths

# ------------------------------  
# Main similarity function  
# ------------------------------  
def calculate_egregore_strength(tokens1, file1, tokens2, file2):  
   E1 = calculate_egregore_tensors(tokens1, file1)  
   E2 = calculate_egregore_tensors(tokens2, file2)

   idx1 = load_json(f"uploads/{file1.split('.')[0]}.json")  
   idx2 = load_json(f"uploads/{file2.split('.')[0]}.json")

   TF1 = load_json(f"uploads/{file1.split('.')[0]}_thoughtforms.json")  
   TF2 = load_json(f"uploads/{file2.split('.')[0]}_thoughtforms.json")

   TF1_list = [TF1[str(i)] for i in range(len(TF1))]  
   TF2_list = [TF2[str(i)] for i in range(len(TF2))]

   E1_dict = dict(zip(TF1_list, E1))  
   E2_dict = dict(zip(TF2_list, E2))

   shared = set(E1_dict) & set(E2_dict)  
   if not shared:  
       return 0

   unified = create_unified_reference_index([file1, file2])

   total = 0  
   for tf in shared:  
       t1 = remap_tensor(E1_dict[tf], idx1, unified)  
       t2 = remap_tensor(E2_dict[tf], idx2, unified)  
       total += np.dot(t1, t2)

   return total

# ------------------------------  
# Text utilities  
# ------------------------------  
def extract_reference_index(text, file_name):  
   words = list(dict.fromkeys(text.split()))  
   mapping = {w: i for i, w in enumerate(words)}

   with open(f"uploads/{file_name.split('.')[0]}.json", "w") as f:  
       json.dump(mapping, f)

def extract_tokens(text, file_name):  
   path = f"uploads/{file_name.split('.')[0]}.json"  
   if not os.path.exists(path):  
       extract_reference_index(text, file_name)

   ref = load_json(path)  
   return ",".join(str(ref[w]) for w in text.split())

def compare_texts(text1, file1, text2, file2):  
   return calculate_egregore_strength(  
       extract_tokens(text1, file1),  
       file1,  
       extract_tokens(text2, file2),  
       file2,  
   )
