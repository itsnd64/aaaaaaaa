# u can baibth() an khe tra vang LOL this is so funny how didnt i notice this

# Constant(s)
HEADERS = {"Content-type": "application/json", "Accept": "text/plain","Accept-Encoding": "gzip, deflate, br, zstd"}

from time import time, sleep
_time = time()
def printTime(msg):
    global _time
    vdprint(f"{msg}: {time()-_time:.4f}s")
    _time = time()

import requests, json, os, argparse

# Arguments parsings
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help="Print debug messages")
parser.add_argument('-vb', action='store_true', help=argparse.SUPPRESS)
parser.add_argument('-nc', "--no_cls", action='store_true', help="Dont clear the screen")
args = parser.parse_args()
dprint = lambda msg: print(msg) if args.debug else None
vdprint = lambda msg: print(msg) if args.vb else None
cls = lambda: os.system("cls" if os.name == 'nt' else "clear") if not args.no_cls else None # mb i should support linux
printTime("import + parse args")

# Setup working dir
# TODO: handle edge cases
temp_dir = os.path.join(os.getenv('TEMP'), 'ligma balls')

if not os.path.exists(temp_dir):os.mkdir(temp_dir)
os.chdir(temp_dir)
vdprint(f'Temp dir: {temp_dir}')
vdprint(f'setup: {time() - _time:.4f}s');_time = time()

# Setup API keys #TODO: hey refac this
if not os.path.exists("Copilot API Key.txt"):open("Copilot API Key.txt", "w").write(input("Hãy nhập Key Copilot của bạn: ").strip())
copilotKey = open("Copilot API Key.txt").read().strip()
if not os.path.exists("AssemblyAI API Key.txt"):open("AssemblyAI API Key.txt", "w").write(input("Hãy nhập Key AssemblyAI của bạn: ").strip())
AAIKey = open("AssemblyAI API Key.txt").read().strip()

# Getting getinfo/startgame/token
try:inp = input("yo gimme getinfo/startgame/token ") #change thissssssssss
except Exception as e:exit(f'Invalid input: {e}')

# Process Input
if len(inp) == 32:# Process Token
    vdprint("Got Token")
    data = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo", headers=HEADERS, json={"api_key": "gameioe","serviceCode": "IOE","token": inp,"IPClient": "","deviceId": ""}).text)
    api_key = "gameioe"
    try:
        token = data["data"]["token"]
        examKey = data["data"]["game"]["examKey"]
    except:
        print("hmm i got this:")
        print(data["message"])
        exit()
    print("Starting the game")
    requests.post("https://api-edu.go.vn/ioe-service/v2/game/startgame", headers=HEADERS, json={"api_key": api_key,"token": token, "gameId":0, "examKey": examKey, "IPClient": "","deviceId": ""})
elif inp.isdigit():exit("wtf r u trying to do?")
else:
    try:input_json = json.loads(inp) 
    except Exception as e:exit(f'Invalid input: {e}')

    # Process getinfo/startgame
    try:input_json["api_key"] # getinfo doesnt have api_key element
    except KeyError: # handle getinfo
        vdprint("Got getinfo")
        token = input_json["data"]["token"]
        api_key = "gameioe"
        examKey = input_json["data"]["game"]["examKey"]
        data = input_json
        # Start the game
        print("Starting the game")
        requests.post("https://api-edu.go.vn/ioe-service/v2/game/startgame", headers=HEADERS, json={"api_key": api_key,"token": token, "gameId":0, "examKey": examKey, "IPClient": "","deviceId": ""})
    else: # handle startgame
        vdprint("Got startgame")
        token = input_json["token"]
        api_key = input_json["api_key"]
        examKey = input_json["examKey"]
        data = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo", headers=HEADERS, json = {"IPClient": "","deviceId": "","api_key": api_key,"token": token}).text)
cls()

try:
    questions = data["data"]["game"]["question"]
    quesnum = len(questions)
    quespoint = data["data"]["game"]["question"][0]["Point"]
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
    print(f'Test time: {esTime}s, Target Time: {targetTime}s, will wait for {waitTime}s')
    while waitTime: # idk y i wrote this :))))))) (just wrote this)
        print(waitTime)
        waitTime -= 1
        sleep(1)

