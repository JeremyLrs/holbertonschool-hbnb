const API_URL = 'http://127.0.0.1:5000/api/v1/';
const placesList = document.querySelector('#places ul');
const placeForm = document.getElementById('place-form');
const reviewsList = document.querySelector('#reviews ul');
const reviewForm = document.querySelector('#review-form');
const amenitiesList = document.querySelector('.amenities-filter ul');

const login = document.getElementById('login');
const account = document.getElementById('account');

document.addEventListener('DOMContentLoaded', async () => {
  const newAccountForm = document.getElementById('account-form');
  const newAccountButton = document.getElementById('new-account');
  const loginForm = document.getElementById('login-form');
  const loginButton = document.getElementById('login-link');
  const logoutButton = document.getElementById('logout-link');
  const newPlaceButton = document.getElementById('new-place');
  const searchButton = document.getElementById('search-button');
  const searchField = document.getElementById('search-field');
  let searchTerm = document.getElementById('search-field');

  const token = await checkAuthentication().then(
    data => { return data; }
  );

  const filter = document.getElementById('filter');
  const filterButton = document.getElementById('filter-button');
  const resetButton = document.getElementById('reset-button');
  const placeDetails = document.getElementById('place-details');
  const animation = document.getElementById('animation');

  if (searchButton) {
    searchButton.addEventListener('click', (event) => {
      const places = document.querySelectorAll('#places li');
      searchTerm = document.getElementById('search-field').value;
      searchPlace(places, searchTerm);
    });
    searchField.addEventListener('keypress', (event) => {
      if (event.key === 'Enter') {
        const places = document.querySelectorAll('#places li');
        searchTerm = document.getElementById('search-field').value;
        searchPlace(places, searchTerm);
      }
    });
  }

  if (filter) {
    let price = 0;
    let capacity = 1;
    let rooms = 1;
    let surface = 1;
    let amenities = [];

    /* Retrieving all amenities */
    const amenityItems = await fetchAmenities().then(
      data => { return data; }
    );

    /* Populating amenities filter */
    addAmenities(amenityItems);

    /* Setting number filters values */
    document.getElementById('price-filter').addEventListener('change', (event) => {
      price = Number(document.getElementById('price-filter').value);
    });
    document.getElementById('capacity-filter').addEventListener('input', (event) => {
      capacity = Number(document.getElementById('capacity-filter').value);
    });
    document.getElementById('rooms-filter').addEventListener('input', (event) => {
      rooms = Number(document.getElementById('rooms-filter').value);
    });
    document.getElementById('surface-filter').addEventListener('input', (event) => {
      surface = Number(document.getElementById('surface-filter').value);
    });

    /* Setting amenities values */
    setAmenities(amenities, 'name');

    /* Filtering places to display */
    filterButton.addEventListener('click', (event) => {
      let places = document.querySelectorAll('#places li');
      searchTerm = document.getElementById('search-field').value;
      /* Filtering only current results in case of a search term */
      if (searchTerm) {
        searchPlace(places, searchTerm);
        places = document.querySelectorAll('#places li:not([style*="display: none;"])');
      } else {
        places = document.querySelectorAll('#places li');
      }
      filterPlaces(places, price, capacity, rooms, surface, amenities);
    });

    /* Reseting filters and places to display */
    resetButton.addEventListener('click', (event) => {
      let places = document.querySelectorAll('#places li');
      price = 0;
      capacity = 1;
      rooms = 1;
      surface = 10;
      amenities = [];
      searchField.value = '';
      resetFilters();
      setAmenities(amenities, 'name');
      filterPlaces(places, price, capacity, rooms, surface, amenities);
    });

    /* Displaying new place button */
    if (token) {
      newPlaceButton.style.display = 'block';
      newPlaceButton.addEventListener('click', (event) => {
        window.location.href = 'add_place.html';
      });
    }
  }

  if (placeDetails) {
    const placeId = getParameterFromURL('place');
    const place = await fetchPlaceDetails(token, placeId).then(
      data => { return data; }
    );
    displayPlaceDetails(token, place);
  }

  if (reviewForm) {
    const placeId = getParameterFromURL('place');
    const reviewId = getParameterFromURL('review');
    
    if (!token) {
      window.location.href = 'index.html';
    }

    let rating = 0;

    /* Pre-filling review form on edition */
    if (reviewId) {
      const h3 = document.querySelector('#review h3');
      h3.textContent = 'Edit Review';
      const review = await fetchReviewDetails(token, reviewId).then(
        data => { return data; }
      );

      const title = document.getElementById('title');
      const text = document.getElementById('text');
      rating = review.rating;

      title.value = review.title;
      text.value = review.text;
      colorStars(review.rating);

      /* Adding delete button */
      const section = document.querySelector('#review');
      const a = document.createElement('a');
      a.className = 'link';
      a.setAttribute('type', 'button');
      a.textContent = 'Delete';
      section.appendChild(a);

      a.addEventListener('click', (event) => {
        const confirmation = confirm('Delete this review?');
        if (confirmation) {
          deleteReview(token, placeId, reviewId);
        }
      });
    } else {
      const h3 = document.querySelector('#review h3');
      const place = await fetchPlaceDetails(token, placeId).then(
        data => { return data; }
      );
      h3.textContent = place.title;
    }

    /* Getting star rating */
    for (let i = 0; i < 5; i++) {
      const star = document.getElementById(`star-${i + 1}`);
      star.addEventListener('click', (event) => {
        rating = i + 1;
        colorStars(rating);
      });
    }

    /* Review submission */
    if (reviewId) { // PUT
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        editReview(
          token,
          reviewForm.title.value,
          reviewForm.text.value,
          rating,
          placeId,
          reviewId
        );
      });
    } else { // POST
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        submitReview(
          token,
          reviewForm.title.value,
          reviewForm.text.value,
          rating,
          placeId
        );
      });
    }
  }

  if (placeForm) {
    const placeId = getParameterFromURL('place');

    /* Redirecting user if not logged in */
    if (!token) {
      window.location.href = 'index.html';
    }

    /* Retrieving all amenities */
    const amenities = [];
    const amenityItems = await fetchAmenities().then(
      data => { return data; }
    );

    /* Populating amenities list */
    addAmenities(amenityItems);

    /* Setting amenities values */
    setAmenities(amenities, 'id');

    /* Pre-filling place form on edition */
    if (placeId) {
      const user = decodeJWT(token);
      const place = await fetchPlaceDetails(token, placeId).then(
        data => { return data; }
      );

      /* Redirection user if not the owner */
      if (user.id !== place.owner.id) {
        window.location.href = 'index.html';
      }

      const list = document.querySelectorAll('.amenities-filter input');

      /* Pre-checking amenities */
      for (let i = 0; i < place.amenities.length; i++) {
        amenities.push(place.amenities[i].id);
        for (let j = 0; j < list.length; j++) {
          if (amenities[i] === list[j].getAttribute('id')) {
            list[j].checked = true;
          }
        }
      }

      const title = document.getElementById('title');
      const description = document.getElementById('description');
      const price = document.getElementById('price');
      const capacity = document.getElementById('capacity');
      const rooms = document.getElementById('rooms');
      const surface = document.getElementById('surface');
      const latitude = document.getElementById('latitude');
      const longitude = document.getElementById('longitude');

      title.value = place.title;
      description.value = place.description;
      price.value = place.price;
      capacity.value = place.capacity;
      rooms.value = place.rooms;
      surface.value = place.surface;
      latitude.value = place.latitude;
      longitude.value = place.longitude;

      /* Adding delete button */
      const section = document.querySelector('#place');
      const a = document.createElement('a');
      a.className = 'link';
      a.setAttribute('type', 'button');
      a.textContent = 'Delete';
      section.appendChild(a);

      a.addEventListener('click', (event) => {
        const confirmation = confirm('Delete this place?');
        if (confirmation) {
          deletePlace(token, placeId);
        }
      });
    }

    /* Place submission */
    if (placeId) { // PUT
      placeForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        editPlace(
          token,
          placeForm.title.value,
          placeForm.description.value,
          parseFloat(placeForm.price.value),
          Number(placeForm.capacity.value),
          Number(placeForm.rooms.value),
          parseFloat(placeForm.surface.value),
          parseFloat(placeForm.latitude.value),
          parseFloat(placeForm.longitude.value),
          amenities,
          placeId
        );
      });
    } else { // POST
      placeForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        submitPlace(
          token,
          placeForm.title.value,
          placeForm.description.value,
          parseFloat(placeForm.price.value),
          Number(placeForm.capacity.value),
          Number(placeForm.rooms.value),
          parseFloat(placeForm.surface.value),
          parseFloat(placeForm.latitude.value),
          parseFloat(placeForm.longitude.value),
          amenities
        );
      });
    }
  }

  if (loginForm) {
    loginButton.style = 'none';
    animation.style.display = 'none';
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      loginUser(loginForm.email.value, loginForm.password.value);
    });
  }

  if (newAccountForm) {
    loginButton.style.display = 'none';
    animation.style.display = 'none';
    newAccountForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      createAccount(
        newAccountForm.first_name.value,
        newAccountForm.last_name.value,
        newAccountForm.email.value,
        newAccountForm.password.value
      );
    });
  }

  if (loginButton) {
    loginButton.addEventListener('click', (event) => {
      window.location.href = 'login.html';
    });
  }

  if (logoutButton) {
    logoutButton.addEventListener('click', (event) => {
      deleteCookie('token');
      window.location.href = 'login.html';
    });
  }
});

