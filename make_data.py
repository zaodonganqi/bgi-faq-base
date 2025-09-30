#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

# ==================== 配置 ====================
FIELDS = ["id", "question", "type", "answer"]  # 数据结构
INPUT_FILE = "test.txt"                        # 原始数据来源
OUTPUT_FILE = "result.json"                    # 输出 JSON 文件

# ==================== 读取 test.txt 并解析 ====================
def parse_input_file(file_path):
    """读取随性文本，解析为标准数据结构"""
    if not os.path.exists(file_path):
        print(f"❌ 输入文件不存在: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]

    records = []
    buffer = []

    # 按至少 2 行空行作为分隔
    for line in lines + ["", ""]:
        if line.strip() == "":
            if len(buffer) >= 3:  # 确保有 id, type, answer
                try:
                    # 倒数第二行是 type
                    record_type = buffer[-2].strip()
                    # 最后一行是 answer
                    record_answer = buffer[-1].strip()
                    # 第一行是 id
                    record_id = int(buffer[0].strip())
                    # 中间是 question
                    record_question = [q.strip() for q in buffer[1:-2] if q.strip()]
                    records.append({
                        "id": record_id,
                        "question": record_question,
                        "type": record_type,
                        "answer": record_answer
                    })
                except Exception as e:
                    print(f"⚠️ 解析数据失败: {buffer} | 错误: {e}")
            buffer = []
        else:
            buffer.append(line)

    return records

# ==================== 读取已有 result.json ====================
def load_existing_json(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 读取 JSON 文件失败: {e}")
        return []

# ==================== 排序函数 ====================
def sort_records(records):
    """先按 type 排序，再按 id 排序，相同 id 按 question[0] 排序"""
    id_map = {}
    for rec in records:
        if rec["id"] in id_map:
            print(f"⚠️ 出现相同 id {rec['id']}，将根据第一条 question 排序")
        id_map[rec["id"]] = True

    return sorted(
        records,
        key=lambda r: (r["type"], r["id"], r["question"][0] if r["question"] else "")
    )

# ==================== 写入 result.json ====================
def save_json(file_path, records):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存 {len(records)} 条记录到 {file_path}")
    except Exception as e:
        print(f"❌ 保存 JSON 文件失败: {e}")

# ==================== 清空输入文件 ====================
def clear_input_file(file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            pass
        print(f"✅ 已清空输入文件: {file_path}")
    except Exception as e:
        print(f"❌ 清空文件失败: {e}")

# ==================== 主流程 ====================
def main():
    new_records = parse_input_file(INPUT_FILE)
    if not new_records:
        print("⚠️ 没有新的数据，退出")
        return

    existing_records = load_existing_json(OUTPUT_FILE)
    all_records = existing_records + new_records
    all_records = sort_records(all_records)
    save_json(OUTPUT_FILE, all_records)
    clear_input_file(INPUT_FILE)

if __name__ == "__main__":
    main()
