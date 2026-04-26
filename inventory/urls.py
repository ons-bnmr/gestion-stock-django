from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Accueil
    path('', views.accueil, name='accueil'),

    # Produits
    path('produits/', views.produit_liste, name='produit_liste'),
    path('produits/ajouter/', views.produit_ajouter, name='produit_ajouter'),
    path('produits/<int:pk>/', views.produit_detail, name='produit_detail'),
    path('produits/<int:pk>/modifier/', views.produit_modifier, name='produit_modifier'),
    path('produits/<int:pk>/supprimer/', views.produit_supprimer, name='produit_supprimer'),

    # Catégories
    path('categories/', views.categorie_liste, name='categorie_liste'),
    path('categories/ajouter/', views.categorie_ajouter, name='categorie_ajouter'),
    path('categories/<int:pk>/modifier/', views.categorie_modifier, name='categorie_modifier'),
    path('categories/<int:pk>/supprimer/', views.categorie_supprimer, name='categorie_supprimer'),
]
