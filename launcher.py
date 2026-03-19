#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
from pathlib import Path

class ProjectLauncher:
    def __init__(self):
        self.projects = [
            {
                'name': 'Project_1(Semianov)',
                'folder': 'Project_1(Semianov)',
                'description': 'Калькулятор на C',
                'file': 'main.c',  # Исходный файл
                'executable': 'calculator.exe',  # Исполняемый файл для C
                'language': 'c'
            },
            {
                'name': 'project_2(Dushanov)',
                'folder': 'project_2(Dushanov)',
                'description': 'Telegram бот на Python',
                'file': 'main.py',
                'language': 'python',
                'is_bot': True,
                'has_database': True
            },
            {
                'name': 'project_3(Kluchnicova)',
                'folder': 'project_3(Kluchnicova)',
                'description': 'Лабораторная работа на C++',
                'file': 'klyuchnikova.cpp',  # Исходный файл
                'executable': 'lab3',  # Бинарный файл для C++ (без расширения)
                'language': 'cpp'
            },
            {
                'name': 'Project_4(Chnegov)',
                'folder': 'Project_4(Chnegov)',
                'description': 'Лабораторная работа на C++',
                'file': 'chnegov.cpp',  # Исходный файл
                'executable': 'lab4',  # Бинарный файл для C++ (без расширения)
                'language': 'cpp'
            }
        ]
        
        self.is_windows = platform.system() == 'Windows'
        self.base_dir = Path(__file__).parent.absolute()

    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if self.is_windows else 'clear')

    def print_colored(self, text, color_code):
        """Вывод цветного текста"""
        colors = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'reset': '\033[0m'
        }
        if self.is_windows:
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                print(f"{colors.get(color_code, '')}{text}{colors['reset']}")
            except:
                print(text)
        else:
            print(f"{colors.get(color_code, '')}{text}{colors['reset']}")

    def print_header(self):
        """Вывод заголовка"""
        print("╔════════════════════════════════════════╗")
        print("║         ВЫБОР ПРОЕКТА ДЛЯ ЗАПУСКА      ║")
        print("╚════════════════════════════════════════╝")
        print()

    def print_projects(self):
        """Вывод списка проектов с информацией о наличии исполняемых файлов"""
        for i, project in enumerate(self.projects, 1):
            if project['language'] == 'c':
                # Для C проверяем наличие exe файла
                status = "✓" if self.check_executable_exists(i-1) else "✗"
                file_type = "exe"
            elif project['language'] == 'cpp':
                # Для C++ проверяем наличие бинарного файла
                status = "✓" if self.check_executable_exists(i-1) else "✗"
                file_type = "bin"
            else:
                # Для Python проверяем наличие исходного файла
                status = "✓" if self.check_project_exists(i-1) else "✗"
                file_type = "py"
            
            status_color = 'green' if status == "✓" else 'red'
            
            print(f"{i}. {project['name']} - {project['description']}")
            self.print_colored(f"   [{status}] Файл {file_type} {status_color == 'green' and 'найден' or 'не найден'}", status_color)
            print()

        print("0. Выход")
        print("────────────────────────────────────────")
        print()

    def check_project_exists(self, index):
        """Проверка существования Python проекта"""
        project = self.projects[index]
        project_path = self.base_dir / project['folder']
        file_path = project_path / project['file']
        
        return project_path.exists() and file_path.exists()

    def check_executable_exists(self, index):
        """Проверка существования исполняемого файла для C/C++ проекта"""
        project = self.projects[index]
        project_path = self.base_dir / project['folder']
        
        if 'executable' not in project:
            return False
            
        exe_path = project_path / project['executable']
        
        # Для Windows проверяем наличие .exe для C и бинарник без расширения для C++
        if self.is_windows and project['language'] == 'c':
            # Для C на Windows добавляем .exe если его нет
            if not str(exe_path).endswith('.exe'):
                exe_path = Path(str(exe_path) + '.exe')
        
        return project_path.exists() and exe_path.exists()

    def run_python(self, project_path, file_name, is_bot=False):
        """Запуск Python проекта"""
        self.print_colored(f"\n[Python] Запуск {file_name}...", 'cyan')
        
        try:
            os.chdir(project_path)
            
            if is_bot and os.path.exists('run.py'):
                self.print_colored("Запуск через run.py...", 'yellow')
                subprocess.run([sys.executable, 'run.py'], check=True)
            else:
                subprocess.run([sys.executable, file_name], check=True)
                
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Ошибка при выполнении Python скрипта: {e}", 'red')
        except KeyboardInterrupt:
            self.print_colored("\n\nПрограмма остановлена пользователем", 'yellow')
        except Exception as e:
            self.print_colored(f"Ошибка: {e}", 'red')
        finally:
            os.chdir(self.base_dir)

    def run_executable(self, project_path, exe_name, language):
        """Запуск исполняемого файла"""
        file_type = "EXE" if language == 'c' else "бинарный"
        self.print_colored(f"\n[Запуск] {file_type} файл: {exe_name}", 'cyan')
        
        try:
            os.chdir(project_path)
            
            # Определяем полный путь к файлу
            if self.is_windows and language == 'c' and not exe_name.endswith('.exe'):
                # Для C на Windows добавляем .exe
                full_path = exe_name + '.exe'
            else:
                full_path = exe_name
            
            # Проверяем существование файла
            if not os.path.exists(full_path):
                self.print_colored(f"Ошибка: Файл {full_path} не найден!", 'red')
                return
            
            self.print_colored("Запуск программы...", 'green')
            print("-" * 50)
            
            # Запускаем файл
            if self.is_windows:
                if language == 'c':
                    # Для C на Windows запускаем .exe
                    subprocess.run(full_path, shell=True)
                else:
                    # Для C++ бинарников на Windows
                    if os.name == 'nt':  # Windows
                        subprocess.run(full_path, shell=True)
                    else:  # Если это не Windows, но пытаемся запустить бинарник
                        subprocess.run(['./' + full_path])
            else:
                # Для Linux/Mac
                subprocess.run(['./' + full_path])
            
            print("-" * 50)
            self.print_colored("Программа завершена", 'yellow')
                
        except FileNotFoundError:
            self.print_colored(f"Ошибка: Не удалось найти или запустить {full_path}", 'red')
        except KeyboardInterrupt:
            self.print_colored("\n\nПрограмма остановлена пользователем", 'yellow')
        except Exception as e:
            self.print_colored(f"Ошибка при запуске: {e}", 'red')
        finally:
            os.chdir(self.base_dir)

    def run_project(self, choice):
        """Запуск выбранного проекта"""
        project = self.projects[choice - 1]
        project_path = self.base_dir / project['folder']
        
        self.print_colored(f"\nЗапуск: {project['name']} - {project['description']}", 'blue')
        self.print_colored("=" * 50, 'blue')
        
        if project['language'] == 'python':
            if not self.check_project_exists(choice - 1):
                self.print_colored(f"\nОшибка: Файл {project['file']} не найден!", 'red')
                return False
            self.run_python(project_path, project['file'], project.get('is_bot', False))
        
        elif project['language'] in ['c', 'cpp']:
            if 'executable' not in project:
                self.print_colored(f"\nОшибка: Не указан исполняемый файл для проекта!", 'red')
                return False
            
            if not self.check_executable_exists(choice - 1):
                exe_name = project['executable']
                if self.is_windows and project['language'] == 'c' and not exe_name.endswith('.exe'):
                    exe_name += '.exe'
                self.print_colored(f"\nОшибка: Исполняемый файл {exe_name} не найден!", 'red')
                self.print_colored(f"Путь: {project_path / exe_name}", 'yellow')
                return False
            
            self.run_executable(project_path, project['executable'], project['language'])
        
        return True

    def check_all_projects(self):
        """Проверка всех проектов перед запуском"""
        self.print_colored("\n🔍 Проверка проектов...", 'cyan')
        
        missing_python = []
        missing_c = []
        missing_cpp = []
        
        for i, project in enumerate(self.projects):
            if project['language'] == 'python':
                if not self.check_project_exists(i):
                    missing_python.append(f"{i+1}. {project['name']} - {project['file']}")
            elif project['language'] == 'c':
                if not self.check_executable_exists(i):
                    exe_name = project.get('executable', 'не указан')
                    if self.is_windows and not exe_name.endswith('.exe'):
                        exe_name += '.exe'
                    missing_c.append(f"{i+1}. {project['name']} - {exe_name}")
            elif project['language'] == 'cpp':
                if not self.check_executable_exists(i):
                    missing_cpp.append(f"{i+1}. {project['name']} - {project.get('executable', 'не указан')} (бинарный файл)")
        
        if missing_python:
            self.print_colored("\n⚠️  Отсутствуют Python файлы:", 'yellow')
            for m in missing_python:
                self.print_colored(f"   {m}", 'yellow')
        
        if missing_c:
            self.print_colored("\n⚠️  Отсутствуют C (EXE) файлы:", 'yellow')
            for m in missing_c:
                self.print_colored(f"   {m}", 'yellow')
        
        if missing_cpp:
            self.print_colored("\n⚠️  Отсутствуют C++ бинарные файлы:", 'yellow')
            for m in missing_cpp:
                self.print_colored(f"   {m}", 'yellow')
        
        if not missing_python and not missing_c and not missing_cpp:
            self.print_colored("\n✅ Все проекты готовы к запуску!", 'green')
        
        print()
        input("Нажмите Enter для продолжения...")

    def suggest_compilation(self):
        """Предложение скомпилировать проекты при отсутствии исполняемых файлов"""
        need_compilation_c = []
        need_compilation_cpp = []
        
        for i, project in enumerate(self.projects):
            if project['language'] == 'c':
                if not self.check_executable_exists(i) and self.check_project_exists(i):
                    need_compilation_c.append({
                        'name': project['name'],
                        'file': project['file'],
                        'output': project.get('executable', 'program')
                    })
            elif project['language'] == 'cpp':
                if not self.check_executable_exists(i) and self.check_project_exists(i):
                    need_compilation_cpp.append({
                        'name': project['name'],
                        'file': project['file'],
                        'output': project.get('executable', 'program')
                    })
        
        if need_compilation_c:
            self.print_colored("\n🔧 Найдены исходные файлы C без EXE:", 'yellow')
            for proj in need_compilation_c:
                self.print_colored(f"   {proj['name']} - {proj['file']}", 'yellow')
            
            print("\nДля компиляции C выполните команды:")
            for proj in need_compilation_c:
                output = proj['output']
                if self.is_windows and not output.endswith('.exe'):
                    output += '.exe'
                print(f"   gcc {proj['file']} -o {output}")
        
        if need_compilation_cpp:
            self.print_colored("\n🔧 Найдены исходные файлы C++ без бинарников:", 'yellow')
            for proj in need_compilation_cpp:
                self.print_colored(f"   {proj['name']} - {proj['file']}", 'yellow')
            
            print("\nДля компиляции C++ выполните команды:")
            for proj in need_compilation_cpp:
                print(f"   g++ {proj['file']} -o {proj['output']} -std=c++11")
            
            print("\nПримечание: Для Windows добавьте .exe к имени выходного файла")
        
        if need_compilation_c or need_compilation_cpp:
            print()

    def run(self):
        """Основной цикл программы"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_projects()
            
            # Проверяем наличие исходных файлов без исполняемых
            self.suggest_compilation()
            
            try:
                choice = input("Выберите проект (0-4, 'c' - проверка): ").strip().lower()
                
                if choice == '0':
                    self.print_colored("\nВыход...", 'yellow')
                    break
                elif choice == 'c':
                    self.check_all_projects()
                    continue
                
                choice = int(choice)
                if 1 <= choice <= 4:
                    self.run_project(choice)
                    input("\nНажмите Enter для продолжения...")
                else:
                    self.print_colored("\nНеверный выбор. Пожалуйста, выберите 0-4.", 'red')
                    input("Нажмите Enter для продолжения...")
                    
            except ValueError:
                self.print_colored("\nПожалуйста, введите число.", 'red')
                input("Нажмите Enter для продолжения...")
            except KeyboardInterrupt:
                self.print_colored("\n\nВыход...", 'yellow')
                break

if __name__ == "__main__":
    launcher = ProjectLauncher()
    launcher.run()
