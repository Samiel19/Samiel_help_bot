import requests
import time
import datetime
import re
import pickle
import funcs

from settings import (API_URL, API_CATS_URL, BOT_TOKEN, ERROR_TEXT,
                      CAT_TEXT_ERR, CAT_REMAIND_TEXT,
                      units, offset, time_units,
                      tasks_dict)


def wait(updates):
    counter = 0
    updates_new = updates
    while counter < 50 and updates == updates_new:
        counter += 1
        time.sleep(0.1)
        updates_new = requests.get(
            f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}'
            ).json()
    return updates_new


def main_bot(API_URL, API_CATS_URL, BOT_TOKEN, ERROR_TEXT,
             CAT_TEXT_ERR, CAT_REMAIND_TEXT,
             units, offset, time_units,
             tasks_dict):
    while True:
        print(tasks_dict)
        with open("task_dict.pickle", "+wb") as file:
            pickle.dump(tasks_dict, file)
        now = datetime.datetime.now()
        done = []
        for task, t in tasks_dict.items():
            if now >= t:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?'
                             f'chat_id={task[1]}&text=Кот напоминает!'
                             f' Пора {task[0]}!')
                funcs.cat_sender(API_CATS_URL,
                                 API_URL,
                                 BOT_TOKEN,
                                 task[1],
                                 CAT_REMAIND_TEXT,
                                 ERROR_TEXT)
                done.append(task)
        for i in done:
            tasks_dict.__delitem__(i)
        updates = requests.get(
            f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}'
            ).json()
        if updates['result']:
            for result in updates['result']:
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                text = result['message']['text']
                question = text[8:]
                questions_dict = {
                    'напомни': 'Хорошо, я напомню!',
                    'что': 'Вот, что ты должен сделать:',
                    'удали': 'Какую задачу удаляем? Имя, дай мне имя!',
                    }
                if text.lower().startswith(f'{("Удали").lower()}'):
                    requests.get(
                        f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}'
                        f'&text={questions_dict["удали"]}\n\n'
                        f'{funcs.my_tasks(tasks_dict, chat_id)}'
                        )
                    updates = wait(updates)
                    for result in updates['result']:
                        text = result['message']['text']
                        if text == 'ПУСТАЯ':
                            text = ''
                        if (text.lower(), chat_id) in tasks_dict.keys():
                            del tasks_dict[text.lower(), chat_id]
                            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?'
                                         f'chat_id={chat_id}&text=Done!')
                        else:
                            requests.get(
                                f'{API_URL}{BOT_TOKEN}/sendMessage?'
                                f'chat_id={chat_id}'
                                f'&text=Нет такой задачи('
                                )
                    offset += 1
                    break
                if text.lower().startswith(f'{("Что").lower()}'):
                    requests.get(
                        f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}'
                        f'&text={questions_dict["что"]}\n\n'
                        f'{funcs.my_tasks(tasks_dict, chat_id)}'
                        )
                    break
                if text.lower().startswith(f'{("напомни").lower()}'):
                    if (question.lower(), chat_id) in tasks_dict.keys():
                        requests.get(
                            f'{API_URL}{BOT_TOKEN}/'
                            f'sendMessage?chat_id={chat_id}'
                            f'&text=Такая задачка от '
                            'тебя уже есть( Создадим другую?'
                        )
                        break
                    requests.get(
                        f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}'
                        f'&text={questions_dict["напомни"]}'
                        )
                    time.sleep(1)
                    requests.get(
                        f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&'
                        'text=А через какое время? '
                        'Сколько дней, часов, минут, секунд? '
                        'Но выбери что-то одно и укажи единицы!'
                        )
                    updates = wait(updates)
                    if updates['result']:
                        for result in updates['result']:
                            offset = result['update_id']
                            answer = result['message']['text']
                            try:
                                bot_time = float(
                                    re.findall('(\d+)', answer)[0]
                                    )
                            except IndexError:
                                requests.get(
                                    f'{API_URL}{BOT_TOKEN}/'
                                    f'sendMessage?'
                                    f'chat_id={chat_id}&text=Ошибочка! '
                                    f'Попробуем ещё раз? Что напомнить?'
                                             )
                                break
                            now = datetime.datetime.now()
                            clear_answer = re.sub(
                                r'[^\w\s]', '', answer
                                ).lower()
                            t = funcs.string_to_time(clear_answer, units)
                            if t in time_units.keys():
                                requests.get(
                                    f'{API_URL}{BOT_TOKEN}/sendMessage?'
                                    f'chat_id={chat_id}&text=Принято! '
                                    f'Значит напомню {question} '
                                    f'через {bot_time} '
                                    f'{time_units[t][0]}!'
                                            )
                                tasks_dict[
                                    (question, chat_id)
                                    ] = datetime.datetime.fromtimestamp(
                                    now.timestamp() + (
                                        bot_time *
                                        time_units[t][1]
                                        )
                                )
                            else:
                                funcs.cat_sender(API_CATS_URL,
                                                 API_URL,
                                                 BOT_TOKEN,
                                                 chat_id,
                                                 CAT_TEXT_ERR,
                                                 ERROR_TEXT)
                else:
                    funcs.cat_sender(API_CATS_URL,
                                     API_URL,
                                     BOT_TOKEN,
                                     chat_id,
                                     CAT_TEXT_ERR,
                                     ERROR_TEXT)

        time.sleep(2.5)


if __name__ == '__main__':
    try:
        with open("task_dict.pickle", 'rb+') as file:
            tasks_dict = pickle.load(file)
    except IOError:
        try:
            with open("task_dict.pickle", 'wb+') as file:
                tasks_dict = pickle.load(file)
        except EOFError as error:
            print(error)
    main_bot(API_URL, API_CATS_URL, BOT_TOKEN, ERROR_TEXT,
             CAT_TEXT_ERR, CAT_REMAIND_TEXT,
             units, offset, time_units,
             tasks_dict)