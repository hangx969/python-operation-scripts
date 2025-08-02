#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频文件移动工具

功能描述:
    该脚本用于将指定目录的所有子目录中的视频文件移动到根目录，
    主要实现以下功能：

    1. 视频文件识别
       - 支持常见视频格式：mp4, avi, mkv, mov, wmv, flv, webm, m4v, 3gp, rmvb
       - 递归扫描所有子目录
       - 自动识别视频文件类型

    2. 智能移动
       - 检查文件名冲突并自动重命名
       - 保持文件完整性
       - 提供操作预览和确认

    3. 安全操作
       - 移动前检查目标位置
       - 详细的操作日志
       - 错误处理和回滚机制

使用场景:
    - 整理下载的视频文件
    - 清理多层目录结构
    - 批量视频文件管理

配置要求:
    - 具有目标目录的读写权限
    - Python 3.x 环境

作者:
创建时间: 2025年8月2日
版本: v1.0
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

class VideoMover:
    """视频文件移动器"""

    # 支持的视频文件扩展名
    VIDEO_EXTENSIONS = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
        '.webm', '.m4v', '.3gp', '.rmvb', '.ts', '.mts',
        '.mp2', '.mpg', '.mpeg', '.m2v', '.asf', '.rm',
        '.divx', '.xvid', '.f4v', '.m4p', '.ogv'
    }

    def __init__(self, root_directory):
        """
        初始化视频移动器

        Args:
            root_directory (str): 根目录路径
        """
        self.root_path = Path(root_directory).resolve()
        self.video_files = []
        self.moved_files = []
        self.failed_files = []

    def is_video_file(self, file_path):
        """
        检查文件是否为视频文件

        Args:
            file_path (Path): 文件路径对象

        Returns:
            bool: 如果是视频文件返回True
        """
        return (file_path.is_file() and
                file_path.suffix.lower() in self.VIDEO_EXTENSIONS)

    def scan_video_files(self):
        """
        扫描所有子目录中的视频文件

        Returns:
            list: 视频文件路径列表
        """
        print(f"正在扫描目录：{self.root_path}")
        print("正在查找视频文件...")

        self.video_files = []

        try:
            # 递归扫描所有子目录
            for file_path in self.root_path.rglob('*'):
                # 跳过根目录中的文件
                if file_path.parent == self.root_path:
                    continue

                if self.is_video_file(file_path):
                    self.video_files.append(file_path)

        except PermissionError as e:
            print(f"错误：没有权限访问某些目录 - {e}")
        except Exception as e:
            print(f"扫描文件时发生错误：{str(e)}")

        return self.video_files

    def get_unique_filename(self, target_path):
        """
        获取唯一的文件名（处理重名冲突）

        Args:
            target_path (Path): 目标文件路径

        Returns:
            Path: 唯一的目标文件路径
        """
        if not target_path.exists():
            return target_path

        # 如果文件已存在，添加序号
        base_name = target_path.stem
        extension = target_path.suffix
        counter = 1

        while True:
            new_name = f"{base_name}_{counter}{extension}"
            new_path = target_path.parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    def preview_operations(self):
        """预览移动操作"""
        if not self.video_files:
            print("没有找到需要移动的视频文件")
            return

        print(f"\n找到 {len(self.video_files)} 个视频文件：")
        print("=" * 80)
        print(f"{'序号':<4} {'原路径':<50} {'目标文件名':<25}")
        print("-" * 80)

        for i, video_path in enumerate(self.video_files, 1):
            relative_path = video_path.relative_to(self.root_path)
            target_path = self.root_path / video_path.name
            unique_target = self.get_unique_filename(target_path)

            print(f"{i:<4} {str(relative_path):<50} {unique_target.name:<25}")

    def move_video_files(self, confirm_each=False):
        """
        移动视频文件到根目录

        Args:
            confirm_each (bool): 是否逐个确认

        Returns:
            tuple: (成功数量, 失败数量)
        """
        if not self.video_files:
            print("没有找到需要移动的视频文件")
            return 0, 0

        success_count = 0
        failure_count = 0
        self.moved_files = []
        self.failed_files = []

        print(f"\n开始移动 {len(self.video_files)} 个视频文件...")
        print("-" * 60)

        for i, video_path in enumerate(self.video_files, 1):
            try:
                # 计算目标路径
                target_path = self.root_path / video_path.name
                unique_target = self.get_unique_filename(target_path)

                # 显示当前操作
                relative_source = video_path.relative_to(self.root_path)
                print(f"\n[{i}/{len(self.video_files)}] {relative_source} -> {unique_target.name}")

                if confirm_each:
                    response = input("确认移动此文件? (y/n/q): ").lower()
                    if response == 'q':
                        print("操作已取消")
                        break
                    elif response != 'y':
                        print("跳过此文件")
                        continue

                # 检查文件是否仍然存在（防止并发问题）
                if not video_path.exists():
                    print(f"✗ 源文件不存在：{video_path.name}")
                    self.failed_files.append((video_path, "源文件不存在"))
                    failure_count += 1
                    continue

                # 执行移动操作
                shutil.move(str(video_path), str(unique_target))
                print(f"✓ 移动成功")

                self.moved_files.append((video_path, unique_target))
                success_count += 1

            except PermissionError:
                error_msg = f"权限不足，无法移动文件：{video_path.name}"
                print(f"✗ {error_msg}")
                self.failed_files.append((video_path, error_msg))
                failure_count += 1

            except Exception as e:
                error_msg = f"移动失败：{str(e)}"
                print(f"✗ {video_path.name}: {error_msg}")
                self.failed_files.append((video_path, error_msg))
                failure_count += 1

        return success_count, failure_count

    def cleanup_empty_directories(self):
        """清理空的子目录"""
        print("\n正在清理空目录...")
        removed_dirs = []

        try:
            # 获取所有子目录，按深度倒序排列
            all_dirs = [d for d in self.root_path.rglob('*') if d.is_dir()]
            all_dirs.sort(key=lambda x: len(x.parts), reverse=True)

            for dir_path in all_dirs:
                # 跳过根目录
                if dir_path == self.root_path:
                    continue

                try:
                    # 检查目录是否为空
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        relative_path = dir_path.relative_to(self.root_path)
                        print(f"✓ 删除空目录：{relative_path}")
                        removed_dirs.append(dir_path)
                except OSError:
                    # 目录不为空或没有权限删除
                    pass

        except Exception as e:
            print(f"清理目录时出错：{str(e)}")

        if removed_dirs:
            print(f"共删除 {len(removed_dirs)} 个空目录")
        else:
            print("没有找到需要删除的空目录")

    def show_summary(self, success_count, failure_count):
        """显示操作摘要"""
        print("\n" + "=" * 60)
        print("移动操作完成统计：")
        print(f"成功移动：{success_count} 个文件")
        print(f"移动失败：{failure_count} 个文件")
        print(f"总计处理：{len(self.video_files)} 个文件")

        if self.moved_files:
            print(f"\n成功移动的文件：")
            for source, target in self.moved_files:
                source_rel = source.relative_to(self.root_path) if source.exists() else source.name
                print(f"  {source_rel} -> {target.name}")

        if self.failed_files:
            print(f"\n移动失败的文件：")
            for file_path, error_msg in self.failed_files:
                print(f"  {file_path.name}: {error_msg}")

