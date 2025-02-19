from time import time, sleep
_time = time()

import requests,json,os,subprocess,argparse

# Arguments parsings
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug_lvl', type=int, choices=range(0, 3), default=1, help="debug lvl thing")
parser.add_argument('-vb', action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-nc', "--no_cls", action='store_true', help="Never clear the screen")
args = parser.parse_args()
dprint = (lambda plvl, msg: print(msg) if plvl <= args.debug_lvl else None) if args.debug_lvl else (lambda _: None)
vdprint = lambda msg: print(msg) if args.vb else None
cls = lambda: os.system("cls" if os.name == 'nt' else "clear") if not args.no_cls else None
vdprint(f"import + parse args: {time()-_time:.4f}s");_time = time()

# Setup working dir
# TODO: handle edge cases
main_dir = os.path.join(os.getenv('TEMP'),'ligma balls')

if not os.path.exists(main_dir):os.mkdir(main_dir)
os.chdir(main_dir)
dprint(2, f'Working dir:{main_dir}')
vdprint(f"setup: {time() - _time:.4f}s");_time = time()

# Getting getinfo/startgame
try: input_json = json.loads(input("smthing idk? "))  
except Exception as e: exit(f'Invalid input: {e}')
cls()

# Processing getinfo/startgame
HEADERS = {"Content-type": "application/json", "Accept": "text/plain","Accept-Encoding": "gzip, deflate"}
try:input_json["api_key"] # getinfo doesnt have api_key element
except KeyError: # handle getinfo
    print("Got getinfo")
    token = input_json["data"]["token"]
    api_key = "gameioe"
    examKey = input_json["data"]["game"]["examKey"]
    data = input_json
    # Start the game
    requests.post("https://api-edu.go.vn/ioe-service/v2/game/startgame", headers=HEADERS, json={"api_key": api_key,"token": token, "gameId":0, "examKey": examKey, "IPClient": "","deviceId": ""})
    print("Game Started!")
    # startTime = 0
else: # handle startgame
    print("Got startgame")
    token = input_json["token"]
    api_key = input_json["api_key"]
    examKey = input_json["examKey"]
    data = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo", headers=HEADERS, json = {"IPClient": "","deviceId": "","api_key": api_key,"token": token}).text)
    # startTime = 1200 - data["data"]["examTime"] #FIXME: THIS IS FIXEDDDDDDDDDDDD,mb wrong

try:
    questions = data["data"]["game"]["question"]
    quesnum = len(questions)
except TypeError:
    print("Token ko hợp lệ")
    exit()
cls()

def checkans(ans: str = "", qid: int = 0, point: int = 10):
    """Return True if answer is correct using IOE's API"""
    return requests.post("https://api-edu.go.vn/ioe-service/v2/game/answercheck", headers=HEADERS, json={"IPClient": "", "deviceId": "", "serviceCode": "IOE", "api_key": api_key, "token": token, "examKey": examKey,"ans": {"questId": qid, "point": point, "ans": ans}}).json()["data"]["point"] == point
def finishgame(ans_list: list[dict]):
    vdprint(ans_list)
    res = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/finishgame",json={"api_key": api_key, "token": token, "serviceCode": "IOE", "examKey": examKey, "ans": ans_list},).text) 
    vdprint(res)
    if res["IsSuccessed"]:print(f'Điểm: {res["data"]["totalPoint"]}\nThời gian: {res["data"]["time"]}s')
    else:
        print("Something goes wrong while finishing game!")
        vdprint(res)

# Small helper functions,idk if i should use lambda for this
def getQID(i):return data["data"]["game"]["question"][i]["id"]
def getAnswers(i):return data["data"]["game"]["question"][i]["ans"]
def getQuestion(i):return data["data"]["game"]["question"][i]["content"]["content"]


# 
def baibth():
    fans = []
    for i in range(quesnum):
        print(f'Tìm đáp án câu {i + 1}')
        qid = getQID(i)
        answers = getAnswers(i)
        for j in range(len(answers)):
            ans = answers[j]["content"]
            if checkans(ans, qid):
                fans.append({"ans": ans, "questId": qid, "point": 10})
                dprint(1, ans)
                break
    print("Gửi chuỗi json tạo được")
    finishgame(fans)

def baighepcap():
    fans = []
    for i in range(6): # dw abt this
        qid = getQID(i)
        ques = getQuestion(i)
        ans = data["data"]["game"]["question"][i]["ans"][0]["content"]
        fans.append({"questId" : qid, "ans" : ques + "|" + ans, "Point": 10})
    print("Gửi chuỗi json tạo được")
    finishgame(fans)

def baitf():
    fans = []
    answers = ["True", "False"]
    for i in range(quesnum):
        print(f'Tìm đáp án câu {i + 1}')
        qid = getQID(i)
        for ans in answers:
            if checkans(ans, qid):
                fans.append({"ans": ans, "questId": qid, "point": 10})
                dprint(1, ans)
                break
    
    print("Gửi chuỗi json tạo được")
    finishgame(fans)
