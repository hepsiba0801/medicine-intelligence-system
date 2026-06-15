import random
import time
import requests

API_URL        = "http://127.0.0.1:8000/medicine"
TOTAL_RECORDS  = 1000
PROGRESS_EVERY = 100

DIST_MEDICINE    = 0.80   # 800 records
DIST_SUSPICIOUS  = 0.10   # 100 records
DIST_NON_MEDICINE = 0.10  # 100 records

MEDICINES = {
    "Antibiotic": [
        "Amoxicillin", "Azithromycin", "Ciprofloxacin", "Doxycycline",
        "Cefixime", "Ceftriaxone", "Metronidazole", "Clindamycin",
        "Erythromycin", "Levofloxacin", "Moxifloxacin", "Ampicillin",
        "Tetracycline", "Trimethoprim", "Sulfamethoxazole", "Nitrofurantoin",
        "Clarithromycin", "Cephalexin", "Cefuroxime", "Linezolid",
        "Vancomycin", "Rifampicin", "Ethambutol", "Isoniazid",
        "Pyrazinamide", "Ofloxacin", "Norfloxacin", "Cefpodoxime",
        "Amoxicillin-Clavulanate", "Piperacillin-Tazobactam",
    ],
    "Antifungal": [
        "Fluconazole", "Itraconazole", "Ketoconazole", "Voriconazole",
        "Amphotericin B", "Terbinafine", "Clotrimazole", "Miconazole",
        "Nystatin", "Caspofungin", "Micafungin", "Anidulafungin",
        "Griseofulvin", "Posaconazole", "Econazole", "Butoconazole",
        "Ciclopirox", "Tolnaftate", "Sertaconazole", "Ravuconazole",
    ],
    "Antiviral": [
        "Acyclovir", "Valacyclovir", "Oseltamivir", "Remdesivir",
        "Lopinavir", "Ritonavir", "Tenofovir", "Emtricitabine",
        "Lamivudine", "Zidovudine", "Abacavir", "Efavirenz",
        "Sofosbuvir", "Ribavirin", "Favipiravir", "Molnupiravir",
        "Famciclovir", "Ganciclovir", "Valganciclovir", "Adefovir",
        "Entecavir", "Telbivudine", "Darunavir", "Atazanavir",
        "Saquinavir", "Indinavir", "Nelfinavir", "Amprenavir",
    ],
    "Analgesic": [
        "Paracetamol", "Ibuprofen", "Diclofenac", "Aspirin",
        "Naproxen", "Indomethacin", "Ketorolac", "Celecoxib",
        "Tramadol", "Morphine", "Codeine", "Oxycodone",
        "Fentanyl", "Buprenorphine", "Nalbuphine", "Pentazocine",
        "Mefenamic Acid", "Piroxicam", "Meloxicam", "Etoricoxib",
        "Flurbiprofen", "Ketoprofen", "Tiaprofenic Acid",
    ],
    "Antipyretic": [
        "Paracetamol", "Ibuprofen", "Aspirin", "Metamizole",
        "Naproxen", "Mefenamic Acid", "Nimesulide", "Diclofenac Sodium",
        "Ketorolac Tromethamine", "Flurbiprofen",
    ],
    "Antihistamine": [
        "Cetirizine", "Levocetirizine", "Fexofenadine", "Loratadine",
        "Desloratadine", "Diphenhydramine", "Chlorpheniramine",
        "Hydroxyzine", "Promethazine", "Azelastine", "Olopatadine",
        "Bilastine", "Rupatadine", "Ebastine", "Mizolastine",
        "Acrivastine", "Terfenadine", "Astemizole", "Mequitazine",
        "Triprolidine", "Brompheniramine", "Doxylamine",
    ],
    "Antidiabetic": [
        "Metformin", "Glimepiride", "Gliclazide", "Glibenclamide",
        "Glipizide", "Pioglitazone", "Rosiglitazone", "Sitagliptin",
        "Vildagliptin", "Saxagliptin", "Alogliptin", "Dapagliflozin",
        "Empagliflozin", "Canagliflozin", "Insulin Glargine",
        "Insulin Aspart", "Insulin Lispro", "Insulin Regular",
        "Liraglutide", "Exenatide", "Dulaglutide", "Semaglutide",
        "Repaglinide", "Nateglinide", "Acarbose", "Miglitol",
    ],
    "Antihypertensive": [
        "Amlodipine", "Telmisartan", "Losartan", "Valsartan",
        "Olmesartan", "Irbesartan", "Enalapril", "Lisinopril",
        "Ramipril", "Captopril", "Perindopril", "Quinapril",
        "Atenolol", "Metoprolol", "Bisoprolol", "Carvedilol",
        "Propranolol", "Nebivolol", "Nifedipine", "Felodipine",
        "Cilnidipine", "Diltiazem", "Verapamil", "Furosemide",
        "Hydrochlorothiazide", "Spironolactone", "Chlorthalidone",
        "Indapamide", "Clonidine", "Prazosin", "Doxazosin",
    ],
    "Antacid": [
        "Omeprazole", "Pantoprazole", "Rabeprazole", "Esomeprazole",
        "Lansoprazole", "Dexlansoprazole", "Ranitidine", "Famotidine",
        "Cimetidine", "Nizatidine", "Magnesium Hydroxide",
        "Aluminium Hydroxide", "Calcium Carbonate", "Sodium Bicarbonate",
        "Sucralfate", "Misoprostol", "Domperidone", "Metoclopramide",
        "Ondansetron", "Granisetron", "Palonosetron",
    ],
    "Vitamin": [
        "Vitamin C", "Vitamin D3", "Vitamin B12", "Vitamin A",
        "Vitamin E", "Vitamin K", "Vitamin B1 (Thiamine)",
        "Vitamin B2 (Riboflavin)", "Vitamin B3 (Niacin)",
        "Vitamin B6", "Vitamin B9 (Folic Acid)", "Vitamin B7 (Biotin)",
        "Multivitamin", "Vitamin D2", "Vitamin B Complex",
    ],
    "Supplement": [
        "Calcium Carbonate", "Zinc Sulphate", "Iron Sulphate",
        "Magnesium Citrate", "Fish Oil", "Omega-3", "Glucosamine",
        "Chondroitin", "Coenzyme Q10", "Alpha Lipoic Acid",
        "Melatonin", "L-Glutamine", "Creatine Monohydrate",
        "Whey Protein", "Collagen Peptide", "Probiotics",
        "Curcumin", "Ashwagandha", "Ginseng Extract", "Lycopene",
        "Lutein", "Zeaxanthin", "Resveratrol", "Spirulina",
    ],
    "Cardiovascular": [
        "Atorvastatin", "Rosuvastatin", "Simvastatin", "Pravastatin",
        "Pitavastatin", "Fluvastatin", "Clopidogrel", "Warfarin",
        "Rivaroxaban", "Apixaban", "Dabigatran", "Digoxin",
        "Amiodarone", "Sotalol", "Flecainide", "Ivabradine",
        "Nitroglycerin", "Isosorbide Dinitrate", "Isosorbide Mononitrate",
    ],
    "Respiratory": [
        "Salbutamol", "Formoterol", "Salmeterol", "Budesonide",
        "Beclomethasone", "Fluticasone", "Tiotropium", "Ipratropium",
        "Montelukast", "Theophylline", "Doxofylline", "Bromhexine",
        "Ambroxol", "Guaifenesin", "Dextromethorphan", "Codeine Phosphate",
        "Acetylcysteine", "Erdosteine",
    ],
    "Antidepressant": [
        "Sertraline", "Fluoxetine", "Escitalopram", "Citalopram",
        "Paroxetine", "Fluvoxamine", "Venlafaxine", "Duloxetine",
        "Mirtazapine", "Bupropion", "Amitriptyline", "Nortriptyline",
        "Clomipramine", "Imipramine", "Trazodone", "Agomelatine",
    ],
    "Antipsychotic": [
        "Risperidone", "Olanzapine", "Quetiapine", "Clozapine",
        "Aripiprazole", "Ziprasidone", "Paliperidone", "Amisulpride",
        "Haloperidol", "Chlorpromazine",
    ],
    "Corticosteroid": [
        "Prednisolone", "Dexamethasone", "Methylprednisolone",
        "Hydrocortisone", "Betamethasone", "Triamcinolone",
        "Fludrocortisone", "Mometasone",
    ],
}

