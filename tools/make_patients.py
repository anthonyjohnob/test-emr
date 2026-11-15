"""Generates data/patients.json: 100 FICTIONAL retina patients for the test EMR.
Every name, date, number and record is invented. Re-running gives the same patients (fixed seed)."""
import json
import random
from datetime import date, timedelta
from pathlib import Path

rnd = random.Random(20261115)
FIRST = ["Adelina", "Barnaby", "Cordelia", "Desmond", "Elowen", "Fitzgerald", "Gwendolyn", "Horatio", "Imogen", "Jasper",
         "Kerensa", "Lysander", "Marigold", "Nathaniel", "Ottoline", "Percival", "Quintessa", "Roderick", "Saoirse",
         "Thaddeus", "Ursula", "Valentin", "Wilhelmina", "Xavier", "Yolanda", "Zebulon", "Annora", "Bertram", "Calliope",
         "Dorian", "Esmeralda", "Florian", "Genevieve", "Hollis", "Isadora", "Jethro", "Kristiana", "Leopold", "Maelis",
         "Norbert", "Odessa", "Peregrine", "Rosalind", "Silvester", "Tamsin", "Ulysses", "Verity", "Winifred", "Ambrose",
         "Beatrix"]
LAST = ["Ashcombe", "Blackwood", "Calloway", "Dunmore", "Ellsworth", "Fairbanks", "Greystone", "Hollingsworth", "Ingleby",
        "Jessop", "Kittredge", "Lockhart", "Merriweather", "Northcott", "Oakhurst", "Pemberton", "Quarrington", "Ravensworth",
        "Stanwick", "Thistlewood", "Underhill", "Vandermeer", "Whitlock", "Yarborough", "Zellweger", "Abernathy",
        "Brightwater", "Cresswell", "Dewhurst", "Esterbrook", "Fenwick", "Gallagher-Shore", "Harrowgate", "Ironside",
        "Juniper", "Kestrel", "Larkspur", "Montgomery-Hale", "Nettlefield", "O'Halloran", "Penhallow", "Rookwood",
        "Silverthorne", "Trelawney", "Upton-Clyde", "Verlaine", "Wexford", "Yardley", "de la Fontaine", "St. Clair"]
PAYERS = [("Sunrise Health Plan (test)", "SHP"), ("Bayline Medicare Advantage (test)", "BMA"),
          ("Coastal Medicaid (test)", "CMD"), ("Keystone Commercial PPO (test)", "KCP"), ("Harborview Health (test)", "HVH")]
DOCS = ["Dr. Lena Marsh (test)", "Dr. Rowan Castell (test)", "Dr. Imani Okoye (test)"]
PCPS = ["Dr. Felix Brandt (test)", "Dr. Nora Lindqvist (test)", "Dr. Omar Haddad (test)", "Dr. June Whitaker (test)"]
EYE_WORD = {"1": "OD", "2": "OS", "3": "OU"}
# (description, code template with {e} = laterality digit, treated with anti-VEGF?)
DX = [("Exudative age-related macular degeneration, with active choroidal neovascularization", "H35.32{e}1", True),
      ("Type 2 diabetes with proliferative diabetic retinopathy with macular edema", "E11.351{e}", True),
      ("Type 2 diabetes with moderate nonproliferative diabetic retinopathy with macular edema", "E11.331{e}", True),
      ("Branch retinal vein occlusion with macular edema", "H34.83{e}0", True),
      ("Central retinal vein occlusion with macular edema", "H34.81{e}0", True),
      ("Nonexudative AMD, advanced atrophic with subfoveal involvement (geographic atrophy)", "H35.31{e}4", False)]
DRUGS = {True: [("Eylea (aflibercept)", "J0178"), ("Eylea HD (aflibercept 8 mg)", "J0177"), ("Vabysmo (faricimab-svoa)", "J2777"),
                ("Lucentis (ranibizumab)", "J2778"), ("Avastin (bevacizumab)", "J9035"), ("Byooviz (ranibizumab-nuna)", "Q5124"),
                ("Cimerli (ranibizumab-eqrn)", "Q5128")],
         False: [("Syfovre (pegcetacoplan)", "J2781"), ("Izervay (avacincaptad pegol)", "J2782")]}
OTHER_DX = [("Pseudophakia", "Z96.1"), ("Primary open-angle glaucoma, mild", "H40.11X1"), ("Dry eye syndrome", "H04.123"),
            ("Nuclear cataract", "H25.13"), ("Posterior vitreous detachment", "H43.813")]
