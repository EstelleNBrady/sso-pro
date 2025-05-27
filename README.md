SSO Dashboard – Flask, AWS Cognito, and Slack OAuth
This project is a lightweight, extensible single sign-on (SSO) platform designed to centralize authentication and app access. It currently supports authentication via AWS Cognito and OAuth-based login with Slack. Built with Flask for flexibility and speed of development, this platform serves as a foundation for a scalable SSO experience.

Overview
This application provides:

SSO Authentication through AWS Cognito
Users authenticate securely via AWS Cognito, which manages login flows, tokens, and session handling.

Slack OAuth Integration
Users can connect their Slack account and view user-specific Slack data upon successful authorization.

Custom Dashboard
A simple HTML/CSS interface shows connected applications and allows users to initiate SSO flows from a single place.

Technologies
Flask (Python)

AWS Cognito (OIDC provider)

Slack OAuth 2.0

HTML/CSS (Jinja templating)

dotenv for environment configuration

ngrok (for local testing with public URLs)

[User] --> [Flask Login] --> [Cognito Hosted UI]
         <-- Auth Code & Tokens --
         --> /dashboard (session stored)
            |
            --> Slack OAuth Login
                |
                --> Slack Access Token
                    |
                    --> Slack API

Features
Secure user login through AWS Cognito

Slack OAuth integration to display user ID and name

Clean dashboard UI for future application expansion

In Progress
AWS Lambda + API Gateway Integration (in development):
Slack token handling is being migrated to AWS Lambda behind API Gateway for a more scalable and serverless architecture.

Expanded Slack Functionality:
Plan to display additional Slack data, such as unread messages or user profile information.

Additional Application Integrations:
Gmail OAuth and others may be integrated as additional services in the dashboard.

Frontend Modernization:
Long-term goal includes moving the frontend to a static S3 site backed by Lambda APIs.

Why Flask and Cognito?
Flask allowed rapid prototyping and flexibility for early development. AWS Cognito was chosen for its secure, standards-based identity management, seamless session handling, and future integration potential across AWS services. Together, they enable quick iteration with enterprise-level security.

Future Work
Finalize Lambda + API Gateway routing for Slack data requests

Introduce multiple connected apps with unified user insight

Optional: Deploy front end to S3 + CloudFront for full cloud-native architecture