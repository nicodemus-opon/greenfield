ll = "bi-90,jj-10,tt-90"
kk = ll.split(",")
print(kk)
op = "-".join(kk)
print(op)
opon = op.split("-")
print(opon)
kkk = []
for z in opon:
    try:
        int(z)
        kkk.append(z)
    except Exception as e:
        pass

full=0
for x in kkk:
    full+=int(x)
print(kkk)
print(full)