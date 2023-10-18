#from transformers import pipeline
#import time
#fill_masker = pipeline(model="bert-base-uncased", task="fill-mask")
def mult(l):
    if len(l) == 1:
        return l[0]
    else:
        l1 = l[0]
        l2 = l[1]
        m = []
        for i in range(len(l1)):
            for j in range(len(l2)):
                n = []
                n.append(l1[i][0]*l2[j][0])
                n += l1[i][1:]
                n += l2[j][1:]
                m.append(n)
        l.append(m)
        return mult(l[2:])
def most_likely_completion(target_words, sentence, fill_masker, hole = 0):
    #start_time = time.time()
    if len(sentence) > 512:
        sentence = sentence[0:512]
        return []
    l = fill_masker(sentence, targets=target_words)
    if type(l[0]) == dict:
        l = [l]
    n_holes = len(l)
    joint = []

    for i in range(n_holes):
        l1 = []
        for pred in l[i]:
            l1.append([pred['score'], pred['token_str']])
        if l1 != []:
            joint.append(l1)
    # arr = mult(joint)
    # arr = sorted(arr, key=lambda x: x[0], reverse=True)
    completions = []
    if len(joint) > hole:
        completions = sorted(joint[hole], key=lambda x: x[0], reverse=True)
    # for i in range(5):
    #     print(f"Prediction {i+1} with a score of {arr[i][0]}:")
    #     j = 1
    #     s=""
    #     words = sentence.split(" ")
    #     for w in words:
    #         if w=="[MASK]":
    #             s+=arr[i][j] + " "
    #             j += 1
    #         else:
    #             s+=w + " "
    #     print(s[:-1])
    # print(completions)
    #end_time = time.time()
    #print("Time taken by LM: {} ms".format((end_time - start_time)*1000))
    return completions 

# most_likely_completion(["door", "box", "empty", "open", "close"],"Check if the [MASK] is [MASK] and close the door.")
"""
Only disadvantage of this approach is that joint probability assumes that these words are independent but they arent.
They have dependence. We can solve this by generating a prediction on all masks at once but that can't take targets as input.
"""


"""
Likelihood of a sentence using BERT
"""
# from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM
# import torch
# import pandas as pd
# import math	
# bertMaskedLM = BertForMaskedLM.from_pretrained('bert-base-uncased')
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# def get_score(sentence):
#     tokenize_input = tokenizer.tokenize(sentence)
#     tensor_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)])
#     predictions=bertMaskedLM(tensor_input)
#     loss_fct = torch.nn.CrossEntropyLoss()
#     loss = loss_fct(predictions.squeeze(),tensor_input.squeeze()).data 
#     return math.exp(loss)
# print("Perplexity of \" Check if the door is open and close the door. \": ",get_score("Check if the door is open and close the door."))
# print("Perplexity of \" Check if the box is open and close the door. \": ", get_score("Check if the box is open and close the door."))
# print("Perplexity of \" Check if the door is empty and close the door. \": ", get_score("Check if the door is open and close the door. "))
# print("Perplexity of \" Check if the empty is open and close the door. \": ", get_score("Check if the empty is open and close the door. "))
