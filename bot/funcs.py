import requests


def cat_sender(api_cats_url: str,
               api_url: str,
               bot_token: str,
               chat_id: str,
               cat_text_err: str,
               error_text: str,
               ):
    cat_response = requests.get(api_cats_url)
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']
        if cat_text_err:
            requests.get(
                f'{api_url}{bot_token}/sendMessage?'
                f'chat_id={chat_id}&text={cat_text_err}'
                )
        requests.get(
            f'{api_url}{bot_token}/sendPhoto?'
            f'chat_id={chat_id}&photo={cat_link}'
            )
    else:
        requests.get(
            f'{api_url}{bot_token}/sendMessage?'
            f'chat_id={chat_id}&text={error_text}'
            )


def string_to_time(string: str, units: dict) -> str:
    list_str = string.split()
    for key, unit in units.items():
        if list_str[-1] in unit:
            return key


def my_tasks(tasks: dict,
             chat: int) -> str:
    tasks_list = [
        (
            f'{task[0]:} ---> {time.strftime("%d-%m-%Y %H:%M:%S")}'
            ) for task, time in tasks.items() if task[1] == chat
        ]
    str_task_list = '\n\n'.join(tasks_list)
    if len(str_task_list) == 0:
        str_task_list = 'Ничего!)'
    return str_task_list
