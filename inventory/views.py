from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.contrib.auth.models import User
from .models import Produit, Categorie
from .forms import ProduitForm, CategorieForm, SearchForm


# ─── Authentification ───────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} ! 👋")
            return redirect('accueil')
        else:
            messages.error(request, "Identifiants incorrects.")
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('login')


# ─── Accueil / Dashboard ─────────────────────────────────────────────────────

@login_required
def accueil(request):
    total_produits = Produit.objects.count()
    total_categories = Categorie.objects.count()
    produits_alerte = Produit.objects.filter(quantite__lte=10).count()
    valeur_totale = sum(p.valeur_stock for p in Produit.objects.all())
    produits_recents = Produit.objects.select_related('categorie').order_by('-created_at')[:5]
    stats_categories = Categorie.objects.annotate(nb_produits=Count('produits')).order_by('-nb_produits')[:5]

    context = {
        'total_produits': total_produits,
        'total_categories': total_categories,
        'produits_alerte': produits_alerte,
        'valeur_totale': valeur_totale,
        'produits_recents': produits_recents,
        'stats_categories': stats_categories,
    }
    return render(request, 'inventory/accueil.html', context)


# ─── Produits CRUD ────────────────────────────────────────────────────────────

@login_required
def produit_liste(request):
    form = SearchForm(request.GET)
    produits = Produit.objects.select_related('categorie').all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        categorie = form.cleaned_data.get('categorie')
        statut = form.cleaned_data.get('statut')

        if q:
            produits = produits.filter(
                Q(nom__icontains=q) |
                Q(reference__icontains=q) |
                Q(description__icontains=q)
            )
        if categorie:
            produits = produits.filter(categorie=categorie)
        if statut:
            produits = produits.filter(statut=statut)

    paginator = Paginator(produits, 8)
    page = request.GET.get('page')
    produits_page = paginator.get_page(page)

    return render(request, 'inventory/produit_liste.html', {
        'produits': produits_page,
        'form': form,
        'total': produits.count(),
    })


@login_required
def produit_detail(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, 'inventory/produit_detail.html', {'produit': produit})


@login_required
def produit_ajouter(request):
    form = ProduitForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            produit = form.save()
            messages.success(request, f"✅ Produit « {produit.nom} » ajouté avec succès !")
            return redirect('produit_liste')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier les champs.")
    return render(request, 'inventory/produit_form.html', {'form': form, 'action': 'Ajouter', 'titre': 'Nouveau Produit'})


@login_required
def produit_modifier(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    form = ProduitForm(request.POST or None, request.FILES or None, instance=produit)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f"✏️ Produit « {produit.nom} » modifié avec succès !")
            return redirect('produit_liste')
    return render(request, 'inventory/produit_form.html', {'form': form, 'action': 'Modifier', 'titre': f'Modifier : {produit.nom}', 'produit': produit})


@login_required
def produit_supprimer(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        nom = produit.nom
        produit.delete()
        messages.success(request, f"🗑️ Produit « {nom} » supprimé.")
        return redirect('produit_liste')
    return render(request, 'inventory/produit_confirm_delete.html', {'produit': produit})


# ─── Catégories CRUD ──────────────────────────────────────────────────────────

@login_required
def categorie_liste(request):
    categories = Categorie.objects.annotate(nb_produits=Count('produits')).order_by('nom')
    return render(request, 'inventory/categorie_liste.html', {'categories': categories})


@login_required
def categorie_ajouter(request):
    form = CategorieForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cat = form.save()
        messages.success(request, f"✅ Catégorie « {cat.nom} » créée !")
        return redirect('categorie_liste')
    return render(request, 'inventory/categorie_form.html', {'form': form, 'action': 'Ajouter', 'titre': 'Nouvelle Catégorie'})


@login_required
def categorie_modifier(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    form = CategorieForm(request.POST or None, instance=categorie)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"✏️ Catégorie « {categorie.nom} » modifiée !")
        return redirect('categorie_liste')
    return render(request, 'inventory/categorie_form.html', {'form': form, 'action': 'Modifier', 'titre': f'Modifier : {categorie.nom}', 'categorie': categorie})


@login_required
def categorie_supprimer(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        nom = categorie.nom
        categorie.delete()
        messages.success(request, f"🗑️ Catégorie « {nom} » supprimée.")
        return redirect('categorie_liste')
    return render(request, 'inventory/categorie_confirm_delete.html', {'categorie': categorie})
