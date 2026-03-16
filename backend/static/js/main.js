// Main JavaScript file for GreenStay

// Global variables
let currentUser = null;
let token = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication status
    checkAuthStatus();
    
    // Setup event listeners
    setupEventListeners();
});

// Check if user is logged in
function checkAuthStatus() {
    token = localStorage.getItem('token');
    
    if (token) {
        // User is logged in
        try {
            currentUser = JSON.parse(localStorage.getItem('user'));
            updateNavigation(true);
            
            // Fetch latest user data
            fetchUserProfile();
        } catch (error) {
            console.error('Error parsing user data:', error);
            logout(); // Force logout if data is corrupted
        }
    } else {
        // User is not logged in
        updateNavigation(false);
    }
}

// Update navigation based on auth status
function updateNavigation(isLoggedIn) {
    const authElements = {
        loginLink: document.getElementById('loginLink'),
        registerLink: document.getElementById('registerLink'),
        profileLink: document.getElementById('profileLink'),
        bookingsLink: document.getElementById('bookingsLink'),
        messagesLink: document.getElementById('messagesLink'),
        logoutLink: document.getElementById('logoutLink')
    };
    
    if (isLoggedIn) {
        // Show authenticated nav items
        if (authElements.loginLink) authElements.loginLink.classList.add('hidden');
        if (authElements.registerLink) authElements.registerLink.classList.add('hidden');
        if (authElements.profileLink) authElements.profileLink.classList.remove('hidden');
        if (authElements.bookingsLink) authElements.bookingsLink.classList.remove('hidden');
        if (authElements.messagesLink) authElements.messagesLink.classList.remove('hidden');
        if (authElements.logoutLink) authElements.logoutLink.classList.remove('hidden');
    } else {
        // Show non-authenticated nav items
        if (authElements.loginLink) authElements.loginLink.classList.remove('hidden');
        if (authElements.registerLink) authElements.registerLink.classList.remove('hidden');
        if (authElements.profileLink) authElements.profileLink.classList.add('hidden');
        if (authElements.bookingsLink) authElements.bookingsLink.classList.add('hidden');
        if (authElements.messagesLink) authElements.messagesLink.classList.add('hidden');
        if (authElements.logoutLink) authElements.logoutLink.classList.add('hidden');
    }
}

// Fetch user profile data
function fetchUserProfile() {
    if (!token) return;
    
    fetch('/api/auth/profile', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch profile');
        }
        return response.json();
    })
    .then(userData => {
        currentUser = userData;
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Update UI with user data if needed
        const userNameElements = document.querySelectorAll('.user-name');
        userNameElements.forEach(el => {
            el.textContent = userData.username;
        });
    })
    .catch(error => {
        console.error('Error fetching user profile:', error);
        if (error.message === 'Failed to fetch profile') {
            // Token might be expired or invalid
            logout();
        }
    });
}

// Login function
function login(email, password) {
    return fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(data => {
        // Save auth data
        token = data.token;
        currentUser = data.user;
        
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(currentUser));
        
        updateNavigation(true);
        return data;
    });
}

// Register function
function register(userData) {
    return fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Registration failed');
        }
        return response.json();
    });
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    token = null;
    currentUser = null;
    updateNavigation(false);
    
    // Redirect to home if on a protected page
    const protectedPages = ['/profile', '/bookings', '/messages', '/become-host'];
    const currentPath = window.location.pathname;
    
    if (protectedPages.some(page => currentPath.startsWith(page))) {
        window.location.href = '/';
    }
}

// Fetch properties
function fetchProperties(filters = {}) {
    let queryString = Object.keys(filters)
        .filter(key => filters[key])
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(filters[key])}`)
        .join('&');
    
    const url = `/api/properties${queryString ? '?' + queryString : ''}`;
    
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch properties');
            }
            return response.json();
        });
}

// Fetch single property
function fetchProperty(propertyId) {
    return fetch(`/api/properties/${propertyId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch property');
            }
            return response.json();
        });
}

