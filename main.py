import telebot
from telebot import types
import json
import random


API_TOKEN = "5245011384:AAFIdUOMdGsrz3fBVYn9GC0zojfBkWxLARs"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message,"Нажмите /start чтобы начать")


@bot.message_handler(commands=["start"])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
    rmk.add("Да,конечно","Не хочу...")
    try:
        msg = bot.reply_to(message,
                        "Привет!Я - Литературная сова,хочешь проверить мои знания?",
                        reply_markup=rmk)
        bot.register_next_step_handler(msg,user_answer1_step)
    except:
        bot.reply_to(message, "Попробуйте еще раз, введите команду /start")


def user_answer1_step(message):
    id=message.chat.id
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add("Писателя","Поэта","Книгу","Монолог","Завершить")
    try:
        if message.text == "Да,конечно": 
            msg = bot.reply_to(message,
                                "Хочешь, я назову тебе :", 
                                reply_markup=rmk)
            bot.register_next_step_handler(msg,user_answer2_step)
        elif message.text == "Не хочу...":
                bot_end(id)      
    except Exception as e:
        bot.reply_to(message, "Попробуйте еще раз, введите команду /start")

def user_answer2_step(message):
    id=message.chat.id
    
    try:
        if message.text == "Завершить":
                bot_end(id)
        else:
            with open("v1.json","r") as file:
                obj = json.load(file)
                i = random.randint(0,(len(obj.get(message.text))-1))
                answer = obj.get(message.text)[i]
                msg=bot.reply_to(message, answer)
            bot.register_next_step_handler(msg, user_answer2_step)         
    except Exception as e:
            bot.reply_to(message, "Попробуйте еще раз2")

def bot_end(chat_id):
    bot.send_message(chat_id,"Ну и ладно, тогда я пойду что-то почитаю...",reply_markup=types.ReplyKeyboardRemove() )
    with open("animation/read_owl.tgs","rb") as animation:
        bot.send_animation(chat_id,animation)



bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()