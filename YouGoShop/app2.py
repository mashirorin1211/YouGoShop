import os, secrets

if __name__ == '__main__':
    os.system("sqlite_web -H 0.0.0.0 -x -p 5005 main_project/yougoshop.db&")
