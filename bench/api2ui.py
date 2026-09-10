#!/usr/bin/env python3
"""把 API 格式的工作流 JSON 转成 ComfyUI 网页可加载的 UI 格式。

用法: ComfyUI/venv/bin/python bench/api2ui.py workflows/xxx.json [输出路径]
需要 ComfyUI 正在 8188 上运行（要读 /object_info 拿节点的输入输出顺序）。
"""
import json, sys, urllib.request, os, uuid
from collections import defaultdict, deque

HOST = "http://127.0.0.1:8188"
# 这些类型是节点之间的连线，不是可填的 widget
LINK_TYPES = {"MODEL","CLIP","VAE","LATENT","IMAGE","CONDITIONING","MASK",
              "CONTROL_NET","STYLE_MODEL","CLIP_VISION","CLIP_VISION_OUTPUT",
              "GLIGEN","UPSCALE_MODEL","SIGMAS","SAMPLER","GUIDER","NOISE","AUDIO"}

def object_info():
    with urllib.request.urlopen(HOST + "/object_info") as r:
        return json.load(r)

def convert(api, oi):
    # 拓扑排序，决定绘制顺序和列位置
    deps = {nid: [v[0] for v in n.get("inputs",{}).values()
                  if isinstance(v, list) and len(v)==2 and isinstance(v[0], str)]
            for nid, n in api.items()}
    depth, seen = {}, set()
    def d(nid):
        if nid in depth: return depth[nid]
        if nid in seen: return 0          # 防环
        seen.add(nid)
        depth[nid] = 1 + max([d(p) for p in deps.get(nid,[]) if p in api] or [-1])
        return depth[nid]
    for nid in api: d(nid)

    col = defaultdict(list)
    for nid in sorted(api, key=lambda x: (depth[x], int(x) if x.isdigit() else 0)):
        col[depth[nid]].append(nid)

    nodes, links, link_id = [], [], 0
    widget_idx_map = {}
    # 先给每个节点算好在画布上的位置
    pos = {}
    for c, ids in col.items():
        for row, nid in enumerate(ids):
            pos[nid] = [c*420 + 40, row*330 + 40]

    # 输出槽：记录每个 (节点, 槽位) 产生的 link id 列表
    out_links = defaultdict(list)
    # 第一遍：建 links
    pending = []
    for nid, n in api.items():
        cls = n["class_type"]
        spec = oi.get(cls, {})
        req = spec.get("input", {}).get("required", {})
        opt = spec.get("input", {}).get("optional", {}) or {}
        order = list(req.keys()) + list(opt.keys())
        slot = 0
        for k in order:
            v = n.get("inputs", {}).get(k)
            if isinstance(v, list) and len(v)==2 and isinstance(v[0], str) and v[0] in api:
                link_id += 1
                src, src_slot = v[0], v[1]
                links.append([link_id, int(src), src_slot, int(nid), slot,
                              (req.get(k) or opt.get(k))[0] if not isinstance((req.get(k) or opt.get(k))[0], list) else "*"])
                out_links[(src, src_slot)].append(link_id)
                pending.append((nid, k, slot, link_id))
                slot += 1

    in_link = {(nid,k): lid for nid,k,_,lid in pending}
    in_slot = {(nid,k): s for nid,k,s,_ in pending}

    for nid, n in api.items():
        cls = n["class_type"]
        spec = oi.get(cls, {})
        req = spec.get("input", {}).get("required", {})
        opt = spec.get("input", {}).get("optional", {}) or {}
        inputs, widgets = [], []
        widx = {}
        for k, meta in list(req.items()) + list(opt.items()):
            t = meta[0]
            extra = meta[1] if len(meta) > 1 else {}
            is_link = (not isinstance(t, list)) and t in LINK_TYPES
            if is_link:
                inputs.append({"name": k, "type": t,
                               "link": in_link.get((nid,k)), "slot_index": in_slot.get((nid,k))})
            else:
                val = n.get("inputs", {}).get(k)
                if val is None:
                    val = extra.get("default", (t[0] if isinstance(t, list) and t else ""))
                # 下拉框(combo)和带 control_after_generate 的要登记到 widget_idx_map
                if isinstance(t, list) or (isinstance(extra, dict) and extra.get("control_after_generate")):
                    widx[k] = len(widgets)
                widgets.append(val)
                # seed 这类带 control_after_generate 的，UI 里紧跟一个控制值
                if isinstance(extra, dict) and extra.get("control_after_generate"):
                    widgets.append("fixed")
        if widx:
            widget_idx_map[str(nid)] = widx
        outs = []
        for i, (ot, oname) in enumerate(zip(spec.get("output", []), spec.get("output_name", []))):
            outs.append({"name": oname, "type": ot, "slot_index": i,
                         "links": out_links.get((nid, i)) or []})
        nodes.append({
            "id": int(nid), "type": cls, "pos": pos[nid], "size": [340, 120],
            "flags": {}, "order": depth[nid], "mode": 0,
            "inputs": inputs, "outputs": outs,
            "properties": {"Node name for S&R": cls},
            "widgets_values": widgets,
        })

    nodes.sort(key=lambda x: x["order"])
    return {"id": str(uuid.uuid4()), "revision": 0,
            "last_node_id": max(int(i) for i in api), "last_link_id": link_id,
            "nodes": nodes, "links": links, "groups": [], "config": {},
            "extra": {}, "version": 0.4, "widget_idx_map": widget_idx_map}

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".json", "_ui.json")
    api = json.load(open(src))
    out = convert(api, object_info())
    json.dump(out, open(dst, "w"), indent=1, ensure_ascii=False)
    print(f"{os.path.basename(src)} → {os.path.basename(dst)}  "
          f"({len(out['nodes'])} 节点 / {len(out['links'])} 连线)")
