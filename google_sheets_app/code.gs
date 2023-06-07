// Health Insurance cross-sell
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Sebmatecho')
    .addItem('Get Prediction', 'PredictAll')
    .addToUi();
}

host_production = 'health-insurance-api-oanp.onrender.com'
// Helper function 
function ApiCall(data, endpoint){
  var url = 'https://' + host_production + endpoint;
  var payload = JSON.stringify( data );

  var options = {'method':'POST', 'contentType':'application/json', 'payload':payload};
  var response = UrlFetchApp.fetch(url, options );

  // get response 
  var rc = response.getResponseCode();
  var responseText = response.getContentText(); 

  if (rc !== 200){
    Logger.log('Response (%s) %s', rc, responseText);
  }
  else{
    prediction = JSON.parse(responseText);
  }

  return prediction;
}

// Health Insurance Propensity Score Prediction

// Health Insurance Propensity Score Prediction
function PredictAll(){
  var ss = SpreadsheetApp.getActiveSheet();
  var titleColumns = ss.getRange('A1:J1').getValues()[0];
  var lastRow = ss.getLastRow()
  var data = ss.getRange('A2' + ':' + 'J' + lastRow).getValues();

  // create a list of JSON objects
  var json_list = []
  for (row in data ) {
    var json = new Object()
    for (var j = 0; j < titleColumns.length; j++){
      json[titleColumns[j]] = data[row][j];
    }
    json_list.push(json);
  }

  // send JSON data to API
  var response = ApiCall(json_list, '/predict');
  // ss.getRange(11, 11).setValue(JSON.parse(response)['score'][0])

  // update spreadsheet with API response
  for (var i = 0; i < response.length; i++) {
    ss.getRange(Number(i) + 2, 11).setValue(JSON.parse(response)['score'][i]);
  }
};