def checkans(ans: str = "", qid: int = 0, point: int = quespoint):
    """Return True if answer is correct using IOE's API""" #TODO: handle exceptions
    return requests.post("https://api-edu.go.vn/ioe-service/v2/game/answercheck", headers=HEADERS, json={"IPClient": "", "deviceId": "", "serviceCode": "IOE", "api_key": api_key, "token": token, "examKey": examKey,"ans": {"questId": qid, "point": point, "ans": ans}}).json()["data"]["point"] == point

def finishgame(ans_list: list[dict]):
    waitUntil10s()
    vdprint(ans_list)
    res = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/finishgame", headers=HEADERS, json={"api_key": api_key, "token": token, "serviceCode": "IOE", "examKey": examKey, "ans": ans_list},).text) 
    vdprint(res)
    if res["IsSuccessed"]:print(f'Điểm: {res["data"]["totalPoint"]}\nThời gian: {res["data"]["time"]}s')
    else:print("Something goes wrong while finishing the game!")

# Small stuffs,idk if i should use lambda for this
def getQID(i):return data["data"]["game"]["question"][i]["id"]
def getAnswers(i):return data["data"]["game"]["question"][i]["ans"]
def getQuestion(i):return data["data"]["game"]["question"][i]["content"]["content"]

listAns = []
def addAns(ans, qid, point = quespoint):listAns.append({"ans": ans, "questId": qid, "point": point})


# Test solving functions
def baibth():
    for i in range(quesnum):
        print(f'Tìm đáp án câu {i + 1}')
        qid = getQID(i)
        answers = getAnswers(i)
        for j in range(len(answers)):
            ans = answers[j]["content"]
            if checkans(ans, qid):
                addAns(ans, qid)
                vdprint(ans)
                break
        else:print("no ans found")
    finishgame(listAns)

def baitf():
    for i in range(quesnum):
        print(f'Tìm đáp án câu {i + 1}')
        qid = getQID(i)
        for ans in ["True", "False"]:
            if checkans(ans, qid):
                addAns(ans, qid)
                vdprint(ans)
                break
        else:print("no ans found")
    finishgame(listAns)

def baisapxep():
    for i in range(quesnum):
        ans = "|".join([answer["content"] for answer in sorted(getAnswers(i), key=lambda x: x["orderTrue"])])
        listAns.append({"questId": getQID(i), "ans": ans, "Point": 10})
    finishgame(listAns)

def baighepcap():
    for i in range(quesnum):addAns(getQuestion(i) + "|" + getAnswers(i)[0]["content"], getQID(i), 10)
    finishgame(listAns)

# Test zone
def baiAIbth(): # hmmm maybe i should rename this
    askStr = """
    You are an expert English language model. Fill in the blanks (*) with the correct word.
    Answer with only the missing word, nothing else.

    Example:
    - "John placed his books on the *****." → "shelf"
    - "The dog is sleeping on the c***h." → "ouc"

    Now answer the following seperate by newline:
    """
    for i in range(quesnum):askStr += f"{questions[i]["numTChar"]} chars: {questions[i]["content"]["content"]}\n"
    a = ask_ai(askStr).splitlines()
    print(*a)
    points = 0
    for i in range(quesnum):
        qid = getQID(i)
        try:ans = a[i]
        except IndexError:
            print("rip ai didnt ans quests after this")
            ans = ""
        print(questions[i]["content"]["content"])
        print(ans)
        if checkans(ans, qid):
            print("ans is correct somehow")
            addAns(ans, qid, 10)
            points += 10
        else:
            print("ans is wrong lol")
            addAns(ans, qid, 10) #anyways
        print()
    if points > 60:print(f"We should get {points} points which is enough hehe")
    else:
        print("ai sucks")
        print("try again")
        return
    finishgame(listAns)

