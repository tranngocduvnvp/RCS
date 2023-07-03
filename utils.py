import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Load model
def load_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

knn_model = load_model('./model/knn.pkl')

data_process = pd.read_csv('./data/data_processed.csv')
data_process = data_process.drop_duplicates(subset=["user_id"], keep='first', inplace=False)

# Khai báo
major_id_arr = ['-1', '537', '615', '7140114D', '7140201A', '7140202A', '7140209A',
       '7140211B', '7140217D', '7140231', '7140231A', '7210403',
       '7210404', '7220201', '7220202', '7220204', '7220209', '7310101_1',
       '7310104', '7310106', '7310108', '7320104', '7340101', '7340115',
       '7340116', '7340120', '7340201', '7340201C09', '7340201C11',
       '7340201_NH', '7340201_TC', '7340301', '7340301C21', '7340302',
       '7340401', '7340409', '7380101', '7380107', '7420201', '7480201',
       '7510302', '7510605', '7520121', '7580101', '7580201_01',
       '7580301', '7580302_01', '7720101', '7720101YHT', '7720115',
       '7720201', '7720301', '7720501', '7720699', '7810201', '7850103',
       '7860100', 'BF1y', 'BF2y', 'CH1Y', 'CN1', 'CN12', 'CN14', 'CN17',
       'CN2', 'CN8', 'EBBA', 'EE-E8y', 'EE-Epy', 'EE1y', 'EE2y',
       'EM-E14y', 'EM3y', 'EM4y', 'EP02', 'EP14', 'ET-E4y', 'ET-E5y',
       'ET-LUHY', 'FL1y', 'FL2y', 'GD1', 'GD2', 'HQT01', 'HQT02', 'HQT03',
       'HQT05', 'HVN02', 'HVN03', 'HVN06', 'HVN07', 'HVN16', 'HVN20',
       'HVN23', 'Hóa học', 'IT - E10x', 'IT - E7x', 'IT- 1x', 'IT- E15x',
       'IT- EPx', 'IT-E6y', 'IT2y', 'ME-LUHy', 'ME-NUTy', 'ME1y', 'ME2y',
       'MI1y', 'MI2y', 'NTH01-01', 'NTH01-02', 'NTH02', 'NTH03', 'NTH07',
       'QHT96', 'QHX01', 'QHX05', 'QHX07', 'QHX14', 'QHX16', 'TE-Epy',
       'TE1y', 'TE2y', 'TE3y', 'TLA106', 'TLA107', 'TLA119', 'TM01',
       'TM04', 'TM22', 'TROY-Bay']

hocluc_arr = ['Giỏi', 'Khá', 'Trung bình', 'Xuất sắc', 'Yếu']

tinhcach_arr = ['ENFJ-A', 'ENFJ-T', 'ENFP-A', 'ENFP-T', 'ENTJ-A', 'ENTJ-T',
       'ENTP-A', 'ENTP-T', 'ESFJ-A', 'ESFJ-T', 'ESFP-A', 'ESFP-T',
       'ESTJ-A', 'ESTJ-T', 'ESTP-A', 'ESTP-T', 'INFJ-A', 'INFJ-T',
       'INFP-A', 'INFP-T', 'INTJ-A', 'INTJ-T', 'INTP-A', 'INTP-T',
       'ISFJ-A', 'ISFJ-T', 'ISFP-A', 'ISFP-T', 'ISTJ-A', 'ISTJ-T',
       'ISTP-A', 'ISTP-T']


# Đọc dữ liệu
df_uni_major = pd.read_excel('./data/Data_Uni.xlsx', sheet_name='Uni_major', dtype={'ID_major': str})
df_uni = pd.read_excel('./data/Data_Uni.xlsx', sheet_name='UNI')


def get_similar_major(major_id, pivot_norm, item_sim_df):
    try:
        index_major_id = major_id_arr.index(str(major_id))
    except:
        # print("Không tìm thấy mã ngành trong danh sách tham chiếu")
        pass
    if index_major_id not in pivot_norm.index:
        return None, None
    else:
        #a = [4,3,2,1]
        sim_major = item_sim_df.sort_values(by=index_major_id, ascending=False).index[1:]
        sim_score = item_sim_df.sort_values(by=index_major_id, ascending=False).loc[:, index_major_id].tolist()[1:]
        return sim_major, sim_score


def convert_major_index_2_uni_major(major_index):
    major_id = major_id_arr[major_index]
    if major_id == "-1":
        return None, None
    try:
        major = df_uni_major.loc[df_uni_major['ID_major'] == major_id]['Major'].values[0]
        uni_id = df_uni_major.loc[df_uni_major['ID_major'] == major_id]['ID_uni'].values[0]
    except:
        pass

    uni = df_uni.loc[df_uni['ID'] == uni_id]['Uni'].values[0]

    return uni, major


