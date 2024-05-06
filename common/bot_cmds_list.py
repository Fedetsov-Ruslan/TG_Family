from aiogram.types import BotCommand


private = [
    BotCommand(command='about', description='Создайте группу, пригласите в нее бота, а затем пригласите в нее свою второу половинку.'),
    BotCommand(command='start', description='Начать работу бота'),
    BotCommand(command='stop', description='Завершить работу с ботом')
]


group = [
    BotCommand(command='about', description='Нажмите кнопку старт или напишите команду "/start", после чего вы перейдете в личку с ботом.'),
    BotCommand(command='start', description='Начать'),
    BotCommand(command='stop', description='Завершить работу с ботом')
]