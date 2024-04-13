import json
import time
import random
import telebot
import multiprocessing

from telebot import types
from telebot.types import ReplyKeyboardRemove

while True:
    try:
    #if 1==1:
        global send_password_by_time
        global get_alphabet
        get_alphabet = 0
        global password_alphabet
        global delete_user
        global set_time
        global contacts
        set_time = 0
        global action
        global trusted_chats
        action = 0
        global proc
        global bot


        with open("token", "r") as file:
            token = file.read()[:-1]
        bot = telebot.TeleBot(token)

        def bot_send_mess(i,password):
            global bot
            bot.send_message(i, text=f"`{password}`", parse_mode='MarkdownV2')


        def send_password_by_time():
            global bot
            print("Start thread")
            while True:
                with open("time", 'r') as f:
                    times = int(f.read())

                with open("password_alphabet", 'r') as f:
                    password_alphabet = f.read()

                with open("trust", "r") as file:
                    lines = file.read()
                trusted_chats = eval(lines)

                random.seed(time.time())
                if times <= 60 :                                                # It`s about one hour
                    password = ''.join(random.choices(password_alphabet, k=7))
                elif times > 60 and times <= 1440:                              # It`s about one day
                    password = ''.join(random.choices(password_alphabet, k=8))
                elif times > 1440 and times <= 4320:                            # It`s about three days
                    password = ''.join(random.choices(password_alphabet, k=9))
                elif times > 4320  and times <= 129600:                         # It`s about seven mounth
                    password = ''.join(random.choices(password_alphabet, k=10))
                else:                                                           # For crack this password you need 41 years
                    password = ''.join(random.choices(password_alphabet, k=11))

                with open("password", 'w') as f:
                    f.write(password)
                f.close()

                print("The password is:", password)
                for i in trusted_chats:
                    bot_send_mess(i, password)

                time.sleep(times*60)



        with open("time", 'r') as f:
            times = f.read().split("\n")[0]

        if times != '':
            proc = multiprocessing.Process(target=send_password_by_time, args=())
            proc.start()


        password_alphabet = ''
        with open("password_alphabet", "r") as file:
            password_alphabet = file.read()

        trusted_chats = []
        queue = []

        with open("boss", "r") as file:
            lines = file.read()

        boss = eval(lines)

        with open("contacts", "r") as file:
            lines = file.read()

        contacts = eval(lines)

        with open("trust", "r") as file:
            lines = file.read()

        trusted_chats = eval(lines)
        #contacts = {}


        @bot.message_handler(commands=['start'])
        def start(message):
            #print(message)
            has_person_in_contacts = False
            for i in list(contacts.keys()):
                if contacts[i]['user_id'] == message.chat.id:
                    has_person_in_contacts = True

            if message.from_user.id in boss:
                bot.send_message(message.chat.id, 'Привет администратор, чтобы открыть меню управлния отправь \n /admin_menu \n А чтобы открыть обычное меню открой \n /menu')
            elif has_person_in_contacts == True:
                bot.send_message(message.chat.id, 'Привет, чтобы открыть меню нажми команду \n /menu')
            else:
                bot.send_message(message.chat.id, "Пожалуйста зарегестрируйтесь командой \n /register")
                #print("asd")

        @bot.message_handler(commands=['register'])
        def phone(message):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
            keyboard.add(button_phone) #Добавляем эту кнопку
            bot.send_message(message.chat.id, 'Для регистрации нажмите на кнопку в меню ', reply_markup=keyboard)

        @bot.message_handler(content_types=['contact'])
        def contact(message):
            global contacts
            global trusted_chats
            if message.contact is not None:
                #print(message.contact)
                #print(message.contact.first_name, message.contact.last_name, message.contact.user_id)
                try:
                    print(contacts[message.contact.phone_number])
                except:
                    print({'first_name': message.contact.first_name, 'last_name': message.contact.last_name, 'user_id': message.contact.user_id, "date": message.json["date"]    })
                    contacts[message.contact.phone_number] = {'first_name': message.contact.first_name, 'last_name': message.contact.last_name, 'user_id': message.contact.user_id, "date": message.json["date"]    }

                queue.append(message.chat.id)


                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton('Да', callback_data=str(message.chat.id))
                button2 = types.InlineKeyboardButton('Нет', callback_data=str(message.chat.id)+'a')
                markup.add(button1)
                markup.add(button2)
                if message.from_user.last_name != None:
                    bot.send_message(boss[0], text=f"Регестрация нового пользователя c: \nИменем: `{message.from_user.first_name} {message.from_user.last_name}`\nНиком: `{message.from_user.username}` \nТелефоном: `{message.contact.phone_number}` ", parse_mode='MarkdownV2', reply_markup=markup)
                else:
                    bot.send_message(boss[0], text=f"Регестрация нового пользователя c: \nИменем: `{message.from_user.first_name}`\nНиком: `{message.from_user.username}` \nТелефоном: ||{message.contact.phone_number}|| ", parse_mode='MarkdownV2', reply_markup=markup)


                with open("contacts", "w") as file:
                    file.write(str(contacts))

                bot.send_message(message.chat.id, "Пользуясь данным продуктом вы соглашаетесь с https://clck.ru/3A3qa5 \n /start", reply_markup=ReplyKeyboardRemove())

        @bot.message_handler(commands=['info'])
        def info(message):
            bot.send_message(message.chat.id, str(contacts))

        @bot.message_handler(commands=['admin_menu'])
        def admin_menu(message):
            if message.chat.id in boss:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Задать алфавит пароля")
                btn2 = types.KeyboardButton("Задать время смены пароля")
                btn3 = types.KeyboardButton("Управление пользователями")
                markup.add(btn1, btn2, btn3)
                bot.send_message(message.chat.id, text="Меню появилось", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "У вас недостаточно прав для этого действия")


        @bot.message_handler(commands=['menu'])
        def menu(message):
            if message.chat.id in trusted_chats:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Активный пароль")
                btn2 = types.KeyboardButton("Отключить уведомления")
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, text="Меню появилось", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text="Пожалуйста зарегестрируйтесь\n/register")

        @bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            try:
                bot.send_message(int(call.data), 'Ваша заявка на регестрацию одобрена')
                bot.send_message(boss[0], 'Заявка на регестрацию одобрена')
                if call.data not in trusted_chats:
                    trusted_chats.append(int(call.data))
                    with open("trust", "w") as file:
                        file.write(str(trusted_chats))
                menu(message)
            except:
                try:
                    trusted_chats.pop(trusted_chats.index(int(call.data[:-1])))
                except:
                    pass
                bot.send_message(int(call.data[:-1]), 'Ваша заявка на регестрацию отклонена')
                bot.send_message(boss[0], 'Заявка на регестрацию отклонена')
                with open("trust", "w") as file:
                    file.write(str(trusted_chats))
                start(message)

            print(trusted_chats)



        @bot.message_handler(content_types=['text'])
        def func(message):
            global send_password_by_time
            global password_alphabet
            global get_alphabet
            global delete_user
            global set_time
            global contacts
            global action
            global trusted_chats
            global proc
            action = 1



            if message.chat.id in trusted_chats:
                if(message.text == "Активный пароль"):
                    #
                    ##
                    ###
                    ####
                    #####
                    ######
                    #######
                    ########            ВЫСЫЛАЕМ АКТИВНЫЙ ПАРОЛЬ
                    with open("password", 'r') as f:
                        password = f.read()
                    #password = 'active_password'
                    bot.send_message(message.chat.id, text=f"`{password}`", parse_mode='MarkdownV2')
                    f.close()
                    action = 0
                elif message.text == "Отключить уведомления":
                    contacts_number = False
                    for i in list(contacts.keys()):
                        if contacts[i]['user_id'] == message.chat.id:
                            contacts_number = i
                    try:
                        contacts.pop(contacts_number)
                    except:
                        print("Something went wrong")

                    try:
                        trusted_chats.pop(index(message.chat.id))
                    except:
                        pass

                    bot.send_message(message.chat.id, "Вы успешно отключили уведомления", reply_markup=ReplyKeyboardRemove())
                    bot.send_message(message.chat.id, "Для дальнейших действий оправьте /start")
                    with open("contacts", "w") as file:
                        file.write(str(contacts))

                    action = 0

                if action == 1:
                    if message.chat.id in boss:
                        if message.text == "Задать алфавит пароля":
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            btn1 = types.KeyboardButton("Заглавные буквы")
                            btn2 = types.KeyboardButton("Маленькие буквы")
                            btn3 = types.KeyboardButton("Все буквы")
                            btn4 = types.KeyboardButton("Цифры")
                            btn5 = types.KeyboardButton("Цифры и маленькие буквы")
                            btn6 = types.KeyboardButton("Цифры и заглавные буквы")
                            btn7 = types.KeyboardButton("Цифры и все буквы")
                            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
                            bot.send_message(message.chat.id, text="Меню появилось", reply_markup=markup)
                            bot.send_message(message.chat.id, "Пожалуйста введите все символы, которые могут содержаться в пароле.")
                            get_alphabet = 1
                        elif get_alphabet == 1:
                            get_alphabet = 0

                            if message.text == "Заглавные буквы":
                                password_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            elif message.text == "Маленькие буквы":
                                password_alphabet = "abcdefghijklmnopqrstuvwxyz"
                            elif message.text == "Все буквы":
                                password_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            elif message.text == "Цифры":
                                password_alphabet = "0123456789"
                            elif message.text == "Цифры и маленькие буквы":
                                password_alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
                            elif message.text == "Цифры и заглавные буквы":
                                password_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            elif message.text == "Цифры и все буквы":
                                password_alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            else:
                                get_alphabet = -1

                            if get_alphabet != -1:
                                print(password_alphabet)
                                with open("password_alphabet", "w") as file:
                                    file.truncate(0)
                                    file.write(password_alphabet)
                                file.close()
                                print("Я вроде как записал алфавит")

                                bot.send_message(message.chat.id, text="Алфавит пароля успешно создан. При следуюшем создании пароля он будет учтен.", reply_markup=ReplyKeyboardRemove())
                                start(message)
                            else:
                                bot.send_message(message.chat.id, "Извините, я ничего не понял\n/start", reply_markup=ReplyKeyboardRemove())

                        elif message.text == "Задать время смены пароля":
                            bot.send_message(message.chat.id, "Напишите время, через которое будет сменяться пароль в МИНУТАХ.", reply_markup=ReplyKeyboardRemove())
                            set_time = 1
                        elif set_time == 1:
                            try:
                                int(message.text)
                                with open("time", 'w') as f:
                                    f.write(message.text)
                                f.close()
                            except:
                                bot.send_message(message.chat.id, "Время указано неверно\nПопробуйте заново.")

                            times = int(message.text)
                            bot.send_message(message.chat.id, f"Новое время смены пароля установлено.\nПароль обновится через: {times//60} ч. {times%60} мин.")
                            set_time = 0

                            #restart_thread()       it`s not working
                            start(message)
                            proc.terminate()
                            raise "Restart system"
                            # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

                        elif message.text == "Управление пользователями":
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            btn1 = types.KeyboardButton("Список пользователей")
                            btn2 = types.KeyboardButton("Удалить пользователя")
                            markup.add(btn1, btn2)
                            bot.send_message(message.chat.id, text="Меню появилось", reply_markup=markup)

                        elif message.text == "Список пользователей":
                            print(contacts)
                            phone_numbers = contacts.keys()
                            datas = ''
                            for i in phone_numbers:
                                try:
                                    datas+= i+" : "+contacts[i]["first_name"]+' '+contacts[i]["last_name"]+" : "+str(contacts[i]["user_id"])+'\n'
                                except:
                                    datas+= i+" : "+contacts[i]["first_name"]+" : "+str(contacts[i]["user_id"])+'\n'
                            bot.send_message(message.chat.id, datas)
                            admin_menu(message)
                        elif message.text == "Удалить пользователя":
                            delete_user = 1
                            bot.send_message(message.chat.id, "Введите номер телефона или id пользователя")
                        elif delete_user == 1:
                            delete_user = 0
                            data_for_delete = message.text
                            try:
                                if data_for_delete.find("+") != -1:
                                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                                    print(contacts[data_for_delete.split('+')[1]]["user_id"], trusted_chats)
                                    trusted_chats.pop(trusted_chats.index(contacts[data_for_delete.split('+')[1]]["user_id"]))
                                    contacts.pop(data_for_delete.split('+')[1])
                                    bot.send_message(message.chat.id, "Пользователь удалён")
                                    admin_menu(message)
                            except:
                                if contacts.find(data_for_delete) != -1:
                                    if contacts.keys().index(data_for_delete) != -1:
                                        trusted_chats.pop(trusted_chats.index(contacts[data_for_delete]["user_id"]))
                                        contacts.pop(data_for_delete)
                                    # Надо доделать
                                else:
                                    bot.send_message(message.chat.id, "По введённым данным ничего не найдено")

                            #print(contacts)
                            #print(trusted_chats)
                            with open("contacts", "w") as file:
                                file.write(str(contacts))




                        else:
                            bot.send_message(message.chat.id, "Извините, я не понимаю. Для меню нажмите на /start")
                    else:
                        bot.send_message(message.chat.id, "Извините, я не понимаю. Для меню нажмите на /start")



            else:
                bot.send_message(message.chat.id, text="Пожалуйста зарегестрируйтесь\n/register")

        bot.polling()
    except:
        print("Restarted the system")
