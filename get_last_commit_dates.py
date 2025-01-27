# old.py
import sys
import csv

def get_last_modified_dates(log_file, target_files):
    last_modified_dates = {}
    commit_date = None

    # 初始化 last_modified_dates
    for file_name in target_files:
        last_modified_dates[file_name] = None  # 初始化为 None

    with open(log_file, 'r', encoding='UTF8') as f:
        for line in f:
            line = line.strip()
            if not line:  # 如果是空行，跳过
                continue
            if len(line) == 40 and all(c in '0123456789abcdef' for c in line):  # 检查是否是提交哈希
                continue
            if len(line) == 10 and line.count('-') == 2:  # 检查是否是日期
                commit_date = line
            else:  # 否则，认为是文件名
                if line in last_modified_dates and last_modified_dates[line] is None:  # 只更新目标文件的日期
                    last_modified_dates[line] = commit_date

    return last_modified_dates

def read_target_files(target_files_path):
    with open(target_files_path, 'r', encoding='UTF8') as tf:
        return [line.strip() for line in tf if line.strip()]  # 读取并去除空行

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python script.py <log_file> <output_file> <target_files>")
        sys.exit(1)

    log_file = sys.argv[1]
    output_file = sys.argv[2]
    target_files_path = sys.argv[3]
    
    # 读取目标文件列表
    target_files = read_target_files(target_files_path)
    
    last_modified_dates = get_last_modified_dates(log_file, target_files)

    # 按照日期升序排列
    sorted_dates = sorted(last_modified_dates.items(), key=lambda item: item[1])

    # 使用csv库写入文件
    with open(output_file, 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(["File", "Last Modified Date"])  # 写入表头
        for file_name, last_modified_date in sorted_dates:
            writer.writerow([file_name, last_modified_date])  # 写入数据行

    print(f"Output written to: {output_file}")
    