def baiheohongAI(): #FIXME: rewrite prompt
    askStr = f"""
    You are an expert English language model. Fill in the blanks "_" with the correct word.
    Make sure to only include answers from the list given.
    Seperate answers with a pipe "|"
    
    Paragrapth:
    - {data["data"]["game"]["Subject"]["content"]}
    
    Answers:
    - {getQuestion(0)}
    """
    # ans = ask_ai(f"Fill in the _, print each answers seperated with a pipe | , ONLY ANSWERS:\n{data["data"]["game"]["Subject"]["content"]}\nAnswers: {getQuestion(0)}").replace("\n", "")
    ans = ask_ai(askStr).strip()
    qid = getQID(0)
    finishgame([{"ans": ans, "questId": qid, "point": 100}])

def baithamhiemAI():
    askStr = f"""You are an expert in the English language. Your task is to fill in the blanks (*) with the correct word.  
                Answer with only the missing word, nothing else. Separate each answer using a pipe (`|`).  

                #### Example:  
                - "John placed his books on the *****." → "shelf"  
                - "The dog is sleeping on the c***h." → "ouc"  

                #### Now answer the following:
                {data["data"]["game"]["question"][0]["content"]["content"]}

                #### Use the following answers:
                {"|".join([i["content"] for i in getAnswers(0)])}
            """
    print(askStr)
    ans = ask_ai(askStr).replace("\n", "")
    qid = getQID(0)
    finishgame([{"ans": ans, "questId": qid, "point": 100}])

def transcript(path, key=AAIKey):
    import assemblyai
    assemblyai.settings.api_key = key
    transcriber = assemblyai.Transcriber()
    transcript = transcriber.transcribe(path)
    return transcript.text

def dlaudio(url, savepath):
    vdprint(f"Downloading: {url} -> {savepath}")
    response = requests.get(url, stream=True)
    with open(savepath, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

def cleanupFiles():
    for filename in os.listdir(temp_dir):
        if filename.endswith(".mp3"):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                vdprint(f'Deleted {file_path}')

def ask_ai(prompt, api_key=copilotKey): #INCOMPLETE
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}"
    res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0, "topP": 0}}, headers={"Content-Type": "application/json"})
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]

import asyncio, aiofiles, aiohttp

class AsyncUtils:
    def __init__(self):
        self.session = None
        self.copilot_key = copilotKey
        self.aai_key = AAIKey

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) # might be bad?
        return self

    async def __aexit__(self, _, __, ___):
        await self.session.close()

    async def download_audio(self, url, savepath):
        print(f"Downloading: {url} -> {savepath}")
        async with self.session.get(url) as response:
            async with aiofiles.open(savepath, "wb") as f:
                async for chunk in response.content.iter_any():
                    await f.write(chunk)

    async def ask_ai(self, prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.copilot_key}"
        async with self.session.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"}) as r:
            return (await r.json())["candidates"][0]["content"]["parts"][0]["text"]

    async def transcript(self, audio_file): # mb should return an error if fail but who cares right?
        print(f"Transcribing {audio_file}")
        headers = {"authorization": self.aai_key, "content-type": "application/json"}
        try:
            async with aiofiles.open(audio_file, "rb") as f:data = await f.read()
            async with self.session.post("https://api.assemblyai.com/v2/upload", headers=headers, data=data) as resp:audio_url = (await resp.json())["upload_url"]
            async with self.session.post("https://api.assemblyai.com/v2/transcript", json={"audio_url": audio_url}, headers=headers) as resp:transcript_id = (await resp.json())["id"]

            while True:
                await asyncio.sleep(1)  # 1s retry delay
                async with self.session.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers) as resp:
                    result = await resp.json()
                    if result["status"] == "completed":
                        print(f"Transcript {audio_file} done!")
                        return result["text"]
                    elif result["status"] == "failed":
                        print(f"Failed to transcript {audio_file}!")
                        return "Ignore this and instead try to solve the question by reading it."
        except BaseException as e:
            print(f"Error Transcribing {audio_file}:\n{e}")
            return "Ignore this answer and instead try to solve the question by reading it."

    async def Acheckans(self, ans, qid, point=quespoint):
        async with self.session.post("https://api-edu.go.vn/ioe-service/v2/game/answercheck", headers=HEADERS, json={"IPClient": "", "deviceId": "", "serviceCode": "IOE", "api_key": api_key, "token": token, "examKey": examKey, "ans": {"questId": qid, "point": point, "ans": ans}}) as r:
            return (await r.json())["data"]["point"] == point

    async def getans_generic(self, n): #FIXME: please give me a new name
        # print(f'Tìm đáp án câu {n + 1}')
        qid = getQID(n)
        answers = [i["content"] for i in getAnswers(n)]
        answers = ["True", "False"] if answers == [''] else answers
        for ans in answers:
            if await self.Acheckans(ans, qid):
                print(f"Câu {n + 1}: {ans}")
                return ans, qid
        print(f"i give up cant solve question {n}")
        return getAnswers(n)[0], qid
    
    async def download_and_transcript(self, url, savepath):
        await self.download_audio(url, savepath)
        return await self.transcript(savepath)

