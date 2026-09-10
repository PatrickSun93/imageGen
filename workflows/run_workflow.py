#!/usr/bin/env python3
"""通过 ComfyUI 的 /prompt API 提交一个工作流 JSON，等待完成并打印耗时和输出文件。

用法: ComfyUI/venv/bin/python workflows/run_workflow.py workflows/pony_v6_xl.json [--seed N]
"""
import json, sys, time, urllib.request, urllib.error, uuid, argparse

HOST = "http://127.0.0.1:8188"

def post(path, payload):
    req = urllib.request.Request(HOST + path,
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def get(path):
    with urllib.request.urlopen(HOST + path) as r:
        return json.load(r)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()

    wf = json.load(open(a.workflow))
    if a.seed is not None:
        for node in wf.values():
            if "seed" in node.get("inputs", {}):
                node["inputs"]["seed"] = a.seed

    client_id = str(uuid.uuid4())
    t0 = time.time()
    try:
        res = post("/prompt", {"prompt": wf, "client_id": client_id})
    except urllib.error.HTTPError as e:
        print("提交失败:", e.code)
        print(e.read().decode()[:4000])
        sys.exit(1)
    pid = res["prompt_id"]
    print(f"已提交 {a.workflow}  prompt_id={pid}")

    while True:
        if time.time() - t0 > a.timeout:
            print("超时"); sys.exit(1)
        h = get(f"/history/{pid}")
        if pid in h:
            entry = h[pid]
            elapsed = time.time() - t0
            status = entry.get("status", {})
            if status.get("status_str") == "error" or not status.get("completed", True):
                print(f"执行失败 ({elapsed:.1f}s):")
                for m in status.get("messages", []):
                    print("  ", json.dumps(m, ensure_ascii=False)[:2000])
                sys.exit(1)
            files = [f"{i['subfolder'] + '/' if i['subfolder'] else ''}{i['filename']}"
                     for o in entry.get("outputs", {}).values() for i in o.get("images", [])]
            print(f"完成，耗时 {elapsed:.1f} 秒  输出: {', '.join(files) or '(无)'}")
            print(f"ELAPSED={elapsed:.3f}")
            return
        time.sleep(2)

if __name__ == "__main__":
    main()
