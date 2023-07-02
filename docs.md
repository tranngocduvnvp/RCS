# 1. Clone repo 
```
git clone https://github.com/tranngocduvnvp/RCS.git
cd RCS
```
# 2. Run tren local
## 2.1 Chay file main de test
```
python main.py
```
## 2.1 Chay server

```
uvicorn --port 8080  app:app --reload
```

## 2.2 Chay docker
Neu chon cach nay thi cach 2.1 ko can su dung. 

```
docker run --rm -p 8080:8000  tranngocdu/rc_project
```

## 2.3 Chay file request de call server

```
python request.py
```
