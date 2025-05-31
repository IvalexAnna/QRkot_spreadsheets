from datetime import datetime
from typing import List, Tuple

from aiogoogle import Aiogoogle

from app.core.config import settings
from . import constants


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Создает новую Google-таблицу с заданными параметрами и возвращает её ID.
    """

    now_date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    service = await wrapper_services.discover("sheets", "v4")

    spreadsheet_body = {
        "properties": {
            "title": constants.SPREADSHEET_TITLE_TEMPLATE.format(
                now_date_time
            ),
            "locale": constants.LOCALE,
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
    spreadsheetid: str,
    projects: List[Tuple[str, str, str]],
    wrapper_services: Aiogoogle,
) -> None:
    now_date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    service = await wrapper_services.discover("sheets", "v4")

    table_values = [
        [constants.TABLE_HEADER_1, now_date_time],
        [constants.TABLE_HEADER_2],
        constants.TABLE_COLUMNS,
    ]

    for project_name_1, project_name_2, project_name_3 in projects:
        new_row = [str(project_name_1),
                   str(project_name_2),
                   str(project_name_3)]
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
