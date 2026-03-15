import multiprocessing
import bot
import dashboard

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=bot.main)
    p2 = multiprocessing.Process(target=lambda: dashboard.app.run(debug=False, port=8050))
    p1.start()
    p2.start()
    p1.join()
    p2.join()