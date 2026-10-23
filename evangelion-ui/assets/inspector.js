'use strict';

// Standalone, local-only syntax inspection. Never evaluate source as JavaScript.
const byId = id => document.getElementById(id);
const source = byId('source');
const limit = 1024 * 1024;
const encoder = new TextEncoder();
let revision = 0;
let checkedSource = null;

function status(message, state) {
  byId('status').textContent = message;
  byId('status').dataset.state = state;
}

function invalidate() {
  revision += 1;
  checkedSource = null;
  byId('download').disabled = true;
  byId('check').disabled = !source.value.trim();
  byId('clear').disabled = !source.value;
  byId('summary').hidden = true;
  byId('empty').hidden = false;
  byId('source-error').textContent = '';
  source.setAttribute('aria-invalid', 'false');
  status(source.value.trim() ? 'Not checked' : 'No source', 'unknown');
  byId('empty').textContent = source.value.trim()
    ? 'Check the source to inspect its type and size.'
    : 'Open or paste JSON to begin. Results come from your source.';
}

function error(message) {
  checkedSource = null;
  byId('download').disabled = true;
  byId('source-error').textContent = message;
  source.setAttribute('aria-invalid', 'true');
  status('Needs correction', 'error');
}

source.addEventListener('input', invalidate);

byId('source-file').addEventListener('change', async event => {
  const file = event.target.files[0];
  if (!file) return;
  const requestedRevision = ++revision;
  // Allow reopening the same file after fixing it on disk.
  event.target.value = '';
  if (file.size > limit) {
    // A refused import leaves the current editor and its checked result intact.
    byId('source-error').textContent = 'File exceeds 1 MiB. The current source was kept.';
    status('File not opened', 'warning');
    return;
  }
  status('Reading file', 'pending');
  try {
    const text = await file.text();
    if (requestedRevision !== revision) return;
    source.value = text;
    invalidate();
    source.focus();
  } catch {
    if (requestedRevision !== revision) return;
    byId('source-error').textContent = 'Could not read this file. The current source was kept.';
    status('File not opened', 'warning');
  }
});

byId('check').addEventListener('click', () => {
  // Cancel an older file read so it cannot replace a freshly checked edit.
  invalidate();
  const text = source.value;
  if (!text.trim()) return;
  const bytes = encoder.encode(text).length;
  if (bytes > limit) {
    error('Source exceeds 1 MiB. Reduce its size before checking.');
    return;
  }
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch (failure) {
    error('JSON syntax error: ' + failure.message);
    return;
  }
  checkedSource = text;
  const array = Array.isArray(parsed);
  const kind = parsed === null ? 'null' : array ? 'array' : typeof parsed;
  byId('bytes').textContent = bytes.toLocaleString() + ' bytes';
  byId('kind').textContent = kind;
  byId('entries-label').textContent = array ? 'Array items' : 'Object properties';
  byId('entries').textContent = array ? String(parsed.length)
    : kind === 'object' ? String(Object.keys(parsed).length) : 'Not applicable';
  byId('summary').hidden = false;
  byId('empty').hidden = true;
  byId('download').disabled = false;
  status('JSON syntax checked', 'success');
});

byId('download').addEventListener('click', () => {
  if (checkedSource === null || checkedSource !== source.value) {
    invalidate();
    return;
  }
  const url = URL.createObjectURL(new Blob([checkedSource], {type:'application/json'}));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'checked.json';
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

byId('clear').addEventListener('click', () => {
  source.value = '';
  invalidate();
  source.focus();
});

byId('palette').addEventListener('change', event => {
  document.body.dataset.palette = event.target.value;
});
byId('analog').addEventListener('change', event => {
  document.body.dataset.analog = event.target.value;
});
invalidate();
