from fastapi import FastAPI
from main import get_final_list_major
from typing import List
from pydantic import BaseModel

app = FastAPI()


class InfoPerson(BaseModel):
    hovaten: str
    hocluc: str
    tinhcach: str

class Nv(BaseModel):
    uni: str
    major: str
    block: str
    islike: str

@app.post("/predict")
async def predictor(info_person: InfoPerson, nv: List[Nv]):
    # print(info_person)
    info_person = dict(info_person)
    nv = [dict(item) for item in nv]
    holuc = info_person['hocluc']
    tinhcach = info_person['tinhcach']
    list_nv = []
    for item in nv:
        uni = item['uni']
        major = item['major']
        block = item['block']
        islike = item['islike']
        list_nv.append([uni, major, block, islike])
    df = get_final_list_major(holuc, tinhcach, list_nv)
    return df


if __name__ == "__main__":
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
