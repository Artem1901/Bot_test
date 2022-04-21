import codecs
import os
import requests
import telebot
import datetime
from telebot import types


token = '5350862817:AAGZcjBItg2uoTzkJG1bMLEoPZQE1HyhiMo'
bot = telebot.TeleBot(token)
d = {"инф-ка": '1', "лит-ра": '2', "алгебра": '3', "ино иэ": '4', "физика": '5',
     "геометрия": '6',
     "русский язык": '7', "химия": '8', "история": '9', "ино са": '0', 'немецкий язык': 'a',
     'астрономия': 'b'}
d1 = {'1': "инф-ка", '2': "лит-ра", '3': "алгебра", '4': "ино, группа иэ", '5': "физика",
      '6': "геометрия",
      '7': "русский язык", '8': "химия", '9': "история", '0': "ино, группа са", 'a': 'немецкий язык',
      'b': 'астрономия'}
wd = {"понедельник": 1, "вторник": 2, "среда": 3, "четверг": 4, "пятница": 5, "суббота": 6}
time = {1: "09:00-09:40", 2: "09:55-10:35", 3: "10:50-11:30", 4: "11:45-12:25", 5: "12:40-13:20",
        6: "13:35-14:15", 7: "14:25-15:05"}
time_dist = {1: "09:00-09:30", 2: "09:55-10:25", 3: "10:50-11:20", 4: "11:45-12:15", 5: "12:40-13:10",
             6: "13:35-14:05", 7: "14:20-14:50"}
__author1__ = "@Talziar"
__author2__ = "@artemgoriunov"
wdnum = 0
num = 0
anum = 0
zoom_num = 0
chat_id = ""  # demo
channel_id = ""  # demo
stroki = []
urllist = []
usersid = []
op = ['591545559']
operators = set(op)
try:
    with codecs.open('dist.txt', 'r', encoding='utf-8') as fi:
        dist = int(fi.read())
except OSError:
    with codecs.open('dist.txt', 'w', encoding='utf-8') as fi:
        fi.seek(0)
        fi.write('0')
try:
    with codecs.open('whitelist.txt', 'r', encoding='utf-8') as fi:
        stroki = map(int, fi.readlines())
except OSError:
    with codecs.open('whitelist.txt', 'w', encoding='utf-8') as fi:
        fi.seek(0)
whitelist = set(stroki)
try:
    with codecs.open('id.txt', 'r', encoding='utf-8') as fi:
        t = fi.readlines()
        for irt in t:
            usersid.append(int(irt))
        usersidset = set(usersid)
except OSError:
    with codecs.open('id.txt', 'w', encoding='utf-8') as fi:
        fi.seek(0)
    usersidset = set([])
    usersid = []
if 591545559 not in whitelist:
    with codecs.open('whitelist.txt', 'w', encoding='utf-8') as fi:
        fi.write('591545559\n')
actionKeyboard = types.ReplyKeyboardMarkup()
actionKeyboard.row('Узнать расписание \n📅', 'Узнать ДЗ \n📖')
actionKeyboard.row('Посмотреть команды \n📔', 'Узнать данные zoom \n📹')
actionKeyboard.row('Просмотреть файлы \n📁', 'Изменить дз \n📖')
subjectKeyboard = types.ReplyKeyboardMarkup(False, True)
subjectKeyboard.row("Инф-ка", "Лит-ра", "Алгебра", "Астрономия")
subjectKeyboard.row("Ино ИЭ", "Ино СА", "Физика", "Геометрия")
subjectKeyboard.row("Русский язык", "Химия", "История", 'Немецкий язык')
timetableKeyboard = types.ReplyKeyboardMarkup(False, True)
timetableKeyboard.row("Понедельник", "Вторник", "Среда")
timetableKeyboard.row("Четверг", "Пятница", "Суббота")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                      'или набери /commands для списка команд.',
                     reply_markup=actionKeyboard)
    if message.from_user.id not in usersidset:
        with codecs.open('id.txt', 'a', encoding='utf-8') as f:
            f.write(str(message.from_user.id) + '\n')
        usersidset.add(message.from_user.id)
        usersid.append(message.from_user.id)