SYS_MEDS = ["Metformin 1000 mg twice daily", "Lisinopril 10 mg daily", "Atorvastatin 40 mg nightly", "Insulin glargine 20 units nightly",
            "Amlodipine 5 mg daily", "Aspirin 81 mg daily", "Levothyroxine 50 mcg daily", "Apixaban 5 mg twice daily"]
EYE_MEDS = ["Artificial tears 4x daily OU", "Latanoprost 0.005% nightly OU", "AREDS2 vitamins twice daily", "Brimonidine 0.2% twice daily OU"]
ALLERGIES = ["No known drug allergies", "No known drug allergies", "Penicillin (rash)", "Sulfa drugs (hives)", "Iodine contrast (nausea)",
             "Latex"]
VA = ["20/20", "20/25", "20/30", "20/40", "20/50", "20/60", "20/80", "20/100", "20/200", "CF 3 ft"]
TODAY = date(2026, 11, 15)


def d(x: date) -> str:
    return x.strftime("%m/%d/%Y")


names, patients = set(), []
while len(patients) < 100:
    first, last = rnd.choice(FIRST), rnd.choice(LAST)
    if (first, last) in names:
        continue
    names.add((first, last))
    i = len(patients)
    dob = date(rnd.randint(1934, 1972), rnd.randint(1, 12), rnd.randint(1, 28))
    sex = rnd.choice(["F", "M"])
    payer, pfx = rnd.choice(PAYERS)
    e = rnd.choice("1233")
    dx_desc, dx_tpl, anti_vegf = rnd.choice(DX)
    eye = EYE_WORD[e]
    drug, jcode = rnd.choice(DRUGS[anti_vegf])
    eyes = ["OD", "OS"] if eye == "OU" else [eye]
    # injections: every 4-10 weeks over the past year
    inj, t = [], TODAY - timedelta(days=rnd.randint(3, 40))
    for _ in range(rnd.randint(3, 8)):
        for ey in eyes:
            inj.append(dict(date=d(t), drug=drug, code=jcode, eye=ey))
        t -= timedelta(weeks=rnd.choice([4, 5, 6, 8, 10]))
    visits = []
    for k, x in enumerate(sorted({row["date"] for row in inj}, key=lambda s: (s[6:], s[:2], s[3:5]), reverse=True)[:4]):
        visits.append(dict(date=x, provider=rnd.choice(DOCS), reason="Injection visit" if k else "Injection + OCT"))
    auth_from = TODAY - timedelta(days=rnd.randint(30, 200))
    status = rnd.choices(["Approved", "Approved", "Approved", "Pending", "Denied"], k=1)[0]
    pas = [dict(payer=payer, drug=drug, eye=eye, status=status,
                auth=(f"{pfx}-{rnd.randint(100000, 999999)}" if status == "Approved" else ("ref " + str(rnd.randint(10000, 99999)))),
                valid_from=d(auth_from) if status == "Approved" else "", valid_to=d(auth_from + timedelta(days=180)) if status == "Approved" else "",
                units=rnd.choice([6, 8, 12]) if status == "Approved" else 0)]
    va = {ey: rnd.choice(VA[:8]) for ey in ("OD", "OS")}
    cst = {ey: (rnd.randint(260, 520) if ey in eyes else rnd.randint(230, 290)) for ey in ("OD", "OS")}
    patients.append(dict(
        mrn=f"T{10001 + i}", last=last, first=first, dob=d(dob), age=(TODAY - dob).days // 365, sex=sex,
        phone=f"(302) 555-01{rnd.randint(0, 99):02d}", payer=payer, member_id=f"{pfx}{rnd.randint(10000000, 99999999)}",
        pcp=rnd.choice(PCPS), physician=rnd.choice(DOCS),
        problems=[dict(desc=dx_desc, code=dx_tpl.format(e=e), eye=eye)] + [dict(desc=a, code=b, eye="OU")
                                                                        for a, b in rnd.sample(OTHER_DX, rnd.randint(0, 2))],
        eye_meds=rnd.sample(EYE_MEDS, rnd.randint(0, 2)), meds=rnd.sample(SYS_MEDS, rnd.randint(1, 4)),
        allergies=rnd.choice(ALLERGIES), va=va, iop={"OD": rnd.randint(11, 21), "OS": rnd.randint(11, 21)}, cst=cst,
        last_oct=visits[0]["date"] if visits else "", injections=inj, visits=visits, prior_auths=pas))
patients.sort(key=lambda p: (p["last"].lower(), p["first"]))
out = Path(__file__).resolve().parent.parent / "data" / "patients.json"
out.write_text(json.dumps(dict(note="FICTIONAL TEST DATA. All 100 patients are invented for software testing.",
                               generated="2026-11-15", patients=patients), indent=1))
print(out, len(patients))
