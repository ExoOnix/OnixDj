export const useUser = () => {
    const { token } = useAccessToken(); // Get token from useAccessToken()


    const isLoggedIn = computed(() => token.value == ""); // Check if token exists

    return { isLoggedIn };
};
