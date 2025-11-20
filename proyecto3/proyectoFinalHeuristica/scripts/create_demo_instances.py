
import os, json, random
import pandas as pd

os.makedirs("instancias_pequeñas/demo1", exist_ok=True)
os.makedirs("instancias_grandes/demo_big1", exist_ok=True)

employees_demo1 = pd.DataFrame([
    {"employee_id":"E1","group_id":"G1","pref_days":"Mon;Wed"},
    {"employee_id":"E2","group_id":"G1","pref_days":"Mon;Thu"},
    {"employee_id":"E3","group_id":"G1","pref_days":""},
    {"employee_id":"E4","group_id":"G2","pref_days":"Tue;Thu"},
    {"employee_id":"E5","group_id":"G2","pref_days":"Tue"},
    {"employee_id":"E6","group_id":"G2","pref_days":""},
])
desks_demo1 = pd.DataFrame([{"desk_id":f"D{i}"} for i in range(1,5)])
compat_demo1 = []
for e in employees_demo1["employee_id"]:
    for d in desks_demo1["desk_id"]:
        compat_demo1.append({"employee_id":e,"desk_id":d,"compatible":1})
compat_demo1 += [{"employee_id":"E3","desk_id":"D1","compatible":0},{"employee_id":"E3","desk_id":"D2","compatible":0}]
compat_demo1 = pd.DataFrame(compat_demo1).drop_duplicates(subset=["employee_id","desk_id"], keep="last")

employees_demo1.to_csv("instancias_pequeñas/demo1/employees.csv", index=False)
desks_demo1.to_csv("instancias_pequeñas/demo1/desks.csv", index=False)
compat_demo1.to_csv("instancias_pequeñas/demo1/compatibility.csv", index=False)
with open("instancias_pequeñas/demo1/params.json","w") as f:
    json.dump({"days":["Mon","Tue","Wed","Thu","Fri"],"isolation_graph":True}, f, indent=2)

random.seed(42)
groups = ["G1","G2","G3"]
employees_big = []
eid = 1
pref_pool = ["Mon;Wed","Tue;Thu","Fri","Mon","Tue","Wed","Thu","Fri","Mon;Thu"]
for g in groups:
    for _ in range(4):
        employees_big.append({"employee_id":f"E{eid}","group_id":g,"pref_days":random.choice(pref_pool)})
        eid += 1
employees_big = pd.DataFrame(employees_big)
desks_big = pd.DataFrame([{"desk_id":f"D{i}"} for i in range(1,9)])
compat_big = []
for e in employees_big["employee_id"]:
    for d in desks_big["desk_id"]:
        compat_big.append({"employee_id":e,"desk_id":d,"compatible":1 if random.random()<0.8 else 0})
compat_big = pd.DataFrame(compat_big)

employees_big.to_csv("instancias_grandes/demo_big1/employees.csv", index=False)
desks_big.to_csv("instancias_grandes/demo_big1/desks.csv", index=False)
compat_big.to_csv("instancias_grandes/demo_big1/compatibility.csv", index=False)
with open("instancias_grandes/demo_big1/params.json","w") as f:
    json.dump({"days":["Mon","Tue","Wed","Thu","Fri"],"isolation_graph":True}, f, indent=2)

print("Instancias demo creadas.")
