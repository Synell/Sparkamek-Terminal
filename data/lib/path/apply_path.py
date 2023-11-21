#----------------------------------------------------------------------

    # Libraries
import os, subprocess
from ..PlatformType import PlatformType
from ..main_functions import format_msg
from ..LogType import LogType
from ..GlobalValues import GlobalValues
from ..main_functions import press_any_key, clear
#----------------------------------------------------------------------

    # Function
def apply_path(path_values: list[str], cwd: str) -> None:
    match GlobalValues.platform:
        case PlatformType.Windows:
            filename = f'{cwd}\\file.reg'

            path_values.append(cwd)
            path_values = [p.replace('\\\\', '\\').replace('\\', '\\\\') for p in path_values]

            with open(filename, 'w', encoding = 'utf-8') as f:
                f.write('Windows Registry Editor Version 5.00\n\n')
                f.write('[HKEY_CURRENT_USER\\Environment]\n')
                f.write('"Path"="' + ';'.join(path_values) + '"\n')

            process = subprocess.Popen(['regedit', '/s', filename], stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            stdout, stderr = process.communicate()

            if os.path.exists(filename):
                os.remove(filename)

            if stderr:
                try: stderr = stderr.decode('utf-8')
                except: stderr = stderr.decode('windows-1250') # Even though it's not the correct encoding, it's better than nothing

                print(format_msg(f'Unable to add to path: {stderr}', LogType.Error))

            else: print(format_msg('Done!', LogType.Success))

        case _:
            print(format_msg('This feature is not available on this platform.', LogType.Error))

    press_any_key()
    clear()
#----------------------------------------------------------------------