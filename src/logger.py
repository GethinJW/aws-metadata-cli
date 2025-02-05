from termcolor import colored

def log(msg: str, logType="INFO") -> None:
    match logType:
        case "WARNING":
            prefix = colored("WARNING: ", "yellow")
        case _, "INFO":
            prefix = colored("INFO: ", "white")
    print(prefix, msg)
