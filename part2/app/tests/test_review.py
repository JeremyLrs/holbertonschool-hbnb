from app.models.review import Review
from app.models.user import User
from app.models.place import Place

def test_review_creation():
    user = User(first_name="Chris", last_name="Barrere", email="chris@example.fr")
    place = Place(title="beau appart", description="Appart au centre", price="100", latitude="50", longitude="100", owner=user)
    review = Review(text="Excellent séjour", rating=5, place=place, user=user)

    assert review.text == "Excellent séjour"
    assert review.rating == 5
    assert review.place == place
    assert review.user == user
    assert review in place.reviews
    print("Review test passed")

test_review_creation()