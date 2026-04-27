# 📦 StockPro — Application Django de Gestion de Stock

Application web complète de gestion de stock développée avec Django.

---

## ✅ Fonctionnalités Implémentées

### Obligatoires
- **2 tables** : `Produit` (9 champs) et `Categorie` (4 champs) avec relation FK
- **4 pages CRUD** pour les produits : Ajout, Affichage, Modification, Suppression
- **SQLite3** comme base de données
- **Templates Django** avec architecture MVT
- **Environnement virtuel** (venv)

### Bonus (7 points potentiels)
| Option | Points |
|--------|--------|
| ✅ Page d'accueil esthétique (Dashboard avec statistiques) | +1 |
| ✅ Système d'authentification login/logout | +2 |
| ✅ 2 tables avec relation (Produit ↔ Catégorie) | +2 |
| ✅ Recherche + filtres (nom, catégorie, statut) | +1 |
| ✅ Framework CSS Bootstrap 5 | +1 |
| ✅ Pagination (8 produits par page) | +1 |
| ✅ Upload d'images produit | +2 |
| ✅ Interface responsive et dark mode | bonus |

---

## 🚀 Installation & Lancement

### 1. Prérequis
```bash
Python 3.10+
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install django pillow
```

### 4. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un administrateur
```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

### 7. Accéder à l'application
- Application : http://127.0.0.1:8000/
- Admin Django : http://127.0.0.1:8000/admin/

**Identifiants par défaut :** `admin` / `admin123`

---

## 🗂️ Structure du Projet (MVT)

```
stock_manager/
├── manage.py
├── db.sqlite3
├── media/                    # Images uploadées
│   └── produits/
├── static/                   # Fichiers statiques
├── templates/                # Templates HTML
│   ├── base.html             # Template de base
│   ├── auth/
│   │   └── login.html        # Page de connexion
│   └── inventory/
│       ├── accueil.html      # Dashboard
│       ├── produit_liste.html
│       ├── produit_detail.html
│       ├── produit_form.html
│       ├── produit_confirm_delete.html
│       ├── categorie_liste.html
│       ├── categorie_form.html
│       └── categorie_confirm_delete.html
├── stock_manager/            # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── inventory/                # Application principale
    ├── models.py             # Modèles (M)
    ├── views.py              # Vues (V)
    ├── urls.py               # Routage URLs
    ├── forms.py              # Formulaires
    ├── admin.py              # Interface admin
    └── migrations/           # Migrations BDD
```

---

## 📊 Modèles de Données

### Categorie
| Champ | Type | Description |
|-------|------|-------------|
| id | AutoField | Clé primaire |
| nom | CharField(100) | Nom de la catégorie |
| description | TextField | Description optionnelle |
| couleur | CharField(7) | Couleur hex (ex: #6366f1) |
| created_at | DateTimeField | Date de création |

### Produit
| Champ | Type | Description |
|-------|------|-------------|
| id | AutoField | Clé primaire |
| nom | CharField(200) | Nom du produit |
| reference | CharField(50) | Référence unique |
| categorie | ForeignKey | Lien vers Categorie |
| description | TextField | Description |
| prix | DecimalField | Prix en TND |
| quantite | PositiveIntegerField | Quantité en stock |
| seuil_alerte | PositiveIntegerField | Seuil d'alerte stock |
| statut | CharField | disponible/rupture/commande |
| image | ImageField | Photo du produit |
| created_at | DateTimeField | Date d'ajout |
| updated_at | DateTimeField | Dernière modification |

---

## 🛠️ Technologies Utilisées
- **Backend** : Django 5.x (Python)
- **Base de données** : SQLite3
- **Frontend** : Bootstrap 5, Bootstrap Icons
- **Polices** : Plus Jakarta Sans, Space Mono (Google Fonts)
- **Upload images** : Pillow
