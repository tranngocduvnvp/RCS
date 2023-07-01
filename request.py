import requests


url = "http://127.0.0.1:8000/predict"

hovaten = input("Ho va ten:")
hocluc = input("Hoc luc:")
tinhcach = input("Tinh cach:")


info_person = {
    "hovaten": hovaten,
    "hocluc": hocluc,
    "tinhcach": tinhcach
}

print("======== Nhap danh sach nguyen vong: ==================")
nv = []
while 1:
    uni = input("Uni:")
    major = input("Major:")
    block = input("Block:")
    islike = input("Islike:")

    nv.append({
        "uni": uni,
        "major": major,
        "block": block,
        "islike": islike
    })
    check = input("Check again? (y/n):")
    if check == "n":
        break


payload = {"info_person": info_person, "nv": nv}

response = requests.post(url, json=payload)

result = response.json()

# print(result)

data_list_proposal = []
for i in range(len(result["Uni"])):
    uni = result["Uni"][str(i)]
    major = result["Major"][str(i)]
    block = result["block"][str(i)]
    data_list_proposal.append([uni, major, block])

print(data_list_proposal)



# info_person = {
#     "hovaten": "tran ngoc du",
#     "hocluc": "Giỏi",
#     "tinhcach": "ENFJ-A"
# }


# nv = [
#     {
#       "uni": "Học viện Âm nhạc Quốc gia Việt Nam",
#       "major": "Âm nhạc học",
#       "block": "N",
#       "islike": "Rất thích"
#     },
#     {
#       "uni": "Học viện Báo chí và Tuyên truyền",
#       "major": "Chính trị phát triển",
#       "block": "A16",
#       "islike": "Thích"
#     },
#     {
#       "uni": "Đại học Bách khoa Hà Nội",
#       "major": "Toán - Tin",
#       "block": "A00",
#       "islike": "Rất thích"
#     }
# ]
