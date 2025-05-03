# 🧹 GitHub Repo Manager

A Python script to **fetch** and **bulk delete** repositories from your GitHub account using your **Personal Access Token (PAT)**.

<p align="center">
  <a href="https://github.com/yourname/repo-manager/actions">
    <img src="https://img.shields.io/github/workflow/status/yourname/repo-manager/CI?label=Build&logo=github" alt="Build Status" />
  </a>
  <a href="https://github.com/yourname/repo-manager">
    <img src="https://img.shields.io/github/license/yourname/repo-manager" alt="License" />
  </a>
  <img src="https://img.shields.io/badge/python-3.6+-blue" alt="Python Version" />
</p>

---

![Demo GIF](https://user-images.githubusercontent.com/10407957/227066141-2641b782-cc82-470c-a4c4-7f7d24880e95.gif)

---

## ⚙️ Features

* 🚀 **Fetch** all your repositories with admin access
* 🗑️ **Bulk delete** multiple repos in one go
* 🌈 Colorful terminal UI and emoji support for extra flair
* 📝 Logs deletion results to a file

## 🔐 Requirements

* Python 3.6+
* A GitHub [Personal Access Token](https://github.com/settings/tokens) with scopes:

  * `repo` (full control of private/public repos)
  * `delete_repo` (required to delete repos)

## 🚀 Quick Start

1. **Clone this repo**

   ```bash
   git clone https://github.com/yourname/repo-manager.git
   cd repo-manager
   ```

2. **Set your GitHub token**

   ```bash
   export GITHUB_TOKEN=your_personal_access_token
   ```

3. **Install dependencies**

   ```bash
   pip install requests
   ```

4. **Run the script**

   ```bash
   python3 delete_repos.py
   ```

<p align="center">
  <img src="https://via.placeholder.com/600x400?text=Terminal+Screenshot" alt="Terminal Screenshot" width="600"/>
</p>

## 📂 Example Workflow

### 1. Fetch repositories

Generates `repos.txt`:

```
repo-one
old-project
test-repo
```

### 2. Edit `repos.txt`

Remove/comment out repos you don’t want to delete.

### 3. Delete

Choose option **2** in the script to remove listed repos.

---

## ⚠️ Disclaimer

This tool **permanently deletes** repositories. Double-check your `repos.txt` before proceeding!

## ❤️ Contribute

Feel free to submit issues or pull requests. All contributions are welcome!

---

<p align="center">
  <img src="https://via.placeholder.com/200?text=Thank+You" alt="Thank You" width="200"/>
</p>
