import config
import none

bot = none.create_bot(config)
none.load_plugins()

app = bot.asgi

if __name__ == '__main__':
    bot.run(host=config.HOST, port=config.PORT)
