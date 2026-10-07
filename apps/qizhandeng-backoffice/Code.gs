const SPREADSHEET_ID = '1JISdp8MVGHwpI3cpsTlcDXRqzlTNt8HSFMW8IWnkr7M';

const MODULES = [
  { key: 'dashboard', name: '營運儀表板', sheet: '營運儀表板', readonly: true },
  { key: 'customers', name: '客戶主檔', sheet: '客戶主檔' },
  { key: 'suppliers', name: '供應商主檔', sheet: '供應商主檔' },
  { key: 'sku', name: '商品主檔', sheet: '商品主檔' },
  { key: 'warehouse', name: '倉庫儲位', sheet: '倉庫儲位' },
  { key: 'orders', name: '客戶訂單', sheet: '客戶訂單' },
  { key: 'purchase', name: '採購單', sheet: '採購單' },
  { key: 'inbound', name: '入庫驗收', sheet: '入庫驗收' },
  { key: 'inventory_ledger', name: '庫存流水', sheet: '庫存流水', readonly: true },
  { key: 'stock', name: '庫存餘額', sheet: '庫存餘額', readonly: true },
  { key: 'delivery', name: '配送排程', sheet: '配送排程' },
  { key: 'proof', name: '配送簽收', sheet: '配送簽收' },
  { key: 'exceptions', name: '異常案件', sheet: '異常案件' },
  { key: 'reconciliation', name: '對帳損益', sheet: '對帳損益' },
  { key: 'notifications', name: '通知佇列', sheet: '通知佇列', readonly: true },
  { key: 'audit', name: '稽核紀錄', sheet: '稽核紀錄', readonly: true },
  { key: 'automation', name: '自動化任務', sheet: '自動化任務' },
  { key: 'tests', name: '驗收測試', sheet: '驗收測試' },
  { key: 'sop', name: '後勤作業SOP', sheet: '後勤作業SOP', readonly: true },
  { key: 'roles', name: '使用者權限', sheet: '使用者權限' },
  { key: 'config', name: '系統設定', sheet: '系統設定' }
];

function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('七盞燈｜供應鏈後勤營運系統')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1, viewport-fit=cover');
}

function getBootstrap() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  return {
    appName: '七盞燈｜供應鏈後勤營運系統',
    modules: MODULES,
    spreadsheetName: ss.getName(),
    lastUpdated: new Date().toISOString(),
    dashboard: getDashboardData_()
  };
}

function getDashboardData_() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName('營運儀表板');
  if (!sheet) return [];
  const rows = Math.max(5, sheet.getLastRow());
  const values = sheet.getRange(1, 1, rows, 3).getDisplayValues();
  return values.slice(1).filter(r => r[0]).map(r => ({ label: r[0], value: r[1], note: r[2] }));
}

function getModuleData(moduleKey, page, pageSize, search) {
  const mod = MODULES.find(m => m.key === moduleKey);
  if (!mod) throw new Error('找不到模組');
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName(mod.sheet);
  if (!sheet) throw new Error('找不到工作表：' + mod.sheet);

  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();
  if (lastRow < 1 || lastCol < 1) return { headers: [], rows: [], total: 0, module: mod };

  const all = sheet.getRange(1, 1, lastRow, lastCol).getDisplayValues();
  const headers = all[0];
  let rows = all.slice(1)
    .map((r, i) => ({ rowNumber: i + 2, values: r }))
    .filter(x => x.values.some(v => String(v).trim() !== ''));

  const q = String(search || '').trim().toLowerCase();
  if (q) rows = rows.filter(x => x.values.some(v => String(v).toLowerCase().includes(q)));

  const total = rows.length;
  page = Math.max(1, Number(page) || 1);
  pageSize = Math.min(100, Math.max(10, Number(pageSize) || 30));
  const start = (page - 1) * pageSize;
  rows = rows.slice(start, start + pageSize);

  return { headers, rows, total, page, pageSize, module: mod };
}

