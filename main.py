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

df = pd.read_csv('/home/tran/recommeder_sys/RC/data/data_processed.csv')




joined = df[['user_id', 'major_id_encode', 'isLike']]
pivot = pd.pivot_table(joined, index='major_id_encode', columns='user_id', values='isLike')
pivot_norm = pivot.apply(lambda x: x - np.nanmean(x), axis=1) #ma tran (ma nganh, user)
pivot_norm.fillna(0, inplace=True)
item_sim_df = pd.DataFrame(cosine_similarity(pivot_norm, pivot_norm), index=pivot_norm.index, columns=pivot_norm.index)


def get_final_list_major(holuc, tinhcach, list_nv, n_output = 5):
    list_id_major = check_list_major_id(list_nv) #ma nganh
    df_1 = get_similar_list_major(list_id_major, pivot_norm, item_sim_df) #loc cong tac
    n = n_output - len(df_1)
    df_2 = knn_recoment(n, holuc, tinhcach) #contenr-based
    if len(df_1) == 0:
        df = df_2
    else:
        df = pd.concat([df_1[['major_id','Uni', 'Major']], df_2])
    df_result = block_recoment(df, list_nv)[['Uni', 'Major', 'block']]
    df_result.to_excel('/home/tran/recommeder_sys/RC/result/result_recoment.xlsx', index = False)
    return df_result


if __name__ == '__main__':
    hovaten = 'Nguyễn Văn A'
    holuc = 'Giỏi'
    tinhcach = 'ENFJ-A'

    # NV1
    uni_1 = "Học viện Âm nhạc Quốc gia Việt Nam"
    major_1 = "Âm nhạc học"  #a
    block_1 = "N"
    islike_1  = "Rất thích"

    # NV2
    uni_2 = "Học viện Báo chí và Tuyên truyền"
    major_2 = "Chính trị phát triển" #b
    block_2 = "A16"
    islike_2 = "Thích"

    # NV3
    uni_3 = "Đại học Bách khoa Hà Nội"
    major_3 = "Toán - Tin"
    block_3 = "A00"
    islike_3 = "Rất thích"

    nv1 = [uni_1, major_1, block_1, islike_1]
    nv2 = [uni_2, major_2, block_2, islike_2]
    nv3 = [uni_3, major_3, block_3, islike_3]

    list_nv = [nv1, nv2, nv3]

    df = get_final_list_major(holuc, tinhcach, list_nv)
    print(df)

    