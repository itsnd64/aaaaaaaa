#TODO: only import and setup api key is request specific tests
#TODO: u can bruteforce bai ghep cap :))))))
#TODO: wtf bai ghep cap alr provide ans??????
#TODO: check bai ghep cap+img
#TODO: startgame's responce is datetime
#TODO: send startgame after getinfo so time is 0s

from time import time
t = time()
import requests,json,os,subprocess,argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug_lvl", type=int, choices=range(0, 3), default=1, help="debug lvl thing")
parser.add_argument("-b1", "--b1", action='store_true', help="b1")
parser.add_argument("-b2", "--b2", action='store_true', help="b2")
parser.add_argument('-vb', "--verbose_output_hehe", action='store_true', help=argparse.SUPPRESS)
args = parser.parse_args()
dprint = (lambda plvl, msg: print(msg) if plvl <= args.debug_lvl else None) if args.debug_lvl else (lambda _: None)
vdprint = lambda msg: print(msg) if args.verbose_output_hehe else None

vdprint(f"import + parse args: {time()-t:.4f}s");t = time()


#FIXME: if openaikey.txt doesnt exist but ligmaballs dir exist will cause a double exception
main_dir = os.path.join(os.getenv('TEMP'),'ligma balls')
if not os.path.exists(main_dir):os.mkdir(main_dir)
os.chdir(main_dir)
dprint(2, f'Working dir:{main_dir}')
try:openaikey = open('bin\\OpenAI key.txt', 'r').read()
except FileNotFoundError:#first run setuppppppp
    bin_dir = os.path.join(main_dir,'bin')
    os.mkdir(bin_dir)
    open(os.path.join('bin','OpenAI key.txt'), 'w').write(input("Hãy nhập OpenAI API Key của bạn "))
openaikey = open(os.path.join('bin','OpenAI key.txt'),'r').read()
if not openaikey:open(os.path.join('bin','OpenAI key.txt'), 'w').write(input("Hãy nhập OpenAI API Key của bạn "))

vdprint(f"setup: {time()-t:.4f}s");t = time()

from openai import OpenAI
import assemblyai as aai
client = OpenAI(api_key=openaikey)
client.api_key = openaikey
aai.settings.api_key = "7f3e7dc553424aa69ac6bac196daa1e9"   #sorry myself,hope this wont cause too much trouble
vdprint(f"api key: {time()-t:.4f}s");t = time()

def timer(f):
    def w(*args, **kwargs):t = time(); r = f(*args, **kwargs);print(f"{f.__name__}() took {time()-t:.4f}s"); return r
    return w


try:
    input1 = input("smthing idk?")#.translate(str.maketrans({"“": " ", "”": " ", "’": " ", "–": " "}))
    os.system("cls")
    print(input1)
    input_thing = json.loads(input1)
except Exception as e:exit(f"invalid input: {e}")

headers = {"Content-type": "application/json", "Accept": "text/plain","Accept-Encoding": "gzip, deflate"}

try:input_thing["api_key"]#FIXME: organize this better
except KeyError:#handle getinfo
    print("Got getinfo")
    token = input_thing["data"]["token"]
    examKey = input_thing["data"]["game"]["examKey"]
    api_key = "gameioe"
    r = input_thing
    #post a start game thing to start it
    requests.post("https://api-edu.go.vn/ioe-service/v2/game/startgame",headers=headers,data=json.dumps({"api_key": api_key,"token": token, "gameId":0, "examKey": examKey, "IPClient": "","deviceId": "",}),)
else:#handle startgame
    print("Got startgame")
    token = input_thing["token"]
    api_key = input_thing["api_key"]
    examKey = input_thing["examKey"]
    r = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo",headers=headers,data=json.dumps({"IPClient": "","deviceId": "","api_key": api_key,"token": token}),).text)

try:
    questions = r["data"]["game"]["question"]
    quesnum = len(questions)
    os.system("cls")