function saveRecord(moduleKey, rowNumber, record) {
  const mod = MODULES.find(m => m.key === moduleKey);
  if (!mod) throw new Error('找不到模組');
  if (mod.readonly) throw new Error('此模組為唯讀');

  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName(mod.sheet);
  if (!sheet) throw new Error('找不到工作表');
  const lastCol = sheet.getLastColumn();
  const headers = sheet.getRange(1, 1, 1, lastCol).getDisplayValues()[0];

  if (rowNumber && Number(rowNumber) >= 2) {
    const target = sheet.getRange(Number(rowNumber), 1, 1, lastCol);
    const formulas = target.getFormulas()[0];
    const current = target.getValues()[0];
    const next = headers.map((h, i) => formulas[i] || (Object.prototype.hasOwnProperty.call(record, h) ? record[h] : current[i]));
    target.setValues([next]);
    appendAudit_('修改', mod.sheet, String(rowNumber), '網站');
    return { ok: true, rowNumber: Number(rowNumber), message: '已更新' };
  }

  const row = headers.map(h => Object.prototype.hasOwnProperty.call(record, h) ? record[h] : '');
  sheet.appendRow(row);
  const newRow = sheet.getLastRow();
  if (newRow > 2) copyFormulaCells_(sheet, newRow - 1, newRow, lastCol);
  appendAudit_('新增', mod.sheet, String(newRow), '網站');
  return { ok: true, rowNumber: newRow, message: '已新增' };
}

function copyFormulaCells_(sheet, sourceRow, targetRow, lastCol) {
  const source = sheet.getRange(sourceRow, 1, 1, lastCol);
  const formulasR1C1 = source.getFormulasR1C1()[0];
  const target = sheet.getRange(targetRow, 1, 1, lastCol);
  const current = target.getValues()[0];
  const next = current.map((v, i) => formulasR1C1[i] || v);
  target.setValues([next]);
}

function voidRecord(moduleKey, rowNumber) {
  const mod = MODULES.find(m => m.key === moduleKey);
  if (!mod) throw new Error('找不到模組');
  if (mod.readonly) throw new Error('此模組為唯讀');
  rowNumber = Number(rowNumber);
  if (!rowNumber || rowNumber < 2) throw new Error('無效資料列');

  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName(mod.sheet);
  const lastCol = sheet.getLastColumn();
  const headers = sheet.getRange(1,1,1,lastCol).getDisplayValues()[0];
  const candidates = ['狀態','訂單狀態','採購單狀態','配送狀態','對帳狀態','驗收狀態'];
  const statusIndex = candidates.map(x => headers.indexOf(x)).find(x => x >= 0);
  if (statusIndex >= 0) sheet.getRange(rowNumber, statusIndex + 1).setValue('已取消');
  else sheet.getRange(rowNumber, 1, 1, lastCol).clearContent();

  appendAudit_('作廢', mod.sheet, String(rowNumber), '網站');
  return { ok: true, message: '已作廢' };
}

function appendAudit_(action, moduleName, referenceId, source) {
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = ss.getSheetByName('稽核紀錄');
    if (!sheet) return;
    const headers = sheet.getRange(1,1,1,sheet.getLastColumn()).getDisplayValues()[0];
    const values = new Array(headers.length).fill('');
    const map = {}; headers.forEach((h,i)=> map[h]=i);
    const put = (h,v) => { if (Object.prototype.hasOwnProperty.call(map,h)) values[map[h]] = v; };
    put('紀錄編號', 'LOG-' + Utilities.getUuid().slice(0,8).toUpperCase());
    put('時間戳記', new Date());
    put('執行者', Session.getActiveUser().getEmail() || '網站使用者');
    put('模組', moduleName); put('動作', action);
    put('關聯類型', '資料列'); put('關聯編號', referenceId);
    put('結果', '成功'); put('來源', source);
    sheet.appendRow(values);
  } catch (e) {
    console.error(e);
  }
}

function refreshDashboard() {
  SpreadsheetApp.flush();
  return getDashboardData_();
}
