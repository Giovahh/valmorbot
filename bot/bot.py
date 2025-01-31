from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from functools import wraps

expenses = []
requests = []
AUTHORIZED_USERS = [2043215276, 987654321]  # Sostituisci con gli ID Telegram degli utenti autorizzati
user_requests = {}  # Dizionario per memorizzare chi ha fatto la richiesta

def restricted(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in AUTHORIZED_USERS:
            update.message.reply_text("Non sei autorizzato a usare questo comando.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Benvenuto nel bot delle finanze dei Valmor!")

@restricted
def spesaaggiungi(update: Update, context: CallbackContext) -> None:
    try:
        price = float(context.args[0])
        expenses.append(price)
        update.message.reply_text(f"Spesa aggiunta: {price:.2f}D")
    except (IndexError, ValueError):
        update.message.reply_text("Per favore, fornisci un prezzo valido.")

@restricted
def spesarimuovi(update: Update, context: CallbackContext) -> None:
    try:
        index = int(context.args[0]) - 1
        if 0 <= index < len(expenses):
            removed = expenses.pop(index)
            update.message.reply_text(f"Spesa rimossa: {removed:.2f}D")
        else:
            update.message.reply_text("Indice di spesa non valido.")
    except (IndexError, ValueError):
        update.message.reply_text("Per favore, fornisci un indice valido.")

@restricted
def spesareset(update: Update, context: CallbackContext) -> None:
    global expenses
    expenses = []
    update.message.reply_text("Tutte le spese sono state resettate.")

@restricted
def spese(update: Update, context: CallbackContext) -> None:
    if expenses:
        total = sum(expenses)
        expense_list = "\n".join([f"{i+1}. {expense:.2f}D" for i, expense in enumerate(expenses)])
        update.message.reply_text(f"Lista delle spese:\n{expense_list}\n\nTotale: {total:.2f}D")
    else:
        update.message.reply_text("Non ci sono spese.")

def richiestacrea(update: Update, context: CallbackContext) -> None:
    try:
        request_text = ' '.join(context.args)
        if not request_text.strip():
            update.message.reply_text("La richiesta non può essere vuota.")
            return
        username = update.message.from_user.username
        user_id = update.message.from_user.id
        requests.append(f"{request_text} (da @{username})")
        user_requests[len(requests)] = user_id
        update.message.reply_text("La tua richiesta è stata creata.")
    except IndexError:
        update.message.reply_text("Per favore, fornisci una richiesta valida.")

@restricted
def vedererichieste(update: Update, context: CallbackContext) -> None:
    if requests:
        requests_list = "\n".join([f"{i+1}. {request}" for i, request in enumerate(requests)])
        update.message.reply_text(f"Elenco delle richieste:\n{requests_list}")
    else:
        update.message.reply_text("Non ci sono richieste.")

@restricted
def richiestereset(update: Update, context: CallbackContext) -> None:
    global requests, user_requests
    requests = []
    user_requests = {}
    update.message.reply_text("Tutte le richieste sono state resettate.")

@restricted
def richiestaaccetta(update: Update, context: CallbackContext) -> None:
    try:
        index = int(context.args[0]) - 1
        if 0 <= index < len(requests):
            accepted_request = requests.pop(index)
            user_id = user_requests.pop(index + 1)
            context.bot.send_message(user_id, text=f"La tua richiesta contenente: {accepted_request} è stata accettata.")
            update.message.reply_text(f"Richiesta accettata: {accepted_request}")
        else:
            update.message.reply_text("Indice di richiesta non valido.")
    except (IndexError, ValueError):
        update.message.reply_text("Per favore, fornisci un indice valido.")

@restricted
def richiestarifiuta(update: Update, context: CallbackContext) -> None:
    try:
        index = int(context.args[0]) - 1
        if 0 <= index < len(requests):
            refused_request = requests.pop(index)
            user_id = user_requests.pop(index + 1)
            context.bot.send_message(user_id, text=f"La tua richiesta contenente: {refused_request} è stata rifiutata.")
            update.message.reply_text(f"Richiesta rifiutata: {refused_request}")
        else:
            update.message.reply_text("Indice di richiesta non valido.")
    except (IndexError, ValueError):
        update.message.reply_text("Per favore, fornisci un indice valido.")

@restricted
def help(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - Avvia il bot\n"
        "/spesaaggiungi - Aggiungi una spesa\n"
        "/spesarimuovi - Rimuovi una spesa\n"
        "/spesareset - Resetta tutte le spese\n"
        "/spese - Mostra la lista delle spese e il totale\n"
        "/vedererichieste - Visualizza tutte le richieste\n"
        "/richiestacrea - Crea una richiesta\n"
        "/richiestereset - Resetta tutte le richieste\n"
        "/richiestaaccetta - Accetta una richiesta\n"
        "/richiestarifiuta - Rifiuta una richiesta\n"
        "/getuserid - Ottieni l'ID utente"
    )
    update.message.reply_text(help_text)

def getuserid(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    update.message.reply_text(f"ID utente: {user_id}\nUsername: @{username}")

def main() -> None:
    updater = Updater("7942794227:AAGheI1wd-6fc8DTixxdvb60xSU_LGM-ykA", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("spesaaggiungi", spesaaggiungi))
    dispatcher.add_handler(CommandHandler("spesarimuovi", spesarimuovi))
    dispatcher.add_handler(CommandHandler("spesareset", spesareset))
    dispatcher.add_handler(CommandHandler("spese", spese))
    dispatcher.add_handler(CommandHandler("richiestacrea", richiestacrea))
    dispatcher.add_handler(CommandHandler("vedererichieste", vedererichieste))
    dispatcher.add_handler(CommandHandler("richiestereset", richiestereset))
    dispatcher.add_handler(CommandHandler("richiestaaccetta", richiestaaccetta))
    dispatcher.add_handler(CommandHandler("richiestarifiuta", richiestarifiuta))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("getuserid", getuserid))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
