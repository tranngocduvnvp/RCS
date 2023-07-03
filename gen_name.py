from vn_fullname_generator import generator
import random
import pandas as pd

list_name = []
for i in range(100):
    name = generator.generate()
    list_name.append(name)
    list_frame = pd.DataFrame({"name":list_name})
    list_frame.to_excel("./result/name_gen.xlsx", index = False)

'Trần Văn Minh'