from django import forms
from .models import Produit, Categorie


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'reference', 'categorie', 'description', 'prix', 'quantite', 'seuil_alerte', 'statut', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'REF-001'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description du produit...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'seuil_alerte': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'couleur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'couleur': forms.TextInput(attrs={'class': 'form-control form-control-color', 'type': 'color'}),
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '🔍 Rechercher un produit...',
            'id': 'search-input'
        })
    )
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + Produit.STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
