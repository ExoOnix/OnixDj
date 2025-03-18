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