def get_similar_list_major(list_major_id, pivot_norm, item_sim_df):
    """
    Get a list of similar majors based on the given list of major IDs.
    
    Parameters:
        - list_major_id (list): danh sach ma nganh
        - pivot_norm (pandas.DataFrame): ma tran pivot
        - item_sim_df (pandas.DataFrame): ma tran item similarity
        
    Returns:
        - df_result_all (pandas.DataFrame): A dataframe containing the list of similar majors.
    """
    result_all = []
    for major_id in list_major_id:
        try:
            sim_major, sim_score = get_similar_major(major_id, pivot_norm, item_sim_df)
        except:
            continue
        for i in range(0, len(sim_score)):
            if sim_score[i] > 0:
                uni, major = convert_major_index_2_uni_major(sim_major[i])
                if uni == None:
                    continue
                result = {
                    'major_id': major_id,
                    'Uni': uni,
                    'Major': major,
                    'score': f"{sim_score[i]:.5f} (c)", #sim_score[i]
                }
                result_all.append(result)
    result_all = result_all[:5]
    df_result_all = pd.DataFrame(result_all)
    # print(df_result_all)
    # df_final = pd.DataFrame(df_result_all.groupby(['Uni', 'Major'])['score'].sum())
    return df_result_all  


def check_major_id(arr_nv):
    name_uni = arr_nv[0]
    name_major = arr_nv[1]
    id_uni = df_uni.loc[df_uni['Uni'] == name_uni]['ID'].values[0]
    df_tmp = df_uni_major.loc[df_uni_major['ID_uni'] == id_uni]
    id_major = df_tmp.loc[df_tmp['Major'] == name_major]['ID_major'].values[0]

    return str(id_major)


def check_list_major_id(list_arr_nv):
    list_id_major = []
    for arr_nv in list_arr_nv:
        try:
            id_major = check_major_id(arr_nv)
            list_id_major.append(id_major)
        except:
            # print("Không tìm thấy mã ngành trong danh sách tham chiếu")
            pass
    
    return list_id_major


def knn_recoment(n, holuc, tinhcach):
    result_all = []
    count = 1
    hocluc_index = hocluc_arr.index(holuc)
    tinhcach_index = tinhcach_arr.index(tinhcach)
    x = [[hocluc_index, tinhcach_index]]
    distances, indices = knn_model.kneighbors(x)
    # print("distances:",distances)
    # indices_in = indices[indices < len(major_id_arr)]
    indices_in = indices[0]
    try:
        list_major_id_encode = list(indices_in[0:-1]) #danh sach nhung nguoi gan nhat
        list_major_id_encode = [data_process.iloc[idx]["major_id_encode"] \
                                for idx in list_major_id_encode]

    except:
        list_major_id_encode = indices_in
    for major_id_encode in list_major_id_encode:
        if count > n:
            break
        uni, major = convert_major_index_2_uni_major(major_id_encode)
        if uni == None:
            continue
        major_id = major_id_arr[major_id_encode]
        result = {
            'major_id': major_id,
            'Uni': uni,
            'Major': major,
            'score': f"{distances[0][count-1]:.5f} (d)"
        }
        result_all.append(result)
        count +=1
    df_result_all = pd.DataFrame(result_all)
    return df_result_all
        

def block_recoment(df, list_arr_nv):
    # Lấy danh sách các ngành mà HS đã chọn
    block_choise_arr = []
    for nv in list_arr_nv:
        block_choise_arr.append(nv[2])

    df['block'] = None
    for i in range(0, len(df)):
        block_choise_in_uni = block_choise_arr[0] #khoi trong nguyen vong ban dau
        block_list_uni = list(df_uni_major.loc[df_uni_major['ID_major'] == str(df['major_id'][i])]['Block'].values)
        # print("block_list_uni:",block_list_uni)
        # print(", df['major_id'][i]:",df['major_id'][i])
        block_list_uni = block_list_uni[0].split(', ') #[D, C] khoi that di kem voiw nganh
        for block_choise in block_choise_arr:
            if block_choise in block_list_uni:
                block_choise_in_uni = block_choise
                break
            else:
                block_choise_in_uni = block_list_uni[0]
                continue
        df['block'][i] = block_choise_in_uni
    
    return df



if __name__ == '__main__':
    hovaten = 'Nguyễn Văn A'
    holuc = 'Giỏi'
    tinhcach = 'ENFJ-A'

    # NV1
    uni_1 = "Học viện Âm nhạc Quốc gia Việt Nam"
    major_1 = "Âm nhạc học"
    block_1 = "N"
    islike_1  = "Rất thích"

    # NV2
    uni_2 = "Học viện Báo chí và Tuyên truyền"
    major_2 = "Chính trị phát triển"
    block_2 = "A16"
    islike_2 = "Thích"

    # NV3
    uni_3 = "Học viện Báo chí và Tuyên truyền"
    major_3 = "Tư tưởng Hồ Chí Minh"
    block_3 = "A16"
    islike_3 = "Rất thích"

    nv1 = [uni_1, major_1, block_1, islike_1]
    nv2 = [uni_2, major_2, block_2, islike_2]
    nv3 = [uni_3, major_3, block_3, islike_3]

    list_nv = [nv1, nv2, nv3]

   

    n = 5
    df_2 = knn_recoment(n, holuc, tinhcach)
    print(df_2)