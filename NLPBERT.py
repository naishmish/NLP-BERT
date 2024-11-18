from transformers import AutoTokenizer, BertModel
import sys
import torch
import numpy as np
from torch.nn.functional import cosine_similarity

if __name__ == "__main__":
    model = BertModel.from_pretrained("bert-base-uncased")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)

    # Parse input arguments for sentences
    sentence1, sentence2 = sys.argv[1:sys.argv.index(",")], sys.argv[sys.argv.index(",")+1:]
    sentence1, sentence2 = " ".join(sentence1), " ".join(sentence2)
    sentences = [sentence1, sentence2]

    # Tokenize each sentence and pad tokens
    inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
    
    # Get the output from the model
    with torch.no_grad():
        output = model(**inputs)
    
    # Max pooling representation
    pool_vectors = torch.max(output.last_hidden_state, dim=1).values
    
    # CLS token representation
    cls_vectors = output.last_hidden_state[:, 0, :]

    # Compute cosine similarity
    cosine_pooling = cosine_similarity(pool_vectors[0], pool_vectors[1], dim=0)
    cosine_cls = cosine_similarity(cls_vectors[0], cls_vectors[1], dim=0)
    
    # Print results rounded to 2 decimals
    print(np.round(cosine_pooling.item(), 2), np.round(cosine_cls.item(), 2))
