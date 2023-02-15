import random
import requests
from src import log

# Load danh sách các từ có 2 từ vào một list
with open('src/assets/tudien.txt', 'r') as f:
    list_words = [word.strip().lower() for word in f.readlines()]

# Chọn ngẫu nhiên một từ từ danh sách các từ có 2 từ
# current_word = random.choice(list_words)
current_word = ''
player_word = ''
history = []
sai = 3
# trích xuất từ cuối cùng của một từ
def last_word(word):
    return word.split()[-1]

# trích xuất từ đầu tiên của một từ

def first_word(word):
    return word.split()[0]

def get_word_starting_with(start):
    matching_words = [word for word in list_words if word.split()[0] == start]
    if matching_words:
        word = random.choice(matching_words)
        addHistory(word)
        return word
    else:
        return False
#TODO lỗi first word 
def check(player_word):
    global sai
    global current_word
    if not current_word:
        current_word = random.choice(list_words)
    
    if last_word(current_word) == first_word(player_word) and sai != 1:
        if player_word in history:
            return 'Đã trả lời từ, vui lòng tìm từ khác'
        if player_word in list_words:
            addHistory(player_word)
            # Tìm một từ mới từ danh sách các từ có 2 từ để đưa ra
            next_word = get_word_starting_with(last_word(player_word))
            current_word = next_word
            if not next_word:
               return win()
            response = 'Từ tiếp theo: **' + next_word + '**'
            return response
        else:
            print('Không tồn tại từ, vui lòng tìm từ khác')
            sai -= 1
            response = 'Không tồn tại từ, vui lòng tìm từ khác, còn ' + str(sai) + ' lần thử'
            return response
    else:
        return loss()

def win():
    global current_word
    global sai
    sai = 3
    current_word = randomWord()
    return '**BẠN ĐÃ THẮNG!** Từ mới: **' + current_word + '**'

def loss():
    global current_word
    global sai
    sai = 3
    current_word = randomWord()
    return '> Thua cuộc, từ đầu bạn đưa ra phải trùng với từ cuối của bot hoặc từ phải có nghĩa! \nTừ mới: **' + current_word + '**'

def start():
    global current_word
    current_word = randomWord()
    return 'Từ hiện tại: **' + current_word + '**'

def randomWord():
    word = random.choice(list_words)
    addHistory(word)
    return word

def addHistory(word):
    history.append(word)

# http://tudientv.com/dictfunctions.php?action=getmeaning&entry=chào

url = "http://tudientv.com/dictfunctions.php"

async def tratu() -> str:
    global current_word
    payload = {
        "action": 'getmeaning',
        "entry": current_word
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
    #     data = json.loads(response.text)
    #     nghia = data.get("message")
    # #   print(message)
    #     logger.info(f"Prompt response: {message}")
        print(response.text)
        return response.text
    else:
        print("Không thể lấy dữ liệu từ API")
        return "Không thể lấy dữ liệu từ API"
