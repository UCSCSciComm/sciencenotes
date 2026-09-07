#!/usr/bin/env python3
"""
fix_domain_links.py

Fixes bare-domain references in a static export of ucscsciencenotes.com
(generated via wget --mirror ... from the temporary Bluehost URL).

- Any href/link pointing to the BARE domain https://ucscsciencenotes.com
  (with or without www., with or without a trailing slash, and NOT followed
  by a path) is rewritten to a relative link to the site's top-level index.html.
  Links that include a path (e.g. https://ucscsciencenotes.com/some-article/)
  are left untouched.

- Any href/link pointing to the BARE domain https://sciencenotes.ucsc.edu
  is rewritten to the Wayback Machine snapshot URL below.

Run this from the root of the exported static site (the folder containing
the top-level index.html).

Usage:
    python3 fix_domain_links.py
"""

import re
import os
import glob

files = glob.glob('**/*.html', recursive=True)

# Matches ONLY the bare domain, optionally with a trailing slash,
# and only when NOT followed by a path character (so /some-article stays untouched)
ucsn_pattern = re.compile(r'https?://(?:www\.)?ucscsciencenotes\.com/?(?=["\'\s)>])')
scicom_pattern = re.compile(r'https?://(?:www\.)?sciencenotes\.ucsc\.edu/?(?=["\'\s)>])')

wayback_url = 'https://web.archive.org/web/20250526084758/https://sciencenotes.ucsc.edu/'

updated_count = 0

for fp in files:
    depth = fp.count(os.sep)
    root_link = ('../' * depth + 'index.html') if depth > 0 else 'index.html'

    with open(fp, encoding='utf-8', errors='ignore') as f:
        content = f.read()

    new_content = ucsn_pattern.sub(root_link, content)
    new_content = scicom_pattern.sub(wayback_url, new_content)

    if new_content != content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated: {fp}  (root -> {root_link})')
        updated_count += 1

print(f'\nDone. {updated_count} file(s) updated.')
print('\nVerify with:')
print('  grep -rl "ucscsciencenotes.com" .')
print('  grep -rl "sciencenotes.ucsc.edu" . | grep -v "web.archive.org"')
print('Both should come back empty (aside from the wayback URL itself for the second check).')