ALL_MEDICINES: list[tuple[str, str]] = [
    (name, category)
    for category, names in MEDICINES.items()
    for name in names
]

SUSPICIOUS_NAMES = [
    # Analgesics / Antipyretics
    "Paracetmol", "Paracetamool", "Paracetamoll", "Parracetamol",
    "Ibuprofn", "Ibupropen", "Ibuprofeen", "Ibuproofen",
    "Aspirn", "Aspirin2", "Asprin", "Aspiren",
    "Diclofenec", "Diclofenack", "Diclofenac2", "Diclofinac",
    "Naproxen2", "Naproxen3", "Naproxn", "Naproxeen",
    # Antibiotics
    "Amoxcillin", "Amoxicilln", "Amoxicilin", "Amoxycillin2",
    "Azithromycn", "Azithrmycin", "Azithromicin", "Azitrhomycin",
    "Ciprofloxacn", "Ciprofloaxcin", "Ciprfloxacin", "Cipro2",
    "Doxycyclne", "Doxycyclin2", "Doxycycilne", "Doxyycline",
    "Cefixim", "Cefixime2", "Cefiximee", "Cefxime",
    "Ceftriaxon", "Ceftriaxone2", "Ceftraixone", "Ceftriaxoone",
    "Metronidazl", "Metronidazole2", "Metronidazol", "Metrnidazole",
    # Antifungals
    "Fluconaazole", "Fluconzole", "Fluconazol", "Fluconazolee",
    "Itraconaazole", "Itraconazol", "Itraconzole", "Itarconazole",
    "Terbinaafine", "Terbinafin", "Terbinafine2", "Terbinafinee",
    # Antihistamines
    "Cetrizine", "Cetirzine", "Cetrizne", "Cetriziine",
    "Levocetirizne", "Levocetrizine", "Levcoetirizine", "Levocetriziine",
    "Fexofenadne", "Fexofenadin", "Fexofenaidne", "Fexofenadien",
    "Lorataadine", "Loratadne", "Loratadinee", "Loratadien",
    # Antidiabetics
    "Metfornin", "Metformn", "Metforni", "Metfrormin",
    "Glimepride", "Glimepirde", "Glimepirdie", "Glimepirid",
    "Sitagliptin2", "Sitagliptn", "Sitaglitin", "Sitagliptni",
    "Dapagliflozn", "Dapaglifozin", "Dapaglflozin", "Dapagliflzoin",
    # Antihypertensives
    "Amlodpine", "Amlodipne", "Amlodipnie", "Amlodiipne",
    "Telmisartn", "Telmisartan2", "Telmisratan", "Telimisartan",
    "Losartn", "Losarrtan", "Losartan2", "Losarrtan",
    "Amlodipine2", "Atenololl", "Metoprrolol", "Bsioprolol",
    "Enalapirl", "Lisinopirl", "Ramipirl", "Captropil",
    # Antacids / PPIs
    "Omeprazol", "Omeprazole2", "Omeprazole3", "Omeprazollee",
    "Pantaprazole", "Pantaprazol", "Pantoprazol2", "Pantoprazollee",
    "Rabeprazol", "Rabeprazole2", "Rabeprazollee", "Rapbeprazole",
    "Esomeprazol", "Esomeprazollee", "Esomeprarzole", "Eomeprazole",
    # Statins
    "Atorvastatin2", "Atrovasatin", "Atorvastatin3", "Atorvastatni",
    "Rosuvasstatin", "Rosuvasatin", "Rosuvastatin2", "Rosuvastatni",
    "Simvasstatin", "Simvasatin", "Simvastatin2", "Simvastatni",
    # Antivirals
    "Acyclovir2", "Acyclovir3", "Acyclvir", "Acycloovir",
    "Oseltamivr", "Oseltamivir2", "Osleltamivir", "Oseltemivir",
    # Vitamins / Supplements
    "Vitamine C", "Vitamin CC", "Vitamine D3", "Vitamin D33",
    "Coenzyme Q110", "Fish Oill", "Omega33", "Probiotcs",
    # Cardiovascular
    "Clopidgrel", "Clopidogerl", "Cloppidogrel", "Warfarin2",
    "Rivaroxabn", "Apixabn", "Dabigatrna", "Digoxin2",
    # Respiratory
    "Salbutamoll", "Salbuttamol", "Formoterol2", "Budesonide2",
    "Monteleukast", "Montelukats", "Theophyllinne", "Ambroxol2",
    # Antidepressants
    "Sertralinne", "Fluoxetinne", "Escitalopram2", "Venlafaxinne",
    "Duloxetinne", "Mirtazapinne", "Bupropion2", "Amitriptylinne",
]

