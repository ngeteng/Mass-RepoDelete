# delete_repos.py
# Script untuk menghapus banyak repository di GitHub menggunakan Personal Access Token

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

# Daftar repository yang ingin dihapus
REPOS = [
    'repo-satu',
    'repo-dua',
    'repo-tiga',
    # Tambahkan repo lainnya di sini
]


def hapus_repo(owner, repo):
    """
    Mengirim permintaan DELETE untuk menghapus repository.
    """
    url = f"{API_URL}/repos/{owner}/{repo}"
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Berhasil menghapus: {owner}/{repo}")
    else:
        print(f"Gagal menghapus: {owner}/{repo} - {response.status_code} {response.json().get('message')}")


def main():
    if not REPOS:
        print("Daftar repository kosong.")
        sys.exit(1)

    print(f"Akan menghapus {len(REPOS)} repository milik {OWNER}.")
    confirm = input("Lanjutkan? (y/N): ")
    if confirm.lower() != 'y':
        print("Dibatalkan pengguna.")
        sys.exit(0)

    for repo in REPOS:
        hapus_repo(OWNER, repo)


if __name__ == '__main__':
    main()
