# Setup Guide

## Project structure
```
├── Makefile
├── backend # Backend folder
│   ├── OnixDj
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py # Settings file for django
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── requirements.txt # Requirements file for pip
│   └── users # Authentication api app
│       ├── __init__.py
│       ├── admin.py # Registers users to admin model
│       ├── apps.py
│       ├── forms.py # Modifies forms for custom user model
│       ├── managers.py # Custom user manager
│       ├── models.py # Custom user model
│       ├── serializers.py # Serializer overwrites for customizations
│       ├── tests.py # Custom user model tests
│       ├── urls.py
│       └── views.py # Custom user views
├── compose # Backend and frontend dockerfiles for different environments
│   ├── development
│   │   ├── backend
│   │   │   └── Dockerfile
│   │   └── frontend
│   │       └── Dockerfile
│   └── production
│       ├── backend
│       │   └── Dockerfile
│       └── frontend
│           └── Dockerfile
├── config
│   └── nginx.conf # Nginx config
├── docker-compose.dev.yaml # Dev compose
├── docker-compose.yaml # Prod compose
├── frontend # Frontend folder
│   ├── README.md
│   ├── app.vue # Root component
│   ├── assets
│   │   └── css
│   │       └── main.css
│   ├── components # Components folder
│   │   ├── page-specific # Page specific components
│   │   │   ├── auth # Auth related components
│   │   │   │   ├── LoginForm.vue
│   │   │   │   ├── RegisterForm.vue
│   │   │   │   ├── ResetPasswordEmailForm.vue
│   │   │   │   └── ResetPasswordForm.vue
│   │   │   └── navbar # Navbar component
│   │   │       └── Navbar.vue
│   │   └── ui # Shadcn components folder
│   │   │   └── ...
│   ├── components.json # Shadcn config
│   ├── lib
│   │   ├── ApiClient # Api client folder, auto generated.
│   │   │   └── ...
│   │   └── utils.ts
│   ├── nuxt.config.ts # Nuxt config
│   ├── openapitools.json
│   ├── package-lock.json
│   ├── package.json
│   ├── pages
│   │   ├── email # Email confirm page
│   │   │   └── confirm
│   │   │       └── [token].vue
│   │   ├── index.vue # Main page
│   │   ├── login # Login page
│   │   │   └── index.vue
│   │   ├── password-reset # Password reset page
│   │   │   ├── confirm
│   │   │   │   └── [uid]
│   │   │   │       └── [token].vue
│   │   │   └── index.vue
│   │   └── register # Register page
│   │       └── index.vue
│   ├── public
│   │   ├── favicon.ico
│   │   └── robots.txt
│   ├── server
│   │   ├── routes
│   │   │   └── auth
│   │   │       └── [...].js # Authjs providers config
│   │   └── tsconfig.json
│   ├── tailwind.config.js
│   └── tsconfig.json
└── readme.md
```

## Adding social providers

To add custom oauth providers you would need to do a number of steps.

1. **Setup backend**
    1. Go to backend/OnixDj/settings.py and add your relevant provider to INSTALLED_APPS:
    ```py
    # backend/OnixDj/settings.py
    INSTALLED_APPS = [
        # ...
        "allauth.socialaccount.providers.google",
    ]
    ```
    2. Write Oauth2 keys in env (Both environments):
    ```
    # .envs/production/.env and .envs/local/.env
    # ...
    GOOGLE_CLIENT_ID=<your id>
    GOOGLE_CLIENT_SECRET=<your secret>
    ```
    3. Write settings configuration:
    ```py
    # backend/OnixDj/settings.py
    SOCIALACCOUNT_PROVIDERS = {
        # ...
        "google": {
            "APP": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "key": "",  # leave empty
            },
            "SCOPE": [
                "profile",
                "email",
            ],
            "AUTH_PARAMS": {
                "access_type": "online",
            },
            "VERIFIED_EMAIL": True,
        },
    }

    ```
    4. Add the relevant view:
    ```py
    # backend/users/views.py
    from dj_rest_auth.registration.views import SocialLoginView
    from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client


    class GoogleLogin(SocialLoginView):
        adapter_class = GoogleOAuth2Adapter
        callback_url = settings.SITE_HOST
        client_class = OAuth2Client
    ```
    5. Add it to the urls.py to serve the view:
    ```py
    from users.views import (
        GoogleLogin,
    )

    urlpatterns = [
        path("dj-rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
    ]
    ```
2. **Setup frontend**
    1. Register the Google sign in handler in frontend/server/routes/auth/[...].js:
    ```js
    // frontend/server/routes/auth/[...].js
    const SIGN_IN_HANDLERS = {
        // ...
        "google": async (user, account, profile, email, credentials) => {
            try {
                const response = await fetch('http://backend:8000/api/dj-rest-auth/google/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({access_token: account.access_token}),
                });
                account["meta"] = response.json();
                return true;
            } catch (error) {
                console.error(error);
                return false;
            }
        }
    }
    ```
    2. add Google provider to the providers array:
    ```js
    // frontend/server/routes/auth/[...].js
    // ...
    import GoogleProvider from "next-auth/providers/google";
    // ...
    export default NuxtAuthHandler({
        // ...
        providers: [
            // ...
            GoogleProvider.default({
                clientId: process.env.GOOGLE_CLIENT_ID,
                clientSecret: process.env.GOOGLE_CLIENT_SECRET,
                authorization: {
                    params: {
                        prompt: "consent",
                        access_type: "offline",
                        response_type: "code"
                    }
                }
            }),
        ]

    })
    ```