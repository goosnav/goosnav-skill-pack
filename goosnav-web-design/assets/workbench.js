/* The conversion function is also available to Node for focused validation. */
(function () {
  "use strict";
  const MAX_BYTES = 256 * 1024;
  const MAX_ITEMS = 5000;
  const MAX_ITEM_LENGTH = 1000;

  function convertList(text, options = {}) {
    if (typeof text !== "string") throw new Error("Provide a plain text list.");
    if (new TextEncoder().encode(text).byteLength > MAX_BYTES) {
      throw new Error("The list is larger than 256 KiB. Split it into smaller files.");
    }
    if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/.test(text)) {
      throw new Error("The input contains binary control characters. Use a UTF-8 plain text file.");
    }
    const lines = text.replace(/^\uFEFF/, "").split(/\r\n|\r|\n/).map(line => line.trim()).filter(Boolean);
    if (!lines.length) throw new Error("Add at least one nonempty item, one per line.");
    if (lines.length > MAX_ITEMS) throw new Error("Use no more than 5,000 nonempty lines in one conversion.");
    const longItem = lines.findIndex(line => line.length > MAX_ITEM_LENGTH);
    if (longItem !== -1) throw new Error(`Item ${longItem + 1} exceeds 1,000 characters. Shorten it or split it across lines.`);
    let items = options.deduplicate === false ? lines.slice() : [...new Set(lines)];
    if (options.sort) items.sort((a, b) => a.localeCompare(b));
    const json = JSON.stringify(items, null, 2) + "\n";
    return {
      items, json, inputCount: lines.length,
      removedCount: lines.length - items.length,
      bytes: new TextEncoder().encode(json).byteLength
    };
  }

  if (typeof module !== "undefined" && module.exports) module.exports = { convertList };
  if (typeof document === "undefined") return;

  const byId = id => document.getElementById(id);
  const form = byId("list-form");
  const controls = byId("input-controls");
  const source = byId("list-source");
  const fileInput = byId("list-file");
  const deduplicate = byId("remove-duplicates");
  const sort = byId("sort-items");
  const convert = byId("convert");
  const download = byId("download");
  const status = byId("status");
  const error = byId("input-error");
  const resultState = byId("result-state");
  let objectURL = null;
  let busy = false;

  function announce(message) {
    if (status.textContent !== message) status.textContent = message;
  }
  function resetError() {
    error.hidden = true;
    error.textContent = "";
    source.removeAttribute("aria-invalid");
    fileInput.removeAttribute("aria-invalid");
  }
  function clearResult() {
    if (objectURL) URL.revokeObjectURL(objectURL);
    objectURL = null;
    download.disabled = true;
    byId("json-preview").textContent = "";
    byId("json-preview").hidden = true;
    byId("empty-result").hidden = false;
    byId("output-count").textContent = "—";
    byId("output-bytes").textContent = "—";
    byId("download-note").textContent = "Convert a list to enable download.";
    resultState.textContent = source.value.trim() ? "Not converted" : "Empty";
    resultState.dataset.state = "empty";
  }
  function refreshInput() {
    const count = source.value.split(/\r\n|\r|\n/).filter(line => line.trim()).length;
    byId("input-count").textContent = count.toLocaleString();
    convert.disabled = busy || count === 0;
  }
  function changed() {
    const hadResult = Boolean(objectURL);
    resetError();
    clearResult();
    refreshInput();
    announce(hadResult ? "Input changed. Convert again for a current download." : source.value.trim() ? "Ready to convert." : "Add a list to begin.");
  }
  function showError(message, field) {
    clearResult();
    error.textContent = message;
    error.hidden = false;
    if (field) field.setAttribute("aria-invalid", "true");
    resultState.textContent = "Needs correction";
    resultState.dataset.state = "error";
    announce("Conversion unavailable. Correct the input above.");
  }
  function setBusy(value) {
    busy = value;
    controls.disabled = value;
    form.setAttribute("aria-busy", String(value));
    download.disabled = value || !objectURL;
    refreshInput();
  }

  source.addEventListener("input", () => {
    byId("source-kind").textContent = source.value.trim() ? "Entered text" : "No input";
    fileInput.value = "";
    changed();
  });
  deduplicate.addEventListener("change", changed);
  sort.addEventListener("change", changed);

  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;
    resetError();
    clearResult();
    if (file.size > MAX_BYTES) {
      showError("Choose a text file no larger than 256 KiB. Your current text has been kept.", fileInput);
      fileInput.value = "";
      return;
    }
    setBusy(true);
    announce(`Reading ${file.name}…`);
    let failed = false;
    try {
      const data = await file.arrayBuffer();
      source.value = new TextDecoder("utf-8", { fatal: true }).decode(data);
      byId("source-kind").textContent = file.name;
      refreshInput();
      announce(`Loaded ${file.name}. Review the list, then convert.`);
    } catch (_) {
      failed = true;
      showError("This file could not be read as UTF-8 text. Choose a plain text file; your current text has been kept.", fileInput);
    } finally {
      fileInput.value = "";
      setBusy(false);
      if (failed) fileInput.focus();
    }
  });

  byId("sample").addEventListener("click", () => {
    source.value = "Lab report\nInput fixture\nBoard assembly\nLab report";
    fileInput.value = "";
    byId("source-kind").textContent = "Sample list";
    changed();
    announce("Sample loaded: four lines, including one exact duplicate.");
    source.focus();
  });

  byId("clear").addEventListener("click", () => {
    form.reset();
    source.value = "";
    byId("source-kind").textContent = "No input";
    changed();
    source.focus();
  });

  form.addEventListener("submit", event => {
    event.preventDefault();
    if (busy) return;
    resetError();
    clearResult();
    try {
      const result = convertList(source.value, { deduplicate: deduplicate.checked, sort: sort.checked });
      objectURL = URL.createObjectURL(new Blob([result.json], { type: "application/json;charset=utf-8" }));
      byId("json-preview").textContent = result.json;
      byId("json-preview").hidden = false;
      byId("empty-result").hidden = true;
      byId("output-count").textContent = result.items.length.toLocaleString();
      byId("output-bytes").textContent = result.bytes.toLocaleString();
      resultState.textContent = "Ready";
      resultState.dataset.state = "ready";
      byId("download-note").textContent = "goosnav-list.json";
      download.disabled = false;
      announce(`Created ${result.items.length} items from ${result.inputCount} lines. Removed ${result.removedCount} exact duplicates.`);
      byId("result-heading").focus();
    } catch (failure) {
      showError(failure.message || "Conversion failed. Check the input and try again.", source);
      source.focus();
    }
  });

  download.addEventListener("click", () => {
    if (!objectURL || busy) return;
    const link = document.createElement("a");
    link.href = objectURL;
    link.download = "goosnav-list.json";
    document.body.append(link);
    link.click();
    link.remove();
  });
  window.addEventListener("beforeunload", () => { if (objectURL) URL.revokeObjectURL(objectURL); });
  controls.disabled = false;
  refreshInput();
}());
