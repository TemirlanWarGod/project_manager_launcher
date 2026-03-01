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
                'name': 'project_1(Semianov)',
                'description': 'Калькулятор на C',
                'file': 'main.c',
                'language': 'c'
            },
            {
                'name': 'project_2(Dushanov)',
                'description': 'Telegram бот на Python',
                'file': 'run.py',
                'language': 'python',
                'is_bot': True
            },
            {
                'name': 'project_3(Kluchnikova)',
                'description': 'Программа на C++',
                'file': 'main.cpp',
                'language': 'cpp'
            },
            {
                'name': 'project_4(Chnegov)',
                'description': 'Лабораторная работа на C++',
                'file': 'Лабораторная робота№2№2.cpp',
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
        project_path = self.base_dir / project['name']
        file_path = project_path / project['file']
        
        return project_path.exists() and file_path.exists()

    def run_python(self, project_path, file_name, is_bot=False):
        """Запуск Python проекта"""
        self.print_colored(f"\n[Python] Запуск {file_name}...", 'cyan')
        
        try:
            # Переходим в директорию проекта
            os.chdir(project_path)
            
            if is_bot and file_name == 'run.py':
                # Для Telegram бота используем специальный запуск
                subprocess.run([sys.executable, file_name], check=True)
            else:
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
            
            subprocess.run(compile_cmd, check=True)
            self.print_colored("Компиляция успешна!", 'green')
            
            # Запуск
            self.print_colored(f"Запуск {output}...", 'cyan')
            run_cmd = [f'./{output}'] if not self.is_windows else [output]
            subprocess.run(run_cmd, check=True)
            
            # Очистка
            if os.path.exists(output):
                os.remove(output)
                
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Ошибка компиляции: {e}", 'red')
        except FileNotFoundError:
            self.print_colored("GCC не найден в системе. Установите компилятор C.", 'red')
        except Exception as e:
            self.print_colored(f"Ошибка: {e}", 'red')
        finally:
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
            
            subprocess.run(compile_cmd, check=True)
            self.print_colored("Компиляция успешна!", 'green')
            
            # Запуск
            self.print_colored(f"Запуск {output}...", 'cyan')
            run_cmd = [f'./{output}'] if not self.is_windows else [output]
            subprocess.run(run_cmd, check=True)
            
            # Очистка
            if os.path.exists(output):
                os.remove(output)
                
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Ошибка компиляции: {e}", 'red')
        except FileNotFoundError:
            self.print_colored("G++ не найден в системе. Установите компилятор C++.", 'red')
        except Exception as e:
            self.print_colored(f"Ошибка: {e}", 'red')
        finally:
            os.chdir(self.base_dir)

    def run_project(self, choice):
        """Запуск выбранного проекта"""
        project = self.projects[choice - 1]
        project_path = self.base_dir / project['name']
        file_name = project['file']
        
        if not self.check_project_exists(choice - 1):
            self.print_colored(f"\nОшибка: Проект {project['name']} не найден!", 'red')
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

    def run(self):
        """Основной цикл программы"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_projects()
            
            try:
                choice = input("Выберите проект (0-4): ").strip()
                
                if choice == '0':
                    self.print_colored("\nВыход...", 'yellow')
                    break
                
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