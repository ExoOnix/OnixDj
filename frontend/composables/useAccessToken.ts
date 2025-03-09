export const useAccessToken = () => {
    const token = ref("");

    const setToken = (value: string) => {
        token.value = value
    };

    return { token, setToken };
}