except TypeError:
    print("Token ko hợp lệ")
    exit()


def checkans(ans :str = "",qid :str = "",point :int = 10,isfinishgame :bool = False,fans :str = ""):
    """Finishgame syntax:{"ans": ans,"qid": qid,"point": 10/20/etc},..."""#weird
    if isfinishgame:
        finishgamejson = {
            "api_key": api_key,
            "token": token,
            "serviceCode": "IOE",
            "examKey": examKey,
            "ans": json.loads(f'[{fans}]')
        }
        # print(finishgamejson)
        r3 = json.loads(requests.post(
        "https://api-edu.go.vn/ioe-service/v2/game/finishgame",
        json=finishgamejson,
    ).text) 
        vdprint(r3)
        if r3["IsSuccessed"]:
            print(f'Điểm: {r3["data"]["totalPoint"]}\nThời gian: {r3["data"]["time"]}s')
        else:
            vdprint(r3)
    else:
        jsonans = {
        "IPClient": "",
        "deviceId": "",
        "serviceCode": "IOE",
        "api_key": api_key,
        "token": token,
        "examKey": examKey,
        "ans": {"questId": qid, "point": point, "ans": ans},
    }
        r2 = requests.post(
            "https://api-edu.go.vn/ioe-service/v2/game/answercheck",
            headers=headers,
            data=json.dumps(jsonans),
        )
        return json.loads(r2.text)["data"]["point"] == 10

def sendmsg(prompt):
    print(prompt)
    completion = client.completions.create(model="gpt-3.5-turbo-instruct",prompt=prompt,max_tokens=600,temperature=0)
    return completion.choices[0].text

@timer
def aaiTrans(path):
    vdprint(f"aai transcripting: {path}")
    res = aai.Transcriber().transcribe(path).text
    print(res)
    vdprint(f"aai transcripting done")
    return res

# TODO: remove this function,it sucks
def jsonStrHandler(astr):return astr if astr and astr[0] == '"' and astr[-1] == '"' else astr.replace('"', '\\"') if '"' in astr else f'"{astr}"'

@timer
def baibth():
    fans = ""
    for i in range(quesnum):
        print("Tìm đáp án câu" + " " + str(i+1))
        qid = r["data"]["game"]["question"][i]["id"]
        answers = r["data"]["game"]["question"][i]["ans"]
        for i in range(len(answers)):
            ans = answers[i]["content"]
            if checkans(ans,qid,10):
                fans += f'{{"ans": {jsonStrHandler(ans)},"questId": "{qid}","point": 10}},'
                vdprint(jsonStrHandler(ans))
                break
    print("Gửi chuỗi json tạo được")
    vdprint(fans[:-1])
    checkans(isfinishgame=True,fans=fans[:-1])
    
@timer
def baitf():
    fans = ""
    for i2 in range(quesnum):
        qid = r["data"]["game"]["question"][i2]["id"]
        answers = [{"content": "True"}, {"content": "False"}]
        for i in range(2):
            ans = answers[i]["content"]
            if checkans(ans,qid,10):
                fans += f'{{"ans": {jsonStrHandler(ans)},"questId": "{qid}","point": 10}},'
                break
    print(fans[:-1])
    checkans(isfinishgame=True,fans=fans[:-1])

def baichontu(isTF :bool = False):
    for i2 in range(quesnum):
        qid = r["data"]["game"]["question"][i2]["id"]
        if isTF:answers = [{"content": "True"}, {"content": "False"}]
        else:answers = r["data"]["game"]["question"][i2]["ans"]
        for i in range(len(answers)):
            ans = answers[int(i)]["content"]
            if checkans(ans,qid,10):
                print(str(i2 + 1) + "." + ans)
                break


