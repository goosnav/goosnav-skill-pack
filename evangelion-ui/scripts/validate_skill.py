#!/usr/bin/env python3
"""Validate portable resources without external packages or a browser."""
from pathlib import Path
from html.parser import HTMLParser
import re, sys, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
errors=[]
text=(root/'SKILL.md').read_text()
if not text.startswith('---\n') or '\n---\n' not in text[4:]:errors.append('Missing YAML frontmatter')
if not re.search(r'^name: evangelion-ui$',text,re.M):errors.append('Wrong skill name')
if root.name!='evangelion-ui' and not root.name.startswith('skill-'):errors.append('Directory must be evangelion-ui')
required=['install.sh','install.ps1','install.command','assets/evangelion.css','assets/noise.svg','assets/fonts/BarlowCondensed-Bold.ttf','assets/fonts/OFL.txt','assets/templates/index.html','assets/graphics/primitives.css','assets/inspector.html','assets/inspector.css','assets/inspector.js','references/product-integration.md']
for name in ['operations','analysis','approval','dossier','catalog','process']:
 required.extend(['assets/templates/'+name+'.html','assets/templates/'+name+'.css'])
for rel in required:
 if not (root/rel).is_file():errors.append('Missing '+rel)
def check_link(file,url):
 if url.startswith(('http:','https:','data:','#','mailto:')):return
 target=(file.parent/url.split('#')[0].split('?')[0]).resolve()
 if not target.is_relative_to(root.resolve()) or not target.exists():errors.append(f'{file.relative_to(root)}: broken/escaping reference {url}')
class Links(HTMLParser):
 def __init__(self,file):super().__init__();self.file=file
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('src','href') and v:check_link(self.file,v)
for file in root.rglob('*'):
 if not file.is_file():continue
 if file.suffix=='.html':Links(file).feed(file.read_text())
 if file.suffix=='.css':
  for url in re.findall(r'url\([\'\"]?([^\)\'\"]+)',file.read_text()):check_link(file,url)
 if file.suffix=='.svg':
  try:ET.parse(file)
  except ET.ParseError as e:errors.append(f'{file.name}: {e}')
 if file.suffix=='.md':
  for url in re.findall(r'\]\(([^)]+)\)',file.read_text()):check_link(file,url)

# Check authored preset pairs. This cannot certify contrast after custom tokens,
# analog overlays, browser forced colors, or application-specific backgrounds.
css=(root/'assets/evangelion.css').read_text()
base=re.search(r'\.eva\s*\{([^}]+)\}',css,re.S)
def colors(block):
 return dict(re.findall(r'--eva-([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})',block))
def luminance(hex_value):
 channels=[int(hex_value[i:i+2],16)/255 for i in (1,3,5)]
 linear=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in channels]
 return sum(a*b for a,b in zip(linear,(.2126,.7152,.0722)))
def contrast(a,b):
 x,y=sorted((luminance(a),luminance(b)))
 return (y+.05)/(x+.05)
if not base:
 errors.append('Missing base theme token block')
else:
 defaults=colors(base.group(1))
 palettes={'classic-amber':defaults}
 for name,block in re.findall(r'\.eva\[data-palette="([\w-]+)"\]\s*\{([^}]+)\}',css):
  palettes[name]={**defaults,**colors(block)}
 for name,tokens in palettes.items():
  for foreground in ('text','muted','primary','secondary','warning','danger','success','focus','border'):
   threshold=3 if foreground in ('focus','border') else 4.5
   for background in ('bg','surface'):
    if foreground not in tokens or background not in tokens:
     errors.append(f'{name}: missing contrast token {foreground}/{background}')
    elif contrast(tokens[foreground],tokens[background])<threshold:
     errors.append(f'{name}: {foreground} on {background} is below {threshold}:1')
for err in errors:print('ERROR:',err,file=sys.stderr)
if errors:raise SystemExit(1)
print('PASS: skill metadata, six template pairs, working inspector assets, font/license, local resource links, SVG parsing, and preset token contrast. Composed appearance and platform execution require separate checks.')
