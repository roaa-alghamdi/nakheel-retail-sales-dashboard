"""Mock retail dataset for Power BI practice: "Nakheel Market" (fictional Saudi retail chain).
Star schema: FactSales + DimDate, DimProduct, DimBranch, DimCustomer + FactTargets.
"""
import numpy as np, pandas as pd, sys, os
rng = np.random.default_rng(2026)
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# ---------------- Branches ----------------
branches = [
    # id, name, city, region, type, open_date, size_sqm, weight
    ("BR01","Olaya","Riyadh","Central","Hypermarket","2019-03-01",5200,1.55),
    ("BR02","Al Malqa","Riyadh","Central","Supermarket","2021-09-15",2400,1.10),
    ("BR03","Al Naseem","Riyadh","Central","Express","2023-02-01",600,0.45),
    ("BR04","Al Rawdah","Jeddah","Western","Hypermarket","2019-11-10",4800,1.35),
    ("BR05","Al Hamra","Jeddah","Western","Supermarket","2022-04-20",2100,0.85),
    ("BR06","Al Aziziyah","Makkah","Western","Supermarket","2020-06-01",2300,0.95),
    ("BR07","Quba","Madinah","Western","Supermarket","2021-01-12",2000,0.80),
    ("BR08","Al Faisaliyah","Dammam","Eastern","Hypermarket","2020-02-02",4500,1.15),
    ("BR09","Al Ulaya","Khobar","Eastern","Supermarket","2022-10-01",1900,0.75),
    ("BR10","Al Muruj","Tabuk","Northern","Supermarket","2021-05-05",1800,0.70),
    ("BR11","Al Rabwah","Abha","Southern","Supermarket","2023-06-18",1700,0.55),
    ("BR12","Al Iskan","Buraydah","Central","Express","2024-03-01",550,0.35),
]
dim_branch = pd.DataFrame(branches, columns=["BranchID","BranchName","City","Region","StoreType","OpenDate","SizeSqm","_w"])
mgr = ["Faisal Al-Otaibi","Noura Al-Qahtani","Saad Al-Harbi","Reem Al-Zahrani","Majed Al-Ghamdi","Huda Al-Shehri",
       "Turki Al-Mutairi","Lama Al-Dosari","Khalid Al-Shammari","Maha Al-Anazi","Omar Al-Asiri","Sara Al-Subaie"]
dim_branch["BranchManager"] = mgr
lat = {"Riyadh":24.71,"Jeddah":21.54,"Makkah":21.39,"Madinah":24.47,"Dammam":26.43,"Khobar":26.28,"Tabuk":28.38,"Abha":18.22,"Buraydah":26.33}
lon = {"Riyadh":46.68,"Jeddah":39.17,"Makkah":39.86,"Madinah":39.61,"Dammam":50.10,"Khobar":50.21,"Tabuk":36.57,"Abha":42.51,"Buraydah":43.97}
dim_branch["Latitude"] = dim_branch.City.map(lat); dim_branch["Longitude"] = dim_branch.City.map(lon)

# ---------------- Products ----------------
cat = {
 "Fresh Food":   (["Dairy","Bakery","Fruits & Vegetables","Meat & Poultry"], (6,60), (0.22,0.32), 1.6),
 "Pantry":       (["Rice & Grains","Oils","Canned Food","Dates"],            (8,90), (0.18,0.28), 1.3),
 "Beverages":    (["Water","Juices","Coffee & Tea","Soft Drinks"],           (3,70), (0.25,0.38), 1.1),
 "Household":    (["Cleaning","Paper Products","Kitchenware"],                (10,180),(0.28,0.40), 0.7),
 "Personal Care":(["Skin Care","Hair Care","Oral Care"],                      (9,140),(0.32,0.45), 0.6),
 "Electronics":  (["Small Appliances","Accessories","Mobiles"],              (49,1900),(0.10,0.18),0.25),
 "Baby & Kids":  (["Diapers","Baby Food","Toys"],                             (15,220),(0.24,0.36), 0.45),
}
brands = ["Almarai","Nadec","Al Watania","Sadia","Abu Kass","Afia","Nestle","Tamimi Select","Nakheel Basics",
          "Saudia","Al Rabie","Persil","Fine","Dove","Colgate","Philips","Anker","Samsung","Pampers","Lego"]
