from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, MessageAction, ImageSendMessage, QuickReply, QuickReplyButton, PostbackEvent, PostbackAction
)
import random
import json

app = Flask(__name__)

line_bot_api = LineBotApi('Channel access token')
handler = WebhookHandler('Channel secret')

base_addr = "https://esl-kids.com/img/worksheets/"
cards_dict = {'actions': ['clap', 'closeyoureyes', 'crawl', 'dance', 'fly', 'hop', 'jump', 'openyoureyes', 'run', 'sit', 'skip', 'stand', 'stomp', 'swim', 'turnaround', 'walk'], 'alphabet': ['Aa', 'Bb', 'Cc', 'Dd', 'Ee', 'Ff', 'Gg', 'Hh', 'Ii', 'Jj', 'Kk', 'Ll', 'Mm', 'Nn', 'Oo', 'Pp', 'Qq', 'Rr', 'Ss', 'Tt', 'Uu', 'Vv', 'Ww', 'Xx', 'Yy', 'Zz'], 'animals': ['alligator', 'bear', 'bird', 'cat', 'chicken', 'cow', 'dog', 'duck', 'elephant', 'fish', 'fox', 'frog', 'giraffe', 'goat', 'hamster', 'hippo', 'horse', 'kangaroo', 'koala', 'lion', 'monkey', 'mouse', 'octopus', 'panda', 'penguin', 'pig', 'rabbit', 'rhino', 'seal', 'shark', 'sheep', 'snake', 'squirrel', 'tiger', 'turtle', 'walrus', 'whale', 'zebra'], 'bodyparts': ['arm', 'back', 'bellybutton', 'bottom', 'ear', 'elbow', 'eye', 'face', 'finger', 'foot', 'hair', 'hand', 'head', 'hips', 'knee', 'leg', 'lips', 'mouth', 'neck', 'nose', 'shoulder', 'teeth', 'toe', 'tongue', 'tummy'], 'buildings': ['bank', 'busstop', 'church', 'cityhall', 'gasstation', 'hospital', 'hotel', 'library', 'movietheater', 'museum', 'park', 'policestation', 'postoffice', 'restaurant', 'school', 'station', 'supermarket', 'university'], 'christmas': ['angel', 'bells', 'bow', 'cake', 'candle', 'candycane', 'carols', 'chimney', 'christmaslights', 'elf', 'fireplace', 'gingerbreadman', 'holly', 'mistletoe', 'northpole', 'ornaments', 'presents', 'reindeer', 'santa', 'sleigh', 'snowflake', 'snowman', 'star', 'stocking', 'toys', 'tree', 'turkey', 'wreath'], 'classroom': ['blackboard', 'book', 'cdplayer', 'chair', 'classroom', 'clock', 'colorpencils', 'computer', 'crayons', 'desk', 'door', 'eraser', 'folder', 'glue', 'inkpad', 'markers', 'nametag', 'notebook', 'paper', 'pen', 'pencil', 'pencilcase', 'pencilsharpener', 'ruler', 'schoolbag', 'scissors', 'stamp', 'stickers', 'students', 'table', 'tapeplayer', 'teacher', 'wall', 'whiteboard', 'window'], 'clothes': ['boots', 'coat', 'dress', 'gloves', 'hat', 'jacket', 'pajamas', 'pants', 'scarf', 'shirt', 'shoes', 'shorts', 'skirt', 'socks', 'sweater', 'tshirt'], 'colors': ['beige', 'black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow'], 'days': ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'], 'dinnerset': ['bowl', 'cup', 'fork', 'glass', 'knife', 'plate', 'spoon'], 'easter': ['basket', 'bunny', 'card', 'chick', 'chocolate', 'egg', 'jellybeans', 'lily'], 'emergencyservices': ['ambulance', 'coastguard', 'firetruck', 'rescuehelicopter', 'policecar', 'policemotorcycle'], 'family': ['baby', 'brother', 'father', 'grandfather', 'grandmother', 'me', 'mother', 'sister'], 'feelings': ['angry', 'bored', 'fine', 'great', 'happy', 'okay', 'sad', 'scared', 'sick', 'tired'], 'fivesenses': ['hear', 'see', 'smell', 'taste', 'touch'], 'food': ['bread', 'broccoli', 'cabbage', 'cake', 'candy', 'carrot', 'celery', 'cheese', 'cheeseburger', 'chicken', 'chocolate', 'coffee', 'cookies', 'corn', 'cornflakes', 'cucumber', 'egg', 'fish', 'frenchfries', 'greenonion', 'ham', 'hamburger', 'hotdog', 'icecream', 'jelly', 'lettuce', 'milk', 'nuts', 'onion', 'orangejuice', 'pancakes', 'peas', 'pizza', 'potatochips', 'potatoes', 'rice', 'salad', 'sandwich', 'sausages', 'soda', 'spaghetti', 'sweetpotato', 'tea', 'toast', 'tomato', 'water'], 'fruit': ['apple', 'banana', 'cherries', 'grapefruit', 'grapes', 'lemon', 'melon', 'orange', 'pear', 'pineapple', 'strawberry', 'watermelon'], 'halloween': ['bat', 'blackcat', 'frankenstein', 'ghost', 'hauntedhouse', 'jackolantern', 'monster', 'mummy', 'owl', 'skeleton', 'spider', 'trickortreat', 'vampire', 'werewolf', 'witch'], 'months': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'], 'musicalinstruments': ['castanets', 'cello', 'clarinet', 'cymbals', 'drum', 'flute', 'guitar', 'harmonica', 'keyboard', 'maracas', 'piano', 'saxophone', 'tambourine', 'triangle', 'trombone', 'trumpet', 'violin', 'xylophone'], 'numbers': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], 'occupations': ['chef', 'doctor', 'firefighter', 'lifeguard', 'mailman', 'nurse', 'policeofficer', 'shopkeeper', 'teacher'], 'playground': ['basketball', 'hopscotch', 'junglegym', 'paddlingpool', 'playhouse', 'sandbox', 'seesaw', 'slide', 'swing', 'trampoline'], 'presents': ['ball', 'bicycle', 'blocks', 'book', 'car', 'cards', 'clothes', 'doll', 'dvd', 'game', 'hulahoop', 'jumprope', 'marbles', 'puzzle', 'robot', 'stuffedtoy', 'teddybear', 'train', 'tricycle', 'videogame', 'yoyo'], 'rooms': ['bathroom', 'bedroom', 'classroom', 'kitchen', 'laundryroom', 'livingroom'], 'shapes': ['circle', 'square', 'triangle', 'rectangle', 'star', 'heart'], 'sports': ['badminton', 'baseball', 'basketball', 'gymnastics', 'karate', 'running', 'skiing', 'soccer', 'sumo', 'swimming', 'tennis', 'volleyball'], 'stpatricks': ['fairy', 'ireland', 'leprechaun', 'gold', 'rainbow', 'shamrock'], 'thingsathome': ['bath', 'bed', 'bookcase', 'cdplayer', 'chair', 'clothes', 'computer', 'cupboard', 'mirror', 'picture', 'refrigerator', 'sink', 'sofa', 'table', 'television', 'toys'], 'transportation': ['bicycle', 'motorcycle', 'car', 'taxi', 'truck', 'bus', 'train', 'boat', 'helicopter', 'airplane'], 'valentines': ['card', 'chocolate', 'couple', 'cupid', 'flowers', 'heart', 'kiss', 'rose'], 'weather': ['sunny', 'rainy', 'cloudy', 'snowy', 'stormy', 'windy', 'hot', 'cold']}
with open('users.json','r+') as f:
    users =  json.load(f)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def handle_Postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    
    if data == 'start' or data == 'next':
        if users[user_id]['progress'] == []:
            users[user_id]['progress'] = list(cards_dict.keys())
        users[user_id]['theme'] = random.choice(users[user_id]['progress'])
        users[user_id]['cards'] = cards_dict[users[user_id]['theme']].copy()
        msg = []
        msg = msg + create_reply(user_id)
        line_bot_api.reply_message(event.reply_token, msg)
        return

    if data == 'info':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='???????????????\n????????????????????????\n????????????????????????\n??????????????????\n?????????????????????????????????????????????\n\n???????????????\n?????????????????????????????????\n???????????????\n??????????????????????????????????????????\n???????????????\n??????????????????????????????????????????????????????',quick_reply=QuickReply(items=[QuickReplyButton(action=PostbackAction(label='??????',data='start')),QuickReplyButton(action=PostbackAction(label='??????',data='info'))])))
        return
    
    if data == 'stop':
        users[user_id]['game'] = -1
        users[user_id]['theme'] = ''
        users[user_id]['answer'] = ''
        database_update()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='???????????????\n?????????????????????\n??????????????????????????????????????????\n??????????????????'))
        return

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global users
    user_id = event.source.user_id
    game_keyword = ['?????????','?????????','?????????']

    if user_id not in users.keys():
        users[user_id] = {'game':-1, 'progress':list(cards_dict.keys()), 'theme':'', 'cards':[], 'answer':''}
        database_update()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='????????????????????????????????????!\n?????????????????????????????????'))
        return
    
    if users[user_id]['theme'] == '':
        users[user_id]['game'] = -1
        
    if event.message.text.replace(' ','') in game_keyword:
        users[user_id]['game'] = game_keyword.index(event.message.text)
        users[user_id]['theme'] = ''
        users[user_id]['cards'] = []
        users[user_id]['answer'] = ''
        database_update()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'???????????????????????????"{event.message.text}"????????????"??????"??????????????????',quick_reply=QuickReply(items=[QuickReplyButton(action=PostbackAction(label='??????',data='start')),QuickReplyButton(action=PostbackAction(label='??????',data='info'))])))
        return

    if event.message.text.lower().replace(' ','') == users[user_id]['answer'].lower():
        users[user_id]['cards'].remove(users[user_id]['answer'])
        if len(users[user_id]['cards']) > 0:
            msg = []
            msg.append(TextSendMessage(text=f'????????????\n???????????????"{len(users[user_id]["cards"])}"??????'))
            msg = msg + create_reply(user_id)
            line_bot_api.reply_message(event.reply_token, msg)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'????????????\n???????????????"{users[user_id]["theme"]}"????????????\n???????????????????????????????????????',quick_reply=QuickReply(items=[QuickReplyButton(action=PostbackAction(label='?????????',data='next')),QuickReplyButton(action=PostbackAction(label='????????????',data='stop'))])))
            users[user_id]['answer'] = ''
            users[user_id]['progress'].remove(users[user_id]['theme'])
            users[user_id]['theme'] = ''
            users[user_id]['cards'] = []
        database_update()
        return
    
    if event.message.text.lower().replace(' ','') != users[user_id]['answer'].lower():
        if users[user_id]['game'] == -1:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='?????????????????????????????????'))
            return
        msg = []
        msg.append(TextSendMessage(text=f'?????????????????????"{users[user_id]["answer"]}"'))
        msg = msg + create_reply(user_id)
        line_bot_api.reply_message(event.reply_token, msg)
        return

