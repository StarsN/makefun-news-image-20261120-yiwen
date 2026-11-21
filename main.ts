// THE WORLD — 20 November 2026 front page.
//
// Entry program for make.fun news-image-20261120. It ships the finished
// front page (entry.png, composed by compose.py from three illustrations
// generated for this entry) and copies it, byte for byte, to the output
// directory the grader provides. No network, no randomness: every run
// writes the same bytes.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
// Fail loudly instead of shipping a truncated copy: the grader runs the
// program twice and both runs must write the same bytes.
const inSize = statSync(source).size;
const outSize = statSync(target).size;
if (inSize !== outSize) {
  throw new Error(`entry.png copy mismatch: ${inSize} vs ${outSize} bytes`);
}
console.log(`wrote ${target} (${outSize} bytes)`);
