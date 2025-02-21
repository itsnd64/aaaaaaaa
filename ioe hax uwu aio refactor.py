#TODO: add usage of token as input

HEADERS = {"Content-type": "application/json", "Accept": "text/plain","Accept-Encoding": "gzip, deflate"}

from time import time, sleep
_time = time()

import requests,json,os,subprocess,argparse

# Arguments parsings
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help="Print debug messages")
parser.add_argument('-vb', action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-nc', "--no_cls", action='store_true', help="Never clear the screen")
args = parser.parse_args()
dprint = lambda msg: print(msg) if args.debug else None
vdprint = lambda msg: print(msg) if args.vb else None
cls = lambda: os.system("cls" if os.name == 'nt' else "clear") if not args.no_cls else None
vdprint(f"import + parse args: {time()-_time:.4f}s");_time = time()

# Setup working dir
# TODO: handle edge cases
temp_dir = os.path.join(os.getenv('TEMP'), 'ligma balls')

if not os.path.exists(temp_dir):os.mkdir(temp_dir)
os.chdir(temp_dir)
dprint(f'Temp dir: {temp_dir}')
vdprint(f'setup: {time() - _time:.4f}s');_time = time()

# Getting getinfo/startgame/token
try:inp = input("yo gimme getinfo/startgame ")#change thissssssssss
except Exception as e:exit(f'Invalid input: {e}')

# Process Input
if len(inp) == 32:# Process Token
    dprint("Got Token")
    data = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo", headers=HEADERS, json={"api_key": "gameioe","serviceCode": "IOE","token": inp,"IPClient": "","deviceId": ""}).text)
    token = inp
    api_key = "gameioe"
    examKey = data["data"]["game"]["examKey"]
elif inp.isdigit():exit("wtf r u trying to do?")
else:
    try:input_json = json.loads(inp) 
    except Exception as e:exit(f'Invalid input: {e}')

    # Process getinfo/startgame
    try:input_json["api_key"] # getinfo dont have api_key element
    except KeyError: # handle getinfo
        dprint("Got getinfo")
        token = input_json["data"]["token"]
        api_key = "gameioe"
        examKey = input_json["data"]["game"]["examKey"]
        data = input_json
        # Start the game
        print("Starting the game")
        requests.post("https://api-edu.go.vn/ioe-service/v2/game/startgame", headers=HEADERS, json={"api_key": api_key,"token": token, "gameId":0, "examKey": examKey, "IPClient": "","deviceId": ""})
    else: # handle startgame
        dprint("Got startgame")
        token = input_json["token"]
        api_key = input_json["api_key"]
        examKey = input_json["examKey"]
        data = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo", headers=HEADERS, json = {"IPClient": "","deviceId": "","api_key": api_key,"token": token}).text)
cls()

try:
    questions = data["data"]["game"]["question"]
    quesnum = len(questions)
except TypeError:
    print("Token ko hợp lệ")
    exit()
cls()

def waitUntil10s():
    """Wait until test time >= 10s so IOE will accept finishgame\n\nThis actually wait for 6/10s depend on test type despite the function name"""
    res = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo", headers=HEADERS, json = {"IPClient": "","deviceId": "","api_key": api_key,"token": token}).text)
    # yes this code can be shorten but idc
    testTime = res["data"]["examTime"]
    esTime = 1200 - testTime
    targetTime = 6 if "Answer the questions correctly to help Edna the starfish solve a jigsaw puzzle." in res["data"]["gameDesc"] else 10
    waitTime = max(0, targetTime - esTime)
    dprint(f'Test time: {esTime}s, Target Time: {targetTime}s, will wait for {waitTime}s')
    while waitTime: # idk y i wrote this :))))))) (just wrote this)
        dprint(waitTime)
        waitTime -= 1
        sleep(1)

def checkans(ans: str = "", qid: int = 0, point: int = 10):
    """Return True if answer is correct using IOE's API"""
    return requests.post("https://api-edu.go.vn/ioe-service/v2/game/answercheck", headers=HEADERS, json={"IPClient": "", "deviceId": "", "serviceCode": "IOE", "api_key": api_key, "token": token, "examKey": examKey,"ans": {"questId": qid, "point": point, "ans": ans}}).json()["data"]["point"] == point

def finishgame(ans_list: list[dict]):
    waitUntil10s()
    vdprint(ans_list)
    res = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/finishgame",json={"api_key": api_key, "token": token, "serviceCode": "IOE", "examKey": examKey, "ans": ans_list},).text) 
    vdprint(res)
    if res["IsSuccessed"]:print(f'Điểm: {res["data"]["totalPoint"]}\nThời gian: {res["data"]["time"]}s')
    else:print("Something goes wrong while finishing the game!")

# Small stuffs,idk if i should use lambda for this
def getQID(i):return data["data"]["game"]["question"][i]["id"]
def getAnswers(i):return data["data"]["game"]["question"][i]["ans"]
def getQuestion(i):return data["data"]["game"]["question"][i]["content"]["content"]

listAns = []
def addAns(ans, qid, point):listAns.append({"ans": ans, "questId": qid, "point": point})

# Auto test solving functions
def baibth():
    for i in range(quesnum):
        print(f'Tìm đáp án câu {i + 1}')
        qid = getQID(i)
        answers = getAnswers(i)
        for j in range(len(answers)):
            ans = answers[j]["content"]
            if checkans(ans, qid):
                addAns(ans, qid, 10)
                dprint(ans)
                break
    print("Gửi chuỗi json tạo được")
    finishgame(listAns)

def baighepcap():
    listAns = []
    for i in range(quesnum):addAns(getQID(i), getQuestion(i) + "|" + getAnswers(i)[0]["content"], 10)
    print("Gửi chuỗi json tạo được")
    finishgame(listAns)

def baitf():
    listAns = []
    answers = ["True", "False"]
    for i in range(quesnum):
        print(f'Tìm đáp án câu {i + 1}')
        qid = getQID(i)
        for ans in answers:
            if checkans(ans, qid):
                addAns(ans, qid, 10)
                dprint(ans)
                break
    print("Gửi chuỗi json tạo được")
    finishgame(listAns)

def baisapxep():
    listAns = []
    for i in range(quesnum):
        answers = sorted(getAnswers(i), key=lambda x: x["orderTrue"])
        ans = "|".join([answer["content"] for answer in answers])
        listAns.append({"questId": getQID(i), "ans": ans, "Point": 10})
    finishgame(listAns)


desc = data["data"]["gameDesc"]
if   "Answer the questions correctly to help Edna the starfish solve a jigsaw puzzle" in desc:baighepcap()
elif "IOE's jewels are lost at sea! Accompany with Dai the octopus to collect them a" in desc:baisapxep()
elif "You're running a marathon. Let's race to reach the finish line as quickly as p" in desc:baibth()
elif "Dai the octopus is sailing his boat to different islands. Let's help him overc" in desc:baibth()
elif "You're on a skateboard. Your mission is skateboarding a halfpipe to get the se" in desc:baibth()
elif "The coral reefs have been destroyed; the dolphin Hubert and his friends in the" in desc:
    if len(getAnswers(0)) == 1:baitf()
    else:baibth()