NON_MEDICINES = [
    # Electronics
    "Laptop Samsung", "Apple MacBook", "Dell XPS Laptop", "HP Pavilion",
    "Lenovo ThinkPad", "Asus ROG Laptop", "Acer Aspire",
    "Keyboard Mechanical", "Mouse Wireless", "Mouse Gaming",
    "Monitor LG 24inch", "Monitor Samsung 27inch", "Monitor Ultrawide",
    "Webcam Logitech", "Headphones Sony", "Earphones JBL",
    "Speaker Bluetooth", "Speaker JBL Flip", "Projector Epson",
    "Printer HP LaserJet", "Printer Canon Inkjet", "Scanner Epson",
    "USB Hub 7-Port", "Hard Drive 1TB", "SSD 512GB",
    "Pendrive 64GB", "Memory Card 128GB", "Graphics Card RTX3060",
    "CPU Intel i7", "Motherboard ASUS", "RAM DDR4 16GB",
    "Power Bank 20000mAh", "Charger Type-C", "Cable HDMI",
    "Router WiFi 6", "Modem Cable", "Switch Ethernet",
    "Smartwatch Apple Watch", "Smartwatch Samsung Galaxy",
    "Tablet iPad", "Tablet Samsung", "Kindle E-Reader",
    "Camera DSLR Nikon", "Camera Sony Mirrorless", "Drone DJI",
    "Smart TV 55inch", "Television Samsung OLED",
    # Food & Beverages
    "Chocolate Cadbury", "Chocolate Dark", "Biscuits Oreo",
    "Coffee Nescafe", "Tea Twinings", "Green Tea Lipton",
    "Protein Bar", "Energy Drink Red Bull", "Juice Orange",
    "Mineral Water Bisleri", "Soft Drink Coca Cola",
    "Snack Lays Chips", "Popcorn Microwave", "Honey Dabur",
    "Peanut Butter", "Jam Strawberry", "Bread Whole Wheat",
    "Pasta Barilla", "Noodles Maggi", "Rice Basmati 5kg",
    # Furniture & Household
    "Table Wooden", "Chair Office", "Chair Gaming",
    "Sofa 3-Seater", "Bookshelf Wooden", "Wardrobe Steel",
    "Bed Frame Queen", "Mattress Memory Foam", "Pillow Orthopedic",
    "Curtain Blackout", "Carpet Persian", "Fan Ceiling",
    "Fan Table", "Air Purifier Dyson", "Vacuum Cleaner",
    "Iron Steam", "Washing Machine", "Refrigerator Double Door",
    "Microwave Oven", "Air Fryer", "Blender Mixer",
    "Water Purifier RO", "Induction Cooktop",
    # Fashion & Apparel
    "Shoes Nike Running", "Shoes Adidas", "Shoes Formal Leather",
    "Sandals Bata", "Sneakers Puma", "Sports Shoes Reebok",
    "T-Shirt Cotton", "Jeans Levi's", "Jacket Winter",
    "Sunglasses Ray-Ban", "Watch Casio", "Belt Leather",
    "Bag Backpack", "Handbag Leather", "Wallet Genuine Leather",
    # Office & Stationery
    "Notebook A4", "Pen Blue", "Pencil HB", "Stapler",
    "Calculator Scientific", "Whiteboard", "Marker Permanent",
    "File Folder", "Sticky Notes", "Tape Dispenser",
    # Tech Companies / Brands (misclassified as items)
    "Google Pixel", "Microsoft Surface", "Amazon Echo",
    "Facebook Portal", "Tesla Model S", "Netflix Subscription",
    "Spotify Premium", "Adobe Photoshop", "Microsoft Office",
    "Zoom License", "Slack Workspace", "GitHub Copilot",
    # Miscellaneous
    "Museum Ticket", "Movie Ticket", "Concert Pass",
    "Gym Membership", "Yoga Mat", "Dumbbell 5kg",
    "Football Nike", "Cricket Bat", "Tennis Racket",
    "Playing Cards", "Chess Board", "Rubik's Cube",
    "Lego Set", "Board Game Monopoly", "Puzzle 1000 Pieces",
    "Plant Money Tree", "Pot Ceramic", "Fertilizer Organic",
    "Dog Food Royal Canin", "Cat Food Whiskas",
    "Aquarium Fish Tank", "Bird Cage",
    "Candle Scented", "Perfume Dior", "Deodorant Axe",
    "Shampoo Head Shoulders", "Soap Dove", "Lotion Body",
    "Toothbrush Electric", "Razor Gillette",
    "Bottle Water Stainless", "Lunch Box", "Thermos Flask",
]

