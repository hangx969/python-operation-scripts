#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件扩展名批量添加工具

功能描述:
    该脚本用于扫描指定目录，找出所有没有扩展名的文件，
    并为它们自动添加 .zip 扩展名。主要实现以下功能：

    1. 文件扫描
       - 扫描指定目录中的所有文件
       - 识别没有扩展名的常规文件
       - 排除目录和隐藏文件

    2. 安全重命名
       - 检查目标文件名是否已存在
       - 提供重命名预览功能
       - 支持批量确认或逐个确认模式

    3. 日志记录
       - 记录重命名操作的详细信息
       - 提供操作统计和错误报告

使用场景:
    - 批量处理下载的压缩文件
    - 整理文件命名规范
    - 自动化文件类型标识

配置要求:
    - 具有目标目录的读写权限
    - Python 3.x 环境

作者:
创建时间: 2025年8月2日
版本: v1.0
"""

import os
import sys
from pathlib import Path

def is_file_without_extension(file_path):
    """
    检查文件是否没有扩展名

    Args:
        file_path (Path): 文件路径对象

    Returns:
        bool: 如果文件没有扩展名返回True，否则返回False
    """
    # 检查是否为常规文件
    if not file_path.is_file():
        return False

    # 检查文件名是否有扩展名
    if file_path.suffix == '':
        return True

    return False

def scan_files_without_extension(directory):
    """
    扫描目录中没有扩展名的文件

    Args:
        directory (str): 要扫描的目录路径

    Returns:
        list: 没有扩展名的文件路径列表
    """
    directory_path = Path(directory)

    if not directory_path.exists():
        print(f"错误：目录 '{directory}' 不存在")
        return []

    if not directory_path.is_dir():
        print(f"错误：'{directory}' 不是一个目录")
        return []

    files_without_extension = []

    try:
        # 只扫描当前目录
        files = directory_path.iterdir()

        for file_path in files:
            if is_file_without_extension(file_path):
                # 排除隐藏文件（以.开头的文件）
                if not file_path.name.startswith('.'):
                    files_without_extension.append(file_path)

    except PermissionError:
        print(f"错误：没有权限访问目录 '{directory}'")
        return []
    except Exception as e:
        print(f"扫描目录时发生错误：{str(e)}")
        return []

    return files_without_extension

def preview_rename_operations(files_list):
    """
    预览重命名操作

    Args:
        files_list (list): 文件路径列表
    """
    if not files_list:
        print("没有找到需要重命名的文件")
        return

    print(f"\n找到 {len(files_list)} 个没有扩展名的文件：")
    print("=" * 60)
    print(f"{'序号':<4} {'原文件名':<30} {'新文件名':<30}")
    print("-" * 60)

    for i, file_path in enumerate(files_list, 1):
        original_name = file_path.name
        new_name = original_name + ".zip"
        print(f"{i:<4} {original_name:<30} {new_name:<30}")

def check_conflicts(files_list):
    """
    检查重命名冲突

    Args:
        files_list (list): 文件路径列表

    Returns:
        list: 有冲突的文件列表
    """
    conflicts = []

    for file_path in files_list:
        new_file_path = file_path.with_suffix('.zip')
        if new_file_path.exists():
            conflicts.append((file_path, new_file_path))

    return conflicts

def rename_files(files_list, confirm_each=False):
    """
    批量重命名文件

    Args:
        files_list (list): 文件路径列表
        confirm_each (bool): 是否逐个确认

    Returns:
        tuple: (成功数量, 失败数量, 错误列表)
    """
    success_count = 0
    failure_count = 0
    errors = []

    for i, file_path in enumerate(files_list, 1):
        original_name = file_path.name
        new_file_path = file_path.with_suffix('.zip')

        if confirm_each:
            response = input(f"\n[{i}/{len(files_list)}] 重命名 '{original_name}' -> '{new_file_path.name}'? (y/n/q): ").lower()
            if response == 'q':
                print("操作已取消")
                break
            elif response != 'y':
                print("跳过此文件")
                continue

        try:
            # 检查目标文件是否已存在
            if new_file_path.exists():
                error_msg = f"目标文件已存在：{new_file_path.name}"
                print(f"跳过：{error_msg}")
                errors.append((file_path, error_msg))
                failure_count += 1
                continue

            # 执行重命名
            file_path.rename(new_file_path)
            print(f"✓ 重命名成功：{original_name} -> {new_file_path.name}")
            success_count += 1

        except PermissionError:
            error_msg = f"权限不足，无法重命名文件：{original_name}"
            print(f"✗ {error_msg}")
            errors.append((file_path, error_msg))
            failure_count += 1

        except Exception as e:
            error_msg = f"重命名失败：{str(e)}"
            print(f"✗ {original_name}: {error_msg}")
            errors.append((file_path, error_msg))
            failure_count += 1

    return success_count, failure_count, errors

def main():
    """主函数"""
    print("文件扩展名批量添加工具")
    print("=" * 50)

    # 获取目录路径
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("请输入目录路径（回车使用当前目录）：").strip()
        if not directory:
            directory = "."

    # 扫描文件
    print(f"\n正在扫描目录：{os.path.abspath(directory)}")
    print("模式：仅当前目录")

    files_without_extension = scan_files_without_extension(directory)

    if not files_without_extension:
        print("\n没有找到需要处理的文件")
        return

    # 预览操作
    preview_rename_operations(files_without_extension)

    # 检查冲突
    conflicts = check_conflicts(files_without_extension)
    if conflicts:
        print(f"\n警告：发现 {len(conflicts)} 个文件名冲突：")
        for original, conflict in conflicts:
            print(f"  {original.name} -> {conflict.name} (已存在)")
        print("这些文件将被跳过")

    # 确认操作
    print(f"\n准备为 {len(files_without_extension)} 个文件添加 .zip 扩展名")

    # 选择确认模式
    mode_input = input("选择确认模式：(a)全部确认 / (i)逐个确认 / (c)取消：").lower()

    if mode_input == 'c':
        print("操作已取消")
        return
    elif mode_input == 'i':
        confirm_each = True
    elif mode_input == 'a':
        confirm_each = False
        final_confirm = input("确定要批量重命名所有文件吗？(y/N)：").lower()
        if final_confirm not in ['y', 'yes']:
            print("操作已取消")
            return
    else:
        print("无效选择，操作已取消")
        return

    # 执行重命名
    print("\n开始重命名操作...")
    print("-" * 40)

    success_count, failure_count, errors = rename_files(files_without_extension, confirm_each)

    # 输出统计结果
    print("\n" + "=" * 40)
    print("操作完成统计：")
    print(f"成功：{success_count} 个文件")
    print(f"失败：{failure_count} 个文件")
    print(f"总计：{len(files_without_extension)} 个文件")

    if errors:
        print(f"\n失败详情：")
        for file_path, error_msg in errors:
            print(f"  {file_path.name}: {error_msg}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已被用户中断")
    except Exception as e:
        print(f"\n程序执行错误：{str(e)}")
        sys.exit(1)
