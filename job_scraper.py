import requests
import pandas as pd
import time
import random

# --- CONFIGURATION ---
limit_per_page = 60 
detailed_offers = []
offers_cache = {} 

# FULL LIST OF CATEGORIES TO SCAN
categories_to_scan = [
    "backend", "frontend", "fullstack", "mobile", "embedded",
    "ai", "data", "testing", "devops", "architecture", "security",
    "game-dev", "project-manager", "business-analyst", 
    "sys-administrator", "design", "support", "erp", "other"
]

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://nofluffjobs.com/"
}

print(f"🚀 Starting TOTAL Scraping + LOCATIONS for {len(categories_to_scan)} categories...")

# --- STEP 1: HARVESTING LIST DATA (Multi-Category Loop) ---
base_api_url = "https://nofluffjobs.com/api/search/posting"
params_url = "?salaryCurrency=PLN&salaryPeriod=month&region=pl"
search_url = base_api_url + params_url

for category in categories_to_scan:
    print(f"\n📂 SWITCHING CATEGORY: >>> {category.upper()} <<<")
    current_page = 1
    
    while True:
        print(f"   📡 Scanning {category} page {current_page}...")
        
        payload = {
            "page": current_page,
            "limit": limit_per_page,
            "criteriaSearch": {"requirement": [category], "remote": True}
        }

        try:
            response = requests.post(search_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                postings = data.get('postings', [])
                
                # Check if list is empty
                if not postings:
                    print(f"   🏁 End of {category} list.")
                    break
                
                new_items_on_page = 0
                for p in postings:
                    o_id = p.get('id')
                    
                    # Only process if we haven't seen this offer ID yet
                    if o_id not in offers_cache:
                        new_items_on_page += 1
                    
                        # --- EXTRACT SALARY ---
                        salary_str = "Hidden"
                        sal_data = p.get('salary') 
                        if sal_data:
                            s_from = sal_data.get('from')
                            s_to = sal_data.get('to')
                            s_curr = sal_data.get('currency', 'PLN')
                            if s_from and s_to: salary_str = f"{s_from} - {s_to} {s_curr}"
                            elif s_from: salary_str = f"{s_from} {s_curr}"
                            elif s_to: salary_str = f"up to {s_to} {s_curr}"
                        
                        # --- EXTRACT LOCATION  ---
                        loc_obj = p.get('location', {})
                        places = loc_obj.get('places', [])
                        
                        # Get city names, filter out empties
                        cities = [place.get('city', '') for place in places if place.get('city')]
                        
                        # Join into a single string (e.g., "Warszawa, Kraków") and remove duplicates using set()
                        location_str = ", ".join(list(set(cities)))
                        
                        # Fallback if no specific city is listed
                        if not location_str:
                            if p.get('fullyRemote'): location_str = "Remote Only"
                            else: location_str = "Unknown"
                        # -------------------------------------

                        # Cache the data including the new Location
                        offers_cache[o_id] = {
                            "Salary": salary_str,
                            "Location": location_str, # <--- Saved here!
                            "Company": p.get('name', 'Unknown'),
                            "Position": p.get('title', 'Unknown'),
                            "Category": p.get('category', category),
                            "Seniority": ", ".join(p.get('seniority', []))
                        }
                
                # --- LOOP DETECTION ---
                if new_items_on_page == 0:
                    print(f"   🏁 Loop detected for {category}. Moving to next category.")
                    break

                print(f"   -> Found +{new_items_on_page} new offers. (Total collected: {len(offers_cache)})")
                current_page += 1
                
                time.sleep(random.uniform(1.0, 2.0))
            else:
                print(f"   ❌ API Error: {response.status_code}")
                break     
        except Exception as e:
            print(f"   ❌ Network Error: {e}")
            break
            
    time.sleep(1)

# --- STEP 2: DEEP SCRAPING (Requirements) ---
all_offer_ids = list(offers_cache.keys())
total_count = len(all_offer_ids)
print(f"\n📦 TOTAL UNIQUE OFFERS COLLECTED: {total_count}. Starting detailed analysis...")

base_details_url = "https://nofluffjobs.com/api/posting/"

for index, offer_id in enumerate(all_offer_ids):
    url = base_details_url + offer_id
    
    # Progress Logger
    if index % 20 == 0: 
        percent = round((index / total_count) * 100, 1)
        print(f"   [{index}/{total_count}] ({percent}%) Processing...")
        
    # Safety Cool-down every 60 requests
    if index > 0 and index % 60 == 0: 
        print("⏸️  Safety Cool-down: Pausing for 10 seconds...")
        time.sleep(10)

    try:
        cached = offers_cache.get(offer_id, {})
        
        # Request details
        try:
            r = requests.get(url, headers=headers)
        except:
             time.sleep(5) # Retry once
             r = requests.get(url, headers=headers)

        must_have = ""
        nice_to_have = ""
        
        if r.status_code == 200:
            job_detail = r.json()
            reqs = job_detail.get('requirements', {})
            
            def clean_tags(tag_list):
                cleaned = []
                for item in tag_list:
                    val = item.get('value') if isinstance(item, dict) else item
                    if val: cleaned.append(str(val))
                return ", ".join(cleaned)

            must_have = clean_tags(reqs.get('musts', []))
            nice_to_have = clean_tags(reqs.get('nices', []))
        
        detailed_offers.append({
            "Position": cached.get('Position'),
            "Company": cached.get('Company'),
            "Salary": cached.get('Salary'),
            "Location": cached.get('Location'), 
            "Category": cached.get('Category'),
            "Seniority": cached.get('Seniority'),
            "Must_Have": must_have,
            "Nice_To_Have": nice_to_have,
            "Link": f"https://nofluffjobs.com/pl/job/{offer_id}"
        })
        
    except Exception as e:
        print(f"⚠️ Error processing {offer_id}: {e}")
    
    time.sleep(random.uniform(0.3, 0.8))

# --- SAVE TO CSV ---
df = pd.DataFrame(detailed_offers)
filename = "Total_Market_Data_With_Location.csv"
df.to_csv(filename, index=False, sep=';', encoding='utf-8-sig')
print(f"\n✅ DONE! Data saved to: {filename}")