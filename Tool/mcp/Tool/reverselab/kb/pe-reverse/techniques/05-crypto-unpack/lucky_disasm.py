#!/usr/bin/env python3
"""
lucky VM — 完整指令流反汇编（运行时真值校准）
=============================================
指令解密 (sub_140001790):
    plain[idx] = (cipher[idx] ^ ((7*idx + seed - 0x5B) & 0xFF))
                 ^ (D100 >> (8*(idx & 3))) & 0xFF
    D100 = dword_140545100 = 0x51A70C1E（实测常驻值）

VM 状态 (a1):
    +0x00..0x3F  16 × u32 虚拟寄存器 v0..v15
    +0x40        EIP（指向字节码流的字节偏移）
    +0x44        halted
    +0x48..0x147 256 字节 vRAM
    +0x148       输入指针
    +0x150       输入长度

操作码表（jump table @ 0x14001c000，0x26 项）
"""

D100 = 0x51A70C1E

# opcode -> (助记符, 语义说明)
OPC = {
    0x00: ("HALT",    "halted = 1"),
    0x01: ("FETCH",   "v16 = u8 code[eip++]"),
    0x02: ("FETCH32", "v16 = u32 code[eip]; eip += 4"),
    0x03: ("FETCH32B","v17 = u32 code[eip]; eip += 4"),
    0x04: ("FETCH16", "v16 = u16 code[eip]; eip += 2"),
    0x05: ("SEL_DST", "dst = v16 & 0xF"),
    0x06: ("SEL2",    "dst = (v16>>4)&0xF; src = v16&0xF"),
    0x07: ("L_V0",    "v16 = reg[dst]"),
    0x08: ("L_V1",    "v17 = reg[src]"),
    0x09: ("S_V0",    "reg[dst] = v16"),
    0x0A: ("XOR",     "v16 ^= v17"),
    0x0B: ("OR",      "v16 |= v17"),
    0x0C: ("AND",     "v16 &= v17"),
    0x0D: ("ADD",     "v16 += v17"),
    0x0E: ("XORAND",  "v16 = (v16^v17) + 2*(v16&v17)  == v16+v17"),
    0x0F: ("SUB",     "v16 -= v17"),
    0x10: ("ANDI",    "v16 &= code[eip++]"),
    0x11: ("SHRI",    "v16 >>= code[eip++] & 0x1F"),
    0x12: ("ROLI",    "v16 = rol32(v16, code[eip++])"),
    0x13: ("ROR8",    "v16 = ror8(u8 v16, v17)"),
    0x14: ("MEMRD",   "v16 = vram[v16 & 0xFF]"),
    0x15: ("MEMWR",   "vram[reg[dst]&0xFF] = reg[src]"),
    0x16: ("INPUTC",  "v16 = (reg[src] < len) ? input[reg[src]] : 0"),
    0x17: ("INPUTLEN","v16 = len(input)"),
    0x18: ("GETCFG",  "v16 = dword_140545110[src & 3]"),
    0x19: ("LOOKUP",  "v16 = lazy_lookup(reg[src])"),
    0x1A: ("EXIT",    "halted = 1"),
    0x1B: ("JNZ",     "if reg[dst] != 0: eip += v16"),
    0x1C: ("JMP",     "eip += v16"),
    0x1D: ("MUL",     "v16 *= v17"),
    0x1E: ("MOVZXB",  "v16 &= 0xFF"),
    0x1F: ("SHL1",    "v16 <<= 1"),
    0x20: ("OR_DST",  "v16 |= reg[dst]"),
    0x21: ("ROLVAR",  "v16 = rol32(v16, v17 & 31)"),
    0x22: ("SHRVAR",  "v16 >>= v17 & 0x1F"),
    0x23: ("MVTSRC",  "v17 = v16"),
    0x24: ("OR_DST2", "v16 |= reg[dst]"),
    0x25: ("MEMRD2",  "v16 = vram[reg[src] & 0xFF]"),
}

# 各 opcode 消费的额外立即数字节数（除 opcode 本身）
EXTRA = {0x01:1, 0x02:4, 0x03:4, 0x04:2, 0x10:1, 0x11:1, 0x12:1}


def decrypt(cipher: bytes, seed: int, d100: int = D100) -> bytes:
    out = bytearray(len(cipher))
    for idx in range(len(cipher)):
        out[idx] = ((cipher[idx] ^ ((7 * idx + seed - 0x5B) & 0xFF))
                    ^ ((d100 >> (8 * (idx & 3))) & 0xFF)) & 0xFF
    return bytes(out)


# 运行时实测的 8 帧（原始密文 + seed）
FRAMES = [
    (0x21, bytes.fromhex("d9c57182fc")),
    (0x2e, bytes.fromhex("ccd244b1f1")),
    (0xab, bytes.fromhex("4f5eed34")),
    (0x7c, bytes.fromhex("3e208e7a2f40ec")),
    (0x36, bytes.fromhex("c4eb49a8e1f2")),
    (0x76, bytes.fromhex("042a887c203ae2")),
    (0xb1, bytes.fromhex("4955c0206c")),
    (0xb9, bytes.fromhex("4372cb")),
]


def disasm(plain: bytes, base_eip=0, verbose=True):
    eip = 0
    lines = []
    while eip < len(plain):
        op = plain[eip]
        start = eip
        eip += 1
        name, doc = OPC.get(op, (f"UNK_{op:02x}", "?"))
        imm = ""
        n = EXTRA.get(op, 0)
        if n:
            if n == 1:
                imm = f"0x{plain[eip]:02x}"
            elif n == 2:
                imm = f"0x{int.from_bytes(plain[eip:eip+2],'little'):04x}"
            else:
                imm = f"0x{int.from_bytes(plain[eip:eip+4],'little'):08x}"
            eip += n
        lines.append(f"  {base_eip+start:03d}  {name:<9} {imm}")
        if op in (0x00, 0x1A):
            break
    if verbose:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    for i, (seed, buf) in enumerate(FRAMES):
        plain = decrypt(buf, seed)
        print(f"\n{'='*52}")
        print(f"帧 #{i}   seed=0x{seed:02x}")
        print(f"  密文: {buf.hex()}")
        print(f"  明文: {plain.hex()}")
        print(f"{'='*52}")
        disasm(plain)
