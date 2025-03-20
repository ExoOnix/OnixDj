import CredentialsProvider from "next-auth/providers/credentials";
import GithubProvider from "next-auth/providers/github";

import { NuxtAuthHandler } from '#auth'

// These two values should be a bit less than actual token lifetimes
const BACKEND_ACCESS_TOKEN_LIFETIME = 4 * 60;            // 45 minutes
const BACKEND_REFRESH_TOKEN_LIFETIME = 0.8 * 24 * 60 * 60;  // 6 days

const getCurrentEpochTime = () => {
    return Math.floor(new Date().getTime() / 1000);
};

const SIGN_IN_HANDLERS = {
    "credentials": async (user, account, profile, email, credentials) => {
        return true;
    },
    "github": async (user, account, profile, email, credentials) => {
        try {
            const response = await fetch('http://backend:8000/api/dj-rest-auth/github/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({access_token: account.access_token}),
            });
            if (!response.ok) {
                throw new Error(JSON.stringify({ errors: "You are unable to sign up", status: false }))
            }
            const responseData = await response.json();
            account["meta"] = responseData;           
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }
};
const SIGN_IN_PROVIDERS = Object.keys(SIGN_IN_HANDLERS);

export default NuxtAuthHandler({
    // A secret string you define, to ensure correct encryption
    secret: process.env.FRONTEND_SECRET_KEY.toString(),
    session: {
        strategy: "jwt",
        maxAge: BACKEND_REFRESH_TOKEN_LIFETIME,
    },
    pages: {
        signIn: '/login',
    },

    providers: [
        CredentialsProvider.default({
            name: "Credentials",
            credentials: {
                email: { label: "Email", type: "email" },
                password: { label: "Password", type: "password" }
            },
            // The data returned from this function is passed forward as the
            // `user` variable to the signIn() and jwt() callback
            async authorize(credentials, req) {
                try {
                    const response = await fetch('http://backend:8000/api/dj-rest-auth/login/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(credentials),
                    });
                    if (response.ok) {
                        const data = await response.json();
                        if (data) return data;
                    }
                    else {
                        throw new Error(JSON.stringify({ errors: "Wrong username or password", status: false }))
                    }
                } catch (error) {
                    console.error(error);
                }
                return null;
            },
        }),
        GithubProvider.default({
            clientId: process.env.GITHUB_CLIENT_ID,
            clientSecret: process.env.GITHUB_CLIENT_SECRET,
            authorization: {
                params: {
                    prompt: "consent",
                    access_type: "offline",
                    response_type: "code"
                }
            }
        }),
    ],
    callbacks: {
        async signIn({ user, account, profile, email, credentials }) {
            if (!SIGN_IN_PROVIDERS.includes(account.provider)) return false;
            return SIGN_IN_HANDLERS[account.provider](
                user, account, profile, email, credentials
            );
        },
        async jwt({ user, token, account }) {
            // If `user` and `account` are set that means it is a login event
            if (user && account) {
                let backendResponse = account.provider === "credentials" ? user : account.meta;
                token["user"] = backendResponse.user;
                token["access_token"] = backendResponse.access;
                token["refresh_token"] = backendResponse.refresh;
                token["ref"] = getCurrentEpochTime() + BACKEND_ACCESS_TOKEN_LIFETIME;
                
                return token;
            }
            // Refresh the backend token if necessary
            if (getCurrentEpochTime() > token["ref"]) {
                const response = await fetch('http://backend:8000/api/dj-rest-auth/token/refresh/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({refresh: token["refresh_token"]}),
                });
                const data = await response.json();
                token["access_token"] = data.access;
                token["refresh_token"] = data.refresh;
                token["ref"] = getCurrentEpochTime() + BACKEND_ACCESS_TOKEN_LIFETIME;
            }
            return token;
        },
        // Since we're using Django as the backend we have to pass the JWT
        // token to the client instead of the `session`.
        async session({ token }) {
            return token;
        },
    }
})