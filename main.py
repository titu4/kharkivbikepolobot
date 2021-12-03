"""
This bot creates training session polls and announcements
"""

from telegram import (
    Poll,
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Updater,
    CallbackContext,
    Filters,
    MessageHandler,
)

help_text = "/help"
poll_weekly_text = "/pw"
poll_training_time_text = "/pt"
training_announcement_text = "/ta"
set_group_id_text = "/sg"
allowed_users = [319478839, 378399460]

b_get_date = False
date = ""
b_get_time = False
time = ""
b_once = False
group_id = "@P0LLoTestGroup"


def set_group_id_handler(update: Update, context: CallbackContext):
    global group_id
    parm_num = len(update.message.text.split(" "))-1
    if parm_num == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="ERROR: group_id not changed\n" +
                 "group_id=" + group_id + "\n" +
                 "parm1 is empty"
        )
    else:
        group_id = "@" + update.message.text.split(" ")[1]
        context.bot.send_message(chat_id=update.effective_chat.id, text="group_id="+group_id)


def poll_weekly_handler(update: Update, context: CallbackContext):

    parms = update.message.text.split(" ")
    parm_num = len(parms) - 1

    if parm_num < 2:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="ERROR: poll not created,\n" +
                 "at least 2 parameters are required:\n" +
                 "parm1 - date start (dd.mm)\n" +
                 "parm2 - date finish (dd.mm)"
        )
    else:
        date_start = parms[1]
        date_finish = parms[2]

        options = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "-"]
        message = context.bot.send_poll(
            group_id,
            "[Планы] " + date_start + " - " + date_finish + " Тренировка",
            options,
            is_anonymous=False,
            allows_multiple_answers=True,
        )

        payload = {
            message.poll.id: {
                "questions_1": options,
                "message_id_1": message.message_id,
                "chat_id": group_id,
                "answers_1": 0,
            }
        }
        context.bot_data.update(payload)


def poll_training_time_handler(update: Update, context: CallbackContext):

    parms = update.message.text.split(" ")
    parm_num = len(parms) - 1

    if parm_num < 2:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="ERROR: poll not created,\n" +
                 "at least 2 parameters are required:\n" +
                 "parm1 - day (dddd)\n" +
                 "parm2 - date (dd.mm)"
        )
    else:
        parm_day = parms[1]
        parm_date = parms[2]
        options = ["<=14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", ">=21:00", "-"]

        message = context.bot.send_poll(
            group_id,
            "[Тренировка] " + parm_day + " " + parm_date + " - Время сбора:",
            options,
            is_anonymous=False,
            allows_multiple_answers=True,
        )
        # save data for later use
        payload = {
            message.poll.id: {
                "questions_2": options,
                "message_id_2": message.message_id,
                "chat_id": group_id,
                "answers_2": 0,
            }
        }
        context.bot_data.update(payload)


def help_handler(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The following commands are available:\n\n" +
             "/pw date date        create Mon-Sun poll\n" +
             "/pt day date           create training time poll\n" +
             "/ta day date time  announce the training\n" +
             "/sg group_id           change group id"
    )


def training_announcement_handler(update: Update, context: CallbackContext):

    parms = update.message.text.split(" ")
    parm_num = len(parms) - 1

    if parm_num < 3:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="ERROR: announcement not created,\n" +
                 "at least 3 parameters are required:\n" +
                 "parm1 - day\n" +
                 "parm2 - date (dd.mm)\n" +
                 "parm3 - time (hh:mm)"
        )
    else:

        parm_day = parms[1]
        parm_date = parms[2]
        parm_time = parms[3]

        context.bot.send_message(
            chat_id=group_id,
            text="[Тренировка]\n\n" +
                 "Когда: " + parm_day + ", " + parm_date + " " + parm_time + "\n" +
                 "Где: https://g.co/kgs/YowiUL\n" +
                 "Будет: да"
        )


def message_handler(update: Update, context: CallbackContext):

    user = update.message.from_user
    if user['id'] not in allowed_users:
        update.message.reply_text(
            text="ERROR: you are not allowed to use this bot\n" +
                 "please contact the creator (@OhManIAmWorried)"
        )
        return False

    text = update.message.text.split(" ")[0]

    if text == help_text:
        return help_handler(update=update, context=context)

    if text == poll_weekly_text:
        return poll_weekly_handler(update=update, context=context)

    if text == poll_training_time_text:
        return poll_training_time_handler(update=update, context=context)

    if text == set_group_id_text:
        return set_group_id_handler(update=update, context=context)

    if text == training_announcement_text:
        return training_announcement_handler(update=update, context=context)

    if text[0] == "/":
        update.message.reply_text(
            text="ERROR: command not recognized"
        )


def main():
    print('Start')

    updater = Updater(
        token='2079505885:AAG2nroyo1tXOoS_4Kxdhx8ZbKJeQ4LPngs',
        use_context=True,
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
