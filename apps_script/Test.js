function testApiKeys() {
  const results = [];

  try {
    const res = callSerper_('test');
    results.push('Serper: OK (' + res.length + ' result(s) returned)');
  } catch (e) {
    results.push('Serper: FAILED — ' + e.message);
  }

  try {
    const draft = callGemini_('Reply with exactly this JSON and nothing else: {"status": "ok"}');
    results.push('Gemini: OK (parsed response: ' + JSON.stringify(draft) + ')');
  } catch (e) {
    results.push('Gemini: FAILED — ' + e.message);
  }

  Logger.log(results.join('\n\n'));
}

// Log-only diagnostic for the Patents-noise question (Serper.js's
// callSerperTyped_ comment: the /patents endpoint was never verified against
// Serper's live docs, and returned unrelated results for Sandstorm — e.g. an
// unrelated fire-alarm IoT patent). Run this directly from the script editor
// (select it in the function dropdown, click Run) with a company row
// selected in the HVT sheet first, then check View > Executions for the raw
// response — that tells us whether the endpoint itself is fundamentally
// noisy or just needs a different query shape, before deciding between a
// prompt-skepticism fix and something more involved.
function testSerperPatentsEndpoint() {
  const input = getActiveRowInput_();
  if (!input) return;

  const apiKey = getScriptProp_('SERPER_API_KEY');
  const response = UrlFetchApp.fetch('https://google.serper.dev/patents', {
    method: 'post',
    contentType: 'application/json',
    headers: { 'X-API-KEY': apiKey },
    payload: JSON.stringify({ q: input.name }),
    muteHttpExceptions: true
  });

  Logger.log('Query: ' + input.name);
  Logger.log('Status: ' + response.getResponseCode());
  Logger.log('Body: ' + response.getContentText());
}

function listGeminiModels() {
  const apiKey = getScriptProp_('GEMINI_API_KEY');
  const url = 'https://generativelanguage.googleapis.com/v1beta/models?key=' + apiKey;

  const response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  if (response.getResponseCode() !== 200) {
    throw new Error('ListModels error (' + response.getResponseCode() + '): ' + response.getContentText());
  }

  const data = JSON.parse(response.getContentText());
  const names = (data.models || [])
    .filter(function (m) { return (m.supportedGenerationMethods || []).indexOf('generateContent') !== -1; })
    .map(function (m) { return m.name.replace('models/', ''); });

  Logger.log(names.join('\n'));
  return names;
}
