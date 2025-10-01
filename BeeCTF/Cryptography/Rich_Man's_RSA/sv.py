#!/usr/bin/env python3
# solve_rsa.py
import argparse
import random
from math import gcd
from Crypto.Util.number import long_to_bytes

def try_decrypt_with_n(c, d, n):
    m_int = pow(c, d, n)
    try:
        m = long_to_bytes(m_int).decode()
    except Exception:
        m = long_to_bytes(m_int)
    return m_int, m

def factor_from_ed(n, e, d, tries=200):
    """
    Coba faktorisasi n dengan trik k = e*d - 1.
    Kembalikan (p,q) bila berhasil, atau None bila gagal.
    """
    k = e * d - 1
    if k <= 0:
        return None
    # k harus genap (biasanya iya)
    s = 0
    r = k
    while r % 2 == 0:
        r //= 2
        s += 1
    # coba beberapa basis random
    for _ in range(tries):
        g = random.randrange(2, n-1)
        y = pow(g, r, n)
        if y == 1 or y == n-1:
            continue
        for _ in range(s):
            x = pow(y, 2, n)
            if x == 1:
                p = gcd(y - 1, n)
                if 1 < p < n:
                    q = n // p
                    return int(p), int(q)
                else:
                    break
            y = x
    return None

def parse_int(s):
    s = s.strip()
    if s.startswith("0x") or s.startswith("0X"):
        return int(s, 16)
    return int(s, 10)

def main():
    p = argparse.ArgumentParser(description="RSA helper: decrypt or factor from (e,d).")
    p.add_argument("--c", required=True, help="ciphertext c (decimal or 0xhex)")
    p.add_argument("--d", required=True, help="private exponent d (decimal or 0xhex)")
    p.add_argument("--n", required=False, help="modulus n (decimal or 0xhex). If omitted, script will try to factor n using e and d.")
    p.add_argument("--e", default="65537", help="public exponent e (default 65537)")
    p.add_argument("--tries", type=int, default=200, help="number of random tries for factoring (default 200)")
    args = p.parse_args()

    c = parse_int(args.c)
    d = parse_int(args.d)
    e = parse_int(args.e)

    if args.n:
        n = parse_int(args.n)
        print("[*] n provided. Doing direct decryption.")
        m_int, m = try_decrypt_with_n(c, d, n)
        print("Recovered m (int):", m_int)
        print("Recovered m (bytes/string):", m)
        return

    # kalau n tidak diberikan -> butuh n
    print("[*] n not provided. Attempting to recover n by factoring using e and d ...")
    # Untuk faktorisasi kita *tidak* tahu n. Tapi wait — kita memang butuh n untuk melakukan factoring.
    # Namun challenge yang kamu tunjukkan sebenarnya menjalankan getPrime lalu n=p*q.
    # Jika pembuat tidak print n, biasanya mereka memberikan n elsewhere. Jika n benar-benar hilang,
    # kita tetap perlu n untuk membagi p and q — jadi skrip ini mengasumsikan kamu punya n but nampaknya lupa paste.
    # Jadi: kita cek apakah user memasukkan n. Jika tidak, kita tidak dapat faktorisasi.
    print("ERROR: untuk faktorisasi kita butuh nilai n juga. Silakan jalankan program challenge lagi dan copy 'n'.")
    print("Jika kamu sudah punya n tetapi lupa memasukkan, jalankan ulang dengan --n <nilai n>.")
    return

if __name__ == "__main__":
    main()
