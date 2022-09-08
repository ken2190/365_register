import gspread
import data


class GoogleSheet:
    def __init__(self):
        gc = gspread.service_account('creds.json')
        sht1 = gc.open_by_key(data.sheet_id)

        worksheets_list = sht1.worksheets()
        title_list = [i.title for i in worksheets_list]

        list1_name = data.list_with_info_name
        list2_name = data.list_with_result_name

        if not list1_name in title_list:
            sht1.add_worksheet(
                title=list1_name,
                cols=99,
                rows=20000
            )

        if not list2_name in title_list:
            sht1.add_worksheet(
                title=list2_name,
                cols=99,
                rows=20000
            )

        self.sht1 = sht1
        self.worksheet1 = self.sht1.worksheet(list1_name)
        self.worksheet2 = self.sht1.worksheet(list2_name)

    def get_all_values_from_worksheet1(self):
        return self.worksheet1.get_all_values()

    def get_all_values_from_worksheet2(self):
        return self.worksheet2.get_all_values()

    def get_row_to_work(self):
        rows = self.get_all_values_from_worksheet1()[1:]
        for row in rows:
            if row[-1] != '+':
                return row

        return []

    def update_info_finish_row(self):
        rows = self.get_all_values_from_worksheet1()
        for i in range(1, len(rows)):
            if rows[i][-1] == '-':
                rows[i][-1] = '+'
                break

        self.worksheet1.update('A1', rows)

    def add_row_to_second_table(self, row):
        rows = self.get_all_values_from_worksheet2()
        rows.append(row)
        print(rows)
        self.worksheet2.update('A1', rows)





if __name__ == '__main__':
    google_sheet_api = GoogleSheet()


    # google_sheet_api.add_row_to_second_table(['111', '222', 'sdd', 'sddsa'])
    # google_sheet_api.update_info_finish_row()
    # print(google_sheet_api.get_row_to_work())
    # Arr = [
    #     [(i+1)*(j+3) for i in range(10)] for j in range(20)
    # ]
    # google_sheet_api.clear_and_write_new_cells_to_worksheets(Arr)
    # print(google_sheet_api.get_all_values_from_worksheet2())

    # exit()
    # gc = gspread.service_account_from_dict(creds_for_google.creds_json)
    #
    # sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TGle4AX8QGAQQlchwZiIYmdLuIiDRGcAGg82Uutfrlw/edit#gid=0')
    #
    # # sht2.sheet1.add_rows(100)
    # Arr = [
    #     [i*j for i in range(10)] for j in range(20)
    # ]
    #
    #
    # worksheet = sht2.sheet1
    # worksheet.clear()
    # worksheet.update('A2', Arr)

    # worksheet_list = sht2.worksheets()
    # # print(worksheet_list)
    # print(sht2.sheet1.get_all_values())
    # print(sht2.sheet1.get())