function searchPlace (places, searchTerm) {
  for (let i = 0; i < places.length; i++) {
    if (places[i].getAttribute('title').toLowerCase().includes(searchTerm)) {
      places[i].style.display = 'block';
    } else {
      places[i].style.display = 'none';
    }
  }
}

async function createAccount (first_name, last_name, email, password) {
  /* Creating new account */
  const response = await fetch(`${API_URL}users/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ first_name, last_name, email, password })
  });

  if (response.ok) {
    loginUser(email, password);
  } else {
    alert('Account creation failed: ' + response.statusText);
  }
}

async function loginUser (email, password) {
  /* Authenticating a user */
  const response = await fetch(`${API_URL}auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  /* Saving token in a cookie */
  if (response.ok) {
    if (login) {
      login.style.display = 'none';
    } else if (account) {
      account.style.display = 'none';
    }
    animation.style.display = 'block';
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.setTimeout(function () {
      animation.style.display = 'none';
      window.location.href = 'index.html';
    }, 5000);
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

async function checkAuthentication () {
  /* Displaying login/logout button */
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');

  if (!token) {
    loginLink.style.display = 'block';
    logoutLink.style.display = 'none';
  } else {
    loginLink.style.display = 'none';
    logoutLink.style.display = 'block';
  }

  if (placesList) {
    document.getElementById('filter').style.display = 'block';
    const places = await fetchPlaces(token);
    displayPlaces(places);
  }

  return token;
}

function getCookie (name) {
  /* Getting a cookie value */
  const cookieList = decodeURIComponent(document.cookie).split('; ');
  for (let i = 0; i < cookieList.length; i++) {
    const cookie = cookieList[i].split('=');
    if (name === cookie[0]) {
      return cookie[1];
    }
  }
}

function deleteCookie (name) {
  /* Deleting a cookie */
  const cookieList = decodeURIComponent(document.cookie).split('; ');
  for (let i = 0; i < cookieList.length; i++) {
    const cookie = cookieList[i].split('=');
    if (name === cookie[0]) {
      document.cookie = `token=${cookie[1]}; expires=Thu, 01 Jan 1970 12:00:00 GMT; path=/`;
    }
  }
}

async function fetchPlaces (token) {
  /* Retrieving all places */
  const response = await fetch(`${API_URL}places/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  } else if (response.status !== 404) {
    const message = await response.json();
    alert(`Failure: ${message.error} (${response.statusText})`);
  }
}

async function fetchAmenities () {
  /* Retrieving all amenities */
  const response = await fetch(`${API_URL}amenities/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    alert('Fetching amenities failed: ' + response.statusText);
  }
}

function addAmenities (amenityItems) {
  /* Populating amenities list */
  for (let i = 0; i < amenityItems.length; i++) {
    const li = document.createElement('li');

    const label = document.createElement('label');
    label.setAttribute('for', amenityItems[i].name);
    label.textContent = amenityItems[i].name;

    const input = document.createElement('input');
    input.setAttribute('type', 'checkbox');
    input.setAttribute('id', amenityItems[i].id);
    input.setAttribute('value', amenityItems[i].name);

    li.appendChild(input);
    li.appendChild(label);
    amenitiesList.appendChild(li);
  }
}

function setAmenities (amenities, parameter) {
  const list = document.querySelectorAll('.amenities-filter input');
  if (parameter === 'name') {
    for (let i = 0; i < list.length; i++) {
      list[i].addEventListener('change', (event) => {
        if (list[i].checked) {
          amenities.push(list[i].defaultValue);
        } else {
          const index = amenities.indexOf(list[i].defaultValue);
          amenities.splice(index, 1);
        }
      });
    }
  } else if (parameter === 'id') {
    for (let i = 0; i < list.length; i++) {
      list[i].addEventListener('change', (event) => {
        if (list[i].checked) {
          amenities.push(list[i].id);
        } else {
          const index = amenities.indexOf(list[i].id);
          amenities.splice(index, 1);
        }
      });
    }
  }
}

function displayPlaces (places) {
  /* Clearing placesList */
  let lastItem = placesList.lastElementChild;
  while (lastItem) {
    placesList.removeChild(lastItem);
    lastItem = placesList.lastElementChild;
  }

  /* Populating placesList */
  if (places) {
    for (let i = 0; i < places.length; i++) {
      const li = document.createElement('li');
      li.classList.add('col-3');
      li.setAttribute('title', places[i].title);
      li.setAttribute('price', places[i].price);
      li.setAttribute('capacity', places[i].capacity);
      li.setAttribute('rooms', places[i].rooms);
      li.setAttribute('surface', places[i].surface);
      li.setAttribute('amenities', places[i].amenities.join(';'));

      const div = document.createElement('div');
      div.classList.add('place-card');
      li.appendChild(div);

      const title = document.createElement('h4');
      title.classList.add('place-title');
      title.textContent = places[i].title;
      div.appendChild(title);

      const price = document.createElement('h5');
      price.classList.add('place-price');
      price.textContent = `${places[i].price} $ / night`;
      div.appendChild(price);

      const button = document.createElement('button');
      button.classList.add('details-button');
      button.textContent = 'Details';
      button.addEventListener('click', (event) => {
        window.location.href = `place.html?place=${places[i].id}`;
      });
      div.appendChild(button);

      placesList.appendChild(li);
    }
  }
}

function filterPlaces (places, price, capacity, rooms, surface, amenities) {
  /* Filtering places to display */
  const amenityFilter = document.querySelector('.amenities-filter');

  for (let i = 0; i < places.length; i++) {
    if (
      (Number(places[i].getAttribute('price')) > price && price > 0) ||
      (Number(places[i].getAttribute('capacity')) < capacity) ||
      (Number(places[i].getAttribute('rooms')) < rooms) ||
      (Number(places[i].getAttribute('surface')) < surface)
    ) {
      places[i].style.display = 'none';
    } else {
      if (!isMissing(amenities, places[i].getAttribute('amenities'))) {
        places[i].style.display = 'block';
      } else {
        places[i].style.display = 'none';
      }
    }
  }

  if (amenityFilter.open === true) {
    amenityFilter.open = false;
  }
}

async function isImage (name) {
  return fetch(`/images/amenities/${name}.png`, { method: 'HEAD' })
    .then((response) => {
      if (response.ok) {
        return true;
      } else {
        return false;
      }
    });
}

function isMissing (amenities, placeAmenities) {
  /* Checking placeAmenities */
  for (let i = 0; i < amenities.length; i++) {
    const array = placeAmenities.split(';');
    let missingAmenity = true;
    for (let j = 0; j < array.length; j++) {
      if (amenities[i] === array[j]) {
        missingAmenity = false;
        break;
      }
    }
    if (missingAmenity) {
      return true;
    }
  }
  return false;
}

function resetFilters () {
  /* Resetting all values to default */
  const amenityFilter = document.querySelector('.amenities-filter');

  document.getElementById('price-filter').value = '0';
  document.getElementById('capacity-filter').value = '1';
  document.getElementById('rooms-filter').value = '1';
  document.getElementById('surface-filter').value = '10';

  /* Unchecking all amenities */
  for (const element of document.querySelectorAll('.amenities-filter input')) {
    element.checked = false;
  }

  if (amenityFilter.open === true) {
    amenityFilter.open = false;
  }
}

function getParameterFromURL (name) {
  const parameters = new URLSearchParams(window.location.search);
  const value = parameters.get(name);
  return value;
}

async function fetchReviewDetails (token, reviewId) {
  const response = await fetch(`${API_URL}reviews/${reviewId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    alert('Fetching review details failed: ' + response.statusText);
  }
}

async function fetchPlaceDetails (token, placeId) {
  const response = await fetch(`${API_URL}places/${placeId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    alert('Fetching place details failed: ' + response.statusText);
  }
}

async function displayPlaceDetails (token, place) {
  /* Populating place details */
  const title = document.querySelector('.place-title');
  title.textContent = place.title;

  const description = document.querySelector('.place-description');
  description.textContent = place.description;

  /* const owner = document.querySelector('.place-owner');
  owner.textContent = `- ${place.owner.first_name} ${place.owner.last_name[0]}.`; */

  const price = document.querySelector('.place-price');
  price.textContent = place.price + ' $';

  const capacity = document.querySelector('.place-capacity');
  capacity.textContent = place.capacity;

  const rooms = document.querySelector('.place-rooms');
  rooms.textContent = place.rooms;

  const surface = document.querySelector('.place-surface');
  surface.textContent = place.surface + ' m';
  const square = document.createElement('sup');
  square.textContent = '2';
  surface.appendChild(square);

  /* Populating place amenities */
  const amenitiesList = document.querySelector('.place-amenities');
  for (let i = 0; i < place.amenities.length; i++) {
    const amenity = document.createElement('li');
    amenity.classList.add('amenity-item');
    const icon = document.createElement('img');
    const imageFound = await isImage(place.amenities[i].name);
    if (imageFound) {
      icon.setAttribute('src', `images/amenities/${place.amenities[i].name}.png`);
    } else {
      icon.setAttribute('src', 'images/amenities/None.png');
    }
    icon.setAttribute('width', '20px');
    icon.setAttribute('height', '20px');
    amenity.appendChild(icon);
    const name = document.createElement('h5');
    name.textContent = place.amenities[i].name;
    amenity.appendChild(name);
    amenitiesList.appendChild(amenity);
  }

  /* Adding edit or review button */
  if (token) {
    const card = document.querySelector('.place-card');
    const user = decodeJWT(token);
    const button = document.createElement('button');
    if (user.id === place.owner.id) {
      button.classList.add('edit-button');
      button.textContent = 'Edit';
      button.addEventListener('click', (event) => {
        window.location.href = `add_place.html?place=${place.id}`;
      });
    } else {
      button.classList.add('review-button');
      button.textContent = 'Review';
      button.addEventListener('click', (event) => {
        window.location.href = `add_review.html?place=${place.id}`;
      });
    }
    card.appendChild(button);
  }


  displayReviews(token, place);
}

function displayReviews (token, place) {
  /* Populating place reviews */
  for (let i = 0; i < place.reviews.length; i++) {
    const li = document.createElement('li');
    li.classList.add('col-3');

    const div = document.createElement('div');
    div.classList.add('review-card');
    li.appendChild(div);

    /* Displaying title */
    const title = document.createElement('h4');
    title.classList.add('review-title');
    title.textContent = place.reviews[i].title;
    div.appendChild(title);

    /* Displaying rating with stars */
    const rating = document.createElement('ul');
    rating.classList.add('review-rating');
    for (let j = 0; j < Number(place.reviews[i].rating); j++) {
      const star = document.createElement('li');
      const icon = document.createElement('img');
      icon.setAttribute('src', 'images/reviews/star_full.png');
      icon.setAttribute('width', '16px');
      icon.setAttribute('height', '16px');
      star.appendChild(icon);
      rating.appendChild(star);
    }
    for (let j = 0; j < 5 - Number(place.reviews[i].rating); j++) {
      const star = document.createElement('li');
      const icon = document.createElement('img');
      icon.setAttribute('src', 'images/reviews/star_empty.png');
      icon.setAttribute('width', '16px');
      icon.setAttribute('height', '16px');
      star.appendChild(icon);
      rating.appendChild(star);
    }
    div.appendChild(rating);

    /* Displaying text */
    const text = document.createElement('p');
    text.classList.add('review-text');
    text.textContent = place.reviews[i].text;
    div.appendChild(text);

    /* Displaying author name */
    const user = document.createElement('p');
    user.classList.add('review-user');
    user.textContent = `- ${place.reviews[i].user.first_name} ${place.reviews[i].user.last_name[0]}.`;
    div.appendChild(user);

    const bottom = document.createElement('span');
    bottom.classList.add('review-bottom');
    div.appendChild(bottom);

    /* Allowing edition if current user matches author */
    if (token) {
      const userId = decodeJWT(token).id;
      if (userId === place.reviews[i].user.id) {
        const edit = document.createElement('button');
        edit.classList.add('edit-button');
        edit.textContent = 'Edit';
        edit.addEventListener('click', (event) => {
          window.location.href = `add_review.html?place=${place.id}&review=${place.reviews[i].id}`;
        });
        bottom.appendChild(edit);
      }
    }

    reviewsList.appendChild(li);
  }
}

function colorStars (rating) {
  for (let i = rating; i > 0; i--) {
    const star = document.querySelector(`#star-${i} path`);
    star.style.fill = '#606060';
  }
  for (let i = rating + 1; i < 6; i++) {
    const star = document.querySelector(`#star-${i} path`);
    star.style.fill = '#dbdbdb';
  }
}

async function submitReview (token, title, text, rating, place_id) {
  /* Creating new review */
  const response = await fetch(`${API_URL}reviews/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, text, rating, place_id })
  });

  handleResponse(response, 'Review submitted successfully!', place_id);
}

async function editReview (token, title, text, rating, place_id, review_id) {
  /* Editing existing review */
  const response = await fetch(`${API_URL}reviews/${review_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, text, rating, place_id })
  });

  handleResponse(response, 'Review edited successfully!', place_id);
}

async function deleteReview (token, place_id, review_id) {
  /* Deleting existing review */
  const response = await fetch(`${API_URL}reviews/${review_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  handleResponse(response, 'Review deleted successfully!', place_id);
}

async function submitPlace (token, title, description, price, capacity, rooms, surface, latitude, longitude, list) {
  /* Submitting place form */
  const user = decodeJWT(token);
  const owner_id = user.id;
  const amenities = [];

  for (let i = 0; i < list.length; i++) {
    const amenity = { id: list[i] };
    amenities.push(amenity);
  }

  const response = await fetch(`${API_URL}places/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, description, price, capacity, rooms, surface, latitude, longitude, owner_id, amenities })
  });

  const data = await response.json();

  handleResponse(response, 'Place submitted successfully!', data.id);
}

