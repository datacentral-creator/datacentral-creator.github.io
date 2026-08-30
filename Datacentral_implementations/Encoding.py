def encode_text(text: str):  
   seen = {}  
   for c in text:  
       if c not in seen:  
           seen[c] = len(seen)

   ref_codex = {i: c for c, i in seen.items()}  
   encoded = [seen[c] for c in text]

   codices = [ref_codex]  
   highest = len(ref_codex)
