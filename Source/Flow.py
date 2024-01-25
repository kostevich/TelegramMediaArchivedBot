
#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from threading import Thread


import requests
import logging

#==========================================================================================#
# >>>>> ПОТОК И ЕГО ОБРАБОТКА <<<<< #
#==========================================================================================#

class Flow:
    
    #==========================================================================================#
    # >>>>> ОБРАБОТКА ПОТОКА <<<<< #
    #==========================================================================================#
        
    def __DownloadThread(self):
        # Логгирование.
        logging.info("Поток запущен.")
        
        # Пока поток запущен.
        while True:
            # Скачиваем файл.
            self.DownloadFile()

    #==========================================================================================#
    # >>>>> КОНСТРУКТОР <<<<< #
    #==========================================================================================#

    def __init__(self, Settings):
        # Создание потока.
        self.__Download = Thread(target = self.__DownloadThread)

        # Очередь медиафайлов.
        self.__MessagesBufer = list()

        # Запуск очереди.
        self.__Download.start()

        # Состояния очереди.
        self.CheckEmptyThread = self.EmptyFlowStatus

        # Настройки.
        self.Settings = Settings

    #==========================================================================================#
    # >>>>> ДОБАВЛЕНИЕ ФАЙЛА В ОЧЕРЕДЬ МЕДИАФАЙЛОВ <<<<< #
    #==========================================================================================#   
                   
    def AddFileInfo(self, FileInfo: any, UserDataObject: any):
        # Добавление файла в список.
        self.__MessagesBufer.append(
            {
                "File": FileInfo,
                "User": UserDataObject.GetUserID()
            }
        )

    #==========================================================================================#
    # >>>>> ЗАГРУЗКА ФАЙЛОВ <<<<< #
    #==========================================================================================# 
           
    def DownloadFile(self):
        # Получение данных файла.
        try:
            # Данные файла из списка словарей.
            File = self.__MessagesBufer[0]["File"]

            # Данные пользователя из списка словарей.
            User = self.__MessagesBufer[0]["User"]

            # Расширение файла.
            FileType = "." + File.file_path.split('.')[-1]

            # Загрузка файла.
            Response = requests.get("https://api.telegram.org/file/bot" + self.Settings["token"] + "/" + f"{File.file_path}")

            # Сохранение файла.
            with open(f"Data/Files/{User}/" + str(File.file_unique_id) + FileType, "wb") as FileWriter:
                FileWriter.write(Response.content)

                # Удаление элемента из списка.
                self.__MessagesBufer.pop(0)
                
        except:
            # Логгирование.
            logging.error("Не получилось загрузить файл.") 

    #==========================================================================================#
    # >>>>> ПРОВЕРКА ПУСТОТЫ ПОТОКА <<<<< #
    #==========================================================================================#
            
    def EmptyFlowStatus(self) -> bool:
        # Если в списке есть элементы.
        if len(self.__MessagesBufer) > 0: 
            return False
        else:
            return True
            