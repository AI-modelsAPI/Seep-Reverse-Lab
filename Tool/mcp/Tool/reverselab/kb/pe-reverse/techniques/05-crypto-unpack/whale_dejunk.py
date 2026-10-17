#!/usr/bin/env python3
"""
Whale VM 全谱花指令消解器（终版）
=================================
经运行时验证，handler 内共 8 类花指令 + 1 类填充，全部为零副作用：

类别  签名                                                  长度  说明
----  ----------------------------------------------------  ----  ---------------------------
FILL  jmp qword ptr [rip+0]  (ff 25 00 00 00 00)             1    跳到下一条，纯占位
A     push rax/rdx; mov eax,K; bsr eax,edx; cmp 0x1f;
      jne; ud2; pop rax/rdx                                  11   bsr 非零数恒 <0x20
B     push rax/rdx; mov eax,K; mov edx,eax; xor edx,eax;
      test edx,edx; je; ud2; jmp[rip+0]; pop                11   自异或恒 0
C     mov eax,K; ror eax,13; rol eax,13; cmp eax,K;
      je; ud2                                                7    移位抵消
D     mov eax,K; and eax,0xFFFFFFFE; test al,1; je;
      call <dead>                                            6    偶数恒不跳
E     stc; jb; ud2                                            3    stc 后 CF=1 恒跳
G     push rcx; push rdx; mov eax,K1; mov ecx,K2; mov edx,eax;
      or edx,ecx; and eax,ecx; sub edx,eax; rol edx,5;
      xor edx,K3; ror edx,3; pop rdx; pop rcx                14   重言式恒等
H     push rcx; mov eax,K; mov ecx,eax; lea eax,[rax+rcx];
      shl ecx,1; cmp eax,ecx; je; ud2; pop rcx                8    2K == 2K 恒真
I     push rcx; mov rax,[rdi+0x400]; mov ecx,K1; xor eax,ecx;
      rol rax,0xb; mov rcx,K2; add rax,rcx;
      mov [rdi+0x400],rax; pop rcx                            9    状态累积器（副作用真！

注：类别 I 不是花指令，是**真实的状态推进**，消解后需单独记录。

剥离后剩下的即 handler 真实语义。
"""

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SIG_FILLER = bytes.fromhex("ff2500000000")


def _m(ins, mn, op=None):
    return ins.mnemonic == mn and (op is None or ins.op_str == op)


def match_junk(a, i):
    """返回 (类别, 消耗指令数)。容错：允许开头的 push rax/rcx/rdx 缺失或已被合并"""
    n = len(a)
    if i >= n:
        return (None, 0)

    # FILL
    if a[i].bytes == SIG_FILLER:
        return ("FILL", 1)

    # I: 状态累积器（可能有前导 push rcx）
    for pre in (0, 1):
        j = i + pre
        if (j + 8 < n and (pre == 0 or _m(a[j], "push", "rcx"))
                and j + 1 < n and "qword ptr [rdi + 0x400]" in a[j + 1].op_str
                and _m(a[j + 8], "pop", "rcx")):
            return ("I_acc", pre + 9)

    # G: 重言式恒等
    for pre in (0, 1, 2):
        j = i + pre
        if j + 13 < n and _m(a[j + 12], "pop", "rdx") and _m(a[j + 13], "pop", "rcx"):
            return ("G", pre + 14)

    # H: 2K == 2K
    for pre in (0, 1):
        j = i + pre
        if (j + 7 < n and _m(a[j + 7], "pop", "rcx")
                and j + 1 < n and _m(a[j + 1], "mov") and a[j + 1].op_str.startswith("eax,")):
            return ("H", pre + 8)

    # A: bsr 型
    for pre in (0, 1, 2):
        j = i + pre
        k = j
        while k < n and k < j + 4 and _m(a[k], "push"):
            k += 1
        if k < n and _m(a[k], "mov") and a[k].op_str.startswith("eax,"):
            if k + 6 < n and _m(a[k + 3], "cmp") and _m(a[k + 6], "ud2"):
                end = k + 7
                if end < n and _m(a[end], "pop"):
                    return ("A", end + 1 - i)

    # B: 自异或型
    for pre in (0, 1, 2):
        j = i + pre
        k = j
        while k < n and k < j + 4 and _m(a[k], "push"):
            k += 1
        if k < n and _m(a[k], "mov") and a[k].op_str.startswith("eax,"):
            if k + 5 < n and _m(a[k + 3], "test") and _m(a[k + 5], "ud2"):
                end = k + 6
                if end < n and a[end].bytes == SIG_FILLER:
                    end += 1
                while end < n and _m(a[end], "pop"):
                    end += 1
                    if end - k >= 8:
                        break
                return ("B", end - i)

    # C
    if (i + 6 < n and _m(a[i], "mov") and a[i].op_str.startswith("eax,")
            and _m(a[i + 1], "ror") and _m(a[i + 2], "rol")
            and _m(a[i + 4], "je") and _m(a[i + 5], "ud2")):
        return ("C", 6)

    # D
    if (i + 5 < n and _m(a[i], "mov") and a[i].op_str.startswith("eax,")
            and "0xfffffffe" in a[i + 1].op_str
            and _m(a[i + 2], "test", "al, 1") and _m(a[i + 4], "call")):
        return ("D", 5)

    # E
    if (i + 2 < n and _m(a[i], "stc") and _m(a[i + 2], "ud2")):
        return ("E", 3)

    return (None, 0)


def clean(code: bytes, base_va: int, verbose=False):
    cs = Cs(CS_ARCH_X86, CS_MODE_64)
    insns = list(cs.disasm(code, base_va))

    out = []
    accs = []
    stats = {}
    i = 0
    while i < len(insns):
        kind, cnt = match_junk(insns, i)
        if kind:
            stats[kind] = stats.get(kind, 0) + 1
            if kind == "I_acc":
                accs.append((insns[i].address,
                             insns[i + 2].op_str,   # mov ecx, K1
                             insns[i + 5].op_str))  # mov rcx, K2
            i += cnt
            continue
        out.append(insns[i])
        i += 1

    # 合并孤立 push rax / pop rax
    merged = []
    i = 0
    paired = 0
    while i < len(out):
        if _m(out[i], "push", "rax"):
            j = i + 1
            while j < len(out) and not _m(out[j], "pop", "rax"):
                j += 1
            if j < len(out):
                merged.extend(out[i + 1:j])
                paired += 1
                i = j + 1
                continue
        merged.append(out[i])
        i += 1

    if verbose:
        s = dict(stats)
        s["push_pop_rax"] = paired
        print(f"  花指令统计: {s}")
        print(f"  状态累积器: {len(accs)} 个")
        print(f"  去花后剩余: {len(merged)} 条")
    return merged, accs, stats


if __name__ == "__main__":
    pe = pefile.PE("/tmp/target/CrackMe0.exe")
    d = pe.get_memory_mapped_image()

    print("=" * 72)
    print("opcode 0x1b handler  0x140098eb0 .. 0x14009e400")
    print("=" * 72)
    cleaned, accs, stats = clean(d[0x98eb0:0x9e400], 0x140098eb0, verbose=True)

    print()
    print("--- 状态累积器（117 处，每处推进滚动校验状态）---")
    for addr, k1, k2 in accs[:6]:
        print(f"  0x{addr:x}: acc = rol(acc ^ {k1.split(',')[1].strip()}, 11) + {k2.split(',')[1].strip()}")

    print()
    print("--- 剩余真语义（前 45 条）---")
    for ins in cleaned[:45]:
        print(f"  0x{ins.address:x}: {ins.mnemonic:<8}{ins.op_str}")
