import traceback
import time

def ErrorLog(error: str):
    cur_time = time.strftime("%Y-%m-%d / %H:%M:%S", time.localtime(time.time()))
    new_log_entry = f"{cur_time} - {error}\n\n"

    # Read the existing content of the file
    try:
        with open("Error_report.txt", "r") as file:
            existing_content = file.read()
    except FileNotFoundError:
        existing_content = ""

    # Write the new log followed by the old content
    with open("Error_report.txt", "w") as file:
        file.write(new_log_entry + existing_content)


try:
    print("Start")
    a = 4/0
    print(a)

except Exception:
    print("Error occurs! Check out the Log")
    err = traceback.format_exc()
    ErrorLog(str(err))

