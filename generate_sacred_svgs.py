# generate_sacred_svgs.py
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

img_dir = 'Kashi_Exact_Offline_Website/assets/images'
os.makedirs(img_dir, exist_ok=True)

# Also create root assets/images if it exists or create it
root_img_dir = 'assets/images'
os.makedirs(root_img_dir, exist_ok=True)

svgs = {
    'Varahi-Devi-Shrine.svg': {
        'title': 'Varahi Devi Sanctum',
        'hindi': 'वाराही देवी • Kashi Varahi Devi',
        'sub': 'Sacred Commander Matrika of Lalita • Ruler of the Kashi Night',
        'bg1': '#1e1b4b', 'bg2': '#431407', 'accent': '#f59e0b', 'motif_color': '#fbbf24',
        'icon': '''
            <!-- Crown & Moon -->
            <path d="M400 150 L420 190 L460 195 L430 220 L440 260 L400 235 L360 260 L370 220 L340 195 L380 190 Z" fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
            <path d="M380 135 A25 25 0 0 1 420 135 A30 30 0 0 0 380 135" fill="#fef3c7"/>
            <!-- Boar Face Silhouette -->
            <ellipse cx="400" cy="285" rx="75" ry="60" fill="#312e81" stroke="#fbbf24" stroke-width="4"/>
            <!-- Snout -->
            <ellipse cx="400" cy="305" rx="35" ry="25" fill="#1e1b4b" stroke="#fbbf24" stroke-width="3"/>
            <circle cx="388" cy="305" r="5" fill="#fbbf24"/>
            <circle cx="412" cy="305" r="5" fill="#fbbf24"/>
            <!-- Tusks -->
            <path d="M365 315 Q355 285 365 270 Q370 290 375 315 Z" fill="#fef3c7" stroke="#fbbf24" stroke-width="2"/>
            <path d="M435 315 Q445 285 435 270 Q430 290 425 315 Z" fill="#fef3c7" stroke="#fbbf24" stroke-width="2"/>
            <!-- Eyes (Third Eye & Radiant Gaze) -->
            <ellipse cx="375" cy="265" rx="12" ry="7" fill="#fbbf24"/>
            <ellipse cx="425" cy="265" rx="12" ry="7" fill="#fbbf24"/>
            <circle cx="375" cy="265" r="4" fill="#451a03"/>
            <circle cx="425" cy="265" r="4" fill="#451a03"/>
            <ellipse cx="400" cy="245" rx="6" ry="12" fill="#ef4444" stroke="#fbbf24" stroke-width="2"/>
            <!-- Sacred Danda & Hala -->
            <line x1="280" y1="200" x2="320" y2="380" stroke="#fbbf24" stroke-width="6" stroke-linecap="round"/>
            <line x1="520" y1="200" x2="480" y2="380" stroke="#fbbf24" stroke-width="6" stroke-linecap="round"/>
            <circle cx="280" cy="200" r="14" fill="#d97706" stroke="#fbbf24" stroke-width="3"/>
        '''
    },
    'Tri-Lokya-Sundary-Shrine.svg': {
        'title': 'Tri Lokya Sundari Sanctum',
        'hindi': 'त्रिलोक्य सुन्दरी • Kashi Tri Lokya Sundari',
        'sub': 'Supreme Sovereign of the Three Worlds • Sri Vidya Lalita',
        'bg1': '#4c0519', 'bg2': '#881337', 'accent': '#f43f5e', 'motif_color': '#fde047',
        'icon': '''
            <!-- Sri Yantra Outer Petals -->
            <g transform="translate(400,280)">
              <circle cx="0" cy="0" r="130" fill="none" stroke="#fde047" stroke-width="3" stroke-dasharray="8 6"/>
              <circle cx="0" cy="0" r="115" fill="#9f1239" stroke="#fbbf24" stroke-width="4"/>
              <!-- Interlocking Sacred Triangles -->
              <polygon points="0,-90 78,45 -78,45" fill="none" stroke="#fde047" stroke-width="4"/>
              <polygon points="0,90 78,-45 -78,-45" fill="none" stroke="#fde047" stroke-width="4"/>
              <polygon points="0,-70 60,35 -60,35" fill="none" stroke="#fca5a5" stroke-width="3"/>
              <polygon points="0,70 60,-35 -60,-35" fill="none" stroke="#fca5a5" stroke-width="3"/>
              <polygon points="0,-50 45,25 -45,25" fill="none" stroke="#fef08a" stroke-width="3"/>
              <polygon points="0,50 45,-25 -45,-25" fill="none" stroke="#fef08a" stroke-width="3"/>
              <!-- Central Bindu -->
              <circle cx="0" cy="0" r="12" fill="#fde047" stroke="#dc2626" stroke-width="3"/>
            </g>
            <!-- Sugarcane Bow & Floral Arrows -->
            <path d="M250 180 Q220 280 250 380" fill="none" stroke="#22c55e" stroke-width="6" stroke-linecap="round"/>
            <path d="M550 180 Q580 280 550 380" fill="none" stroke="#22c55e" stroke-width="6" stroke-linecap="round"/>
        '''
    },
    'Dhundhi-Vinayak-Shrine.svg': {
        'title': 'Dhundhi Vinayak Sanctum',
        'hindi': 'ढूंढि विनायक • Kashi Dhundhi Vinayak',
        'sub': 'Primordial Gatekeeper of Vishweshwar • First Worshipped in Kashi',
        'bg1': '#7c2d12', 'bg2': '#c2410c', 'accent': '#fbbf24', 'motif_color': '#fef08a',
        'icon': '''
            <!-- Ganesha Silhouette -->
            <g transform="translate(400,270)">
              <!-- Ears -->
              <ellipse cx="-85" cy="-20" rx="45" ry="60" fill="#9a3412" stroke="#fef08a" stroke-width="4"/>
              <ellipse cx="85" cy="-20" rx="45" ry="60" fill="#9a3412" stroke="#fef08a" stroke-width="4"/>
              <!-- Crown / Mukut -->
              <path d="M-40 -70 L0 -140 L40 -70 Z" fill="#fbbf24" stroke="#d97706" stroke-width="4"/>
              <circle cx="0" cy="-145" r="8" fill="#ef4444"/>
              <!-- Head & Cheeks -->
              <ellipse cx="0" cy="-10" rx="65" ry="60" fill="#ea580c" stroke="#fef08a" stroke-width="4"/>
              <!-- Trishula Tilak & Third Eye -->
              <path d="M-15 -45 L0 -20 L15 -45 L0 -65 Z" fill="#fef08a"/>
              <circle cx="0" cy="-35" r="5" fill="#dc2626"/>
              <!-- Eyes -->
              <ellipse cx="-30" cy="-15" rx="8" ry="4" fill="#fff"/>
              <circle cx="-30" cy="-15" r="3" fill="#000"/>
              <ellipse cx="30" cy="-15" rx="8" ry="4" fill="#fff"/>
              <circle cx="30" cy="-15" r="3" fill="#000"/>
              <!-- Trunk Sweeping Left to Modaka -->
              <path d="M-12 15 Q-15 75 -45 80 Q-70 85 -75 60 Q-80 40 -60 40 Q-45 42 -40 60 Q-30 65 -15 35 Q-5 15 12 15" fill="#c2410c" stroke="#fef08a" stroke-width="4"/>
              <!-- Modaka (Laddoo) -->
              <circle cx="-65" cy="45" r="14" fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
              <!-- Ekadanta Single Tusk -->
              <path d="M22 20 L35 45 L26 47 Z" fill="#fff" stroke="#fef08a" stroke-width="2"/>
            </g>
        '''
    },
    'Siddhi-Vinayak-Shrine.svg': {
        'title': 'Siddhi Vinayak Sanctum',
        'hindi': 'सिद्धि विनायक • Kashi Siddhi Vinayak',
        'sub': 'Bestower of Spiritual Accomplishment & Supreme Success',
        'bg1': '#831843', 'bg2': '#be185d', 'accent': '#f472b6', 'motif_color': '#fde047',
        'icon': '''
            <!-- Radiant Aura -->
            <g transform="translate(400,270)">
              <circle cx="0" cy="0" r="130" fill="none" stroke="#fde047" stroke-width="3" stroke-dasharray="10 6"/>
              <!-- Ears -->
              <ellipse cx="-85" cy="-20" rx="45" ry="60" fill="#9d174d" stroke="#fde047" stroke-width="4"/>
              <ellipse cx="85" cy="-20" rx="45" ry="60" fill="#9d174d" stroke="#fde047" stroke-width="4"/>
              <!-- Crown -->
              <path d="M-40 -70 L0 -140 L40 -70 Z" fill="#fde047" stroke="#b45309" stroke-width="4"/>
              <circle cx="0" cy="-145" r="9" fill="#ef4444"/>
              <!-- Face -->
              <ellipse cx="0" cy="-10" rx="65" ry="60" fill="#db2777" stroke="#fde047" stroke-width="4"/>
              <!-- Tripundra Tilak -->
              <line x1="-20" y1="-45" x2="20" y2="-45" stroke="#fef08a" stroke-width="3"/>
              <line x1="-20" y1="-38" x2="20" y2="-38" stroke="#fef08a" stroke-width="3"/>
              <circle cx="0" cy="-41" r="4" fill="#dc2626"/>
              <!-- Trunk Right-curled (Siddhi Vinayak is typically Valampuri / Right-curled) -->
              <path d="M12 15 Q15 75 45 80 Q70 85 75 60 Q80 40 60 40 Q45 42 40 60 Q30 65 15 35 Q5 15 -12 15" fill="#be185d" stroke="#fde047" stroke-width="4"/>
              <!-- Modaka -->
              <circle cx="65" cy="45" r="14" fill="#fde047" stroke="#d97706" stroke-width="3"/>
              <!-- Left Tusk -->
              <path d="M-22 20 L-35 45 L-26 47 Z" fill="#fff" stroke="#fde047" stroke-width="2"/>
            </g>
        '''
    },
    'Avi-Mukta-Vinayak-Shrine.svg': {
        'title': 'Avi Mukta Vinayak Sanctum',
        'hindi': 'अविमुक्त विनायक • Kashi Avi Mukta Vinayak',
        'sub': 'Eternal Guardian of the Never-Forsaken Sacred Kshetra',
        'bg1': '#1c1917', 'bg2': '#44403c', 'accent': '#e7e5e4', 'motif_color': '#fbbf24',
        'icon': '''
            <!-- Crescent Moon & Shivaite Trishula halo -->
            <g transform="translate(400,270)">
              <circle cx="0" cy="0" r="130" fill="none" stroke="#fbbf24" stroke-width="3" stroke-dasharray="12 6"/>
              <path d="M-40 -110 Q0 -135 40 -110 Q20 -150 -40 -110" fill="#fef08a"/>
              <!-- Ears -->
              <ellipse cx="-85" cy="-20" rx="45" ry="60" fill="#292524" stroke="#fbbf24" stroke-width="4"/>
              <ellipse cx="85" cy="-20" rx="45" ry="60" fill="#292524" stroke="#fbbf24" stroke-width="4"/>
              <!-- Crown -->
              <path d="M-35 -70 L0 -130 L35 -70 Z" fill="#fbbf24" stroke="#78350f" stroke-width="4"/>
              <!-- Face -->
              <ellipse cx="0" cy="-10" rx="65" ry="60" fill="#57534e" stroke="#fbbf24" stroke-width="4"/>
              <!-- Sacred Bhasma Tripundra -->
              <line x1="-25" y1="-45" x2="25" y2="-45" stroke="#f5f5f4" stroke-width="4"/>
              <line x1="-25" y1="-38" x2="25" y2="-38" stroke="#f5f5f4" stroke-width="4"/>
              <line x1="-25" y1="-31" x2="25" y2="-31" stroke="#f5f5f4" stroke-width="4"/>
              <circle cx="0" cy="-38" r="4" fill="#dc2626"/>
              <!-- Trunk -->
              <path d="M-12 15 Q-15 75 -45 80 Q-70 85 -75 60 Q-80 40 -60 40 Q-45 42 -40 60 Q-30 65 -15 35 Q-5 15 12 15" fill="#44403c" stroke="#fbbf24" stroke-width="4"/>
              <circle cx="-65" cy="45" r="14" fill="#fbbf24" stroke="#b45309" stroke-width="3"/>
            </g>
        '''
    },
    'Gyan-Madhav-Shrine.svg': {
        'title': 'Gyan Madhav Sanctum',
        'hindi': 'ज्ञान माधव • Kashi Gyan Madhav',
        'sub': 'Bestower of Spiritual Wisdom • Among the Sacred Pancha Madhavas',
        'bg1': '#0f172a', 'bg2': '#1e3a8a', 'accent': '#38bdf8', 'motif_color': '#fde047',
        'icon': '''
            <!-- Sudarshana & Shankha Emblems -->
            <g transform="translate(400,265)">
              <circle cx="0" cy="0" r="125" fill="none" stroke="#fde047" stroke-width="3" stroke-dasharray="14 6"/>
              <!-- Central Vishnu Tilak (Urdhva Pundra) -->
              <path d="M-30 -90 L-10 10 L0 30 L10 10 L30 -90 L12 -90 L0 -40 L-12 -90 Z" fill="#fff" stroke="#fde047" stroke-width="3"/>
              <path d="M-4 -70 L-4 5 L4 5 L4 -70 Z" fill="#dc2626"/>
              <!-- Lotus Base -->
              <path d="M-90 80 Q0 30 90 80 Q50 120 0 110 Q-50 120 -90 80 Z" fill="#f43f5e" stroke="#fde047" stroke-width="3"/>
              <!-- Shankha (Conch) Left -->
              <g transform="translate(-100,-20) scale(0.6)">
                <ellipse cx="0" cy="0" rx="35" ry="50" fill="#f8fafc" stroke="#fde047" stroke-width="4"/>
                <path d="M-15 -40 Q15 0 -15 40" fill="none" stroke="#94a3b8" stroke-width="4"/>
              </g>
              <!-- Sudarshana Chakra Right -->
              <g transform="translate(100,-20) scale(0.6)">
                <circle cx="0" cy="0" r="45" fill="none" stroke="#fde047" stroke-width="6"/>
                <circle cx="0" cy="0" r="15" fill="#fde047"/>
                <line x1="-45" y1="0" x2="45" y2="0" stroke="#fde047" stroke-width="4"/>
                <line x1="0" y1="-45" x2="0" y2="45" stroke="#fde047" stroke-width="4"/>
              </g>
            </g>
        '''
    },
    'Gopi-Govind-Shrine.svg': {
        'title': 'Gopi Govind Sanctum',
        'hindi': 'गोपी गोविन्द • Kashi Gopi Govind',
        'sub': 'Lord Govinda • Beloved Protector of Devotees & Holy Surabhi Cows',
        'bg1': '#064e3b', 'bg2': '#047857', 'accent': '#34d399', 'motif_color': '#fde047',
        'icon': '''
            <!-- Divine Flute & Peacock Feather Motif -->
            <g transform="translate(400,265)">
              <circle cx="0" cy="0" r="125" fill="none" stroke="#fde047" stroke-width="3" stroke-dasharray="10 8"/>
              <!-- Mor Pankh (Peacock Feather) -->
              <ellipse cx="0" cy="-60" rx="35" ry="55" fill="#0284c7" stroke="#fde047" stroke-width="3"/>
              <ellipse cx="0" cy="-60" rx="22" ry="35" fill="#047857" stroke="#fde047" stroke-width="2"/>
              <ellipse cx="0" cy="-60" rx="10" ry="18" fill="#1e1b4b" stroke="#fde047" stroke-width="2"/>
              <circle cx="0" cy="-60" r="5" fill="#fde047"/>
              <!-- Divine Bansuri (Flute) -->
              <line x1="-120" y1="30" x2="120" y2="-10" stroke="#fbbf24" stroke-width="10" stroke-linecap="round"/>
              <circle cx="-60" cy="20" r="3" fill="#78350f"/>
              <circle cx="-30" cy="15" r="3" fill="#78350f"/>
              <circle cx="0" cy="10" r="3" fill="#78350f"/>
              <circle cx="30" cy="5" r="3" fill="#78350f"/>
              <circle cx="60" cy="0" r="3" fill="#78350f"/>
              <!-- Sacred Cow Silhouette Emblem Base -->
              <path d="M-80 90 Q0 60 80 90 Q40 120 0 115 Q-40 120 -80 90 Z" fill="#fef08a" stroke="#b45309" stroke-width="3"/>
            </g>
        '''
    },
    'Vitank-Narsimha-Shrine.svg': {
        'title': 'Vitank Narsimha Sanctum',
        'hindi': 'विटंक नरसिंह • Kashi Vitank Narsimha',
        'sub': 'Fierce Divine Protector • Dispeller of Demonic Perils & Fears',
        'bg1': '#7f1d1d', 'bg2': '#b91c1c', 'accent': '#f87171', 'motif_color': '#fef08a',
        'icon': '''
            <!-- Fiery Mane & Lion Crown Silhouette -->
            <g transform="translate(400,265)">
              <circle cx="0" cy="0" r="130" fill="none" stroke="#fef08a" stroke-width="4" stroke-dasharray="12 6"/>
              <!-- Sunburst Flames -->
              <path d="M0 -140 L20 -115 L40 -135 L45 -105 L75 -115 L65 -90 L95 -90 L75 -65 L105 -55 L80 -35 L105 -15 L75 0 L100 20 L70 30 L85 55 L55 60 L65 85 L35 80 L35 110 L10 95 L-10 95 L-35 110 L-35 80 L-65 85 L-55 60 L-85 55 L-70 30 L-100 20 L-75 0 L-105 -15 L-80 -35 L-105 -55 L-75 -65 L-95 -90 L-65 -90 L-75 -115 L-45 -105 L-40 -135 L-20 -115 Z" fill="#ea580c" stroke="#fef08a" stroke-width="3"/>
              <!-- Crown -->
              <path d="M-35 -80 L0 -135 L35 -80 Z" fill="#fef08a" stroke="#b45309" stroke-width="3"/>
              <!-- Face of the Man-Lion -->
              <ellipse cx="0" cy="-10" rx="55" ry="55" fill="#991b1b" stroke="#fef08a" stroke-width="4"/>
              <!-- Fierce Eyes -->
              <ellipse cx="-25" cy="-20" rx="12" ry="7" fill="#fef08a"/>
              <ellipse cx="25" cy="-20" rx="12" ry="7" fill="#fef08a"/>
              <circle cx="-25" cy="-20" r="5" fill="#000"/>
              <circle cx="25" cy="-20" r="5" fill="#000"/>
              <circle cx="0" cy="-35" r="6" fill="#fef08a"/>
              <!-- Muzzle & Fangs -->
              <path d="M-25 10 Q0 -5 25 10 Q0 35 -25 10 Z" fill="#7f1d1d" stroke="#fef08a" stroke-width="3"/>
              <polygon points="-15,15 -10,32 -6,15" fill="#fff"/>
              <polygon points="15,15 10,32 6,15" fill="#fff"/>
            </g>
        '''
    }
}

