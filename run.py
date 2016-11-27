import traceback


def main():
    print("Starting bot...")
    try:
        from dcbot import bot
        bot = bot.DestinyChildBot()
        print("Connecting...", end='', flush=True)
        bot.run()
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    main()