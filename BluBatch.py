# import subprocess

# def create_batch_files(commands_to_run=[]):
#     number_of_batches = len(commands_to_run)

#     fileList = []

#     for n, command in enumerate(commands_to_run):
#     	fileList.append(f"batch_{n}.py")
#         with open(f"batch_{n}.py", "w") as batch_file:
#             code = f'import subprocess\nsubprocess.run(r"{command}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)'
#             batch_file.write(code)

    

# # Example usage with a list of commands
# # commands = [
# #     'your_command_1',
# #     'your_command_2',
# #     'your_command_3'
# # ]

# # create_batch_files(commands)

import subprocess
import multiprocessing

def run_command(command):
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

def create_batch_files(commands_to_run=[]):
    with multiprocessing.Pool() as pool:
        pool.map(run_command, commands_to_run)

# def function():
#     pass

# Example usage with a list of commands
commands = [
    'your_command_1',
    'your_command_2',
    'your_command_3'
]

# if __name__ == "__main__":
#     create_batch_files(commands)


# import subprocess


# def createJobs(app_to_run=[]):
#     number_of_batches = len(app_to_run)
#     batches = []

#     # Create batches by distributing apps evenly across files
#     for n in range(number_of_batches):
#         batches.append([])
#         for i in range(len(app_to_run)):
#             batches[n].append(app_to_run[i])

#     # Generate batch scripts
#     for n, batch in enumerate(batches):
#         with open(f"_batch-{n}.py", "w") as _b:
#             commands = []
#             for app in batch:
#                 commands.append(f'subprocess.run("{app}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)')

#             _b.write("\n".join(commands))


# createJobs(['C:/Program Files (x86)/PPSSPP/PPSSPPWindows.exe', 'C:/Program Files (x86)/PPSSPP/PPSSPPWindows64.exe', 'C:/Program Files (x86)/PPSSPP/unins000.exe'])
