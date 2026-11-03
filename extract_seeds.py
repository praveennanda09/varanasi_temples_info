# extract_seeds.py
import re
from urllib.parse import urlparse

# The HTML snippet provided by the user in the prompt
nav_html = """
<div class="art-Block-body">
<div class="art-BlockHeader">
    <div class="l"></div>
    <div class="r"></div>
    <div class="art-header-tag-icon">
        <div class="t">Temple Details</div>
    </div>
</div><div class="art-BlockContent">
    <div class="art-BlockContent-body">
<ul id="widget-collapscat-3-top" class="collapsing categories list">
      <li class="collapsing categories item"><a href="https://varanasitemples.in/category/a-introduction/" title="View all posts filed under A. Introduction">A. Introduction</a>      </li> <!-- ending category -->
      <li class="collapsing categories item"><a href="https://varanasitemples.in/category/about-kashi-khand/" title="View all posts filed under About Kashi Khand">About Kashi Khand</a>      </li> <!-- ending category -->
      <li class="collapsing categories item"><a href="https://varanasitemples.in/category/kashi-yatra-performed-by-south-indians/" title="View all posts filed under Kashi Yatra performed by South Indians">Kashi Yatra performed by South Indians</a>      </li> <!-- ending category -->
      <li class="collapsing categories item"><a href="https://varanasitemples.in/category/jyotir-lings/" title="Jyotirlings in Kashi">SHIV LINGS IN KASHI WORSHIPPED AS JYOTIRLINGS</a>      </li> <!-- ending category -->
      <li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/importance-of-river-ganga/" title="View all posts filed under Importance of River Ganga">Importance of River Ganga</a></span>
     <div id="collapsCat-316:3" style="display:block">
<ul><li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/river-ganga/" title="View all posts filed under River Ganga">River Ganga</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/" title="View all posts filed under Important Teerths/Ghats">Important Teerths/Ghats</a></span>
<div id="collapsCat-317:3" style="display:block">
<ul><li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/assi-sangam/" title="View all posts filed under Assi Sangam">Assi Sangam</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/dasaswamedh/" title="View all posts filed under Dasaswamedh">Dasaswamedh</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/gyan-vapi/" title="View all posts filed under Gyan Vapi">Gyan Vapi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/lolark-kund/" title="View all posts filed under Lolark Kund">Lolark Kund</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/manikarnika/" title="View all posts filed under Manikarnika">Manikarnika</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/padodak-teerth/" title="View all posts filed under Padodak Teerth">Padodak Teerth</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/panch-ganga-panch-nada-teerth/" title="View all posts filed under Panch Ganga (Panch Nada Teerth)">Panch Ganga (Panch Nada Teerth)</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/pilpila-teerth/" title="View all posts filed under Pilpila Teerth">Pilpila Teerth</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/varuna-sangam/" title="View all posts filed under Varuna Sangam">Varuna Sangam</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/importance-of-river-ganga/important-teerthsghats/vimal-teerth-pisachmochan/" title="View all posts filed under Vimal Teerth (Pisachmochan)">Vimal Teerth (Pisachmochan)</a>         </li> <!-- ending subcategory -->
</ul>          </div>
         </li> <!-- ending subcategory -->
</ul>        </div>
      </li> <!-- ending category -->
      <li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/aditya-temples/" title="Temples of aditya, or the sun god in varanasi">Aditya Temples</a></span>
     <div id="collapsCat-4:3" style="display:block">
<ul><li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/all-places-of-worship-of-lord-surya-aditya-in-kashi/" title="View all posts filed under All Places of Worship of Lord Surya (Aditya) in Kashi">All Places of Worship of Lord Surya (Aditya) in Kashi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/arun-aditya/" title="View all posts filed under Arun Aditya">Arun Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/draupad-aditya/" title="View all posts filed under Draupad Aditya">Draupad Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/ganga-aditya/" title="View all posts filed under Ganga Aditya">Ganga Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/keshava-aditya/" title="View all posts filed under Keshava Aditya">Keshava Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/khakholkh-aditya/" title="View all posts filed under Khakholkh Aditya">Khakholkh Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/lolark-aditya/" title="View all posts filed under Lolark Aditya">Lolark Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/mayukh-aditya/" title="View all posts filed under Mayukh Aditya">Mayukh Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/saamba-aditya/" title="View all posts filed under Saamba Aditya">Saamba Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/uttarark-aditya/" title="View all posts filed under Uttarark Aditya">Uttarark Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/vimal-aditya/" title="View all posts filed under Vimal Aditya">Vimal Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/vriddh-aditya/" title="View all posts filed under Vriddh Aditya">Vriddh Aditya</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/aditya-temples/yama-aditya/" title="View all posts filed under Yama Aditya">Yama Aditya</a>         </li> <!-- ending subcategory -->
</ul>        </div>
      </li> <!-- ending category -->
      <li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/bhairav-temples/" title="View all posts filed under Bhairav Temples">Bhairav Temples</a></span>
     <div id="collapsCat-14:3" style="display:block">
<ul><li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/kaal-bhairav/" title="View all posts filed under Kaal Bhairav">Kaal Bhairav</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/" title="View all posts filed under Other Bhairav Temples">Other Bhairav Temples</a></span>
<div id="collapsCat-246:3" style="display:block">
<ul><li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/a-brief-about-bhairav-temples/" title="View all posts filed under A Brief about Bhairav Temples">A Brief about Bhairav Temples</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/asitang-bhairav/" title="View all posts filed under Asitang Bhairav">Asitang Bhairav</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/bheeshan-bhairav/" title="View all posts filed under Bheeshan Bhairav">Bheeshan Bhairav</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/chand-bhairav/" title="View all posts filed under Chand Bhairav">Chand Bhairav</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/kapal-bhairav-laat-bhairav/" title="View all posts filed under Kapal Bhairav (Laat Bhairav)">Kapal Bhairav (Laat Bhairav)</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/krodhan-bhairav/" title="View all posts filed under Krodhan Bhairav">Krodhan Bhairav</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/ruru-bhairav/" title="View all posts filed under Ruru Bhairav">Ruru Bhairav</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/samhar-bhairav/" title="View all posts filed under Samhar Bhairav">Samhar Bhairav</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/unmat-bhairav/" title="View all posts filed under Unmat Bhairav">Unmat Bhairav</a>         </li> <!-- ending subcategory -->
</ul>          </div>
         </li> <!-- ending subcategory -->
</ul>        </div>
      </li> <!-- ending category -->
      <li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/devi-temples/" title="View all posts filed under Devi Temples">Devi Temples</a></span>
     <div id="collapsCat-12:3" style="display:block">
<ul><li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/annapurna-devi/" title="View all posts filed under Annapurna Devi">Annapurna Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/bandi-devi/" title="View all posts filed under Bandi Devi">Bandi Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/bhavani-gauri/" title="View all posts filed under Bhavani Gauri">Bhavani Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/brahma-charini-devi/" title="View all posts filed under Brahma Charini Devi">Brahma Charini Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/chamunda-devi/" title="View all posts filed under Chamunda Devi">Chamunda Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/chandi-devi/" title="View all posts filed under Chandi Devi">Chandi Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/charma-munda-devi/" title="View all posts filed under Charma Munda Devi">Charma Munda Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/chitra-ghanta-devi/" title="View all posts filed under Chitra Ghanta Devi">Chitra Ghanta Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/durga-devi-kooshmanda-durga/" title="View all posts filed under Durga Devi (Kooshmanda Durga)">Durga Devi (Kooshmanda Durga)</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/hayakanti-devi/" title="View all posts filed under Hayakanti Devi">Hayakanti Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/jyeshta-gauri/" title="View all posts filed under Jyeshta Gauri">Jyeshta Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/kalratri/" title="View all posts filed under Kalratri">Kalratri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/kamakhya-devi-kamakshi/" title="View all posts filed under Kamakhya Devi (Kamakshi)">Kamakhya Devi (Kamakshi)</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/katyayani/" title="View all posts filed under Katyayani">Katyayani</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/lalitha-gauri/" title="View all posts filed under Lalitha Gauri">Lalitha Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/mahalakshmi-gauri/" title="View all posts filed under Mahalakshmi Gauri">Mahalakshmi Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/mangala-gauri/" title="View all posts filed under Mangala Gauri">Mangala Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/mani-karnika-devi/" title="View all posts filed under Mani Karnika Devi">Mani Karnika Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/mukhnirmalika-gauri/" title="View all posts filed under Mukhnirmalika Gauri">Mukhnirmalika Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/sankata-devi/" title="View all posts filed under Sankata Devi">Sankata Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/shailputri/" title="View all posts filed under Shailputri">Shailputri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/shringar-gauri/" title="View all posts filed under Shringar Gauri">Shringar Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/siddha-lakshmi-devi/" title="View all posts filed under Siddha Lakshmi Devi">Siddha Lakshmi Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/siddheshwari/" title="View all posts filed under Siddheshwari">Siddheshwari</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/skanda-mata/" title="View all posts filed under Skanda Mata">Skanda Mata</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/sowbhagya-gauri/" title="View all posts filed under Sowbhagya Gauri">Sowbhagya Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/tri-lokya-sundary/" title="View all posts filed under Tri Lokya Sundary">Tri Lokya Sundary</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/tripura-bhairavi/" title="View all posts filed under Tripura Bhairavi">Tripura Bhairavi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/varahi-devi/" title="View all posts filed under Varahi Devi">Varahi Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/vindhya-devi/" title="View all posts filed under Vindhya Devi">Vindhya Devi</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/vishalakshi-gauri/" title="View all posts filed under Vishalakshi Gauri">Vishalakshi Gauri</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/devi-temples/vishwa-bhuja-gauri/" title="View all posts filed under Vishwa Bhuja Gauri">Vishwa Bhuja Gauri</a>         </li> <!-- ending subcategory -->
</ul>        </div>
      </li> <!-- ending category -->
      <li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/shiva-temples/" title="Shiva temples in Varanasi">Shiva Temples</a></span>
     <div id="collapsCat-5:3" style="display:block">
<ul><li class="collapsing categories expandable"><span class="collapsing categories collapse"><span class="sym">&#9660;</span><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/" title="View all posts filed under Main Shiva Temples">Main Shiva Temples</a></span>
<div id="collapsCat-35:3" style="display:block">
<ul><li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/atma-veereshwar/" title="View all posts filed under Atma Veereshwar">Atma Veereshwar</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/dharmeshwar/" title="View all posts filed under Dharmeshwar">Dharmeshwar</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/gabhasteeshwar/" title="View all posts filed under Gabhasteeshwar">Gabhasteeshwar</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/kedareshwar/" title="View all posts filed under Kedareshwar">Kedareshwar</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/krithi-vaseshwar/" title="View all posts filed under Krithi Vaseshwar">Krithi Vaseshwar</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/mrityunjay-mahadev/" title="View all posts filed under Mrityunjay Mahadev">Mrityunjay Mahadev</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/omkareshwar/" title="View all posts filed under Omkareshwar">Omkareshwar</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/visweshwar-vishwanath/" title="View all posts filed under Visweshwar (Vishwanath)">Visweshwar (Vishwanath)</a>         </li> <!-- ending subcategory -->
<li class="collapsing categories item"><a href="https://varanasitemples.in/category/shiva-temples/main-shiva-temples/vridha-kalelshwar/" title="View all posts filed under Vridha Kalelshwar">Vridha Kalelshwar</a>         </li> <!-- ending subcategory -->
</ul>          </div>
         </li> <!-- ending subcategory -->
"""

# Let's also extract the other URLs in collapsItems from the prompt text
full_prompt_text = open("extract_seeds.py", "r", encoding="utf-8").read()

# All hrefs in the prompt
hrefs = re.findall(r'href=[\'\"](https://varanasitemples\.in/[^\'\"]+)[\'\"]', nav_html)
print(f"Extracted {len(hrefs)} links from initial block.")
print("Unique:", len(set(hrefs)))
