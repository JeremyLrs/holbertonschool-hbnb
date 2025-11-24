const API_BASE = "http://127.0.0.1:5000/api/v1";

function setCookie(name, value) {
    document.cookie = `${name}=${value}; path=/`;
}

function getCookie(name) {
    const c = document.cookie.split("; ").find(row => row.startsWith(name + "="));
    return c ? c.split("=")[1] : null;
}

function requireAuth() {
    const token = getCookie("token");
    if (!token) window.location.href = "login.html";
    return token;
}

document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;

    if (path.endsWith("login.html")) initLogin();
    if (path.endsWith("index.html")) initIndex();
    if (path.endsWith("place.html")) initPlace();
    if (path.endsWith("add_review.html")) initAddReview();
});

function initLogin() {
    const form = document.getElementById("login-form");
    form.addEventListener("submit", async e => {
        e.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const res = await fetch(API_BASE + "/auth/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password })
        });

        if (!res.ok) return alert("Invalid credentials");
        const data = await res.json();
        setCookie("token", data.access_token);
        window.location.href = "index.html";
    });
}

function initIndex() {
    const loginLink = document.getElementById("login-link");
    const token = getCookie("token");
    if (!token) loginLink.style.display = "block";
    else loginLink.style.display = "none";

    const priceFilter = document.getElementById("price-filter");
    ["All", 10, 50, 100].forEach(v => {
        const opt = document.createElement("option");
        opt.value = v;
        opt.textContent = v;
        priceFilter.appendChild(opt);
    });

    fetch(API_BASE + "/places")
        .then(r => r.json())
        .then(data => {
            if (!Array.isArray(data)) return;
            displayPlaces(data);

            priceFilter.addEventListener("change", () => {
                const max = priceFilter.value === "All" ? Infinity : Number(priceFilter.value);
                document.querySelectorAll(".place-card").forEach(card => {
                    const price = Number(card.dataset.price);
                    card.style.display = price <= max ? "block" : "none";
                });
            });
        });
}

function displayPlaces(places) {
    const container = document.getElementById("places-list");
    container.innerHTML = "";

    places.forEach(p => {
        const div = document.createElement("div");
        div.className = "place-card";
        div.dataset.price = p.price;
        div.innerHTML = `
            <h3>${p.title}</h3>
            <p>Price: ${p.price} €</p>
            <button class="details-button" onclick="window.location='place.html?id=${p.id}'">View Details</button>
        `;
        container.appendChild(div);
    });
}

function initPlace() {
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");

    fetch(API_BASE + "/places/" + placeId)
        .then(r => r.json())
        .then(place => displayPlace(place));

    fetch(API_BASE + "/places/" + placeId + "/reviews")
        .then(r => r.json())
        .then(reviews => displayReviews(reviews));
}

function displayPlace(place) {
    const c = document.getElementById("place-details");
    c.innerHTML = `
        <div class="place-details">
            <h2>${place.title}</h2>
            <p>${place.description}</p>
            <p>Price: ${place.price} €</p>
            <p>Amenities: ${place.amenities.map(a => a.name).join(", ")}</p>
        </div>
    `;
}

function displayReviews(reviews) {
    const c = document.getElementById("reviews");
    c.innerHTML = "";
    reviews.forEach(r => {
        const div = document.createElement("div");
        div.className = "review-card";
        const user = r.user || {};
        div.innerHTML = `
            <h4>${user.first_name || "User"} ${user.last_name || ""}</h4>
            <p>${r.text}</p>
            <p>Rating: ${r.rating}</p>
        `;
        c.appendChild(div);
    });
}

function initAddReview() {
    const token = requireAuth();

    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");

    const form = document.getElementById("review-form");

    const ratingSel = document.getElementById("rating");
    [1,2,3,4,5].forEach(n => {
        const o = document.createElement("option");
        o.value = n;
        o.textContent = n;
        ratingSel.appendChild(o);
    });

    form.addEventListener("submit", async e => {
        e.preventDefault();
        const text = document.getElementById("review").value;
        const rating = document.getElementById("rating").value;

        const res = await fetch(API_BASE + "/reviews", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                text: text,
                rating: rating,
                place_id: placeId
            })
        });

        if (!res.ok) return alert("Error submitting review");
        alert("Review submitted!");
        window.location.href = `place.html?id=${placeId}`;
    });
}
