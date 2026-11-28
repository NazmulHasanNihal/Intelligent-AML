import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import robots from '@/app/robots';

function walkSrc(dir: string, exts = new Set(['.ts', '.tsx', '.js', '.jsx', '.css'])): string[] {
  const results: string[] = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walkSrc(full, exts));
    } else if (exts.has(path.extname(entry.name))) {
      results.push(full);
    }
  }
  return results;
}

describe('Static Hygiene, Zero-CDN & Architecture Guardrails', () => {
  const srcDir = path.resolve(__dirname, '..');
  const files = walkSrc(srcDir);

  it('contains zero raw Tailwind hex classes in src/', () => {
    const rawHexRe = /(?:bg|text|border|ring|divide|from|to|via|fill|stroke)-\[#[0-9a-fA-F]+\]/g;
    const offenders: string[] = [];
    for (const f of files) {
      const text = fs.readFileSync(f, 'utf8');
      if (rawHexRe.test(text)) {
        offenders.push(path.relative(srcDir, f));
      }
    }
    expect(offenders).toEqual([]);
  });

  it('contains zero console.log calls, external CDN links, or stray C-STOB typos', () => {
    const offenders: string[] = [];
    const cdnRe = /https?:\/\/(?:fonts\.googleapis\.com|unpkg\.com|cdn\.jsdelivr\.net)/i;
    for (const f of files) {
      if (f.includes('static-hygiene.test.ts')) continue;
      const text = fs.readFileSync(f, 'utf8');
      if (text.includes('console.log(') || cdnRe.test(text) || text.includes('C-STOB')) {
        offenders.push(path.relative(srcDir, f));
      }
    }
    expect(offenders).toEqual([]);
  });

  it('has removed legacy Vite light-theme.css, index.css, tailwind.config.js, and middleware.ts', () => {
    const rootDir = path.resolve(srcDir, '..');
    expect(fs.existsSync(path.join(srcDir, 'styles', 'light-theme.css'))).toBe(false);
    expect(fs.existsSync(path.join(srcDir, 'index.css'))).toBe(false);
    expect(fs.existsSync(path.join(rootDir, 'tailwind.config.js'))).toBe(false);
    expect(fs.existsSync(path.join(srcDir, 'middleware.ts'))).toBe(false);
    expect(fs.existsSync(path.join(srcDir, 'proxy.ts'))).toBe(true);
  });

  it('disallows /api/ and /styleguide in robots.txt while keeping /, /governance, and /app crawlable', () => {
    const bot = robots();
    const rule = Array.isArray(bot.rules) ? bot.rules[0]! : bot.rules;
    expect(rule.disallow).toContain('/api/');
    expect(rule.disallow).toContain('/styleguide');
    expect(rule.allow).toContain('/');
    expect(rule.allow).toContain('/governance');
    expect(rule.allow).toContain('/app');
  });
});