async function editPlace (token, title, description, price, capacity, rooms, surface, latitude, longitude, list, place_id) {
  /* Editing existing place */
  const user = decodeJWT(token);
  const owner_id = user.id;
  const amenities = [];

  for (let i = 0; i < list.length; i++) {
    const amenity = { id: list[i] };
    amenities.push(amenity);
  }

  const response = await fetch(`${API_URL}places/${place_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, description, price, capacity, rooms, surface, latitude, longitude, owner_id, amenities })
  });

  handleResponse(response, 'Place edited successfully!', place_id);
}

async function deletePlace (token, place_id) {
  /* Deleting existing place */
  const response = await fetch(`${API_URL}places/${place_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  handleResponse(response, 'Place deleted successfully!');
}

async function handleResponse (response, successMessage, place_id) {
  if (response.ok) {
    alert(`${successMessage}`);
    if (place_id) {
      window.location.href = `place.html?place=${place_id}`;
    } else {
      window.location.href = 'index.html';
    }
  } else {
    const message = await response.json();
    alert(`Failure: ${message.error} (${response.statusText})`);
  }
}

function decodeJWT (token) {
  const response = JSON.parse(atob(token.split('.')[1]));
  return response.sub;
}

/* `http://maps.google.com/?ll=${},${}` */

const track = document.querySelector('.track');
const prev = document.querySelector('.prev');
const next = document.querySelector('.next');

let index = 0;
const images = document.querySelectorAll('.track img');
const width = 1430; // largeur d'une image

next.addEventListener('click', () => {
  index = (index + 1) % images.length;
  track.style.transform = `translateX(-${index * width}px)`;
});

prev.addEventListener('click', () => {
  index = (index - 1 + images.length) % images.length;
  track.style.transform = `translateX(-${index * width}px)`;
});