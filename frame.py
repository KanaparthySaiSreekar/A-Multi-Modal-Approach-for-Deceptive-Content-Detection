import json
import requests
import flask
import mysql.connector
import uuid

from bardapi import *

app = flask.Flask(__name__)


@app.route("/")
def get():
    return "hi"


@app.route("/products", methods=['GET'])
def products():
    req = requests.get('http://localhost/products.php')
    x = req.json()

    with open("C:/Users/vixha/AndroidStudioProjects/inventorymanagement/assets/abc1.json", 'w') as fl:
        json.dump(x, fl)

    return "hii"


@app.route("/current_trending", methods=['GET'])
def current():
    token = "aQhwRbYVaqqcxxXoSj_eX-jQE3sWaFR3An4YNsj9tyat5Y9iNg3ErTfeh9dzKtdC53sgbw."
    bard = Bard(token=token)
    input_query = f"""
        generate current trending real product names in ecommerce and give only the real product names in form of python list
        """
    # response_text = bard.get_answer(input_text=input_query)["content"]
    # response_text = response_text.lstrip()
    # left_brac = response_text.index('{')
    # right_brac = response_text.index('}')
    # response_text = response_text[left_brac:right_brac+1]

    # final_result = json.loads(response_text)
    # print(response_text)

    product_names = [
        "Align Leggings by Lululemon",
        "Alo Yoga Pants",
        "Outdoor Voices Movement Pants",
        "Gender-neutral T-shirt by adidas",
        "Phluid Project Tank Top",
        "Agender Hoodie",
        "Threadflip Custom Shirt",
        "Cuyana Custom Dress",
        "Stitch Fix Custom Outfit",
        "Patagonia Down Sweater Hoody",
        "The North Face ThermoBall Eco Hoodie",
        "Cotopaxi Base Camp Pullover",
        "Amazon Echo Dot",
        "Google Nest Mini",
        "Nest Thermostat",
        "Dyson Pure Cool Tower",
        "Coway Airmega 250",
        "Blueair Classic 205",
        "Litter-Robot 3 Connect",
        "CatGenie Self-Cleaning Litter Box",
        "PetSafe Simply Clean Self-Cleaning Litter Box",
        "peterson Fiddle-Leaf Fig ",
        "PetFusion Smart Pet Feeder",
        "K&H Pet Products Elevated Pet Feeder",
        "PetSafe Staywell Automatic Waterer",
        "Burt's Bees Beeswax Lip Balm",
        "The Body Shop Body Butter",
        "Lush Bath Bomb",
        "Paula's Choice 2% BHA Liquid Exfoliant",
        "Drunk Elephant T.L.C. Framboos Glycolic Night Serum",
        "The Ordinary Niacinamide 10% + Zinc 1%",
        "Briogeo Don't Despair, Repair! Deep Conditioning Mask",
        "Living Proof Restore Perfecting Spray",
        "Olaplex No. 3 Hair Perfector",
        "Ethique Shampoo Bar",
        "Lush Solid Conditioner",
        "Natural Balance Ultra Premium Dry Dog Food",
        "Blue Buffalo Wilderness Dry Dog Food",
        "Wellness Complete Health Dry Dog Food",
        "Scruffs Ethical Dog Toys",
        "Planet Dog Orbee-Tuff Toys",
        "Kong Extreme Toys",
        "Litter-Robot 3 Connect",
        "CatGenie Self-Cleaning Litter Box",
        "PetSafe Simply Clean Self-Cleaning Litter Box",
        "Embark Breed + Health Kit",
        "Wisdom Panel Complete Kit",
        "Basepaws DNA Test Kit",
        "Purina Beneful Healthy Naturals Wet Dog Food",
        "Blue Buffalo Blue Bits Tender Beef and Vegetable Recipe Soft-Moist Dog Food",
        "Wellness CORE Natural Grain-Free Turkey and Sweet Potato Recipe Dry Dog Food",
        "Samsung Frame TV",
        "LG OLED C1",
        "Sony A80J",
        "Apple AirPods Pro",
        "Sony WF-1000XM4",
        "Samsung Galaxy Buds Pro",
        "Sony WH-1000XM4",
        "Bose QuietComfort 35 II",
        "Apple AirPods Max",
        "Samsung Galaxy Z Fold 3",
        "Huawei Mate X2",
        "Motorola Razr 5G",
        "Furbo Dog Camera",
        "Petcube Bites 2",
        "Wopet Smart Pet Feeder",
        "The North Face Base Camp Tent",
        "Coleman PeakPro Camping Stove",
        "Yeti Tundra 45 Cooler",
        "Salomon Speedcross 5",
        "Hoka One One Speedgoat 4",
        "Merrell Moab 2 GTX",
        "Manduka PROlite Yoga Mat",
        "Lululemon The Mat",
        "Gaiam Essentials Yoga Mat",
    ]
    product_companies = [
        "Lululemon",
        "Alo Yoga",
        "Outdoor Voices",
        "Adidas",
        "Phluid Project",
        "Phluid Project",
        "Threadflip",
        "Cuyana",
        "Stitch Fix",
        "Patagonia",
        "The North Face",
        "Cotopaxi",
        "Amazon",
        "Google",
        "Google",
        "Dyson",
        "Coway",
        "Blueair",
        "AutoPets",
        "CatGenie",
        "PetSafe",
        "Peterson",
        "PetFusion",
        "K&H Pet Products",
        "PetSafe",
        "Burt's Bees",
        "The Body Shop",
        "Lush",
        "Paula's Choice",
        "Drunk Elephant",
        "The Ordinary",
        "Briogeo",
        "Living Proof",
        "Olaplex",
        "Ethique",
        "Lush",
        "Natural Balance",
        "Blue Buffalo",
        "Wellness",
        "Scruffs",
        "Planet Dog",
        "Kong",
        "AutoPets",
        "CatGenie",
        "PetSafe",
        "Embark",
        "Wisdom Panel",
        "Basepaws",
        "Purina",
        "Blue Buffalo",
        "Wellness",
        "Samsung",
        "LG",
        "Sony",
        "Apple",
        "Sony",
        "Samsung",
        "Sony",
        "Bose",
        "Apple",
        "Samsung",
        "Huawei",
        "Motorola",
        "Furbo",
        "Petcube",
        "Wopet",
        "The North Face",
        "Coleman",
        "Yeti",
        "Salomon",
        "Hoka One One",
        "Merrell",
        "Manduka",
        "Lululemon",
        "Gaiam"
    ]

    dic = {}
    for i, j in zip(product_names, product_companies):
        dic[i] = j

    return dic


