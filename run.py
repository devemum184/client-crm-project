import multiprocessing
import bot
import dashboard


def run_dash():
    dashboard.app.run(debug=False, port=8050)


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=bot.main)
    p2 = multiprocessing.Process(target=run_dash)

    p1.start()
    p2.start()

    p1.join()
    p2.join()