def random_quantity() -> int:
    return random.randint(1, 500)

def build_record(name: str | None = None) -> dict:
    payload: dict = {"medicine_name": name, "quantity": random_quantity()}
    return payload

def post_record(session: requests.Session, payload: dict) -> bool:
    try:
        resp = session.post(API_URL, json=payload, timeout=10)
        return resp.status_code in (200, 201)
    except requests.exceptions.RequestException as exc:
        print(f"  ⚠  Request failed: {exc}")
        return False

# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main() -> None:
    random.seed(42)  # reproducible distribution

    # ── Calculate target counts ────────────────
    n_medicines    = int(TOTAL_RECORDS * DIST_MEDICINE)
    n_suspicious   = int(TOTAL_RECORDS * DIST_SUSPICIOUS)
    n_non_medicine = TOTAL_RECORDS - n_medicines - n_suspicious

    print("=" * 60)
    print("  Medicine Intelligence System — Inventory Seeder")
    print("=" * 60)
    print(f"  Target  : {TOTAL_RECORDS:,} records")
    print(f"  Medicines     : {n_medicines:,}  ({DIST_MEDICINE*100:.0f}%)")
    print(f"  Suspicious    : {n_suspicious:,}  ({DIST_SUSPICIOUS*100:.0f}%)")
    print(f"  Non-medicines : {n_non_medicine:,}  ({DIST_NON_MEDICINE*100:.0f}%)")
    print("-" * 60)

    # ── Build work list ────────────────────────
    records: list[tuple[str, str, str]] = []   # (name, category_label, kind)

    # 80% real medicines — draw with replacement from the large pool
    medicine_pool = ALL_MEDICINES  # 250+ (name, category) tuples
    for _ in range(n_medicines):
        name, cat = random.choice(medicine_pool)
        records.append((name, cat, "medicine"))

    # 10% suspicious
    for _ in range(n_suspicious):
        name = random.choice(SUSPICIOUS_NAMES)
        records.append((name, "Unknown", "suspicious"))

    # 10% non-medicine
    for _ in range(n_non_medicine):
        name = random.choice(NON_MEDICINES)
        records.append((name, "Non-Medicine", "non_medicine"))

    # Shuffle so category blocks don't appear in sequence
    random.shuffle(records)

    counters = {"medicine": 0, "suspicious": 0, "non_medicine": 0}
    failures = 0
    start    = time.time()

    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})

    print("\n  Inserting records …\n")

    for i, (name, category, kind) in enumerate(records, start=1):
        payload = build_record(name)
        success = post_record(session, payload)

        if success:
            counters[kind] += 1
        else:
            failures += 1

        if i % PROGRESS_EVERY == 0:
            elapsed  = time.time() - start
            inserted = sum(counters.values())
            rate     = inserted / elapsed if elapsed else 0
            print(
                f"  [{i:>5}/{TOTAL_RECORDS}]  "
                f"inserted={inserted}  failures={failures}  "
                f"rate={rate:.1f} rec/s"
            )

    session.close()
    elapsed   = time.time() - start
    total_ok  = sum(counters.values())

    print("\n" + "=" * 60)
    print("Seeding Complete")
    print("=" * 60)
    print(f"  Total inserted   : {total_ok:,}")
    print(f"  Medicines        : {counters['medicine']:,}")
    print(f"  Suspicious       : {counters['suspicious']:,}")
    print(f"  Non-medicines    : {counters['non_medicine']:,}")
    print(f"  Failures         : {failures:,}")
    print(f"  Elapsed time     : {elapsed:.2f}s")
    print(f"  Avg throughput   : {total_ok/elapsed:.1f} records/sec")
    print("=" * 60)


if __name__ == "__main__":
    main()