def create_reply(user_id):
    msg = []
    users[user_id]['answer'] = random.choice(users[user_id]['cards'])
    quick_reply = quick_reply_items(user_id)
    tf_reply = true_false_reply(user_id)
    msg.append(ImageSendMessage(base_addr + users[user_id]['theme'] + '/' + users[user_id]['answer'] + '.gif', base_addr + users[user_id]['theme'] + '/' + users[user_id]['answer'] + '.gif',quick_reply=quick_reply))
    msg.append(tf_reply) if tf_reply is not None else None
    return msg

def quick_reply_items(user_id):
    quick_reply = None
    if users[user_id]['game'] == 1:
        copy_cards = cards_dict[users[user_id]['theme']].copy()
        copy_cards.remove(users[user_id]['answer'])
        opts = random.sample(copy_cards,k=3)
        opts.append(users[user_id]['answer'])
        random.shuffle(opts)
        items = []
        for opt in opts:
            items.append(QuickReplyButton(action=MessageAction(label=opt, text=opt)))
        quick_reply = QuickReply(items=items)
    return quick_reply

def true_false_reply(user_id):
    if users[user_id]['game'] == 2:
        copy = cards_dict[users[user_id]['theme']].copy()
        copy.remove(users[user_id]['answer'])
        tmp_rnd = random.choice(copy)
        if random.choice([True,False]):
            tmp_reply = users[user_id]['answer']
            true_ans = users[user_id]['answer']
            false_ans = 'False'
        else:
            tmp_reply = tmp_rnd
            true_ans = 'True'
            false_ans = users[user_id]['answer']
        return TextSendMessage(text=tmp_reply,quick_reply=QuickReply(items=[QuickReplyButton(action=MessageAction(label='True', text=true_ans)),QuickReplyButton(action=MessageAction(label='False', text=false_ans))]))
    return None

def database_update():
    with open('users.json','w') as f:
        json.dump(users,f,indent=4)

if __name__ == "__main__":
    app.run(debug=True)
