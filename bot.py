import spacy
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent,Update
from telegram.ext import Application, CommandHandler, InlineQueryHandler, MessageHandler, filters,ConversationHandler,CallbackContext
import logging
import random


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

animals_facts = {
    "what is a cat?": "A cat is a small domesticated carnivorous mammal with soft fur, a short snout, and retractable claws. It is often kept as a pet.",
    "what do cats eat?": "Cats are obligate carnivores, which means they need a diet of meat. They typically eat small animals like rodents, birds, and fish.",
    "how long do cats live?": "The average lifespan of a domestic cat is around 13-17 years, though some cats can live into their 20s.",
    "why do cats purr?": "Cats purr for various reasons, including contentment, relaxation, and even when they are in pain as a self-soothing mechanism.",
    "how do cats communicate?": "Cats communicate through a variety of vocalizations like meowing, purring, hissing, and growling, as well as through body language such as tail positioning, ear movement, and eye contact.",
    "why do cats knead?": "Kneading is when cats push their paws in and out against a soft surface. This behavior is a comforting action that they carry over from kittenhood, when they knead their mother’s belly to stimulate milk flow.",
    "do cats dream?": "Yes, cats do dream! Like humans, they experience REM (Rapid Eye Movement) sleep, which is when dreaming occurs. You might notice your cat twitching or moving slightly during this phase.",
    "can cats see in the dark?": "Cats have excellent night vision. While they can’t see in complete darkness, their eyes are much more sensitive to light than human eyes, allowing them to see in very low light conditions.",
    "why do cats like boxes?": "Cats are naturally drawn to small, enclosed spaces like boxes because they make them feel safe and secure. It also gives them a place to hide and stalk 'prey' from.",
    "why do cats bring 'gifts'?": "When a cat brings you a 'gift' like a dead mouse or bird, it’s actually a sign of affection. In the wild, cats bring prey back to their colony, so your cat is showing that it considers you part of its family.",
    "why do cats have whiskers?": "Cats use their whiskers as highly sensitive tools to gauge the size of objects and spaces, helping them navigate their environment, especially in the dark. Whiskers also pick up on vibrations and changes in the air, alerting cats to nearby movement.",
    "how do cats show affection?": "Cats show affection in various ways, including purring, rubbing against you, slow blinking, kneading, and sometimes even gently biting. Each cat has its own unique way of expressing love.",
    "do cats recognize their names?": "Yes, cats can recognize their names! Studies have shown that cats can differentiate their names from other words and may respond when called, though they might choose to ignore you if they’re not interested.",
    "why do cats sleep so much?": "Cats are crepuscular, meaning they are most active during dawn and dusk. They sleep for about 12-16 hours a day to conserve energy for hunting, even if they’re well-fed pets.",
    
    "what is a dog?": "A dog is a domesticated carnivorous mammal that has been selectively bred over thousands of years for various behaviors, sensory capabilities, and physical attributes. Dogs are known for their loyalty, intelligence, and companionship.",
    "what do dogs eat?": "Dogs are omnivores, meaning they can eat a variety of foods including meat, vegetables, and grains. However, a balanced diet rich in protein is essential for their health.",
    "how long do dogs live?": "The average lifespan of a dog varies by breed, but most dogs live between 10-13 years. Smaller breeds tend to live longer, sometimes up to 16-18 years.",
    "why do dogs wag their tails?": "Dogs wag their tails as a form of communication. A wagging tail usually indicates happiness or excitement, but the speed, height, and direction of the wag can convey other emotions such as nervousness or aggression.",
    "why do dogs bark?": "Dogs bark to communicate with their owners and other animals. They might bark to alert you to danger, express excitement, seek attention, or respond to other dogs.",
    "how do dogs show affection?": "Dogs show affection by wagging their tails, licking, leaning against you, bringing you toys, and following you around. They might also rest their head on you or give you a 'doggy smile.'",
    "can dogs recognize their owners?": "Yes, dogs have an incredible sense of smell and vision that allows them to recognize their owners even from a distance. They can also remember your scent for long periods.",
    "why do dogs roll in the grass?": "Dogs might roll in the grass to scratch an itch, cool off, or mark their scent. Sometimes they do it to mask their own scent with something they find interesting or strong-smelling in the grass.",
    "why do dogs tilt their heads?": "Dogs tilt their heads to better hear and understand what you're saying, especially if they’re trying to recognize a word or tone of voice. It also helps them see your facial expressions more clearly.",
    "why do dogs dig holes?": "Dogs dig for several reasons, including to cool off, hide food, or satisfy their instinct to burrow. Some breeds are more prone to digging due to their hunting or working backgrounds."
}


async def state0_handler(update, context):
    """if there's a question mark, then it's a question!"""
    if update.message.text[-1] == '?':
        await update.message.reply_text(random.choice([
            "Why do you ask?",
            "What do you think?",
            "That's a good question. How would you answer?",
        ]))
    else:
        await update.message.reply_text(random.choice([
            "Oh, I see. Tell me why that is.",
            "Alright. Please go on...",
            "I understand. And so?",
        ]))
    return



async def state0_handler(update: Update, context: CallbackContext) -> str:
    """Use SpaCy to handle state0"""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(update.message.text)
    reply = ''
    
    if doc[0].tag_ in ['WDT', 'WP', 'WP$', 'WRB']:
        reply = "This is a wh-question."
    elif (doc[0].tag_ in ['MD']) or (doc[0].tag_ in ['VBP', 'VBD', 'VBZ'] and doc[1].tag_ in ['PRP', 'PRP$']):
        reply = "This is a yes/no question."
    else:
        reply = "This doesn't seem to be a question."
    if reply:
        await update.message.reply_text(reply)
    return 'STATE0'


async def start(update, context):
    await update.message.reply_text("Hello! I'm your Telegram Bot. Type /help for available commands.")

async def help_command(update, context):
    await update.message.reply_text("Available commands:\n"
                              "/start - Start the bot\n"
                              "/help - Display available commands\n"
                              "/cat - Get a random cat picture\n"
                              "/dogs -Get a random dog picture\n"
                              "/cancel - Cancel the bot\n"
                              "Ask me questions about cats or dogs!")

async def cat(update, context):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    cat_url = data[0]['url']
    await update.message.reply_photo(cat_url)
    
async def dog(update,context):
    response=requests.get("https://api.thedogapi.com/v1/images/search")
    data = response.json()
    dog_url = data[0]['url']
    await update.message.reply_photo(dog_url)


async def answer_animals_questions(update, context):
    question = update.message.text.lower()
    answer = animals_facts.get(question, "I don't know the answer to that question. Ask me something else about cats or dogs!")
    await update.message.reply_text(answer)

async def cancel(update, context):
    await update.message.reply_text("Thanks for the chat. I'll be off then!")
    return ConversationHandler.END

# Define a function to handle inline queries
def inline_query(update, context):
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Echo",
            input_message_content=InputTextMessageContent(query)
        )
    ]
    update.inline_query.answer(results)

def main():
    api_key = '7278215422:AAFVP2-G_byQ86ouuE7eG8OUc1krRc-Xk38'

    application = Application.builder().token(api_key).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cat", cat))
    application.add_handler(CommandHandler("dog", dog))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_animals_questions))

    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling(1.0)

    application.idle()

if __name__ == '__main__':
    main()
