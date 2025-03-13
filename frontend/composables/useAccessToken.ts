import { ref, onMounted } from 'vue';
import { jwtDecode } from 'jwt-decode';

const token = ref('');
let expirationTimer: ReturnType<typeof setTimeout> | null = null;

export const useAccessToken = () => {
    // Retrieve the token from the cookie on initial load
    const tokenCookie = useCookie('token');
    token.value = tokenCookie.value || '';

    // Function to set the token and manage its expiration
    const setToken = (value: string) => {
        token.value = value;
        tokenCookie.value = value; // Store the token in the cookie

        // Clear previous expiration timer if it exists
        if (expirationTimer) {
            clearTimeout(expirationTimer);
        }

        try {
            if (token.value !== '') {
                // Decode the token and get expiration time (assuming it's a JWT token)
                const decodedToken: any = jwtDecode(value);

                // Get expiration time from the decoded token (usually in 'exp' field)
                const expirationTime = decodedToken.exp * 1000; // Convert to milliseconds

                const currentTime = Date.now();
                const timeToExpire = expirationTime - currentTime - 60000; // Subtract 1 minute (60000 ms)

                // Set a new timer to refresh the token 1 minute before expiration
                if (timeToExpire > 0) {
                    expirationTimer = setTimeout(() => {
                        refreshToken();
                    }, timeToExpire);
                }
            }
        } catch (error) {
            setToken('');
        }
    };

    // Token refresh function
    const refreshToken = () => {
        fetch('/api/dj-rest-auth/token/refresh/', { credentials: 'include', method: 'POST' })
            .then(response => {
                if (!response.ok) {
                    setToken('');
                }
                return response.json(); // Parse the response as JSON
            })
            .then(data => {
                console.log(data.access)
                setToken(data.access);
            })
            .catch(error => {
                console.error('Fetch error:', error);
                setToken('');
            });
    };

    // Check token on mount and refresh if it's expired
    onMounted(() => {
        if (token.value != "") {
            try {
                const decodedToken: any = jwtDecode(token.value);
                const expirationTime = decodedToken.exp * 1000;
                const currentTime = Date.now();

                if (expirationTime < currentTime) {
                    // Token is expired, refresh it
                    refreshToken();
                } else {
                    // Token is still valid, set expiration timer
                    setToken(token.value);
                }
            } catch (error) {
                // If token is invalid, reset it and try to refresh
                setToken('');
                refreshToken();
            }
        }
        else {
            refreshToken()
        }
    });

    return { token, setToken, refreshToken };
};
