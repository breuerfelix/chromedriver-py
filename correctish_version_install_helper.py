import platform
from subprocess import Popen, PIPE

def input_until_ok(question, options):
    while True:
        print(question)
        for option in options[1]:
            print(option)
        pick = input("Choice: ").lower()
        if pick in options[0]:
            return pick
        else:
            print("Sorry about that. You need to pick one of the given options. Try again.")


def sort_out_chrome_version():
    os_str = platform.system()
    if "Darwin" in os_str:
        proc = Popen("/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version", shell=True, stdout=PIPE)
        proc.wait()
        chrome_version_str = proc.stdout.read()
        return chrome_version_str.decode().split(" ")[2]
    elif "Windows" in os_str:
        print("Implement Windows chrome check")
        exit()
    elif "Linux" in os_str:
        proc = Popen("google-chrome --version", shell=True)
        proc.wait()
        print(proc.stdout)
        print("Finish implementing Linux chrome check")
        exit()


def install_correct_version_of_chromedriver(version):
    proc = Popen("pip3 show chromedriver-py", shell=True, stderr=PIPE, stdout=PIPE)
    proc.wait()
    res_str = proc.stderr.read().decode()
    res_str_out = proc.stdout.read().decode()
    current_version = ""
    if "warning" in res_str.lower():
        print("no current version of chromedriver-py locally")
    else:
        current_version = res_str_out.split('\n')[1].split(' ')[1]
    if current_version == version:
        return
    if current_version == "":
        print("You nave no chromedriver-py installed and you need %s" % version)
    if current_version != "":
        print("You have chromedriver_py %s but you need %s to match your chrome version" % (current_version, version))
    proc = Popen("pip3 install chromedriver-py==%s" % version, shell=True, stderr=PIPE)
    proc.wait()
    error_msg = proc.stderr.read().decode()
    if "ERROR" in error_msg:
        print("Looks like there is currently no matching chromedriver-py in pip, which is really a pitty")
        print("There is a chance that a very recent version of chromedriver-py might work anyway.")
        pick = input_until_ok("Would you to try to install a more recent version just to see it helps? (there is a chance this will work)", [['y', 'n'], ['(y)es', '(n)o']])
        if pick == "y":
            proc = Popen("pip3 index versions chromedriver-py", shell=True, stdout=PIPE)
            version_data = proc.stdout.read().decode()
            rows = version_data.split("\n")
            for row in rows:
                if "Available versions:" in row:
                    versions = row.split(", ")[1:5]
                    for version_ in versions:
                        proc = Popen("pip3 install chromedriver-py==%s" % version_, shell=True, stdout=PIPE)
                        proc.wait()
                        command_output = proc.stdout.read().decode()
                        rows = command_output.split("\n")
                        if len(rows) == 1:
                            # alread installed
                            pass
                        elif len(rows) == 2:
                            # no such version
                            pass
                        elif len(rows) > 2:
                            # installed!
                            print("Yay, we managed to install a only slightly outdated versions for you (%s when you actually wanted %s). Fingers crossed." % (version_, version))
                            from chromedriver_py import binary_path
                            return 0

            from chromedriver_py import binary_path
        pick = input_until_ok("Would you to try to run the program anyway? (there is a chance and older driver will still work)", [['y', 'n'], ['(y)es', '(n)o']])
        if pick == "y":
            proc = Popen("pip3 install chromedriver-py", shell=True, stdout=PIPE)
            proc.wait()
            from chromedriver_py import binary_path
        elif pick == "n":
            sys.exit()

current_crome_version_str = sort_out_chrome_version()
install_correct_version_of_chromedriver(current_crome_version_str)
