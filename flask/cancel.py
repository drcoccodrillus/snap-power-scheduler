import schedule

def cancel_shutdown_scheduler():
    schedule.clear()

if __name__ == '__main__':
    cancel_shutdown_scheduler()