prows=[]; pid=1
for c,(subs,(lo,hi),(mlo,mhi),cw) in cat.items():
    for s in subs:
        for k in range(rng.integers(6,10)):
            price = float(np.round(np.exp(rng.uniform(np.log(lo),np.log(hi))),2))
            margin = rng.uniform(mlo,mhi)
            prows.append((f"P{pid:04d}", f"{s} Item {k+1:02d}", c, s, rng.choice(brands), price,
                          round(price*(1-margin),2), cw*rng.uniform(0.5,1.5)))
            pid+=1
dim_product = pd.DataFrame(prows, columns=["ProductID","ProductName","Category","SubCategory","Brand","UnitPrice","UnitCost","_w"])
# readable names
names = {"Dairy":["Fresh Milk 2L","Laban 1L","Greek Yogurt","Cheddar Slices","Labneh 500g","Butter 400g","Cream 250ml","Feta Cheese","Kids Milk 6pk"],
 "Bakery":["Arabic Bread","Brown Toast","Croissant 6pk","Samoli 6pk","Date Maamoul","Muffins 4pk","Tortilla Wraps","Burger Buns","Rusk"],
 "Fruits & Vegetables":["Bananas 1kg","Tomatoes 1kg","Cucumbers","Potatoes 2kg","Onions 2kg","Apples Red","Oranges 2kg","Lettuce","Mixed Herbs"],
 "Meat & Poultry":["Whole Chicken","Chicken Breast","Minced Beef","Lamb Cuts","Chicken Nuggets","Beef Burger","Turkey Slices","Sausages","Chicken Wings"],
 "Rice & Grains":["Basmati Rice 5kg","Sella Rice 10kg","Lentils 1kg","Oats","Bulgur","Pasta 500g","Flour 2kg","Freekeh","Quinoa"],
 "Oils":["Sunflower Oil 1.8L","Olive Oil 1L","Corn Oil 1.5L","Ghee 800g","Coconut Oil","Canola Oil","Sesame Oil","Avocado Oil","Spray Oil"],
 "Canned Food":["Tuna 3pk","Fava Beans","Chickpeas","Tomato Paste","Sweet Corn","Mushrooms","Baked Beans","Sardines","Coconut Milk"],
 "Dates":["Sukkari Dates 1kg","Ajwa Dates","Khalas Dates","Medjool Dates","Date Paste","Stuffed Dates","Safawi Dates","Date Syrup","Date Gift Box"],
 "Water":["Water 330ml x40","Water 1.5L x6","Sparkling Water","Zamzam Pack","Water 5 Gal","Alkaline Water","Kids Water","Water 600ml x12","Mineral Water"],
 "Juices":["Orange Juice 1.75L","Mango Nectar","Apple Juice","Mixed Berry","Lemon Mint","Guava Juice","Pomegranate","Kids Juice Box","Carrot Juice"],
 "Coffee & Tea":["Saudi Coffee 500g","Espresso Beans","Instant Coffee","Black Tea 100","Green Tea","Cardamom 250g","Coffee Pods","Karak Mix","Herbal Tea"],
 "Soft Drinks":["Cola 6pk","Lemon Soda","Energy Drink","Malt Drink","Iced Tea","Orange Soda","Diet Cola","Ginger Ale","Tonic Water"],
 "Cleaning":["Laundry Detergent","Dish Soap","Floor Cleaner","Bleach","Glass Cleaner","Fabric Softener","Dishwasher Tabs","Multi Surface","Sponges"],
 "Paper Products":["Tissues 5pk","Toilet Roll 24","Kitchen Towels","Napkins","Wet Wipes","Paper Plates","Foil Roll","Cling Film","Garbage Bags"],
 "Kitchenware":["Non-stick Pan","Pot Set","Knife Set","Food Containers","Tea Set","Coffee Dallah","Cutting Board","Thermos Flask","Serving Tray"],
 "Skin Care":["Body Lotion","Sunscreen","Face Wash","Moisturizer","Hand Cream","Lip Balm","Body Wash","Face Mask","Deodorant"],
 "Hair Care":["Shampoo","Conditioner","Hair Oil","Hair Mask","Hair Serum","Kids Shampoo","Hair Gel","Dry Shampoo","Hair Brush"],
 "Oral Care":["Toothpaste","Toothbrush 2pk","Mouthwash","Dental Floss","Electric Brush Heads","Whitening Strips","Kids Toothpaste","Miswak 5pk","Tongue Cleaner"],
 "Small Appliances":["Air Fryer","Blender","Kettle","Coffee Maker","Iron","Vacuum Cleaner","Microwave","Toaster","Juicer"],
 "Accessories":["Power Bank","USB-C Cable","Earbuds","Phone Case","Charger 65W","Smart Plug","HDMI Cable","Mouse","Screen Protector"],
 "Mobiles":["Smartphone A15","Smartphone S24","Smartphone Note","Tablet 10in","Smartwatch","Kids Tablet","Feature Phone","Foldable Phone","Phone Bundle"],
 "Diapers":["Diapers Size 3","Diapers Size 4","Diapers Size 5","Pull-Ups","Newborn Diapers","Baby Wipes","Diaper Cream","Swim Diapers","Night Diapers"],
 "Baby Food":["Infant Formula","Cereal Stage 1","Fruit Puree","Baby Snacks","Toddler Milk","Veg Puree","Baby Biscuits","Rice Cereal","Baby Juice"],
 "Toys":["Building Blocks","Puzzle 100pc","Toy Car","Doll","Board Game","Coloring Set","Plush Camel","Ball","Science Kit"]}
