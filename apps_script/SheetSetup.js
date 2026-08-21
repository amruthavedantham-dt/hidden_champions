function setupHVTSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  let hvtSheet = ss.getSheetByName(HVT_SHEET_NAME);
  let migratedRows = [];
  if (!hvtSheet) {
    hvtSheet = ss.insertSheet(HVT_SHEET_NAME);
  } else {
    // Schema can change (columns added/removed/reordered) between runs.
    // Migrate by COLUMN NAME, not position, so existing rows survive any
    // future schema edit instead of only surviving a same-shape rewrite.
    migratedRows = readHvtRowsByColumnName_(hvtSheet);
    // clear() alone clears content/formats but leaves existing data
    // validation rules attached to their cells. If a future schema change
    // inserts/reorders columns, a physical cell that used to hold one
    // column's value (validated against one enum) can become the target of
    // a differently-named column (validated against a different enum) —
    // writing that column's migrated value into a cell still carrying the
    // OLD validation rule throws "violates the data validation rules".
    // clearContent()+clearDataValidations() wipes both, so the validation
    // rules set up below are the only ones in effect after this runs.
    const fullRange = hvtSheet.getRange(1, 1, hvtSheet.getMaxRows(), hvtSheet.getMaxColumns());
    fullRange.clearContent();
    fullRange.clearDataValidations();
    fullRange.clearFormat();
  }

  hvtSheet.getRange(1, 1, 1, HVT_HEADERS.length).setValues([HVT_HEADERS]);
  hvtSheet.setFrozenRows(1);

  if (migratedRows.length > 0) {
    const rebuiltRows = migratedRows.map(function (rowMap) {
      return HVT_HEADERS.map(function (colName) { return rowMap[colName] !== undefined ? rowMap[colName] : ''; });
    });
    hvtSheet.getRange(2, 1, rebuiltRows.length, HVT_HEADERS.length).setValues(rebuiltRows);
  }

  const reviewRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(REVIEW_STATUS_OPTIONS, true)
    .setAllowInvalid(false)
    .build();

  const maxRows = 1200; // bumped from 500 for the 1,100-company scale-up
  REVIEW_COLUMNS.forEach(function (colName) {
    const colIndex = HVT_HEADERS.indexOf(colName) + 1;
    hvtSheet.getRange(2, colIndex, maxRows - 1, 1).setDataValidation(reviewRule);
  });

  let rawSheet = ss.getSheetByName(RAW_EVIDENCE_SHEET_NAME);
  if (!rawSheet) rawSheet = ss.insertSheet(RAW_EVIDENCE_SHEET_NAME);
  rawSheet.clear();
  rawSheet.getRange(1, 1, 1, RAW_EVIDENCE_HEADERS.length).setValues([RAW_EVIDENCE_HEADERS]);
  rawSheet.setFrozenRows(1);

  SpreadsheetApp.getUi().alert(
    'HVT and RAW_EVIDENCE sheets are set up.\n\n' +
    'HVT: ' + HVT_HEADERS.length + ' columns, header row frozen, dropdown validation live on ' +
    REVIEW_COLUMNS.join(', ') + ' (rows 2-500).\n' +
    (migratedRows.length > 0 ? migratedRows.length + ' existing row(s) migrated by column name.\n' : '') +
    'RAW_EVIDENCE: staging sheet for Serper results, ready.'
  );
}

function readHvtRowsByColumnName_(sheet) {
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();
  if (lastRow < 2 || lastCol < 1) return [];

  const oldHeaders = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  const dataRows = sheet.getRange(2, 1, lastRow - 1, lastCol).getValues();

  return dataRows
    .filter(function (row) { return row.some(function (cell) { return cell !== ''; }); })
    .map(function (row) {
      const rowMap = {};
      oldHeaders.forEach(function (headerName, idx) {
        if (headerName) rowMap[headerName] = row[idx];
      });
      return rowMap;
    });
}
