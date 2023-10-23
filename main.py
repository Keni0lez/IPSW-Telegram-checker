import telebot
from telebot import types
from urllib.request import Request, urlopen
import json
import sys
import os

bot = telebot.TeleBot('TOKEN')

adminid = 111 # type ur chat id

chat_ids = []
try:
    with open('chat_ids.json', 'r') as json_file:
        chat_ids = json.load(json_file)
except FileNotFoundError:
    pass

def idkk():
    try:
        def load_model_to_identifier_from_json(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            return data

        json_file_path = 'model_to_identifier.json'
        model_to_identifier = load_model_to_identifier_from_json(json_file_path)

        def send_message_to_all_users(message_text):
            with open('chat_ids.json', 'r') as json_file:
                chat_ids = json.load(json_file)
                for chat_id in chat_ids:
                    bot.send_message(chat_id, message_text)

        send_message_to_all_users("...")


        @bot.message_handler(commands=['start'])
        def send_start_message(message):
            chat_id = message.chat.id
            if chat_id not in chat_ids:
                chat_ids.append(chat_id)
                bot.send_message(chat_id, "Bot updated")

                # Сохраняем обновленный список chat_ids в JSON-файл
                with open('chat_ids.json', 'w') as json_file:
                    json.dump(chat_ids, json_file)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item2g = types.KeyboardButton("iPhone 2G")
            item3g = types.KeyboardButton("iPhone 3G")
            item3gs = types.KeyboardButton("iPhone 3Gs")
            item1 = types.KeyboardButton("iPhone 4")
            item4s = types.KeyboardButton("iPhone 4s")
            item2 = types.KeyboardButton("iPhone 5")
            item5s = types.KeyboardButton("iPhone 5s")
            item3 = types.KeyboardButton("iPhone 6")
            item6plus = types.KeyboardButton("iPhone 6+")
            item6s = types.KeyboardButton("iPhone 6s")
            item6splus = types.KeyboardButton("iPhone 6s+")
            item4 = types.KeyboardButton("iPhone 7")
            item5 = types.KeyboardButton("iPhone 7 Plus")
            item6 = types.KeyboardButton("iPhone SE (1st)")
            item7 = types.KeyboardButton("iPhone 8")
            item8 = types.KeyboardButton("iPhone 8 Plus")
            item9 = types.KeyboardButton("iPhone X")
            item10 = types.KeyboardButton("iPhone XR")
            item11 = types.KeyboardButton("iPhone XS")
            item12 = types.KeyboardButton("iPhone XS Max")
            item13 = types.KeyboardButton("iPhone 11")
            item14 = types.KeyboardButton("iPhone 11 Pro")
            item15 = types.KeyboardButton("iPhone 11 Pro Max")
            item16 = types.KeyboardButton("iPhone SE (2nd)")
            item17 = types.KeyboardButton("iPhone 12")
            item18 = types.KeyboardButton("iPhone 12 mini")
            item19 = types.KeyboardButton("iPhone 13")
            item20 = types.KeyboardButton("iPhone 13 Pro")
            item21 = types.KeyboardButton("iPhone 13 Pro Max")
            itemse3 = types.KeyboardButton("iPhone SE (3nd)")
            item14q = types.KeyboardButton("iPhone 14")
            item14plus = types.KeyboardButton("iPhone 14 Plus")
            item14pro = types.KeyboardButton("iPhone 14 Pro")
            item14promax = types.KeyboardButton("iPhone 14 Pro Max")
            item15q = types.KeyboardButton("iPhone 15")
            item15plus = types.KeyboardButton("iPhone 15 Plus")
            item15pro = types.KeyboardButton("iPhone 15 Pro")
            item15promax = types.KeyboardButton("iPhone 15 Pro Max")

            markup.row(item2g, item3g)
            markup.row(item3gs, item1)
            markup.row(item2, item3)
            markup.row(item6plus, item6s)
            markup.row(item4, item5)
            markup.row(item6, item7)
            markup.row(item8, item9)
            markup.row(item10, item11)
            markup.row(item12, item13)
            markup.row(item14, item15)
            markup.row(item16, item17)
            markup.row(item18, item19)
            markup.row(item20, item21 )
            markup.row(itemse3, item14q)
            markup.row(item14plus, item14pro)
            markup.row(item14promax, item15q)
            markup.row(item15plus, item15pro)
            markup.row(item15promax)

            bot.send_message(message.chat.id, "Select the iPhone model:", reply_markup=markup)

        def is_allowed_to_restart(chat_id):
            return chat_id == adminid


        @bot.message_handler(commands=['restart'])
        def handle_restart(message):
            chat_id = message.chat.id
            if is_allowed_to_restart(chat_id):
                bot.send_message(chat_id, "Restarting...")
                bot.stop_polling()
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                bot.send_message(chat_id, "Error: Are you root?")

        @bot.message_handler(commands=['say'])
        def send_to_all(message):
            if message.chat.id == adminid:  # Замените YOUR_ADMIN_CHAT_ID на ваш собственный chat_id
                args = message.text.split()[1:]
                message_text = " ".join(args) if args else "This is a message sent to all users."
                send_message_to_all_users(message_text)
            else:
                bot.send_message(message.chat.id, "Error: Are you root?")

        @bot.message_handler(func=lambda message: message.text in model_to_identifier)
        def handle_selected_model(message):
            try:
                model_name = message.text
                device_identifier = model_to_identifier[model_name]

                headers = {
                    'Accept': 'application/json'
                }
                request_url = f'https://api.ipsw.me/v4/device/{device_identifier}?type=ipsw'

                request = Request(request_url, headers=headers)
                response_body = urlopen(request).read().decode('utf-8')

                data = json.loads(response_body)

                signed_firmwares = [fw for fw in data['firmwares'] if fw['signed']]

                if signed_firmwares:
                    response_text = f"<b>✅ Signed IPSW for {model_name} | {device_identifier}</b>\n\n"
                    for firmware in signed_firmwares:
                        download_link = f"https://api.ipsw.me/v4/ipsw/download/{device_identifier}/{firmware['buildid']}"
                        releasedate = firmware.get('releasedate', '')
                        uploaddate = firmware.get('uploaddate', '')

                        if releasedate:
                            releasedate = releasedate.split('T')[0]

                        if uploaddate:
                            uploaddate = uploaddate.split('T')[0]

                        response_text += f"├ Version: {firmware['version']} ({firmware['buildid']})\n"
                        response_text += f"├ Release date: {releasedate}\n"
                        response_text += f"├ Upload date: {uploaddate}\n"
                        response_text += f"├ <a href='{download_link}'>Download</a>\n"
                        response_text += f"└────────────────\n"

                    bot.send_message(message.chat.id, response_text, parse_mode='HTML')
                else:
                    response_text = f"Signed IPSW doesn't exist for {model_name} (identifier: {device_identifier})."
                    bot.send_message(message.chat.id, response_text)
            except Exception as e:
                bot.send_message(message.chat.id, f"Error: {str(e)}")

        bot.polling()
    except:
        idkk()
idkk()