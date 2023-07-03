import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import warnings
warnings.filterwarnings('ignore')

from utils import *

df = pd.read_csv('./data/data_processed.csv')




joined = df[['user_id', 'major_id_encode', 'isLike']]
pivot = pd.pivot_table(joined, index='major_id_encode', columns='user_id', values='isLike')
pivot_norm = pivot.apply(lambda x: x - np.nanmean(x), axis=1) #ma tran (ma nganh, user)
pivot_norm.fillna(0, inplace=True)
item_sim_df = pd.DataFrame(cosine_similarity(pivot_norm, pivot_norm), index=pivot_norm.index, columns=pivot_norm.index)


def get_final_list_major(holuc, tinhcach, list_nv, n_output = 5):
    
    list_id_major = check_list_major_id(list_nv) #ma nganh
    if len(list_id_major)== 0 :
        return None
    
    df_1 = get_similar_list_major(list_id_major, pivot_norm, item_sim_df) #loc cong tac
    n = n_output - len(df_1)
    df_2 = knn_recoment(n, holuc, tinhcach) #contenr-based
    if len(df_1) == 0:
        df = df_2
    else:
        df = pd.concat([df_1[['major_id','Uni', 'Major', 'score']], df_2])
    df.reset_index(drop=True, inplace=True)
    
    # print(df)

    df_result = block_recoment(df, list_nv)[['Uni', 'Major', 'block', 'score']]
    # df_result.to_excel('./result/result_recoment.xlsx', index = False)
    return df_result


if __name__ == '__main__':

    list_frame = []
    dataframe = pd.read_excel("./data/Survey_data_new.xlsx",\
                              sheet_name=["data","aspiration"])
    data = dataframe["data"]
    aspiration = dataframe["aspiration"]
    for i in range(0, len(data)):
        id = data.iloc[i]["id"]
        name = data.iloc[i]["name"]
        holuc = data.iloc[i]["academic"]
        tinhcach = data.iloc[i]["personality"]

        nv = aspiration[aspiration["id_data"]==id]
        nv_list = []
        for item in range(0, len(nv)):
            uni = nv.iloc[item]["university"]
            major = nv.iloc[item]["major"]
            block = nv.iloc[item]["block"]
            is_like = nv.iloc[item]["isLike"]
            nv_list.append([uni, major, block, is_like])
        # print(f"========= nguyen vong de xuat cho user {i} ================")
        # if i == 4:
        #     print(i)
        df = get_final_list_major(holuc, tinhcach, nv_list)
        if df is not None:
            # print(df)
            list_frame.append(df)
            result_frame = pd.concat(list_frame)
            result_frame.to_csv("./result/result_recoment.csv", index=False)
            result_frame.to_excel("./result/result_recoment.xlsx", index=False)

        

 
    # df = get_final_list_major(holuc, tinhcach, list_nv)
    # print(df)

    # hovaten = 'Nguyễn Văn A'
    # holuc = 'Giỏi'
    # tinhcach = 'ENFJ-A'

    # # NV1
    # uni_1 = "Học viện Âm nhạc Quốc gia Việt Nam"
    # major_1 = "Âm nhạc học"  #a
    # block_1 = "N"
    # islike_1  = "Rất thích"

    # # NV2
    # uni_2 = "Học viện Báo chí và Tuyên truyền"
    # major_2 = "Chính trị phát triển" #b
    # block_2 = "A16"
    # islike_2 = "Thích"

    # # NV3
    # uni_3 = "Đại học Bách khoa Hà Nội"
    # major_3 = "Toán - Tin"
    # block_3 = "A00"
    # islike_3 = "Rất thích"