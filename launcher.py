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
                'executable': 'bez.exe',  # Исполняемый файл
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
                'file': 'main.cpp',  # Исходный файл
                'executable': 'bez_pol.exe',  # Исполняемый файл
                'language': 'cpp'
            },
            {
                'name': 'Project_4(Chnegov)',
                'folder': 'Project_4(Chnegov)',
                'description': 'Лабораторная работа на C++',
                'file': 'Chnegov.cpp',  # Исходный файл
                'executable': 'Chnegov.exe',  # Исполняемый файл
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
        """Вывод списка проектов с информацией о наличии exe файлов"""
        for i, project in enumerate(self.projects, 1):
            if project['language'] in ['c', 'cpp']:
                # Для C/C++ проверяем наличие exe файла
                status = "✓" if self.check_executable_exists(i-1) else "✗"
                file_type = "exe"
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
        """Проверка существования exe файла для C/C++ проекта"""
        project = self.projects[index]
        project_path = self.base_dir / project['folder']
        
        if 'executable' not in project:
            return False
            
        exe_path = project_path / project['executable']
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

    def run_executable(self, project_path, exe_name):
        """Запуск exe файла"""
        self.print_colored(f"\n[Запуск] Исполняемый файл: {exe_name}", 'cyan')
        
        try:
            os.chdir(project_path)
            
            # Проверяем существование файла
            if not os.path.exists(exe_name):
                self.print_colored(f"Ошибка: Файл {exe_name} не найден!", 'red')
                return
            
            self.print_colored("Запуск программы...", 'green')
            print("-" * 50)
            
            # Запускаем exe файл
            if self.is_windows:
                # Для Windows используем shell=True для корректного запуска .exe
                subprocess.run(exe_name, shell=True)
            else:
                # Для Linux/Mac (если есть wine или нативные бинарники)
                subprocess.run(['./' + exe_name] if not self.is_windows else [exe_name])
            
            print("-" * 50)
            self.print_colored("Программа завершена", 'yellow')
                
        except FileNotFoundError:
            self.print_colored(f"Ошибка: Не удалось найти или запустить {exe_name}", 'red')
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
                self.print_colored(f"\nОшибка: Исполняемый файл {project['executable']} не найден!", 'red')
                self.print_colored(f"Путь: {project_path / project['executable']}", 'yellow')
                return False
            
            self.run_executable(project_path, project['executable'])
        
        return True

    def check_all_projects(self):
        """Проверка всех проектов перед запуском"""
        self.print_colored("\n🔍 Проверка проектов...", 'cyan')
        
        missing_python = []
        missing_exe = []
        
        for i, project in enumerate(self.projects):
            if project['language'] == 'python':
                if not self.check_project_exists(i):
                    missing_python.append(f"{i+1}. {project['name']} - {project['file']}")
            else:
                if not self.check_executable_exists(i):
                    missing_exe.append(f"{i+1}. {project['name']} - {project.get('executable', 'не указан')}")
        
        if missing_python:
            self.print_colored("\n⚠️  Отсутствуют Python файлы:", 'yellow')
            for m in missing_python:
                self.print_colored(f"   {m}", 'yellow')
        
        if missing_exe:
            self.print_colored("\n⚠️  Отсутствуют исполняемые файлы:", 'yellow')
            for m in missing_exe:
                self.print_colored(f"   {m}", 'yellow')
        
        if not missing_python and not missing_exe:
            self.print_colored("\n✅ Все проекты готовы к запуску!", 'green')
        
        print()  # Пустая строка для отступа
        input("Нажмите Enter для продолжения...")

    def suggest_compilation(self):
        """Предложение скомпилировать проекты при отсутствии exe файлов"""
        need_compilation = []
        
        for i, project in enumerate(self.projects):
            if project['language'] in ['c', 'cpp']:
                if not self.check_executable_exists(i) and self.check_project_exists(i):
                    need_compilation.append({
                        'index': i,
                        'name': project['name'],
                        'file': project['file'],
                        'language': project['language']
                    })
        
        if need_compilation:
            self.print_colored("\n🔧 Найдены исходные файлы без исполняемых:", 'yellow')
            for proj in need_compilation:
                self.print_colored(f"   {proj['name']} - {proj['file']}", 'yellow')
            
            print("\nДля компиляции выполните команды:")
            for proj in need_compilation:
                if proj['language'] == 'c':
                    print(f"   gcc {proj['file']} -o calculator.exe")
                else:
                    print(f"   g++ {proj['file']} -o lab{proj['index']+1}.exe -std=c++11")
            
            print()  # Пустая строка

    def run(self):
        """Основной цикл программы"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_projects()
            
            # Проверяем наличие исходных файлов без exe
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