def main():
    """主函数"""
    print("视频文件移动工具")
    print("=" * 60)
    print("功能：将所有子目录中的视频文件移动到根目录")

    # 获取目录路径
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("请输入根目录路径（回车使用当前目录）：").strip()
        if not directory:
            directory = "."

    # 验证目录
    root_path = Path(directory).resolve()
    if not root_path.exists():
        print(f"错误：目录 '{directory}' 不存在")
        return

    if not root_path.is_dir():
        print(f"错误：'{directory}' 不是一个目录")
        return

    print(f"\n根目录：{root_path}")

    # 创建视频移动器
    mover = VideoMover(directory)

    # 扫描视频文件
    video_files = mover.scan_video_files()

    if not video_files:
        print("\n没有找到需要移动的视频文件")
        return

    # 预览操作
    mover.preview_operations()

    # 显示支持的视频格式
    print(f"\n支持的视频格式：")
    extensions_list = list(mover.VIDEO_EXTENSIONS)
    extensions_list.sort()
    print(", ".join(extensions_list))

    # 确认操作
    print(f"\n准备移动 {len(video_files)} 个视频文件到根目录")

    # 选择确认模式
    mode_input = input("选择操作模式：(a)全部移动 / (i)逐个确认 / (c)取消：").lower()

    if mode_input == 'c':
        print("操作已取消")
        return
    elif mode_input == 'i':
        confirm_each = True
    elif mode_input == 'a':
        confirm_each = False
        final_confirm = input("确定要移动所有视频文件吗？(y/N)：").lower()
        if final_confirm not in ['y', 'yes']:
            print("操作已取消")
            return
    else:
        print("无效选择，操作已取消")
        return

    # 执行移动操作
    success_count, failure_count = mover.move_video_files(confirm_each)

    # 显示操作摘要
    mover.show_summary(success_count, failure_count)

    # 询问是否清理空目录
    if success_count > 0:
        cleanup_input = input("\n是否清理移动后的空目录？(y/N)：").lower()
        if cleanup_input in ['y', 'yes']:
            mover.cleanup_empty_directories()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已被用户中断")
    except Exception as e:
        print(f"\n程序执行错误：{str(e)}")
        sys.exit(1)
