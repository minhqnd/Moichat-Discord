import random

# Load danh sách các từ có 2 từ vào một list
with open('assets/tudien.txt', 'r') as f:
    list_words = [word.strip().lower() for word in f.readlines()]

# Chọn ngẫu nhiên một từ từ danh sách các từ có 2 từ
# current_word = random.choice(list_words)
current_word = ''
player_word = ''

# Hàm trích xuất từ cuối cùng của một từ
def last_word(word):
    return word.split()[-1]

def first_word(word):
    return word.split()[0]

def get_word_starting_with(start):
    matching_words = [word for word in list_words if word.startswith(start)]
    if matching_words:
        return random.choice(matching_words)
    else:
        return None

def askplayer(current_word):
    print('Từ hiện tại:', current_word)
    player_word = input('Từ của bạn: ').lower()
    check(player_word)

def check(player_word):
    global current_word
    if last_word(current_word) == first_word(player_word):
        if player_word in list_words:
            # Tìm một từ mới từ danh sách các từ có 2 từ để đưa ra
            next_word = get_word_starting_with(last_word(player_word))
            current_word = next_word
            print('Từ tiếp theo:', next_word)
        else:
            print('Không tồn tại từ, vui lòng tìm từ khác')
            # player_word = input('Từ của bạn: ').lower()
    else:
        print('Thua cuộc, từ đầu bạn đưa ra phải trùng với từ cuối của bot!')

def start():
    global current_word
    current_word = random.choice(list_words)
    askplayer(current_word)

start()

    