@bot.message_handler(commands=['knowadmin'])
def become_admin(message):
    msg = bot.send_message(message.chat.id, 'Создатели - @Talziar, @artemgoriunov')
    bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                      'или набери /commands для списка команд.',
                     reply_markup=actionKeyboard)


@bot.message_handler(commands=['adminrebirth'])
def become_admin(message):
    msg = bot.send_message(message.chat.id, 'Вы уверены, что хотите отправить заявку '
                                            'на становление администратором?/n Ответьте да или нет')
    bot.register_next_step_handler(msg, becoming_admin)


@bot.message_handler(commands=['commands'])
def help_message(message):
    msg_text = 'Список команд:\n/alltasks - вывод всех заданий на экран\n/belltableshow - показ расписания звонков\n' \
               '/help - для связи с администраторами\n' \
               '/adminrebirth - для запроса на получение админ-прав\n' \
               '/knowadmin - узнать авторов'
    if message.from_user.id in whitelist:
        msg_text += '\n/timetablechange - чтобы изменить расписание на определенный день\n' \
                    '/zoomchange - чтобы изменить идентификатор и пароль для zoom по определенному предмету\n' \
                    '/taskadd - добавление задания к существующему по определенному предмету\n' \
                    '/announce - сделать объявление в группе'
    if str(message.from_user.id) in operators:
        msg_text += '\n/newadmin - добавить нового администратора\n/deleteadmin - забрать права администратора' \
                    '\n/distchange - сменить режим обучения'
    bot.send_message(message.chat.id, msg_text, reply_markup=actionKeyboard)


@bot.message_handler(commands=['newadmin'])
def add_new_admin(message):
    if str(message.from_user.id) in operators:
        msg = bot.send_message(message.chat.id, "Кого ты хочешь сделать новым админиcтратором?")
        bot.register_next_step_handler(msg, adding_new_admin)
    else:
        bot.send_message(message.chat.id, "У тебя нет прав для совершения этого действия")


@bot.message_handler(commands=['deleteadmin'])
def delete_admin(message):
    if str(message.from_user.id) in operators:
        msg = bot.send_message(message.chat.id, "У кого ты хочешь забрать права администратора?")
        bot.register_next_step_handler(msg, deleting_admin)
    else:
        bot.send_message(message.chat.id, "У тебя нет прав для совершения этого действия")


@bot.message_handler(commands=['announce'])
def announce(message):
    if message.from_user.id in whitelist:
        msg = bot.send_message(message.chat.id, "О чем ты хочешь сообщить?")
        bot.register_next_step_handler(msg, announcement)
    else:
        bot.send_message(message.chat.id, "У тебя нет прав использовать эту команду")


@bot.message_handler(commands=['help'])
def admin_help(message):
    msg = bot.send_message(message.chat.id, "О чем ты хочешь сообщить администраторам?")
    bot.register_next_step_handler(msg, admin_helping)


@bot.message_handler(commands=['alltasks'])
def all_tasks_output(message):
    try:
        with codecs.open('task.txt', encoding='utf-8') as f:
            lines = f.readlines()
    except OSError:
        with codecs.open('task.txt', 'w', encoding='utf-8') as f:
            f.seek(0)
        bot.send_message(message.chat.id, "Нет домашнего задания")
    else:
        for i in lines:
            if i != '':
                bot.send_message(message.chat.id, d1[i[0]].capitalize() + ': ' + i[2].lower() + i[3:])


@bot.message_handler(commands=['distchange'])
def dist_change(message):
    if str(message.from_user.id) in operators:
        global dist
        try:
            with codecs.open('dist.txt', 'r', encoding='utf-8') as f:
                dist = int(f.read())
        except OSError:
            with codecs.open('dist.txt', 'w', encoding='utf-8') as f:
                f.seek(0)
                f.write('0')
                dist = 0
                bot.send_message(message.chat.id, "Установлен школьный режим обучения")
        else:
            with codecs.open('dist.txt', 'w', encoding='utf-8') as f:
                f.seek(0)
                f.write(str(abs(dist - 1)))
                dist = abs(dist - 1)
                if dist == 0:
                    bot.send_message(message.chat.id, "Установлен школьный режим обучения")
                else:
                    bot.send_message(message.chat.id, "Установлен дистанционный режим обучения")
    else:
        bot.send_message(message.chat.id, "У тебя нет прав использовать эту команду")


