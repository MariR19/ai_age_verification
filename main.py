from Worker import worker
import settings

def main():
    cfg = settings.Settings('settings.ini')
    worker.start_job(cfg)


if __name__ == "__main__":
    main()
