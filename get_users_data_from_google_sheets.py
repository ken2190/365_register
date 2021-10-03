import httplib2
# import apiclient.discovery
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import data

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
# spreadsheet_id = 'id то таблицы'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)


spreadsheetId = data.sheet_id
ranges = ["A1:G1000"]

results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                   ranges=ranges,
                                                   valueRenderOption='FORMATTED_VALUE',
                                                   dateTimeRenderOption='FORMATTED_STRING').execute()
sheet_user_values = results['valueRanges'][0]['values']
print(sheet_user_values)





#
# line_for_google = 1
# def google_table(line_for_google, a1,a2,a3,a4,a5,a6,a7,a8,a9,a10):
#     values = service.spreadsheets().values().batchUpdate(
#         spreadsheetId=spreadsheet_id,
#         body={
#             "valueInputOption": "USER_ENTERED",
#             "data": [
#                 {f"range": f"A{line_for_google}:J{line_for_google}",
#                  "majorDimension": "ROWS",
#                  "values": [[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10]]},
#
#             ]
#         }
#     ).execute()
# line_for_google+=1