@bot.message_handler(commands=['belltableshow'])
def bell_table_show(message):
    belltable = 'Расписание звонков\n'
    for i in range(1, 8):
        belltable += str(i) + ')' + time[i] + '\n'
    bot.send_message(message.chat.id, belltable)
    belltable_dist = 'Расписание звонков во время дистанционного обучения\n'
    for i in range(1, 8):
        belltable_dist += str(i) + ')' + time_dist[i] + '\n'
    bot.send_message(message.chat.id, belltable_dist)


@bot.message_handler(commands=['taskchange'])
def task_change(message):
    if message.from_user.id not in whitelist:
        bot.send_message(message.chat.id, "У тебя нет прав изменять домашнее задание")
    else:
        msg = bot.send_message(message.chat.id, 'По какому предмету ты хочешь внести дз?', reply_markup=subjectKeyboard)
        bot.register_next_step_handler(msg, subject_input)


@bot.message_handler(commands=['taskadd'])
def task_add(message):
    if message.from_user.id not in whitelist:
        bot.send_message(message.chat.id, "У тебя нет прав изменять домашнее задание")
    else:
        msg = bot.send_message(message.chat.id, 'По какому предмету ты хочешь добавить дз?',
                               reply_markup=subjectKeyboard)
        bot.register_next_step_handler(msg, subject_add)


@bot.message_handler(commands=['uploadphoto'])
def send_photo(message):
    msg = bot.send_message(message.chat.id, "Go on, honey")
    bot.register_next_step_handler(msg, sending_photo)


def sending_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    msg = bot.send_message(message.chat.id, 'В какую директорию вы хотите положить данный файл?',
                           reply_markup=subjectKeyboard)
    bot.register_next_step_handler(msg, get_file_name, file_info)


def get_file_name(message, file_info):
    dr = message.text
    msg = bot.send_message(message.chat.id, "Как назвать фото?")
    r = requests.get(
        'https://api.telegram.org/file/bot1066163670:AAFsraOqL5QCp-dHXN9J5LaFlBfFXCBuTm8/' + file_info.file_path)
    bot.register_next_step_handler(msg, save_photo, r, dr)


def save_photo(message, r, direct):
    file_name = str(message.text) + '.jpg'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, direct)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    path = os.path.join(dest_dir, file_name)
    open(path, 'wb').write(r.content)
    bot.send_message(message.chat.id, "Фото добавлено, господин!")


@bot.message_handler(commands=['deletephoto'])
def delete_photo(message):
    msg = bot.send_message(message.chat.id, "Выбери предмет, "
                                            "по которому хочешь удалить фото", reply_markup=subjectKeyboard)
    bot.register_next_step_handler(msg, photo_choose)


def photo_choose(message):
    if show_list_all_photos(message):
        msg = bot.send_message(message.chat.id, "Введи название фото, которое хочешь удалить")
        bot.register_next_step_handler(msg, deleting_photo, message.text)


def deleting_photo(message, direct):
    file_name = message.text
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, direct)
    file_path = os.path.join(dest_dir, file_name)
    try:
        os.remove(file_path)
    except OSError as e:
        bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте еще раз")
        delete_photo(message)
        return
    bot.send_message(message.chat.id, 'Фото успешно удалено')


@bot.message_handler(commands=['listallphotos'])
def list_all_photos(message):
    msg = bot.send_message(message.chat.id, "Выбери предмет", reply_markup=subjectKeyboard)
    bot.register_next_step_handler(msg, show_list_all_photos)


def show_list_all_photos(message):
    for root, dirs, files in os.walk(message.text):
        for filename in files:
            dest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), message.text)
            path = os.path.join(dest_dir, filename)
            img = open(path, 'rb')
            bot.send_photo(message.chat.id, img, filename)
        return True
    bot.send_message(message.chat.id, "По этому предмету нет фотографий")
    return False


@bot.message_handler(commands=['timetablechange'])
def timetable_change(message):
    if message.from_user.id not in whitelist:
        bot.send_message(message.chat.id, "У тебя нет прав изменять расписание")
    else:
        msg = bot.send_message(message.chat.id, 'На какой день недели ты хочешь изменить расписание?',
                               reply_markup=timetableKeyboard)
        bot.register_next_step_handler(msg, day_input)


