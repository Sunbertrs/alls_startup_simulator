import requests
import json

def get_commit(url: str) -> dict:
    while True:
        commit = requests.get(url)
        if commit.status_code == 200:
            print(f"Get commit {url}")
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
            print(f"Downloading {url}")
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
        print("Skip program install")
        return
    else:
        tmp = []
        for i in commits:
            tmp.append(i["sha"])
            if i["sha"] == config["hash"]:
                tmp.pop()
                break

    total = len(tmp)
    while len(tmp) != 0:
        arg = [total-len(tmp)+1, total]
        display_process(*arg, f"{0:.2%}")
        commit = get_commit(f"https://api.github.com/repos/Sunbertrs/alls_startup_simulator/commits/{tmp[-1]}")
        for file in commit["files"]:
            display_process(*arg, f'{(commit["files"].index(file) / len(commit["files"])):.2%}')
            download_file(file["raw_url"])
            for p in range(int((commit["files"].index(file) / len(commit["files"]))*100), int((commit["files"].index(file)+1 / len(commit["files"])))*100):
                display_process(*arg, f'{p/100:.2%}')
        tmp.pop()
    display_process(total, total, f"{1:.2%}")
    update_hash(config["hash"], commits[0]["sha"])