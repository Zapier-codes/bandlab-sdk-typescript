#!/usr/bin/env node
/*
 * Coverage report.
 *
 * Parses api.md into endpoint rows (verb, path, accessor, method, file) and diffs them
 * against the inventory snapshot in docs/handover/endpoint-inventory.tsv.
 * With --markdown it prints the seed for docs/endpoint-status.md instead.
 * No dependencies; run it through ./scripts/coverage.
 *
 * Exit codes: 0 = no drift, 1 = drift between api.md and the inventory,
 *             2 = could not read or parse an input.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const DEFAULT_API = path.join(ROOT, 'api.md');
const DEFAULT_INVENTORY = path.join(ROOT, 'docs', 'handover', 'endpoint-inventory.tsv');

// <code title="get /users/{userId}">client.users.<a href="./src/resources/users/users.ts">retrieve</a>(...) -> ...</code>
const ROW = /<code title="([a-z]+) ([^"]+)">client\.([A-Za-z0-9_.]*)<a href="([^"]+)">([A-Za-z0-9_]+)<\/a>/;

const USAGE = `Usage: scripts/coverage [options]

Parses api.md into endpoint rows and diffs them against the inventory snapshot.

Options:
  --api <file>         api.md to read (default: api.md at the repo root)
  --inventory <file>   inventory TSV to compare against
                       (default: docs/handover/endpoint-inventory.tsv)
  --tsv                print the parsed rows as TSV and exit (verb, path, accessor, method, file); no diff
  --markdown           print the seed for docs/endpoint-status.md and exit; no diff. Rows present in the
                       inventory get status 'spec', any other row gets 'unverified'. Output is deterministic.
                       Seed only: edit the Status column by hand afterwards and do not regenerate over it.
  -h, --help           show this help

Exit codes: 0 no drift, 1 drift, 2 input could not be read or parsed.`;

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(2);
}

function readFile(file, label) {
  try {
    return fs.readFileSync(file, 'utf8');
  } catch (err) {
    return fail(`cannot read ${label} (${file}): ${err.code || err.message}`);
  }
}

/** Returns { rows, unparsed } where unparsed lists api.md lines that look like endpoints but do not match. */
function parseApiMd(text) {
  const rows = [];
  const unparsed = [];
  text.split('\n').forEach((line, index) => {
    if (!line.includes('<code title="')) return;
    const match = ROW.exec(line);
    if (!match) {
      unparsed.push({ line: index + 1, text: line.trim().slice(0, 140) });
      return;
    }
    const [, verb, urlPath, accessor, file, method] = match;
    rows.push({ verb, path: urlPath, accessor, method, file });
  });
  return { rows, unparsed };
}

/** Inventory rows are tab-separated: verb, path, accessor (the accessor keeps its trailing dot). */
function parseInventory(text) {
  const rows = [];
  const bad = [];
  text.split('\n').forEach((line, index) => {
    if (line.trim() === '') return;
    const fields = line.split('\t');
    if (fields.length !== 3 || fields.some((f) => f === '')) {
      bad.push({ line: index + 1, text: line.slice(0, 140) });
      return;
    }
    rows.push({ verb: fields[0], path: fields[1], accessor: fields[2] });
  });
  return { rows, bad };
}

const keyOf = (row) => `${row.verb}\t${row.path}\t${row.accessor}`;
// The inventory has no method names, so rows that only come from it show "*" in their place.
const describe = (row) => `${row.verb} ${row.path}  (client.${row.accessor}${row.method || '*'})`;

function countBy(rows) {
  const counts = new Map();
  for (const row of rows) counts.set(keyOf(row), (counts.get(keyOf(row)) || 0) + 1);
  return counts;
}

/** Multiset diff: rows present in `a` more times than in `b`. */
function surplus(aRows, bCounts) {
  const seen = new Map();
  const out = [];
  for (const row of aRows) {
    const key = keyOf(row);
    const used = (seen.get(key) || 0) + 1;
    seen.set(key, used);
    if (used > (bCounts.get(key) || 0)) out.push(row);
  }
  return out;
}

// Same order as the inventory snapshot: path first, then verb (byte order).
const byPathThenVerb = (a, b) =>
  a.path < b.path ? -1
  : a.path > b.path ? 1
  : a.verb < b.verb ? -1
  : a.verb > b.verb ? 1
  : 0;

const STATUS_VOCABULARY = [
  ['spec', 'in the original OpenAPI spec; never run against BandLab from this repo'],
  ['captured', 'seen in a real request capture supplied by the owner'],
  ['unverified', 'inferred or added without evidence'],
  ['live-ok', 'the owner ran it successfully against BandLab'],
  ['missing', 'looked for, not found'],
];