@bot.message_handler(commands=['zoomchange'])
def zoom_ind_change_choice(message):
    if message.from_user.id not in whitelist:
        bot.send_message(message.chat.id, "У тебя нет прав изменять данные zoom")
    else:
        msg = bot.send_message(message.chat.id,
                               "По какому предмету ты хочешь изменить идентификатор и пароль для входа в zoom?",
                               reply_markup=subjectKeyboard)
        bot.register_next_step_handler(msg, subject_zoom_input)


@bot.message_handler(content_types=['text'])
def send_text(message):
    st = message.text.lower()
    global whitelist
    if message.chat.id != channel_id and message.chat.id != chat_id:
        if st == "узнать дз \n📖":
            msg = bot.send_message(message.chat.id, 'По какому предмету ты хочешь узнать дз?',
                                   reply_markup=subjectKeyboard)
            bot.register_next_step_handler(msg, task_output)
        elif st == "узнать расписание \n📅":
            msg = bot.send_message(message.chat.id, 'На какой день недели ты хочешь узнать расписание?',
                                   reply_markup=timetableKeyboard)
            bot.register_next_step_handler(msg, time_table_output)
        elif st == "узнать данные zoom \n📹":
            msg = bot.send_message(message.chat.id,
                                   "По какому предмету ты хочешь получить идентификатор и пароль для входа в zoom?",
                                   reply_markup=subjectKeyboard)
            bot.register_next_step_handler(msg, zoom_ind_out)
        elif st == "Спасибо!":
            bell_table_show()
        elif st == "изменить дз \n📖":
            if message.from_user.id in whitelist:
                msg = bot.send_message(message.chat.id, 'По какому предмету ты хочешь внести дз?',
                                       reply_markup=subjectKeyboard)
                bot.register_next_step_handler(msg, subject_input)
            else:
                bot.send_message(message.chat.id,
                                 "У вас нет прав использовать эту команду. "
                                 "Свяжитесь с администратором для предоставления доступа через команду /help.")
        elif st == "посмотреть команды \n📔":
            msg_text = 'Список команд:\n/alltasks - вывод всех заданий на экран\n' \
                       '/belltableshow - показ расписания звонков\n/help - для связи с администраторами\n' \
                       '/knowadmin - узнать создателей бота\n' \
                       '/adminrebirth - для запроса на получение админ-прав'

            if message.from_user.id in whitelist:
                msg_text += '\n/timetablechange - чтобы изменить расписание на определенный день\n' \
                            '/zoomchange - чтобы изменить идентификатор и пароль для zoom по определенному предмету\n' \
                            '/taskadd - добавление задания к существующему по определенному предмету\n' \
                            '/announce - сделать объявление в группе\n' \
                            '/uploadphoto - Выгрузить фото в бота'
            if str(message.from_user.id) in operators:
                msg_text += '\n/newadmin - добавить нового администратора\n' \
                            '/deleteadmin - забрать права администратора' \
                            '\n/distchange - сменить режим обучения'
            bot.send_message(message.chat.id, msg_text, reply_markup=actionKeyboard)
        elif st == "просмотреть файлы \n📁":
            bot.send_message(message.chat.id, "Файлы для 10В:\nhttps://yadi.sk/d/RoGusYVeKUkPcg?w=1",
                             reply_markup=actionKeyboard)
        else:
            bot.send_message(message.chat.id, 'Такой команды не существует', reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def subject_input(subject):
    if subject.text != '/start':
        global num
        try:
            num = d[subject.text.lower()]
        except KeyError:
            msg = bot.reply_to(subject, 'Тварь болотная, все еще не можешь запомнить предметы?. Попробуй еще раз.',
                               reply_markup=subjectKeyboard)
            bot.register_next_step_handler(msg, subject_input)
        else:
            message = bot.reply_to(subject, 'Укажи домашнее задание по этому предмету')
            bot.register_next_step_handler(message, task_input)
    else:
        bot.send_message(subject.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def subject_add(subject):
    if subject.text != '/start':
        global anum
        try:
            anum = d[subject.text.lower()]
        except KeyError:
            msg = bot.reply_to(subject, 'Тварь болотная, все еще не можешь запомнить предметы?. Попробуй еще раз.',
                               reply_markup=subjectKeyboard)
            bot.register_next_step_handler(msg, subject_input)
        else:
            try:
                with codecs.open('task.txt', encoding='utf-8') as f:
                    for line in f:
                        if line[0] == anum:
                            msg = bot.reply_to(subject, line[2:] + '\nЧто ты хочешь добавить к этому заданию?',
                                               reply_markup=actionKeyboard)
                            bot.register_next_step_handler(msg, adding_task)
                            break
                    else:
                        bot.send_message(subject.chat.id, 'Дз по этому предмету не существует',
                                         reply_markup=actionKeyboard)
            except OSError:
                with codecs.open('task.txt', 'w', encoding='utf-8') as f:
                    f.seek(0)
                bot.send_message(subject.chat.id, 'Дз по этому предмету не существует', reply_markup=actionKeyboard)
    else:
        bot.send_message(subject.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def day_input(message):
    if message.text != '/start':
        global wdnum
        try:
            wdnum = wd[message.text.lower()]
        except KeyError:
            msg = bot.reply_to(message, 'Такого дня недели не существует. Попробуй еще раз.',
                               reply_markup=timetableKeyboard)
            bot.register_next_step_handler(msg, day_input)
        else:
            message = bot.reply_to(message, 'Укажите расписание на выбранный день по следующему правилу:\n'
                                            '1)Если урока нет,то нужно написать blank;\n'
                                            '2)Все предметы записывать через запятую Без пробела. Например:\n'
                                            'blank,blank,Математика,Математика,Русский язык,Литература,Иностранный')
            bot.register_next_step_handler(message, time_table_input)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def subject_zoom_input(message):
    if message.text != '/start':
        global zoom_num
        try:
            zoom_num = d[message.text.lower()]
        except KeyError:
            msg = bot.reply_to(message, 'Такого предмета не существует. Попробуй еще раз.',
                               reply_markup=subjectKeyboard)
            bot.register_next_step_handler(msg, subject_zoom_input)
        else:
            msg = bot.reply_to(message,
                               'Укажите идентификатор и пароль для входа в zoom для предмету, который вы выбрали')
            bot.register_next_step_handler(msg, zoom_ind_in)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def time_table_input(message):
    if message.text != '/start':
        lines = []
        try:
            with codecs.open('timetable.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except OSError:
            with codecs.open('timetable.txt', 'w', encoding='utf-8') as f:
                f.seek(0)
        with codecs.open('timetable.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                if int(line[0]) != wdnum:
                    f.write(line)
            f.seek(0, 2)
            f.write(str(wdnum) + ")" + message.text + '\n')
        bot.reply_to(message, 'Расписание изменено. Тебе еще что-то нужно?', reply_markup=actionKeyboard)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def time_table_output(message):
    if message.text != '/start':
        try:
            chislo = wd[message.text.lower()]
        except KeyError:
            msg = bot.reply_to(message, 'Такого дня недели не существует. Попробуй еще раз.',
                               reply_markup=timetableKeyboard)
            bot.register_next_step_handler(msg, time_table_output)
        else:
            try:
                with codecs.open('timetable.txt', encoding='utf-8') as f:
                    for line in f:
                        if int(line[0]) == chislo:
                            items = str(line[2:]).split(',')
                            out = ''
                            if dist == 1:
                                times = time_dist
                            else:
                                times = time
                            for ind, val in enumerate(items, 1):
                                if val == 'blank':
                                    out += str(ind) + ')\n'
                                else:
                                    out += str(ind) + ')' + times[ind] + ' ' + val + '\n'
                            bot.reply_to(message, out, reply_markup=actionKeyboard)
                            break
                    else:
                        bot.send_message(message.chat.id, 'Расписание на этот день не занесено в базу данных',
                                         reply_markup=actionKeyboard)
            except OSError:
                with codecs.open('timetable.txt', 'w', encoding='utf-8') as f:
                    f.seek(0)
                bot.send_message(message.chat.id, "Расписание не занесено в базу данных", reply_markup=actionKeyboard)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def task_input(task):
    if task.text != '/start':
        now = datetime.datetime.now()
        lines = []
        try:
            with codecs.open('task.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except OSError:
            with codecs.open('task.txt', 'w', encoding='utf-8') as f:
                f.seek(0)
        with codecs.open('task.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                if line[0] != num:
                    f.write(line)
            f.seek(0, 2)
            f.write(str(num) + ")" + task.text + ". Дата добавления задания " + now.strftime("%d-%m-%Y %H:%M") + "\n")
        bot.reply_to(task, 'Задание записано. Тебе еще что-то нужно?', reply_markup=actionKeyboard)
        """ for i in whitelist:
           try:
               # if not i == task.from_user.id:
               bot.send_message(i, "@" + task.from_user.username +
                               " изменил задание по предмету - " +
                                d1[num].capitalize() + '\nВот его содержимое: ' + task.text)
           except telebot.apihelper.ApiTelegramException:
               continue
           except TypeError:
               bot.send_message(i, "Что-то пошло не так. Проверьте есть ли у вас имя пользователя")
               break
        """
    else:
        bot.send_message(task.chat.id, 'Нажми одну из кнопок '
                                       'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


""" 
Почему не так, идиот?
if message.text.lower() == '/start':
        bot.send_message(task.chat.id, 'Нажми одну из кнопок '
                                       'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)
        return
"""


@bot.message_handler(content_types=['text'])
def task_output(message):
    if message.text != '/start':
        global num
        try:
            num = d[message.text.lower()]
        except KeyError:
            msg = bot.reply_to(message, 'Тварь болотная, все еще не можешь запомнить предметы? Попробуй еще раз.',
                               reply_markup=subjectKeyboard)
            bot.register_next_step_handler(msg, task_output)
        else:
            try:
                with codecs.open('task.txt', encoding='utf-8') as f:
                    for line in f:
                        if line[0] == num:
                            bot.reply_to(message, str(line[2:]).replace(';', '\n'), reply_markup=actionKeyboard)
                            break
                    else:
                        bot.send_message(message.chat.id, 'Дз по этому предмету не существует',
                                         reply_markup=actionKeyboard)
            except OSError:
                with codecs.open('task.txt', 'w', encoding='utf-8') as f:
                    f.seek(0)
                bot.send_message(message.chat.id, 'Дз по этому предмету не существует', reply_markup=actionKeyboard)
            bot.send_message(message.chat.id, 'Тебе еще что-то нужно?', reply_markup=actionKeyboard)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def zoom_ind_in(message):
    if message.text != '/start':
        lines = []
        try:
            with codecs.open('zoom.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except OSError:
            with codecs.open('zoom.txt', 'w', encoding='utf-8') as f:
                f.seek(0)
        with codecs.open('zoom.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                if line[0] != zoom_num:
                    f.write(line)
            f.seek(0, 2)
            sp = str(message.text).split()
            f.write(str(zoom_num) + ")" + "Идентификатор - " + sp[0] + ". " + "Пароль - " + sp[1] + "\n")
        bot.reply_to(message, 'Данные записаны. Тебе еще что-то нужно?', reply_markup=actionKeyboard)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def zoom_ind_out(message):
    if message.text != '/start':
        try:
            chislo = d[message.text.lower()]
        except KeyError:
            msg = bot.reply_to(message,
                               'Такого предмета не существует. Попробуй еще раз.', reply_markup=subjectKeyboard)
            bot.register_next_step_handler(msg, zoom_ind_out)
        else:
            try:
                with codecs.open('zoom.txt', encoding='utf-8') as f:
                    for line in f:
                        if line[0] == chislo:
                            bot.reply_to(message, line[2:], reply_markup=actionKeyboard)
                            break
                    else:
                        bot.send_message(message.chat.id,
                                         'Идентификатор zoom для этого предмета не внесен в базу данных',
                                         reply_markup=actionKeyboard)
            except OSError:
                with codecs.open('zoom.txt', 'w', encoding='utf-8') as f:
                    f.seek(0)
                bot.send_message(message.chat.id, "Идентификаторы zoom не внесены в базу данных",
                                 reply_markup=actionKeyboard)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def adding_new_admin(message):
    mes = message.text
    if mes != '/start':
        if not mes.isdigit():
            msg = bot.send_message(message.chat.id, "Ты ввел что-то не так. Попробуй еще раз.")
            bot.register_next_step_handler(msg, adding_new_admin)
        else:
            whitelist.add(int(mes))
            try:
                with codecs.open('whitelist.txt', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except OSError:
                with codecs.open('whitelist.txt', 'w', encoding='utf-8') as f:
                    f.seek(0)
            with codecs.open('whitelist.txt', 'w', encoding='utf-8') as f:
                for line in lines:
                    if int(line) != int(mes):
                        f.write(line)
                f.seek(0, 2)
                f.write(mes + '\n')
            bot.send_message(message.chat.id, "Новый администратор успешно добавлен!")
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def deleting_admin(message):
    mes = message.text
    if mes == "383193252":
        bot.send_message(message.chat.id, "Ты не можешь забрать права администратора у моего создателя")
    elif mes != '/start':
        if not mes.isdigit():
            msg = bot.send_message(message.chat.id, "Ты ввел что-то не так. Попробуй еще раз.")
            bot.register_next_step_handler(msg, adding_new_admin)
        else:
            whitelist.discard(int(mes))
            try:
                with codecs.open('whitelist.txt', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except OSError:
                with codecs.open('whitelist.txt', 'w', encoding='utf-8') as f:
                    f.seek(0)
            with codecs.open('whitelist.txt', 'w', encoding='utf-8') as f:
                for line in lines:
                    if int(line) != int(mes):
                        f.write(line)
            bot.send_message(message.chat.id, "Права администратора забраны")
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def announcement(message):
    # bot.forward_message(chat_id, message.from_user.id, message.message_id)
    for i in usersid:
        try:
            if not i == message.from_user.id:
                bot.send_message(i, "Уважаемый(ая) " + "@" + message.from_user.username +
                                 " попросил(а) меня передать пользователям:", "\n" + message.text)
        except telebot.apihelper.ApiTelegramException:
            continue
    bot.send_message(message.chat.id, "Сообщение успешно отправлено!")


@bot.message_handler(content_types=['text'])
def admin_helping(message):
    if message.text != '/start':
        for i in whitelist:
            try:
                if not i == message.from_user.id:
                    bot.send_message(i,
                                     "Личность с именем " + "@" + message.from_user.username +
                                     " попросило меня передать администраторам:", "\n" + str(message.text))
            except telebot.apihelper.ApiTelegramException:
                continue
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Ты ввел(а) что-то нет так, попробуй еще раз')
                bot.register_next_step_handler(msg, admin_help)
        bot.send_message(message.chat.id, "Сообщение успешно отправлено!")
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


@bot.message_handler(content_types=['text'])
def becoming_admin(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Нажми одну из кнопок ' + 'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)
        return
    if message.text.lower() == 'да':
        try:
            name = message.from_user.first_name + ' ' + message.from_user.last_name
            user_id = str(message.from_user.id)
            bot.send_message(383193252, name + ' хочет стать админом. ' + 'Вы согласны? Вот его айди:' + '\n' + user_id)
        except TypeError:
            msg = bot.send_message(message.chat.id,
                                   'Something is wrong. Do you have both firstname and surname in Telegram?')
            bot.register_next_step_handler(msg, becoming_admin)
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Запрос на получение прав администратора отменен')
    else:
        msg = bot.send_message(message.chat.id, 'Вы ввели что-то не так. Так вы хотите стать администратором? да/нет')
        bot.register_next_step_handler(msg, becoming_admin)


@bot.message_handler(content_types=['text'])
def adding_task(message):
    mes = message.text
    if mes != '/start':
        lines = []
        try:
            with codecs.open('task.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except OSError:
            with codecs.open('task.txt', 'w', encoding='utf-8') as f:
                f.seek(0)
        with codecs.open('task.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                if line[0] != anum:
                    f.write(line)
                else:
                    f.seek(0, 2)
                    f.write(line[:-1] + ' ' + mes + '\n')
        bot.reply_to(message, 'Задание записано. Тебе еще что-то нужно?', reply_markup=actionKeyboard)
    else:
        bot.send_message(message.chat.id, 'Нажми одну из кнопок '
                                          'или набери /commands для списка команд.',
                         reply_markup=actionKeyboard)


bot.polling(none_stop=True)
