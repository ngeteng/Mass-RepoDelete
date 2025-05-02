# delete_repos.py
# Script untuk mengambil daftar repository dan menghapus banyak repository di GitHub menggunakan Personal Access Token

import os
import sys
import requests

# Konfigurasi
TOKEN = os.getenv('GITHUB_TOKEN')
if not TOKEN:
    print("Error: environment variable GITHUB_TOKEN tidak ditemukan.")
    print("Silakan set GITHUB_TOKEN dengan Personal Access Token Anda.")
    sys.exit(1)

API_URL = 'https://api.github.com'

# Ganti dengan username atau organisasi pemilik repository
OWNER = 'nama_user_atau_org'

# Nama file untuk menyimpan daftar repository
REPOS_FILE = 'repos.txt'

# Header untuk GitHub API
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}


def fetch_repos(owner):
    """
    Mengambil daftar semua repository milik OWNER dari GitHub dan menyimpannya ke REPOS_FILE.
    """
    repos = []
    page = 1
    while True:
        url = f"{API_URL}/user/repos?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Gagal mengambil daftar repos: {response.status_code} {response.json().get('message')}")
            sys.exit(1)
        data = response.json()
        if not data:
            break
        for r in data:
            if r.get('owner', {}).get('login', '').lower() == owner.lower():
                repos.append(r['name'])
        page += 1

    if not repos:
        print(f"Tidak ada repository ditemukan untuk owner '{owner}'.")
        sys.exit(0)

    try:
        with open(REPOS_FILE, 'w') as f:
            for name in sorted(repos):
                f.write(name + '\n')
        print(f"Daftar {len(repos)} repository berhasil disimpan ke '{REPOS_FILE}'.")
    except Exception as e:
        print(f"Error menulis file {REPOS_FILE}: {e}")
        sys.exit(1)


def hapus_repo(owner, repo):
    """
    Mengirim permintaan DELETE untuk menghapus repository.
    """
    url = f"{API_URL}/repos/{owner}/{repo}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Berhasil menghapus: {owner}/{repo}")
    else:
        print(f"Gagal menghapus: {owner}/{repo} - {response.status_code} {response.json().get('message')}")


def delete_from_file(owner):
    """
    Membaca daftar repo dari REPOS_FILE dan menghapusnya satu per satu.
    """
    try:
        with open(REPOS_FILE, 'r') as f:
            repos = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error membaca file {REPOS_FILE}: {e}")
        sys.exit(1)

    if not repos:
        print("Daftar repository kosong.")
        sys.exit(0)

    print(f"Akan menghapus {len(repos)} repository milik {owner}.")
    confirm = input("Lanjutkan penghapusan? (y/N): ")
    if confirm.lower() != 'y':
        print("Dibatalkan pengguna.")
        sys.exit(0)

    for repo in repos:
        hapus_repo(owner, repo)


if __name__ == '__main__':
    print("=== GitHub Repo Manager ===")
    print("1. Fetch daftar repo")
    print("2. Hapus repo dari file")
    choice = input("Pilih aksi (1/2): ")

    if choice == '1':
        fetch_repos(OWNER)
    elif choice == '2':
        delete_from_file(OWNER)
    else:
        print("Pilihan tidak valid. Keluar.")
        sys.exit(0)
