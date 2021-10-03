import httplib2
# import apiclient.discovery
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import data


class GoogleWriter:
    def __init__(self):
        CREDENTIALS_FILE = 'creds.json'
        # ID Google Sheets документа (можно взять из его URL)
        # spreadsheet_id = 'id то таблицы'

        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = discovery.build('sheets', 'v4', http=httpAuth)

        self.spreadsheet_id = data.sheet_id


        self.list2_name = data.list2_name
        self.current_row = 1

    def write_row(self, row):

        values = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {f"range": f"{self.list2_name}!A{self.current_row }:H{self.current_row }",
                     "majorDimension": "ROWS",
                     "values": [row]},

                ]
            }
        ).execute()

        self.current_row += 1



GoogleWriter1 = GoogleWriter()