// Create booking
function createBooking(bookingData) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/bookings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(bookingData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Booking failed');
        }
        return response.json();
    });
}

// Fetch user bookings
function fetchUserBookings() {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/bookings', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch bookings');
        }
        return response.json();
    });
}

// Fetch host bookings
function fetchHostBookings() {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/bookings/host', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch host bookings');
        }
        return response.json();
    });
}

// Update booking status
function updateBookingStatus(bookingId, status) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch(`/api/bookings/${bookingId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ status })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update booking');
        }
        return response.json();
    });
}

// Cancel booking
function cancelBooking(bookingId) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch(`/api/bookings/${bookingId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to cancel booking');
        }
        return response.json();
    });
}

// Fetch property reviews
function fetchPropertyReviews(propertyId) {
    return fetch(`/api/reviews/property/${propertyId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch reviews');
            }
            return response.json();
        });
}

// Create review
function createReview(reviewData) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(reviewData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to create review');
        }
        return response.json();
    });
}

// Fetch conversations
function fetchConversations() {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/messages/conversations', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch conversations');
        }
        return response.json();
    });
}

// Fetch conversation messages
function fetchConversation(userId) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch(`/api/messages/conversation/${userId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch conversation');
        }
        return response.json();
    });
}

// Send message
function sendMessage(messageData) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(messageData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to send message');
        }
        return response.json();
    });
}

// Create property listing
function createProperty(propertyData) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/properties', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(propertyData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to create property');
        }
        return response.json();
    });
}

// Update property
function updateProperty(propertyId, propertyData) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch(`/api/properties/${propertyId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(propertyData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update property');
        }
        return response.json();
    });
}

// Delete property
function deleteProperty(propertyId) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch(`/api/properties/${propertyId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete property');
        }
        return response.json();
    });
}

// Update user profile
function updateProfile(profileData) {
    if (!token) {
        throw new Error('Authentication required');
    }
    
    return fetch('/api/auth/profile', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profileData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update profile');
        }
        return response.json();
    })
    .then(data => {
        // Update stored user data
        currentUser = data.user;
        localStorage.setItem('user', JSON.stringify(currentUser));
        return data;
    });
}

// Setup global event listeners
function setupEventListeners() {
    // Search form submission
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const location = document.getElementById('searchLocation').value;
            const checkIn = document.getElementById('searchCheckIn').value;
            const checkOut = document.getElementById('searchCheckOut').value;
            const guests = document.getElementById('searchGuests').value;
            
            let searchUrl = '/properties?';
            if (location) searchUrl += `location=${encodeURIComponent(location)}&`;
            if (checkIn) searchUrl += `check_in=${encodeURIComponent(checkIn)}&`;
            if (checkOut) searchUrl += `check_out=${encodeURIComponent(checkOut)}&`;
            if (guests) searchUrl += `guests=${encodeURIComponent(guests)}`;
            
            window.location.href = searchUrl;
        });
    }
    
    // Logout button
    const logoutButton = document.getElementById('logoutLink');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
}

// Format date for display
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Calculate number of nights between dates
function calculateNights(checkIn, checkOut) {
    const start = new Date(checkIn);
    const end = new Date(checkOut);
    const diffTime = Math.abs(end - start);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Show error message
function showError(message, elementId) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    } else {
        alert(message);
    }
}

// Show success message
function showSuccess(message, elementId) {
    const successElement = document.getElementById(elementId);
    if (successElement) {
        successElement.textContent = message;
        successElement.classList.remove('hidden');
    }
}

// Clear form fields
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

// Check if user is authenticated, redirect if not
function requireAuth() {
    if (!token) {
        window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
        return false;
    }
    return true;
}

// Generate star rating HTML
function generateStarRating(rating) {
    let starsHtml = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            starsHtml += '<i class="fas fa-star"></i>';
       
(Content truncated due to size limit. Use line ranges to read in chunks)