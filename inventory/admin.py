from django.contrib import admin
from .models import Produit, Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur', 'description']
    search_fields = ['nom']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'reference', 'categorie', 'prix', 'quantite', 'statut']
    list_filter = ['categorie', 'statut']
    search_fields = ['nom', 'reference']
    list_editable = ['quantite', 'statut']
