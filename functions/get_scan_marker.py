

def FIND_SCAN_MARKER(worksheet):
    worksheet_title_row = worksheet.row_values(1)
    marker_dist = {}
    for seller_name in worksheet_title_row:
        seller_name_cell = worksheet.find(seller_name)
        seller_scan_marker = worksheet.cell(seller_name_cell.row + 2, seller_name_cell.col).value
        marker_dist.update({seller_name : seller_scan_marker})
    print(marker_dist)
    return marker_dist