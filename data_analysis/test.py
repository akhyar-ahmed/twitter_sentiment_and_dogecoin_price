import pandas as pd
import numpy as np
import json

file = open("datasets/2020_full_processed.json","r", encoding= "utf8")

df = pd.read_json("datasets/2020_full_processed.json")
print(df) 