for s,grp in dim_product.groupby("SubCategory"):
    for i,(ix) in enumerate(grp.index): dim_product.at[ix,"ProductName"]=names[s][i]

# ---------------- Customers ----------------
N_CUST = 6000
first_m=["Abdullah","Mohammed","Fahad","Khalid","Saud","Nasser","Ali","Yousef","Bandar","Turki","Sultan","Omar","Faisal","Hamad","Ibrahim"]
first_f=["Nora","Sara","Reem","Lama","Haya","Maha","Amal","Hessa","Dana","Joud","Shahad","Ghada","Rawan","Wejdan","Asma"]
last=["Al-Ghamdi","Al-Qahtani","Al-Otaibi","Al-Harbi","Al-Zahrani","Al-Shehri","Al-Mutairi","Al-Dosari","Al-Anazi","Al-Shammari","Al-Asiri","Al-Subaie","Al-Balawi","Al-Juhani","Al-Malki"]
gender = rng.choice(["Male","Female"], N_CUST, p=[0.52,0.48])
fn = np.where(gender=="Male", rng.choice(first_m,N_CUST), rng.choice(first_f,N_CUST))
home_branch = rng.choice(dim_branch.BranchID, N_CUST, p=(dim_branch._w/dim_branch._w.sum()).values)
age = np.clip(rng.normal(36,11,N_CUST).round(),18,75).astype(int)
ageband = pd.cut(age,[17,24,34,44,54,120],labels=["18-24","25-34","35-44","45-54","55+"]).astype(str)
join = pd.to_datetime("2022-01-01")+pd.to_timedelta(rng.integers(0,1400,N_CUST),unit="D")
tier = rng.choice(["Basic","Silver","Gold","Platinum"],N_CUST,p=[0.55,0.25,0.15,0.05])
dim_customer = pd.DataFrame({"CustomerID":[f"C{i:05d}" for i in range(1,N_CUST+1)],
    "CustomerName":[f"{a} {b}" for a,b in zip(fn,rng.choice(last,N_CUST))],
    "Gender":gender,"Age":age,"AgeGroup":ageband,"LoyaltyTier":tier,
    "HomeBranchID":home_branch,"JoinDate":join.date})
dim_customer["City"]=dim_customer.HomeBranchID.map(dim_branch.set_index("BranchID").City)
tier_freq = {"Basic":1.0,"Silver":1.8,"Gold":2.8,"Platinum":4.0}
cust_w = dim_customer.LoyaltyTier.map(tier_freq).values

# ---------------- Calendar & seasonality ----------------
dates = pd.date_range("2024-01-01","2025-12-31",freq="D")
def season(d):
    m=1.0
    if d.dayofweek in (3,4): m*=1.25            # Thu/Fri weekend shopping
    if d.dayofweek==5: m*=1.10
    ram = [("2024-03-11","2024-04-09"),("2025-03-01","2025-03-29")]
    eidf= [("2024-04-10","2024-04-13"),("2025-03-30","2025-04-02")]
    eida= [("2024-06-15","2024-06-19"),("2025-06-05","2025-06-09")]
    def inr(rs): return any(pd.Timestamp(a)<=d<=pd.Timestamp(b) for a,b in rs)
    if inr(ram): m*=1.45
    if inr([(pd.Timestamp(a)-pd.Timedelta(days=10),pd.Timestamp(a)-pd.Timedelta(days=1)) for a,_ in ram]): m*=1.35  # pre-Ramadan stocking
    if inr(eidf): m*=1.30
    if inr(eida): m*=1.25
    if d.month==8 and d.day>=15: m*=1.20       # back to school
    if d.month==9 and d.day in (21,22,23,24): m*=1.30  # National Day
    if d.month==2 and d.day==22: m*=1.15        # Founding Day
    if d.month==11 and 20<=d.day<=30: m*=1.55   # White Friday
    if d.month in (7,) : m*=0.90                # summer travel
    if d.year==2025: m*=1.11                    # YoY growth
    return m