@app.route("/get_trend", methods=['POST'])
def get_trend():
    data = flask.request.json
    name = data['name']
    token = "aQhOMByn6YhOu1uTcC--_0VJ9GtKOKQb2ZYGtxrf6Mfjt1CRkhbiH5_3ksDyCUfy_rVjAQ."
    bard = Bard(token=token)
    input_query = f"""
        please provide the product_page_views, average_time_spent_on_page, number_of_clicks, conversion_rate, cart_abandonment_rate, social_media_engagement in percentage for the ecommerce product based on the current demand for {name} product
        """
    response_text = bard.get_answer(input_text=input_query)["content"]
    response_text = response_text.lstrip()
    left_brac = response_text.index('{')
    right_brac = response_text.index('}')
    response_text = response_text[left_brac:right_brac + 1]

    final_result = json.loads(response_text)
    print(response_text)
    return final_result


@app.route("/add_product", methods=["POST"])
def add_product():
    req = requests.get('http://localhost/products.php')
    x = req.json()
    data = flask.request.json
    names = [i['name'].lower() for i in x]
    skus = [i['product_SKU'] for i in x]
    quantity = [i['quantities'] for i in x]
    name, main, sub, img, pr, sp, qt, at, sptm, sku = data['product'], data['main_category'], data[
        'sub_category'], data['image'], data['actual_price'], data['specs'], data['quantity'], data['arrival_date'], \
        data['supplier_time'], data['product_sku']

    name_attributes = ['main_category', 'sub_category', 'image', 'actual_price', 'specs', 'arrival_date',
                       'supplier_time']
    at = at.split(' ')[0].split('-')
    at = f"{at[2]}-{at[1]}-{at[0]}"
    if sp != '':
        x = '{'
        sp = sp[1:len(sp) - 1]
        sp = sp.split(',')
        print(sp)
        for i in sp:
            y = i.split(':')
            if y[0][0] == ' ':
                y[0] = y[0][1:]
            x += f'"{y[0]}"'
            x += ':'
            if y[1][0] == ' ':
                y[1] = y[1][1:]
            x += f'"{y[1]}", '
        x = x[0:len(x) - 2]
        x += '}'
        sp = x

    print(img)
    attributes = [main, sub, img, pr, sp, at, sptm]
    if name.lower() in names:
        ind = names.index(name.lower())
        sku = skus[ind]
        set_string = 'set '
        for i in range(len(attributes)):
            if i != '':
                set_string += f"{name_attributes[i]}='{attributes[i]}', "
        if qt != '':
            qt = str(float(qt) + float(quantity[ind]))
            set_string += f"quantities='{qt}' "

        query1 = f"UPDATE product_table {set_string} where name='{name}';"
        print(query1)
        conn = mysql.connector.connect(host="localhost", user="root", passwd="vishal09876", database="invtry")
        cur = conn.cursor()
        cur.execute(query1)
        conn.commit()
        conn.close()

        print(query1)
    else:
        sku = str(uuid.uuid4().hex)
        query1 = f"INSERT into product_table VALUES('{name}', '{main}', '{sub}', '{img}', '{pr}', '{sp}', '{qt}', '{at}', '{sptm}', '{sku}');"
        print(query1)
        print(query1)
        conn = mysql.connector.connect(host="localhost", user="root", passwd="vishal09876", database="invtry")
        cur = conn.cursor()
        cur.execute(query1)
        conn.commit()
        conn.close()
    req = requests.get('http://localhost/products.php')
    x = req.json()
    print(x)
    with open("C:/Users/vixha/AndroidStudioProjects/inventorymanagement/assets/abc1.json", 'w') as fl:
        json.dump(x, fl)
    return 'thanks'


@app.route("/del", methods=["POST"])
def delete():
    data = flask.request.json
    act = data['product']
    conn = mysql.connector.connect(host="localhost", user="root", passwd="vishal09876", database="invtry")
    cur = conn.cursor()
    query = f"DELETE FROM product_table where name={act}"
    cur.execute(query)
    conn.commit()
    conn.close()
    return 'thanks'

# current()
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
