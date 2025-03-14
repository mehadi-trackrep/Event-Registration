const SHEET_URL = "https://docs.google.com/spreadsheets/d/............/edit?gid=0#gid=0";
const SHEET_NAME = "smsService";

const doGet = () => {
  const sheet = SpreadsheetApp.openByUrl(SHEET_URL).getSheetByName(SHEET_NAME);
  const [header, ...data] = sheet.getDataRange().getDisplayValues();

  const PHONE = header.indexOf("PhoneNumber");
  const TEXT = header.indexOf("Message");
  const STATUS = header.indexOf("Status");
  const VERIFIED = header.indexOf("Verified?");

  const output = [];

  data.forEach((row, index) => {
    if (row[STATUS] === "" && row[VERIFIED] === "y" && row[PHONE] !== "" && row[PHONE].trim().startsWith("+880")) {
      output.push([index + 1, row[PHONE], row[TEXT]]);
    }
  });

  const json = JSON.stringify(output);

  return ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.TEXT);
};

const doPost = e => {
  const sheet = SpreadsheetApp.openByUrl(SHEET_URL).getSheetByName(SHEET_NAME);
  const [header] = sheet.getRange("A1:1").getValues();
  const STATUS = header.indexOf("Status");
  var rowId = Number(e.parameter.row);
  sheet.getRange(rowId + 1, STATUS + 1).setValue("SMS Sent");
  return ContentService.createTextOutput("").setMimeType(ContentService.MimeType.TEXT);
};