const cell = (text) => String(text).replace(/\|/g, '\\|');
const byAccessorThenPathThenVerb = (a, b) =>
  a.accessor < b.accessor ? -1
  : a.accessor > b.accessor ? 1
  : byPathThenVerb(a, b);

function renderMarkdown(rows, inventoryRows) {
  const known = countBy(inventoryRows);
  const body = rows
    .slice()
    .sort(byAccessorThenPathThenVerb)
    .map((row) => {
      const status = known.has(keyOf(row)) ? 'spec' : 'unverified';
      return { status, row };
    });
  const tally = new Map();
  for (const { status } of body) tally.set(status, (tally.get(status) || 0) + 1);

  const lines = ['# Endpoint Status', ''];
  lines.push(
    'One row per endpoint the SDK exposes, sorted by SDK accessor. Seeded by `./scripts/coverage --markdown` from `api.md`;',
    'after that the **Status** column is edited by hand as evidence arrives. Do not regenerate over a hand-edited file.',
    'To check that `api.md` still matches the inventory snapshot, run `./scripts/coverage`.',
    '',
  );
  lines.push('| Status | Meaning |', '|--------|---------|');
  for (const [name, meaning] of STATUS_VOCABULARY) lines.push(`| \`${name}\` | ${meaning} |`);
  lines.push('');
  const summary = [...tally.entries()].map(([name, n]) => `${n} \`${name}\``).join(', ');
  lines.push(`**${rows.length} endpoints: ${summary}.**`, '');
  lines.push('| Status | Verb | Path | SDK call | Source |', '|--------|------|------|----------|--------|');
  for (const { status, row } of body) {
    const source = row.file.replace(/^\.\//, '');
    lines.push(
      `| \`${status}\` | ${row.verb.toUpperCase()} | \`${cell(row.path)}\` | \`client.${row.accessor}${
        row.method
      }()\` | \`${cell(source)}\` |`,
    );
  }
  lines.push('');
  return lines.join('\n');
}

function main(argv) {
  let apiFile = DEFAULT_API;
  let inventoryFile = DEFAULT_INVENTORY;
  let tsv = false;
  let markdown = false;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '-h' || arg === '--help') {
      console.log(USAGE);
      return 0;
    } else if (arg === '--tsv') {
      tsv = true;
    } else if (arg === '--markdown') {
      markdown = true;
    } else if (arg === '--api' || arg === '--inventory') {
      const value = argv[++i];
      if (!value) return fail(`${arg} needs a file argument`);
      if (arg === '--api') apiFile = path.resolve(value);
      else inventoryFile = path.resolve(value);
    } else {
      return fail(`unknown option: ${arg}\n\n${USAGE}`);
    }
  }

  if (tsv && markdown) return fail('--tsv and --markdown cannot be combined');

  const api = parseApiMd(readFile(apiFile, 'api.md'));
  if (api.unparsed.length > 0) {
    console.error(
      `error: ${api.unparsed.length} line(s) in api.md look like endpoints but could not be parsed:`,
    );
    for (const u of api.unparsed) console.error(`  line ${u.line}: ${u.text}`);
    return 2;
  }
  if (api.rows.length === 0) return fail('no endpoint rows found in api.md');

  if (tsv) {
    for (const row of api.rows.slice().sort(byPathThenVerb)) {
      console.log([row.verb, row.path, row.accessor, row.method, row.file].join('\t'));
    }
    return 0;
  }

  const inventory = parseInventory(readFile(inventoryFile, 'inventory'));
  if (inventory.bad.length > 0) {
    console.error(
      `error: ${inventory.bad.length} malformed line(s) in the inventory (expected 3 tab-separated fields):`,
    );
    for (const b of inventory.bad) console.error(`  line ${b.line}: ${b.text}`);
    return 2;
  }

  if (markdown) {
    process.stdout.write(renderMarkdown(api.rows, inventory.rows));
    return 0;
  }

  const added = surplus(api.rows, countBy(inventory.rows)); // in api.md, not in the inventory
  const removed = surplus(inventory.rows, countBy(api.rows)); // in the inventory, not in api.md

  console.log(`api.md     ${api.rows.length} endpoints  (${path.relative(ROOT, apiFile) || apiFile})`);
  console.log(
    `inventory  ${inventory.rows.length} rows       (${path.relative(ROOT, inventoryFile) || inventoryFile})`,
  );

  if (added.length === 0 && removed.length === 0) {
    console.log('drift      none');
    return 0;
  }

  console.log(`drift      ${added.length + removed.length} difference(s)`);
  for (const row of added.sort(byPathThenVerb))
    console.log(`  + in api.md, not in inventory: ${describe(row)}`);
  for (const row of removed.sort(byPathThenVerb))
    console.log(`  - in inventory, not in api.md: ${describe(row)}`);
  return 1;
}

process.exit(main(process.argv.slice(2)));
