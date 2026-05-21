import sys
import os

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == "exit":
            break

        elif command.startswith("echo "):
            print(command[5:])

        elif command.startswith("type "):
            arg = command[5:]
            found = False 

            if arg in ["echo","exit","type"] :
                print(f"{arg} is a shell builtin")
            else :
                for dir in os.environ["PATH"].split(os.pathsep) :
                    if os.path.isdir(dir):
                        for file in os.listdir(dir):
                            file_path = os.path.join(dir,file)
                            
                            if file == arg and os.access(file_path, os.X_OK):
                                print(f"{arg} is {file_path}")
                                found = True 
                                break
                        
                        if found :
                            break
                if not found :           
                    print(f"{arg}: not found")

        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
