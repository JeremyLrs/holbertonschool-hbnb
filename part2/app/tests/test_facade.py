# test_facade.py
from app.models.user import User
from app.models.place import Place
from app.services.facade import HBnBFacade

# Création de la façade
facade = HBnBFacade()

# ---- Créer un utilisateur ---- #
# Comme create_user n'est pas encore implémenté, on peut créer un User directement
user = User(id=1, name="Alice")
# Si tu as un repo en mémoire, ajoute-le
facade.user_repo.add(user)

# ---- Créer une place ---- #
place_data = {
    "title": "Stade Central",
    "description": "Un grand stade",
    "price": 500,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": 1,
    "amenities": []
}

place = facade.create_place(place_data)
print("Place créée :", place.to_dict())

# ---- Récupérer toutes les places ---- #
all_places = facade.get_all_places()
print("Toutes les places :")
for p in all_places:
    print(p.to_dict())
