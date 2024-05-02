import mysql.connector
from mysql.connector import Error
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from middleware_casas import get_alerta_recursiva

TOKEN = "6833534632:AAG2QJ5-v0RTRlJeRIrQOmlvsSRrdjGBAQE"

DB_HOST = "localhost"
DB_USER = "user2"
DB_PASSWORD = "123"
DB_NAME = "casas_db"

active_chats = set()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("¡Hola! Soy un bot que puede recibir mensajes de 'casa vacía ###' o 'casa habitada ###' mas el numero de casa '123'.")

    active_chats.add(update.message.chat_id)

def handle_status_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text.lower()

    palabras = message_text.split()

    if len(palabras) < 3 or palabras[0] not in ['casa', 'habitada'] or palabras[1] not in ['vacía', 'habitada']:
        update.message.reply_text("Formato incorrecto. Utiliza 'casa vacía <numero>' o 'casa habitada <numero>'.")
        return

    try:
        numero_de_casa = int(palabras[2])
    except ValueError:
        update.message.reply_text("No se proporcionó un número de casa válido.")
        return

    if palabras[1] == 'vacía':
        update.message.reply_text(f"Se ha registrado que la casa {numero_de_casa} está vacía.")
        update_database(0, numero_de_casa)
    else:
        update.message.reply_text(f"Se ha registrado que la casa {numero_de_casa} está habitada.")
        update_database(1, numero_de_casa)

    active_chats.add(update.message.chat_id)

def update_database(is_empty: int, numero_de_casa: int) -> None:
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM casas WHERE idcasas = %s", (numero_de_casa,))
        existing_record = cursor.fetchone()

        if existing_record:
            cursor.execute("UPDATE casas SET statusUSO = %s WHERE idcasas = %s", (is_empty, numero_de_casa))
            print(f"DEBUG: Se ha actualizado el estado de la casa {numero_de_casa}.")
        else:
            cursor.execute("INSERT INTO casas (idcasas, statusUSO) VALUES (%s, %s)", (numero_de_casa, is_empty))
            print(f"DEBUG: Se ha registrado una nueva casa: {numero_de_casa} {'vacía' if is_empty else 'habitada'}.")

        connection.commit()

    except Error as e:
        print("Error al conectarse a la base de datos:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def send_alerts(context: CallbackContext) -> None:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    cursor.execute("SELECT mensaje FROM alertas")

    alerts = cursor.fetchall()

    if alerts:
        for chat_id in active_chats:
            for alert in alerts:
                context.bot.send_message(chat_id=chat_id, text=alert[0])

    connection.commit()

    cursor.close()
    connection.close()



def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_status_message))

    updater.job_queue.run_repeating(send_alerts, interval=10)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()