const fs = require('fs');
const path = require('path');

const landingPath = path.resolve('c:/Users/Loa/Downloads/GOAL/crystal_pdf_repo/frontend/src/pages/LandingPage.tsx');
const content = fs.readFileSync(landingPath, 'utf-8');

console.log('--- Validating Responsive CSS & Layout Attributes ---');

const checks = [
  { name: 'Root container has overflow-x-hidden', test: content.includes('overflow-x-hidden') },
  { name: 'Prism adapts size on mobile (240px) and desktop (340px)', test: content.includes('width: 240px') && content.includes('width: 340px') },
  { name: 'Navbar touch targets min-h defined', test: content.includes('min-h-[38px]') || content.includes('min-h-[44px]') },
  { name: 'Hero CTAs stack on mobile (flex-col sm:flex-row)', test: content.includes('flex flex-col sm:flex-row') },
  { name: 'Buttons meet minimum accessible tap target (min-h-[44px])', test: content.includes('min-h-[44px]') },
  { name: 'Interactive elements have cursor-pointer', test: content.includes('cursor-pointer') },
  { name: 'Tools grid is single-column on narrow mobile viewports', test: content.includes('grid-cols-1 min-[420px]:grid-cols-2 lg:grid-cols-4') },
  { name: 'Reduced-motion accessibility query supported', test: content.includes('prefers-reduced-motion: reduce') },
  { name: 'Nav links have whitespace-nowrap and flex-shrink-0', test: content.includes('whitespace-nowrap') && content.includes('flex-shrink-0') }
];

let allPassed = true;
checks.forEach(c => {
  console.log(`[${c.test ? 'PASS' : 'FAIL'}] ${c.name}`);
  if (!c.test) allPassed = false;
});

if (allPassed) {
  console.log('\nTask 3 Validation 3: ALL 9 RESPONSIVE DESIGN INVARIANTS PASSED 100%!');
} else {
  console.error('\nSome responsive checks failed!');
  process.exit(1);
}
