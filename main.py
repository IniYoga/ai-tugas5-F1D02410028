import json
with open("kb_pompa.json", "r", encoding="utf-8") as file:
    data = json.load(file)

aturan = data["aturan"]
fakta = []
jejak = {}
siklus = 0

hasil_aturan = [r["maka"] for r in aturan]
pertanyaan = []

for r in aturan:
    for kondisi in r["jika"]:
        if kondisi not in hasil_aturan and kondisi not in pertanyaan:
            pertanyaan.append(kondisi)

print("======================================")
print(data["judul"])
print("======================================")
print("Jawab y/t.\n")

for i, p in enumerate(pertanyaan, 1):
    while True:
        jawab = input(f"{i}. Apakah {p}? (y/t) > ").lower()

        if jawab == "y":
            fakta.append(p)
            break
        elif jawab == "t":
            break
        else:
            print("Masukkan y atau t.")

print("\nFakta awal:")
if fakta:
    print(", ".join(fakta))
else:
    print("Tidak ada fakta yang ditemukan.")

print("\nProses Forward Chaining:")

berubah = True

while berubah:
    berubah = False
    aturan_baru = []

    for r in aturan:
        cocok = []

        for kondisi in r["jika"]:
            if kondisi in fakta:
                cocok.append(kondisi)

        if r["mode"] == "dan":
            terpenuhi = len(cocok) == len(r["jika"])
        else:
            terpenuhi = len(cocok) > 0

        if terpenuhi and r["maka"] not in fakta:
            fakta.append(r["maka"])

            jejak[r["maka"]] = []

            for kondisi in cocok:
                if kondisi in jejak:
                    jejak[r["maka"]].extend(jejak[kondisi])

            jejak[r["maka"]].append(r["id"])

            aturan_baru.append(r)
            berubah = True

    siklus += 1

    if aturan_baru:
        for r in aturan_baru:
            print(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    else:
        print(f"Siklus {siklus}: tidak ada aturan baru, berhenti")

def tampilkan_alasan(hasil, tingkat=0):
    spasi = "  " * tingkat

    for r in aturan:
        if r["maka"] == hasil:
            print(f"{spasi}{hasil} <- {r['id']}")

            for kondisi in r["jika"]:
                if kondisi in jejak:
                    tampilkan_alasan(kondisi, tingkat + 1)
                else:
                    print(f"{spasi}  {kondisi}")

            break
print("\n======================================")
print("KESIMPULAN")
print("======================================")
ada_hasil = False

for r in aturan:
    perantara = False

    for aturan_lain in aturan:
        if r["maka"] in aturan_lain["jika"]:
            perantara = True

    if r["maka"] in fakta and not perantara:
        ada_hasil = True

        print("\nKesimpulan:", r["maka"])
        print("Alasan:")
        tampilkan_alasan(r["maka"])

        print("Sumber:", r["sumber"], "-", data["sumber"][r["sumber"]])

if not ada_hasil:
    print("Tidak ditemukan kesimpulan berdasarkan fakta yang diberikan.")
print("\nBatas keberlakuan:")
print(data["batas"])