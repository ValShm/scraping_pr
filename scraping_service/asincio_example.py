import asyncio
#корутина для задач
async def task_coroutine(value):
    # вывод сообщения
    print(f'task {value} is running')
    # краткая блокировка
    await asyncio.sleep(1)
#определение главной корутины
async def main():
    # вывод сообщения
    print('main coroutine started')
    # запуск нескольких задач
    started_tasks = [asyncio.create_task(task_coroutine(i)) for i in range(10)]
    # выделение времени, необходимого на то, чтобы некоторые из задач запустились
    await asyncio.sleep(0.1)
    # получение всех задач
    tasks = asyncio.all_tasks()
    # вывод сведений обо всех задачах
    for task in tasks:
        print(f'> {task.get_name()}, {task.get_coro()}')
    # ждём завершения всех задач
    for task in started_tasks:
        await task
#запуск asyncio-программы
asyncio.run(main())