template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <radialGradient id="auraGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{motif_color}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{motif_color}" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="800" height="500" rx="12" fill="url(#bgGrad)"/>
  
  <!-- Outer Ornate Border -->
  <rect x="18" y="18" width="764" height="464" rx="8" fill="none" stroke="{accent}" stroke-width="2" opacity="0.6"/>
  <rect x="26" y="26" width="748" height="448" rx="6" fill="none" stroke="{motif_color}" stroke-width="1.5" stroke-dasharray="10 6" opacity="0.8"/>

  <!-- Corner Mandalas -->
  <g fill="{motif_color}" opacity="0.7">
    <circle cx="36" cy="36" r="6"/>
    <circle cx="764" cy="36" r="6"/>
    <circle cx="36" cy="464" r="6"/>
    <circle cx="764" cy="464" r="6"/>
  </g>

  <!-- Radiant Aura -->
  <circle cx="400" cy="265" r="180" fill="url(#auraGrad)"/>

  <!-- Deity Sacred Emblem -->
  {icon}

  <!-- Header Banner -->
  <g transform="translate(400, 50)" text-anchor="middle">
    <text y="0" font-family="'Segoe UI', Roboto, 'Noto Sans Devanagari', Arial, sans-serif" font-size="24" font-weight="bold" fill="{motif_color}" filter="url(#glow)">{hindi}</text>
    <text y="24" font-family="'Segoe UI', Roboto, Arial, sans-serif" font-size="13" font-weight="600" fill="#e2e8f0" letter-spacing="1">{sub}</text>
  </g>

  <!-- Authentic Provenance Notice Footer -->
  <g transform="translate(400, 455)" text-anchor="middle">
    <rect x="-260" y="-18" width="520" height="26" rx="13" fill="#000" opacity="0.55"/>
    <text y="-1" font-family="'Segoe UI', Roboto, Arial, sans-serif" font-size="11.5" fill="#fef08a" font-weight="500">
      &#128330; Sacred Kashi Scriptural Iconography &bull; varanasitemples.in Knowledge Base
    </text>
  </g>
</svg>
"""

for fname, d in svgs.items():
    content = template.format(
        bg1=d['bg1'],
        bg2=d['bg2'],
        accent=d['accent'],
        motif_color=d['motif_color'],
        icon=d['icon'],
        hindi=d['hindi'],
        sub=d['sub']
    )
    # Save in Kashi_Exact_Offline_Website/assets/images/
    p1 = os.path.join(img_dir, fname)
    with open(p1, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Save in root assets/images/
    p2 = os.path.join(root_img_dir, fname)
    with open(p2, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Generated: {fname} ({len(content)} bytes)")

print("\nSUCCESS! All 8 sacred deity illustrations generated successfully.")