def sortcri(l):return l["orderTrue"]
def baisapxep():
    fans = ''
    for i in range(quesnum):
        answers = r["data"]["game"]["question"][i]["ans"]
        answers.sort(key=sortcri)
        ans = ''
        for j in range(len(answers)):ans += answers[j]["content"] + ' '
        ans = "|".join(ans)[:-2]
        qid = r["data"]["game"]["question"][i]["id"]
        fans += f'{{"questId": {qid}, "ans": "{ans}", "Point": 10}},'
    checkans("","",0,True,fans[:-1])



#functions for listening test
#TODO: organize this shit
temp_dir = os.path.join("bin","temp")
output_file = os.path.join(temp_dir,"output.mp3")
def temp_init():
    if not os.path.exists(temp_dir):os.makedirs(temp_dir);print(f'Đã tạo: {temp_dir}')
    else:print(f'dir alr exist')
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
            print(f'Deleted {file_path}')
def dlaudio(url, savepath):
    vdprint(f"download: {url} to {savepath}")
    response = requests.get(url, stream=True)
    with open(savepath, 'wb') as audiofile:
        for chunk in response.iter_content(chunk_size=1024):audiofile.write(chunk)
    vdprint(f"download {url} done")
def readaudio(filepath):
    audio_file= open(filepath, "rb")
    return client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )[:-1]
def stupiddiff(a, b):#i should've use set() but it works anyway
    diff = ''
    for a,b in zip(a,b):
        if a != b:diff += a
    return diff

qids = []
questions = []

@timer
def baiheo():#ioe_game_16
    print("Lưu ý:Bài được làm bởi AI(ChatGPT) nên sai sót không thể tránh khỏi")
    answers = ''
    ques = r["data"]["game"]["Subject"]["content"]
    qid = r["data"]["game"]["question"][0]["id"]
    for i in r["data"]["game"]["question"][0]["ans"]:answers += i["content"] + ","
    ans = sendmsg(f'{"Đọc bài văn sau"}\n{ques}\n{"Điền các từ sau vào đoạn văn cách nhau bởi dấu | chỉ cần câu trả lời"}\n{answers[:-1]}')[1:]
    fans = '|'.join([line.split('. ')[1] for line in ans.split('\n') if line])
    fans = f'{{"questId": {qid},"ans": "{fans}","Point": 100}}'
    checkans("","",0,True,fans)
@timer
def bainghe():
    temp_init()
    print("Lưu ý:Bài được làm bởi AI(Whisper) nên sai sót không thể tránh khỏi")
    for i in range(quesnum):
        qids.append(r["data"]["game"]["question"][i]["id"])
        questions.append(r["data"]["game"]["question"][i]["content"]["content"])
        dlaudio(r["data"]["game"]["question"][i]["Description"]["content"],temp_dir +"\\"+str(i)+".mp3")
        print(f'Trạng Thái: Tải xuống bài nghe {i+1}')
    print(f'Trạng Thái: Kết hợp các file mp3')
    #warn:next line is huge and stupid bc for some reason my previous beautifully code sometime doesnt work with ffmpeg
    subprocess.run('copy /b bin\\temp\\0.mp3+bin\\lol.mp3+bin\\temp\\1.mp3+bin\\lol.mp3+bin\\temp\\2.mp3+bin\\lol.mp3+bin\\temp\\3.mp3+bin\\lol.mp3+bin\\temp\\4.mp3+bin\\lol.mp3+bin\\temp\\5.mp3+bin\\lol.mp3+bin\\temp\\6.mp3+bin\\lol.mp3+bin\\temp\\7.mp3+bin\\lol.mp3+bin\\temp\\8.mp3+bin\\lol.mp3+bin\\temp\\9.mp3+bin\\lol.mp3 bin\\temp\\output.mp3', shell=True, check=True)
    result_list = [a for a in readaudio(output_file).split(" Gay. ")[:-1] if a]
    idk = []
    for a,b in zip(result_list,questions):idk.append(stupiddiff(a,b).replace('.',''))
    flist = [{"qid": qid, "ans": answer, 'point': 10} for qid, answer in zip(qids, idk)]
    fans = ""
    for item in flist:fans += f'{{"qid": {item["qid"]}, "ans": "{item["ans"]}", "point": {item["point"]}}},'
    dprint(2, fans[:-1])
    checkans(isfinishgame=True,fans=fans[:-1])

