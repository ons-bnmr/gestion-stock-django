from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    couleur = models.CharField(max_length=7, default='#6366f1', verbose_name="Couleur (hex)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Produit(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('rupture', 'Rupture de stock'),
        ('commande', 'En commande'),
    ]

    nom = models.CharField(max_length=200, verbose_name="Nom du produit")
    reference = models.CharField(max_length=50, unique=True, verbose_name="Référence")
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produits',
        verbose_name="Catégorie"
    )
    description = models.TextField(blank=True, verbose_name="Description")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (TND)")
    quantite = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    seuil_alerte = models.PositiveIntegerField(default=10, verbose_name="Seuil d'alerte")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible', verbose_name="Statut")
    image = models.ImageField(upload_to='produits/', blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nom} ({self.reference})"

    @property
    def stock_faible(self):
        return self.quantite <= self.seuil_alerte

    @property
    def valeur_stock(self):
        return self.prix * self.quantite
