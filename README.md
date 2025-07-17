#  Freelance Marketplace API

This is a backend REST API for a Freelance Job Marketplace, built using Django and Django REST Framework.

It supports two types of users: **Clients** and **Freelancers**. Clients can post jobs, and Freelancers can create profiles and send proposals for jobs.

---

## 📦 Features

- ✅ **User Signup & Login**
- ✅ **Role-based Users** (Client or Freelancer)
- ✅ **Freelancer Profiles**
- ✅ **Job Posting** by Clients
- ✅ **Proposals** submitted by Freelancers
- ✅ **JWT Authentication**
- ✅ **Permissions** for accessing/modifying jobs or proposals
- ✅ **Basic Unit Testing**

---

## 👥 User Roles

### 1. Client
- Can post jobs
- Can view proposals from freelancers

### 2. Freelancer
- Can create a profile (with hourly rate)
- Can browse all jobs
- Can send proposals to any job

---

## 🔑 Authentication

This API uses **JWT (JSON Web Token)** authentication.

- After login, users receive a token
- They must include this token in the header for protected routes:

