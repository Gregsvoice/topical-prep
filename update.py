"""Collect attributed headlines and prepare cautious radio reads; no API key required."""
import json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCES=[('Capital FM','UK','capitalfm.com'),('BBC Entertainment','UK','bbc.com'),('Official Charts','UK','officialcharts.com'),('KIIS FM','USA','kiisfm.iheart.com'),('Billboard','USA','billboard.com'),('Variety','USA','variety.com'),('People','USA','people.com')]

def category(t):
 t=t.lower()
 if any(x in t for x in ('chart','number one','top 40','billboard 200')):return 'Charts'
 if any(x in t for x in ('tour','concert','festival','tickets','gig','residency')):return 'Tours'
 if any(x in t for x in ('tv','film','movie','netflix','series','celebrity','actor','actress')):return 'Showbiz'
 return 'Music'

def fetch(source,region,domain):
 q=f'site:{domain} (music OR singer OR celebrity OR entertainment OR tour) when:3d'
 url='https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=en-GB&gl=GB&ceid=GB:en'
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; TopicalPrep/2.0)'})
 try:
  with urllib.request.urlopen(req,timeout=18) as response: root=ET.fromstring(response.read())
 except Exception as exc:
  print('Unavailable:',source,exc);return []
 out=[]
 for item in root.findall('.//item')[:15]:
  raw=(item.findtext('title') or '').strip()
  title=re.sub(r'\s+-\s+[^-]+$','',raw).strip()
  link=(item.findtext('link') or '').strip()
  if not title or not link.startswith('https://'):continue
  try: published=parsedate_to_datetime(item.findtext('pubDate')).astimezone(timezone.utc).isoformat()
  except Exception: published=''
  # This is a headline-based read, not an independently verified article summary.
  read=f"According to {source}, {title.rstrip('.!?')}."
  out.append({'title':title,'url':link,'source':source,'region':region,'category':category(title),'published':published,'read10':read,'verification':'Headline-based read; check original article before broadcast.'})
 return out

def main():
 items=[];unavailable=[]
 for source,region,domain in SOURCES:
  result=fetch(source,region,domain)
  if not result:unavailable.append(source)
  items.extend(result)
 seen=set();unique=[]
 for item in sorted(items,key=lambda x:x['published'],reverse=True):
  key=re.sub(r'[^a-z0-9]','',item['title'].lower())[:85]
  if key not in seen:seen.add(key);unique.append(item)
 target=Path(__file__).with_name('news.json')
 if not unique:
  print('No results; preserving last successful edition');return
 now=datetime.now(timezone.utc)
 local=now.astimezone(ZoneInfo('Europe/London'))
 edition='Morning' if local.hour<12 else 'Midday'
 # Three attributed headlines, paced for approximately 30 seconds at radio reading speed.
 selection=unique[:3]
 buzz=' '.join(f"{s['source']} reports: {s['title'].rstrip('.!?')}." for s in selection)
 data={'updatedAt':now.isoformat(),'edition':edition,'timezone':'Europe/London','items':unique[:75], 'buzz30':buzz,'buzzSources':[{'source':s['source'],'url':s['url']} for s in selection], 'unavailableSources':unavailable,'editorialNote':'Presenter scripts are headline-based and attributed. Open the original report and verify facts before broadcast.'}
 target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Published',len(data['items']),'stories for',edition)
if __name__=='__main__':main()
