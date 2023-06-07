from csv import DictWriter

from xlwt import Workbook


class SaveFile():
    """Сохранение данных в файлы."""
    def __init__(self) -> None:
        pass

    def to_csv(self, data, path):
        """Сохраняет данные в CSV."""
        keys = list(data[0].keys())
        with open(path, mode='w',
                  newline='', encoding='utf-8') as file:
            writer = DictWriter(file, keys)
            writer.writeheader()
            writer.writerows(data)

    def to_excel(self, data, path):
        """Сохраняет данные в Excel."""
        keys = list(data[0].keys())
        workbook = Workbook()
        worksheet = workbook.add_sheet('data')

        for i in range(len(keys)):
            worksheet.write(0, i, keys[i])

        for i in range(len(data)):
            j = 0
            for hotel in data[i].values():
                worksheet.write(i+1, j, str(hotel))
                j += 1
        workbook.save(path)
