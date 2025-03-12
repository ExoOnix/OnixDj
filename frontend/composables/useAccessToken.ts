import { ref } from 'vue';
import { jwtDecode } from "jwt-decode";

const token = ref(""); // Global state
let expirationTimer: ReturnType<typeof setTimeout> | null = null;


export const useAccessToken = () => {
    const setToken = (value: string) => {
        token.value = value;

        // Clear previous expiration timer if it exists
        if (expirationTimer) {
            clearTimeout(expirationTimer);
        }

        try {
            if (token.value != "") {
                // Decode the token and get expiration time (assuming it's a JWT token)
                const decodedToken: any = jwtDecode(value);

                // Get expiration time from the decoded token (usually in 'exp' field)
                const expirationTime = decodedToken.exp * 1000; // Convert to milliseconds

                const currentTime = Date.now();
                const timeToExpire = expirationTime - currentTime - 60000; // Subtract 1 minute (60000 ms)
                console.log(timeToExpire)
                // Set a new timer to log a message 1 minute before expiration
                if (timeToExpire > 0) {
                    expirationTimer = setTimeout(() => {
                        fetch('/api/dj-rest-auth/token/refresh/', { credentials: 'include', method: 'POST' })
                            .then(response => {
                                if (!response.ok) {
                                    setToken("")
                                    throw new Error(`HTTP error! Status: ${response.status}`);
                                }
                                return response.json(); // Parse the response as JSON
                            })
                            .then(data => {
                                console.log(data.access); // Handle the data from the response
                                setToken(data.access)
                            })
                            .catch(error => {
                                console.error('Fetch error:', error);
                                setToken("")
                            });
                    }, timeToExpire);
                }
            }
        } catch (error) {
            setToken("")
        }
    };

    return { token, setToken };
};