seas = np.array([season(d) for d in dates])

# ---------------- Orders ----------------
BASE = 52   # orders per day, average branch weight 1
orders=[]
oid=1
bw = dim_branch.set_index("BranchID")._w
bopen = pd.to_datetime(dim_branch.set_index("BranchID").OpenDate)
cust_by_branch = {b: (dim_customer.index[dim_customer.HomeBranchID==b].values) for b in dim_branch.BranchID}
for di,d in enumerate(dates):
    for b,w in bw.items():
        if d < bopen[b]: continue
        ramp = min(1.0, 0.55 + (d-bopen[b]).days/365*0.45)
        n = rng.poisson(BASE*w*seas[di]*ramp/5.2)
        if n==0: continue
        pool = cust_by_branch[b]
        member = rng.random(n) < 0.72
        cw = cust_w[pool]/cust_w[pool].sum()
        cids = np.where(member, dim_customer.CustomerID.values[rng.choice(pool,n,p=cw)], "C00000")
        for c in cids:
            orders.append((oid,d,b,c)); oid+=1
orders = pd.DataFrame(orders, columns=["OrderNo","OrderDate","BranchID","CustomerID"])
n_o = len(orders)
# channel shifts toward online in 2025
yr = orders.OrderDate.dt.year.values
p_online = np.where(yr==2025, 0.27, 0.18)
u = rng.random(n_o)
orders["Channel"] = np.where(u<p_online, np.where(rng.random(n_o)<0.6,"Mobile App","Delivery Partner"), "In-Store")
orders.loc[orders.BranchID.isin(["BR03","BR12"]) & (orders.Channel=="Delivery Partner"),"Channel"]="In-Store"
orders["PaymentMethod"] = rng.choice(["Mada","Credit Card","Apple Pay","Cash","STC Pay","Tabby (BNPL)"], n_o, p=[0.38,0.14,0.22,0.12,0.08,0.06])
orders.loc[(orders.Channel!="In-Store")&(orders.PaymentMethod=="Cash"),"PaymentMethod"]="Apple Pay"

# ---------------- Lines ----------------
lines_per = rng.choice([1,2,3,4,5],n_o,p=[0.32,0.28,0.2,0.12,0.08])
idx = np.repeat(np.arange(n_o), lines_per)
pw = (dim_product._w/dim_product._w.sum()).values
prod_ix = rng.choice(len(dim_product), len(idx), p=pw)
L = orders.iloc[idx].reset_index(drop=True)
P = dim_product.iloc[prod_ix].reset_index(drop=True)
L["ProductID"]=P.ProductID.values
qty = np.where(P.Category.values=="Electronics", 1, rng.choice([1,1,1,2,2,3,4,6],len(idx)))
L["Quantity"]=qty
price = P.UnitPrice.values*np.where(L.OrderDate.dt.year.values==2025,1.03,1.0)  # 3% inflation
# Ramadan: dates & pantry boost already through volume; discounts in White Friday
wf = (L.OrderDate.dt.month.values==11)&(L.OrderDate.dt.day.values>=20)
disc = np.where(wf, rng.choice([0.10,0.15,0.20,0.25],len(idx)), rng.choice([0,0,0,0,0.05,0.10],len(idx)))
L["UnitPrice"]=price.round(2)
L["DiscountPct"]=disc
L["GrossSales"]=(L.Quantity*L.UnitPrice).round(2)
L["DiscountAmount"]=(L.GrossSales*L.DiscountPct).round(2)
L["NetSales"]=(L.GrossSales-L.DiscountAmount).round(2)
L["Cost"]=(L.Quantity*P.UnitCost.values*np.where(L.OrderDate.dt.year.values==2025,1.025,1.0)).round(2)
L["Profit"]=(L.NetSales-L.Cost).round(2)
# returns: higher for electronics, online
rr = np.where(P.Category.values=="Electronics",0.07,0.012) * np.where(L.Channel.values!="In-Store",1.8,1.0)
L["IsReturned"]=(rng.random(len(idx))<rr).astype(int)
# delivery minutes for online
L["DeliveryMinutes"]=np.where(L.Channel.values=="In-Store", np.nan, np.clip(rng.gamma(4,13,len(idx)),15,240).round())
# keep per-order delivery consistent
dm = L.groupby("OrderNo").DeliveryMinutes.transform("first"); L["DeliveryMinutes"]=dm
L["OrderID"]="SO-"+L.OrderNo.astype(str).str.zfill(7)
L.insert(0,"SalesLineID",np.arange(1,len(L)+1))
fact = L[["SalesLineID","OrderID","OrderDate","BranchID","CustomerID","ProductID","Channel","PaymentMethod",
          "Quantity","UnitPrice","DiscountPct","GrossSales","DiscountAmount","NetSales","Cost","Profit","IsReturned","DeliveryMinutes"]]
