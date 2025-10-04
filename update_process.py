import requests
import json

def get_commit(url: str) -> dict:
    while True:
        commit = requests.get(url)
        if commit.status_code == 200:
            print(f"get commit {url}")
            break
    return commit.json()

def get_file_name(url: str) -> str:
    url = url.replace("https://", "")
    url = url.split("/")
    return url[-1]

def download_file(url: str) -> None:
    retry_timeout = 3
    for _ in range(retry_timeout):
        file = requests.get(url)
        if file.status_code == 200:
            print(f"dl file {url}")
            file_name = get_file_name(url)
            open(file_name, "wb").write(file.content)
            break

def update_hash(old_hash: str, new_hash: str) -> None:
    with open("config.json", "r", encoding="utf-8") as f:
        content = f.readlines()

    for i, l in enumerate(content):
        if old_hash in l:
            content[i] = l.replace(old_hash, new_hash)

    with open("config.json", "w", encoding="utf-8") as f:
        f.writelines(content)

def process(display_process):
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    commits = get_commit("https://api.github.com/repos/Sunbertrs/alls_startup_simulator/commits")

    if config["hash"] == commits[0]["sha"]:
        print("No need to")
        return
    else:
        tmp = []
        for i in commits:
            tmp.append(i["sha"])
            if i["sha"] == config["hash"]:
                tmp.pop()
                break

    while len(tmp) != 0:
        arg = [len(tmp)-tmp.index(tmp[-1]), len(tmp), "0.00%"]
        display_process(*arg)
        commit = get_commit(f"https://api.github.com/repos/Sunbertrs/alls_startup_simulator/commits/{tmp[-1]}")
        for file in commit["files"]:
            arg[2] = f'{(commit["files"].index(file)+1 / len(commit["files"])):.2%}'
            display_process(*arg)
            download_file(file["raw_url"])
        tmp.pop()

    update_hash(config["hash"], commits[0]["sha"])