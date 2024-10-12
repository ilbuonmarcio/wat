import subprocess

COMMANDS = {
    'core_temps': "sensors | grep 'Core' | awk '{print $3}' | sed -e 's/+//g' | sed -e 's/°C//g' | xargs | sed -e 's/ /,/g'",
    'cpu_temp': "sensors | grep 'CPU:' | grep '+' | awk '{print $2}' | sed -e 's/+//g' | sed -e 's/°C//g'"
}

def execute_command(command):
    if command not in COMMANDS.keys():
        raise Exception(f"'{command}' is not a valid executable command")

    try:
        result = subprocess.check_output(COMMANDS[command], shell=True, text=True)
        return result
    except Exception as e:
        raise e
