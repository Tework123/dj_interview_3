import os
import sys
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


def main():
    # load_dotenv(os.path.join(basedir, '.env'))
    load_dotenv()
    env = os.environ.get('ENV')

    if env == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_interview_3.settings.production')

    if env == 'development':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_interview_3.settings.development')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