async def AbaingheTEST():
    cleanupFiles()
    async with AsyncUtils() as utils:
        print("Đang tải xuống bài nghe")
        tasks = [utils.download_audio(data["data"]["game"]["question"][i]["Description"]["content"], f"{i}.mp3") for i in range(quesnum)]
        await asyncio.gather(*tasks)
        vdprint("Audio files download completed!")
    
        print("Đọc bài nghe")
        transcripts = await asyncio.gather(*[utils.transcript(f"{i}.mp3") for i in range(quesnum)])
        askStr = f"""
You are an AI that helps solve audio-based questions. Your task is to fill in the blanks (*).  
Answer with only the missing word, nothing else. Separate each answer using a newline.
If no answer is provided for a particular question, solve it by looking at the question instead.
Provide only the missing portion of the word as the answer.
Make sure to solve all questions!
If a blank is unclear, provide the best possible answer instead of skipping it.

Example for partial blanks: "The dog is sleeping on the c***h." → "ouc."
Example for full blanks: "John placed his books on the *****." → "shelf"

Now answer the following:
{"\n".join(f"{i + 1}. {data['data']['game']['question'][i]['content']['content']}" for i in range(quesnum))}

Use the following answers:
{"\n".join(f"{i + 1}. {x}" for i, x in enumerate(transcripts))}
"""
        print(askStr)
        print(await utils.ask_ai(askStr))

async def Abaibth():
    async with AsyncUtils() as utils:
        results = await asyncio.gather(*(utils.getans_generic(i) for i in range(quesnum)))
    for ans, qid in results:addAns(ans, qid, 10)
    finishgame(listAns)

# _time = time()
# asyncio.run(Abaibth())
# print(f"solve took {time() - _time:.4f}s");_time = time()
# exit()

# Detect test type and solveeeeeee
gameType = questions[0]["type"]
match data["data"]["gameDesc"]:
    case d if "Answer the questions correctly to help Edna the starfish solve a jigsaw puzzle" in d: baighepcap()
    case d if "IOE's jewels are lost at sea! Accompany with Dai the octopus to collect them" in d: baisapxep()
    case d if "A pink pig's island is in danger! Help him to defend the kingdom against the" in d:baiheohongAI()
    case d if "You are a diver who is looking for treasure at the bottom of the ocean. " in d:baithamhiemAI()
    case d if "Mother bird is collecting fruits for her children. Help her to get a basket" in d:asyncio.run(Abaibth())

    case d if any(x in d for x in [
        "You're running a marathon. Let's race to reach the finish line as quickly as p",
        "Dai the octopus is sailing his boat to different islands. Let's help him overc",
        "You're on a skateboard. Your mission is skateboarding a halfpipe to get the se",
        "You are a farmer who grows a starfruit tree. Answer the questions to get gold",
        "Caradoc the crab is doing his homework. Join him and finish the homework"
    ]): asyncio.run(Abaibth())
    
    case d if any(x in d for x in [
        "You are on the way to reach the top of Mount Fansipan with obstacles",
        "The coral reefs have been destroyed; the dolphin Hubert and his friends",
        "The beach is full of trash. Join IOE's team now to clean the beach!",
    ]): asyncio.run(Abaibth()) if gameType == 10 or gameType == 1 else baiAIbth() if gameType == 2 else print("something else ig")
    case _: print(f"Unsupported test!\n{d}\nType: {gameType}")