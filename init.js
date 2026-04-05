#!/usr/bin/env node
"use strict";

const fs   = require("fs");
const path = require("path");

const src  = path.join(__dirname, "src");
const dest = path.join(process.cwd(), "formseal");

if (fs.existsSync(dest)) {
  console.error("[formseal] ./formseal/ already exists.");
  console.error("           Remove it first if you want a fresh scaffold.");
  process.exit(1);
}

function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const srcPath  = path.join(from, entry.name);
    const destPath = path.join(to, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

copyDir(src, dest);

console.log("[formseal] Scaffolded into ./formseal/");
console.log("");
console.log("Next steps:");
console.log("  1. Edit formseal/config/formseal.config.js");
console.log("       -- set endpoint");
console.log("       -- set recipientPublicKey");
console.log("  2. Edit formseal/config/fields.schema.js");
console.log("       -- set formSelector, submitSelector, statusSelector");
console.log("       -- define your field validation rules");
console.log("  3. Add to your HTML:");
console.log('       <script src="/formseal/globals.js"></script>');
console.log("");
console.log("See sample/index.html in the repo for a complete wiring example.");
console.log("https://github.com/grayguava/formseal-client/blob/main/sample/index.html");