def baingheft():
    temp_init()
    print("Lưu ý:Bài được làm bởi AI(AssemblyAI) nên sai sót không thể tránh khỏi")
    for i in range(quesnum):
        qids.append(r["data"]["game"]["question"][i]["id"])
        questions.append(r["data"]["game"]["question"][i]["content"]["content"])
        dlaudio(r["data"]["game"]["question"][i]["Description"]["content"],temp_dir +"\\"+str(i)+".mp3")
        print(f'Trạng Thái: Tải xuống bài nghe {i+1}')
    print(f'Trạng Thái: Kết hợp các file mp3')
    #warn:next line is huge and stupid bc for some reason my previous beautifully code sometime doesnt work with ffmpeg
    subprocess.run('copy /b bin\\temp\\0.mp3+bin\\lol.mp3+bin\\temp\\1.mp3+bin\\lol.mp3+bin\\temp\\2.mp3+bin\\lol.mp3+bin\\temp\\3.mp3+bin\\lol.mp3+bin\\temp\\4.mp3+bin\\lol.mp3+bin\\temp\\5.mp3+bin\\lol.mp3+bin\\temp\\6.mp3+bin\\lol.mp3+bin\\temp\\7.mp3+bin\\lol.mp3+bin\\temp\\8.mp3+bin\\lol.mp3+bin\\temp\\9.mp3+bin\\lol.mp3 bin\\temp\\output.mp3', shell=True, check=True)
    result_list = [a for a in aai.Transcriber().transcribe("bin\\temp\\output.mp3").text.split(" Lol. ")[:-1] if a]
    idk = []
    for a,b in zip(result_list,questions):idk.append(stupiddiff(a,b).replace('.',''))
    flist = [{"qid": qid, "ans": answer, 'point': 10} for qid, answer in zip(qids, idk)]
    fans = ""
    for item in flist:fans += f'{{"qid": {item["qid"]}, "ans": "{item["ans"]}", "point": {item["point"]}}},'
    dprint(2, fans[:-1])
    checkans(isfinishgame=True,fans=fans[:-1])

@timer
def bailuyennghetest():
    temp_init()
    print("Lưu ý:Bài được làm bởi AI(AssemblyAI) nên sai sót không thể tránh khỏi")
    dlaudio(r["data"]["game"]["Subject"]["content"], temp_dir + "\\a.mp3")
    aaiTrans("bin\\temp\\a.mp3")
    for i in range(quesnum):
        qids.append(r["data"]["game"]["question"][i]["id"])
        questions.append(r["data"]["game"]["question"][i]["content"]["content"])
        print(r["data"]["game"]["question"][i]["content"]["content"])
        answers = r["data"]["game"]["question"][i]["ans"]
        for i in range(len(answers)):
            ans = answers[i]["content"]
            print("\t" + ans)

#TODO: add output to autobaitf()
desc = r["data"]["gameDesc"]
if "The coral reefs have been destroyed; the dolphin Hubert" in desc:
    # if len(r["data"]["data"]["game"]["question"][0]["ans"]) == 4:baibth()
    # else:baitf()
    baibth()
    # baitf()
elif "IOE's jewels are lost at sea! Accompany with Dai the " in desc:baisapxep()
elif "You are on the way to reach the top of Mount Fansipan" in desc:baibth()
elif "A pink pig's island is in danger! Help him to defend " in desc:baiheo()
elif "The beach is full of trash. Join IOE's team now to cl" in desc:baibth()
# elif "Caradoc the crab is doing his homework. Join him and " in desc:bailuyennghetest()
else:print("prob unsupported")