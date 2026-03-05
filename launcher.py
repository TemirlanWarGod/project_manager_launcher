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
                'folder': 'Project_1(Semianov)',  # Явно указываем имя папки
                'description': 'Калькулятор на C',
                'file': 'main.c',
                'language': 'c'
            },
            {
                'name': 'project_2(Dushanov)',
                'folder': 'project_2(Dushanov)',  # Явно указываем имя папки
                'description': 'Telegram бот на Python',
                'file': 'main.py',  # Изменено с run.py на main.py
                'language': 'python',
                'is_bot': True,
                'has_database': True  # Флаг наличия базы данных
            },
            {
                'name': 'project_3(Kluchnicova)',
                'folder': 'project_3(Kluchnicova)',  # Явно указываем имя папки
                'description': 'Лабораторная работа на C++',
                'file': 'klyuchnikova.cpp',
                'language': 'cpp'
            },
            {
                'name': 'Project_4(Chnegov)',
                'folder': 'Project_4(Chnegov)',  # Явно указываем имя папки
                'description': 'Лабораторная работа на C++',
                'file': 'chnegov.cpp',
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
            # Для Windows пытаемся использовать цветной вывод
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
        """Вывод списка проектов"""
        for i, project in enumerate(self.projects, 1):
            status = "✓" if self.check_project_exists(i-1) else "✗"
            status_color = 'green' if status == "✓" else 'red'
            
            print(f"{i}. {project['name']} - {project['description']}")
            self.print_colored(f"   [{status}] Проект {status_color == 'green' and 'найден' or 'не найден'}", status_color)
            print()

        print("0. Выход")
        print("────────────────────────────────────────")
        print()

    def check_project_exists(self, index):
        """Проверка существования проекта"""
        project = self.projects[index]
        project_path = self.base_dir / project['folder']
        file_path = project_path / project['file']
        
        return project_path.exists() and file_path.exists()

    def check_dependencies(self):
        """Проверка наличия необходимых компиляторов"""
        missing = []
        
        # Проверяем GCC для C
        try:
            subprocess.run(['gcc', '--version'], capture_output=True, check=True)
        except:
            missing.append('GCC (для C)')
        
        # Проверяем G++ для C++
        try:
            subprocess.run(['g++', '--version'], capture_output=True, check=True)
        except:
            missing.append('G++ (для C++)')
        
        return missing

    def run_python(self, project_path, file_name, is_bot=False):
        """Запуск Python проекта"""
        self.print_colored(f"\n[Python] Запуск {file_name}...", 'cyan')
        
        try:
            # Переходим в директорию проекта
            os.chdir(project_path)
            
            # Проверяем наличие run.py для бота
            if is_bot and os.path.exists('run.py'):
                self.print_colored("Запуск через run.py...", 'yellow')
                subprocess.run([sys.executable, 'run.py'], check=True)
            else:
                # Обычный запуск Python файла
                subprocess.run([sys.executable, file_name], check=True)
                
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Ошибка при выполнении Python скрипта: {e}", 'red')
        except KeyboardInterrupt:
            self.print_colored("\n\nПрограмма остановлена пользователем", 'yellow')
        except Exception as e:
            self.print_colored(f"Ошибка: {e}", 'red')
        finally:
            # Возвращаемся в исходную директорию
            os.chdir(self.base_dir)

    def compile_and_run_c(self, project_path, file_name):
        """Компиляция и запуск C проекта"""
        output = f"build_{Path(file_name).stem}"
        if self.is_windows:
            output += ".exe"
        
        self.print_colored(f"\n[C] Компиляция {file_name}...", 'cyan')
        
        try:
            # Переходим в директорию проекта
            os.chdir(project_path)
            
            # Компиляция
            compiler = 'gcc'
            compile_cmd = [compiler, file_name, '-o', output]
            
            # Добавляем дополнительные флаги для Windows
            if self.is_windows:
                compile_cmd.append('-D_WIN32')
            
            result = subprocess.run(compile_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.print_colored("Ошибка компиляции:", 'red')
                print(result.stderr)
                return
            
            self.print_colored("Компиляция успешна!", 'green')
            
            # Запуск
            self.print_colored(f"Запуск {output}...", 'cyan')
            run_cmd = [f'./{output}'] if not self.is_windows else [output]
            
            # Для интерактивных программ
            subprocess.run(run_cmd)
            
        except FileNotFoundError:
            self.print_colored("GCC не найден в системе. Установите компилятор C.", 'red')
        except Exception as e:
            self.print_colored(f"Ошибка: {e}", 'red')
        finally:
            # Очистка
            if os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            os.chdir(self.base_dir)

    def compile_and_run_cpp(self, project_path, file_name):
        """Компиляция и запуск C++ проекта"""
        output = f"build_{Path(file_name).stem}"
        if self.is_windows:
            output += ".exe"
        
        self.print_colored(f"\n[C++] Компиляция {file_name}...", 'cyan')
        
        try:
            # Переходим в директорию проекта
            os.chdir(project_path)
            
            # Компиляция
            compiler = 'g++'
            compile_cmd = [compiler, file_name, '-o', output, '-std=c++11']
            
            # Добавляем дополнительные флаги для Windows
            if self.is_windows:
                compile_cmd.append('-D_WIN32')
            
            result = subprocess.run(compile_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.print_colored("Ошибка компиляции:", 'red')
                print(result.stderr)
                return
            
            self.print_colored("Компиляция успешна!", 'green')
            
            # Запуск
            self.print_colored(f"Запуск {output}...", 'cyan')
            run_cmd = [f'./{output}'] if not self.is_windows else [output]
            
            # Для интерактивных программ
            subprocess.run(run_cmd)
            
        except FileNotFoundError:
            self.print_colored("G++ не найден в системе. Установите компилятор C++.", 'red')
        except Exception as e:
            self.print_colored(f"Ошибка: {e}", 'red')
        finally:
            # Очистка
            if os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            os.chdir(self.base_dir)

    def run_project(self, choice):
        """Запуск выбранного проекта"""
        project = self.projects[choice - 1]
        project_path = self.base_dir / project['folder']
        file_name = project['file']
        
        if not self.check_project_exists(choice - 1):
            self.print_colored(f"\nОшибка: Проект {project['name']} не найден!", 'red')
            self.print_colored(f"Путь: {project_path}", 'yellow')
            return False
        
        self.print_colored(f"\nЗапуск: {project['name']} - {project['description']}", 'blue')
        self.print_colored("=" * 50, 'blue')
        
        if project['language'] == 'python':
            self.run_python(project_path, file_name, project.get('is_bot', False))
        elif project['language'] == 'c':
            self.compile_and_run_c(project_path, file_name)
        elif project['language'] == 'cpp':
            self.compile_and_run_cpp(project_path, file_name)
        
        return True

    def check_all_projects(self):
        """Проверка всех проектов перед запуском"""
        self.print_colored("\n🔍 Проверка проектов...", 'cyan')
        
        missing = []
        for i, project in enumerate(self.projects):
            if not self.check_project_exists(i):
                missing.append(f"{i+1}. {project['name']}")
        
        if missing:
            self.print_colored("\n⚠️  Отсутствуют проекты:", 'yellow')
            for m in missing:
                self.print_colored(f"   {m}", 'yellow')
            
            # Проверяем наличие компиляторов
            deps = self.check_dependencies()
            if deps:
                self.print_colored("\n⚠️  Отсутствуют компиляторы:", 'yellow')
                for d in deps:
                    self.print_colored(f"   {d}", 'yellow')
        
        input("\nНажмите Enter для продолжения...")

    def run(self):
        """Основной цикл программы"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_projects()
            
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
