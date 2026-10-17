import struct, zlib

p = '/root/逆向测试/windows/vmp-crackmes/Custom-Packer-Nested-VM/crackme.lucky.exe'
d = open(p, 'rb').read()

lfa = struct.unpack_from('<I', d, 0x3c)[0]
_, ns, _, _, _, osz, _ = struct.unpack_from('<HHIIIHH', d, lfa + 4)
opt = lfa + 24
ib = struct.unpack_from('<Q', d, opt + 24)[0]
sec = opt + osz

secs = []
for i in range(ns):
    b = sec + i * 40
    n = d[b:b+8].rstrip(b'\0').decode('latin1')
    vs, va, rs, pr = struct.unpack_from('<IIII', d, b + 8)
    secs.append((n, va, vs, pr, rs))

def r2o(r):
    for n, va, vs, pr, rs in secs:
        if va <= r < va + max(vs, rs) and rs and r - va < rs:
            return pr + (r - va)
    return None

# Find .lucky0 for CRC32 (a7)
for n, va, vs, pr, rs in secs:
    if n == '.lucky0':
        lucky0_raw = d[pr : pr + rs]
        a7 = zlib.crc32(lucky0_raw)
        break

print(f"[+] a7 (CRC32 of .lucky0): 0x{a7:08x}")

# Find .lucky1
for n, va, vs, pr, rs in secs:
    if n == '.lucky1':
        lucky1_raw = d[pr : pr + rs]
        break

# Parse header at lucky1
# Header: 32 bytes
hdr = lucky1_raw[:32]
v10, a6, a8, off_cmd, a2, off_data, a4 = struct.unpack('<IIIIIII', hdr[:28])
print(f"[+] Header magic: 0x{v10:x} (expected 0x314b554c 'LUK1')")
print(f"[+] a6 (unpacked size): {a6} (0x{a6:x})")
print(f"[+] a8 (checksum): 0x{a8:08x}")
print(f"[+] Commands: offset={off_cmd}, size={a2}")
print(f"[+] Data: offset={off_data}, size={a4}")

cmd_buf = lucky1_raw[off_cmd : off_cmd + a2]
data_buf = lucky1_raw[off_data : off_data + a4]

out = bytearray(a6)
v8 = 0
v11 = 0
v12 = 0

while v8 < a6 and v12 < a2:
    v14 = cmd_buf[v12]
    v13 = v12 + 1
    if v14 == 0:
        break
    if v14 == 0xA2: # -94
        if v13 >= a2: break
        v11 += cmd_buf[v13]
        v12 += 2
        if v12 >= a2: break
    elif v14 == 0xA1: # -95
        if v11 >= a4: break
        # v17 = (a8 >> ((8 * v8 + 16) & 0x18)) ^ (-98 * v8) ^ (4 * v8) ^ (a7 >> (8 * (v8 & 3)));
        # v18 = 7 * v8 * v8;
        # v19 = 13 * v8++ - 89;
        # v20 = (v19 + v18) ^ v17;
        # out[v8] = data[v11++] ^ v20 ^ 0x5a
        shift1 = (8 * v8 + 16) & 0x18
        shift2 = 8 * (v8 & 3)
        v17 = ((a8 >> shift1) & 0xFF) ^ ((-98 * v8) & 0xFF) ^ ((4 * v8) & 0xFF) ^ ((a7 >> shift2) & 0xFF)
        v18 = (7 * v8 * v8) & 0xFF
        v19 = (13 * v8 - 89) & 0xFF
        v20 = (v19 + v18) ^ v17
        out[v8] = data_buf[v11] ^ (v20 & 0xFF) ^ 0x5A
        v8 += 1
        v11 += 1
        v12 = v13
    elif v14 == 0xA5: # -91
        if v13 >= a2: break
        v12 += 2
    elif v14 == 0xA6: # -90
        v12 += 1
        if v11 < a4:
            v11 += 1
    else:
        print(f"[-] Invalid command: 0x{v14:02x} at {v12}")
        break

print(f"[+] Decompressed {v8} / {a6} bytes!")
if out.startswith(b'MZ'):
    print("[🎉] Valid PE header found (MZ)!")
    out_path = '/root/逆向测试/work/lucky-vm/out/unpacked_lucky.exe'
    with open(out_path, 'wb') as f:
        f.write(out)
    print(f"[+] Saved unpacked PE to {out_path}")
else:
    print(f"[-] Header mismatch: {out[:16].hex()}")
