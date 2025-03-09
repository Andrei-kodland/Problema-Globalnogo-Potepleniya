import telebot
import random
import os
from model import get_class  # Ensure your 'get_class' function works fine
from bot_logic import gen_pass, gen_emodji, flip_coin  # Import functions from bot_logic

# Replace 'TOKEN' with your bot's token
bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши команду /hello, /bye, /pass, /photo, /emodji , /deystviyaizzakotorihglobalnoepoteplenienachinaetsya, /antideystviyaprotivglobalnogopotepleniya или /coin  ")

@bot.message_handler(commands=['deystviyaizzakotorihglobalnoepoteplenienachinaetsya'])
def send_hello(message):
    
    messages = [
        "Чтобы способствовать глобальному потеплению и увеличению его последствий, можно перечислить несколько действий, которые негативно воздействуют на климат. Во-первых, сжигание ископаемых видов топлива, таких как уголь, нефть и газ, для производства энергии, транспорта и промышленности значительно увеличивает выбросы углекислого газа (CO₂) и других парниковых газов в атмосферу.",
        "Вырубка лесов также играет важную роль, так как уничтожение деревьев уменьшает способность Земли поглощать углерод и способствует выбросу CO₂. Использование неустойчивых сельскохозяйственных практик, таких как чрезмерное использование удобрений, пестицидов и вырубка лесов под сельское хозяйство, приводит к выбросам метана и закиси азота.",
        "Задержка отходов на свалках также вызывает выбросы метана, мощного парникового газа. Использование традиционных транспортных средств с двигателями внутреннего сгорания и отсутствие перехода на электромобили увеличивает уровень загрязнения атмосферы углекислым газом.",
        "Нерациональное использование воды, выкачка воды для сельского хозяйства и индустриальных нужд приводит к дополнительным затратам энергии для ее очистки и транспортировки. Наконец, поддержка и инвестирование в предприятия, которые используют экологически вредные методы производства и ресурсы, а также отказ от продвижения политики по сокращению выбросов парниковых газов, усиливают изменения климата и ухудшают состояние окружающей среды."
    ]
    
    
    random_message = random.choice(messages)
    
    
    bot.reply_to(message, random_message)

@bot.message_handler(commands=['antideystviyaprotivglobalnogopotepleniya'])
def send_hello(message):
    
    messages = [
        "Чтобы помочь в борьбе с глобальным потеплением и уменьшить его последствия, можно предпринять несколько важных действий. Во-первых, стоит перейти на возобновляемые источники энергии, такие как солнечная, ветряная или гидроэнергия, а также поддерживать инициативы, способствующие их развитию. Улучшение энергоэффективности, использование энергоэкономных приборов, светодиодного освещения и лучшая изоляция дома также помогут сократить потребление энергии.",
        "Важно выбирать устойчивые виды транспорта — пользоваться общественным транспортом, ездить на велосипеде, ходить пешком или перейти на электрические автомобили. Кроме того, стоит сажать деревья и поддерживать усилия по восстановлению лесов, так как они поглощают CO₂.",
        "Снижение отходов, переработка материалов и отказ от одноразового пластика помогут уменьшить количество мусора на свалках, которые выделяют метан. Поддержка устойчивого сельского хозяйства, выбор растительной пищи и сокращение пищевых отходов также играют важную роль в борьбе с изменением климата.",
        "Экономия воды, использование водосберегающих технологий и поддержка экологически чистых бизнесов, которые используют возобновляемые источники энергии, также способствует снижению углеродных выбросов. Наконец, важно повышать осведомленность о проблеме изменения климата, поддерживать экологически ориентированные политики и выступать за более строгие меры по защите окружающей среды."
    ]
    
    
    random_message = random.choice(messages)
    
    
    bot.reply_to(message, random_message)
    
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    '''When a user sends an image, the bot will process and analyze it.'''
    try:
        # If there's no photo, let the user know
        if not message.photo:
            bot.send_message(message.chat.id, "You forgot to upload a picture. Please try again!")
            return

        # Get file information for the highest resolution photo
        file_info = bot.get_file(message.photo[-1].file_id)
        file_name = file_info.file_path.split('/')[-1]  # Extract the filename

        # Download the file to a local directory
        downloaded_file = bot.download_file(file_info.file_path)

        # Ensure the local path is valid and create the directory if it doesn't exist
        local_path = f'./images/{file_name}'
        os.makedirs(os.path.dirname(local_path), exist_ok=True)  # Create folder if it doesn't exist
        
        # Save the file locally
        with open(local_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Log the image path for debugging
        print(f"Image saved to: {local_path}")

        # Path to your model (ensure this path is correct)
        model_path = r"C:\Users\1505105\OneDrive\Рабочий стол\Ai bot\keras_model.h5"
        labels_path = r"C:\Users\1505105\OneDrive\Рабочий стол\Ai bot\labels.txt"

        # Call the get_class function for classification
        result = get_class(model_path=model_path, labels_path=labels_path, image_path=local_path)

        # Debugging the result
        print(f"Model result (raw): {result}")

        # Log the type of the result
        print(f"Result type: {type(result)}")

        # If result is a tuple, extract the label from it
        if isinstance(result, tuple):
            label = result[0]  # Assuming the label is the first item in the tuple
            print(f"Extracted label: {label}")
        else:
            label = result  # Otherwise, use the result directly
            print(f"Extracted label: {label}")

        # Check if result is valid
        if label is None:
            bot.send_message(message.chat.id, "Unable to classify the image. Please try again.")
            return
        
        # Log the label to check if it's what we expect
        print(f"Final label: {label}")

        # Send the result to the user based on classification
        if isinstance(label, str):
            if label.lower() == "bad":  # Assuming the result is "bad" or "good"
                bot.send_message(message.chat.id, "This image is bad for global warming.")
            elif label.lower() == "good":
                bot.send_message(message.chat.id, "This image is good for global warming.")
            else:
                bot.send_message(message.chat.id, f"Unrecognized label: {label}")
        else:
            bot.send_message(message.chat.id, "The result from the model was not in the expected format.")

    except Exception as e:
        # Log the exception and send a specific error message
        print(f"Error occurred: {e}")
        bot.send_message(message.chat.id, f"Something went wrong while processing the image. Error: {e}")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(10)  # Устанавливаем длину пароля, например, 10 символов
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

# Запускаем бота
bot.polling()




        

