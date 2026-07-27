// Rebuilt-on-demand review queue, same pattern as COST_SUMMARY — lists only
// the rows with triage_status = needs-review, so a human works from a short
// list instead of opening all 1,100 HVT rows to find the handful that
// actually need a look. triage_status itself is computed in Gemini.js's
// runGeminiStructure, right after unresolved_pillars — this file only reads
// it back out.
const REVIEW_QUEUE_SHEET_NAME = 'REVIEW_QUEUE';

function buildReviewQueue() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const hvtSheet = ss.getSheetByName(HVT_SHEET_NAME);
  if (!hvtSheet) throw new Error('HVT sheet not found.');

  const lastRow = hvtSheet.getLastRow();
  let queueSheet = ss.getSheetByName(REVIEW_QUEUE_SHEET_NAME);
  if (queueSheet) queueSheet.clear();
  else queueSheet = ss.insertSheet(REVIEW_QUEUE_SHEET_NAME);

  const headers = ['Company', 'Unresolved Pillars', 'Sector', 'Go to Row'];
  queueSheet.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
  queueSheet.setFrozenRows(1);

  if (lastRow <= 1) {
    SpreadsheetApp.getUi().alert('No company rows in HVT yet.');
    return;
  }

  const values = hvtSheet.getRange(2, 1, lastRow - 1, HVT_HEADERS.length).getValues();
  const nameCol = HVT_HEADERS.indexOf('company_name');
  const sectorCol = HVT_HEADERS.indexOf('sector');
  const unresolvedCol = HVT_HEADERS.indexOf('unresolved_pillars');
  const triageCol = HVT_HEADERS.indexOf('triage_status');

  const spreadsheetUrl = ss.getUrl();
  const hvtGid = hvtSheet.getSheetId();

  const rows = [];
  values.forEach(function (row, idx) {
    if (row[triageCol] !== TRIAGE_STATUS.NEEDS_REVIEW) return;
    const companyName = row[nameCol];
    const sheetRowNum = idx + 2;
    const link = '=HYPERLINK("' + spreadsheetUrl + '#gid=' + hvtGid + '&range=A' + sheetRowNum + '","Row ' + sheetRowNum + '")';
    rows.push([companyName, row[unresolvedCol], row[sectorCol], link]);
  });

  if (rows.length > 0) {
    queueSheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }
  queueSheet.autoResizeColumns(1, headers.length);

  SpreadsheetApp.getUi().alert('Review Queue rebuilt: ' + rows.length + ' row(s) need review out of ' + values.length + ' total.');
}
