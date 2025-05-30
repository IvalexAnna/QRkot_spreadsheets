from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

from . import constants

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Создает новую Google-таблицу с заданными параметрами и возвращает её ID.
    """

    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover("sheets", "v4")

    spreadsheet_body = {
        "properties": {
            "title": constants.SPREADSHEET_TITLE_TEMPLATE.format(
                now_date_time
            ),
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": constants.SHEET_TYPE,
                    "sheetId": constants.SHEET_ID,
                    "title": constants.SHEET_TITLE,
                    "gridProperties": {
                        "rowCount": constants.ROW_COUNT,
                        "columnCount": constants.COLUMN_COUNT,
                    },
                }
            }
        ],
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        "type": constants.PERMISSION_TYPE,
        "role": constants.PERMISSION_ROLE,
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str, projects: list, wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")

    table_values = [
        [constants.TABLE_HEADER_1, now_date_time],
        [constants.TABLE_HEADER_2],
        constants.TABLE_COLUMNS,
    ]

    for project in projects:
        new_row = [str(project[0]), str(project[1]), str(project[2])]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=constants.UPDATE_RANGE,
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
