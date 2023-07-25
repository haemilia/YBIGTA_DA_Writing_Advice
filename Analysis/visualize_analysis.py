import json


def main():
    path = input("Please enter the path to analysis result json file")  
    with open(path) as json_file:
        results = json.load(json_file)

if __name__ == "__main__":
    main()