fact = fact.assign(OrderDate=fact.OrderDate.dt.date)

# ---------------- Date dimension ----------------
dd = pd.DataFrame({"Date":dates})
dd["Year"]=dd.Date.dt.year; dd["Quarter"]="Q"+dd.Date.dt.quarter.astype(str)
dd["MonthNo"]=dd.Date.dt.month; dd["MonthName"]=dd.Date.dt.strftime("%b")
dd["YearMonth"]=dd.Date.dt.strftime("%Y-%m"); dd["DayName"]=dd.Date.dt.strftime("%a")
dd["DayOfWeekNo"]=(dd.Date.dt.dayofweek+1)%7+1   # Sun=1
dd["IsWeekend"]=dd.Date.dt.dayofweek.isin([4,5]).astype(int)
def ev(d):
    for a,b,n in [("2024-03-11","2024-04-09","Ramadan"),("2025-03-01","2025-03-29","Ramadan"),
                  ("2024-04-10","2024-04-13","Eid Al-Fitr"),("2025-03-30","2025-04-02","Eid Al-Fitr"),
                  ("2024-06-15","2024-06-19","Eid Al-Adha"),("2025-06-05","2025-06-09","Eid Al-Adha"),
                  ("2024-11-20","2024-11-30","White Friday"),("2025-11-20","2025-11-30","White Friday"),
                  ("2024-09-21","2024-09-24","National Day"),("2025-09-21","2025-09-24","National Day"),
                  ("2024-02-22","2024-02-22","Founding Day"),("2025-02-22","2025-02-22","Founding Day"),
                  ("2024-08-15","2024-08-31","Back to School"),("2025-08-15","2025-08-31","Back to School")]:
        if pd.Timestamp(a)<=d<=pd.Timestamp(b): return n
    return "Regular"
dd["Season"]=[ev(d) for d in dd.Date]
dd["Date"]=dd.Date.dt.date

# ---------------- Targets ----------------
f2 = fact.copy(); f2["YearMonth"]=pd.to_datetime(f2.OrderDate).dt.strftime("%Y-%m")
act = f2.groupby(["BranchID","YearMonth"]).NetSales.sum().reset_index()
act["SalesTarget"]=(act.NetSales*rng.normal(1.04,0.06,len(act))/1000).round()*1000
targets = act[["BranchID","YearMonth","SalesTarget"]]
targets["MonthStart"]=pd.to_datetime(targets.YearMonth+"-01").dt.date

dim_branch=dim_branch.drop(columns="_w"); dim_product=dim_product.drop(columns="_w")
# walk-in customer row
dim_customer = pd.concat([pd.DataFrame([{"CustomerID":"C00000","CustomerName":"Walk-in (non-member)","Gender":"Unknown","Age":None,
    "AgeGroup":"Unknown","LoyaltyTier":"Non-member","HomeBranchID":None,"JoinDate":None,"City":"Unknown"}]),dim_customer])

tables = {"FactSales":fact,"DimDate":dd,"DimProduct":dim_product,"DimBranch":dim_branch,"DimCustomer":dim_customer,"FactTargets":targets}
csvdir=os.path.join(OUT,"csv"); os.makedirs(csvdir,exist_ok=True)
for n,t in tables.items(): t.to_csv(os.path.join(csvdir,n+".csv"),index=False,encoding="utf-8")
with pd.ExcelWriter(os.path.join(OUT,"Nakheel_Market_Sales_DB.xlsx"),engine="openpyxl") as w:
    for n,t in tables.items(): t.to_excel(w,sheet_name=n,index=False)
for n,t in tables.items(): print(n,t.shape)
print("Net sales by year:", fact.assign(y=pd.to_datetime(fact.OrderDate).dt.year).groupby("y").NetSales.sum().round(0).to_dict())
